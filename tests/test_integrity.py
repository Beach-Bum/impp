"""Tests for the full-coverage artifact integrity digest.

The content address (``hash``) covers four fields. The integrity digest
covers every field. These tests walk a serialized artifact generically and
change one thing at a time, so a field added to the schema later is covered
by the tests without anyone remembering to add it here.
"""

import copy
import hashlib
import json

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from amm.artifact.schema import (
    MemoryArtifact,
    ArtifactDomain,
    ArtifactKnowledge,
    ArtifactProvenance,
    ArtifactAttestation,
    ArtifactCard,
    ConflictDeclaration,
    EvaluationSuite,
    SourceMaterial,
    integrity_digest,
)
from amm.verification.certificate import VerificationCertificate, generate_certificate


def make_artifact() -> MemoryArtifact:
    """An artifact with every nested structure populated."""
    return MemoryArtifact(
        domain=ArtifactDomain(category="DeFi", subcategory="risk-assessment"),
        knowledge=ArtifactKnowledge(
            format="markdown",
            content="Check the oracle before the collateral ratio.",
            sections=["calibration", "heuristics"],
            token_count=8,
        ),
        provenance=ArtifactProvenance(
            agent_id="test-agent-001",
            model="test-model",
            training_rounds=20,
            training_items=["AlphaLend", "YieldMaxi"],
            created_at="2026-01-01T00:00:00+00:00",
            license="MIT",
            source_material=[SourceMaterial(name="corpus", url="https://example.org", license="MIT")],
        ),
        attestation=ArtifactAttestation(
            expert_avg_error=3.25,
            transfer_efficiency_pct=92.2,
            eval_items_count=8,
            trials=3,
            evaluation_suite=EvaluationSuite(name="defi", version="1", held_out_count=12, benchmark_hash="abc"),
        ),
        artifact_type="procedural",
        card=ArtifactCard(intended_use="risk triage", contraindications=["legal advice"]),
        conflicts=[ConflictDeclaration(artifact="deadbeef", reason="contradicts")],
    )


def _changed(value):
    """A value of the same JSON type that differs from ``value``."""
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 0.5
    if isinstance(value, str):
        return value + "x"
    raise TypeError(f"unexpected leaf type: {type(value)}")


def single_mutations(node, path=()):
    """Yield (path, mutate) for every single change that can be made to a
    JSON-like structure: each leaf altered, each key removed, each list
    lengthened and shortened. ``mutate(root)`` applies the change in place."""

    def at(root, p):
        for step in p:
            root = root[step]
        return root

    if isinstance(node, dict):
        for key, child in node.items():
            yield path + (key, "<removed>"), lambda root, p=path, k=key: at(root, p).pop(k)
            yield from single_mutations(child, path + (key,))
        yield path + ("<added key>",), lambda root, p=path: at(root, p).update({"injected": 1})
    elif isinstance(node, list):
        for i, child in enumerate(node):
            yield from single_mutations(child, path + (i,))
        yield path + ("<appended>",), lambda root, p=path: at(root, p).append("injected")
        if node:
            yield path + ("<truncated>",), lambda root, p=path: at(root, p).pop()
    else:
        def set_leaf(root, p=path, old=node):
            at(root, p[:-1])[p[-1]] = _changed(old)

        yield path, set_leaf


def test_walker_reaches_every_section():
    """Guard the test itself: the generic walk must reach every part of the artifact."""
    data = make_artifact().seal().to_dict()
    paths = [p for p, _ in single_mutations(data)]
    top_level = {p[0] for p in paths}
    assert top_level >= {
        "domain", "knowledge", "provenance", "attestation", "version", "hash",
        "artifact_type", "attach", "card", "privacy", "conflicts", "revocation",
        "integrity",
    }
    assert ("attestation", "transfer_efficiency_pct") in paths
    assert ("attestation", "evaluation_suite", "benchmark_hash") in paths
    assert ("provenance", "source_material", 0, "url") in paths
    assert len(paths) > 80


def test_sealed_artifact_round_trips():
    artifact = make_artifact().seal()
    assert artifact.integrity.startswith("sha256:")
    assert artifact.integrity_status() == "verified"
    assert artifact.validate() == []

    restored = MemoryArtifact.from_json(artifact.to_json())
    assert restored.integrity == artifact.integrity
    assert restored.integrity_status() == "verified"
    assert restored.to_dict() == artifact.to_dict()


def test_every_single_change_to_a_sealed_artifact_is_rejected():
    """Change one thing at a time, everywhere; each must fail to load."""
    original = make_artifact().seal().to_dict()
    checked = 0
    for path, mutate in single_mutations(original):
        if path == ("integrity", "<removed>"):
            # Stripping the digest turns the file into an old-format artifact,
            # which must still load. That downgrade is caught by the signed
            # certificate instead: see
            # test_certificate_detects_change_outside_the_content_hash.
            continue
        data = copy.deepcopy(original)
        mutate(data)
        assert data != original, f"mutation at {path} changed nothing"
        with pytest.raises(ValueError, match="tampered"):
            MemoryArtifact.from_dict(data)
        checked += 1
    assert checked > 80


def test_fields_outside_the_content_hash_were_previously_unprotected():
    """The defect being fixed: without the digest, editing the measured
    results goes unnoticed; with it, the same edit is rejected."""
    unsealed = make_artifact().to_dict()
    unsealed["attestation"]["transfer_efficiency_pct"] = 99.9
    loaded = MemoryArtifact.from_dict(unsealed)  # loads: hash does not cover it
    assert loaded.attestation.transfer_efficiency_pct == 99.9
    assert loaded.integrity_status() == "absent"

    sealed = make_artifact().seal().to_dict()
    sealed["attestation"]["transfer_efficiency_pct"] = 99.9
    with pytest.raises(ValueError, match="Integrity digest mismatch"):
        MemoryArtifact.from_dict(sealed)


def test_in_memory_change_after_sealing_is_reported():
    artifact = make_artifact().seal()
    artifact.attestation.trials = 300
    assert artifact.integrity_status() == "mismatch"
    assert not artifact.verify_integrity()
    assert "Integrity digest check failed" in artifact.validate()


def test_content_hash_is_unchanged_by_the_digest():
    """The content address keeps its old definition and value."""
    artifact = make_artifact()
    expected = hashlib.sha256(
        (
            "DeFi:risk-assessment"
            "|Check the oracle before the collateral ratio."
            "|test-agent-001"
            "|2026-01-01T00:00:00+00:00"
        ).encode("utf-8")
    ).hexdigest()
    assert artifact.hash == expected
    assert artifact.seal().hash == expected


def test_old_format_artifact_without_digest_still_loads():
    """A v0.1-style file: no integrity field, no v0.2 sections."""
    created_at = "2025-06-01T00:00:00+00:00"
    content = "Old knowledge"
    old_hash = hashlib.sha256(f"DeFi:risk-assessment|{content}|agent-old|{created_at}".encode()).hexdigest()
    old = {
        "version": "0.1.0",
        "domain": {"category": "DeFi", "subcategory": "risk-assessment", "scope": "protocol-level"},
        "knowledge": {"format": "markdown", "content": content, "sections": [], "token_count": 2},
        "provenance": {
            "agent_id": "agent-old",
            "model": "old-model",
            "training_rounds": 5,
            "training_items": [],
            "created_at": created_at,
            "experiment_version": "0.1.0",
        },
        "attestation": {"expert_avg_error": 4.0, "transfer_efficiency_pct": 50.0, "eval_items_count": 8, "trials": 3},
        "hash": old_hash,
    }
    artifact = MemoryArtifact.from_dict(old)
    assert artifact.hash == old_hash
    assert artifact.integrity == ""
    assert artifact.integrity_status() == "absent"
    assert artifact.verify_integrity()
    assert artifact.validate() == []


def test_unsealed_artifact_serializes_without_integrity_key():
    """Unsealed output is what it was before the digest existed."""
    assert "integrity" not in make_artifact().to_dict()


def test_from_dict_does_not_modify_its_input():
    data = make_artifact().seal().to_dict()
    snapshot = copy.deepcopy(data)
    MemoryArtifact.from_dict(data)
    assert data == snapshot
    MemoryArtifact.from_dict(data)  # and can therefore be loaded twice


def test_digest_is_independent_of_key_order_and_whitespace():
    data = make_artifact().to_dict()
    reordered = json.loads(json.dumps(dict(reversed(list(data.items()))), indent=7))
    assert integrity_digest(reordered) == integrity_digest(data)


# ── Binding the digest to the signed certificate ──────────────────────


ADVERSARIAL = {
    "aggregate_score": 15.0,
    "bias_score": 10.0,
    "consistency_score": 20.0,
    "stego_score": 15.0,
    "overfit_score": 10.0,
    "verdict": "PASS",
    "all_flags": [],
}


def _certificate_for(artifact, key, with_digest=True):
    return generate_certificate(
        artifact_hash=artifact.hash,
        benchmark_info={"id": "bench-1", "domain": "defi"},
        results={"transfer_efficiency_pct": 85.0},
        adversarial=ADVERSARIAL,
        trust_score=82.5,
        referee_model="test-model",
        signing_key=key,
        artifact_integrity=artifact.compute_integrity() if with_digest else "",
    )


def test_certificate_detects_change_outside_the_content_hash():
    """Removing the digest from the artifact file does not help an attacker:
    the certificate carries its own signed copy."""
    key = Ed25519PrivateKey.generate()
    artifact = make_artifact().seal()
    cert = _certificate_for(artifact, key)
    assert cert.matches_artifact(artifact)

    data = artifact.to_dict()
    data.pop("integrity")  # strip the digest so the file loads as "old format"
    data["attestation"]["transfer_efficiency_pct"] = 99.9
    forged = MemoryArtifact.from_dict(data)
    assert forged.hash == artifact.hash  # content address is blind to the edit
    assert not cert.matches_artifact(forged)

    # Re-sealing the forgery does not help either
    assert not cert.matches_artifact(forged.seal())


def test_certificate_digest_is_covered_by_the_signature():
    key = Ed25519PrivateKey.generate()
    artifact = make_artifact()
    cert = _certificate_for(artifact, key)
    assert cert.verify_signature(key.public_key())

    forged = make_artifact()
    forged.attestation.transfer_efficiency_pct = 99.9
    cert.artifact_integrity = forged.compute_integrity()
    assert not cert.verify_signature(key.public_key())


def test_certificate_without_digest_is_unchanged():
    """Certificates issued before the digest existed keep their serialized
    form and signed payload, so their signatures still verify."""
    key = Ed25519PrivateKey.generate()
    artifact = make_artifact()
    cert = _certificate_for(artifact, key, with_digest=False)
    d = cert.to_dict()
    assert "artifact_integrity" not in d
    assert set(d) == {
        "id", "version", "artifact_hash", "benchmark", "results", "adversarial",
        "trust_score", "issued_at", "expires_at", "referee_model", "signature",
    }
    restored = VerificationCertificate.from_json(cert.to_json())
    assert restored.verify_signature(key.public_key())
    assert restored.matches_artifact(artifact)  # content address only

    other = make_artifact()
    other.knowledge.content = "something else"
    other.hash = other.compute_hash()
    assert not restored.matches_artifact(other)

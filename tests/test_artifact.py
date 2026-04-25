"""Tests for the artifact schema."""

from amm.artifact.schema import (
    MemoryArtifact,
    ArtifactDomain,
    ArtifactKnowledge,
    ArtifactProvenance,
    ArtifactAttestation,
)


def make_test_artifact(content="Test artifact content") -> MemoryArtifact:
    """Create a test artifact."""
    return MemoryArtifact(
        domain=ArtifactDomain(category="DeFi", subcategory="risk-assessment"),
        knowledge=ArtifactKnowledge(
            format="markdown",
            content=content,
            sections=["calibration", "heuristics"],
            token_count=100,
        ),
        provenance=ArtifactProvenance(
            agent_id="test-agent-001",
            model="claude-sonnet-4-20250514",
            training_rounds=20,
            training_items=["AlphaLend", "YieldMaxi"],
        ),
        attestation=ArtifactAttestation(
            expert_avg_error=3.25,
            transfer_efficiency_pct=92.2,
            eval_items_count=8,
            trials=3,
        ),
    )


def test_artifact_creation():
    artifact = make_test_artifact()
    assert artifact.hash
    assert len(artifact.hash) == 64  # SHA-256 hex


def test_artifact_serialization():
    artifact = make_test_artifact()
    json_str = artifact.to_json()
    restored = MemoryArtifact.from_json(json_str)
    assert restored.hash == artifact.hash
    assert restored.knowledge.content == artifact.knowledge.content


def test_artifact_hash_deterministic():
    a1 = make_test_artifact("same content")
    a2 = MemoryArtifact(
        domain=a1.domain,
        knowledge=ArtifactKnowledge(format="markdown", content="same content"),
        provenance=ArtifactProvenance(
            agent_id=a1.provenance.agent_id,
            model=a1.provenance.model,
            created_at=a1.provenance.created_at,
        ),
        attestation=a1.attestation,
    )
    assert a1.hash == a2.hash


def test_artifact_hash_changes_with_content():
    a1 = make_test_artifact("content A")
    a2 = make_test_artifact("content B")
    assert a1.hash != a2.hash


def test_artifact_validation():
    artifact = make_test_artifact()
    issues = artifact.validate()
    assert len(issues) == 0


def test_artifact_validation_empty_content():
    artifact = make_test_artifact("")
    issues = artifact.validate()
    assert any("empty" in i for i in issues)


def test_artifact_tamper_detection():
    artifact = make_test_artifact()
    json_str = artifact.to_json()

    # Tamper with content
    import json
    data = json.loads(json_str)
    data["knowledge"]["content"] = "TAMPERED"

    try:
        MemoryArtifact.from_dict(data)
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "tampered" in str(e).lower()

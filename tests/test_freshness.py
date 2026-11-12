"""Tests that the trust score uses the artifact's real freshness.

The benchmark and the adversarial probes are replaced with fixed results,
so no model is called and nothing touches the network.
"""

from datetime import datetime, timedelta, timezone

import pytest

import amm.verification.certificate as certificate_module
import amm.verification.referee as referee
from amm.artifact.schema import (
    MemoryArtifact,
    ArtifactDomain,
    ArtifactKnowledge,
    ArtifactProvenance,
    ArtifactAttestation,
)
from amm.benchmark.sandbox import AssessmentResult
from amm.domains import get_domain
from amm.registry.trust import compute_freshness_pct
from amm.verification.referee import compute_trust_score, verify_artifact

TE = 80.0
ADVERSARIAL_SCORE = 10.0


def artifact_aged(days: float) -> MemoryArtifact:
    created = datetime.now(timezone.utc) - timedelta(days=days)
    return MemoryArtifact(
        domain=ArtifactDomain(category="DeFi", subcategory="risk-assessment"),
        knowledge=ArtifactKnowledge(format="markdown", content="Some knowledge"),
        provenance=ArtifactProvenance(
            agent_id="agent-1", model="test-model", created_at=created.isoformat()
        ),
        attestation=ArtifactAttestation(),
    )


@pytest.fixture
def offline_referee(monkeypatch, tmp_path):
    """Replace every step of verify_artifact that would call a model."""

    def fake_benchmark(client, domain, artifact_content, model, novice_cache):
        return {
            "metrics": {
                "transfer_efficiency_pct": TE,
                "buyer_avg_error": 2.0,
                "novice_avg_error": 10.0,
            },
            "buyer_results": [
                AssessmentResult(protocol="p0", agent_score=52, true_score=50, error=2,
                                 reasoning="", confidence="high", red_flags=[])
            ],
        }

    def fake_probes(**kwargs):
        return {
            "aggregate_score": ADVERSARIAL_SCORE,
            "bias_score": 10.0,
            "consistency_score": 10.0,
            "stego_score": 10.0,
            "overfit_score": 10.0,
            "verdict": "PASS",
            "all_flags": [],
        }

    monkeypatch.setattr(referee, "run_verification_benchmark", fake_benchmark)
    monkeypatch.setattr(referee, "run_all_probes", fake_probes)
    # No signing key on disk: keeps the test independent of the machine
    monkeypatch.setattr(certificate_module, "CERTS_DIR", tmp_path / "certs")
    return object()  # stands in for the API client; never used


def test_freshness_decay_curve():
    assert compute_freshness_pct(datetime.now(timezone.utc).isoformat()) == pytest.approx(100.0, abs=0.1)
    half_life_ago = (datetime.now(timezone.utc) - timedelta(days=180)).isoformat()
    assert compute_freshness_pct(half_life_ago) == pytest.approx(50.0, abs=0.1)
    two_half_lives_ago = (datetime.now(timezone.utc) - timedelta(days=360)).isoformat()
    assert compute_freshness_pct(two_half_lives_ago) == pytest.approx(25.0, abs=0.1)
    future = (datetime.now(timezone.utc) + timedelta(days=30)).isoformat()
    assert compute_freshness_pct(future) == 100.0


def test_new_artifact_scores_as_before(offline_referee):
    cert = verify_artifact(artifact_aged(0), get_domain("defi"), client=offline_referee)
    assert cert.results["freshness_pct"] == pytest.approx(100.0, abs=0.1)
    # 0.5 * 80 + 0.3 * (100 - 10) + 0.2 * 100
    assert cert.trust_score == pytest.approx(87.0, abs=0.1)


def test_old_artifact_scores_lower(offline_referee):
    cert = verify_artifact(artifact_aged(180), get_domain("defi"), client=offline_referee)
    assert cert.results["freshness_pct"] == pytest.approx(50.0, abs=0.1)
    # 0.5 * 80 + 0.3 * (100 - 10) + 0.2 * 50
    assert cert.trust_score == pytest.approx(77.0, abs=0.1)
    assert cert.trust_score == pytest.approx(
        compute_trust_score(TE, ADVERSARIAL_SCORE, freshness_pct=cert.results["freshness_pct"]), abs=0.05
    )


def test_trust_score_falls_monotonically_with_age(offline_referee):
    scores = [
        verify_artifact(artifact_aged(days), get_domain("defi"), client=offline_referee).trust_score
        for days in (0, 30, 180, 720)
    ]
    assert scores == sorted(scores, reverse=True)
    assert len(set(scores)) == len(scores)


def test_certificate_carries_artifact_integrity(offline_referee):
    artifact = artifact_aged(1)
    cert = verify_artifact(artifact, get_domain("defi"), client=offline_referee)
    assert cert.artifact_integrity == artifact.compute_integrity()
    assert cert.matches_artifact(artifact)


def test_bad_timestamp_fails_before_the_benchmark_runs(monkeypatch, offline_referee):
    def must_not_run(**kwargs):
        raise AssertionError("benchmark ran despite an unreadable created_at")

    monkeypatch.setattr(referee, "run_verification_benchmark", must_not_run)
    artifact = artifact_aged(0)
    artifact.provenance.created_at = "not a timestamp"
    artifact.hash = artifact.compute_hash()
    with pytest.raises(ValueError):
        verify_artifact(artifact, get_domain("defi"), client=offline_referee)

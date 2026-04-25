"""Tests for Ed25519 certificate signing and verification."""

import json
import tempfile
from pathlib import Path

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

from amm.verification.certificate import (
    VerificationCertificate,
    generate_certificate,
    generate_keypair,
    load_private_key,
    load_public_key,
)


@pytest.fixture
def sample_adversarial():
    return {
        "aggregate_score": 15.0,
        "bias_score": 10.0,
        "consistency_score": 20.0,
        "stego_score": 15.0,
        "overfit_score": 10.0,
        "verdict": "PASS",
        "all_flags": [],
    }


@pytest.fixture
def sample_cert(sample_adversarial):
    return generate_certificate(
        artifact_hash="abc123def456",
        benchmark_info={"id": "bench-1", "domain": "defi"},
        results={"transfer_efficiency_pct": 85.0},
        adversarial=sample_adversarial,
        trust_score=82.5,
        referee_model="claude-sonnet-4-20250514",
        signing_key=None,
    )


@pytest.fixture
def keypair(tmp_path):
    priv_path, pub_path = generate_keypair(tmp_path)
    return priv_path, pub_path


class TestKeypairGeneration:
    def test_generates_key_files(self, keypair):
        priv_path, pub_path = keypair
        assert priv_path.exists()
        assert pub_path.exists()

    def test_private_key_permissions(self, keypair):
        priv_path, _ = keypair
        mode = priv_path.stat().st_mode & 0o777
        assert mode == 0o600

    def test_load_roundtrip(self, keypair):
        priv_path, pub_path = keypair
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)
        # Sign and verify with loaded keys
        msg = b"test message"
        sig = priv.sign(msg)
        pub.verify(sig, msg)  # Raises if invalid


class TestCertificateSigning:
    def test_sign_and_verify(self, sample_cert, keypair):
        priv_path, pub_path = keypair
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        sample_cert.sign(priv)
        assert sample_cert.signature != ""
        assert sample_cert.verify_signature(pub)

    def test_tampered_cert_fails(self, sample_cert, keypair):
        priv_path, pub_path = keypair
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        sample_cert.sign(priv)
        sample_cert.trust_score = 99.9  # Tamper
        assert not sample_cert.verify_signature(pub)

    def test_wrong_key_fails(self, sample_cert, keypair, tmp_path):
        priv_path, _ = keypair
        priv = load_private_key(priv_path)
        sample_cert.sign(priv)

        # Generate a different keypair
        other_dir = tmp_path / "other"
        other_dir.mkdir()
        _, other_pub_path = generate_keypair(other_dir)
        other_pub = load_public_key(other_pub_path)
        assert not sample_cert.verify_signature(other_pub)

    def test_unsigned_cert_fails_verify(self, sample_cert, keypair):
        _, pub_path = keypair
        pub = load_public_key(pub_path)
        assert not sample_cert.verify_signature(pub)

    def test_json_roundtrip_preserves_signature(self, sample_cert, keypair):
        priv_path, pub_path = keypair
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        sample_cert.sign(priv)
        json_str = sample_cert.to_json()

        restored = VerificationCertificate.from_json(json_str)
        assert restored.signature == sample_cert.signature
        assert restored.verify_signature(pub)


class TestGenerateCertificateAutoSign:
    def test_auto_signs_with_key(self, sample_adversarial, keypair):
        priv_path, pub_path = keypair
        priv = load_private_key(priv_path)
        pub = load_public_key(pub_path)

        cert = generate_certificate(
            artifact_hash="xyz789",
            benchmark_info={"id": "bench-2", "domain": "cybersec"},
            results={"transfer_efficiency_pct": 90.0},
            adversarial=sample_adversarial,
            trust_score=88.0,
            referee_model="claude-sonnet-4-20250514",
            signing_key=priv,
        )
        assert cert.signature != ""
        assert cert.verify_signature(pub)

    def test_no_key_produces_unsigned(self, sample_adversarial):
        cert = generate_certificate(
            artifact_hash="xyz789",
            benchmark_info={"id": "bench-2", "domain": "cybersec"},
            results={"transfer_efficiency_pct": 90.0},
            adversarial=sample_adversarial,
            trust_score=88.0,
            referee_model="claude-sonnet-4-20250514",
            signing_key=None,
        )
        # No key on disk = unsigned
        assert cert.signature == ""

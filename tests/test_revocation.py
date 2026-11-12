"""Tests that a revoked certificate is actually refused."""

import json

import pytest
from click.testing import CliRunner
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

import amm.verification.certificate as certificate_module
from amm.cli import cli
from amm.verification.certificate import (
    check_revocation,
    generate_certificate,
    generate_keypair,
    load_crl,
    load_private_key,
    revoke_certificate,
    verify_certificate,
)

ADVERSARIAL = {
    "aggregate_score": 15.0,
    "bias_score": 10.0,
    "consistency_score": 20.0,
    "stego_score": 15.0,
    "overfit_score": 10.0,
    "verdict": "PASS",
    "all_flags": [],
}


def make_cert(key, expiry_days=90):
    return generate_certificate(
        artifact_hash="abc123def456",
        benchmark_info={"id": "bench-1", "domain": "defi"},
        results={"transfer_efficiency_pct": 85.0},
        adversarial=ADVERSARIAL,
        trust_score=82.5,
        referee_model="test-model",
        signing_key=key,
        expiry_days=expiry_days,
    )


@pytest.fixture
def key():
    return Ed25519PrivateKey.generate()


def test_missing_revocation_list_means_not_revoked(key, tmp_path):
    crl = tmp_path / "does-not-exist.json"
    cert = make_cert(key)
    assert load_crl(crl) == []
    assert check_revocation(cert.id, crl) is False
    result = verify_certificate(cert, key.public_key(), crl_path=crl)
    assert result.valid and result.status == "valid"


def test_not_revoked_certificate_passes(key, tmp_path):
    crl = tmp_path / "crl.json"
    cert, other = make_cert(key), make_cert(key)
    revoke_certificate(other.id, crl_path=crl)  # someone else's certificate
    result = verify_certificate(cert, key.public_key(), crl_path=crl)
    assert result.valid


def test_revoked_certificate_is_refused(key, tmp_path):
    crl = tmp_path / "crl.json"
    cert = make_cert(key)
    assert verify_certificate(cert, key.public_key(), crl_path=crl).valid

    revoke_certificate(cert.id, reason="benchmark leak", crl_path=crl)

    assert cert.verify_signature(key.public_key())  # the signature is still good
    assert not cert.is_expired()
    result = verify_certificate(cert, key.public_key(), crl_path=crl)
    assert not result.valid
    assert result.status == "revoked"
    assert "benchmark leak" in result.reason


def test_revocation_takes_precedence_over_other_failures(key, tmp_path):
    crl = tmp_path / "crl.json"
    cert = make_cert(key, expiry_days=-1)
    assert verify_certificate(cert, key.public_key(), crl_path=crl).status == "expired"
    revoke_certificate(cert.id, crl_path=crl)
    assert verify_certificate(cert, key.public_key(), crl_path=crl).status == "revoked"


def test_other_refusals(key, tmp_path):
    crl = tmp_path / "crl.json"
    wrong_key = Ed25519PrivateKey.generate().public_key()
    cert = make_cert(key)
    assert verify_certificate(cert, wrong_key, crl_path=crl).status == "signature_invalid"

    cert.trust_score = 99.0  # edited after signing
    assert verify_certificate(cert, key.public_key(), crl_path=crl).status == "signature_invalid"


# ── The CLI `impp verify` path ────────────────────────────────────────


@pytest.fixture
def cli_setup(tmp_path, monkeypatch):
    """A signed certificate on disk, its public key, and an isolated CRL."""
    priv_path, pub_path = generate_keypair(tmp_path / "keys")
    cert = make_cert(load_private_key(priv_path))
    cert_path = tmp_path / "certificate.json"
    cert_path.write_text(cert.to_json())
    crl = tmp_path / "crl.json"
    monkeypatch.setattr(certificate_module, "CRL_PATH", crl)
    return cert, cert_path, pub_path, crl


def test_cli_verifies_certificate_that_is_not_revoked(cli_setup):
    cert, cert_path, pub_path, crl = cli_setup
    result = CliRunner().invoke(cli, ["verify", str(cert_path), "--key", str(pub_path)])
    assert result.exit_code == 0, result.output
    assert "VERIFIED" in result.output


def test_cli_refuses_revoked_certificate(cli_setup):
    cert, cert_path, pub_path, crl = cli_setup
    revoke_certificate(cert.id, crl_path=crl)
    assert json.loads(crl.read_text())[0]["cert_id"] == cert.id

    result = CliRunner().invoke(cli, ["verify", str(cert_path), "--key", str(pub_path)])
    assert result.exit_code == 1
    assert "REVOKED" in result.output
    assert "VERIFIED" not in result.output

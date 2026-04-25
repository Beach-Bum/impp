"""IMPP CLI — verify, search, publish, and attach agent memory artifacts."""

import json
import sys
from pathlib import Path

import click
import httpx

from .config import API_BASE_URL, AMM_DIR, CERTS_DIR
from .verification.certificate import (
    VerificationCertificate,
    generate_keypair,
    load_public_key,
)


@click.group()
@click.version_option(package_name="impp")
def cli():
    """IMPP — The Agent Memory Registry CLI."""
    pass


@cli.command()
@click.argument("artifact", type=click.Path(exists=True))
@click.option("--local", is_flag=True, help="Run verification locally (no server)")
@click.option("--key", type=click.Path(exists=True), help="Public key for signature verification")
def verify(artifact: str, local: bool, key: str | None):
    """Verify a memory artifact or its certificate."""
    path = Path(artifact)
    data = json.loads(path.read_text())

    # If the file is a certificate, verify its signature
    if "artifact_hash" in data and "signature" in data:
        cert = VerificationCertificate.from_dict(data)

        if cert.is_expired():
            click.secho("EXPIRED", fg="red", bold=True)
            click.echo(f"  Certificate expired at {cert.expires_at}")
            sys.exit(1)

        if cert.signature:
            pub_key_path = Path(key) if key else None
            try:
                pub = load_public_key(pub_key_path)
                if cert.verify_signature(pub):
                    click.secho("VERIFIED", fg="green", bold=True)
                    click.echo(f"  Trust score: {cert.trust_score}")
                    click.echo(f"  Adversarial: {cert.adversarial['verdict']}")
                    click.echo(f"  Expires: {cert.expires_at}")
                else:
                    click.secho("SIGNATURE INVALID", fg="red", bold=True)
                    sys.exit(1)
            except FileNotFoundError:
                click.secho("NO PUBLIC KEY", fg="yellow", bold=True)
                click.echo("  Certificate has a signature but no public key found.")
                click.echo(f"  Use --key to provide one, or place it at {CERTS_DIR / 'impp_signing.pub'}")
                sys.exit(1)
        else:
            click.secho("UNSIGNED", fg="yellow", bold=True)
            click.echo(f"  Trust score: {cert.trust_score}")
        return

    # Otherwise, send to verification server
    if local:
        click.echo("Local verification requires the full amm pipeline.")
        click.echo("Run: python -m amm.verification.referee <artifact>")
        return

    click.echo(f"Submitting {path.name} to {API_BASE_URL}/api/verify ...")
    try:
        resp = httpx.post(
            f"{API_BASE_URL}/api/verify",
            json={"artifact": data},
            timeout=120,
        )
        resp.raise_for_status()
        result = resp.json()
        click.secho(f"Trust score: {result.get('trust_score', 'N/A')}", fg="green")
        cert_path = path.with_suffix(".cert.json")
        cert_path.write_text(json.dumps(result.get("certificate", result), indent=2))
        click.echo(f"Certificate saved to {cert_path}")
    except httpx.HTTPError as e:
        click.secho(f"Verification failed: {e}", fg="red")
        sys.exit(1)


@cli.command()
@click.option("--domain", help="Filter by domain")
@click.option("--min-trust", type=float, default=0, help="Minimum trust score")
@click.option("--limit", type=int, default=20, help="Max results")
def search(domain: str | None, min_trust: float, limit: int):
    """Search the IMPP registry for verified artifacts."""
    params = {"limit": limit, "min_trust": min_trust}
    if domain:
        params["domain"] = domain

    try:
        resp = httpx.get(f"{API_BASE_URL}/api/search", params=params, timeout=30)
        resp.raise_for_status()
        results = resp.json()

        if not results.get("artifacts"):
            click.echo("No artifacts found.")
            return

        for art in results["artifacts"]:
            trust = art.get("trust_score", "?")
            domain_tag = art.get("domain", "unknown")
            name = art.get("name", art.get("artifact_hash", "?")[:12])
            click.echo(f"  [{trust:>5}] {name}  ({domain_tag})")

    except httpx.HTTPError as e:
        click.secho(f"Search failed: {e}", fg="red")
        sys.exit(1)


@cli.command()
@click.argument("artifact", type=click.Path(exists=True))
@click.option("--domain", required=True, help="Artifact domain (e.g. defi, cybersec)")
@click.option("--name", help="Artifact name")
def publish(artifact: str, domain: str, name: str | None):
    """Publish a verified artifact to the IMPP registry."""
    path = Path(artifact)
    data = json.loads(path.read_text())

    payload = {
        "artifact": data,
        "domain": domain,
    }
    if name:
        payload["name"] = name

    click.echo(f"Publishing {path.name} to {API_BASE_URL}/api/publish ...")
    try:
        resp = httpx.post(
            f"{API_BASE_URL}/api/publish",
            json=payload,
            timeout=120,
        )
        resp.raise_for_status()
        result = resp.json()
        click.secho("Published.", fg="green")
        click.echo(f"  Registry ID: {result.get('id', 'N/A')}")
        click.echo(f"  Trust score: {result.get('trust_score', 'N/A')}")
    except httpx.HTTPError as e:
        click.secho(f"Publish failed: {e}", fg="red")
        sys.exit(1)


@cli.command()
@click.argument("artifact", type=click.Path(exists=True))
@click.option("--agent", required=True, help="Target agent identifier")
def attach(artifact: str, agent: str):
    """Attach a verified memory artifact to an agent."""
    path = Path(artifact)
    click.echo(f"Attaching {path.name} to agent '{agent}' ...")

    agent_dir = AMM_DIR / "agents" / agent
    agent_dir.mkdir(parents=True, exist_ok=True)
    dest = agent_dir / path.name
    dest.write_text(path.read_text())
    click.secho(f"Attached to {dest}", fg="green")


@cli.command("keygen")
@click.option("--dir", "key_dir", type=click.Path(), help="Directory for keys")
def keygen(key_dir: str | None):
    """Generate an Ed25519 signing keypair."""
    out_dir = Path(key_dir) if key_dir else None
    priv_path, pub_path = generate_keypair(out_dir)
    click.secho("Keypair generated.", fg="green")
    click.echo(f"  Private: {priv_path}")
    click.echo(f"  Public:  {pub_path}")


def main():
    cli()


if __name__ == "__main__":
    main()

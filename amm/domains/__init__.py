"""Domain configurations for benchmark evaluation."""

from .base import Domain


DOMAIN_REGISTRY: dict[str, type[Domain]] = {}


def _register_domains():
    from .defi_risk import DeFiRiskDomain
    from .cybersec import CyberSecDomain

    DOMAIN_REGISTRY["defi"] = DeFiRiskDomain
    DOMAIN_REGISTRY["cybersec"] = CyberSecDomain


def get_domain(name: str) -> Domain:
    """Get a domain instance by name.

    Args:
        name: Domain key (e.g., 'defi', 'cybersec')

    Returns:
        Domain instance.

    Raises:
        ValueError: If the domain name is not registered.
    """
    if not DOMAIN_REGISTRY:
        _register_domains()

    if name not in DOMAIN_REGISTRY:
        available = ", ".join(sorted(DOMAIN_REGISTRY.keys()))
        raise ValueError(f"Unknown domain '{name}'. Available: {available}")

    return DOMAIN_REGISTRY[name]()


def list_domains() -> list[str]:
    """Return available domain names."""
    if not DOMAIN_REGISTRY:
        _register_domains()
    return sorted(DOMAIN_REGISTRY.keys())

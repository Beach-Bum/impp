# IMPP — The Agent Memory Registry

**Paper:** [PDF](paper/agent-memory-markets.pdf) | **Docs:** [impp.sh/docs](https://impp.sh/docs) | **Registry:** [impp.sh](https://impp.sh)

> A verification protocol for cross-model AI agent knowledge transfer. Install verified memory packages with `impp install`.

## What This Is

AI agents learn through experience. An agent that spends 20 rounds learning DeFi risk assessment develops calibrated heuristics, error patterns, and domain intuition. IMPP asks: **can that learned behavior be extracted, verified, and transferred to another agent?**

Yes. With 95-110% transfer efficiency across models.

The hard problem is trust. Memory artifacts have information asymmetry worse than traditional lemons markets: revealing the artifact to prove quality destroys its value. IMPP solves this with a **referee protocol** that verifies artifact quality without exposing contents, plus adversarial probes that catch poisoned or fraudulent artifacts before any buyer is exposed.

## Key Results

| Domain | Expert Error | Novice Error | Buyer Error | Transfer Efficiency |
|--------|-------------|-------------|-------------|-------------------|
| DeFi Risk Assessment | 3.3 | 7.4 | 3.2 | **109.9%** |
| Cybersecurity Vuln Assessment | 3.9 | 18.0 | 4.5 | **95.5%** |

Cross-model transfer (GPT-4o to Claude Sonnet) verified across 56 artifacts. Three trials each, statistically significant.

### Poisoned Artifact Detection

| Metric | Result |
|--------|--------|
| Seller claimed TE | 95% |
| Measured TE | **-39%** |
| Verdict | **WARN** |
| Trust Score | 35.8/100 |
| Stego Score | 100 (hidden instructions detected) |

The verification protocol catches fraudulent artifacts before any buyer is exposed.

## Quick Start

### Install the CLI

```bash
pip install impp
```

### Define dependencies

```json
{
  "require": {
    "impp/defi-risk-assessment": "^2.1",
    "impp/cybersec-threat-intel": "^1.4"
  }
}
```

### Install and use

```bash
impp install
```

```python
import impp
artifacts = impp.autoload()
```

### Verify an artifact

```bash
impp verify artifact.json
```

### Run a full benchmark (train + export + verify)

```bash
export ANTHROPIC_API_KEY=your-key
python run_experiment.py --trials 3 --domain defi_risk
```

**Estimated costs:** Single verification ~$0.35 (25 API calls). Full train + verify (3 trials) ~$2.00.

## The Referee Protocol

```
Seller submits artifact (sealed)
         |
         v
   Referee Agent (independent, disposable)
   |-- Runs artifact on HELD-OUT benchmark
   |-- Benchmark is NOT known to seller
   +-- Adversarial probes run in parallel
         |
         v
   Verification Certificate (Ed25519 signed)
   |-- Transfer efficiency (verified)
   |-- Adversarial probe results
   +-- Trust score (composite)
         |
         v
   Published to registry (artifact contents still sealed)
```

## Trust Score

The trust score is a composite metric. Higher is better.

| Component | Weight | Description |
|-----------|--------|-------------|
| Transfer Efficiency | 50% | How well the artifact transfers knowledge |
| Adversarial Clean | 30% | `100 - adversarial_risk` — lower risk = higher trust |
| Freshness | 20% | How recently the artifact was verified |

### Adversarial Risk Score

Four probes compute an adversarial risk score (lower = cleaner):

| Probe | Weight | What it catches |
|-------|--------|----------------|
| Bias | 30% | Systematic skew via trap protocols |
| Consistency | 25% | Fragile artifacts via perturbation testing |
| Steganography | 25% | Hidden instructions embedded in artifact text |
| Overfitting | 20% | Performance gap between seen and unseen data |

**Risk thresholds:** 0-30 = PASS (clean), 31-50 = WARNING (review recommended), 51-100 = FAIL (reject).

## Memory Artifact Schema

**M = (D, K, P, A, H)**

| Component | Description |
|-----------|-------------|
| **D** (Domain) | Category, subcategory, scope |
| **K** (Knowledge) | The learned content (markdown) |
| **P** (Provenance) | Agent ID, model, training history |
| **A** (Attestation) | Self-reported performance metrics |
| **H** (Hash) | SHA-256 content-addressed identifier |

## Domains

Domain-agnostic framework. Currently implemented:

1. **DeFi Risk Assessment** — 32 synthetic protocols with ground truth risk scores (0-100)
2. **Cybersecurity Vulnerability Assessment** — 8 synthetic vulnerabilities with ground truth severity scores (0-100)

Adding a new domain requires only a domain config file. No changes to benchmark, verification, or adversarial code.

## Project Structure

```
impp/
|-- paper/                          # Research paper (CC-BY-4.0)
|   |-- agent-memory-markets.tex    # LaTeX source
|   +-- agent-memory-markets.pdf    # Compiled PDF
|-- amm/                            # Core protocol package (Apache-2.0)
|   |-- config.py                   # Weights, thresholds, constants
|   |-- artifact/                   # M = (D, K, P, A, H) spec
|   |-- domains/                    # Domain configs (DeFi, CyberSec)
|   |-- benchmark/                  # Training + evaluation engine
|   |-- verification/               # Referee protocol + Ed25519 certificates
|   |-- adversarial/                # 4 probe types + runner
|   |-- registry/                   # Trust registry
|   +-- marketplace/                # Identity, listings, previews
|-- ui/                             # Web UI (Next.js + shadcn/ui)
|-- api_server.py                   # Reference registry API (FastAPI)
|-- schemas/                        # JSON Schema definitions
|-- spec/                           # Protocol specifications
|-- tests/                          # Test suite
|-- run_experiment.py               # CLI: full end-to-end pipeline
|-- run_verify.py                   # CLI: verify a single artifact
+-- cross_model_test.py             # Cross-model transfer experiments
```

## Development

```bash
# Python (protocol + CLI)
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
AMM_TESTING=1 pytest

# UI
cd ui && npm install && npm run dev
```

## Threat Model

IMPP's trust scores are heuristic, versioned, and not a guarantee. They are useful signals, not oracles. The public scoring formula is the reference implementation. Production verification uses independent, rotating, non-public holdout probes that are not included in this repository.

For the full threat model, see [the paper](paper/agent-memory-markets.pdf).

## Citation

```bibtex
@article{karlovich2026agent,
  title={Agent Memory Markets: A Verification Protocol for Cross-Model Knowledge Transfer},
  author={Karlovich, Ned},
  journal={arXiv preprint},
  year={2026}
}
```

## License

- **Code:** [Apache-2.0](LICENSE) — includes explicit patent grant
- **Paper & docs:** [CC-BY-4.0](paper/LICENSE)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). All contributions require DCO sign-off.

## Security

See [SECURITY.md](SECURITY.md). Report vulnerabilities privately.

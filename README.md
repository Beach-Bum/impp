# Agent Memory Markets: Tokenizing Learned Behavior as a Transferable Economic Asset

**Paper:** [PDF](paper/agent-memory-markets.pdf) | **Author:** Ned Karlovich (ned.karlovich@pm.me)

> The first empirical work on whether AI agent learned behavior can be extracted, verified, and traded as an economic asset.

## Key Results

| Domain | Expert Error | Novice Error | Buyer Error | Transfer Efficiency |
|--------|-------------|-------------|-------------|-------------------|
| DeFi Risk Assessment | 3.3 | 7.4 | 3.2 | **109.9%** (relative) |
| Cybersecurity Vuln Assessment | 3.9 | 18.0 | 4.5 | **95.5%** (relative) |

A "buyer" agent using a purchased memory artifact matches or exceeds expert performance across both domains. Three trials each, statistically significant.

### Poisoned Artifact Detection

| Metric | Result |
|--------|--------|
| Seller claimed TE | 95% |
| Measured TE | **-39%** |
| Verdict | **WARN** |
| Trust Score | 35.8/100 |
| Bias Score | 50 |
| Stego Score | 100 (hidden instructions detected) |

The verification protocol catches fraudulent artifacts before any buyer is exposed.

## What This Is

AI agents learn through experience. An agent that spends 20 rounds learning DeFi risk assessment develops calibrated heuristics, error patterns, and domain intuition. This project asks: **can that learned behavior be extracted and sold to another agent?**

Yes. With 95-110% transfer efficiency.

The harder problem is trust. Memory artifacts have an information asymmetry worse than traditional lemons markets: revealing the artifact to prove quality destroys its value. We solve this with a **referee protocol** that verifies artifact quality without exposing its contents.

## The Referee Protocol

```
Seller submits artifact (sealed)
         │
         ▼
   Referee Agent (independent, disposable)
   ├── Runs artifact on HELD-OUT benchmark
   ├── Benchmark is NOT known to seller
   └── Adversarial probes run in parallel
         │
         ▼
   Verification Certificate
   ├── Transfer efficiency (verified)
   ├── Adversarial probe results
   └── Trust score (composite)
         │
         ▼
   Published to registry (artifact contents still sealed)
```

### Adversarial Detection

Four probes catch different attack vectors:

- **Bias Probe** (weight: 0.30) — Trap protocols designed to expose systematic skew in seller's favor
- **Consistency Probe** (weight: 0.25) — Perturbation testing: modify inputs, verify proportional response
- **Steganographic Probe** (weight: 0.25) — Auditor agent scans for hidden instructions embedded in artifact text
- **Overfitting Probe** (weight: 0.20) — Compares performance on seen vs unseen protocols

Aggregate score determines verdict: **PASS** (<30), **WARN** (30-60), **FAIL** (>60).

## Memory Artifact Schema

Formal specification: **M = (D, K, P, A, H)**

| Component | Description |
|-----------|-------------|
| **D** (Domain) | Category, subcategory, scope |
| **K** (Knowledge) | The actual learned content (markdown) |
| **P** (Provenance) | Agent ID, model, training history |
| **A** (Attestation) | Self-reported performance metrics |
| **H** (Hash) | SHA-256 content-addressed identifier |

## Domains

Domain-agnostic framework. Currently implemented:

1. **DeFi Risk Assessment** — 8 synthetic protocols with ground truth risk scores (0-100)
2. **Cybersecurity Vulnerability Assessment** — 8 synthetic vulnerabilities with ground truth severity scores (0-100)

Adding a new domain requires only a domain config file. No changes to benchmark, verification, or adversarial code.

## Usage

### Run a full benchmark (train + export + verify)
```bash
export ANTHROPIC_API_KEY=your-key
python run_experiment.py --trials 3 --domain defi_risk
```

### Verify an existing artifact
```bash
python run_verify.py --artifact path/to/artifact.json
```

### Estimated costs
- Single verification: ~25 API calls (~$0.35)
- Full train + verify (3 trials): ~$2.00
- Model: claude-sonnet-4-20250514

## Project Structure

```
agent-memory-market-protocol/
├── paper/
│   ├── agent-memory-markets.tex      # LaTeX paper (ArXiv-ready)
│   └── agent-memory-markets.pdf      # Compiled PDF
├── run_verify.py                     # CLI: verify a single artifact
├── run_experiment.py                 # CLI: full end-to-end pipeline
├── amm/                              # Core package
│   ├── api.py                        # Anthropic API wrapper
│   ├── config.py                     # Model, paths, constants
│   ├── artifact/                     # M = (D, K, P, A, H) spec
│   ├── domains/                      # Domain configs (DeFi, CyberSec)
│   ├── benchmark/                    # Training + evaluation engine
│   ├── verification/                 # Referee protocol + certificates
│   ├── adversarial/                  # 4 probe types + runner
│   └── registry/                     # SQLite trust registry
├── schemas/                          # JSON Schema definitions
└── tests/
```

## How It Works

1. **Train** an expert agent over 20 rounds with ground-truth feedback
2. **Export** its accumulated knowledge as a structured memory artifact
3. **Verify** the artifact using a disposable referee agent on held-out benchmarks
4. **Probe** for adversarial content (bias, inconsistency, steganography, overfitting)
5. **Certify** with a verification certificate and trust score
6. **Trade** — buyer receives artifact + certificate, never needs to trust the seller

## Citation

```bibtex
@article{karlovich2026agent,
  title={Agent Memory Markets: Tokenizing Learned Behavior as a Transferable Economic Asset},
  author={Karlovich, Ned},
  journal={arXiv preprint},
  year={2026}
}
```

## License

MIT

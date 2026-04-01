# Agent Memory Market Protocol

A verification protocol for agent memory markets — solving the hardest problem in trading AI agent experience: **how does a buyer trust an artifact they can't inspect?**

## Background

This project builds on the [Agent Memory Markets](https://github.com/) working paper (March 2026), which demonstrated that AI agent experience is transferable with 92% efficiency. The experiment trained an expert agent over 20 rounds of DeFi risk assessment, exported its knowledge as a "memory artifact," and showed that a buyer agent using that artifact nearly matched the expert's performance.

The missing piece: **verification and trust**. Without it, there's no market.

## The Problem

Memory artifacts have an information asymmetry problem worse than traditional lemons markets:

1. **Pre-purchase**: Revealing the artifact to prove quality destroys its value
2. **During purchase**: Evaluating requires using the artifact — and you can't "un-know" it
3. **Post-purchase**: Feedback is delayed; early buyers are exposed
4. **Adversarial**: Poisoned artifacts can embed biased heuristics or steganographic instructions

## The Solution: Referee Protocol

```
Seller submits artifact (sealed)
         |
         v
   Referee Agent (independent, disposable)
   - Runs artifact on HELD-OUT benchmark
   - Benchmark is NOT known to seller
   - Adversarial probes run in parallel
         |
         v
   Verification Certificate
   - Performance score (verified)
   - Transfer efficiency (differential vs novice)
   - Adversarial probe results
   - Trust score (composite)
         |
         v
   Published to registry (artifact contents still sealed)
```

## Architecture

### 5 Components

| Component | Purpose |
|-----------|---------|
| **Artifact Spec** | Formal schema for M = (D, K, P, A, H) — Domain, Knowledge, Provenance, Attestation, Hash |
| **Benchmark Engine** | Domain-agnostic evaluation framework with held-out test sets |
| **Verification Protocol** | Referee orchestration: seal, benchmark, score, certify |
| **Adversarial Detection** | 4 probe types: bias traps, consistency, steganographic scan, overfitting |
| **Trust Registry** | Content-addressed artifact store + verification certificates + trust scores |

### Adversarial Detection (Novel Contribution)

- **Bias Probe**: Trap protocols designed to expose systematic skew in seller's favor
- **Consistency Probe**: Perturbation testing — modify inputs, verify proportional response
- **Steganographic Probe**: Auditor agent scans for hidden instructions in artifact text
- **Overfitting Probe**: Compares performance on seen vs unseen protocols

## Domains

Domain-agnostic from day one. First domain: **DeFi protocol risk assessment** (8 synthetic protocols with ground truth scores).

Adding a new domain requires only a domain config file — no changes to benchmark, verification, or adversarial code.

## Usage

### Verify an existing artifact
```bash
export ANTHROPIC_API_KEY=your-key
python run_verify.py --artifact path/to/artifact.json
```

### Full end-to-end (train + export + verify)
```bash
python run_experiment.py --trials 3 --domain defi_risk
```

### Estimated costs
- Single verification: ~25 API calls (~$0.35)
- Full train + verify (3 trials): ~$2.00
- Model: claude-sonnet-4-20250514

## Project Structure

```
agent-memory-market-protocol/
├── run_verify.py                     # CLI: verify a single artifact
├── run_experiment.py                 # CLI: full end-to-end pipeline
├── amm/                              # Core package
│   ├── api.py                        # Anthropic API wrapper
│   ├── config.py                     # Model, paths, constants
│   ├── artifact/                     # M = (D, K, P, A, H) spec
│   ├── domains/                      # Domain configs (DeFi risk first)
│   ├── benchmark/                    # Training + evaluation engine
│   ├── verification/                 # Referee protocol + certificates
│   ├── adversarial/                  # 4 probe types + runner
│   └── registry/                     # SQLite trust registry
├── schemas/                          # JSON Schema definitions
└── tests/
```

## Related Work

- **Working Paper**: "Agent Memory Markets: Tokenizing Learned Behavior as a Transferable Economic Asset" (March 2026)
- **Proof-of-Concept Experiment**: 92% transfer efficiency in DeFi risk assessment
- **ERC-8004**: Agent Identity, Reputation, and Validation (Ethereum)
- **Agentic Identity Protocol**: Memory + Expression + Environment framework

## Status

**In development.** Building the verification protocol prototype.

## License

MIT

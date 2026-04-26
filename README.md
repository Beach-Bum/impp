# IMPP — Inter-Model Memory Protocol

**Active paper draft:** [IMPP: A Protocol for Portable Procedural Memory in AI Agent Systems](paper/impp-portable-procedural-memory.md)  
**Docs:** [impp.sh/docs](https://impp.sh/docs) | **Reference registry:** [impp.sh](https://impp.sh)

> IMPP is a protocol and reference registry for portable procedural and semantic memory artifacts in AI agent systems.

## What this is

AI agents increasingly accumulate useful memory: task traces, skill files, prompt refinements, domain heuristics, user preferences, tool-use rules, and structured notes. Today that memory is usually bound to a single app, framework, model provider, or deployment.

IMPP asks a narrower and more useful question:

> Can bounded procedural and semantic memory be packaged as signed, versioned, evaluable artifacts and safely attached to other agent systems?

The current answer is: early evidence suggests yes, but only with explicit protocol machinery. Portable memory artifacts need scope, attach semantics, provenance, privacy and license metadata, verification, revocation, and tests for negative transfer.

This repository is currently being reframed around the protocol-first version of the work. Marketplace mechanisms are future work; the first serious research claim is about making portable memory artifacts concrete, attachable, evaluable, and governable.

## Core concepts

### Memory artifacts

An IMPP artifact packages bounded agent memory with enough metadata to evaluate and attach it safely.

The original compact model is:

```text
M = (D, K, P, A, H)
```

where:

| Component | Description |
|---|---|
| `D` Domain | Task/domain scope |
| `K` Knowledge | Procedural or semantic memory payload |
| `P` Provenance | Source, author, model, observation window |
| `A` Attestation | Claimed performance or verification evidence |
| `H` Hash | Content-addressed identifier |

The v0.2 schema expands this into a richer artifact manifest with license, privacy, attach modes, evaluation suites, conflicts, freshness, and revocation metadata.

See:

- [Artifact schema v0.2](docs/artifact_schema_v0_2.md)
- [JSON Schema](schemas/impp.artifact.v0.2.schema.json)

### Attach modes

Installing memory is ambiguous unless the runtime contract is explicit. IMPP defines attach modes for how an artifact influences an agent:

| Attach mode | Runtime behavior | Main risk |
|---|---|---|
| `prepend_policy` | Adds guidance near the top of context | Hidden instructions or policy conflict |
| `few_shot_examples` | Provides examples for imitation or calibration | Benchmark leakage or anchoring |
| `retrieval_only` | Retrieves relevant chunks on demand | Retrieval poisoning or irrelevant context |
| `tool_policy` | Constrains or guides tool use | Unsafe authorization or blocking |
| `read_only_reference` | Exposes artifact without automatic injection | Underuse |

See [attach modes](docs/attach_modes.md).

### Two-layer trust

IMPP separates trust into two layers.

1. **Container / supply-chain trust** verifies artifact identity, authorship, signatures, hashes, publication history, and revocation state.
2. **Semantic / behavioral trust** evaluates whether the artifact improves downstream behavior safely within its declared scope.

Signatures prove integrity. They do not prove that an artifact is safe or useful.

See [trust model](docs/trust_model.md).

### Staged trust ladder

Artifacts should move through staged trust states:

```text
imported -> parsed -> evaluated -> verified -> curated
```

Artifacts can also be rejected, revoked, or superseded. A new artifact version starts over. A stale artifact can be downgraded.

## Verification

The reference verifier follows a referee-style protocol:

```text
Artifact submitted
        |
        v
Schema, hash, provenance, and attach-mode checks
        |
        v
No-memory baseline + artifact-attached evaluation
        |
        v
Adversarial probes and negative-transfer tests
        |
        v
Signed verification certificate with reason codes
        |
        v
Registry trust state update
```

The current trust score is a provisional heuristic:

| Component | Weight | Description |
|---|---:|---|
| Transfer efficiency | 50% | Does the artifact improve behavior? |
| Adversarial cleanliness | 30% | Does it avoid known manipulation patterns? |
| Freshness | 20% | Is the artifact still current? |

The current adversarial risk score includes bias, consistency, steganography, and overfitting probes. These weights are reference defaults, not universal truth.

## Pilot evidence

The prototype includes pilot experiments in:

1. **DeFi risk assessment** — synthetic protocols with ground-truth risk scores.
2. **Cybersecurity vulnerability assessment** — synthetic vulnerabilities with ground-truth severity scores.

The early results suggest that structured memory artifacts can transfer useful calibration behavior. The evidence is still pilot-scale and should be treated conservatively. Known limitations include small synthetic domains, benchmark leakage risk, prompt/model variance, incomplete negative-transfer testing, and uncalibrated trust-score weights.

The protocol-first paper should not claim universal cross-model transfer, objective trust scoring, automatic safety, or proof that a full marketplace will exist.

## Quick start

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

### Run a benchmark

```bash
export ANTHROPIC_API_KEY=your-key
python run_experiment.py --trials 3 --domain defi_risk
```

## Reproducibility package

The planned public paper package lives under [`data/paper_v1/`](data/paper_v1/README.md). It is intended to contain sanitized artifacts, public tasks, sample labels, result tables, and split metadata sufficient to reproduce the paper's public tables.

Production holdouts, live adversarial prompts, canary artifacts, abuse heuristics, raw private traces, and proprietary artifacts should remain private or rotating.

## Project structure

```text
impp/
|-- paper/                          # Research paper drafts (CC-BY-4.0)
|   |-- impp-portable-procedural-memory.md
|   |-- agent-memory-markets.tex    # Legacy marketplace-first draft
|   +-- agent-memory-markets.pdf
|-- docs/                           # Protocol docs
|-- amm/                            # Core protocol package (Apache-2.0)
|   |-- config.py
|   |-- artifact/
|   |-- domains/
|   |-- benchmark/
|   |-- verification/
|   |-- adversarial/
|   |-- registry/
|   +-- marketplace/
|-- data/paper_v1/                  # Planned reproducibility package
|-- ui/                             # Web UI
|-- api_server.py                   # Reference registry API
|-- schemas/                        # JSON Schema definitions
|-- spec/                           # Protocol specifications
|-- tests/
|-- run_experiment.py
|-- run_verify.py
+-- cross_model_test.py
```

## Development

```bash
# Python protocol and CLI
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
AMM_TESTING=1 pytest

# UI
cd ui && npm install && npm run dev
```

## Threat model

Portable memory is behavioral supply-chain material. It should be assumed untrusted until parsed, evaluated, and attached under an explicit mode.

See [threat model](docs/threat_model.md).

## Citation

The active citation target is being rewritten around the protocol-first paper:

```bibtex
@article{karlovich2026impp,
  title={IMPP: A Protocol for Portable Procedural Memory in AI Agent Systems},
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

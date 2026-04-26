# IMPP paper v1 reproducibility package

Public reproducibility package for:

> IMPP: A Protocol for Portable Procedural Memory in AI Agent Systems

## Contents

| File | Description |
|------|-------------|
| `artifacts_sanitized.jsonl` | 3 sanitized example artifacts (DeFi, CyberSec, poisoned) with IMPP schema metadata |
| `tasks.jsonl` | 41 synthetic evaluation tasks across DeFi (32) and CyberSec (9) domains |
| `labels.csv` | Ground-truth risk/severity scores for all 41 items (original format) |
| `labels_public_sample.csv` | Same labels with split and is_sample annotations |
| `results.csv` | Canonical experiment results used to generate paper tables |
| `splits.json` | Core (8-item) and extended (24-item) split definitions per domain |
| `adversarial_results.json` | Poisoned artifact detection: probe scores, flags, and verdict |

All data is synthetic. All items are marked `is_sample=true`. No PII, real protocols, or production holdouts.

## Reproducing paper tables

```bash
# Generate markdown tables to paper/tables/
python experiments/generate_paper_tables.py

# Print legacy plain-text tables to stdout
python experiments/generate_tables.py
```

## Experiment conditions

The paper evaluates 8 conditions (see `experiments/README.md`):

1. `no_memory` — baseline, no artifact
2. `raw_context` — full artifact dumped into context
3. `prompt_skill_file` — structured prompt-only (no IMPP metadata)
4. `impp_artifact` — full IMPP artifact with attach mode
5. `retrieval_only` — RAG retrieval from artifact chunks
6. `few_shot` — few-shot examples from artifact
7. `negative_transfer` — wrong-domain artifact
8. `poisoned_artifact` — deliberately manipulated artifact

## Public vs private data

**Public** (in this directory): sanitized artifacts, synthetic tasks, sample labels, aggregate results, probe categories, trust-score formula.

**Private** (not included): live holdout tasks, canary artifacts, production adversarial prompts, abuse heuristics, raw traces, proprietary artifacts, credentials.

## Limitations

- Pilot-scale synthetic domains (DeFi risk, cybersec vulnerability)
- Small item counts (8 core, 32 extended)
- Benchmark leakage risk from public labels
- Prompt and model variance across runs
- Incomplete negative-transfer testing
- Uncalibrated trust-score weights

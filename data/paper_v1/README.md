# IMPP Paper v1 — Reproducibility Package

Data and scripts for reproducing the results in:

> **IMPP: A Protocol for Portable Procedural Memory in AI Agent Systems**
> Karlovich, Ned (2026). Preprint.

## Contents

| File | Description |
|------|-------------|
| `tasks.jsonl` | Evaluation tasks: DeFi risk scoring (8+24 protocols) and CyberSec vulnerability scoring (8 vulnerabilities) |
| `labels.csv` | Ground-truth scores for all evaluation items |
| `results.csv` | Per-trial results across all experiments (DeFi 3-trial, CyberSec 3-trial, cross-model) |
| `splits.json` | Train/held-out splits for each domain |
| `adversarial_results.json` | Poisoned artifact detection results |

## Experiment Setup

- **DeFi domain**: 8 protocols (core set) + 24 protocols (extended cross-model set)
- **CyberSec domain**: 8 vulnerabilities
- **Seller model** (artifact creator): Claude Sonnet 4 (`claude-sonnet-4-20250514`)
- **Buyer model** (same-model transfer): Claude Sonnet 4
- **Cross-model buyer**: GPT-4o (manual ChatGPT evaluation)
- **Trials**: 3 independent runs per configuration
- **Metric**: Transfer Efficiency = `(novice_error - buyer_error) / (novice_error - expert_error) * 100`

## Reproducing Results

```bash
cd experiments/
python generate_tables.py
```

## Limitations

- Synthetic evaluation domains (generated protocol/vulnerability profiles, not real-world data)
- Small item counts (8-32 per domain)
- Cross-model experiment was manual (ChatGPT web interface), not automated API
- 3 trials per configuration — limited statistical power
- Trust score weights are hand-tuned, not calibrated against downstream outcomes

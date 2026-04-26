# Experiments

Scripts for running and reproducing IMPP paper v1 experiments.

## Scripts

### `generate_tables.py`

Legacy table generator. Reads `data/paper_v1/results.csv` and prints plain-text tables to stdout.

```bash
python experiments/generate_tables.py
```

### `generate_paper_tables.py`

Paper-ready table generator. Reads `data/paper_v1/` and writes markdown tables to `paper/tables/`.

```bash
python experiments/generate_paper_tables.py
```

### `run_paper_v1.py`

Experiment orchestrator for all paper v1 conditions. Two modes:

**Dry-run (default-safe, no API calls):**
```bash
python experiments/run_paper_v1.py --dry-run
python experiments/run_paper_v1.py --dry-run --domain defi_risk
python experiments/run_paper_v1.py --dry-run --domain cybersec_vuln
```

Validates data fixtures, loads tasks and labels, prints a run manifest. No LLM calls, no output file.

**Live (real API calls):**
```bash
python experiments/run_paper_v1.py --live --domain defi_risk \
    --conditions no_memory impp_artifact --trials 1
```

Requires `ANTHROPIC_API_KEY`. Currently supports `no_memory` and `impp_artifact` conditions. Results are appended to `data/paper_v1/results_real.csv` (sample fixtures in `results.csv` are never modified).

If neither `--dry-run` nor `--live` is specified, defaults to `--dry-run`.

## Conditions

| Condition | Description | Attach mode |
|-----------|-------------|-------------|
| `no_memory` | Baseline with no artifact | none |
| `raw_context` | Full artifact text in context | prepend_policy |
| `prompt_skill_file` | Structured prompt-only skill file | prepend_policy |
| `impp_artifact` | Full IMPP artifact with metadata | prepend_policy |
| `retrieval_only` | RAG-style retrieval from chunks | retrieval_only |
| `few_shot` | Few-shot examples from artifact | few_shot_examples |
| `negative_transfer` | Wrong-domain artifact | prepend_policy |
| `poisoned_artifact` | Deliberately manipulated artifact | prepend_policy |

## Data

All experiment data lives in `data/paper_v1/`. See that directory's README for file descriptions and the public/private data boundary.

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

Experiment orchestrator for all paper v1 conditions. Validates data fixtures, runs trials across conditions, writes results.

```bash
# Validate setup (no LLM calls)
python experiments/run_paper_v1.py --dry-run

# Run a specific domain
python experiments/run_paper_v1.py --domain defi_risk --trials 3

# Run specific conditions
python experiments/run_paper_v1.py --conditions no_memory impp_artifact --trials 3
```

Requires `ANTHROPIC_API_KEY` for Claude conditions. `OPENAI_API_KEY` for cross-model conditions (optional).

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

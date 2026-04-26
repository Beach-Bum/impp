# IMPP paper v1 reproducibility package

This directory is the planned public reproducibility package for the protocol-first IMPP paper:

> IMPP: A Protocol for Portable Procedural Memory in AI Agent Systems

The goal is to make the paper's main empirical tables reproducible without publishing live production holdouts, private adversarial probes, customer data, or proprietary artifacts.

## Planned contents

```text
data/paper_v1/
  README.md
  artifacts_sanitized.jsonl
  tasks.jsonl
  labels_public_sample.csv
  results.csv
  splits.json
```

## File descriptions

### `artifacts_sanitized.jsonl`

Public sanitized memory artifacts used for paper experiments. These should remove benchmark answer keys, private traces, credentials, PII, proprietary source material, and live holdout clues.

Each record should include enough metadata to validate the IMPP artifact schema and reproduce the declared attach-mode behavior.

### `tasks.jsonl`

Public evaluation tasks used to regenerate paper tables. Tasks should be synthetic or clearly licensed for public redistribution.

### `labels_public_sample.csv`

Ground-truth labels for the public sample. This file should support reproducibility of published tables, but it should not include private rotating holdouts used by a production registry.

### `results.csv`

Canonical result rows used by the paper. At minimum:

```text
run_id,domain,model,condition,attach_mode,task_id,score,error,cost_usd,latency_ms
```

### `splits.json`

Train, public-test, and holdout split metadata. Public test splits can be included. Private production holdout identifiers should not be included.

## Public vs private evaluation material

Public:

- schema-valid sanitized artifacts;
- public benchmark tasks;
- sample labels;
- reproducibility scripts;
- aggregate results;
- probe categories;
- trust-score formula version.

Private or rotating:

- live holdout tasks;
- canary artifacts;
- production adversarial prompts;
- abuse heuristics;
- raw user or customer traces;
- proprietary expert artifacts;
- credentials, deployment IDs, and infrastructure details.

## Minimum experiments for the first arXiv version

The first credible paper package should support:

1. no-memory baseline;
2. raw-context baseline;
3. RAG baseline if available;
4. prompt-only skill-file baseline;
5. IMPP artifact with declared attach mode;
6. attach-mode ablation;
7. negative-transfer test;
8. red-team artifact test;
9. trust-score calibration table if enough artifacts exist.

## Rule of thumb

Publish the protocol and enough data to reproduce the paper's public tables. Do not publish the live exam key used to operate a production registry.

## Summary Statistics (Real Runs)

### Per-Model Results

| Metric | Value |
|--------|-------|
| defi / anthropic/claude-sonnet-4 / impp_artifact MAE | 7.38 +/- 0.65 (n=3, 32 items) |
| defi / anthropic/claude-sonnet-4 / no_memory MAE | 7.81 +/- 0.41 (n=3, 32 items) |
| defi / anthropic/claude-sonnet-4 TE (novice→artifact) | 5.6% |
| defi / gpt-4o / impp_artifact MAE | 8.03 +/- 0.69 (n=4, 32 items) |
| defi / gpt-4o / no_memory MAE | 7.82 +/- 0.24 (n=4, 32 items) |
| defi / gpt-4o TE (novice→artifact) | -2.7% |
| cybersec / anthropic/claude-sonnet-4 / impp_artifact MAE | 18.33 +/- 0.85 (n=3, 8 items) |
| cybersec / anthropic/claude-sonnet-4 / no_memory MAE | 17.04 +/- 1.23 (n=3, 8 items) |
| cybersec / anthropic/claude-sonnet-4 TE (novice→artifact) | -7.6% |
| cybersec / gpt-4o / impp_artifact MAE | 16.42 +/- 0.75 (n=3, 8 items) |
| cybersec / gpt-4o / no_memory MAE | 15.33 +/- 1.83 (n=3, 8 items) |
| cybersec / gpt-4o TE (novice→artifact) | -7.1% |

### Pooled Across Models

*Exploratory only — do not interpret as same-model transfer.*

| Metric | Value |
|--------|-------|
| defi pooled TE | 0.9% (novice n=7, artifact n=7) |
| cybersec pooled TE | -7.3% (novice n=6, artifact n=6) |

*TE = transfer efficiency = (novice_MAE - artifact_MAE) / novice_MAE x 100. Positive TE means the artifact improved performance over novice baseline.*

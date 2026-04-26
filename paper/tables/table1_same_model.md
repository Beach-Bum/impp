> **SAMPLE TABLE** — generated from synthetic/sample fixtures. Do not cite as final empirical evidence.

## Table 1: Same-Model Transfer Results

| Domain | Trial | Expert MAE | Novice MAE | Artifact MAE | TE (%) |
|--------|-------|-----------|-----------|-------------|--------|
| defi | 1 | 4.5 | 7.0 | 3.0 | 57.1 |
| defi | 2 | 3.0 | 7.375 | 4.625 | 37.3 |
| defi | 3 | 2.5 | 7.875 | 2.125 | 73.0 |
| **defi avg** | | | | | **55.8 +/- 17.9** |

| cybersec | 1 | 2.75 | 18.125 | 3.625 | 80.0 |
| cybersec | 2 | 2.75 | 17.75 | 3.75 | 78.9 |
| cybersec | 3 | 6.125 | 18.125 | 6.25 | 65.5 |
| **cybersec avg** | | | | | **74.8 +/- 8.1** |


*Conditions: claude-sonnet-4, 8 synthetic items per domain, 3 independent trials. TE = (novice_error - artifact_error) / (novice_error - expert_error) x 100.*

## Table: Condition Comparison (Real Runs)

| Domain | Model | Condition | Items | MAE | Trials |
|--------|-------|-----------|-------|-----|--------|
| defi | anthropic/claude-sonnet-4 | impp_artifact | 32 | 7.38 | 3 |
| defi | anthropic/claude-sonnet-4 | no_memory | 32 | 7.81 | 3 |
| defi | gpt-4o | impp_artifact | 32 | 8.03 | 4 |
| defi | gpt-4o | no_memory | 32 | 7.82 | 4 |
| cybersec | anthropic/claude-sonnet-4 | impp_artifact | 8 | 18.33 | 3 |
| cybersec | anthropic/claude-sonnet-4 | no_memory | 8 | 17.04 | 3 |
| cybersec | gpt-4o | impp_artifact | 8 | 16.42 | 3 |
| cybersec | gpt-4o | no_memory | 8 | 15.33 | 3 |

*MAE = mean absolute error averaged across trials. Each trial evaluates the paper fixture task set.*

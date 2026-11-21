# Evaluation Report (n=50)

**Status:** Complete for baseline Prompt A (50 of 50 images). Prompt B follow-up covers 47 of 50 images.
**Model:** gemini-2.5-flash (pinned). **Positive class:** FAIL (defect).
**Dataset:** 50 labeled images (25 defective, 25 good), Kaggle casting product image data.

## Results (baseline Prompt A)

| Metric | Value | Meaning |
|---|---|---|
| Clean results | 50 | 25 defective, 25 good |
| Recall | 0.84 | 21 of 25 defects caught |
| False-pass rate | 0.16 | 4 of 25 defects marked PASS |
| False-alarm rate | 0.40 | 10 of 25 good parts marked FAIL |
| Precision | 0.68 | 21 of 31 FAIL predictions were real defects |

|  | Predicted FAIL | Predicted PASS |
|---|---|---|
| Actual FAIL | 21 | 4 |
| Actual PASS | 10 | 15 |

REVIEW, QUOTA_ERROR and ERROR counts were all 0 in the final baseline run. An earlier 23-image batch showed 12 of 12 defects caught; the full sample did not confirm that.

## Failure analysis

### Missed defects (4 of 25)
All four were marked PASS with **0.95 confidence**. In three of them the model's reason says the visible hole or notch "appears to be a design feature", so it saw the feature but treated it as normal. In the fourth it reported no visible rust, cracks or dents. I manually reviewed three

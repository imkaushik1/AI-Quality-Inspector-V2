# Evaluation Report (n=50)

**Status:** Complete. All 50 images evaluated.
**Model:** gemini-2.5-flash (pinned). **Positive class:** FAIL (defect).
**Dataset:** 50 labeled images (25 defective, 25 good), Kaggle casting product image data.

## Results

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

REVIEW, QUOTA_ERROR and ERROR counts were all 0 in the final run. An earlier 23-image batch showed 12 of 12 defects caught; the full sample did not confirm that.

## Failure analysis

### Missed defects (4 of 25)
All four were marked PASS with **0.95 confidence**. In three of them the model's reason says the visible hole or notch "appears to be a design feature", so it saw the feature but treated it as normal. In the fourth it reported no visible rust, cracks or dents. I manually reviewed three of the four images and saw something in each; the fourth was not reviewed.

### False alarms (10 of 25)
I manually reviewed four of them; they looked normal to me. The model's reasons describe minor surface irregularities, pitting or uneven texture, rated cosmetic or minor at 0.8 to 0.9 confidence. This suggests the model treats natural casting texture as damage. The other six were not reviewed.

## What this means

1. **Confidence cannot route human review.** Wrong PASS verdicts came at 0.95 and the reviewed wrong FAIL verdicts at 0.8 to 0.9.
2. **The prompt does not define normal vs defective for castings.** It lists rust, cracks and dents, while casting defects are pinholes, blow holes and burrs. This is a hypothesis, not yet tested.
3. **Guardrail status:** false-pass rate (16%) is above the assumed hard limit of 5%, and false-alarm rate (40%) is above the assumed 20%. The current prompt does not meet the targets.

## Limitations
- Small sample, single dataset. One image changes recall by 4 points.
- Manual review covered 7 of 14 errors (3 misses, 4 false alarms).
- Targets are my assumptions, not validated with QA professionals.
- Earlier runs used a different model alias and are excluded.

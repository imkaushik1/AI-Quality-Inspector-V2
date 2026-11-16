# Evaluation Report (Partial, n=44)

**Status:** In progress. 44 of 50 images have a clean PASS or FAIL. Final numbers will replace this table after the remaining 6 images are run.
**Model:** gemini-2.5-flash (pinned). **Positive class:** FAIL (defect).
**Dataset:** 50 labeled images (25 defective, 25 good), Kaggle casting product image data.

## Results so far

| Metric | Value | Meaning |
|---|---|---|
| Clean results | 44 | 23 defective, 21 good |
| Recall | 0.87 | 20 of 23 defects caught |
| False-pass rate | 0.13 | 3 of 23 defects marked PASS |
| False-alarm rate | 0.48 | 10 of 21 good parts marked FAIL |
| Precision | 0.67 | 20 of 30 FAIL predictions were real defects |

|  | Predicted FAIL | Predicted PASS |
|---|---|---|
| Actual FAIL | 20 | 3 |
| Actual PASS | 10 | 11 |

An earlier smaller batch (n=23) showed 12 of 12 defects caught. The larger sample did not confirm that, which is why small-sample results are not reported as findings.

## Failure analysis

### Missed defects (3 of 23)
All three were marked PASS with **0.95 confidence**. I reviewed the images manually and saw something in each of them. In two cases the model's reason says the visible hole or notch "appears to be a design feature", so the model saw the feature but treated it as normal. In the third, it reported no visible rust, cracks or dents.

### False alarms (10 of 21)
I manually reviewed four of them. They looked normal to me, with no major problem. The model's reasons describe minor surface irregularities, pitting or uneven texture, and rated them cosmetic or minor at 0.8 to 0.9 confidence. This suggests the model treats natural casting texture as damage.

## What this means

1. **Confidence cannot route human review.** Wrong PASS verdicts came at 0.95 and wrong FAIL verdicts at 0.8 to 0.9.
2. **The prompt does not define normal vs defective for castings.** It lists rust, cracks and dents, but casting defects are pinholes, blow holes and burrs. This is a hypothesis, not yet tested.
3. **Guardrail status:** false-pass rate (13%) is above the assumed hard limit of 5%, and false-alarm rate (48%) is above the assumed 20% limit. The current prompt does not meet the targets.

## Limitations
- Small sample and a single dataset. One image changes recall by about 4 points.
- Manual review covered 7 images (3 misses, 4 false alarms), not all errors.
- Targets (5% and 20%) are my assumptions, not validated with QA professionals.
- Earlier runs used a different model alias and are excluded.


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
All four were marked PASS with **0.95 confidence**. In three of them the model's reason says the visible hole or notch "appears to be a design feature", so it saw the feature but treated it as normal. In the fourth it reported no visible rust, cracks or dents. I manually reviewed three of the four images and saw something in each; the fourth was not reviewed.

### False alarms (10 of 25)
I manually reviewed four of them; they looked normal to me. The model's reasons describe minor surface irregularities, pitting or uneven texture, rated cosmetic or minor at 0.8 to 0.9 confidence. This suggests the model treats natural casting texture as damage. The other six were not reviewed.

## Prompt B follow-up (paired, n=47)

| Metric | Prompt A | Prompt B |
|---|---|---|
| Missed defects | 4 of 25 (16%) | 2 of 25 (8%) |
| False alarms | 10 of 22 (45%) | 3 of 22 (14%) |

B fixed 3 of A's 4 misses but introduced one new miss at 0.95 confidence. One defect (`cast_def_0_9163`) was missed by both prompts. A's false-alarm rate is 45% here (22 good images) versus 40% above (25 good images) because the paired comparison uses only the 47 images evaluated on both prompts. Details: [experiment memo](experiment_memo.md).

## What this means

1. **Confidence cannot route human review.** Wrong PASS verdicts came at 0.95 and the reviewed wrong FAIL verdicts at 0.8 to 0.9.
2. **The prompt does not define normal vs defective for castings.** It lists rust, cracks and dents, while casting defects are pinholes, blow holes and burrs. A casting-aware Prompt B tested this: it cut false alarms from 45% to 14% on 47 paired images, which supports the hypothesis, with the caveat that B was written after seeing these errors.
3. **Guardrail status:** baseline false-pass rate (16%) is above the assumed hard limit of 5%, and false-alarm rate (40%) is above the assumed 20%. Prompt B meets the false-alarm target (14%) but still misses the false-pass target (8%).

## Limitations
- Small sample, single dataset. One image changes recall by 4 points.
- Manual review covered 7 of 14 baseline errors (3 misses, 4 false alarms).
- Targets are my assumptions, not validated with QA professionals.
- Prompt B was evaluated on 47 of 50 images (3 not run because of API quota) and was written after seeing A's errors on the same images, so its gain is likely overstated.
- Earlier runs used a different model alias and are excluded.

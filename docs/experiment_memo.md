# Experiment Memo: Prompt A vs Prompt B

**Type:** Offline, paired comparison (same images, same model gemini-2.5-flash).
**Sample:** 47 of 50 images (25 defective, 22 good). 3 good images were not evaluated on B because of API quota.

## Hypothesis
Baseline prompt A treats natural casting texture as damage and dismisses holes and notches as design features. A prompt B that defines normal casting texture and names real casting defects will cut false alarms without raising missed defects.

## Result (paired, n=47)

| Metric | Prompt A | Prompt B |
|---|---|---|
| Missed defects (false-pass) | 4 of 25 (16%) | 2 of 25 (8%) |
| False alarms | 10 of 22 (45%) | 3 of 22 (14%) |
| Recall | 84% | 92% |

A and B disagreed on 13 images: B fixed 11 and made 2 worse. Both prompts missed `cast_def_0_9163`.

## Guardrails (my assumed targets)
- False-alarm under 20%: met by B (14%).
- False-pass under 5%: not met by B (8%), though half of A.

## Findings
1. B fixed 3 of A's 4 misses (hole or notch called a "design feature") and most false alarms.
2. B introduced one new miss (`cast_def_0_5205`) at 0.95 confidence. Confidence stays unreliable under both prompts.
3. One defect is missed by both prompts, so a prompt alone is not enough. Reference images or SOPs (RAG) are the next idea.

## Decision
**Iterate, do not ship.** B beats A on both metrics but still misses the false-pass guardrail. Keep human review for PASS verdicts on risky parts.

## Limitations
- B was written after seeing A's errors on the same images, so the improvement is likely overstated.
- Small sample, one dataset. One image moves recall by 4 points.
- 3 images were not evaluated on B.
- Targets are assumptions, not validated with QA professionals.

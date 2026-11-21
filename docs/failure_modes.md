# Failure Modes and Guardrails

| # | Failure mode | Example | Severity | Guardrail / fallback |
|---|---|---|---|---|
| 1 | Missed defect (wrong PASS) | Baseline A: 4 of 25 defective parts marked PASS (16%). Prompt B: 2 of 25 (8%, n=47 paired) | Critical | Track false-pass rate as a hard limit (target under 5%); send risky cases to human review |
| 2 | False alarm (wrong FAIL) | Baseline A: 10 of 25 good castings flagged FAIL for minor surface irregularities (40%). Prompt B cut this to 3 of 22 (14%, n=47 paired) | Medium | Casting-aware Prompt B; keep measuring false-alarm rate |
| 3 | Overconfident output | All 4 baseline wrong PASS verdicts at 0.95; Prompt B's misses also at 0.95; wrong FAIL at 0.8 to 0.9 in the baseline errors reviewed | High | Do not route on confidence alone |
| 4 | Unparseable model output | Response is not valid JSON | Low | Status set to REVIEW, not PASS |
| 5 | API quota exhausted | Free tier limit of 20 requests per day | Medium | Stop early with a clear message; run evaluation in daily batches |
| 6 | Timeout or network error | Request hangs | Medium | 60 second timeout, status ERROR with real error text |
| 7 | Plausible but wrong reason text | Reason says a hole is a "design feature" | Medium | Treat reason as a hint, not proof; reviewer confirms |
| 8 | Defect missed by every prompt | `cast_def_0_9163` was missed by both Prompt A and Prompt B | High | Human review for PASS on risky parts; reference images or SOPs (RAG) are a planned next step |
| 9 | Different lighting or angle | Image differs from the eval set | Unknown | Not tested yet; listed as a limitation |

## Fallback rule
If the tool returns ERROR, QUOTA_ERROR or REVIEW, the part goes to manual inspection. The tool never auto-passes a part it could not assess.

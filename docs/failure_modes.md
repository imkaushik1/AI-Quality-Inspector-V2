# Failure Modes and Guardrails

| # | Failure mode | Example | Severity | Guardrail / fallback |
|---|---|---|---|---|
| 1 | Missed defect (wrong PASS) | Defective part marked PASS with 0.95 confidence in an earlier run | Critical | Track false-pass rate as a hard limit; send risky cases to human review |
| 2 | False alarm (wrong FAIL) | Good casting flagged for minor surface irregularities (4 of 11 in early batch) | Medium | Prompt B with a clearer definition of normal texture; measure false-alarm rate |
| 3 | Overconfident output | Wrong verdicts at 0.8 to 0.95 confidence | High | Do not route on confidence alone |
| 4 | Unparseable model output | Response is not valid JSON | Low | Status set to REVIEW, not PASS |
| 5 | API quota exhausted | Free tier limit of 20 requests per day | Medium | Stop early with a clear message; run evaluation in daily batches |
| 6 | Timeout or network error | Request hangs | Medium | 60 second timeout, status ERROR with real error text |
| 7 | Plausible but wrong reason text | Reason describes damage that is not there | Medium | Treat reason as a hint, not proof; reviewer confirms |
| 8 | Different lighting or angle | Image differs from the eval set | Unknown | Not tested yet; listed as a limitation |

## Fallback rule
If the tool returns ERROR, QUOTA_ERROR or REVIEW, the part goes to manual inspection. The tool never auto-passes a part it could not assess.

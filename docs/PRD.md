# Product Requirements Document: AI Quality Inspector

**Owner:** Himanshu Sharma | **Status:** Draft v1 (eval in progress)

## 1. Overview
An LLM-based tool that inspects images of cast metal parts and returns a structured verdict (PASS / FAIL / REVIEW, defect type, severity, confidence, reason). It works without training a custom vision model.

## 2. User
**Primary user:** QA supervisor at a small casting or machining shop (30-100 people, 2-4 production lines, no ML or data team).
*Assumption: based on my own research, not yet validated with real QA professionals.*

**Today:** Inspectors check parts visually and log results on paper or in Excel.

## 3. Problem
Manual inspection in small casting shops is slow and inconsistent, and traditional camera-AI needs thousands of labeled images and retraining for every new part. LLM-based inspection works without training, but it can be confidently wrong (a wrong PASS or a wrong FAIL), so it must run with human review.

## 4. Goals
- Catch as many real defects as possible before parts ship.
- Keep false alarms low enough that inspectors still save time.
- Give every inspection a structured, reviewable record.

## 5. Non-goals (for now)
- Real-time conveyor or PLC integration
- Edge deployment or sub-second latency
- Replacing human inspectors on safety-critical parts
- Multi-material or multi-industry support

## 6. Success metrics

| Type | Metric | Definition | Target (assumption) | Current (early, n=23) |
|---|---|---|---|---|
| North Star | Defect catch rate (recall) | Defective parts correctly flagged / all defective parts | As high as possible | 12 of 12 |
| Guardrail (hard limit) | False-pass rate | Defective parts marked PASS / all defective parts | Near 0, never above 5% | 0 of 12 |
| Guardrail | False-alarm rate | Good parts marked FAIL / all good parts | Under 20% | 4 of 11 (36%) |
| Guardrail | Cost per inspection | API cost per image | Not measured yet | n/a |
| Guardrail | Latency | Seconds per image | Not measured yet | n/a |

*Targets are assumptions to be validated with QA users. Early numbers come from a small, partly complete eval and are not a production claim.*

## 7. Requirements
- Structured JSON output: status, defect type, severity, confidence, reason
- Unparseable or failed responses go to REVIEW or ERROR, never silently PASS
- Downloadable CSV report
- Automated eval pipeline on a labeled set (recall, precision, false-pass, false-alarm)
- Planned: human review screen, SQLite logging, offline prompt A/B test

## 8. Evidence so far
- Eval set: 50 labeled images (25 defective, 25 good), Kaggle casting dataset. Model: gemini-2.5-flash.
- Early batch: all defects caught, but 4 of 11 good parts flagged FAIL for minor surface irregularities.
- Earlier run (different model alias): one defective part marked PASS with 0.95 confidence, so confidence alone is not a safe routing rule.
- Final numbers will be added after all 50 images are evaluated.

## 9. Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Missed defect (wrong PASS) | Defective part reaches customer | Hard limit on false-pass rate; human review for risky cases |
| Over-flagging natural casting texture | Inspectors lose time, distrust the tool | Prompt B experiment with a clear definition of normal vs defective |
| Overconfident outputs | Confidence cannot be used alone for routing | Review rules beyond confidence |
| Free-tier quota and timeouts | Slow or interrupted evaluation | Batched runs, pinned model, timeouts |
| Deprecated SDK | Future breakage | Migrate to google-genai |
| Small, single-dataset eval | Results may not generalize | Report n= and limitations honestly |

## 10. Open questions
- What false-alarm rate would real QA supervisors accept?
- How many seconds per part does manual inspection take today?
- What does one missed defect cost a typical shop?

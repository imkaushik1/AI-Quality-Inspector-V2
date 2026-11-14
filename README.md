# AI Quality Inspector

LLM-based defect inspection for small casting shops, with eval-driven quality checks.

## Problem and user

Small casting and machining shops rely on manual visual inspection. It is slow, inconsistent between inspectors, and tiring, so small defects (pinholes, blow holes, burrs) get missed. Traditional camera-AI needs thousands of labeled images and retraining for every new part, which these shops cannot afford.

**Primary user:** QA supervisor at a small casting or machining shop (30-100 people, no ML team).

**Key concern:** a defective part that reaches the customer costs far more than a false alarm. So the main guardrail metric is the **false-pass rate** (defects wrongly marked PASS).

## What it does

Upload a part image -> Gemini returns structured JSON (status, defect type, severity, confidence, reason) -> PASS / FAIL / REVIEW result -> downloadable CSV report.

## Evaluation (in progress)

- Dataset: 50 labeled images (25 defective, 25 good) sampled from a public casting-defect dataset (Kaggle, casting product image data).
- Model: gemini-2.5-flash (pinned). FAIL is the positive class.
- Metrics: recall, precision, false-pass rate, false-alarm rate, confusion matrix. REVIEW and API errors are counted separately.
- Status: running in daily batches because the free API tier allows only 20 requests per day.

Final results table: coming soon (will be reported with n= and class split).

## Key finding so far

On one defective part, the model answered PASS with 0.95 confidence. So confidence alone is not a safe rule for deciding what goes to human review.

## Limitations

- Small sample (50 images) and a single dataset (casting), so results are an early signal, not a production claim.
- Free-tier quota (20 requests/day) forced batched evaluation.
- The gemini-flash-latest alias caused request timeouts, so the model is pinned to a fixed version.
- Uses the deprecated google-generativeai SDK; migration to google-genai is planned.

## Roadmap

- Now: finish the 50-image eval and write the eval report.
- Next: human review screen, SQLite logging and SQL analytics, prompt A/B test (offline).
- Later: RAG over inspection SOPs, migrate to google-genai SDK, edge deployment.

## Built by

Himanshu Sharma, aspiring AI Product Manager. Product owner for problem definition, metrics and evaluation design; code built with AI assistance.

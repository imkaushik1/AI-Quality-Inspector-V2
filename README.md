# 🏭 AI Quality Inspector

### LLM-based defect inspection for small casting shops, with eval-driven quality checks

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red) ![Model](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-green) ![Status](https://img.shields.io/badge/Status-Eval%20complete-brightgreen)

🚀 **Live demo:** https://ai-quality-inspector-pro.streamlit.app/

📄 **Docs:** [PRD](docs/PRD.md) | [Eval report](docs/eval_report.md) | [Experiment memo](docs/experiment_memo.md) | [Failure modes](docs/failure_modes.md)

---

## 🛑 The Problem

- **Manual inspection is slow and inconsistent:** inspectors tire, and small defects (pinholes, blow holes, burrs) get missed.
- **Traditional camera-AI is rigid:** it needs thousands of labeled images and retraining for every new part.
- **Small shops cannot afford that:** no ML team, no labeled data.

**Primary user (assumption, not yet validated with QA professionals):** QA supervisor at a small casting or machining shop (30-100 people, no ML team).

**Key concern:** a defective part reaching the customer costs far more than a false alarm. So the main guardrail metric is the **false-pass rate** (defects wrongly marked PASS).

---

## 💡 What It Does

| Step | What happens |
|---|---|
| 📷 Input | Upload an image of a casting part |
| 🧠 Processing | Gemini analyses the image and returns structured JSON |
| 📋 Output | Status (PASS / FAIL / REVIEW), defect type, severity, confidence, reason |
| 📥 Report | Downloadable CSV of all inspections |

---

## 📊 Evaluation

| Item | Detail |
|---|---|
| Dataset | 50 labeled images (25 defective, 25 good), Kaggle casting product image data |
| Model | gemini-2.5-flash (pinned), FAIL = positive class |
| Metrics | Recall, precision, false-pass rate, false-alarm rate, confusion matrix |
| Handling errors | REVIEW and API errors are counted separately (0 in the final run) |
| Status | Baseline A: 50 of 50 images. Prompt B: 47 of 50 (API quota). Run in daily batches (free tier: 20 requests/day) |

| Metric (baseline A) | Result (n=50) |
|---|---|
| Recall | 84% (21 of 25 defects caught) |
| False-pass rate | 16% (4 of 25 defects marked PASS) |
| False-alarm rate | 40% (10 of 25 good parts marked FAIL) |
| Precision | 68% (21 of 31 FAIL predictions were real defects) |

Against my assumed targets (false-pass under 5%, false-alarm under 20%), the baseline prompt misses both. Details in the [eval report](docs/eval_report.md).

**Prompt experiment (offline A/B, paired on 47 images):** a casting-aware prompt B cut false alarms from 45% to 14% and missed defects from 16% to 8%, but still misses the 5% false-pass target and was tuned on the same images, so the gain is likely overstated. See the [experiment memo](docs/experiment_memo.md).

---

## 🔍 Key Findings

- All 4 missed defects were marked PASS at **0.95 confidence**. Confidence alone is not a safe rule for human-review routing.
- In 3 of those 4 misses, the model's reason says a visible hole or notch "appears to be a design feature": it saw the feature but treated it as normal.
- 10 of 25 good parts were flagged FAIL for minor surface irregularities, so the prompt likely treated natural casting texture as damage. Prompt B, which defines normal casting texture, cut this to 14% (see the experiment memo).
- An earlier 23-image batch looked better (12 of 12 defects caught). The full sample did not confirm it, a reminder that small samples mislead.
- Prompt B still missed 2 defects at 0.95 confidence, and one defect (`cast_def_0_9163`) was missed by both prompts, so a prompt alone is not enough.

---

## ⚠️ Limitations

- Small sample (50 images) and a single dataset: results are an early signal, not a production claim. One image moves recall by 4 points.
- Targets (5% and 20%) are my assumptions, not validated with QA professionals.
- Prompt B was evaluated on 47 of 50 images (3 not run because of API quota) and was written after seeing A's errors on the same images, so the gain is likely overstated.
- Free-tier quota (20 requests/day) forced batched evaluation.
- gemini-flash-latest timed out during testing, so the model is pinned to a fixed version.
- Uses the deprecated google-generativeai SDK; migration to google-genai is planned.

---

## 👨‍💻 Built By

**Himanshu Sharma**
*Aspiring AI Product Manager.*

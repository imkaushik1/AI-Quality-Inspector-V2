# 🏭 AI Quality Inspector

### LLM-based defect inspection for small casting shops, with eval-driven quality checks

![Python](https://img.shields.io/badge/Python-3.13-blue) ![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-red) ![Model](https://img.shields.io/badge/Model-Gemini%202.5%20Flash-green) ![Status](https://img.shields.io/badge/Status-Eval%20in%20progress-orange)

🚀 **Live demo:** https://ai-quality-inspector-pro.streamlit.app/

📄 **Docs:** [PRD](docs/PRD.md) | [Failure modes](docs/failure_modes.md)

---

## 🛑 The Problem

- **Manual inspection is slow and inconsistent:** inspectors tire, and small defects (pinholes, blow holes, burrs) get missed.
- **Traditional camera-AI is rigid:** it needs thousands of labeled images and retraining for every new part.
- **Small shops cannot afford that:** no ML team, no labeled data.

**Primary user:** QA supervisor at a small casting or machining shop (30-100 people, no ML team).

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

## 📊 Evaluation (in progress)

| Item | Detail |
|---|---|
| Dataset | 50 labeled images (25 defective, 25 good), Kaggle casting product image data |
| Model | gemini-2.5-flash (pinned), FAIL = positive class |
| Metrics | Recall, precision, false-pass rate, false-alarm rate, confusion matrix |
| Handling errors | REVIEW and API errors are counted separately |
| Status | Running in daily batches (free tier: 20 requests/day) |

**Final results table: coming soon** (will be reported with n= and class split).

---

## 🔍 Key Finding So Far

On one defective part, the model answered **PASS with 0.95 confidence**. Confidence alone is therefore not a safe rule for deciding what goes to human review.

---

## ⚠️ Limitations

- Small sample (50 images) and a single dataset, so results are an early signal, not a production claim.
- Free-tier quota (20 requests/day) forced batched evaluation.
- The gemini-flash-latest alias caused request timeouts, so the model is pinned to a fixed version.
- Uses the deprecated google-generativeai SDK; migration to google-genai is planned.

---

## 👨‍💻 Built By

**Himanshu Sharma**

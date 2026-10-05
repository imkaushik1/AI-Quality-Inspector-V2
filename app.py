import streamlit as st
import google.generativeai as genai
from PIL import Image
import pandas as pd
import time
import json

# --- 1. Page Configuration ---
st.set_page_config(page_title="Quality Inspector AI", page_icon="🏭", layout="wide")
st.title("🏭 Quality Inspector AI")
st.markdown("### Automated Defect Detection System")
st.write("Upload images of mechanical parts to inspect for defects (Rust, Cracks, etc.)")

# --- 2. API Key Authentication ---
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("🚨 Error: API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# --- 3. Model Configuration ---
current_model = "gemini-2.5-flash"

# Sidebar Information
with st.sidebar:
    st.header("System Status")
    st.success("✅ Server Online")
    st.info(f"🤖 Active Model: `{current_model}`")


def parse_inspection_json(text):
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```", 2)[1]
        if cleaned.lower().startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    data = json.loads(cleaned)
    status = str(data.get("status", "")).strip().upper()
    if status not in ("PASS", "FAIL"):
        raise ValueError("Invalid status")

    confidence = data.get("confidence", "")
    try:
        confidence = float(confidence)
    except (TypeError, ValueError):
        confidence = ""

    return {
        "status": status,
        "defect_type": str(data.get("defect_type", "")).strip(),
        "severity": str(data.get("severity", "")).strip(),
        "confidence": confidence,
        "reason": str(data.get("reason", "")).strip(),
    }


# --- 4. Main Application Loop ---
uploaded_files = st.file_uploader("Upload Component Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.info("ℹ️ Note: Processing speed is optimized to prevent API errors.")

    if st.button(f"Start Inspection for {len(uploaded_files)} Items"):

        st.divider()
        st.subheader("🔍 Inspection Results")

        model = genai.GenerativeModel(current_model)
        inspection_results = []

        prompt = """
        Analyze this industrial image for defects (rust, cracks, dents, damage).
        Return only JSON with these keys:
        status: PASS or FAIL
        defect_type: rust, crack, dent, none, other
        severity: none, cosmetic, minor, critical
        confidence: a number from 0 to 1
        reason: one short sentence
        """

        for file in uploaded_files:
            col1, col2 = st.columns([1, 2])

            img = Image.open(file)
            col1.image(img, caption=file.name, use_container_width=True)

            with col2:
                with st.spinner("Analyzing component..."):
                    status = "ERROR"
                    defect_type = ""
                    severity = ""
                    confidence = ""
                    reason = ""
                    max_attempts = 3

                    for attempt in range(max_attempts):
                        try:
                            response = model.generate_content([prompt, img])
                            text = response.text.strip()
                            try:
                                parsed = parse_inspection_json(text)
                                status = parsed["status"]
                                defect_type = parsed["defect_type"]
                                severity = parsed["severity"]
                                confidence = parsed["confidence"]
                                reason = parsed["reason"]
                            except Exception:
                                status = "REVIEW"
                                defect_type = ""
                                severity = ""
                                confidence = ""
                                reason = "Could not parse model output."

                            if status == "PASS":
                                st.success("**STATUS: PASS**")
                            elif status == "FAIL":
                                st.error("**STATUS: FAIL**")
                            else:
                                st.warning("⚠️ Manual Review Needed")

                            st.write(f"**Defect type:** {defect_type or '—'}")
                            st.write(f"**Severity:** {severity or '—'}")
                            st.write(f"**Confidence:** {confidence if confidence != '' else '—'}")
                            if reason:
                                st.caption(reason)
                            break

                        except Exception as e:
                            err_msg = str(e)
                            if "429" in err_msg and attempt < max_attempts - 1:
                                time.sleep(5)
                                continue

                            if "429" in err_msg:
                                st.error("⚠️ Quota Limit Reached. Please use a new API Key.")
                                status = "QUOTA_ERROR"
                                reason = "Daily limit reached."
                            else:
                                st.error(f"Error: {err_msg}")
                                status = "ERROR"
                                reason = err_msg

                    inspection_results.append({
                        "File Name": file.name,
                        "Status": status,
                        "Defect Type": defect_type,
                        "Severity": severity,
                        "Confidence": confidence,
                        "Details": reason
                    })

        # --- 5. Final Report ---
        if inspection_results:
            st.divider()
            st.subheader("📋 Final Report Summary")

            df = pd.DataFrame(inspection_results)
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Inspection Report (CSV)",
                data=csv,
                file_name="inspection_report.csv",
                mime="text/csv",
            )

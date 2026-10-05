import streamlit as st
from PIL import Image
import pandas as pd

from inspector import MODEL_NAME, get_api_key, inspect_image

# --- 1. Page Configuration ---
st.set_page_config(page_title="Quality Inspector AI", page_icon="🏭", layout="wide")
st.title("🏭 Quality Inspector AI")
st.markdown("### Automated Defect Detection System")
st.write("Upload images of mechanical parts to inspect for defects (Rust, Cracks, etc.)")

# --- 2. API Key Authentication ---
if not get_api_key():
    st.error("🚨 Error: API Key not found. Please add GOOGLE_API_KEY to Streamlit Secrets.")
    st.stop()

# --- 3. Model Configuration ---
current_model = MODEL_NAME

# Sidebar Information
with st.sidebar:
    st.header("System Status")
    st.success("✅ Server Online")
    st.info(f"🤖 Active Model: `{current_model}`")


# --- 4. Main Application Loop ---
uploaded_files = st.file_uploader("Upload Component Images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    st.info("ℹ️ Note: Processing speed is optimized to prevent API errors.")

    if st.button(f"Start Inspection for {len(uploaded_files)} Items"):

        st.divider()
        st.subheader("🔍 Inspection Results")

        inspection_results = []

        for file in uploaded_files:
            col1, col2 = st.columns([1, 2])

            img = Image.open(file)
            col1.image(img, caption=file.name, use_container_width=True)

            with col2:
                with st.spinner("Analyzing component..."):
                    parsed = inspect_image(img)
                    status = parsed["status"]
                    defect_type = parsed["defect_type"]
                    severity = parsed["severity"]
                    confidence = parsed["confidence"]
                    reason = parsed["reason"]

                    if status == "PASS":
                        st.success("**STATUS: PASS**")
                    elif status == "FAIL":
                        st.error("**STATUS: FAIL**")
                    elif status == "QUOTA_ERROR":
                        st.error("⚠️ Quota Limit Reached. Please use a new API Key.")
                    elif status == "ERROR":
                        st.error(f"Error: {reason}")
                    else:
                        st.warning("⚠️ Manual Review Needed")

                    if status in ("PASS", "FAIL", "REVIEW"):
                        st.write(f"**Defect type:** {defect_type or '—'}")
                        st.write(f"**Severity:** {severity or '—'}")
                        st.write(f"**Confidence:** {confidence if confidence != '' else '—'}")
                        if reason:
                            st.caption(reason)

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

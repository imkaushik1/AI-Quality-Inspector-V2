import json
import os
import time
from pathlib import Path

import google.generativeai as genai

MODEL_NAME = "gemini-flash-latest"
PROMPT = """
        Analyze this industrial image for defects (rust, cracks, dents, damage).
        Return only JSON with these keys:
        status: PASS or FAIL
        defect_type: rust, crack, dent, none, other
        severity: none, cosmetic, minor, critical
        confidence: a number from 0 to 1
        reason: one short sentence
        """


def _parse_secrets_toml(path):
    if not path.is_file():
        return ""

    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        if key.strip() != "GOOGLE_API_KEY":
            continue
        return value.strip().strip('"').strip("'")
    return ""


def get_api_key():
    env_key = os.environ.get("GOOGLE_API_KEY", "").strip()
    if env_key:
        return env_key

    secrets_path = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"
    file_key = _parse_secrets_toml(secrets_path).strip()
    if file_key:
        return file_key

    try:
        import streamlit as st

        if "GOOGLE_API_KEY" in st.secrets:
            return str(st.secrets["GOOGLE_API_KEY"]).strip()
    except Exception:
        pass

    return ""


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


def _result(status, defect_type="", severity="", confidence="", reason=""):
    return {
        "status": status,
        "defect_type": defect_type,
        "severity": severity,
        "confidence": confidence,
        "reason": reason,
    }


def inspect_image(img):
    api_key = get_api_key()
    if not api_key:
        return _result("ERROR", reason="API Key not found.")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)
    max_attempts = 3

    for attempt in range(max_attempts):
        try:
            response = model.generate_content([PROMPT, img])
            text = response.text.strip()
            try:
                return parse_inspection_json(text)
            except Exception:
                return _result("REVIEW", reason="Could not parse model output.")
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg and attempt < max_attempts - 1:
                time.sleep(5)
                continue

            if "429" in err_msg:
                return _result("QUOTA_ERROR", reason=err_msg)
            return _result("ERROR", reason=err_msg)

    return _result("ERROR", reason="Inspection failed.")

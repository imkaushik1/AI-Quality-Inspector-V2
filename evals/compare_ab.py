import sqlite3
from pathlib import Path

import pandas as pd

R = Path(__file__).resolve().parent / "results"
CLEAN = ["PASS", "FAIL"]

a = pd.read_csv(R / "predictions.csv")
b = pd.read_csv(R / "predictions_B.csv")
a = a[a["predicted_status"].isin(CLEAN)][["filename", "label", "predicted_status", "confidence"]]
b = b[b["predicted_status"].isin(CLEAN)][["filename", "label", "predicted_status", "confidence"]]

conn = sqlite3.connect(":memory:")
a.to_sql("a", conn, index=False)
b.to_sql("b", conn, index=False)

Q1 = """
SELECT 'A' AS prompt,
       COUNT(*) AS images,
       SUM(a.label = 'FAIL') AS defects,
       SUM(a.label = 'FAIL' AND a.predicted_status = 'PASS') AS missed,
       SUM(a.label = 'PASS') AS good,
       SUM(a.label = 'PASS' AND a.predicted_status = 'FAIL') AS false_alarms
FROM a JOIN b ON a.filename = b.filename
UNION ALL
SELECT 'B',
       COUNT(*),
       SUM(b.label = 'FAIL'),
       SUM(b.label = 'FAIL' AND b.predicted_status = 'PASS'),
       SUM(b.label = 'PASS'),
       SUM(b.label = 'PASS' AND b.predicted_status = 'FAIL')
FROM a JOIN b ON a.filename = b.filename
"""

Q2 = """
SELECT a.filename, a.label, a.predicted_status AS a_pred, b.predicted_status AS b_pred,
       a.confidence AS a_conf, b.confidence AS b_conf
FROM a JOIN b ON a.filename = b.filename
WHERE a.predicted_status != b.predicted_status
ORDER BY a.label
"""

Q3 = """
SELECT filename, label, predicted_status, confidence
FROM b
WHERE label != predicted_status
ORDER BY confidence DESC
"""

out = []
for title, q in [
    ("1. Paired comparison (same images, both prompts clean)", Q1),
    ("2. Images where A and B disagree", Q2),
    ("3. B errors (wrong verdicts), highest confidence first", Q3),
]:
    df = pd.read_sql_query(q, conn)
    out.append(title + "\n" + (df.to_string(index=False) if len(df) else "(none)") + "\n")

text = "\n".join(out)
print(text)
(R / "ab_comparison.txt").write_text(text, encoding="utf-8")
print("Saved to", R / "ab_comparison.txt")

import argparse
import sys
import time
from pathlib import Path

import pandas as pd
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from inspector import inspect_image

EVAL_DIR = Path(__file__).resolve().parent
IMAGES_DIR = EVAL_DIR / "images"
LABELS_PATH = EVAL_DIR / "labels.csv"
RESULTS_DIR = EVAL_DIR / "results"
PREDICTIONS_PATH = RESULTS_DIR / "predictions.csv"
SUMMARY_PATH = RESULTS_DIR / "summary.md"
PREDICTION_COLUMNS = [
    "filename",
    "label",
    "predicted_status",
    "defect_type",
    "severity",
    "confidence",
    "reason",
]


def _fmt_rate(value):
    if value is None:
        return "n/a"
    return f"{value:.4f}"


def _rate(numerator, denominator):
    if denominator == 0:
        return None
    return numerator / denominator


SHUFFLE_SEED = 42


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum number of labeled images to consider after shuffle (if any) and --skip",
    )
    parser.add_argument(
        "--skip",
        type=int,
        default=0,
        help="Number of labeled images to skip from the start (after shuffle, if any)",
    )
    parser.add_argument(
        "--shuffle",
        action="store_true",
        help=(
            f"Shuffle labeled images with fixed seed {SHUFFLE_SEED} before --skip/--limit "
            "so batches mix FAIL and PASS. Deterministic across runs."
        ),
    )
    return parser.parse_args()


def load_existing_predictions():
    if not PREDICTIONS_PATH.is_file():
        return pd.DataFrame(columns=PREDICTION_COLUMNS)

    existing = pd.read_csv(PREDICTIONS_PATH)
    for column in PREDICTION_COLUMNS:
        if column not in existing.columns:
            existing[column] = ""
    return existing[PREDICTION_COLUMNS]


def write_summary(predictions):
    total = len(predictions)
    review_count = int((predictions["predicted_status"] == "REVIEW").sum()) if total else 0
    quota_error_count = int((predictions["predicted_status"] == "QUOTA_ERROR").sum()) if total else 0
    error_count = int((predictions["predicted_status"] == "ERROR").sum()) if total else 0
    unclean_count = review_count + quota_error_count + error_count
    scored = predictions[predictions["predicted_status"].isin(["PASS", "FAIL"])] if total else predictions

    tp = int(((scored["predicted_status"] == "FAIL") & (scored["label"] == "FAIL")).sum()) if total else 0
    fp = int(((scored["predicted_status"] == "FAIL") & (scored["label"] == "PASS")).sum()) if total else 0
    tn = int(((scored["predicted_status"] == "PASS") & (scored["label"] == "PASS")).sum()) if total else 0
    fn = int(((scored["predicted_status"] == "PASS") & (scored["label"] == "FAIL")).sum()) if total else 0

    recall = _rate(tp, tp + fn)
    precision = _rate(tp, tp + fp)
    false_pass_rate = _rate(fn, tp + fn)
    false_alarm_rate = _rate(fp, fp + tn)

    unclean_share = unclean_count / total if total else 0
    if unclean_share > 0.10:
        print(
            f"WARNING: {unclean_count}/{total} images ({unclean_share:.1%}) "
            "did not get a clean PASS or FAIL (REVIEW, QUOTA_ERROR, or ERROR)."
        )

    summary = f"""# Evaluation Summary

Positive class: **FAIL**

| Metric | Value |
| --- | --- |
| Images | {total} |
| Clean PASS/FAIL | {len(scored)} |
| REVIEW | {review_count} |
| QUOTA_ERROR | {quota_error_count} |
| ERROR | {error_count} |
| Recall | {_fmt_rate(recall)} |
| Precision | {_fmt_rate(precision)} |
| False-pass rate | {_fmt_rate(false_pass_rate)} |
| False-alarm rate | {_fmt_rate(false_alarm_rate)} |

## Confusion matrix (clean PASS/FAIL only)

|  | Predicted FAIL | Predicted PASS |
| --- | --- | --- |
| Actual FAIL | {tp} | {fn} |
| Actual PASS | {fp} | {tn} |
"""
    SUMMARY_PATH.write_text(summary, encoding="utf-8")
    print(summary)
    print(f"Saved predictions to {PREDICTIONS_PATH}")
    print(f"Saved summary to {SUMMARY_PATH}")


def main():
    args = parse_args()
    labels = pd.read_csv(LABELS_PATH)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    if args.shuffle:
        labels = labels.sample(frac=1, random_state=SHUFFLE_SEED).reset_index(drop=True)
        print(f"Shuffled {len(labels)} labeled images with seed {SHUFFLE_SEED}.")
    if args.skip:
        labels = labels.iloc[args.skip :]
    if args.limit is not None:
        labels = labels.iloc[: args.limit]

    existing = load_existing_predictions()
    already_clean = set()
    if not existing.empty:
        clean = existing[existing["predicted_status"].isin(["PASS", "FAIL"])]
        already_clean = set(clean["filename"].astype(str))

    work = []
    for _, row in labels.iterrows():
        filename = str(row["filename"])
        if filename in already_clean:
            continue
        work.append(row)

    new_rows = []
    consecutive_quota = 0
    stopped_early = False

    for i, row in enumerate(work):
        filename = str(row["filename"])
        expected = str(row["label"]).strip().upper()
        image_path = IMAGES_DIR / filename

        if not image_path.is_file():
            result = {
                "status": "ERROR",
                "defect_type": "",
                "severity": "",
                "confidence": "",
                "reason": f"Image not found: {image_path}",
            }
        else:
            with Image.open(image_path) as img:
                result = inspect_image(img)

        new_rows.append({
            "filename": filename,
            "label": expected,
            "predicted_status": result["status"],
            "defect_type": result["defect_type"],
            "severity": result["severity"],
            "confidence": result["confidence"],
            "reason": result["reason"],
        })

        if result["status"] == "QUOTA_ERROR":
            consecutive_quota += 1
            if consecutive_quota >= 3:
                stopped_early = True
                print("Stopped early: 3 QUOTA_ERRORs in a row.")
                break
        else:
            consecutive_quota = 0

        if not stopped_early and i < len(work) - 1:
            time.sleep(2)

    if new_rows:
        new_df = pd.DataFrame(new_rows, columns=PREDICTION_COLUMNS)
        rerun_names = set(new_df["filename"].astype(str))
        kept = existing[~existing["filename"].astype(str).isin(rerun_names)]
        predictions = pd.concat([kept, new_df], ignore_index=True)
    else:
        predictions = existing

    predictions.to_csv(PREDICTIONS_PATH, index=False)
    write_summary(predictions)


if __name__ == "__main__":
    main()

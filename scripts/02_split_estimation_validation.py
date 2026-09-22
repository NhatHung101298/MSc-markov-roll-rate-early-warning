"""Chia trajectory thành estimation set / validation set theo mốc lịch chung τ.

τ = mốc tháng ở percentile 80% trên trục lịch gộp (danh sách tháng liên tục từ
tháng nhỏ nhất đến lớn nhất có trong trajectory), áp dụng đồng nhất cho cả 3
vintage (không tính riêng % theo từng vintage) -- theo Ch.3 §3.2.3.

Chạy: python scripts/02_split_estimation_validation.py [--limit] [--suffix smoke|full]
"""

import argparse
import json
import logging
import os

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
DEFAULT, PREPAID = 4, 5
ESTIMATION_FRACTION = 0.8


def month_index_to_yyyymm(month_index):
    year = (month_index - 1) // 12
    month = (month_index - 1) % 12 + 1
    return year * 100 + month


def compute_tau(month_indices):
    """Moc thang o percentile 80% tren truc lich gop lien tuc."""
    all_months = list(range(int(month_indices.min()), int(month_indices.max()) + 1))
    n_months = len(all_months)
    cut_pos = int(n_months * ESTIMATION_FRACTION) - 1
    cut_pos = max(0, min(cut_pos, n_months - 1))
    tau = all_months[cut_pos]
    logger.info(
        "Trục lịch gộp: %s..%s (%d tháng). τ = tháng thứ %d = %s (YYYYMM=%d)",
        month_index_to_yyyymm(all_months[0]),
        month_index_to_yyyymm(all_months[-1]),
        n_months,
        cut_pos + 1,
        tau,
        month_index_to_yyyymm(tau),
    )
    return tau


def summarize_split(df, split_name):
    n_rows = len(df)
    n_loans = df["loan_id"].nunique()
    n_default = df.loc[df["state"] == DEFAULT, "loan_id"].nunique()
    n_prepaid = df.loc[df["state"] == PREPAID, "loan_id"].nunique()
    logger.info(
        "[%s] dòng=%d, khoản vay=%d, khoản chạm Default=%d, khoản chạm Prepaid=%d",
        split_name, n_rows, n_loans, n_default, n_prepaid,
    )
    return {"rows": n_rows, "loans": n_loans, "default_loans": n_default, "prepaid_loans": n_prepaid}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", action="store_true", help="Dùng trajectory smoke thay vì full")
    args = parser.parse_args()

    suffix = "smoke" if args.limit else "full"
    traj_path = os.path.join(DATA_DIR, f"loan_trajectory_{suffix}.parquet")
    trajectory = pd.read_parquet(traj_path)
    logger.info("Đọc %s: %d dòng", traj_path, len(trajectory))

    tau = compute_tau(trajectory["month_index"])
    trajectory["split"] = trajectory["month_index"].apply(
        lambda m: "estimation" if m <= tau else "validation"
    )

    estimation = trajectory[trajectory["split"] == "estimation"].drop(columns=["split"])
    validation = trajectory[trajectory["split"] == "validation"].drop(columns=["split"])

    est_summary = summarize_split(estimation, "estimation")
    val_summary = summarize_split(validation, "validation")

    est_path = os.path.join(DATA_DIR, f"estimation_set_{suffix}.parquet")
    val_path = os.path.join(DATA_DIR, f"validation_set_{suffix}.parquet")
    estimation.to_parquet(est_path, index=False)
    validation.to_parquet(val_path, index=False)
    logger.info("Đã lưu: %s, %s", est_path, val_path)

    manifest = {
        "tau_month_index": int(tau),
        "tau_yyyymm": month_index_to_yyyymm(tau),
        "month_range": [
            month_index_to_yyyymm(int(trajectory["month_index"].min())),
            month_index_to_yyyymm(int(trajectory["month_index"].max())),
        ],
        "estimation": est_summary,
        "validation": val_summary,
    }
    manifest_path = os.path.join(DATA_DIR, f"split_manifest_{suffix}.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    logger.info("Đã lưu manifest: %s", manifest_path)


if __name__ == "__main__":
    main()

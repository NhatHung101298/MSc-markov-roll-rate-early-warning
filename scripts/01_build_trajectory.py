"""Xây bảng quỹ đạo trạng thái theo tháng (loan_id, month, state) từ dữ liệu Freddie Mac thô.

Rời rạc hóa delinquency_status/zero_balance_code thành 6 trạng thái theo bảng ánh xạ
Ch.3 §3.2.1, áp quy tắc "sticky absorbing" (giữ bản ghi, ép state=Default/Prepaid lặp
lại đến hết dữ liệu thô một khi đã chạm ngưỡng lần đầu — không cho "cure").

Chạy: python scripts/01_build_trajectory.py [--limit N] [--chunksize C]
"""

import argparse
import logging
import os

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

RAW_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "raw")
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "processed")
VINTAGES = ["2016", "2017", "2018"]

CURRENT, DPD30, DPD60, DPD90PLUS, DEFAULT, PREPAID = 0, 1, 2, 3, 4, 5

PERF_USECOLS = [0, 1, 3, 8]  # cot 1,2,4,9 (1-based) trong DATA_DICTIONARY.md
PERF_NAMES = ["loan_id", "month", "delinquency_status", "zero_balance_code"]


def load_loan_universe(limit=None):
    """Doc loan_id tu cac file orig, gan vintage. Neu limit: lay N loan_id dau."""
    frames = []
    for v in VINTAGES:
        path = os.path.join(RAW_DIR, f"sample_orig_{v}.txt")
        df = pd.read_csv(
            path, sep="|", header=None, usecols=[19], names=["loan_id"], dtype=str
        )
        df["vintage"] = f"F{v[2:]}"
        frames.append(df)
    universe = pd.concat(frames, ignore_index=True)
    logger.info("Tổng số khoản vay (orig, 3 vintage): %d", len(universe))
    if limit:
        universe = universe.head(limit)
        logger.info("Giới hạn smoke test: chỉ lấy %d khoản vay đầu", len(universe))
    return universe


def load_perf(loan_ids, chunksize):
    """Doc perf 3 vintage theo chunk, loc theo loan_ids, tra ve 1 DataFrame."""
    loan_id_set = set(loan_ids)
    chunks = []
    for v in VINTAGES:
        path = os.path.join(RAW_DIR, f"sample_perf_{v}.txt")
        n_rows_read = 0
        for chunk in pd.read_csv(
            path,
            sep="|",
            header=None,
            usecols=PERF_USECOLS,
            names=PERF_NAMES,
            dtype=str,
            chunksize=chunksize,
        ):
            n_rows_read += len(chunk)
            chunk = chunk[chunk["loan_id"].isin(loan_id_set)]
            if not chunk.empty:
                chunks.append(chunk)
        logger.info("Đã đọc %s: %d dòng thô", os.path.basename(path), n_rows_read)
    perf = pd.concat(chunks, ignore_index=True)
    logger.info("Tổng dòng perf sau lọc theo loan universe: %d", len(perf))
    return perf


def map_raw_state(perf):
    """Anh xa (delinquency_status, zero_balance_code) -> state tho (chua ap sticky).

    Thu tu uu tien theo Ch.3 §3.2.1: Default truoc, roi Prepaid, roi delinquency thuong.
    """
    dq = perf["delinquency_status"]
    zbc = perf["zero_balance_code"].fillna("")

    dq_numeric = pd.to_numeric(dq, errors="coerce")
    is_default = (dq == "RA") | zbc.isin(["02", "03", "09"]) | (dq_numeric >= 6)
    is_prepaid = zbc == "01"

    conditions = [
        is_default,
        is_prepaid,
        dq == "00",
        dq == "01",
        dq == "02",
        dq.isin(["03", "04", "05"]),
    ]
    choices = [DEFAULT, PREPAID, CURRENT, DPD30, DPD60, DPD90PLUS]
    state_raw = np.select(conditions, choices, default=-1)

    n_unmapped = int((state_raw == -1).sum())
    if n_unmapped > 0:
        logger.warning(
            "%d dòng không map được state (delinquency_status lạ) -- kiểm tra dữ liệu", n_unmapped
        )
    perf = perf.copy()
    perf["state_raw"] = state_raw
    return perf


def apply_sticky_absorbing(perf):
    """Ep state=Default/Prepaid lap lai sau khi cham lan dau (khong cho quay lai)."""
    perf = perf.sort_values(["loan_id", "month_index"]).reset_index(drop=True)
    hit_default = perf.groupby("loan_id")["state_raw"].transform(
        lambda s: (s == DEFAULT).cummax()
    )
    hit_prepaid = perf.groupby("loan_id")["state_raw"].transform(
        lambda s: (s == PREPAID).cummax()
    )
    state = perf["state_raw"].to_numpy().copy()
    state[hit_default.to_numpy()] = DEFAULT
    # Prepaid chỉ áp nếu chưa từng Default trước đó trong cùng tháng trở về sau
    # (Default có ưu tiên tuyệt đối vì đã ép trước ở dòng trên).
    prepaid_only = hit_prepaid.to_numpy() & ~hit_default.to_numpy()
    state[prepaid_only] = PREPAID
    perf["state"] = state
    return perf


def flag_gaps(perf):
    """Danh segment_id trong moi loan_id: tang khi month_index khong lien tuc."""
    perf = perf.sort_values(["loan_id", "month_index"]).reset_index(drop=True)
    diff = perf.groupby("loan_id")["month_index"].diff()
    is_gap = (diff.notna()) & (diff != 1)
    perf["segment_id"] = is_gap.groupby(perf["loan_id"]).cumsum()
    n_gap_rows = int(is_gap.sum())
    n_gap_loans = int(perf.loc[is_gap, "loan_id"].nunique())
    logger.info("Phát hiện %d dòng có gap báo cáo trên %d khoản vay", n_gap_rows, n_gap_loans)
    return perf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="Giới hạn số khoản vay (smoke test)")
    parser.add_argument("--chunksize", type=int, default=200_000)
    args = parser.parse_args()

    os.makedirs(OUT_DIR, exist_ok=True)

    universe = load_loan_universe(limit=args.limit)
    perf = load_perf(universe["loan_id"], chunksize=args.chunksize)
    perf = perf.merge(universe, on="loan_id", how="left")

    perf["month"] = perf["month"].astype(int)
    perf["month_index"] = (perf["month"] // 100) * 12 + (perf["month"] % 100)

    perf = perf.drop_duplicates(subset=["loan_id", "month_index"])

    perf = map_raw_state(perf)
    perf = apply_sticky_absorbing(perf)
    perf = flag_gaps(perf)

    trajectory = perf[["loan_id", "vintage", "month", "month_index", "state", "segment_id"]]
    trajectory = trajectory.sort_values(["loan_id", "month_index"]).reset_index(drop=True)

    n_loans = trajectory["loan_id"].nunique()
    n_rows = len(trajectory)
    state_counts = trajectory["state"].value_counts().sort_index()
    ever_default = trajectory.loc[trajectory["state"] == DEFAULT, "loan_id"].nunique()
    ever_prepaid = trajectory.loc[trajectory["state"] == PREPAID, "loan_id"].nunique()

    logger.info("Tổng khoản vay trong trajectory: %d", n_loans)
    logger.info("Tổng dòng trajectory: %d", n_rows)
    logger.info("Phân phối state:\n%s", state_counts.to_string())
    logger.info("Khoản vay từng chạm Default: %d", ever_default)
    logger.info("Khoản vay từng chạm Prepaid: %d", ever_prepaid)

    suffix = "smoke" if args.limit else "full"
    out_path = os.path.join(OUT_DIR, f"loan_trajectory_{suffix}.parquet")
    trajectory.to_parquet(out_path, index=False)
    logger.info("Đã lưu: %s", out_path)


if __name__ == "__main__":
    main()

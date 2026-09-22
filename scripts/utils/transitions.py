"""Ghép cặp trạng thái cách nhau k tháng từ bảng quỹ đạo (Phase 1).

Hàm thuần túy, tôn trọng segment_id (không ghép cặp giả qua chỗ gap báo cáo).
Không thuộc diện DRAFT/REVIEWED/FROZEN (giống scripts/utils/markov.py).
"""

import numpy as np
import pandas as pd


def build_pair_counts(df, k, loan_col="loan_id", time_col="month_index",
                       segment_col="segment_id", state_col="state"):
    """Ghép (state_from, state_to) cho các cặp cách nhau đúng k tháng, cùng segment.

    Cùng segment_id đảm bảo không có gap ở giữa (segment_id chỉ tăng đúng tại
    chỗ month_index không liên tục -- xem scripts/01_build_trajectory.py).
    Trả về DataFrame cột [state_from, state_to, t1] -- giữ lại t1 (tháng đích,
    dạng month_index) để script gọi tự gắn nhãn giai đoạn con (VD theo năm của
    t1, đúng quy ước "tag theo tháng xảy ra chuyển" ở Ch.3 §3.2.2) mà không
    cần ghép cặp lại.
    """
    left = df[[loan_col, time_col, segment_col, state_col]].rename(
        columns={time_col: "t0", state_col: "state_from"}
    )
    right = df[[loan_col, time_col, segment_col, state_col]].rename(
        columns={time_col: "t1", state_col: "state_to"}
    )
    right = right.assign(t0=right["t1"] - k)
    pairs = left.merge(
        right, on=[loan_col, segment_col, "t0"], how="inner", suffixes=("", "_r")
    )
    return pairs[["state_from", "state_to", "t1"]]


def pairs_to_count_matrix(pairs_df, n_states=6):
    """Dem n_ij tu DataFrame cap -> numpy.ndarray (K x K)."""
    counts = np.zeros((n_states, n_states), dtype=float)
    grouped = pairs_df.groupby(["state_from", "state_to"]).size()
    for (i, j), n in grouped.items():
        counts[int(i), int(j)] = n
    return counts


def build_triple_counts(df, loan_col="loan_id", time_col="month_index",
                         segment_col="segment_id", state_col="state"):
    """Ghep bo ba trang thai lien tiep (t-2, t-1, t), cung segment (khong gap).

    Tra ve DataFrame cot [state_prev, state_mid, state_next] voi
    state_prev = trang thai tai t-2, state_mid = t-1, state_next = t --
    dung dinh dang ma lr_test_markov_order (scripts/utils/markov.py) yeu cau.
    """
    base = df[[loan_col, time_col, segment_col, state_col]]
    m0 = base.rename(columns={time_col: "t0", state_col: "state_prev"})
    m1 = base.rename(columns={time_col: "t1", state_col: "state_mid"}).assign(
        t0=lambda x: x["t1"] - 1
    )
    m2 = base.rename(columns={time_col: "t2", state_col: "state_next"}).assign(
        t0=lambda x: x["t2"] - 2
    )
    merged = m0.merge(m1, on=[loan_col, segment_col, "t0"], how="inner").merge(
        m2, on=[loan_col, segment_col, "t0"], how="inner"
    )
    return merged[["state_prev", "state_mid", "state_next"]]


def triples_to_count_matrix(triples_df, n_states=6):
    """Dem n_ijk tu DataFrame bo ba -> numpy.ndarray (K x K x K)."""
    counts = np.zeros((n_states, n_states, n_states), dtype=float)
    grouped = triples_df.groupby(["state_prev", "state_mid", "state_next"]).size()
    for (i, j, k), n in grouped.items():
        counts[int(i), int(j), int(k)] = n
    return counts

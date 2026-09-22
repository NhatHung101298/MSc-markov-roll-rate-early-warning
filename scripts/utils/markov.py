"""Hàm Markov thủ công dùng chung cho toàn pipeline (Ch.2 công thức 2.7-2.19).

Không dùng hmmlearn/lifelines/scikit-survival — mọi công thức tự cài đặt bằng
numpy/scipy theo PROJECT_BRIEF.md muc 5.
"""

import logging

import numpy as np
from scipy.stats import chi2

logger = logging.getLogger(__name__)


def mle_transition_matrix(counts, absorbing_states=()):
    """p_hat_ij = n_ij / sum_k n_ik -- cong thuc (2.10).

    counts: ma tran dem n_ij, K x K.
    absorbing_states: chi so cac trang thai hap thu, hang tuong ung bi ep
        cung thanh vector don vi (dung P thuc su la ma tran hap thu).
    Hang co tong = 0 (khong quan sat duoc lan chuyen nao) -> tra ve NaN, canh bao.
    """
    counts = np.asarray(counts, dtype=float)
    row_sums = counts.sum(axis=1, keepdims=True)
    p_hat = np.full_like(counts, np.nan)
    nonzero = row_sums[:, 0] > 0
    p_hat[nonzero] = counts[nonzero] / row_sums[nonzero]
    if not np.all(nonzero):
        logger.warning(
            "mle_transition_matrix: trang thai %s khong co quan sat chuyen nao (hang NaN)",
            np.where(~nonzero)[0].tolist(),
        )
    for i in absorbing_states:
        p_hat[i] = 0.0
        p_hat[i, i] = 1.0
    return p_hat


def matrix_power(P, n):
    """P^n -- Chapman-Kolmogorov, cong thuc (2.12)."""
    return np.linalg.matrix_power(np.asarray(P, dtype=float), n)


def frobenius_deviation(A, B):
    """Sai lech Frobenius -- cong thuc (2.13). Tra (frobenius_norm, max_abs_cell)."""
    diff = np.asarray(A, dtype=float) - np.asarray(B, dtype=float)
    return float(np.linalg.norm(diff, "fro")), float(np.max(np.abs(diff)))


def stationary_distribution(P):
    """Giai pi P = pi, sum_i pi_i = 1 -- cong thuc (2.14).

    Voi xich hap thu nhieu hon 1 trang thai hap thu, nghiem suy bien
    (khong duy nhat) -- ham chi tra MOT nghiem hop le theo lstsq; dien giai
    "suy bien tai tap hap thu" thuoc ve script goi (xem Ch.2 muc 2.4.4).
    """
    P = np.asarray(P, dtype=float)
    k = P.shape[0]
    A = np.vstack([P.T - np.eye(k), np.ones((1, k))])
    b = np.zeros(k + 1)
    b[-1] = 1.0
    pi, *_ = np.linalg.lstsq(A, b, rcond=None)
    return pi


def forecast_distribution(mu0, P, t):
    """mu^(t0) P^(t-t0) -- phan phoi du bao huu han ky (Ch.3 muc 3.4.4)."""
    return np.asarray(mu0, dtype=float) @ matrix_power(P, t)


def fundamental_matrix(Q):
    """N = (I - Q)^-1 -- cong thuc (2.16)."""
    Q = np.asarray(Q, dtype=float)
    return np.linalg.inv(np.eye(Q.shape[0]) - Q)


def absorption_probabilities(N, R):
    """B = N R -- cong thuc (2.18)."""
    return np.asarray(N, dtype=float) @ np.asarray(R, dtype=float)


def pd_finite_horizon(N, R, Q, H):
    """PD_i(H) = (I - Q^H) N R -- cong thuc (2.19), dung cho backtest H thang."""
    Q = np.asarray(Q, dtype=float)
    QH = matrix_power(Q, H)
    return (np.eye(Q.shape[0]) - QH) @ absorption_probabilities(N, R)


def chi2_homogeneity_test(counts_list, alpha=0.05):
    """Kiem dinh thuan nhat theo thoi gian (Anderson-Goodman LR test) -- Ch.2 muc 2.6.

    counts_list: danh sach ma tran dem n_ij(g), moi phan tu la mot giai doan con,
        cung kich thuoc K x K.
    Tra (statistic, dof, p_value, reject_H0).
    """
    counts_list = [np.asarray(c, dtype=float) for c in counts_list]
    pooled = sum(counts_list)
    p_pooled = mle_transition_matrix(pooled)
    k = pooled.shape[0]
    stat = 0.0
    dof = 0
    for i in range(k):
        if pooled[i].sum() == 0:
            continue
        support = p_pooled[i] > 0
        r_i = int(support.sum())
        if r_i <= 1:
            continue
        periods_with_data = 0
        for counts_g in counts_list:
            n_ig = counts_g[i].sum()
            if n_ig == 0:
                continue
            periods_with_data += 1
            p_g_row = counts_g[i] / n_ig
            for j in np.where(support)[0]:
                n_igj = counts_g[i, j]
                if n_igj > 0:
                    stat += 2.0 * n_igj * np.log(p_g_row[j] / p_pooled[i, j])
        dof += max(periods_with_data - 1, 0) * (r_i - 1)
    if dof <= 0:
        logger.warning("chi2_homogeneity_test: khong du du lieu de uoc luong dof (%s)", dof)
        return stat, dof, np.nan, False
    p_value = float(chi2.sf(stat, dof))
    return float(stat), int(dof), p_value, bool(p_value < alpha)


def lr_test_markov_order(counts_order1, counts_order2, alpha=0.05):
    """LR test bac Markov 1 vs 2 -- Ch.2 muc 2.6.

    counts_order1: n_jk, K x K (dem cap trang thai lien tiep, bac 1).
    counts_order2: n_ijk, K x K x K (dem bo ba trang thai lien tiep, bac 2),
        chi so [i, j, k] = so lan (t-2=i, t-1=j, t=k).
    Tra (statistic, dof, p_value, reject_H0). H0: bac 1 la du.
    """
    counts_order1 = np.asarray(counts_order1, dtype=float)
    counts_order2 = np.asarray(counts_order2, dtype=float)
    k = counts_order1.shape[0]
    p1 = mle_transition_matrix(counts_order1)

    log_l1 = 0.0
    log_l2 = 0.0
    free_params_order2 = 0
    for i in range(k):
        for j in range(k):
            n_ij_total = counts_order2[i, j, :].sum()
            if n_ij_total == 0:
                continue
            p2_row = counts_order2[i, j, :] / n_ij_total
            support = p2_row > 0
            r = int(support.sum())
            if r <= 1:
                continue
            free_params_order2 += r - 1
            for kk in np.where(support)[0]:
                n_ijk = counts_order2[i, j, kk]
                if n_ijk > 0 and p1[j, kk] > 0:
                    log_l2 += n_ijk * np.log(p2_row[kk])
                    log_l1 += n_ijk * np.log(p1[j, kk])

    free_params_order1 = 0
    for j in range(k):
        if counts_order1[j].sum() == 0:
            continue
        support1 = p1[j] > 0
        r1 = int(support1.sum())
        if r1 > 1:
            free_params_order1 += r1 - 1

    dof = free_params_order2 - free_params_order1
    stat = -2.0 * (log_l1 - log_l2)
    if dof <= 0:
        logger.warning("lr_test_markov_order: khong du du lieu de uoc luong dof (%s)", dof)
        return stat, dof, np.nan, False
    p_value = float(chi2.sf(stat, dof))
    return float(stat), int(dof), p_value, bool(p_value < alpha)

"""Smoke test cho scripts/utils/markov.py bằng ma trận toy (không dùng dữ liệu thật).

Chạy: python scripts/00_smoke_test_markov.py
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from utils.markov import (  # noqa: E402
    absorption_probabilities,
    chi2_homogeneity_test,
    forecast_distribution,
    frobenius_deviation,
    fundamental_matrix,
    lr_test_markov_order,
    matrix_power,
    mle_transition_matrix,
    pd_finite_horizon,
    stationary_distribution,
)

# Toy chain 4 trạng thái: A(0), B(1) tạm thời; Default(2), Prepaid(3) hấp thụ.
STATES = ["A", "B", "Default", "Prepaid"]
P = np.array(
    [
        [0.5, 0.3, 0.1, 0.1],
        [0.2, 0.3, 0.3, 0.2],
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
    ]
)
Q = P[:2, :2]
R = P[:2, 2:]

# N, B tính tay (phân số mẫu 29): N=[[70/29,30/29],[20/29,50/29]], B=[[16/29,13/29],[17/29,12/29]]
N_EXPECTED = np.array([[70 / 29, 30 / 29], [20 / 29, 50 / 29]])
B_EXPECTED = np.array([[16 / 29, 13 / 29], [17 / 29, 12 / 29]])

failures = []


def check(name, condition):
    status = "PASS" if condition else "FAIL"
    print(f"[{status}] {name}")
    if not condition:
        failures.append(name)


# 1. mle_transition_matrix: đếm toy khớp đúng P (dùng P*100 làm n_ij)
counts = (P * 100).astype(float)
p_hat = mle_transition_matrix(counts, absorbing_states=[2, 3])
check("mle_transition_matrix khop P toy", np.allclose(p_hat, P))

# 2. fundamental_matrix + absorption_probabilities khớp tính tay
N = fundamental_matrix(Q)
B = absorption_probabilities(N, R)
check("fundamental_matrix N khop tinh tay", np.allclose(N, N_EXPECTED))
check("absorption_probabilities B khop tinh tay", np.allclose(B, B_EXPECTED))
check("moi hang B tong = 1", np.allclose(B.sum(axis=1), 1.0))

# 3. pd_finite_horizon: H lớn phải hội tụ về B (vì Q^H -> 0)
pd_h_large = pd_finite_horizon(N, R, Q, H=50)
check("pd_finite_horizon(H=50) hoi tu ve B", np.allclose(pd_h_large, B, atol=1e-6))
pd_h_1 = pd_finite_horizon(N, R, Q, H=1)
check("pd_finite_horizon(H=1) khop R", np.allclose(pd_h_1, R))

# 4. Chapman-Kolmogorov: P^2 . P^1 == P^3 (kiểm chứng bằng số)
lhs = matrix_power(P, 2) @ matrix_power(P, 1)
rhs = matrix_power(P, 3)
check("Chapman-Kolmogorov P^2.P^1 = P^3", np.allclose(lhs, rhs))
fro, max_cell = frobenius_deviation(lhs, rhs)
check("frobenius_deviation = 0 khi hai ma tran giong nhau", np.isclose(fro, 0.0) and np.isclose(max_cell, 0.0))

# 5. stationary_distribution: nghiệm phải thỏa mãn pi P = pi và tổng = 1
pi = stationary_distribution(P)
check("stationary_distribution thoa man piP=pi", np.allclose(pi @ P, pi, atol=1e-8))
check("stationary_distribution tong = 1", np.isclose(pi.sum(), 1.0))

# 6. forecast_distribution: mu0 tại A, dự báo 1 bước phải khớp hàng A của P
mu0 = np.array([1.0, 0.0, 0.0, 0.0])
forecast_1 = forecast_distribution(mu0, P, 1)
check("forecast_distribution 1 buoc tu A khop hang A cua P", np.allclose(forecast_1, P[0]))

# 7. chi2_homogeneity_test: 2 giai đoạn toy, không crash, p-value hợp lệ
rng = np.random.default_rng(42)
counts_period1 = (counts + rng.integers(0, 5, size=counts.shape)).astype(float)
counts_period2 = (counts + rng.integers(0, 5, size=counts.shape)).astype(float)
stat_h, dof_h, p_h, reject_h = chi2_homogeneity_test([counts_period1, counts_period2])
check("chi2_homogeneity_test tra p-value hop le [0,1]", dof_h > 0 and 0.0 <= p_h <= 1.0)
check("chi2_homogeneity_test statistic >= 0", stat_h >= 0.0)

# 8. lr_test_markov_order: sinh n_ijk toy từ counts (giả định bậc 1 đúng), không crash
k = len(STATES)
counts_order2 = np.zeros((k, k, k))
for i in range(k):
    for j in range(k):
        n_ij = counts[i, j]
        if n_ij > 0:
            counts_order2[i, j, :] = p_hat[j] * n_ij
stat_o, dof_o, p_o, reject_o = lr_test_markov_order(counts, counts_order2)
check("lr_test_markov_order tra p-value hop le [0,1]", dof_o > 0 and 0.0 <= p_o <= 1.0)
check("lr_test_markov_order statistic >= 0 (xấp xỉ, dư sai số số học)", stat_o >= -1e-6)

print()
if failures:
    print(f"KẾT QUẢ: {len(failures)} FAIL -- {failures}")
    sys.exit(1)
print("KẾT QUẢ: TOÀN BỘ PASS")
sys.exit(0)

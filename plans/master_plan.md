# Master Plan — Roll-rate Markov Chain cho Cảnh báo sớm Nợ

> Kế hoạch tổng của toàn dự án. Nguồn spec gốc: `PROJECT_BRIEF.md` (đọc full trước khi code).
> File này ít thay đổi — chỉ cập nhật khi phạm vi hoặc thứ tự buổi làm thay đổi.
> Bước đang làm chi tiết: xem `plans/active_plan.md`. Nhật ký quyết định: xem `plans/logs.md`.

---

## 1. Tóm tắt dự án

- **Môn:** MAT6206 — Các phương pháp ngẫu nhiên và ứng dụng (Thạc sĩ KHDL, VNU-HUS).
- **Loại:** Bài tập cuối kỳ (KHÔNG phải luận văn). Thời lượng ước tính ~6 buổi.
- **Bài toán:** Xây mô hình xích Markov rời rạc thời gian, không gian trạng thái hữu hạn (roll-rate matrix) để cảnh báo sớm nợ vỡ.
- **Trạng thái (6, hai trạng thái hấp thụ):** `Current (0) → 30 DPD → 60 DPD → 90+ DPD` là 4 trạng thái tạm thời; `Default/Foreclosure` và `Prepaid` (trả hết nợ trước hạn/đáo hạn) là 2 trạng thái hấp thụ. Quyết định 2026-09-22 (xem `logs.md`): dùng 2 trạng thái hấp thụ (Phương án B) để `B=NR` có ý nghĩa phân biệt rủi ro, thay vì chỉ 1 trạng thái Default khiến `B=1`.
- **Dữ liệu chính:** Freddie Mac Single-Family Loan-Level Dataset (Standard/Sample), **3 vintage 2016+2017+2018 gộp** (150.000 khoản vay) — mở rộng từ 1 vintage ban đầu (quyết định 2026-09-22, xem `logs.md`) vì cần đủ sự kiện Default cho kiểm định + backtest.
  - **Dự phòng:** Kaggle "American Express Default Prediction" (~13 tháng) — nếu dùng, kiểm định thuần nhất theo thời gian co lại thành so 2 nửa kỳ.
- **Định nghĩa trạng thái Default (quyết định 2026-09-22):** ngưỡng 180 ngày quá hạn (`delinquency_status ≥ '06'`) HOẶC `RA` HOẶC `zero_balance_code ∈ {02,03,09}`, kèm quy tắc "sticky absorbing" (một khi chạm ngưỡng, không cho quay lại). Chi tiết + số liệu so sánh 3 phương án: `logs.md`, Ch.3 §3.2.1 của báo cáo.
- **Chia dữ liệu:** theo thời gian, KHÔNG random. ~80% kỳ đầu = estimation set, ~20% kỳ cuối = validation set.
- **Công cụ:** Python + `pandas`, `numpy`, `scipy.stats`, `matplotlib`/`seaborn`. Tự cài đặt toàn bộ công thức Markov thủ công.
- **Output cuối:** Báo cáo tiếng Việt, công thức LaTeX annotate biến số, xuất Markdown/HTML + MathJax (theme indigo/jade, card layout).

## 2. Mục tiêu học thuật phải chứng minh

1. Xích Markov rời rạc thời gian, không gian trạng thái hữu hạn
2. MLE cho ma trận chuyển: `p_hat_ij = n_ij / sum_k n_ik`
3. Phương trình Chapman–Kolmogorov: `P^(m+n) = P^(m) · P^(n)`
4. Phân phối dừng: `π P = π`, `sum_i π_i = 1`
5. Xích Markov hấp thụ: dạng chuẩn `P = [[Q, R], [0, I]]`, ma trận cơ bản `N = (I - Q)^{-1}`, xác suất hấp thụ `B = N R`
6. Kiểm định giả thiết mô hình: tính thuần nhất theo thời gian (χ²), bậc Markov 1 vs 2 (likelihood ratio test) — mỗi kiểm định phải có kết luận bác bỏ / không bác bỏ H0 rõ ràng.

> **Nguyên tắc chấm điểm ngầm định:** giảng viên đánh giá cao *kiểm tra giả thiết mô hình* và *đối chiếu dự đoán lý thuyết với dữ liệu kiểm định thực tế*, hơn là áp công thức và xuất kết quả không phản biện.

## 3. Kế hoạch theo buổi

| Buổi | Mục tiêu | Đầu ra chính | Chương báo cáo |
|---|---|---|---|
| 1 | Setup môi trường + lấy dữ liệu | venv đầy đủ package, `requirements.txt`, dữ liệu thô trong `data/`, cấu trúc thư mục | — |
| 2 | Tiền xử lý | Bảng quỹ đạo `(loan_id, month, state)`, split estimation/validation theo thời gian, artifact trung gian | Ch.3 |
| 3 | Ước lượng P_hat + Chapman–Kolmogorov | `P_hat` + heatmap + bảng đếm quan sát (4.1); kiểm chứng CK bằng số (4.3) | Ch.4.1, 4.3 |
| 4 | Kiểm định giả thiết | χ² thuần nhất theo thời gian + LR test bậc Markov, cả hai có kết luận H0 (4.2) | Ch.3 (thiết kế), Ch.4.2 |
| 5 | Phân phối dừng + xích hấp thụ + backtest | π so tần suất thực nghiệm (4.4); N, B; backtest B vs tỷ lệ vỡ nợ thực tế trên validation set (4.5) | Ch.4.4, 4.5 |
| 6 | Viết báo cáo | Ch.1–2 (lý thuyết + LaTeX), ghép 4.1–4.5 (số + diễn giải lời), kết luận; xuất Markdown/HTML; chạy end-to-end tái lập | Ch.1, 2, Kết luận |

### Buổi 1 — Setup + dữ liệu
- [ ] Kích hoạt venv `stochastic\Scripts\Activate.ps1`
- [ ] `pip install pandas numpy scipy matplotlib seaborn jupyter` → tạo `requirements.txt`
- [ ] Tải Freddie Mac Single-Family Loan-Level (Standard/Sample). Nếu quá nặng → chuyển sang Amex (ghi quyết định vào `logs.md`)
- [ ] Dựng thư mục `scripts/`, `scripts/feature_engineering/`, `data/`, `outputs/`, `outputs/reports/`
- [ ] Ghi chú schema dữ liệu thô (cột trạng thái quá hạn, mã DPD)

### Buổi 2 — Tiền xử lý (Chương 3)
- [ ] Load dữ liệu, rời rạc hóa DPD thành 5 bucket `{0, 30, 60, 90+, Default}`
- [ ] Xây bảng quỹ đạo trạng thái theo tháng cho từng khoản vay `(loan_id, month, state)`
- [ ] Xử lý theo chunk, log tiến độ, có chế độ smoke test / `--limit`
- [ ] Chia theo thời gian: estimation set (80% kỳ đầu) / validation set (20% kỳ cuối)
- [ ] Lưu artifact trung gian (parquet/csv có suffix ngày)

### Buổi 3 — Ước lượng + Chapman–Kolmogorov (4.1, 4.3)
- [ ] Đếm `n_ij` trên estimation set, tính MLE `p_hat_ij = n_ij / sum_k n_ik`
- [ ] Heatmap ma trận chuyển + bảng số quan sát mỗi trạng thái
- [ ] Tính `P_hat^(1)` theo tháng, ước lượng trực tiếp `P_hat^(3)` theo quý
- [ ] So `(P_hat^(1))^3` với `P_hat^(3)` — định lượng sai lệch (Frobenius norm + so từng ô)

### Buổi 4 — Kiểm định giả thiết (4.2)
- [ ] **Thiết kế** (ghi vào Ch.3): chia estimation set thành giai đoạn con theo năm; thiết kế χ²-test so từng cặp ma trận. H0: ma trận không đổi theo thời gian
- [ ] **Chạy** χ² thuần nhất → bảng kết quả theo từng cặp giai đoạn + kết luận bác bỏ / không bác bỏ H0
- [ ] **Thiết kế + chạy** LR test bậc Markov 1 vs 2. H0: bậc 1 là đủ → kết luận rõ ràng
- [ ] Diễn giải: mô hình Markov bậc 1 thuần nhất có phù hợp dữ liệu không

### Buổi 5 — Phân phối dừng + xích hấp thụ (4.4, 4.5)
- [ ] Giải `π P = π`, `sum_i π_i = 1` (eigenvector trái / hệ tuyến tính)
- [ ] So π với tần suất thực nghiệm quan sát trong dữ liệu (đối chiếu, không tính suông)
- [ ] Dạng chuẩn `P = [[Q, R], [0, I]]`; tính `N = (I - Q)^{-1}`, `B = N R`
- [ ] **Backtest bắt buộc (4.5):** so xác suất hấp thụ dự đoán `B` với tỷ lệ vỡ nợ **thực tế quan sát trên validation set**, theo từng trạng thái xuất phát
- [ ] Diễn giải sai lệch dự đoán vs thực tế

### Buổi 6 — Báo cáo
- [ ] Ch.1 Giới thiệu: đặt vấn đề, mục tiêu, phạm vi (nêu rõ chỉ dùng Markov quan sát được, không HMM/Cox/hazard — lựa chọn chủ động)
- [ ] Ch.2 Cơ sở lý thuyết: 7 công thức, annotate rõ từng biến, LaTeX
- [ ] Ghép kết quả 4.1–4.5: mỗi mục có số + diễn giải bằng lời
- [ ] Kết luận: mô hình Markov có phù hợp không (dựa 4.2); hạn chế (chỉ phụ thuộc trạng thái); hướng mở rộng (chỉ nêu, KHÔNG code)
- [ ] Xuất báo cáo Markdown/HTML tiếng Việt + MathJax, theme indigo/jade
- [ ] Chạy notebook/script end-to-end, xác nhận tái lập toàn bộ Chương 4

## 4. Định nghĩa hoàn thành (Definition of Done)

1. Notebook/script chạy end-to-end, tái lập toàn bộ kết quả Chương 4
2. Mỗi mục 4.1–4.5 có: kết quả số + diễn giải bằng lời
3. Ít nhất 2 chỗ có kiểm định giả thiết + kết luận rõ ràng bác bỏ / không bác bỏ H0 (mục 4.2)
4. Mục 4.5 có đối chiếu dự đoán mô hình với validation set thực tế (bắt buộc)
5. Báo cáo cuối dạng Markdown/HTML, tiếng Việt, công thức LaTeX đầy đủ chú thích biến số

## 5. Ràng buộc phạm vi — Việc KHÔNG được làm

- ❌ HMM, Baum-Welch, Viterbi
- ❌ Discrete-time hazard / Cox PH / survival analysis
- ❌ Multistate hoặc semi-Markov regression
- ❌ So sánh với Random Survival Forest, XGBoost-AFT, bất kỳ mô hình ML nào
- ❌ Chiến lược giao dịch / backtest kiểu trading strategy
- ❌ Segment-level transition matrix — chỉ thêm nếu HUNG chủ động yêu cầu
- ❌ Bootstrap confidence interval cho π hoặc B — chỉ thêm khi được yêu cầu rõ

> Nếu giữa chừng nảy ra hướng mở rộng "rất hay" → **dừng lại, hỏi HUNG**, ghi vào `logs.md`, không tự thêm.

## 6. Luồng code chi tiết theo phase (script-level, map vào buổi ở mục 3)

> Bổ sung 2026-09-22: chi tiết hóa "buổi" thành phase/script cụ thể để code trực tiếp, không đổi phạm vi hay thứ tự buổi.

| Phase | Buổi | File | Nội dung | Map lý thuyết |
|---|---|---|---|---|
| 0 | (nền tảng, làm đầu buổi 2) | `scripts/utils/markov.py` | `mle_transition_matrix`, `chapman_kolmogorov_power`, `stationary_distribution`, `fundamental_matrix`, `absorption_probabilities`, `chi2_homogeneity_test`, `lr_test_markov_order` | Ch.2 toàn bộ 7 công thức — tự cài đặt thủ công |
| 1 | Buổi 2 | `scripts/01_build_trajectory.py`, `scripts/02_split_estimation_validation.py` | Load 3 vintage, rời rạc hóa 6 state + sticky absorbing, xây `(loan_id, month, state)`, chunk + `--limit`, split theo thời gian | Ch.3 tiền xử lý |
| 2 | Buổi 3 | `scripts/03_estimate_transition_matrix.py` | `P_hat` tháng (4.1) + heatmap; `P_hat^(3)` quý trực tiếp vs `(P_hat^(1))^3` (4.3) | 4.1, 4.3 |
| 3 | Buổi 4 | `scripts/04_hypothesis_tests.py` | χ² thuần nhất theo giai đoạn con; LR test bậc 1 vs 2 | 4.2 |
| 4 | Buổi 5 | `scripts/05_stationary_and_absorption.py` | π vs tần suất thực nghiệm; `N=(I-Q)^-1`, `B=NR`; backtest B vs default/prepaid thực tế validation set (H=12) | 4.4, 4.5 (bắt buộc) |
| 5 | Buổi 6 | `report/report.ipynb` | Ghép Ch.1-2 (text) + 4.1-4.5 (số + diễn giải), export Markdown/HTML MathJax | Toàn bộ |

Artifact convention: `data/processed/`, `outputs/tables/`, `outputs/figures/` theo cấu trúc thư mục ở mục 7bis của `PROJECT_BRIEF.md`.

## 7. Cấu trúc thư mục dự kiến

```
plans/                    ← master_plan.md, active_plan.md, logs.md
scripts/                  ← pipeline chạy lại được
scripts/feature_engineering/  ← rời rạc hóa state, xây quỹ đạo, split
data/                     ← dữ liệu thô + đã clean
outputs/                  ← artifact: P_hat, N, B, heatmap, kết quả kiểm định
outputs/reports/          ← log job, báo cáo Markdown/HTML cuối
```

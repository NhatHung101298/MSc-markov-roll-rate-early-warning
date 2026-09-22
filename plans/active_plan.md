# Active Plan — Bước đang làm

> Chỉ chứa buổi / bước ĐANG thực hiện. Khi xong 1 buổi: đánh dấu hoàn thành, chép checklist buổi kế từ `master_plan.md` vào đây, ghi 1 dòng vào `logs.md`.
> Bức tranh tổng: `plans/master_plan.md`.

---

## Trạng thái hiện tại

- **Ngày cập nhật:** 2026-09-22
- **Buổi:** đang ở Buổi 2 (2 / 6) — **Phase 1 xong, chuẩn bị Phase 2** (`scripts/03_estimate_transition_matrix.py`, xem mục 6 `master_plan.md`)
- **Tình trạng:** Phase 0 + Phase 1 hoàn tất, có artifact thật trong `data/processed/`. Song song đã viết nháp lý thuyết Ch.1–3 của báo cáo cuối kỳ (`outputs/TranNhatHung_MAT6206_BaoCaoCuoiKy/`) trước khi có kết quả số — Ch.3 §3.2.3 đã đồng bộ τ thật (xem bên dưới), Ch.4 vẫn là khung chờ Phase 2-4.
- **Blocker:** không còn.

## Checklist Phase 0 — `scripts/utils/markov.py` — HOÀN TẤT (2026-09-22)

- [x] Dựng thư mục `scripts/`, `scripts/utils/`
- [x] `mle_transition_matrix(counts, absorbing_states)` — (2.10), hàng absorbing ép identity, hàng rỗng → NaN + warning
- [x] `matrix_power(P, n)`, `frobenius_deviation(A, B)` — (2.12), (2.13)
- [x] `stationary_distribution(P)`, `forecast_distribution(mu0, P, t)` — (2.14), dự báo hữu hạn kỳ §3.4.4
- [x] `fundamental_matrix(Q)`, `absorption_probabilities(N, R)`, `pd_finite_horizon(N, R, Q, H)` — (2.16), (2.18), (2.19)
- [x] `chi2_homogeneity_test(counts_list)` (Anderson-Goodman LR), `lr_test_markov_order(counts_order1, counts_order2)`
- [x] Smoke test `scripts/00_smoke_test_markov.py` bằng ma trận toy 4 trạng thái (2 tạm thời + 2 hấp thụ), N/B đối chiếu tính tay bằng phân số — **15/15 PASS**, exit code 0
- [ ] `outputs/reports/` — dời sang khi có script ghi log thật (chưa cần cho Phase 0)

Chưa làm: `quasi_stationary_distribution` (để dành nếu Phase 4 cần diễn giải thêm, xem plan Phase 0 đã duyệt).

## Checklist buổi 1 — HOÀN TẤT

- [x] Venv `stochastic/` đã cài: pandas 3.0.5, numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.1, seaborn 0.13.2, jupyter
- [x] `requirements.txt` đã tạo (108 dòng, `pip freeze`)
- [x] Chốt nguồn dữ liệu: **Freddie Mac Single-Family Loan-Level — Sample, 3 vintage 2016+2017+2018 gộp** (ban đầu chỉ 2016, mở rộng 2026-09-22, xem `logs.md`)
- [x] Dữ liệu đã có trong `data/raw/`: `sample_orig_{2016,2017,2018}.txt` (50.000 khoản vay/năm, 150.000 tổng), `sample_perf_{2016,2017,2018}.txt` (3.379.650 + 2.800.219 + 2.059.564 = 8.239.433 dòng, kỳ 201601/201701/201801 – 202603)
- [x] Ghi chú schema đầy đủ — xem `data/raw/DATA_DICTIONARY.md`
- [ ] Dựng thư mục `scripts/`, `scripts/feature_engineering/`, `outputs/reports/` — dời sang đầu Buổi 2 (chưa cần cho tới khi viết code)

## Quyết định đã chốt (2026-09-22)

1. **Trạng thái hấp thụ — Phương án B:** 6 trạng thái, 2 trạng thái hấp thụ (Default/Foreclosure + Prepaid). Lý do: nếu chỉ 1 trạng thái hấp thụ, `B=NR=1` cho mọi trạng thái xuất phát — vô nghĩa cho backtest §4.5.
2. **Mở rộng dữ liệu — 3 vintage 2016+2017+2018 gộp** (150.000 khoản vay). Lý do: 1 vintage (2016) cho quá ít sự kiện Default (76–78, tùy định nghĩa) để kiểm định + backtest có ý nghĩa thống kê.
3. **Ngưỡng Default — Phương án C:** `delinquency_status ≥ '06'` (≥180 ngày quá hạn) HOẶC `RA` HOẶC `zero_balance_code ∈ {02,03,09}`, kèm quy tắc **"sticky absorbing"** (một khi chạm ngưỡng, mọi bản ghi sau đó bị ép gán Default dù dữ liệu thô cho thấy giảm quá hạn). Cho **4.921 sự kiện** trên bộ gộp 150.000 khoản vay (so với A: 215, B: 7.991 — xem bảng so sánh ở Ch.3 §3.2.1).
4. **Kỳ hạn backtest §4.5 — Phương án A: chỉ $H=12$ tháng** (không dùng thêm $H=24$). Lý do: tập validation chỉ ~25 tháng nên $H=24$ khít dữ liệu (đệm ~1 tháng); $H=12$ an toàn hơn (đệm ~13 tháng) và giữ đúng tinh thần "cảnh báo sớm". Tại $\tau\approx$02/2024: $i=0$ 39.195 khoản/34 sự kiện; $i=1$ 392/15; $i=2$ 84/13; $i=3$ 70/38.

Đã cập nhật: `PROJECT_BRIEF.md`, `plans/master_plan.md`, `data/raw/DATA_DICTIONARY.md`, `outputs/.../outline.md`, Ch.1 §1.2/1.4, Ch.2 §2.5.5, Ch.3 §3.1.2/3.2.1/3.2.2/3.2.3/3.3/3.4.5 của báo cáo. Chi tiết + số liệu: `logs.md` 2026-09-22.

## Checklist Phase 1 — ETL — HOÀN TẤT (2026-09-22)

- [x] Dựng thư mục `scripts/` (đã có từ Phase 0), `data/processed/`
- [x] Load dữ liệu **3 vintage** (`orig`/`perf` × 2016/2017/2018), gộp theo `loan_id` — `scripts/01_build_trajectory.py`
- [x] Rời rạc hóa DPD thành **6 bucket** theo bảng Ch.3 §3.2.1, áp dụng **sticky absorbing** — **sửa lại cách hiểu so với dòng cũ bên dưới**: KHÔNG cắt quỹ đạo, giữ nguyên bản ghi tháng sau và ép `state=Default`/`Prepaid` lặp lại đến hết dữ liệu thô (đúng nghĩa đen Ch.3, xem plan Phase 1 đã duyệt)
- [x] Xây bảng quỹ đạo `(loan_id, vintage, month, month_index, state, segment_id)` — `segment_id` đánh dấu gap báo cáo để Phase 2 ghép cặp đúng
- [x] Xử lý theo chunk (`--chunksize`), log tiến độ, `--limit` cho smoke test
- [x] Chia theo thời gian: **τ = 2024/02** (tính bằng percentile 80% trên trục lịch gộp 201601–202603, 123 tháng, mốc thứ 98) — `scripts/02_split_estimation_validation.py`
- [x] Lưu artifact: `data/processed/loan_trajectory_full.parquet`, `estimation_set_full.parquet`, `validation_set_full.parquet`, `split_manifest_full.json` (+ bản `_smoke` cho 2000 khoản vay)

**Kết quả full run (150.000 khoản vay, 8.239.433 dòng — khớp chính xác tổng đã biết):**
- Phân phối state: Current 7.819.062, 30DPD 63.839, 60DPD 18.958, 90+DPD 26.417, Default 200.323, Prepaid 110.834
- Khoản vay từng chạm Default: **4.921** (khớp chính xác số Phương án C đã tính trước bằng awk)
- Khoản vay từng chạm Prepaid: 110.834 (thấp hơn số thô zbc=01 là 112.875 khoảng 2.041 — do một số khoản vay có zbc=01 nhưng đã chạm Default trước đó nên bị ép giữ Default theo ưu tiên sticky-absorbing, đúng thiết kế)
- Estimation set: 7.253.423 dòng, 150.000 khoản vay, 4.728 chạm Default, 105.230 chạm Prepaid (trong khung thời gian estimation)
- Validation set: 986.010 dòng, 42.458 khoản vay, 2.910 chạm Default, 5.604 chạm Prepaid
- 1 dòng có gap báo cáo trên 1 khoản vay (không đáng kể)

## Đặc điểm dữ liệu đã xác minh

- `sample_orig_{2016,2017,2018}.txt` — pipe-delimited, không header, 50.000 dòng/năm = 150.000 khoản vay tổng. Cột 20 = `LOAN_SEQUENCE_NUMBER` (khóa nối, prefix `F16/F17/F18` không trùng giữa các năm), cột 2 = `FIRST_PAYMENT_DATE` (YYYYMM).
- `sample_perf_{2016,2017,2018}.txt` — pipe-delimited, không header, 3.379.650+2.800.219+2.059.564 = 8.239.433 dòng, cùng schema 35 cột. Cột 1 = `LOAN_SEQUENCE_NUMBER`, cột 2 = `MONTHLY_REPORTING_PERIOD` (YYYYMM), cột 4 = `CURRENT_LOAN_DELINQUENCY_STATUS`, cột 9 = `ZERO_BALANCE_CODE`.
- **Kỳ báo cáo:** 201601 (2016) / 201701 (2017) / 201801 (2018) → 202603, cùng mốc cắt cho cả 3 vintage → chia estimation/validation theo lịch áp dụng đồng nhất được.
- **Mã delinquency (col 4):** `00`=Current, `01`=30 DPD, `02`=60 DPD, `03`-`05`=90+ DPD (tạm thời), `≥06`=Default (cùng `RA`), … tới `70`.
- **Mã zero-balance (col 9), đếm trên bộ gộp 3 vintage:** `01` prepaid/matured (112.875) → **Prepaid**; `02`/`03`/`09` (105+22+78=205) → **Default**; `15`/`16`/`96` (61+243+285) → kiểm duyệt.
- **So sánh 3 phương án định nghĩa Default (bộ gộp 150.000 khoản vay):** A (chỉ tổn thất tín dụng thực tế) = 215 sự kiện; B (A ∪ DPD≥90) = 7.991; **C (A ∪ DPD≥180, đã chọn) = 4.921**.

## Việc còn mở (chưa chốt)

Không còn — toàn bộ quyết định thiết kế trước Buổi 2 đã chốt (xem "Quyết định đã chốt" ở trên). Sẵn sàng bắt đầu dựng `scripts/` và viết code Buổi 2.

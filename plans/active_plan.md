# Active Plan — Bước đang làm

> Chỉ chứa buổi / bước ĐANG thực hiện. Khi xong 1 buổi: đánh dấu hoàn thành, chép checklist buổi kế từ `master_plan.md` vào đây, ghi 1 dòng vào `logs.md`.
> Bức tranh tổng: `plans/master_plan.md`.

---

## Trạng thái hiện tại

- **Ngày cập nhật:** 2026-09-07
- **Buổi:** 1 / 6 — Setup môi trường + lấy dữ liệu
- **Tình trạng:** GẦN XONG — còn dựng thư mục output + notebook khởi đầu
- **Blocker:** không còn

## Checklist buổi 1

- [x] Venv `stochastic/` đã cài: pandas 3.0.5, numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.1, seaborn 0.13.2, jupyter
- [x] `requirements.txt` đã tạo (108 dòng, `pip freeze`)
- [x] Chốt nguồn dữ liệu: **Freddie Mac Single-Family Loan-Level — bộ Sample vintage 2016** (xem `logs.md`)
- [x] Dữ liệu đã có trong `data/raw/`: `sample_orig_2016.txt` (50.000 khoản vay), `sample_perf_2016.txt` (3.379.650 dòng, kỳ 201603–202603)
- [ ] Dựng thư mục `scripts/`, `scripts/feature_engineering/`, `outputs/`, `outputs/reports/`
- [ ] Ghi chú schema chi tiết 2 file (mapping cột theo layout Freddie Mac chính thức)

## Đặc điểm dữ liệu đã xác minh (2026-09-07)

- `sample_orig_2016.txt` — pipe-delimited, không header, 50.000 dòng = 50.000 khoản vay. Cột 20 = `LOAN_SEQUENCE_NUMBER` (khóa nối), cột 2 = `FIRST_PAYMENT_DATE` (YYYYMM). Có 41.660 khoản origination 2016, 8.331 năm 2017, vài khoản 2018/2020.
- `sample_perf_2016.txt` — pipe-delimited, không header, 3.379.650 dòng. Cột 1 = `LOAN_SEQUENCE_NUMBER`, cột 2 = `MONTHLY_REPORTING_PERIOD` (YYYYMM), cột 4 = `CURRENT_LOAN_DELINQUENCY_STATUS`, cột 9 = `ZERO_BALANCE_CODE`.
- **Kỳ báo cáo:** 201603 → 202603 ≈ 121 tháng → thừa giai đoạn con cho kiểm định thuần nhất theo năm.
- **Mã delinquency (col 4):** `00` (current, 98.4%), `01`=30 DPD, `02`=60 DPD, `03`=90 DPD, … tới `70`, và `RA` (REO Acquisition). Cần map: `00→Current`, `01→30DPD`, `02→60DPD`, `>=03→90+ DPD`.
- **Mã zero-balance (col 9):** `01` prepaid/matured (35.734), `02` third-party sale, `03` short sale, `09` REO disposition, `15`/`16` reperforming/repurchase, `96` removal. → Default/Foreclosure absorbing khớp với `03`, `09` (+ delinquency cao) — cần chốt định nghĩa "Default" ở buổi 2.

## Việc cần HUNG quyết định ở Buổi 2

1. Định nghĩa trạng thái hấp thụ "Default/Foreclosure": chỉ delinquency `>= 90 DPD` kéo dài, hay gộp cả zero-balance code `03/09` (short sale, REO)? (mặc định đề xuất: DPD >= 6 tháng HOẶC zero-balance ∈ {03,09})
2. Ngưỡng gộp `90+ DPD`: gộp mọi mã `>= 03` vào 1 bucket "90+ DPD" (không hấp thụ) trước khi rơi vào Default?

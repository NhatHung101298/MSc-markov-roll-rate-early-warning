# Ma trận chuyển trạng thái (Roll-rate Matrix) cho Cảnh báo sớm Nợ

Bài tập cuối kỳ môn **MAT6206 — Các phương pháp ngẫu nhiên và ứng dụng**, Thạc sĩ Khoa học Dữ liệu, Khoa Toán – Cơ – Tin, Trường Đại học Khoa học Tự nhiên, ĐHQGHN.

> Chi tiết đầy đủ (mục tiêu học thuật, checklist triển khai, ràng buộc phạm vi) nằm ở [`PROJECT_BRIEF.md`](./PROJECT_BRIEF.md) — đọc file đó trước khi code.

## Tóm tắt bài toán

Xây dựng mô hình xích Markov rời rạc, không gian trạng thái hữu hạn để mô hình hóa chuyển trạng thái quá hạn của khoản vay, dùng cho cảnh báo sớm nợ xấu.

- **Trạng thái (5, trạng thái cuối hấp thụ):** `Current (0) → 30 DPD → 60 DPD → 90+ DPD → Default/Foreclosure`
- **Dữ liệu:** Freddie Mac Single-Family Loan-Level Dataset (dự phòng: Kaggle "American Express Default Prediction")
- **Chia dữ liệu:** theo thời gian — không random split (estimation set / validation set)

## Nội dung chính

1. Ước lượng MLE ma trận chuyển `P_hat`
2. Kiểm định tính thuần nhất theo thời gian (χ²) và bậc Markov (likelihood ratio test)
3. Kiểm chứng Chapman–Kolmogorov bằng số
4. Phân phối dừng π, đối chiếu với tần suất thực nghiệm
5. Ma trận cơ bản `N` và xác suất hấp thụ `B` — backtest trên validation set

## Việc KHÔNG làm

Không dùng HMM, Cox PH/hazard, semi-Markov regression, so sánh ML (Random Survival Forest, XGBoost-AFT), phân tích theo phân khúc, hay bootstrap CI — trừ khi được yêu cầu rõ. Chi tiết: `PROJECT_BRIEF.md` §6.

## Môi trường

```powershell
# kích hoạt venv
stochastic\Scripts\Activate.ps1

# cài thư viện (chưa cài sẵn)
pip install pandas numpy scipy matplotlib seaborn
```

## Cấu trúc thư mục

```
PROJECT_BRIEF.md   # spec đầy đủ của bài tập
docs/              # tài liệu tham khảo (cheatsheet, đề thi, tài liệu môn học)
stochastic/        # Python 3.11 venv
```

Các thư mục `scripts/`, `data/`, `outputs/` sẽ được tạo khi bắt đầu triển khai code.

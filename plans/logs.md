# Logs — Nhật ký thực hiện & Quyết định

> Nhật ký thời gian thực. Ghi: quyết định của HUNG, lý do chọn hướng đi, thay đổi phạm vi, kết quả kiểm tra artifact, giai đoạn làm report.
> Mỗi entry: ngày + loại + nội dung ngắn gọn. Entry mới ở TRÊN CÙNG (reverse chronological).
> Loại entry: `[QUYẾT ĐỊNH]` · `[TASK]` · `[KẾT QUẢ]` · `[PHẠM VI]` · `[RỦI RO]` · `[REPORT]`

---

## 2026-09-19

- `[TASK]` `data/raw/` (bị gitignore) đã mất khỏi máy — tải lại từ freddiemac.embs.com. Kiểm tra: `sample_orig_2016.txt` 50.000 dòng/31 cột, `sample_perf_2016.txt` 3.379.650 dòng/35 cột, loan_id unique = 50.000 trong orig — khớp tuyệt đối với log 2026-09-07. Lệch nhỏ: kỳ báo cáo thực tế bắt đầu `201601` (log cũ ghi nhầm `201603`), do tổng dòng khớp 100% nên coi là cùng file, chỉ sửa lại ghi chú.

## 2026-09-17

- `[REPORT]` Tạo `outputs/TranNhatHung_MAT6206_BaoCaoCuoiKy/`: `outline.md` (tổng quan), `noi_dung_chi_tiet/00..06_*.md` (mỗi phần 1 file), `build_docx.sh` (pandoc gộp → .docx). Ch.1, Ch.2, Ch.3 viết nháp đầy đủ; Ch.4 + Tóm tắt kết luận là khung TODO.
- `[RỦI RO]` Với Default là trạng thái hấp thụ DUY NHẤT thì $B = NR = \mathbf{1}$ (vô nghĩa cho backtest 4.5). Cần HUNG chốt: (A) censor khoản prepaid + dùng PD kỳ hạn hữu hạn $(I-Q^H)NR$, hoặc (B) thêm trạng thái hấp thụ "Prepaid". Đã viết lý thuyết cho cả hai ở Ch.2 mục 2.5.5.

---

## 2026-09-07

- `[TASK]` Tạo folder `plans/` với `master_plan.md`, `active_plan.md`, `logs.md`. Cập nhật `CLAUDE.md` để tham chiếu master + active plan.
- `[QUYẾT ĐỊNH]` **Nguồn dữ liệu: Freddie Mac Single-Family Loan-Level — bộ Sample vintage 2016.** HUNG chốt. Lý do: dữ liệu đã có sẵn trong `data/raw/`, kỳ báo cáo 201603–202603 (~121 tháng) đủ dày cho kiểm định thuần nhất theo thời gian. Không dùng Amex.
- `[TASK]` Cài venv `stochastic/`: pandas 3.0.5, numpy 2.4.6, scipy 1.17.1, matplotlib 3.11.1, seaborn 0.13.2, jupyter. Nâng pip 24.0 → 26.2.1. Tạo `requirements.txt` bằng `pip freeze` (108 dòng). Kiểm tra: `import` cả 5 thư viện OK, exit 0.
- `[KẾT QUẢ]` Xác minh `data/raw/`: `sample_orig_2016.txt` 50.000 dòng (50k khoản vay, pipe-delimited, không header); `sample_perf_2016.txt` 3.379.650 dòng, kỳ 201603→202603. Mã delinquency col 4: `00`..`70` + `RA`; `00` chiếm 98.4%. Zero-balance col 9: chủ yếu `01` (prepaid, 35.734), ít `02/03/09/15/16/96`.
- `[RỦI RO]` Định nghĩa trạng thái hấp thụ "Default/Foreclosure" chưa chốt — cần quyết ở Buổi 2 (delinquency kéo dài vs gộp zero-balance code REO/short sale). Ghi câu hỏi trong `active_plan.md`.

---

## Mẫu entry

```
## YYYY-MM-DD

- `[QUYẾT ĐỊNH]` Chọn X thay vì Y. Lý do: ... . Ảnh hưởng: ... .
- `[TASK]` Đã làm: ... . File/output: ... . Kiểm tra: exit code / schema / số dòng / metric.
- `[KẾT QUẢ]` Artifact `outputs/...`: giá trị chính, có hợp lý không, còn nghi vấn gì.
- `[PHẠM VI]` Cân nhắc thêm Z (ngoài brief). HUNG quyết định: thêm / không thêm. Lý do.
- `[RỦI RO]` Phát hiện: ... . Hướng xử lý: ... .
```

---

## Nhật ký giai đoạn làm Report (Buổi 6)

> Điền khi bắt đầu viết báo cáo. Theo dõi tiến độ từng chương và quyết định trình bày.

| Phần | Trạng thái | Ngày | Ghi chú (quyết định trình bày, công thức, số liệu trích từ artifact nào) |
|---|---|---|---|
| Ch.1 Giới thiệu | chưa làm | | |
| Ch.2 Cơ sở lý thuyết | chưa làm | | 7 công thức, annotate biến, LaTeX |
| Ch.3 Dữ liệu & phương pháp | chưa làm | | mô tả preprocessing + thiết kế kiểm định |
| Ch.4.1 Ước lượng P_hat | chưa làm | | heatmap + bảng đếm |
| Ch.4.2 Kiểm định thuần nhất + bậc Markov | chưa làm | | 2 kết luận H0 rõ ràng |
| Ch.4.3 Chapman–Kolmogorov | chưa làm | | Frobenius norm |
| Ch.4.4 Phân phối dừng | chưa làm | | π vs tần suất thực nghiệm |
| Ch.4.5 Backtest N, B | chưa làm | | B vs default rate thực tế validation set |
| Kết luận | chưa làm | | phù hợp / hạn chế / hướng mở rộng |
| Xuất Markdown/HTML + MathJax | chưa làm | | theme indigo/jade |
| Chạy end-to-end tái lập | chưa làm | | |

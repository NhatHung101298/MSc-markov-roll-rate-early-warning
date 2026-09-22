# Logs — Nhật ký thực hiện & Quyết định

> Nhật ký thời gian thực. Ghi: quyết định của HUNG, lý do chọn hướng đi, thay đổi phạm vi, kết quả kiểm tra artifact, giai đoạn làm report.
> Mỗi entry: ngày + loại + nội dung ngắn gọn. Entry mới ở TRÊN CÙNG (reverse chronological).
> Loại entry: `[QUYẾT ĐỊNH]` · `[TASK]` · `[KẾT QUẢ]` · `[PHẠM VI]` · `[RỦI RO]` · `[REPORT]`

---

## 2026-09-22

- `[KẾT QUẢ]` Phase 0 hoàn tất: `scripts/utils/markov.py` (8 hàm, công thức 2.10-2.19) + `scripts/00_smoke_test_markov.py` (ma trận toy 4 trạng thái, N/B đối chiếu tính tay bằng phân số mẫu 29). Chạy bằng `stochastic\Scripts\python.exe scripts\00_smoke_test_markov.py` — 15/15 PASS, exit code 0. Chưa chạm dữ liệu thật; tiếp theo là Phase 1 (ETL, buổi 2).
- `[TASK]` Thêm mục 6 vào `master_plan.md`: script-level breakdown (Phase 0-5, tên file cụ thể trong `scripts/`, `report/report.ipynb`) map vào buổi 2-6 đã có ở mục 3 — không đổi phạm vi/thứ tự buổi, chỉ chi tiết hóa để bắt đầu code. Set `active_plan.md` sang Phase 0: `scripts/utils/markov.py` (7 hàm Markov thủ công).
- `[QUYẾT ĐỊNH]` **Trạng thái hấp thụ: 6 trạng thái, 2 trạng thái hấp thụ (Default/Foreclosure + Prepaid) — Phương án B.** HUNG chốt, sau khi so sánh với Phương án A (censoring + PD kỳ hạn hữu hạn). Lý do: giữ `B=NR` ở dạng chuẩn (2.18), tách bạch 2 kết cục cạnh tranh (vỡ nợ trước khi trả hết nợ), không cần thêm khái niệm censoring/horizon riêng cho việc ước lượng B trọn đời. Đánh đổi: lệch khỏi mô tả "5 trạng thái" gốc trong `PROJECT_BRIEF.md`/`master_plan.md` (đã cập nhật lại), backtest §4.5 vẫn cần công thức kỳ hạn hữu hạn (2.19) áp cho cột Default của R (vì validation set hữu hạn kỳ).
- `[TASK]` Cập nhật tài liệu theo quyết định trên (chưa động vào code, vì code chưa tồn tại): `PROJECT_BRIEF.md` §3, `plans/master_plan.md` §1, `CLAUDE.md` (project-level), `plans/active_plan.md` (đồng bộ lại theo tình trạng thực tế — trước đó bị lệch mốc, còn ghi ngày 2026-09-07 dù đã có nháp Ch.1–3 báo cáo), và báo cáo `outputs/TranNhatHung_MAT6206_BaoCaoCuoiKy/noi_dung_chi_tiet/`: Ch.1 §1.4.2 (mô tả 6 trạng thái), Ch.2 §2.5.5 (chốt phương án B), Ch.3 §3.2.1/3.2.2/3.3/3.4.5 (bảng ánh xạ trạng thái, công thức B/PD_i(H) theo cột Default).
- `[RỦI RO]` Còn 3 mục `[CẦN CHỐT]` trong Ch.3: ngưỡng chính xác của trạng thái Default (gộp `RA`/zero-balance 02,03,09/DPD≥180 ngày ra sao), cách gộp mã `>=03` vào bucket 90+ DPD, và kỳ hạn backtest $H$ (đề xuất 12/24 tháng). Cần chốt trước khi bắt đầu code Buổi 2.

---

## 2026-09-22 (tiếp — mở rộng dữ liệu + chốt định nghĩa Default)

- `[PHẠM VI]` **Mở rộng dữ liệu ước lượng từ 1 vintage (2016, 50.000 khoản vay) sang 3 vintage gộp (2016+2017+2018, 150.000 khoản vay).** HUNG tự tải thêm `sample_orig_2017.txt`, `sample_perf_2017.txt`, `sample_orig_2018.txt`, `sample_perf_2018.txt` vào `data/raw/`. Lý do: kiểm tra thực tế cho thấy trên 1 vintage, ngay cả định nghĩa Default rộng nhất (ngưỡng 180 ngày) cũng chỉ có ~1.376 sự kiện trên 50.000 khoản vay — không đủ mạnh cho kiểm định §4.2 và backtest theo từng trạng thái xuất phát §4.5. Kiểm tra: schema 3 file `perf` khớp nhau (35 cột), `loan_id` không trùng khóa giữa 3 vintage (prefix `F16/F17/F18`), cùng mốc cắt performance `202603` cho cả 3 → gộp trực tiếp được, chia estimation/validation theo lịch vẫn áp dụng đồng nhất. Tổng sau gộp: 150.000 khoản vay (orig), 8.239.433 dòng (perf, exact: 3.379.650+2.800.219+2.059.564).
- `[KẾT QUẢ]` Đếm lại 3 phương án định nghĩa Default trên bộ gộp 3 vintage (dùng `awk` trực tiếp trên file thô, không qua code chính thức — chỉ để ra quyết định):

  | Phương án | Định nghĩa | Số sự kiện (2016 riêng) | Số sự kiện (3 vintage gộp) |
  |---|---|---|---|
  | A | `RA` ∪ zero-balance{02,03,09} | 78 | 215 |
  | B | A ∪ delinquency ≥ `03` (90+ ngày) | 2.367 | 7.991 |
  | C | A ∪ delinquency ≥ `06` (180+ ngày) | 1.376 | 4.921 |

  Số liệu phụ trợ (3 vintage gộp): prepaid (`zbc=01`) = 112.875 (75,3%); từng chạm 90+ DPD = 7.990 khoản (5,3%); từng chạm 180+ DPD = 4.907 khoản (3,3%); tổn thất tín dụng thực tế thuần túy (`zbc`∈{02,03,09}) = 205; `RA` = 88.
- `[QUYẾT ĐỊNH]` **Chọn Phương án C — ngưỡng Default = 180 ngày quá hạn (`delinquency_status ≥ '06'`) HOẶC `RA` HOẶC `zero_balance_code ∈ {02,03,09}`, kèm quy tắc "sticky absorbing".** HUNG chốt. Lý do chọn C thay A: A quá thưa sự kiện (215/150.000 = 0,14%) ngay cả sau khi mở rộng dữ liệu. Lý do chọn C thay B: ngưỡng 90 ngày của B trùng đúng ranh giới vào state 3 "90+ DPD" — gần như toàn bộ 7.990 khoản từng chạm 90+ đều bị gộp ngay vào Default (7.991/7.990), khiến state 3 mất ý nghĩa của một trạng thái tạm thời riêng biệt. C giữ được ~3.083 khoản đi qua 90–179 ngày mà không chạm Default, đồng thời có 4.921 sự kiện — đủ cho các kiểm định Chương 4.
  - **Quy tắc "sticky absorbing" đi kèm:** vì `delinquency_status` có thể giảm sau khi trả một phần (quan sát thực tế trong dữ liệu, ví dụ chuỗi `07→01→02→03`), một khi khoản vay chạm điều kiện Default lần đầu, mọi bản ghi sau đó trong quỹ đạo bị ép gán Default — không cho "cure" khỏi state 4.
- `[TASK]` Cập nhật tài liệu theo 2 quyết định trên (vẫn chưa động vào code): `PROJECT_BRIEF.md` §3, `plans/master_plan.md` §1, `plans/active_plan.md` (toàn bộ), `data/raw/DATA_DICTIONARY.md` (mô tả 3 vintage + bảng ánh xạ 6 state + quy tắc sticky), báo cáo `outputs/TranNhatHung_MAT6206_BaoCaoCuoiKy/noi_dung_chi_tiet/`: Ch.1 §1.2/1.4.1/1.4.2 (mô tả mẫu 3 vintage), Ch.3 §3.1.2 (số liệu mẫu + lý do mở rộng + hạn chế trộn vintage), §3.2.1 (bảng ánh xạ Default cuối cùng + bảng so sánh A/B/C + quy tắc sticky), §3.2.3 (mốc chia estimation/validation cập nhật theo kỳ báo cáo mới).
- `[RỦI RO]` Trộn 3 vintage làm mẫu không đồng nhất về tuổi khoản vay tại cùng một thời điểm lịch (vintage 2016 "già" hơn 2018 hai năm tại cùng tháng báo cáo) — mô hình vẫn giả định xác suất chuyển không phụ thuộc vintage/tuổi. Đã ghi vào Ch.3 §3.1.2 như một hạn chế, cần nhắc lại ở phần Kết luận nếu kiểm định thuần nhất theo thời gian (§4.2) bác bỏ $H_0$.
- `[RỦI RO]` Chỉ còn 1 mục `[CẦN CHỐT]` trong Ch.3: kỳ hạn backtest $H$ cho §4.5 (đề xuất 12 và 24 tháng). Cần chốt trước khi bắt đầu code Buổi 2.

---

## 2026-09-22 (tiếp — chốt kỳ hạn backtest, toàn bộ quyết định thiết kế đã xong)

- `[KẾT QUẢ]` Đếm thử (bằng `awk` trên dữ liệu thô, không qua code chính thức) số khoản vay theo trạng thái xuất phát tại mốc $\tau \approx$ 02/2024 (đầu tập validation dự kiến) trên bộ gộp 3 vintage, và số sự kiện Default quan sát được trong 12 tháng vs 24 tháng sau đó:

  | State $i$ | N tại $\tau$ | Default trong 12m | Default trong 24m |
  |---|---|---|---|
  | 0 Current | 39.195 | 34 (0,09%) | 98 (0,25%) |
  | 1 30 DPD | 392 | 15 (3,8%) | 29 (7,4%) |
  | 2 60 DPD | 84 | 13 (15,5%) | 17 (20,2%) |
  | 3 90+ DPD | 70 | 38 (54,3%) | 42 (60,0%) |

  Nhận xét: $H=24$ tăng mạnh số sự kiện ở nhóm Current (34→98) nhưng chỉ vừa khít tập validation (~25 tháng, đệm còn ~1 tháng tới mốc cắt 202603); $H=12$ có đệm an toàn hơn (~13 tháng) và với nhóm 90+ DPD gần như không thêm thông tin (38→42) vì khoản vay nhóm này vỡ nợ rất nhanh nếu vỡ nợ. Nhóm 1, 2 luôn mỏng bất kể $H$.
- `[QUYẾT ĐỊNH]` **Chọn Phương án A — chỉ dùng kỳ hạn $H=12$ tháng cho backtest §4.5, không dùng thêm $H=24$.** HUNG chốt. Lý do: giữ đúng tinh thần "cảnh báo sớm" của đề tài, an toàn hơn về dữ liệu (nhiều đệm hơn tới mốc cắt), đơn giản hóa việc trình bày Chương 4 (1 bộ kết quả thay vì 2). Đánh đổi: bỏ qua lợi ích tăng sức mạnh thống kê mà $H=24$ mang lại cho nhóm Current; đã ghi vào Ch.3 §3.4.5 rằng nhóm $i=1,2$ (392 và 84 khoản) sẽ có khoảng tin cậy rộng bất kể lựa chọn $H$ — là hạn chế của mẫu, không phải của $H=12$.
- `[TASK]` Cập nhật tài liệu theo quyết định trên (chưa động vào code): `plans/active_plan.md` (mục "Quyết định đã chốt" #4, xóa mục "Việc còn mở"), `outputs/TranNhatHung_MAT6206_BaoCaoCuoiKy/outline.md` (đánh dấu Ch.3 hết CẦN CHỐT, cập nhật mục "Đã chốt trước khi viết Ch.4"), Ch.3 §3.4.5 (banner đầu file + nội dung backtest cố định theo $H=12$, công thức $\mathrm{PD}_i(12)$).
- `[TASK]` **Toàn bộ 4 quyết định thiết kế trước khi code (trạng thái hấp thụ, mở rộng dữ liệu 3 vintage, ngưỡng Default, kỳ hạn backtest) đã chốt.** Sẵn sàng bắt đầu Buổi 2 — dựng `scripts/`, viết pipeline tiền xử lý.

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

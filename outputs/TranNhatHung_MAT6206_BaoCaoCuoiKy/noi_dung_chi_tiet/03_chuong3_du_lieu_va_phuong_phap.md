# CHƯƠNG 3: DỮ LIỆU VÀ PHƯƠNG PHÁP

> **[Đã chốt toàn bộ — 2026-09-22, xem `plans/logs.md`]** (1) mô hình sáu trạng thái, hai trạng thái hấp thụ Default/Prepaid (mục 2.5.5); (2) mẫu dữ liệu mở rộng sang 3 vintage 2016–2018 (150.000 khoản vay); (3) định nghĩa trạng thái Default = ngưỡng 180 ngày quá hạn (Phương án C, mục 3.2.1); (4) kỳ hạn backtest $H=12$ tháng, không dùng $H=24$ (Phương án A, mục 3.4.5); (5) **Phase 1 (ETL) đã chạy thực tế 2026-09-22** — $\tau = 02/2024$ (số thật, xem mục 3.2.3), pipeline `scripts/01_build_trajectory.py` + `scripts/02_split_estimation_validation.py`, kết quả full run: 150.000 khoản vay, 8.239.433 dòng, 4.921 sự kiện Default (khớp chính xác Phương án C), 110.834 khoản Prepaid.

## 3.1. Dữ liệu

### 3.1.1. Nguồn dữ liệu

Nghiên cứu sử dụng **Freddie Mac Single-Family Loan-Level Dataset**, bộ dữ liệu công khai về các khoản vay thế chấp nhà ở cho một gia đình, lãi suất cố định, được Freddie Mac mua lại trên thị trường thứ cấp. Bộ dữ liệu gồm hai loại tệp cho mỗi năm khởi tạo khoản vay:

- **Tệp khởi tạo (origination file):** mỗi dòng là một khoản vay, chứa các đặc điểm tại thời điểm giải ngân (điểm tín dụng, tỷ lệ khoản vay trên giá trị tài sản, lãi suất, kỳ hạn, bang, …).
- **Tệp hiệu suất hàng tháng (monthly performance file):** mỗi dòng là một cặp khoản vay–tháng báo cáo, chứa dư nợ hiện tại, trạng thái quá hạn, tuổi khoản vay, và mã lý do khoản vay rời khỏi danh mục (nếu có).

Hai tệp được liên kết với nhau qua mã định danh khoản vay (`LOAN_SEQUENCE_NUMBER`).

### 3.1.2. Mẫu dữ liệu sử dụng

Nghiên cứu sử dụng bộ **Sample** ứng với **ba năm khởi tạo 2016, 2017, 2018** (gộp), với các đặc điểm đã kiểm tra:

| Đặc điểm | Giá trị |
|---|---|
| Số khoản vay (tệp khởi tạo, gộp 3 vintage) | 150.000 (50.000 mỗi vintage) |
| Số bản ghi khoản vay–tháng (tệp hiệu suất, gộp) | 8.239.433 (2016: 3.379.650; 2017: 2.800.219; 2018: 2.059.564) |
| Kỳ báo cáo | 01/2016 (vintage 2016) / 01/2017 (2017) / 01/2018 (2018) – 03/2026, cùng mốc cắt |
| Tần suất | Theo tháng |
| Định dạng | Văn bản phân cách bằng ký tự `|`, không có dòng tiêu đề |

Ba tệp cùng layout 35 cột (Release 47), `loan_id` không trùng khóa giữa các vintage (tiền tố `F16/F17/F18`) nên gộp trực tiếp theo `loan_id` mà không cần xử lý xung đột khóa.

**Lý do mở rộng sang 3 vintage (quyết định 2026-09-22).** Bản dựng ban đầu chỉ dùng vintage 2016 (50.000 khoản vay). Khi thiết kế định nghĩa trạng thái Default (mục 3.2.1), kiểm tra thực tế cho thấy số sự kiện Default trên 1 vintage quá mỏng để kiểm định giả thiết (mục 4.2) và backtest theo từng trạng thái xuất phát (mục 4.5) có sức mạnh thống kê chấp nhận được — kể cả với ngưỡng nới lỏng nhất (180 ngày quá hạn) chỉ có khoảng 1.376 sự kiện trên 50.000 khoản vay. Gộp thêm 2 vintage độc lập (2017, 2018) đưa số sự kiện Default lên 4.921 trên 150.000 khoản vay (xem mục 3.2.1), đồng thời giữ nguyên các mốc thời gian quan sát then chốt (COVID-19 2020–2021, chu kỳ tăng lãi suất 2022–2023) cho kiểm định tính thuần nhất.

**Đánh đổi cần lưu ý (hạn chế mô hình, thảo luận lại ở Kết luận):** việc trộn 3 vintage làm mẫu không còn đồng nhất về tuổi khoản vay tại mỗi thời điểm lịch — tại một tháng báo cáo cho trước, vintage 2016 đã "già" hơn vintage 2018 hai năm. Mô hình vẫn giả định xác suất chuyển chỉ phụ thuộc trạng thái hiện tại (không phụ thuộc vintage/tuổi khoản vay), nên nếu tồn tại hiệu ứng vintage/seasoning thực sự, sai lệch đó sẽ không được mô hình bắt được và có thể là một phần nguyên nhân nếu kiểm định thuần nhất theo thời gian (mục 4.2) bác bỏ $H_0$.

### 3.1.3. Các trường dữ liệu sử dụng

| Trường | Tệp | Vai trò trong nghiên cứu |
|---|---|---|
| `LOAN_SEQUENCE_NUMBER` | Khởi tạo, hiệu suất | Định danh khoản vay, khóa liên kết |
| `MONTHLY_REPORTING_PERIOD` | Hiệu suất | Tháng báo cáo (định dạng YYYYMM), chỉ số thời gian $t$ |
| `CURRENT_LOAN_DELINQUENCY_STATUS` | Hiệu suất | Mức quá hạn, cơ sở rời rạc hóa trạng thái |
| `ZERO_BALANCE_CODE` | Hiệu suất | Lý do dư nợ về 0 (trả hết, bán nợ, xử lý tài sản, …) |
| `ZERO_BALANCE_EFFECTIVE_DATE` | Hiệu suất | Thời điểm khoản vay rời khỏi danh mục |

Các trường đặc điểm khoản vay trong tệp khởi tạo không được đưa vào mô hình (theo phạm vi ở mục 1.4.2), chỉ dùng cho mô tả thống kê.

## 3.2. Tiền xử lý dữ liệu

### 3.2.1. Rời rạc hóa trạng thái

Trường `CURRENT_LOAN_DELINQUENCY_STATUS` ghi nhận số chu kỳ thanh toán bị chậm: `00` là đúng hạn (hoặc chậm dưới 30 ngày), `01` là chậm 30–59 ngày, `02` là chậm 60–89 ngày, `03` là chậm 90–119 ngày, và tiếp tục tăng dần; giá trị `RA` biểu thị khoản vay đã chuyển thành tài sản thu hồi (REO Acquisition). Trong mẫu dữ liệu, mã `00` chiếm khoảng 98,4% số bản ghi.

Trường `ZERO_BALANCE_CODE` cho biết lý do dư nợ khoản vay về 0: `01` trả hết trước hạn hoặc đáo hạn; `02` bán cho bên thứ ba (qua đấu giá tịch biên); `03` bán thiếu (short sale) hoặc xóa nợ; `09` xử lý tài sản thu hồi (REO disposition); `15`, `16` bán khoản vay (bán nợ, bán khoản vay đã tái hoạt động); `96` loại bỏ khỏi danh mục (mua lại). Trong mẫu, mã `01` chiếm đa số tuyệt đối (35.734 khoản vay).

**Quyết định (2026-09-22):** mô hình dùng **sáu trạng thái**, hai trạng thái hấp thụ — Default/Foreclosure và Prepaid — theo Phương án B của mục 2.5.5, nhằm giữ $B = NR$ ở dạng chuẩn (2.18) và tách bạch hai kết cục cạnh tranh (vỡ nợ trước khi trả hết nợ, hay ngược lại), thay vì phải kiểm duyệt (censoring) quỹ đạo và chuyển sang xác suất vỡ nợ theo kỳ hạn hữu hạn.

Quy tắc ánh xạ sang sáu trạng thái của mô hình:

| Điều kiện trên dữ liệu gốc | Trạng thái mô hình |
|---|---|
| Delinquency = `00` | 0 — Current |
| Delinquency = `01` | 1 — 30 DPD |
| Delinquency = `02` | 2 — 60 DPD |
| Delinquency $\in \{03, 04, 05\}$ (90–179 ngày), chưa thỏa điều kiện Default | 3 — 90+ DPD |
| Delinquency = `RA`, hoặc zero-balance $\in$ {`02`, `03`, `09`}, hoặc Delinquency $\ge$ `06` (**$\ge$ 180 ngày quá hạn**) | 4 — Default/Foreclosure (hấp thụ) |
| Zero-balance = `01` (trả hết nợ trước hạn/đáo hạn) | 5 — Prepaid (hấp thụ) |

**Quyết định (2026-09-22) — Phương án C.** Ngưỡng Default = 180 ngày quá hạn (mã $\ge$ `06`), hợp với các mã tất toán do tổn thất tín dụng thực tế (`RA`, zero-balance {02,03,09}). Đây là kết quả so sánh 3 phương án trên bộ gộp 3 vintage (150.000 khoản vay, xem `plans/logs.md` 2026-09-22):

| Phương án | Định nghĩa | Số sự kiện Default |
|---|---|---|
| A | Chỉ tổn thất tín dụng thực tế: `RA` $\cup$ zbc{02,03,09} | 215 |
| B | A $\cup$ Delinquency $\ge$ `03` (90+ ngày) | 7.991 |
| **C (đã chọn)** | A $\cup$ Delinquency $\ge$ `06` (180+ ngày) | **4.921** |

Lý do chọn C thay vì A: A quá thưa sự kiện cho kiểm định/backtest chia theo trạng thái xuất phát. Lý do chọn C thay vì B: ngưỡng 90 ngày của B trùng đúng ranh giới vào state 3, khiến gần như toàn bộ số khoản vay từng chạm 90+ DPD (7.990/7.990 trên bộ gộp) bị gộp thẳng vào Default — state 3 mất hết ý nghĩa của một trạng thái tạm thời riêng biệt. C giữ được khoảng 3.083 khoản vay đi qua 90–179 ngày mà không chạm ngưỡng Default, đồng thời có đủ 4.921 sự kiện cho các kiểm định ở Chương 4.

**Quy tắc "sticky absorbing".** `delinquency_status` có thể giảm sau khi người vay trả một phần (dữ liệu thực tế quan sát được chuỗi như `07 → 01 → 02 → 03`). Vì Default phải là trạng thái hấp thụ tuyệt đối, một khi khoản vay chạm điều kiện Default lần đầu tiên (theo bảng trên), **mọi bản ghi sau đó trong quỹ đạo của khoản vay đó bị ép gán trạng thái 4 — Default**, bất kể giá trị `delinquency_status` báo cáo thực tế giảm xuống bao nhiêu. Không có "cure" khỏi state 4 trong phạm vi mô hình này.

Không gian trạng thái tạm thời $\mathcal{T} = \{0, 1, 2, 3\}$, không gian hấp thụ $\{4, 5\}$; $R$ có hai cột (cột Default, cột Prepaid) và $b_{i,\text{Default}} + b_{i,\text{Prepaid}} = 1$ với mọi $i \in \mathcal{T}$.

Các khoản vay rời danh mục vì lý do không phải sự kiện tín dụng (mã `15`, `16`, `96`) được xử lý như **kiểm duyệt**: quỹ đạo kết thúc tại tháng cuối cùng quan sát được, không ghi nhận lần chuyển giả sang trạng thái hấp thụ nào.

### 3.2.2. Xây dựng bảng quỹ đạo trạng thái

Từ tệp hiệu suất, dữ liệu được sắp xếp theo `(LOAN_SEQUENCE_NUMBER, MONTHLY_REPORTING_PERIOD)` để thu được bảng quỹ đạo dạng dài với cấu trúc `(loan_id, month, state)`. Các bước xử lý:

1. **Kiểm tra chất lượng:** loại bỏ bản ghi trùng lặp theo cặp (khoản vay, tháng); kiểm tra giá trị thiếu ở trường trạng thái; kiểm tra tính liên tục của chuỗi tháng. Nếu một khoản vay bị gián đoạn tháng báo cáo, quỹ đạo được tách tại điểm gián đoạn để không tạo ra lần chuyển giả qua nhiều tháng.
2. **Cắt quỹ đạo sau hấp thụ:** một khi khoản vay vào trạng thái Default hoặc Prepaid, các bản ghi sau đó (nếu có) bị loại bỏ, đảm bảo đúng tính chất hấp thụ.
3. **Tạo các bảng chuyển trạng thái** phục vụ các phần khác nhau của Chương 4:
   - cặp liên tiếp $(S_t, S_{t+1})$ — ước lượng $\hat{P}$ (mục 4.1) và kiểm định thuần nhất (mục 4.2);
   - bộ ba liên tiếp $(S_{t-1}, S_t, S_{t+1})$ — kiểm định bậc Markov (mục 4.2);
   - cặp cách ba tháng $(S_t, S_{t+3})$ — ước lượng trực tiếp $\hat{P}^{(3)}$ cho kiểm chứng Chapman–Kolmogorov (mục 4.3).

Mỗi lần chuyển được gắn với **tháng xảy ra chuyển** (tháng $t+1$), làm căn cứ chia dữ liệu theo thời gian.

### 3.2.3. Chia dữ liệu theo thời gian

Vì đây là dữ liệu chuỗi thời gian, việc chia ngẫu nhiên sẽ làm rò rỉ thông tin của tương lai vào quá trình ước lượng. Việc chia áp dụng theo **mốc lịch chung** $\tau$ cho cả 3 vintage (hợp lệ vì cả 3 vintage cùng chung một mốc cắt 03/2026, chỉ khác điểm bắt đầu quan sát):

- **Tập ước lượng (estimation set):** các lần chuyển xảy ra trong khoảng 80% số tháng đầu tiên của khung quan sát chung, từ 01/2016 đến **$\tau=$ 02/2024** (98/123 tháng trên trục lịch gộp; vintage 2017/2018 chỉ đóng góp dữ liệu từ điểm bắt đầu quan sát của mình). Toàn bộ tham số $\hat{P}$, $\hat{\pi}$, $\hat{N}$, $\hat{B}$ và các kiểm định ở mục 4.1–4.4 chỉ sử dụng tập này. Kết quả thật: 7.253.423 dòng, 150.000 khoản vay, 4.728 khoản chạm Default trong khung thời gian này.
- **Tập kiểm định (validation set):** 20% số tháng cuối, từ 03/2024 đến 03/2026 (25 tháng), chỉ dùng cho backtest ở mục 4.5. Kết quả thật: 986.010 dòng, 42.458 khoản vay, 2.910 khoản chạm Default.

**$\tau = 02/2024$ (số thật, chạy 2026-09-22)** — tính bằng mốc percentile 80% trên trục lịch gộp liên tục 201601–202603 (123 tháng, mốc thứ 98), khớp với ước tính $\tau\approx$02/2024 đã dùng để size backtest $H=12$ ở mục 3.4.5. Pipeline: `scripts/01_build_trajectory.py` (xây quỹ đạo, rời rạc hóa 6 state, sticky absorbing) → `scripts/02_split_estimation_validation.py` (tính $\tau$, chia tập). Artifact: `data/processed/{loan_trajectory,estimation_set,validation_set}_full.parquet`.

## 3.3. Phương pháp ước lượng và tính toán

Toàn bộ các phép tính của mô hình được **tự cài đặt** bằng Python (thư viện `pandas`, `numpy`, `scipy.stats`), không sử dụng các thư viện mô hình Markov, HMM hay phân tích sống sót có sẵn, nhằm đảm bảo mỗi kết quả đều truy vết được về công thức ở Chương 2.

1. **Ma trận đếm và MLE:** đếm $n_{ij}$ từ bảng cặp chuyển theo (2.7), chuẩn hóa theo hàng để được $\hat{P}$ theo (2.10); gán hàng hấp thụ bằng vectơ đơn vị.
2. **Ma trận chuyển nhiều bước:** tính $\hat{P}^n$ bằng phép nhân ma trận lặp theo (2.12).
3. **Phân phối dừng:** giải hệ tuyến tính (2.14) với điều kiện chuẩn hóa như mô tả ở mục 2.4.3; tính thêm phân phối tựa dừng từ $\hat{Q}$ nếu cần thiết cho diễn giải (mục 2.4.4).
4. **Ma trận cơ bản và xác suất hấp thụ:** tách $\hat{Q}$ (4×4, bốn trạng thái tạm thời) và $\hat{R}$ (4×2, hai cột Default/Prepaid) theo dạng chuẩn (2.15); thay vì nghịch đảo ma trận trực tiếp, giải hệ tuyến tính $(I - \hat{Q})\hat{B} = \hat{R}$ và $(I - \hat{Q})\hat{\tau} = \mathbf{1}$ để đảm bảo ổn định số; $\hat{B}$ có hai cột $\hat{b}_{i,\text{Default}}$, $\hat{b}_{i,\text{Prepaid}}$. Cho backtest kỳ hạn hữu hạn (mục 3.4.5), áp dụng (2.19) riêng cho cột Default: $\mathrm{PD}_i(H) = \big[(I - \hat{Q}^H)\hat{B}\big]_{i,\text{Default}}$.

## 3.4. Thiết kế kiểm định và đánh giá mô hình

### 3.4.1. Kiểm định tính thuần nhất theo thời gian

- **Giai đoạn con:** chia tập ước lượng theo **năm dương lịch** của tháng xảy ra chuyển. Kết quả chạy thực tế (mục 4.2.1): 9 giai đoạn (2016–2024), mỗi năm đều đủ quan sát (năm ít nhất — 2024 — vẫn có 80.133 quan sát ở 4 trạng thái tạm thời) nên không cần gộp giai đoạn nào; quy tắc gộp năm liền kề khi thiếu quan sát vẫn giữ trong thiết kế cho trường hợp tổng quát.
- **Kiểm định tổng thể:** áp dụng (2.20)/(2.21) cho toàn bộ $G$ giai đoạn, bậc tự do theo (2.22).
- **Kiểm định từng cặp:** so sánh các cặp năm liền kề (và cặp trước/sau 2020) với $G = 2$, hiệu chỉnh Bonferroni cho mức ý nghĩa.
- **Mức ý nghĩa:** $\alpha = 0{,}05$.
- **Đánh giá bổ sung:** chuẩn Frobenius giữa $\hat{P}(g)$ và $\hat{P}$ gộp cho từng giai đoạn, nhằm đánh giá ý nghĩa thực tiễn của sự khác biệt (mục 2.6.4).

### 3.4.2. Kiểm định bậc Markov

- Từ bảng bộ ba $(S_{t-1}, S_t, S_{t+1})$ trong tập ước lượng, tính $n_{hij}$, $\hat{p}_{hij}$ và $\hat{p}_{ij}$ trên cùng tập bộ ba.
- Tính thống kê $\Lambda_{\text{bậc}}$ theo (2.23), bậc tự do theo (2.24), p-value từ phân phối $\chi^2$.
- $H_0$: xích bậc 1 là đủ; mức ý nghĩa $\alpha = 0{,}05$.
- Bổ sung: so sánh trực quan một số hàng $\hat{p}_{hi\cdot}$ theo các giá trị $h$ khác nhau (ví dụ trạng thái 30 DPD khi đến từ Current so với khi đến từ 60 DPD) để diễn giải nguồn gốc khác biệt.

### 3.4.3. Kiểm chứng Chapman–Kolmogorov

- Tính $\hat{P}^3$ từ ma trận tháng và $\hat{P}^{(3)}_{\text{trực tiếp}}$ từ bảng cặp cách ba tháng, cả hai trên tập ước lượng.
- Định lượng sai lệch bằng chuẩn Frobenius (2.13), sai lệch tuyệt đối lớn nhất, và bảng chênh lệch từng ô; trực quan hóa bằng heatmap chênh lệch.

### 3.4.4. Phân phối dừng và phân phối thực nghiệm

- Tính phân phối dừng lý thuyết từ $\hat{P}$ và diễn giải theo mục 2.4.4.
- So sánh phân phối trạng thái thực tế quan sát tại các thời điểm với phân phối mô hình dự báo $\mu^{(t_0)} \hat{P}^{t - t_0}$ xuất phát từ phân phối quan sát tại một thời điểm gốc $t_0$, và (nếu dùng) với phân phối tựa dừng.

### 3.4.5. Backtest xác suất vỡ nợ trên tập kiểm định

Đây là bước đánh giá quan trọng nhất của báo cáo, đối chiếu dự báo của mô hình với thực tế ngoài mẫu:

**Quyết định (2026-09-22) — Phương án A: chỉ dùng kỳ hạn $H = 12$ tháng.** Lý do: tập validation chỉ dài ~25 tháng nên $H$ không thể vượt quá khoảng này; $H=12$ giữ đúng tinh thần "cảnh báo **sớm**" của đề tài, dữ liệu dư đệm an toàn (~13 tháng) so với mốc cắt, còn $H=24$ chỉ vừa khít tập validation (đệm ~1 tháng) và làm loãng tính "sớm". Kiểm tra trên bộ gộp 3 vintage tại mốc $\tau \approx$ 02/2024: số khoản vay theo trạng thái xuất phát và số sự kiện Default quan sát trong 12 tháng sau đó — $i=0$ (Current): 39.195 khoản, 34 sự kiện; $i=1$ (30 DPD): 392 khoản, 15 sự kiện; $i=2$ (60 DPD): 84 khoản, 13 sự kiện; $i=3$ (90+ DPD): 70 khoản, 38 sự kiện. Nhóm $i=1,2$ vốn mỏng nên khoảng tin cậy sẽ rộng bất kể chọn $H$ nào — nêu rõ như một hạn chế ở mục 3.4.5 bước 4 và ở phần Kết luận.

1. Tại mốc $\tau$ (đầu giai đoạn kiểm định), xác định trạng thái của mọi khoản vay còn trong danh mục; nhóm các khoản vay theo trạng thái xuất phát $i \in \{0, 1, 2, 3\}$.
2. **Dự báo:** với mỗi $i$, tính xác suất vỡ nợ mô hình dự báo trong 12 tháng, $\mathrm{PD}_i(12) = \big[(I - \hat{Q}^{12})\hat{B}\big]_{i,\text{Default}}$ (cột Default của $\hat B$, theo mục 3.3), sử dụng tham số ước lượng từ tập ước lượng.
3. **Thực tế:** theo dõi các khoản vay trong nhóm $i$ qua 12 tháng của tập kiểm định, tính tỷ lệ vỡ nợ quan sát được $\widehat{\mathrm{DR}}_i(12)$ = số khoản vay vào Default trong 12 tháng / số khoản vay trong nhóm. Khoản vay rơi vào Prepaid trong 12 tháng được tính là **không vỡ nợ** (kết cục cạnh tranh, khớp với ý nghĩa cột Default của $\hat B$), không loại khỏi mẫu số.
4. **Đối chiếu:** so sánh $\mathrm{PD}_i(12)$ với $\widehat{\mathrm{DR}}_i(12)$ cho từng trạng thái xuất phát; kiểm tra xem tỷ lệ thực tế có nằm trong khoảng tin cậy nhị thức xấp xỉ $\mathrm{PD}_i(12) \pm 1{,}96\sqrt{\mathrm{PD}_i(12)(1 - \mathrm{PD}_i(12))/m_i}$ hay không, với $m_i$ là số khoản vay trong nhóm; đánh giá mô hình dự báo cao hay thấp một cách có hệ thống, và liên hệ với kết quả kiểm định thuần nhất ở mục 4.2.

## 3.5. Công cụ thực hiện

- **Ngôn ngữ:** Python 3.11.
- **Thư viện:** `pandas`, `numpy` (xử lý dữ liệu, đại số tuyến tính), `scipy.stats` (phân phối $\chi^2$, p-value), `matplotlib`, `seaborn` (heatmap, biểu đồ).
- **Tổ chức mã nguồn:** pipeline gồm các script đánh số theo thứ tự chạy, các hàm Markov dùng chung (MLE, lũy thừa ma trận, $N$, $B$, phân phối dừng, các thống kê kiểm định) đặt trong một module tiện ích; toàn bộ kết quả của Chương 4 có thể tái lập bằng cách chạy lại pipeline từ dữ liệu gốc.

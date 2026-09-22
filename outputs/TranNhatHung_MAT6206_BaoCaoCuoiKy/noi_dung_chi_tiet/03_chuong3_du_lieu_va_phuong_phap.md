# CHƯƠNG 3: DỮ LIỆU VÀ PHƯƠNG PHÁP

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

**Lý do sử dụng ba năm khởi tạo.** Thiết kế ban đầu của nghiên cứu chỉ dùng vintage 2016 (50.000 khoản vay). Tuy nhiên, khi xây dựng định nghĩa trạng thái Default ở mục 3.2.1, việc đếm thử trên mẫu một vintage cho thấy số sự kiện vỡ nợ quá mỏng để các kiểm định ở mục 4.2 và đặc biệt là backtest theo từng trạng thái xuất phát ở mục 4.5 có sức mạnh thống kê chấp nhận được: ngay cả với ngưỡng rộng nhất trong các phương án được cân nhắc (180 ngày quá hạn) cũng chỉ thu được khoảng 1.376 sự kiện trên 50.000 khoản vay, và khi chia tiếp theo bốn trạng thái xuất phát thì mỗi nhóm chỉ còn vài chục quan sát. Gộp thêm hai vintage độc lập 2017 và 2018 nâng số sự kiện vỡ nợ lên 4.921 trên 150.000 khoản vay, đồng thời vẫn giữ nguyên các mốc thời gian quan trọng đối với kiểm định tính thuần nhất (giai đoạn COVID-19 2020–2021 và chu kỳ tăng lãi suất 2022–2023).

Cái giá phải trả của lựa chọn này là mẫu không còn đồng nhất về tuổi khoản vay: tại cùng một tháng báo cáo, khoản vay thuộc vintage 2016 đã "già" hơn khoản vay vintage 2018 đúng hai năm. Mô hình vẫn giả định xác suất chuyển chỉ phụ thuộc trạng thái quá hạn hiện tại, không phụ thuộc vintage hay tuổi khoản vay, nên nếu tồn tại hiệu ứng seasoning thực sự thì hiệu ứng đó không được mô hình nắm bắt và có thể là một phần nguyên nhân nếu kiểm định tính thuần nhất theo thời gian ở mục 4.2 bác bỏ $H_0$. Hạn chế này được thảo luận lại ở phần Kết luận.

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

Trường `CURRENT_LOAN_DELINQUENCY_STATUS` ghi nhận số chu kỳ thanh toán bị chậm: `00` là đúng hạn (hoặc chậm dưới 30 ngày), `01` là chậm 30–59 ngày, `02` là chậm 60–89 ngày, `03` là chậm 90–119 ngày, và tiếp tục tăng dần; giá trị `RA` biểu thị khoản vay đã chuyển thành tài sản thu hồi (REO Acquisition). Trong mẫu dữ liệu, mã `00` chiếm 97,87% số bản ghi (8.063.538 trên 8.239.433 bản ghi khoản vay–tháng), cho thấy danh mục phần lớn ở trạng thái trả nợ đúng hạn.

Trường `ZERO_BALANCE_CODE` cho biết lý do dư nợ khoản vay về 0: `01` trả hết trước hạn hoặc đáo hạn; `02` bán cho bên thứ ba (qua đấu giá tịch biên); `03` bán thiếu (short sale) hoặc xóa nợ; `09` xử lý tài sản thu hồi (REO disposition); `15`, `16` bán khoản vay (bán nợ, bán khoản vay đã tái hoạt động); `96` loại bỏ khỏi danh mục (mua lại). Trong mẫu, mã `01` chiếm đa số tuyệt đối với 112.875 khoản vay, tức khoảng ba phần tư danh mục rời mẫu vì trả hết nợ chứ không phải vì vỡ nợ.

Trên cơ sở đó, mô hình sử dụng **sáu trạng thái** với hai trạng thái hấp thụ là Default/Foreclosure và Prepaid, theo phương án đã phân tích ở mục 2.5.5. Cách làm này giữ được $B = NR$ ở dạng chuẩn (2.18) và tách bạch hai kết cục cạnh tranh — khoản vay vỡ nợ trước khi trả hết, hay trả hết trước khi vỡ nợ — thay vì phải kiểm duyệt quỹ đạo và chỉ còn làm việc được với xác suất vỡ nợ theo kỳ hạn hữu hạn.

Quy tắc ánh xạ sang sáu trạng thái của mô hình:

| Điều kiện trên dữ liệu gốc | Trạng thái mô hình |
|---|---|
| Delinquency = `00` | 0 — Current |
| Delinquency = `01` | 1 — 30 DPD |
| Delinquency = `02` | 2 — 60 DPD |
| Delinquency $\in \{03, 04, 05\}$ (90–179 ngày), chưa thỏa điều kiện Default | 3 — 90+ DPD |
| Delinquency = `RA`, hoặc zero-balance $\in$ {`02`, `03`, `09`}, hoặc Delinquency $\ge$ `06` (**$\ge$ 180 ngày quá hạn**) | 4 — Default/Foreclosure (hấp thụ) |
| Zero-balance = `01` (trả hết nợ trước hạn/đáo hạn) | 5 — Prepaid (hấp thụ) |

**Về ngưỡng vào trạng thái Default.** Ranh giới giữa "quá hạn nặng" và "đã vỡ nợ" không có sẵn trong dữ liệu mà là một lựa chọn mô hình. Nghiên cứu cân nhắc ba phương án và đếm số sự kiện tương ứng trên toàn bộ 150.000 khoản vay:

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

1. **Kiểm tra chất lượng:** loại bỏ bản ghi trùng lặp theo cặp (khoản vay, tháng); kiểm tra giá trị thiếu ở trường trạng thái; kiểm tra tính liên tục của chuỗi tháng. Nếu một khoản vay bị gián đoạn tháng báo cáo, quỹ đạo được tách tại điểm gián đoạn để không tạo ra lần chuyển giả qua nhiều tháng. Trên toàn mẫu chỉ có duy nhất một khoản vay xuất hiện gián đoạn kiểu này, nên ảnh hưởng là không đáng kể.
2. **Áp quy tắc hấp thụ:** khi khoản vay chạm điều kiện Default hoặc Prepaid lần đầu tiên, mọi bản ghi sau đó của khoản vay vẫn được giữ trong bảng quỹ đạo nhưng bị ép gán đúng trạng thái hấp thụ đã chạm, theo quy tắc "sticky absorbing" ở mục 3.2.1. Trường hợp một khoản vay thỏa đồng thời cả hai điều kiện tại các thời điểm khác nhau, điều kiện Default được ưu tiên vì đây là sự kiện tín dụng xảy ra trước. Cách xử lý này khác với việc cắt bỏ phần đuôi quỹ đạo: nó giữ lại thông tin về số tháng khoản vay thực sự nằm trong trạng thái hấp thụ, đồng thời vẫn đảm bảo không có lần chuyển ngược nào ra khỏi trạng thái đó.
3. **Tạo các bảng chuyển trạng thái** phục vụ các phần khác nhau của Chương 4:
   - cặp liên tiếp $(S_t, S_{t+1})$ — ước lượng $\hat{P}$ (mục 4.1) và kiểm định thuần nhất (mục 4.2);
   - bộ ba liên tiếp $(S_{t-1}, S_t, S_{t+1})$ — kiểm định bậc Markov (mục 4.2);
   - cặp cách ba tháng $(S_t, S_{t+3})$ — ước lượng trực tiếp $\hat{P}^{(3)}$ cho kiểm chứng Chapman–Kolmogorov (mục 4.3).

Mỗi lần chuyển được gắn với **tháng xảy ra chuyển** (tháng $t+1$), làm căn cứ chia dữ liệu theo thời gian.

### 3.2.3. Chia dữ liệu theo thời gian

Vì đây là dữ liệu chuỗi thời gian, việc chia ngẫu nhiên sẽ làm rò rỉ thông tin của tương lai vào quá trình ước lượng. Việc chia áp dụng theo **mốc lịch chung** $\tau$ cho cả 3 vintage (hợp lệ vì cả 3 vintage cùng chung một mốc cắt 03/2026, chỉ khác điểm bắt đầu quan sát):

Mốc $\tau$ được xác định là tháng nằm ở phân vị 80% của trục lịch gộp liên tục từ 01/2016 đến 03/2026 (123 tháng, tương ứng tháng thứ 98), cho kết quả $\tau = 02/2024$. Hai tập dữ liệu thu được như sau:

- **Tập ước lượng:** các lần chuyển xảy ra từ 01/2016 đến hết 02/2024, gồm 7.253.423 bản ghi của 150.000 khoản vay, trong đó 4.728 khoản vay chạm trạng thái Default. Toàn bộ tham số $\hat{P}$, $\hat{\pi}$, $\hat{N}$, $\hat{B}$ và các kiểm định ở mục 4.1–4.4 chỉ sử dụng tập này.
- **Tập kiểm định:** 25 tháng cuối, từ 03/2024 đến 03/2026, gồm 986.010 bản ghi của 42.458 khoản vay còn hoạt động, trong đó 2.910 khoản vay chạm trạng thái Default. Tập này chỉ được dùng ở bước backtest tại mục 4.5.

Cần lưu ý rằng vintage 2017 và 2018 chỉ đóng góp dữ liệu kể từ tháng bắt đầu quan sát của chính chúng, nên tập ước lượng không cân bằng hoàn toàn giữa ba vintage ở các năm đầu.

## 3.3. Phương pháp ước lượng và tính toán

Toàn bộ các phép tính của mô hình được **tự cài đặt** bằng Python (thư viện `pandas`, `numpy`, `scipy.stats`), không sử dụng các thư viện mô hình Markov, HMM hay phân tích sống sót có sẵn, nhằm đảm bảo mỗi kết quả đều truy vết được về công thức ở Chương 2.

1. **Ma trận đếm và MLE:** đếm $n_{ij}$ từ bảng cặp chuyển theo (2.7), chuẩn hóa theo hàng để được $\hat{P}$ theo (2.10); gán hàng hấp thụ bằng vectơ đơn vị.
2. **Ma trận chuyển nhiều bước:** tính $\hat{P}^n$ bằng phép nhân ma trận lặp theo (2.12).
3. **Phân phối dừng:** giải hệ tuyến tính (2.14) kèm điều kiện chuẩn hóa như mô tả ở mục 2.4.3, bằng phương pháp bình phương tối thiểu. Phân phối tựa dừng nêu ở mục 2.4.4 được cân nhắc nhưng cuối cùng không sử dụng, vì phép so sánh có ý nghĩa thực nghiệm đã được thực hiện qua phân phối dự báo hữu hạn kỳ (mục 3.4.4).
4. **Ma trận cơ bản và xác suất hấp thụ:** tách $\hat{Q}$ (4×4, bốn trạng thái tạm thời) và $\hat{R}$ (4×2, hai cột Default/Prepaid) theo dạng chuẩn (2.15), tính $\hat{N} = (I - \hat{Q})^{-1}$ theo (2.16) và $\hat{B} = \hat{N}\hat{R}$ theo (2.18). Ma trận $\hat{Q}$ chỉ có kích thước 4×4 và cách xa ma trận suy biến nên phép nghịch đảo trực tiếp là ổn định về mặt số; số tháng kỳ vọng đến khi bị hấp thụ xuất phát từ trạng thái $i$ được tính bằng tổng hàng $i$ của $\hat{N}$. Cho backtest kỳ hạn hữu hạn ở mục 3.4.5, áp dụng (2.19) và lấy riêng cột Default: $\mathrm{PD}_i(H) = \big[(I - \hat{Q}^H)\hat{N}\hat{R}\big]_{i,\text{Default}}$.

## 3.4. Thiết kế kiểm định và đánh giá mô hình

### 3.4.1. Kiểm định tính thuần nhất theo thời gian

- **Giai đoạn con:** chia tập ước lượng theo **năm dương lịch** của tháng xảy ra chuyển, thu được 9 giai đoạn từ 2016 đến 2024. Thiết kế dự phòng quy tắc gộp hai năm liền kề nếu một năm có quá ít lần chuyển xuất phát từ các trạng thái quá hạn; trên dữ liệu thực tế, quy tắc này không phải dùng đến vì năm mỏng nhất (2024, chỉ tính đến mốc $\tau$) vẫn có 80.133 lần chuyển xuất phát từ bốn trạng thái tạm thời.
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

**Lựa chọn kỳ hạn.** Nghiên cứu chỉ sử dụng một kỳ hạn duy nhất là $H = 12$ tháng. Tập kiểm định dài khoảng 25 tháng nên về nguyên tắc có thể thử thêm $H = 24$, nhưng khi đó cửa sổ theo dõi vừa khít độ dài dữ liệu còn lại (chỉ dư khoảng một tháng đệm), bất kỳ khoản vay nào rời mẫu sớm cũng làm hỏng quan sát, và kỳ hạn hai năm cũng làm loãng ý nghĩa "cảnh báo **sớm**" của đề tài. Với $H = 12$, cửa sổ theo dõi còn dư khoảng 13 tháng đệm so với mốc cắt dữ liệu. Đếm thử tại mốc $\tau$ cho thấy quy mô từng nhóm như sau: trạng thái Current có 39.195 khoản vay, 30 DPD có 392 khoản, 60 DPD có 84 khoản và 90+ DPD có 70 khoản. Hai nhóm giữa vốn đã rất mỏng, nên khoảng tin cậy của tỷ lệ quan sát sẽ rộng bất kể chọn kỳ hạn nào; đây là hạn chế được nêu lại ở bước 4 dưới đây và ở phần Kết luận.

1. Tại mốc $\tau$, xác định trạng thái của mọi khoản vay còn trong danh mục và nhóm chúng theo trạng thái xuất phát $i \in \{0, 1, 2, 3\}$. Các khoản vay đã bị hấp thụ trước $\tau$ đương nhiên không thuộc nhóm nào, vì câu hỏi dự báo chỉ có nghĩa với khoản vay còn ở trạng thái tạm thời.
2. **Dự báo:** với mỗi $i$, tính xác suất vỡ nợ mô hình dự báo trong 12 tháng, $\mathrm{PD}_i(12) = \big[(I - \hat{Q}^{12})\hat{N}\hat{R}\big]_{i,\text{Default}}$, sử dụng tham số ước lượng hoàn toàn từ tập ước lượng.
3. **Thực tế:** theo dõi các khoản vay trong nhóm $i$ qua 12 tháng của tập kiểm định và tính tỷ lệ vỡ nợ quan sát được $\widehat{\mathrm{DR}}_i(12)$, bằng số khoản vay chạm trạng thái Default tại bất kỳ tháng nào trong cửa sổ chia cho số khoản vay $m_i$ của nhóm. Khoản vay rơi vào Prepaid trong cửa sổ được tính là **không vỡ nợ** đúng theo tinh thần kết cục cạnh tranh của cột Default trong $\hat{B}$, và không bị loại khỏi mẫu số. Khoản vay rời mẫu vì các lý do vận hành (mã `15`, `16`, `96`) mà chưa chạm trạng thái hấp thụ nào cũng được giữ trong mẫu số và tính là chưa xảy ra sự kiện; đây là quy ước đơn giản hóa, chấp nhận được vì nhóm này rất nhỏ và vì các kỹ thuật hiệu chỉnh kiểm duyệt nằm ngoài phạm vi nghiên cứu.
4. **Đối chiếu:** so sánh $\mathrm{PD}_i(12)$ với $\widehat{\mathrm{DR}}_i(12)$ cho từng trạng thái xuất phát. Để đánh giá xem chênh lệch có vượt quá mức dao động lấy mẫu hay không, nghiên cứu tính khoảng tin cậy Wilson 95% cho tỷ lệ quan sát $\widehat{\mathrm{DR}}_i(12)$ và kiểm tra xem giá trị dự báo $\mathrm{PD}_i(12)$ có rơi vào khoảng đó hay không. Khoảng Wilson được chọn thay cho khoảng xấp xỉ chuẩn thông thường vì nó vẫn cho kết quả hợp lệ khi tỷ lệ quan sát gần 0 hoặc khi cỡ mẫu nhóm nhỏ, đúng tình huống của các nhóm 60 DPD và 90+ DPD ở đây. Lưu ý rằng đây là khoảng tin cậy cho đại lượng thực nghiệm, không phải khoảng tin cậy cho tham số $\hat{B}$ của mô hình; việc định lượng độ bất định của chính $\hat{B}$ nằm ngoài phạm vi nghiên cứu và được nêu ở phần hướng phát triển.

## 3.5. Công cụ thực hiện

- **Ngôn ngữ:** Python 3.11.
- **Thư viện:** `pandas`, `numpy` (xử lý dữ liệu, đại số tuyến tính), `scipy.stats` (phân phối $\chi^2$, p-value), `matplotlib`, `seaborn` (heatmap, biểu đồ).
- **Tổ chức mã nguồn:** chương trình được tách thành các bước đánh số theo đúng thứ tự thực hiện (tiền xử lý và chia tập, ước lượng ma trận chuyển, kiểm định giả thiết, tính phân phối dừng và backtest). Các hàm Markov dùng chung — ước lượng hợp lý cực đại, lũy thừa ma trận, ma trận cơ bản $N$, xác suất hấp thụ $B$, phân phối dừng và các thống kê kiểm định — được gom vào một mô-đun tiện ích riêng và kiểm thử trước trên ma trận nhỏ có nghiệm tính tay được, trước khi áp lên dữ liệu thật. Nhờ cách tổ chức này, toàn bộ kết quả của Chương 4 có thể tái lập bằng cách chạy lại chương trình từ dữ liệu gốc.

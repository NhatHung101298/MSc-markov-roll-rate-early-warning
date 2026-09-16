# CHƯƠNG 3: DỮ LIỆU VÀ PHƯƠNG PHÁP

> **[CẦN CHỐT — xóa ghi chú này khi hoàn thiện]** Các mục đánh dấu **[CẦN CHỐT]** phụ thuộc vào quyết định định nghĩa trạng thái Default, cách xử lý khoản vay trả hết nợ trước hạn, và kỳ hạn backtest. Các con số về điểm chia tập dữ liệu là dự kiến, cần cập nhật theo kết quả chạy thực tế.

## 3.1. Dữ liệu

### 3.1.1. Nguồn dữ liệu

Nghiên cứu sử dụng **Freddie Mac Single-Family Loan-Level Dataset**, bộ dữ liệu công khai về các khoản vay thế chấp nhà ở cho một gia đình, lãi suất cố định, được Freddie Mac mua lại trên thị trường thứ cấp. Bộ dữ liệu gồm hai loại tệp cho mỗi năm khởi tạo khoản vay:

- **Tệp khởi tạo (origination file):** mỗi dòng là một khoản vay, chứa các đặc điểm tại thời điểm giải ngân (điểm tín dụng, tỷ lệ khoản vay trên giá trị tài sản, lãi suất, kỳ hạn, bang, …).
- **Tệp hiệu suất hàng tháng (monthly performance file):** mỗi dòng là một cặp khoản vay–tháng báo cáo, chứa dư nợ hiện tại, trạng thái quá hạn, tuổi khoản vay, và mã lý do khoản vay rời khỏi danh mục (nếu có).

Hai tệp được liên kết với nhau qua mã định danh khoản vay (`LOAN_SEQUENCE_NUMBER`).

### 3.1.2. Mẫu dữ liệu sử dụng

Nghiên cứu sử dụng bộ **Sample** ứng với **năm khởi tạo 2016**, với các đặc điểm đã kiểm tra:

| Đặc điểm | Giá trị |
|---|---|
| Số khoản vay (tệp khởi tạo) | 50.000 |
| Số bản ghi khoản vay–tháng (tệp hiệu suất) | 3.379.650 |
| Kỳ báo cáo | 03/2016 – 03/2026 (khoảng 121 tháng) |
| Tần suất | Theo tháng |
| Định dạng | Văn bản phân cách bằng ký tự `|`, không có dòng tiêu đề |

Phần lớn các khoản vay có kỳ thanh toán đầu tiên trong năm 2016 (41.660 khoản) và năm 2017 (8.331 khoản), số còn lại rải rác ở các năm sau.

**Lý do chọn mẫu.** Khoảng thời gian mười năm của mẫu bao trùm nhiều bối cảnh kinh tế khác biệt: giai đoạn thị trường nhà ở tăng trưởng ổn định (2016–2019), cú sốc đại dịch COVID-19 cùng các chương trình hoãn trả nợ thế chấp (2020–2021), và chu kỳ tăng lãi suất mạnh của Cục Dự trữ Liên bang Hoa Kỳ (2022–2023). Sự đa dạng này là điều kiện thuận lợi để kiểm định tính thuần nhất theo thời gian của ma trận chuyển. Việc chỉ dùng một năm khởi tạo giúp các khoản vay trong mẫu tương đối đồng nhất về tuổi, tránh việc trộn lẫn các khoản vay ở giai đoạn vòng đời rất khác nhau.

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

Quy tắc ánh xạ sang năm trạng thái của mô hình:

| Điều kiện trên dữ liệu gốc | Trạng thái mô hình |
|---|---|
| Delinquency = `00` | 0 — Current |
| Delinquency = `01` | 1 — 30 DPD |
| Delinquency = `02` | 2 — 60 DPD |
| Delinquency $\ge$ `03`, chưa thỏa điều kiện Default | 3 — 90+ DPD |
| **[CẦN CHỐT]** Delinquency = `RA`, hoặc zero-balance $\in$ {`02`, `03`, `09`}, hoặc quá hạn kéo dài vượt ngưỡng (đề xuất: $\ge$ 180 ngày, mã $\ge$ `06`) | 4 — Default/Foreclosure (hấp thụ) |

**[CẦN CHỐT] Khoản vay trả hết nợ trước hạn/đáo hạn (zero-balance `01`).** Như đã chỉ ra ở mục 2.5.5, nếu chỉ có Default là trạng thái hấp thụ thì $B = \mathbf{1}$. Hai phương án:

- *Phương án A — kiểm duyệt (censoring):* quỹ đạo khoản vay kết thúc tại tháng cuối cùng trước khi trả hết nợ; không có lần chuyển nào được ghi nhận vào ma trận đếm sau thời điểm đó. Giữ nguyên năm trạng thái, xác suất vỡ nợ được đánh giá theo kỳ hạn hữu hạn bằng công thức (2.19).
- *Phương án B — thêm trạng thái hấp thụ "Prepaid":* không gian trạng thái có sáu phần tử, $R$ có hai cột, $B$ cho xác suất vỡ nợ trọn đời có ý nghĩa (vỡ nợ trước khi trả hết nợ).

Các khoản vay rời danh mục vì lý do không phải sự kiện tín dụng (mã `15`, `16`, `96`) được xử lý như **kiểm duyệt** trong cả hai phương án.

### 3.2.2. Xây dựng bảng quỹ đạo trạng thái

Từ tệp hiệu suất, dữ liệu được sắp xếp theo `(LOAN_SEQUENCE_NUMBER, MONTHLY_REPORTING_PERIOD)` để thu được bảng quỹ đạo dạng dài với cấu trúc `(loan_id, month, state)`. Các bước xử lý:

1. **Kiểm tra chất lượng:** loại bỏ bản ghi trùng lặp theo cặp (khoản vay, tháng); kiểm tra giá trị thiếu ở trường trạng thái; kiểm tra tính liên tục của chuỗi tháng. Nếu một khoản vay bị gián đoạn tháng báo cáo, quỹ đạo được tách tại điểm gián đoạn để không tạo ra lần chuyển giả qua nhiều tháng.
2. **Cắt quỹ đạo sau hấp thụ:** một khi khoản vay vào trạng thái Default, các bản ghi sau đó (nếu có) bị loại bỏ, đảm bảo đúng tính chất hấp thụ.
3. **Tạo các bảng chuyển trạng thái** phục vụ các phần khác nhau của Chương 4:
   - cặp liên tiếp $(S_t, S_{t+1})$ — ước lượng $\hat{P}$ (mục 4.1) và kiểm định thuần nhất (mục 4.2);
   - bộ ba liên tiếp $(S_{t-1}, S_t, S_{t+1})$ — kiểm định bậc Markov (mục 4.2);
   - cặp cách ba tháng $(S_t, S_{t+3})$ — ước lượng trực tiếp $\hat{P}^{(3)}$ cho kiểm chứng Chapman–Kolmogorov (mục 4.3).

Mỗi lần chuyển được gắn với **tháng xảy ra chuyển** (tháng $t+1$), làm căn cứ chia dữ liệu theo thời gian.

### 3.2.3. Chia dữ liệu theo thời gian

Vì đây là dữ liệu chuỗi thời gian, việc chia ngẫu nhiên sẽ làm rò rỉ thông tin của tương lai vào quá trình ước lượng. Do đó dữ liệu được chia theo một **mốc thời gian** $\tau$:

- **Tập ước lượng (estimation set):** các lần chuyển xảy ra trong khoảng 80% số tháng đầu tiên (dự kiến từ 03/2016 đến khoảng 03/2024). Toàn bộ tham số $\hat{P}$, $\hat{\pi}$, $\hat{N}$, $\hat{B}$ và các kiểm định ở mục 4.1–4.4 chỉ sử dụng tập này.
- **Tập kiểm định (validation set):** khoảng 20% số tháng cuối (dự kiến từ khoảng 04/2024 đến 03/2026, xấp xỉ 24 tháng), chỉ dùng cho backtest ở mục 4.5.

Mốc $\tau$ chính xác được xác định khi chạy pipeline và ghi lại trong Chương 4.

## 3.3. Phương pháp ước lượng và tính toán

Toàn bộ các phép tính của mô hình được **tự cài đặt** bằng Python (thư viện `pandas`, `numpy`, `scipy.stats`), không sử dụng các thư viện mô hình Markov, HMM hay phân tích sống sót có sẵn, nhằm đảm bảo mỗi kết quả đều truy vết được về công thức ở Chương 2.

1. **Ma trận đếm và MLE:** đếm $n_{ij}$ từ bảng cặp chuyển theo (2.7), chuẩn hóa theo hàng để được $\hat{P}$ theo (2.10); gán hàng hấp thụ bằng vectơ đơn vị.
2. **Ma trận chuyển nhiều bước:** tính $\hat{P}^n$ bằng phép nhân ma trận lặp theo (2.12).
3. **Phân phối dừng:** giải hệ tuyến tính (2.14) với điều kiện chuẩn hóa như mô tả ở mục 2.4.3; tính thêm phân phối tựa dừng từ $\hat{Q}$ nếu cần thiết cho diễn giải (mục 2.4.4).
4. **Ma trận cơ bản và xác suất hấp thụ:** tách $\hat{Q}$, $\hat{R}$ theo dạng chuẩn (2.15); thay vì nghịch đảo ma trận trực tiếp, giải hệ tuyến tính $(I - \hat{Q})\hat{B} = \hat{R}$ và $(I - \hat{Q})\hat{\tau} = \mathbf{1}$ để đảm bảo ổn định số; tính $\mathrm{PD}_i(H)$ theo (2.19).

## 3.4. Thiết kế kiểm định và đánh giá mô hình

### 3.4.1. Kiểm định tính thuần nhất theo thời gian

- **Giai đoạn con:** chia tập ước lượng theo **năm dương lịch** của tháng xảy ra chuyển (dự kiến khoảng 8 giai đoạn, 2016–2023). Nếu một năm có quá ít lần chuyển từ các trạng thái quá hạn, các năm liền kề sẽ được gộp lại để đảm bảo số quan sát kỳ vọng trong các ô đủ lớn.
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

1. Tại mốc $\tau$ (đầu giai đoạn kiểm định), xác định trạng thái của mọi khoản vay còn trong danh mục; nhóm các khoản vay theo trạng thái xuất phát $i \in \{0, 1, 2, 3\}$.
2. **Dự báo:** với mỗi $i$, tính xác suất vỡ nợ mô hình dự báo trong kỳ hạn $H$ theo (2.19) (và/hoặc $b_{i,\text{Default}}$ nếu dùng phương án B), sử dụng tham số ước lượng từ tập ước lượng.
3. **Thực tế:** theo dõi các khoản vay trong nhóm $i$ qua $H$ tháng của tập kiểm định, tính tỷ lệ vỡ nợ quan sát được $\widehat{\mathrm{DR}}_i(H)$ = số khoản vay vào Default trong $H$ tháng / số khoản vay trong nhóm. **[CẦN CHỐT]** kỳ hạn $H$ (đề xuất 12 và 24 tháng) và cách xử lý khoản vay rời danh mục trước khi hết $H$ tháng.
4. **Đối chiếu:** so sánh $\mathrm{PD}_i(H)$ với $\widehat{\mathrm{DR}}_i(H)$ cho từng trạng thái xuất phát; kiểm tra xem tỷ lệ thực tế có nằm trong khoảng tin cậy nhị thức xấp xỉ $\mathrm{PD}_i(H) \pm 1{,}96\sqrt{\mathrm{PD}_i(H)(1 - \mathrm{PD}_i(H))/m_i}$ hay không, với $m_i$ là số khoản vay trong nhóm; đánh giá mô hình dự báo cao hay thấp một cách có hệ thống, và liên hệ với kết quả kiểm định thuần nhất ở mục 4.2.

## 3.5. Công cụ thực hiện

- **Ngôn ngữ:** Python 3.11.
- **Thư viện:** `pandas`, `numpy` (xử lý dữ liệu, đại số tuyến tính), `scipy.stats` (phân phối $\chi^2$, p-value), `matplotlib`, `seaborn` (heatmap, biểu đồ).
- **Tổ chức mã nguồn:** pipeline gồm các script đánh số theo thứ tự chạy, các hàm Markov dùng chung (MLE, lũy thừa ma trận, $N$, $B$, phân phối dừng, các thống kê kiểm định) đặt trong một module tiện ích; toàn bộ kết quả của Chương 4 có thể tái lập bằng cách chạy lại pipeline từ dữ liệu gốc.

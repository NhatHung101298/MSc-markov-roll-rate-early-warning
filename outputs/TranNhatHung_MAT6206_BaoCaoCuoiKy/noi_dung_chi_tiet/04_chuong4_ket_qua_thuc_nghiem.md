# CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM

Chương này trình bày kết quả chạy mô hình trên mẫu dữ liệu đã mô tả ở Chương 3. Trừ khi nói rõ khác đi, mọi tham số đều được ước lượng trên tập ước lượng (01/2016 – 02/2024) và tập kiểm định chỉ xuất hiện ở mục 4.5.

## 4.1. Ước lượng ma trận chuyển trạng thái

Tập ước lượng gồm 7.253.423 bản ghi khoản vay–tháng của 150.000 khoản vay. Sau khi ghép các cặp trạng thái liên tiếp trong cùng một đoạn quan sát liền mạch, thu được 7.103.422 lần chuyển hợp lệ; phần chênh lệch khoảng 150 nghìn bản ghi là các tháng cuối cùng của mỗi quỹ đạo, vốn không có tháng kế tiếp để ghép cặp.

Số quan sát ứng với mỗi trạng thái xuất phát được trình bày ở Bảng 4.1. Đại lượng $n_{i\cdot}$ chính là mẫu số trong công thức ước lượng hợp lý cực đại (2.10), nên nó cho biết trực tiếp độ tin cậy của từng hàng trong ma trận chuyển.

**Bảng 4.1.** Số lần chuyển quan sát được theo trạng thái xuất phát

| Trạng thái xuất phát | $n_{i\cdot}$ | Tỷ trọng |
|---|---|---|
| Current | 6.875.554 | 96,79% |
| 30 DPD | 54.505 | 0,77% |
| 60 DPD | 16.903 | 0,24% |
| 90+ DPD | 24.906 | 0,35% |
| Default | 131.554 | 1,85% |
| Prepaid | 0 | 0% |

Hàng Prepaid có $n_{i\cdot} = 0$. Đây không phải lỗi dữ liệu mà là hệ quả trực tiếp của cách Freddie Mac ghi nhận khoản vay: khi khoản vay được trả hết, bản ghi tháng đó là bản ghi cuối cùng và khoản vay không còn xuất hiện trong các tháng sau, nên không tồn tại cặp $(S_t, S_{t+1})$ nào xuất phát từ Prepaid. Hàng này trong $\hat{P}$ vì vậy được gán bằng vectơ đơn vị theo đúng dạng chuẩn của ma trận hấp thụ (2.6), không ước lượng từ dữ liệu. Ngược lại, trạng thái Default vẫn có 131.554 quan sát vì khoản vay chạm ngưỡng quá hạn 180 ngày thường tiếp tục được báo cáo thêm nhiều tháng trước khi hồ sơ được tất toán dứt điểm.

Ma trận chuyển ước lượng được trình bày ở Bảng 4.2 và trực quan hóa ở Hình 4.1.

**Bảng 4.2.** Ma trận chuyển trạng thái ước lượng $\hat{P}$ (theo tháng)

| Trạng thái tháng $t$ (hàng) → tháng $t+1$ (cột) | Current | 30 DPD | 60 DPD | 90+ DPD | Default | Prepaid |
|---|---|---|---|---|---|---|
| Current | 0,9798 | 0,0051 | 0,0000 | 0,0000 | 0,0000 | 0,0150 |
| 30 DPD | 0,4293 | 0,3220 | 0,2289 | 0,0008 | 0,0001 | 0,0190 |
| 60 DPD | 0,1505 | 0,0950 | 0,2266 | 0,5120 | 0,0005 | 0,0154 |
| 90+ DPD | 0,1109 | 0,0128 | 0,0214 | 0,6517 | 0,1888 | 0,0144 |
| Default | 0 | 0 | 0 | 0 | 1 | 0 |
| Prepaid | 0 | 0 | 0 | 0 | 0 | 1 |

![Hình 4.1. Ma trận chuyển trạng thái ước lượng](../../figures/heatmap_P_hat.png)

Ba đặc điểm của ma trận này đáng được chú ý.

Thứ nhất, danh mục rất ổn định ở trạng thái bình thường: xác suất một khoản vay đang trả đúng hạn tiếp tục đúng hạn ở tháng sau là 0,9798, và phần lớn khối lượng rời khỏi Current thực ra không đi vào quá hạn mà đi vào Prepaid (0,0150) — tức khoản vay trả hết nợ chứ không phải suy giảm chất lượng.

Thứ hai, mức độ trượt sang trạng thái xấu hơn tăng mạnh theo mức quá hạn hiện tại. Từ 30 DPD, xác suất trượt xuống 60 DPD là 0,2289; từ 60 DPD, xác suất trượt xuống 90+ DPD đã là 0,5120; và từ 90+ DPD, xác suất ở lại chính trạng thái đó là 0,6517 cùng với 0,1888 rơi thẳng vào Default. Nói cách khác, một khi khoản vay vượt qua mốc 60 ngày quá hạn thì xu hướng chủ đạo không còn là phục hồi mà là tiếp tục xấu đi.

Thứ ba, khả năng phục hồi vẫn tồn tại đáng kể chứ không phải hiện tượng hiếm gặp: từ 30 DPD có tới 0,4293 quay về Current ngay tháng sau, từ 60 DPD có 0,1505 và thậm chí từ 90+ DPD vẫn có 0,1109 quay thẳng về trạng thái trả đúng hạn. Tỷ lệ phục hồi cao như vậy phù hợp với đặc thù của thị trường thế chấp Hoa Kỳ trong giai đoạn khảo sát, khi các chương trình hoãn trả nợ và tái cơ cấu giúp một bộ phận người vay khôi phục được lịch trả nợ sau khi đã quá hạn nặng.

Về độ tin cậy, hai hàng Current và Default có số quan sát rất lớn nên ước lượng ổn định. Hai hàng 60 DPD và 90+ DPD chỉ có lần lượt 16.903 và 24.906 quan sát, nên các ô có xác suất rất nhỏ trong hai hàng này — chẳng hạn xác suất 0,0005 chuyển thẳng từ 60 DPD sang Default — có sai số tương đối lớn và không nên được diễn giải quá chi tiết.

## 4.2. Kết quả kiểm định giả thiết mô hình

Tập ước lượng được chia thành 9 giai đoạn con theo năm dương lịch của tháng xảy ra chuyển, từ 2016 đến 2024. Năm mỏng nhất là 2024 (chỉ tính đến mốc $\tau$) vẫn có 80.133 lần chuyển xuất phát từ bốn trạng thái tạm thời, nên quy tắc gộp giai đoạn dự phòng ở mục 3.4.1 không cần dùng đến.

### 4.2.1. Kiểm định tính thuần nhất theo thời gian

Giả thiết không $H_0$ phát biểu rằng ma trận chuyển là như nhau ở mọi giai đoạn con. Áp dụng kiểm định tỷ số hợp lý theo (2.20)–(2.22) cho toàn bộ 9 giai đoạn, thống kê thu được là 69.101,63 với 160 bậc tự do, tương ứng p-value nhỏ hơn mọi mức ý nghĩa thông dụng. Giả thiết thuần nhất theo thời gian bị **bác bỏ**.

Để xác định khác biệt nằm ở đâu, kiểm định tiếp tục được áp cho từng cặp giai đoạn liền kề, cùng với một phép so sánh gộp giữa giai đoạn trước và từ năm 2020 trở đi. Vì có tất cả 9 phép so sánh, mức ý nghĩa được hiệu chỉnh Bonferroni thành $\alpha = 0{,}05/9 \approx 0{,}0056$.

**Bảng 4.3.** Kiểm định thuần nhất theo từng cặp giai đoạn

| Cặp giai đoạn | Thống kê | Bậc tự do | p-value | Kết luận |
|---|---|---|---|---|
| 2016 – 2017 | 115,66 | 17 | $1{,}03\times10^{-16}$ | Bác bỏ $H_0$ |
| 2017 – 2018 | 211,54 | 19 | $1{,}70\times10^{-34}$ | Bác bỏ $H_0$ |
| 2018 – 2019 | 4.282,29 | 19 | $< 10^{-300}$ | Bác bỏ $H_0$ |
| 2019 – 2020 | 19.344,72 | 20 | $< 10^{-300}$ | Bác bỏ $H_0$ |
| 2020 – 2021 | 2.969,72 | 20 | $< 10^{-300}$ | Bác bỏ $H_0$ |
| 2021 – 2022 | 6.469,45 | 20 | $< 10^{-300}$ | Bác bỏ $H_0$ |
| 2022 – 2023 | 1.348,13 | 20 | $1{,}45\times10^{-273}$ | Bác bỏ $H_0$ |
| 2023 – 2024 | 26,26 | 19 | 0,1232 | Không bác bỏ |
| Trước 2020 – từ 2020 | 35.627,60 | 20 | $< 10^{-300}$ | Bác bỏ $H_0$ |

Tám trên chín phép so sánh đều bác bỏ $H_0$. Điều đáng chú ý hơn con số bác bỏ là **độ lớn** của thống kê giữa các cặp: cặp 2019–2020 có thống kê 19.344,72, gấp khoảng ba lần cặp lớn thứ hai là 2021–2022, trong khi cặp 2023–2024 chỉ có 26,26 và không bác bỏ được $H_0$. Diễn biến này khớp với bối cảnh kinh tế của giai đoạn khảo sát: các chương trình hoãn trả nợ quy mô lớn triển khai từ năm 2020 đã thay đổi hẳn hành vi chuyển trạng thái của người vay — vừa làm tăng số khoản vay rơi vào quá hạn, vừa làm tăng mạnh khả năng phục hồi từ trạng thái quá hạn — và hiệu ứng này giảm dần khi các chương trình hỗ trợ kết thúc, để rồi đến 2023–2024 ma trận chuyển gần như trở lại ổn định.

Cần nói thêm một điểm về cách đọc kết quả. Với cỡ mẫu hàng triệu lần chuyển, kiểm định $\chi^2$ có sức mạnh rất lớn, nên ngay cả những khác biệt nhỏ về mặt thực tiễn cũng đủ để bác bỏ $H_0$ về mặt thống kê. Việc cặp 2016–2017 bị bác bỏ với thống kê 115,66 không có cùng ý nghĩa thực tiễn với việc cặp 2019–2020 bị bác bỏ với thống kê gấp gần 170 lần như vậy. Vì thế, kết luận đúng của mục này không phải là "ma trận chuyển thay đổi hoàn toàn qua mọi năm", mà là giả thiết thuần nhất không đứng vững, và mức độ vi phạm tập trung rõ rệt ở giai đoạn 2019–2022.

### 4.2.2. Kiểm định bậc Markov

Giả thiết không ở đây là xích bậc 1 đủ để mô tả dữ liệu, tức xác suất chuyển sang trạng thái kế tiếp không phụ thuộc vào trạng thái của hai tháng trước. Áp dụng kiểm định tỷ số hợp lý theo (2.23)–(2.24) trên bảng bộ ba trạng thái liên tiếp của tập ước lượng, thống kê thu được là 36.899,997 với 54 bậc tự do, p-value nhỏ hơn mọi mức ý nghĩa thông dụng. Giả thiết bậc 1 bị **bác bỏ**.

Kết quả này nhất quán với sai lệch quan sát được ở mục 4.3 dưới đây. Về mặt trực giác, nó nói rằng hai khoản vay cùng đang ở 60 DPD nhưng có lịch sử khác nhau — một khoản vừa trượt xuống từ 30 DPD, một khoản đang trên đà hồi phục từ 90+ DPD — không có cùng triển vọng ở tháng kế tiếp, trong khi mô hình bậc 1 buộc phải gán cho chúng cùng một phân phối chuyển. Cách diễn giải tương đương và gần với thực tế nghiệp vụ hơn là xác suất chuyển còn phụ thuộc vào **thời gian khoản vay đã nằm trong trạng thái hiện tại**, một yếu tố mà xích Markov bậc 1 theo định nghĩa không thể mang theo.

## 4.3. Kiểm chứng Chapman–Kolmogorov bằng số

Phép kiểm chứng này so sánh hai cách tính cùng một đại lượng: ma trận chuyển ba tháng suy ra từ lũy thừa bậc ba của ma trận tháng, $(\hat{P}^{(1)})^3$, và ma trận chuyển ba tháng ước lượng trực tiếp từ 6.803.851 cặp trạng thái cách nhau đúng ba tháng, $\hat{P}^{(3)}_{\text{trực tiếp}}$. Nếu mô hình Markov thuần nhất bậc 1 đúng, hai ma trận này phải trùng nhau trong phạm vi sai số lấy mẫu.

**Bảng 4.4.** Sai lệch giữa hai cách tính ma trận chuyển ba tháng

| Chỉ số | Giá trị |
|---|---|
| Chuẩn Frobenius $\lVert (\hat{P}^{(1)})^3 - \hat{P}^{(3)}_{\text{trực tiếp}} \rVert_F$ | 0,4220 |
| Sai lệch tuyệt đối lớn nhất trên một ô | 0,1866 |

![Hình 4.2. Chênh lệch từng ô giữa hai cách tính ma trận chuyển ba tháng](../../figures/heatmap_ck_deviation.png)

Để đánh giá con số 0,4220 là lớn hay nhỏ, cần một mốc so sánh. Hai hàng hấp thụ luôn trùng khớp tuyệt đối ở cả hai cách tính, nên toàn bộ sai lệch chỉ đến từ bốn hàng tạm thời. Khoảng cách Euclid tối đa giữa hai phân phối xác suất trên cùng một hàng là $\sqrt{2}$, nên chuẩn Frobenius tối đa về mặt lý thuyết cho bốn hàng là $\sqrt{4 \times 2} \approx 2{,}83$. Sai lệch quan sát được tương đương khoảng 15% mức tối đa đó: không nhỏ đến mức bỏ qua được, nhưng cũng chưa phải mức phá vỡ hoàn toàn cấu trúc mô hình.

Thông tin có giá trị chẩn đoán hơn đến từ việc so sánh với cỡ mẫu. Một phép chạy kiểm tra trước đó trên mẫu con 2.000 khoản vay cho chuẩn Frobenius 0,465. Khi mở rộng lên toàn bộ 150.000 khoản vay, tức cỡ mẫu tăng khoảng 60 lần, sai lệch chỉ giảm xuống 0,4220. Nếu nguồn gốc của sai lệch chỉ là dao động lấy mẫu thì nó phải giảm theo tốc độ $1/\sqrt{n}$ và gần như biến mất ở cỡ mẫu này. Việc nó hầu như đứng yên cho thấy đây là **sai lệch có hệ thống** chứ không phải nhiễu ngẫu nhiên, và nguyên nhân phải nằm ở bản thân giả thiết mô hình. Kiểm định bậc Markov ở mục 4.2.2 đã xác nhận điều đó một cách chính thức.

## 4.4. Phân phối dừng: lý thuyết so với thực nghiệm

Giải hệ $\pi\hat{P} = \pi$ kèm điều kiện chuẩn hóa trên toàn bộ ma trận sáu trạng thái cho nghiệm $\pi = (0;\ 0;\ 0;\ 0;\ 0{,}5;\ 0{,}5)$. Kết quả này đúng như lý thuyết ở mục 2.4.4 đã dự báo: vì xích có hai trạng thái hấp thụ, tập nghiệm của hệ không duy nhất mà là toàn bộ đoạn thẳng nối hai phân phối suy biến tại Default và tại Prepaid; giá trị 50/50 chỉ là một điểm cụ thể mà thuật toán bình phương tối thiểu trả về, không mang ý nghĩa kinh tế nào. Về dài hạn tuyệt đối, mô hình khẳng định mọi khoản vay đều rời khỏi danh mục, điều hiển nhiên đúng nhưng không dùng để đối chiếu với dữ liệu quan sát được.

Phép so sánh có ý nghĩa thực nghiệm vì vậy phải là phân phối trạng thái dự báo sau một số hữu hạn kỳ. Gọi $\mu_\tau$ là phân phối trạng thái thực tế của danh mục tại mốc $\tau$, gồm 42.677 khoản vay còn được theo dõi tại thời điểm đó. Mô hình dự báo phân phối tại tháng $\tau + t$ bằng $\mu_\tau \hat{P}^{t}$, và đại lượng này được đối chiếu với phân phối thực tế của **đúng nhóm 42.677 khoản vay đó** ở từng tháng tiếp theo.

Một chi tiết kỹ thuật cần nói rõ vì nó ảnh hưởng trực tiếp đến tính đúng đắn của phép so sánh. Nếu ở mỗi tháng ta tính tỷ lệ trên số khoản vay còn đang được báo cáo tháng đó, mẫu số sẽ teo dần theo thời gian — sau 25 tháng chỉ còn khoảng 85,7% số khoản vay ban đầu, do khoản vay đã trả hết nợ hoặc đã tất toán hồ sơ vỡ nợ đều ngừng xuất hiện trong dữ liệu. Mẫu số co lại như vậy không khớp với vế dự báo, vốn luôn bảo toàn toàn bộ khối lượng xác suất trên nhóm ban đầu. Để hai vế so sánh được với nhau, trạng thái của khoản vay đã ngừng báo cáo được giữ nguyên bằng trạng thái hấp thụ cuối cùng đã biết, đúng tinh thần quy tắc hấp thụ ở mục 3.2.1, nhờ đó mẫu số cố định ở 42.677 khoản vay trong suốt 25 tháng.

**Bảng 4.5.** Phân phối trạng thái dự báo so với thực tế (đơn vị %)

| $t$ (tháng sau $\tau$) | Current dự báo | Current thực tế | Default dự báo | Default thực tế | Prepaid dự báo | Prepaid thực tế |
|---|---|---|---|---|---|---|
| 1 | 90,43 | 91,31 | 6,43 | 6,43 | 1,89 | 1,01 |
| 5 | 84,82 | 89,02 | 6,64 | 6,51 | 7,29 | 3,28 |
| 10 | 78,31 | 86,15 | 6,95 | 6,60 | 13,58 | 6,02 |
| 15 | 72,30 | 83,83 | 7,24 | 6,69 | 19,38 | 8,40 |
| 20 | 66,75 | 80,91 | 7,51 | 6,77 | 24,74 | 11,28 |
| 25 | 61,62 | 78,48 | 7,77 | 6,85 | 29,69 | 13,61 |

![Hình 4.3. Phân phối trạng thái dự báo so với thực tế theo thời gian](../../figures/forecast_vs_actual_distribution.png)

Kết quả tách thành hai phần rất khác nhau về chất lượng dự báo.

Phần khớp tốt là trạng thái Default và ba trạng thái quá hạn. Tỷ trọng Default dự báo và thực tế trùng nhau gần như tuyệt đối ở tháng đầu tiên (6,43% ở cả hai vế) và chỉ doãng ra rất chậm, đến tháng thứ 25 cũng mới lệch 0,92 điểm phần trăm. Ba trạng thái quá hạn 30, 60 và 90+ DPD, không trình bày trong Bảng 4.5 vì tỷ trọng đều dưới 1%, cũng bám sát thực tế với sai lệch dưới 0,3 điểm phần trăm trong suốt giai đoạn.

Phần lệch lớn nằm ở cặp Current và Prepaid. Đến tháng thứ 25, mô hình dự báo còn 61,62% danh mục ở trạng thái Current trong khi thực tế là 78,48%, đồng thời dự báo 29,69% đã trả hết nợ trong khi thực tế chỉ 13,61%. Hai sai lệch này gần như triệt tiêu nhau về độ lớn (−16,86 và +16,08 điểm phần trăm), cho thấy chúng không phải hai vấn đề độc lập mà là hai mặt của cùng một hiện tượng: mô hình cho rằng khoản vay rời khỏi trạng thái Current để trả hết nợ nhanh hơn thực tế khoảng hai lần, nên phần khối lượng bị rút khỏi Current sớm hơn những gì dữ liệu thực tế cho thấy.

Nguyên nhân của sai lệch này có thể truy về kết quả mục 4.2.1. Ma trận $\hat{P}$ được ước lượng gộp trên toàn giai đoạn 2016–2024, trong đó có hai năm 2020–2021 với mặt bằng lãi suất rất thấp và làn sóng tái cấp vốn mạnh, đẩy xác suất chuyển sang Prepaid trong ma trận trung bình lên cao. Khi đem ma trận đó dự báo cho giai đoạn 2024–2026 với mặt bằng lãi suất cao hơn hẳn, người vay mất phần lớn động lực trả nợ trước hạn, và mô hình đương nhiên dự báo vượt. Nói cách khác, chính sự vi phạm giả thiết thuần nhất đã được kiểm định ở mục 4.2.1 là thứ trực tiếp tạo ra sai lệch quan sát được ở đây.

## 4.5. Ma trận cơ bản, xác suất vỡ nợ và backtest trên tập kiểm định

### 4.5.1. Ma trận cơ bản và xác suất hấp thụ

Tách ma trận $\hat{P}$ theo dạng chuẩn (2.15) và tính $\hat{N} = (I - \hat{Q})^{-1}$, $\hat{B} = \hat{N}\hat{R}$ cho kết quả ở Bảng 4.6. Cột thời gian kỳ vọng là tổng hàng tương ứng của $\hat{N}$, tức số tháng trung bình khoản vay còn nằm trong nhóm các trạng thái tạm thời trước khi bị hấp thụ.

**Bảng 4.6.** Thời gian kỳ vọng đến khi bị hấp thụ và xác suất hấp thụ trọn đời

| Trạng thái xuất phát | Số tháng kỳ vọng đến khi bị hấp thụ | $b_{i,\text{Default}}$ | $b_{i,\text{Prepaid}}$ |
|---|---|---|---|
| Current | 63,39 | 0,0441 | 0,9559 |
| 30 DPD | 54,64 | 0,1704 | 0,8296 |
| 60 DPD | 38,49 | 0,4196 | 0,5804 |
| 90+ DPD | 27,42 | 0,5883 | 0,4117 |

Hai cột xác suất hấp thụ cho thấy rõ giá trị phân biệt rủi ro của mô hình: một khoản vay đang trả đúng hạn chỉ có 4,41% khả năng kết thúc bằng vỡ nợ, trong khi khoản vay đang quá hạn từ 90 ngày trở lên có tới 58,83%, cao hơn mười ba lần. Đây chính là điều mà việc bổ sung trạng thái hấp thụ thứ hai ở mục 2.5.5 nhằm đạt được: nếu chỉ có một trạng thái hấp thụ duy nhất, mọi $b_i$ đều bằng 1 và bảng này sẽ không nói lên điều gì.

Thời gian kỳ vọng đến khi bị hấp thụ giảm đều theo mức độ quá hạn, từ 63,39 tháng với khoản vay đang trả đúng hạn xuống còn 27,42 tháng với khoản vay quá hạn nặng. Cần lưu ý rằng con số này tính chung cho cả hai lối thoát: với khoản vay Current, phần lớn trong 63 tháng đó là quãng thời gian trả nợ bình thường cho tới khi tất toán, chứ không phải thời gian tiến tới vỡ nợ.

Áp dụng công thức kỳ hạn hữu hạn (2.19) với $H = 12$ tháng thu được các xác suất ở Bảng 4.7. Đây là các đại lượng sẽ được đối chiếu với thực tế ở mục tiếp theo.

**Bảng 4.7.** Xác suất bị hấp thụ trong vòng 12 tháng

| Trạng thái xuất phát | $\mathrm{PD}_i(12)$ | Xác suất trả hết nợ trong 12 tháng |
|---|---|---|
| Current | 0,41% | 16,64% |
| 30 DPD | 13,18% | 15,96% |
| 60 DPD | 38,89% | 12,40% |
| 90+ DPD | 56,62% | 9,31% |

### 4.5.2. Đối chiếu với tỷ lệ vỡ nợ thực tế ngoài mẫu

Tại mốc $\tau$, danh mục có 39.741 khoản vay đang ở một trong bốn trạng thái tạm thời. Theo dõi các khoản vay này qua 12 tháng đầu của tập kiểm định và so sánh tỷ lệ thực tế với dự báo cho kết quả ở Bảng 4.8.

**Bảng 4.8.** Xác suất dự báo so với tỷ lệ thực tế quan sát được, kỳ hạn 12 tháng

| Trạng thái xuất phát | $m_i$ | $\mathrm{PD}_i(12)$ dự báo | $\widehat{\mathrm{DR}}_i(12)$ thực tế | Khoảng tin cậy Wilson 95% | Chênh lệch |
|---|---|---|---|---|---|
| Current | 39.195 | 0,41% | 0,09% | [0,06% – 0,12%] | +0,33 đpt |
| 30 DPD | 392 | 13,18% | 3,83% | [2,33% – 6,22%] | +9,35 đpt |
| 60 DPD | 84 | 38,89% | 15,48% | [9,27% – 24,70%] | +23,42 đpt |
| 90+ DPD | 70 | 56,62% | 54,29% | [42,70% – 65,43%] | +2,33 đpt |

**Bảng 4.9.** Xác suất trả hết nợ dự báo so với thực tế, kỳ hạn 12 tháng

| Trạng thái xuất phát | $m_i$ | Dự báo | Thực tế | Khoảng tin cậy Wilson 95% | Chênh lệch |
|---|---|---|---|---|---|
| Current | 39.195 | 16,64% | 6,84% | [6,59% – 7,09%] | +9,81 đpt |
| 30 DPD | 392 | 15,96% | 9,69% | [7,14% – 13,03%] | +6,26 đpt |
| 60 DPD | 84 | 12,40% | 7,14% | [3,31% – 14,72%] | +5,26 đpt |
| 90+ DPD | 70 | 9,31% | 0,00% | [0% – 5,20%] | +9,31 đpt |

![Hình 4.4. Xác suất dự báo so với tỷ lệ thực tế theo trạng thái xuất phát](../../figures/backtest_4_5.png)

Về xác suất vỡ nợ, mô hình dự báo cao hơn thực tế ở cả bốn trạng thái xuất phát, nhưng mức độ chênh lệch không tăng đơn điệu theo mức quá hạn. Sai lệch lớn nhất rơi vào trạng thái 60 DPD, nơi mô hình dự báo 38,89% trong khi thực tế chỉ 15,48%, tức cao hơn khoảng hai lần rưỡi. Ở ba trạng thái Current, 30 DPD và 60 DPD, giá trị dự báo đều nằm ngoài khoảng tin cậy của tỷ lệ thực tế, nghĩa là chênh lệch không thể quy cho dao động lấy mẫu.

Trường hợp 90+ DPD khác hẳn: dự báo 56,62% nằm gọn trong khoảng tin cậy [42,70%; 65,43%] của tỷ lệ thực tế 54,29%, tức mô hình và dữ liệu không phân biệt được với nhau về mặt thống kê. Đây là kết quả có ý nghĩa thực tiễn đáng kể, bởi 90+ DPD chính là nhóm mà một hệ thống cảnh báo sớm cần dự báo chính xác nhất. Tuy vậy cần trung thực rằng nhóm này chỉ có 70 khoản vay nên khoảng tin cậy rộng tới hơn 22 điểm phần trăm; kết luận "không phân biệt được" vì thế phản ánh cả độ chính xác của mô hình lẫn sự hạn chế của cỡ mẫu.

Về xác suất trả hết nợ, mô hình dự báo vượt thực tế ở toàn bộ bốn trạng thái, lặp lại đúng hiện tượng đã thấy ở mục 4.4. Trường hợp cực đoan nhất là nhóm 90+ DPD: mô hình dự báo 9,31% số khoản vay sẽ trả hết nợ trong 12 tháng, trong khi thực tế không có khoản nào trong 70 khoản làm được điều đó. Kết quả này hợp lý về mặt kinh tế — một khoản vay đã quá hạn từ 90 ngày trở lên gần như không còn khả năng tái cấp vốn hay bán tài sản để tất toán bình thường — và nó cũng cho thấy hạn chế của việc áp một ma trận chuyển chung cho mọi trạng thái: tham số trả trước hạn học được chủ yếu từ nhóm khoản vay tốt đã bị áp sang cả nhóm khoản vay xấu.

Tổng hợp lại, mô hình có xu hướng **phóng đại rủi ro một cách có hệ thống** trên phần lớn danh mục, ở cả hai chiều vỡ nợ và trả trước hạn. Xu hướng này nhất quán với kết luận ở mục 4.2.1: ma trận $\hat{P}$ ước lượng trên toàn giai đoạn 2016–2024 mang trong nó dấu vết của thời kỳ bất thường 2020–2022 và vì vậy không đại diện tốt cho hành vi danh mục ngay sau mốc $\tau$. Điều đáng ghi nhận là sai lệch này không đồng đều: đúng ở nhóm khoản vay rủi ro cao nhất, nơi quyết định quản trị cần thông tin chính xác nhất, dự báo của mô hình lại sát thực tế nhất.

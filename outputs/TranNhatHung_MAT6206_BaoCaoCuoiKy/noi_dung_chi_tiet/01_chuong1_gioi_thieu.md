# CHƯƠNG 1: GIỚI THIỆU

## 1.1. Đặt vấn đề

Rủi ro tín dụng — khả năng bên vay không thực hiện đầy đủ nghĩa vụ trả nợ — là loại rủi ro lớn nhất trong hoạt động của các tổ chức cho vay. Cuộc khủng hoảng tài chính toàn cầu 2007–2008, khởi phát từ thị trường cho vay thế chấp nhà ở tại Hoa Kỳ, cho thấy việc đánh giá thấp tốc độ suy giảm chất lượng của một danh mục cho vay có thể gây ra hậu quả mang tính hệ thống. Sau khủng hoảng, các chuẩn mực quản trị rủi ro và kế toán như Basel II/III (phương pháp tiếp cận dựa trên xếp hạng nội bộ — IRB) và IFRS 9 (mô hình tổn thất tín dụng kỳ vọng — ECL) đều yêu cầu tổ chức tín dụng phải ước lượng **xác suất vỡ nợ (Probability of Default — PD)** một cách có cơ sở, mang tính hướng về tương lai, và theo dõi được sự suy giảm tín dụng của từng khoản vay theo thời gian.

Trong thực hành giám sát danh mục, một chỉ báo quen thuộc là **tỷ lệ nợ quá hạn tại một thời điểm** (ví dụ tỷ lệ dư nợ quá hạn trên 90 ngày). Tuy nhiên, chỉ báo tĩnh này có hai nhược điểm cơ bản. Thứ nhất, nó chỉ phản ánh "ảnh chụp" của danh mục tại một ngày báo cáo mà không cho biết các khoản vay đang **di chuyển** như thế nào giữa các mức quá hạn. Thứ hai, nó là chỉ báo **trễ**: khi một khoản vay đã được ghi nhận là nợ xấu thì cơ hội can thiệp sớm (nhắc nợ, tái cơ cấu, trích lập dự phòng kịp thời) đã phần lớn bị bỏ lỡ.

Để khắc phục, ngành ngân hàng từ lâu đã sử dụng **ma trận tỷ lệ chuyển (roll-rate matrix)**: một bảng cho biết trong số các khoản vay đang ở một mức quá hạn nhất định (ví dụ quá hạn 30 ngày) tại tháng này, bao nhiêu phần trăm sẽ "trôi" sang mức quá hạn nặng hơn, bao nhiêu phần trăm giữ nguyên, và bao nhiêu phần trăm "phục hồi" về trạng thái trả nợ đúng hạn vào tháng sau. Nhìn từ góc độ xác suất, ma trận roll-rate chính là **ma trận chuyển của một xích Markov** trên không gian các trạng thái quá hạn. Cách nhìn này mang lại hai lợi ích quan trọng:

- Nó cho phép sử dụng toàn bộ bộ máy lý thuyết của xích Markov — phương trình Chapman–Kolmogorov, phân phối dừng, lý thuyết xích hấp thụ — để **suy ra các đại lượng có ý nghĩa quản trị rủi ro** từ một ma trận chuyển một bước, chẳng hạn xác suất một khoản vay đang quá hạn 60 ngày cuối cùng sẽ vỡ nợ, hay số tháng kỳ vọng trước khi vỡ nợ.
- Nó buộc người xây dựng mô hình phải **phát biểu tường minh các giả thiết** — tính Markov (tương lai chỉ phụ thuộc trạng thái hiện tại) và tính thuần nhất theo thời gian (xác suất chuyển không đổi qua các giai đoạn) — và do đó các giả thiết này có thể được **kiểm định thống kê** thay vì được chấp nhận một cách mặc nhiên.

Chính điểm thứ hai là khoảng trống thường gặp trong thực hành: ma trận roll-rate thường được ước lượng như một bảng tần suất rồi dùng trực tiếp để dự báo, trong khi hiếm khi có câu hỏi liệu ma trận của năm 2019 có giống ma trận của năm 2021 hay không, hay liệu lịch sử quá hạn của tháng trước nữa có mang thêm thông tin dự báo hay không. Báo cáo này đặt trọng tâm vào việc trả lời các câu hỏi đó trên dữ liệu thực tế.

## 1.2. Lý do chọn đề tài và dữ liệu

**Về đề tài.** Việc lựa chọn đề tài xuất phát từ hai lý do. Một là tính gắn kết chặt chẽ với nội dung môn học Các phương pháp ngẫu nhiên và ứng dụng: bài toán roll-rate sử dụng gần như trọn vẹn các kết quả cốt lõi của lý thuyết xích Markov rời rạc thời gian với không gian trạng thái hữu hạn, đồng thời đòi hỏi các công cụ kiểm định của thống kê suy diễn (kiểm định $\chi^2$, kiểm định tỷ số hợp lý). Hai là tính ứng dụng trực tiếp trong lĩnh vực mô hình hóa rủi ro tín dụng (IFRS 9, IRB), nơi ma trận chuyển trạng thái là công cụ phổ biến để ước lượng cấu trúc kỳ hạn của PD và để phân loại giai đoạn suy giảm tín dụng. Đề tài vì vậy là cơ hội để hình thức hóa lại một công cụ nghiệp vụ quen thuộc trên nền tảng xác suất chặt chẽ.

**Về dữ liệu.** Nghiên cứu sử dụng **Freddie Mac Single-Family Loan-Level Dataset** — bộ dữ liệu công khai cấp độ khoản vay do Freddie Mac (Federal Home Loan Mortgage Corporation), một trong hai doanh nghiệp được Chính phủ Hoa Kỳ bảo trợ trên thị trường thế chấp thứ cấp, công bố. Bộ dữ liệu này phù hợp với mục tiêu nghiên cứu vì các lý do sau:

- **Ghi nhận trạng thái quá hạn theo tháng của từng khoản vay** trong suốt vòng đời khoản vay, là dạng dữ liệu quỹ đạo (trajectory) mà mô hình xích Markov đòi hỏi.
- **Độ dài quan sát lớn**: mẫu được sử dụng (ba năm khởi tạo 2016, 2017, 2018) được theo dõi đến tháng 03/2026 (khoảng 123 kỳ báo cáo cho vintage 2016), trải qua nhiều bối cảnh kinh tế khác nhau — giai đoạn tăng trưởng ổn định trước 2020, cú sốc COVID-19 cùng các chương trình hoãn trả nợ (2020–2021), và chu kỳ tăng lãi suất (2022–2023). Đây là điều kiện lý tưởng để kiểm định tính thuần nhất theo thời gian của ma trận chuyển.
- **Tính công khai và minh bạch**: dữ liệu có tài liệu mô tả trường dữ liệu chính thức, cho phép tái lập toàn bộ kết quả của báo cáo.
- **Quy mô đủ lớn cho các kiểm định của Chương 4**: thiết kế ban đầu chỉ dùng một năm khởi tạo (2016, 50.000 khoản vay), nhưng với định nghĩa vỡ nợ được chọn ở mục 3.2.1 thì mẫu này chỉ cho khoảng 1.376 sự kiện, và khi chia tiếp theo bốn trạng thái xuất phát thì mỗi nhóm chỉ còn vài chục quan sát — không đủ để các kiểm định và bước đối chiếu ngoài mẫu có sức thuyết phục. Mẫu cuối cùng gộp ba năm khởi tạo độc lập (2016, 2017, 2018), tổng 150.000 khoản vay với khoảng 8,24 triệu bản ghi khoản vay–tháng, cho 4.921 sự kiện vỡ nợ mà vẫn xử lý được trên máy tính cá nhân. Cái giá của việc trộn nhiều năm khởi tạo được thảo luận ở mục 3.1.2 và phần Kết luận.

## 1.3. Mục tiêu nghiên cứu

Mục tiêu tổng quát của báo cáo là xây dựng, kiểm định và đánh giá khả năng dự báo của một mô hình xích Markov rời rạc thời gian cho quá trình chuyển trạng thái quá hạn của khoản vay thế chấp. Cụ thể, báo cáo hướng đến năm mục tiêu:

1. **Ước lượng ma trận chuyển trạng thái** một bước (theo tháng) bằng phương pháp hợp lý cực đại từ dữ liệu quỹ đạo khoản vay.
2. **Kiểm định các giả thiết nền tảng của mô hình**: (i) tính thuần nhất theo thời gian của ma trận chuyển giữa các giai đoạn con, và (ii) bậc của xích Markov (bậc 1 so với bậc 2).
3. **Kiểm chứng phương trình Chapman–Kolmogorov bằng số liệu**: so sánh ma trận chuyển ba tháng suy ra từ lũy thừa ma trận tháng với ma trận chuyển ba tháng ước lượng trực tiếp.
4. **Tính phân phối dừng** của xích Markov ước lượng được, và đối chiếu phân phối trạng thái mà mô hình dự báo sau một số hữu hạn tháng với phân phối quan sát thực tế.
5. **Tính ma trận cơ bản và xác suất hấp thụ** (xác suất vỡ nợ) theo từng trạng thái xuất phát, và **đối chiếu dự báo này với tỷ lệ vỡ nợ thực tế trên tập dữ liệu kiểm định ngoài mẫu** (backtest).

Tương ứng, báo cáo tìm cách trả lời các câu hỏi nghiên cứu:

- Ma trận chuyển trạng thái quá hạn của khoản vay thế chấp có ổn định theo thời gian hay không?
- Giả thiết Markov bậc 1 có đủ để mô tả quá trình chuyển trạng thái hay không?
- Xác suất vỡ nợ mà mô hình dự báo có phù hợp với tỷ lệ vỡ nợ thực tế quan sát được trong giai đoạn kiểm định hay không?

## 1.4. Đối tượng và phạm vi nghiên cứu

### 1.4.1. Đối tượng nghiên cứu

- **Đối tượng dữ liệu:** quỹ đạo trạng thái quá hạn theo tháng của các khoản vay thế chấp nhà ở cho một gia đình (single-family mortgage) có lãi suất cố định, thuộc bộ Freddie Mac Single-Family Loan-Level Dataset, mẫu Sample các năm khởi tạo 2016, 2017, 2018.
- **Đối tượng phương pháp:** xích Markov rời rạc thời gian với không gian trạng thái hữu hạn, lý thuyết xích Markov hấp thụ, ước lượng hợp lý cực đại và các kiểm định giả thiết cho xích Markov (kiểm định $\chi^2$ về tính thuần nhất, kiểm định tỷ số hợp lý về bậc).

### 1.4.2. Phạm vi nghiên cứu

**Phạm vi về dữ liệu:**

- Dữ liệu là bộ Sample của Freddie Mac cho ba năm khởi tạo 2016, 2017, 2018 (gộp), tổng 150.000 khoản vay, kỳ báo cáo đến 03/2026, tần suất theo tháng.
- Trạng thái của khoản vay được rời rạc hóa thành sáu trạng thái: bốn trạng thái tạm thời — Trả nợ đúng hạn (Current), Quá hạn 30 ngày (30 DPD), Quá hạn 60 ngày (60 DPD), Quá hạn từ 90 ngày trở lên (90+ DPD) — và hai trạng thái hấp thụ — Vỡ nợ/Tịch biên (Default/Foreclosure) và Trả hết nợ trước hạn/đáo hạn (Prepaid). Việc bổ sung Prepaid làm trạng thái hấp thụ thứ hai (thay vì chỉ có Default) là cần thiết để xác suất hấp thụ $B$ mang ý nghĩa phân biệt rủi ro giữa các khoản vay, thay vì luôn bằng 1 (xem mục 2.5.5).
- Dữ liệu được chia **theo trục thời gian** (không chia ngẫu nhiên): khoảng 80% giai đoạn đầu dùng để ước lượng tham số, khoảng 20% giai đoạn cuối dùng để kiểm định ngoài mẫu.

**Phạm vi về nội dung và phương pháp:**

- Nghiên cứu chỉ sử dụng **xích Markov quan sát được**, tức trạng thái của khoản vay tại mỗi tháng được quan sát trực tiếp từ dữ liệu. Đây là một **lựa chọn chủ động** nhằm tập trung vào các kết quả cốt lõi của môn học và đảm bảo tính minh bạch của mọi phép tính (toàn bộ công thức được tự cài đặt, không dùng thư viện mô hình có sẵn).
- Nghiên cứu **không** sử dụng mô hình Markov ẩn (HMM), mô hình sống sót (mô hình rủi ro tỷ lệ Cox, mô hình hazard rời rạc), mô hình semi-Markov hay các mô hình học máy; **không** xây dựng ma trận chuyển riêng cho từng phân khúc khách hàng.
- Mô hình giả định xác suất chuyển trạng thái chỉ phụ thuộc vào trạng thái quá hạn, không phụ thuộc vào đặc điểm khoản vay (điểm tín dụng, tỷ lệ khoản vay trên giá trị tài sản, …) hay các biến kinh tế vĩ mô. Các yếu tố này được coi là hướng mở rộng và được thảo luận ở phần Kết luận.

## 1.5. Cấu trúc báo cáo

Ngoài phần Giới thiệu, báo cáo gồm các phần sau:

- **Chương 2 — Cơ sở lý thuyết:** trình bày xích Markov rời rạc thời gian, ước lượng hợp lý cực đại cho ma trận chuyển, phương trình Chapman–Kolmogorov, phân phối dừng, lý thuyết xích Markov hấp thụ và các kiểm định giả thiết cho xích Markov.
- **Chương 3 — Dữ liệu và phương pháp:** mô tả dữ liệu, quy trình tiền xử lý, cách chia tập ước lượng/kiểm định, và thiết kế chi tiết các kiểm định, phép kiểm chứng cùng quy trình backtest.
- **Chương 4 — Kết quả thực nghiệm:** trình bày và diễn giải kết quả ước lượng, kết quả kiểm định, kiểm chứng Chapman–Kolmogorov, phân phối dừng và backtest xác suất vỡ nợ.
- **Kết luận:** tóm tắt kết quả, nêu hạn chế và hướng phát triển.

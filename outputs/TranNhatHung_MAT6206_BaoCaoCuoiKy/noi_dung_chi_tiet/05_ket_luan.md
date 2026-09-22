# KẾT LUẬN

## Tóm tắt kết quả

> **[TODO — cần kết quả Chương 4]** Tóm tắt: (i) mức độ phù hợp của giả thiết thuần nhất và giả thiết Markov bậc 1 (mục 4.2); (ii) kết quả kiểm chứng Chapman–Kolmogorov (mục 4.3); (iii) kết quả backtest xác suất vỡ nợ (mục 4.5); (iv) kết luận chung về giá trị của mô hình roll-rate Markov cho cảnh báo sớm.

## Hạn chế

Bên cạnh các kết quả đạt được, mô hình trong báo cáo có một số hạn chế cần được nhận thức rõ khi áp dụng:

- **Không phân biệt đặc điểm khoản vay.** Mô hình giả định mọi khoản vay ở cùng một trạng thái quá hạn có cùng xác suất chuyển, bất kể điểm tín dụng, tỷ lệ khoản vay trên giá trị tài sản, lãi suất hay khu vực địa lý. Trong thực tế, hai khoản vay cùng quá hạn 30 ngày nhưng có hồ sơ tín dụng khác nhau có thể có khả năng phục hồi rất khác nhau; ma trận gộp vì vậy phản ánh hành vi "trung bình" của danh mục và có thể không phù hợp khi cơ cấu danh mục thay đổi.
- **Không đưa biến kinh tế vĩ mô vào mô hình.** Xác suất chuyển trạng thái chịu ảnh hưởng mạnh của điều kiện kinh tế (thất nghiệp, lãi suất, giá nhà) và các chính sách hỗ trợ (như chương trình hoãn trả nợ giai đoạn COVID-19). Một ma trận chuyển cố định không thể phản ánh những thay đổi này; kết quả kiểm định thuần nhất theo thời gian cho biết mức độ nghiêm trọng của hạn chế này trên dữ liệu.
- **Giả thiết Markov bậc 1.** Mô hình bỏ qua thông tin về lịch sử quá hạn trước tháng hiện tại và thời gian khoản vay đã lưu lại ở trạng thái hiện tại. Nếu kiểm định bậc Markov bác bỏ giả thiết bậc 1, đây là một nguồn sai lệch dự báo cần tính đến.
- **Giả định độc lập giữa các khoản vay.** Các kiểm định và khoảng tin cậy dựa trên giả định các khoản vay độc lập, trong khi thực tế chúng cùng chịu các cú sốc chung, khiến độ bất định thực sự có thể lớn hơn mức mà mô hình phản ánh.
- **Trộn nhiều năm khởi tạo (vintage) không đồng nhất về tuổi khoản vay.** Mẫu ước lượng gộp ba năm khởi tạo 2016, 2017, 2018 (150.000 khoản vay) để có đủ số sự kiện vỡ nợ cho các kiểm định và backtest (mục 3.1.2). Tại cùng một thời điểm lịch, vintage 2016 đã "già" hơn vintage 2018 hai năm, trong khi mô hình giả định xác suất chuyển chỉ phụ thuộc trạng thái hiện tại, không phụ thuộc vintage hay tuổi khoản vay (seasoning). Nếu tồn tại hiệu ứng seasoning thực sự, nó không được mô hình bắt được và có thể là một phần nguyên nhân nếu kiểm định thuần nhất theo thời gian (mục 4.2) bác bỏ $H_0$.
- **Phạm vi dữ liệu.** Nghiên cứu chỉ sử dụng bộ **Sample** (không phải Standard/full) của một tổ chức (Freddie Mac) cho một loại sản phẩm (vay thế chấp lãi suất cố định), ba năm khởi tạo 2016–2018; kết quả chưa chắc khái quát được cho các loại khoản vay, tổ chức phát hành, hoặc thị trường khác.
- **Phạm vi phương pháp được giới hạn chủ động.** Báo cáo không so sánh với các mô hình phức tạp hơn (mô hình Markov ẩn, mô hình sống sót, mô hình học máy); do đó không khẳng định mô hình xích Markov là lựa chọn tốt nhất cho bài toán, mà chỉ đánh giá mức độ phù hợp của nó.

## Hướng phát triển

Các hướng sau được đề xuất cho nghiên cứu tiếp theo (không triển khai trong phạm vi báo cáo):

- **Mô hình semi-Markov hoặc Markov không thuần nhất có biến vĩ mô:** cho phép xác suất chuyển phụ thuộc vào thời gian lưu lại tại trạng thái, hoặc biến thiên theo các chỉ số kinh tế vĩ mô qua từng giai đoạn — phù hợp với yêu cầu ước lượng mang tính hướng về tương lai của IFRS 9.
- **Ma trận chuyển theo phân khúc khách hàng:** ước lượng riêng cho các nhóm điểm tín dụng, tỷ lệ khoản vay trên giá trị tài sản hoặc khu vực địa lý, qua đó khắc phục hạn chế về tính đồng nhất của danh mục.
- **Định lượng độ bất định của ước lượng:** xây dựng khoảng tin cậy cho phân phối dừng và ma trận xác suất hấp thụ, chẳng hạn bằng phương pháp bootstrap theo khoản vay, để đánh giá độ tin cậy của các dự báo xác suất vỡ nợ.
- **Mở rộng dữ liệu:** dùng bộ Standard (full) thay vì Sample, hoặc thêm các năm khởi tạo khác ngoài 2016–2018, để tăng số sự kiện vỡ nợ và kiểm tra độ ổn định của ma trận chuyển giữa nhiều thế hệ khoản vay hơn; đồng thời có thể mô hình hóa tường minh hiệu ứng vintage/seasoning (hạn chế nêu ở mục "Hạn chế") thay vì gộp trực tiếp như báo cáo hiện tại.

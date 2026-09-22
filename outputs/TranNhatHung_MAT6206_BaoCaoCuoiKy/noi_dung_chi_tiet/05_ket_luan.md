# KẾT LUẬN

## Tóm tắt kết quả

Báo cáo đã xây dựng một mô hình xích Markov rời rạc thời gian sáu trạng thái cho quá trình chuyển trạng thái quá hạn của khoản vay thế chấp, ước lượng trên 150.000 khoản vay thuộc ba năm khởi tạo 2016–2018 của bộ dữ liệu Freddie Mac, và kiểm định mô hình đó trên dữ liệu ngoài mẫu. Năm kết quả chính có thể tóm lại như sau.

Thứ nhất, ma trận chuyển ước lượng được mô tả hợp lý cấu trúc rủi ro của danh mục. Xác suất một khoản vay đang trả đúng hạn tiếp tục đúng hạn ở tháng sau là 0,9798; xác suất trượt xấu tăng nhanh theo mức quá hạn, lên tới 0,5120 từ 60 DPD sang 90+ DPD; đồng thời khả năng phục hồi vẫn tồn tại đáng kể ở mọi mức quá hạn. Xác suất vỡ nợ trọn đời tính từ ma trận cơ bản phân biệt rõ ràng giữa các nhóm rủi ro, từ 4,41% với khoản vay đang trả đúng hạn đến 58,83% với khoản vay quá hạn từ 90 ngày.

Thứ hai, cả hai giả thiết nền tảng của mô hình đều bị bác bỏ trên dữ liệu thực tế. Kiểm định tính thuần nhất theo thời gian cho thống kê 69.101,63 với 160 bậc tự do, và kiểm định bậc Markov cho thống kê 36.899,997 với 54 bậc tự do; cả hai đều có p-value nhỏ hơn mọi mức ý nghĩa thông dụng. Mức độ vi phạm tính thuần nhất tập trung rõ rệt vào giai đoạn 2019–2022, trùng với thời kỳ các chương trình hoãn trả nợ qui mô lớn được triển khai.

Thứ ba, kiểm chứng Chapman–Kolmogorov bằng số cho sai lệch 0,4220 theo chuẩn Frobenius giữa ma trận ba tháng suy ra từ lũy thừa và ma trận ba tháng ước lượng trực tiếp. Điều đáng chú ý là sai lệch này gần như không giảm khi cỡ mẫu tăng khoảng 60 lần, qua đó khẳng định một cách độc lập rằng nguồn gốc của nó là sai lệch hệ thống chứ không phải dao động lấy mẫu — nhất quán với kết quả kiểm định bậc Markov.

Thứ tư, khi đối chiếu phân phối trạng thái dự báo với phân phối thực tế trong 25 tháng ngoài mẫu, mô hình dự báo tốt tỷ trọng vỡ nợ và các trạng thái quá hạn (sai lệch dưới một điểm phần trăm trong suốt giai đoạn), nhưng dự báo tốc độ trả hết nợ trước hạn cao hơn thực tế khoảng hai lần (29,69% so với 13,61% ở tháng thứ 25). Sai lệch này truy nguyên được về chính việc giả thiết thuần nhất bị vi phạm: ma trận ước lượng mang dấu vết của thời kỳ lãi suất thấp 2020–2021 nhưng lại được dùng để dự báo cho giai đoạn lãi suất cao hơn.

Thứ năm, ở bước backtest xác suất vỡ nợ theo từng trạng thái xuất phát, mô hình dự báo cao hơn thực tế ở cả bốn nhóm, với sai lệch lớn nhất ở nhóm 60 DPD (38,89% so với 15,48%). Riêng nhóm 90+ DPD, dự báo 56,62% nằm trong khoảng tin cậy 95% của tỷ lệ thực tế 54,29%, tức không phân biệt được về mặt thống kê, dù cần lưu ý rằng nhóm này chỉ có 70 khoản vay.

Đánh giá chung, xích Markov roll-rate là một công cụ minh bạch và dễ diễn giải, cho phép suy ra những đại lượng quản trị rủi ro có ý nghĩa — xác suất vỡ nợ trọn đời, xác suất vỡ nợ theo kỳ hạn, thời gian kỳ vọng đến khi khoản vay rời danh mục — chỉ từ một ma trận chuyển một bước. Nhưng các giả thiết đơn giản hóa của nó không đứng vững trên dữ liệu thực, và hệ quả của việc đó đo lường được: mô hình phóng đại rủi ro một cách có hệ thống trên phần lớn danh mục. Điểm tích cực đáng ghi nhận là sai lệch không đồng đều, và đúng ở nhóm khoản vay rủi ro cao nhất — nhóm mà một hệ thống cảnh báo sớm quan tâm nhất — dự báo của mô hình lại sát thực tế nhất. Kết luận thực dụng rút ra là mô hình này dùng được cho mục đích xếp hạng và cảnh báo tương đối giữa các nhóm khoản vay, nhưng cần thận trọng nếu dùng trực tiếp các con số xác suất tuyệt đối cho mục đích trích lập hay định giá.

## Hạn chế

Bên cạnh các kết quả đạt được, mô hình trong báo cáo có một số hạn chế cần được nhận thức rõ khi áp dụng.

**Không phân biệt đặc điểm khoản vay.** Mô hình giả định mọi khoản vay ở cùng một trạng thái quá hạn có cùng xác suất chuyển, bất kể điểm tín dụng, tỷ lệ khoản vay trên giá trị tài sản, lãi suất hay khu vực địa lý. Trong thực tế, hai khoản vay cùng quá hạn 30 ngày nhưng có hồ sơ tín dụng khác nhau có thể có khả năng phục hồi rất khác nhau; ma trận gộp vì vậy phản ánh hành vi trung bình của danh mục và có thể không phù hợp khi cơ cấu danh mục thay đổi.

**Không đưa biến kinh tế vĩ mô vào mô hình.** Xác suất chuyển trạng thái chịu ảnh hưởng mạnh của điều kiện kinh tế và của các chính sách hỗ trợ người vay, nhưng một ma trận chuyển cố định không thể phản ánh những thay đổi đó. Kết quả kiểm định ở mục 4.2.1 cho thấy hạn chế này là có thật chứ không phải nguy cơ lý thuyết: giả thiết thuần nhất bị bác bỏ, và mức độ khác biệt lớn nhất rơi đúng vào cặp 2019–2020 với thống kê 19.344,72, gấp khoảng ba lần cặp lớn thứ hai.

**Giả thiết Markov bậc 1.** Mô hình bỏ qua lịch sử quá hạn trước tháng hiện tại và thời gian khoản vay đã nằm trong trạng thái hiện tại. Kiểm định ở mục 4.2.2 bác bỏ giả thiết này, và sai lệch Chapman–Kolmogorov ở mục 4.3 xác nhận cùng một kết luận từ một hướng độc lập. Báo cáo không chuyển sang mô hình bậc cao hơn vì điều đó nằm ngoài phạm vi đã xác định ở mục 1.4.2, mà ghi nhận đây là một nguồn sai lệch dự báo đã được kiểm định chứ không phải một giả thiết được chấp nhận mặc nhiên.

**Phóng đại tốc độ trả hết nợ trước hạn.** Kết quả ở mục 4.4 và 4.5 cho thấy mô hình dự báo tốc độ trả trước hạn cao hơn thực tế khoảng hai lần ở cấp độ danh mục, và cao hơn thực tế ở cả bốn trạng thái xuất phát trong backtest. Nguyên nhân là ma trận chuyển được ước lượng gộp cả giai đoạn lãi suất thấp 2020–2021 với làn sóng tái cấp vốn mạnh, không đại diện cho môi trường lãi suất của giai đoạn kiểm định. Hạn chế này ảnh hưởng chủ yếu tới nhánh kết cục cạnh tranh Prepaid; dự báo xác suất vỡ nợ ở nhóm quá hạn nặng vẫn giữ được độ chính xác chấp nhận được.

**Cỡ mẫu mỏng ở các trạng thái quá hạn.** Tại mốc chia tập, nhóm 60 DPD chỉ có 84 khoản vay và nhóm 90+ DPD chỉ có 70 khoản vay. Khoảng tin cậy của tỷ lệ vỡ nợ thực tế ở hai nhóm này vì vậy rất rộng, khiến kết luận "dự báo phù hợp với thực tế" ở nhóm 90+ DPD phản ánh cả độ chính xác của mô hình lẫn giới hạn về độ phân giải thống kê của dữ liệu.

**Giả định độc lập giữa các khoản vay.** Các kiểm định và khoảng tin cậy trong báo cáo đều dựa trên giả định các khoản vay độc lập với nhau, trong khi thực tế chúng cùng chịu các cú sốc chung về kinh tế và chính sách. Độ bất định thực sự của các ước lượng vì vậy có thể lớn hơn mức mà báo cáo phản ánh.

**Trộn nhiều năm khởi tạo không đồng nhất về tuổi khoản vay.** Mẫu ước lượng gộp ba vintage 2016, 2017 và 2018 để có đủ số sự kiện vỡ nợ. Tại cùng một tháng báo cáo, khoản vay vintage 2016 đã già hơn khoản vay vintage 2018 hai năm, trong khi mô hình giả định xác suất chuyển không phụ thuộc tuổi khoản vay. Nếu tồn tại hiệu ứng seasoning thực sự thì nó không được mô hình nắm bắt, và đây có thể là một phần nguyên nhân khiến giả thiết thuần nhất bị bác bỏ.

**Phạm vi dữ liệu và phương pháp.** Nghiên cứu chỉ sử dụng bộ Sample của một tổ chức, cho một loại sản phẩm là vay thế chấp lãi suất cố định, trong ba năm khởi tạo; kết quả chưa chắc khái quát được cho loại khoản vay, tổ chức phát hành hay thị trường khác. Báo cáo cũng không so sánh với các mô hình phức tạp hơn, nên không khẳng định xích Markov là lựa chọn tốt nhất cho bài toán mà chỉ đánh giá mức độ phù hợp của nó.

## Hướng phát triển

Các hướng sau được đề xuất cho nghiên cứu tiếp theo, không triển khai trong phạm vi báo cáo này.

**Nới lỏng giả thiết thuần nhất theo thời gian.** Cách đơn giản nhất và gần nhất với kết quả đã có là ước lượng ma trận chuyển trên một cửa sổ thời gian trượt gần thời điểm dự báo, thay vì gộp toàn bộ lịch sử. Hướng bài bản hơn là mô hình Markov không thuần nhất có tham số phụ thuộc biến vĩ mô như lãi suất, tỷ lệ thất nghiệp hay chỉ số giá nhà, phù hợp với yêu cầu ước lượng hướng về tương lai của IFRS 9.

**Nới lỏng giả thiết bậc 1.** Kết quả kiểm định bậc Markov gợi ý hai hướng tương đương về mặt trực giác: xích bậc hai, hoặc mô hình semi-Markov cho phép xác suất chuyển phụ thuộc vào thời gian khoản vay đã lưu lại trong trạng thái hiện tại. Hướng thứ hai thường tiết kiệm tham số hơn và gần với cách diễn giải nghiệp vụ hơn.

**Ma trận chuyển theo phân khúc.** Ước lượng riêng cho các nhóm điểm tín dụng, tỷ lệ khoản vay trên giá trị tài sản hoặc khu vực địa lý sẽ khắc phục hạn chế về tính đồng nhất của danh mục, với điều kiện mỗi phân khúc còn đủ số sự kiện vỡ nợ để ước lượng ổn định.

**Định lượng độ bất định của ước lượng.** Báo cáo mới chỉ tính khoảng tin cậy cho các tỷ lệ quan sát thực nghiệm. Việc xây dựng khoảng tin cậy cho chính phân phối dừng và ma trận xác suất hấp thụ, chẳng hạn bằng phương pháp bootstrap theo khoản vay, sẽ cho phép đánh giá đầy đủ hơn độ tin cậy của các dự báo xác suất vỡ nợ.

**Mở rộng dữ liệu.** Dùng bộ Standard thay cho bộ Sample, hoặc bổ sung các năm khởi tạo khác, sẽ tăng số sự kiện vỡ nợ và đặc biệt là làm dày các nhóm quá hạn nặng vốn chỉ có vài chục quan sát trong nghiên cứu này. Mẫu lớn hơn cũng cho phép mô hình hóa tường minh hiệu ứng vintage thay vì gộp trực tiếp như hiện tại.

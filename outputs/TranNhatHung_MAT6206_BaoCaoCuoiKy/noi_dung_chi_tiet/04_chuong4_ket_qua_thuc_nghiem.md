# CHƯƠNG 4: KẾT QUẢ THỰC NGHIỆM

> **[TODO — cần chạy pipeline]** Chương này chỉ là khung. Mỗi mục liệt kê bảng/hình cần chèn và các ý cần diễn giải. Không điền số liệu giả định.

## 4.1. Ước lượng ma trận chuyển trạng thái

- Bảng: số bản ghi, số khoản vay, số lần chuyển trong tập ước lượng; phân phối số quan sát $n_i$ theo trạng thái.
- Bảng: ma trận đếm $(n_{ij})$.
- Bảng + Hình: ma trận $\hat{P}$ (heatmap).
- Diễn giải: xác suất ở lại Current, tỷ lệ trượt (roll-forward) và phục hồi (cure) theo từng mức quá hạn, các số không cấu trúc, độ chính xác của các hàng ít quan sát (mục 2.2.3).

## 4.2. Kết quả kiểm định giả thiết mô hình

### 4.2.1. Kiểm định tính thuần nhất theo thời gian

- Bảng: $\Lambda_{\text{TN}}$ (hoặc $\chi^2_{\text{TN}}$), bậc tự do, p-value cho kiểm định tổng thể và từng cặp giai đoạn.
- Hình: $\hat{P}(g)$ theo năm hoặc diễn biến một số xác suất chuyển chính theo năm; chuẩn Frobenius theo giai đoạn.
- Kết luận: bác bỏ / không bác bỏ $H_0$; ý nghĩa thực tiễn (đặc biệt giai đoạn 2020–2021).

### 4.2.2. Kiểm định bậc Markov

- Bảng: $\Lambda_{\text{bậc}}$, bậc tự do, p-value.
- Bảng: so sánh $\hat{p}_{hi\cdot}$ theo trạng thái trước đó $h$.
- Kết luận: bác bỏ / không bác bỏ $H_0$; diễn giải.

## 4.3. Kiểm chứng Chapman–Kolmogorov bằng số

- Bảng: $\hat{P}^3$, $\hat{P}^{(3)}_{\text{trực tiếp}}$, chênh lệch từng ô.
- Chỉ số: chuẩn Frobenius, sai lệch tuyệt đối lớn nhất.
- Hình: heatmap chênh lệch.
- Diễn giải: liên hệ với kết quả kiểm định bậc Markov.

## 4.4. Phân phối dừng: lý thuyết so với thực nghiệm

- Kết quả phân phối dừng lý thuyết (và phân phối tựa dừng nếu dùng).
- Bảng/Hình: phân phối trạng thái mô hình dự báo so với phân phối quan sát thực tế theo thời gian.
- Diễn giải theo mục 2.4.4.

## 4.5. Ma trận cơ bản, xác suất vỡ nợ và backtest trên tập kiểm định

- Bảng: $\hat{N}$, thời gian kỳ vọng đến hấp thụ $\hat{\tau}$, $\hat{B}$ và/hoặc $\mathrm{PD}_i(H)$.
- Bảng: $\mathrm{PD}_i(H)$ so với $\widehat{\mathrm{DR}}_i(H)$ theo trạng thái xuất phát, số khoản vay $m_i$, khoảng tin cậy.
- Hình: biểu đồ cột dự báo so với thực tế.
- Diễn giải: mức độ phù hợp, sai lệch có hệ thống, liên hệ với kết quả mục 4.2.

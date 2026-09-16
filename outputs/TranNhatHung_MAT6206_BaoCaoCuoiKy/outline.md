# Outline báo cáo cuối kỳ MAT6206

**Đề tài:** Xây dựng Ma trận Chuyển trạng thái (Roll-rate Matrix) bằng Xích Markov cho Cảnh báo sớm Rủi ro Vỡ nợ
**Tham khảo format:** `docs/theory/Gr17_LOIGIANGHUY_BUITHANHMAI_NGUYENHUONGTRA.pdf`
**Nội dung chi tiết:** `noi_dung_chi_tiet/` (mỗi phần 1 file) → gộp thành Word bằng `build_docx.sh`

| Phần | Cần làm gì | File | Trạng thái |
|---|---|---|---|
| Trang bìa + Mục lục | Thông tin môn, đề tài, giảng viên, học viên | `00_trang_bia.md` | Nháp (thiếu tên GV) |
| **Ch.1 Giới thiệu** | Đặt vấn đề, lý do chọn đề tài/dữ liệu, mục tiêu, đối tượng & phạm vi, cấu trúc báo cáo | `01_chuong1_gioi_thieu.md` | Nháp đầy đủ |
| **Ch.2 Cơ sở lý thuyết** | Xích Markov, MLE, Chapman–Kolmogorov, phân phối dừng, xích hấp thụ, kiểm định χ²/LR | `02_chuong2_co_so_ly_thuyet.md` | Nháp đầy đủ |
| **Ch.3 Dữ liệu & phương pháp** | Mô tả dữ liệu, tiền xử lý, chia tập theo thời gian, thiết kế kiểm định & backtest | `03_chuong3_du_lieu_va_phuong_phap.md` | Nháp — còn mục **[CẦN CHỐT]** |
| **Ch.4 Kết quả thực nghiệm** | 4.1 ước lượng P̂ · 4.2 hai kiểm định · 4.3 Chapman–Kolmogorov · 4.4 phân phối dừng · 4.5 backtest B | `04_chuong4_ket_qua_thuc_nghiem.md` | Khung — cần chạy pipeline |
| **Kết luận** | Tóm tắt (cần Ch.4), hạn chế, hướng mở rộng | `05_ket_luan.md` | Một phần |
| Tài liệu tham khảo | Sách/bài báo lý thuyết, tài liệu dữ liệu | `06_tai_lieu_tham_khao.md` | Nháp |

## Việc cần chốt trước khi viết Ch.4

1. Định nghĩa trạng thái **Default/Foreclosure** (mã DPD nào, zero-balance code nào).
2. Xử lý khoản vay **trả hết trước hạn (prepaid)**: kiểm duyệt (censoring) hay thêm trạng thái hấp thụ thứ hai — ảnh hưởng trực tiếp đến ý nghĩa của $B = NR$ (xem Ch.2 mục 2.5.5).
3. Kỳ hạn (horizon) dùng cho backtest ở 4.5 (ví dụ 12 và 24 tháng).

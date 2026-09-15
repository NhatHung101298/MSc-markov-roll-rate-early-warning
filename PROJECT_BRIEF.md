# Project Brief: Ma trận chuyển trạng thái (Roll-rate Matrix) cho Cảnh báo sớm Nợ

> File này là ngữ cảnh dự án dành cho Claude Code / bất kỳ AI coding assistant nào hỗ trợ triển khai. Đọc toàn bộ file trước khi viết bất kỳ dòng code nào — đặc biệt là phần "Ràng buộc phạm vi" và "Việc KHÔNG được làm".

---

## 1. Bối cảnh

Đây là **project cuối kỳ** của môn **MAT6206 — Các phương pháp ngẫu nhiên và ứng dụng**, chương trình Thạc sĩ Khoa học Dữ liệu, Khoa Toán – Cơ – Tin, Trường Đại học Khoa học Tự nhiên, ĐHQGHN.

- **Người thực hiện:** Trần Nhật Hưng, làm việc trong lĩnh vực risk modelling / IFRS 9 / IRB tại một công ty dữ liệu tài chính.
- **Vai trò của AI hỗ trợ:** đóng vai trò lập trình viên/cộng sự kỹ thuật, triển khai code theo đúng outline đã thống nhất bên dưới. Không tự ý mở rộng phạm vi lý thuyết.
- **Đây KHÔNG phải luận văn Thạc sĩ.** Đây là bài tập cuối kỳ của một môn học duy nhất, thời lượng làm việc ước tính **~6 buổi**. Người thực hiện còn nhiều công việc khác (đi làm, các môn học khác) nên mọi đề xuất mở rộng phạm vi cần được cân nhắc rất kỹ trước khi thêm vào.

## 2. Mục tiêu học thuật của project

Project phải chứng minh được sự hiểu biết về:
1. Xích Markov rời rạc thời gian, không gian trạng thái hữu hạn
2. Ước lượng hợp lý cực đại (MLE) cho ma trận chuyển
3. Phương trình Chapman–Kolmogorov
4. Phân phối dừng
5. Xích Markov hấp thụ (ma trận cơ bản, xác suất hấp thụ)
6. Kiểm định giả thiết mô hình (tính thuần nhất theo thời gian, bậc Markov) bằng các công cụ kiểm định đã học ở môn Thống kê Suy diễn (χ², likelihood ratio test)

**Nguyên tắc chấm điểm ngầm định:** giảng viên sẽ đánh giá cao việc *kiểm tra giả thiết mô hình* và *đối chiếu dự đoán lý thuyết với dữ liệu thực tế kiểm định*, hơn là việc áp công thức và xuất kết quả không phản biện.

## 3. Dữ liệu

**Nguồn chính:** Freddie Mac Single-Family Loan-Level Dataset (bộ Standard/Sample công khai).

- Mỗi khoản vay có lịch sử trạng thái quá hạn theo tháng.
- Rời rạc hóa thành 5 trạng thái: `{Current (0), 30 DPD, 60 DPD, 90+ DPD, Default/Foreclosure}`.
- `Default/Foreclosure` là **trạng thái hấp thụ**.
- Cần dữ liệu trải nhiều năm để có đủ giai đoạn con cho kiểm định tính thuần nhất (Chương 3–4).

**Dự phòng nếu Freddie Mac khó tải/quá nặng:** "American Express Default Prediction" (Kaggle) — ~13 tháng lịch sử hành vi/khách hàng. Nhẹ hơn nhưng ít giai đoạn hơn để so sánh — nếu dùng bộ này, phần kiểm định tính thuần nhất theo thời gian (4.2) có thể co lại thành so sánh 2 nửa kỳ thay vì nhiều giai đoạn theo năm.

**Chia dữ liệu:** theo thời gian (không random), ví dụ 80% đầu để ước lượng tham số, 20% cuối để kiểm định (validate) ở mục 4.5. Không random-split vì đây là dữ liệu chuỗi thời gian.

## 4. Cấu trúc báo cáo & checklist triển khai

### Chương 1 — Giới thiệu
- Đặt vấn đề, mục tiêu, phạm vi (nêu rõ: chỉ dùng xích Markov quan sát được, không dùng HMM/Cox/hazard — đây là lựa chọn chủ động).
- Không cần code, chỉ cần văn bản.

### Chương 2 — Cơ sở lý thuyết
Trình bày (kèm annotate rõ từng biến trong công thức khi viết báo cáo):

- **Ma trận chuyển:** `p_ij = P(S_{t+1}=j | S_t=i)`, ràng buộc `sum_j p_ij = 1`
- **MLE cho ma trận chuyển:** `p_hat_ij = n_ij / sum_k n_ik`
- **Chapman–Kolmogorov:** `P^(m+n) = P^(m) · P^(n)`
- **Phân phối dừng:** `π P = π`, `sum_i π_i = 1`
- **Dạng chuẩn ma trận hấp thụ:** `P = [[Q, R], [0, I]]`
- **Ma trận cơ bản:** `N = (I - Q)^{-1}`
- **Xác suất hấp thụ:** `B = N R`

Đây là phần văn bản lý thuyết, không phải code — nhưng code ở các chương sau phải cài đặt đúng các công thức này (không dùng thư viện HMM/survival có sẵn để "tắt" phần tính toán).

### Chương 3 — Dữ liệu & phương pháp
**Tiền xử lý:**
- [ ] Load dữ liệu, rời rạc hóa trạng thái DPD thành 5 bucket
- [ ] Xây bảng quỹ đạo trạng thái theo tháng cho từng khoản vay (loan_id, month, state)
- [ ] Chia theo thời gian: tập ước lượng (estimation set) / tập kiểm định (validation set)

**Phương pháp kiểm định (thiết kế, chưa chạy — chạy ở Chương 4):**
- [ ] Kiểm định tính thuần nhất theo thời gian: chia estimation set thành các giai đoạn con (theo năm), ước lượng P_hat riêng từng giai đoạn, thiết kế χ²-test so sánh từng cặp ma trận. H0: ma trận không đổi theo thời gian.
- [ ] Kiểm định bậc Markov: so sánh log-likelihood mô hình bậc 1 vs bậc 2 bằng likelihood ratio test. H0: bậc 1 là đủ.

### Chương 4 — Kết quả thực nghiệm
- [ ] **4.1** Ước lượng P_hat trên toàn bộ estimation set, heatmap ma trận chuyển, bảng số quan sát mỗi trạng thái
- [ ] **4.2** Chạy kiểm định thuần nhất theo thời gian → bảng kết quả χ² theo từng cặp giai đoạn + kết luận
- [ ] **4.2** Chạy kiểm định bậc Markov → kết quả LR test + kết luận
- [ ] **4.3** Kiểm chứng Chapman–Kolmogorov bằng số: tính P_hat^(1) theo tháng, ước lượng trực tiếp P_hat^(3) theo quý, so sánh (P_hat^(1))^3 với P_hat^(3) — định lượng sai lệch (VD: Frobenius norm hoặc so từng ô)
- [ ] **4.4** Tính phân phối dừng π từ P_hat, so sánh với tần suất thực nghiệm quan sát trong dữ liệu (không chỉ tính suông — phải đối chiếu)
- [ ] **4.5** Tính N và B từ estimation set → so sánh xác suất hấp thụ dự đoán (B) với tỷ lệ vỡ nợ **thực tế quan sát được trên validation set**, theo từng trạng thái xuất phát (đây là bước bắt buộc, tương đương "backtest" — không được bỏ qua)

### Kết luận
- Tóm tắt: mô hình Markov có phù hợp với dữ liệu không, dựa trên kết quả 4.2
- Hạn chế: giả định chỉ phụ thuộc trạng thái, không phụ thuộc đặc điểm khách hàng
- Hướng mở rộng (chỉ nêu, KHÔNG triển khai): semi-Markov với biến vĩ mô, phân tích theo phân khúc khách hàng

## 5. Yêu cầu kỹ thuật

- **Ngôn ngữ lập trình:** Python (người thực hiện đã thành thạo R từ môn Suy diễn thống kê trước đó, môn này chủ động chuyển sang Python — không cần ôn lại R).
- **Thư viện đề xuất:** `pandas`, `numpy` (tự cài đặt các công thức Markov thủ công, không dùng thư viện HMM/Markov có sẵn để giữ tính minh bạch học thuật), `scipy.stats` (cho χ², likelihood ratio test), `matplotlib`/`seaborn` (heatmap, biểu đồ).
- **Không dùng** các thư viện `hmmlearn`, `lifelines`, `scikit-survival` hay tương đương — phạm vi project không bao gồm HMM hay survival analysis (xem mục 6).
- **Output báo cáo:** tiếng Việt, công thức LaTeX, có thể xuất dạng Markdown/HTML với MathJax theo phong cách đã dùng ở các module trước của môn này (theme indigo/jade, layout dạng card).
- Mỗi phần code nên đi kèm chú thích rõ ràng nối lại công thức lý thuyết ở Chương 2 tương ứng — để khi viết báo cáo có thể trích thẳng.

## 6. Việc KHÔNG được làm (chặn scope creep)

Đây là phần quan trọng nhất để giữ project đúng khối lượng ~6 buổi. **Không** triển khai các nội dung sau dù có vẻ liên quan hoặc "làm cho đẹp":

- ❌ Hidden Markov Model (HMM), thuật toán Baum-Welch, Viterbi
- ❌ Discrete-time hazard / Cox Proportional Hazards / survival analysis
- ❌ Multistate hoặc semi-Markov regression
- ❌ So sánh với Random Survival Forest, XGBoost-AFT hay bất kỳ mô hình ML nào
- ❌ Xây dựng chiến lược giao dịch, backtest kiểu trading strategy (không liên quan bài toán này)
- ❌ Phân tích theo phân khúc khách hàng (segment-level transition matrix) — đây là hướng mở rộng hay, nhưng CHỈ thêm nếu người thực hiện chủ động yêu cầu, không tự ý thêm vì lo "chưa đủ dày"
- ❌ Bootstrap confidence interval cho π hoặc B — cùng lý do như trên, chỉ thêm khi được yêu cầu rõ

Nếu trong quá trình code thấy một hướng mở rộng "rất hay", hãy **dừng lại và hỏi người thực hiện** trước khi triển khai, thay vì tự động thêm vào.

## 7bis. Cấu trúc thư mục dự án

```
Stochastic_method/
├── main.py              # điểm chạy chính: orchestrate toàn bộ pipeline (import từ scripts/, không subprocess)
├── data/
│   ├── raw/              # file gốc tải từ Freddie Mac — KHÔNG sửa tay (sample_orig_2016.txt, sample_perf_2016.txt, .zip)
│   └── processed/        # output ETL, build lại được (loan_trajectory, estimation_set, validation_set)
├── notebooks/            # EDA thăm dò dữ liệu thô — không phải deliverable, không cần chạy lại từ đầu đến cuối
├── scripts/
│   ├── 01..08_*.py       # từng bước theo checklist Chương 3–4, đánh số theo thứ tự chạy
│   └── utils/            # hàm Markov thủ công dùng lại (MLE, Chapman-Kolmogorov, N=(I-Q)^-1, B=NR...)
├── outputs/
│   ├── figures/          # heatmap, biểu đồ
│   ├── tables/           # bảng số (χ², LR test, so sánh B vs actual...)
│   └── reports/          # log/stdout từng lần chạy
└── report/               # report.ipynb — deliverable cuối, chỉ gọi lại utils/, không viết logic mới
```

Đã chốt cấu trúc folder lớn (2026-09-07); nội dung/file bên trong từng folder sẽ tạo dần theo tiến độ, không tạo sẵn.

## 7. Định nghĩa hoàn thành (Definition of Done)

Project được coi là hoàn chỉnh khi có:
1. Notebook/script chạy được từ đầu đến cuối, tái lập toàn bộ kết quả Chương 4
2. Mỗi mục 4.1–4.5 có: kết quả số + diễn giải bằng lời (không chỉ in bảng số)
3. Ít nhất 2 chỗ có **kiểm định giả thiết + kết luận rõ ràng bác bỏ/không bác bỏ H0** (mục 4.2, hai kiểm định)
4. Mục 4.5 có **đối chiếu dự đoán mô hình với dữ liệu validation set thực tế** — đây là tiêu chí bắt buộc, không phải tùy chọn
5. Báo cáo cuối cùng dạng Markdown/HTML, tiếng Việt, công thức LaTeX đầy đủ chú thích biến số

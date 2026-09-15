# 10 đề tài dự án / luận văn Data Science trong ngân hàng
### Tổng hợp cho Trần Nhật Hưng — dùng để thực hành và chọn hướng luận văn Thạc sĩ KHDL (ĐH KHTN)

> Bộ đề tài này được chọn lọc dựa trên: (1) thế mạnh nghề nghiệp của bạn (risk modelling, IFRS 9/IRB tại FiinGroup) và dự án `credit-risk-ifrs9` đang xây; (2) chương trình môn học Thạc sĩ KHDL bạn đang theo; (3) danh sách 129 luận văn trường đã hướng dẫn (đối chiếu để mỗi đề tài đều có giảng viên phù hợp); (4) khảo sát repo/dataset/cuộc thi nổi bật trên GitHub–Kaggle và các công bố học thuật 2024–2026.

---

## Tiêu chí chấm điểm mỗi đề tài

Mỗi đề tài được đánh giá trên 5 trục (thang ★1–5):

- **Signature / lượng nghiên cứu**: mức độ "kinh điển" và số lượng tài liệu để bảo vệ.
- **Khả thi dữ liệu**: có bộ dữ liệu công khai, chất lượng, đủ cho luận văn hay không.
- **Chiều sâu toán/mô hình**: có "đất" để thể hiện năng lực KHDL (không chỉ gọi thư viện).
- **Phù hợp thế mạnh của bạn**: tận dụng domain IFRS 9/IRB + dự án sẵn có.
- **Tính mới để bảo vệ**: khả năng tạo đóng góp riêng, tránh "đề tài dùng lại".

---

# TẦNG A — Rủi ro tín dụng / IFRS 9 / IRB (lõi thế mạnh, có dự án sẵn)

## Đề tài 1 ⭐ (FLAGSHIP) — Mô hình cấu trúc kỳ hạn PD trọn đời (Lifetime PD term-structure) theo IFRS 9 bằng phân tích sống sót có biến vĩ mô

**Bài toán & vì sao "signature":** IFRS 9 yêu cầu PD *point-in-time, forward-looking* trải theo từng năm của vòng đời khoản vay (marginal PD theo t), thay vì một PD 12 tháng tĩnh kiểu IRB. Đây chính là mắt xích khó nhất và quan trọng nhất của ECL — và là phần Block 2 trong dự án của bạn. Đề tài này biến kiến thức lý thuyết bạn đã học thành một mô hình định lượng đầy đủ, có thể tái lập.

**Mô hình cốt lõi (tăng dần độ phức tạp — đúng "đất" để so sánh trong luận văn):**
1. Chuỗi Markov / ma trận chuyển trạng thái (baseline TTC).
2. Survival thời gian rời rạc (discrete-time hazard) qua hồi quy logistic / complementary log-log với biến phụ thuộc thời gian → cho PD biên theo từng kỳ.
3. Cox Proportional Hazards + biến đồng thời biến thiên theo thời gian (macro covariates).
4. Multistate / semi-Markov hồi quy (Markov + Beta regression + Multinomial logistic cho từng ô ma trận chuyển).
5. So sánh với ML sống sót: Random Survival Forest, XGBoost-AFT.

**Dữ liệu (công khai, đủ cho lifetime):**
- Freddie Mac Single-Family Loan-Level Dataset / Fannie Mae — dữ liệu hiệu suất khoản vay theo tháng, nhiều năm → lý tưởng để dựng đường cong sống sót và gắn biến vĩ mô.
- Lending Club (Kaggle, 2007–2015, >800k khoản) — dùng được cho PD/LGD/EAD.
- Hoặc dùng chính bộ mô phỏng `data_simulation.py` của bạn để kiểm soát ground truth (tốt cho phần validation).

**Điểm mới để bảo vệ:** so sánh có hệ thống PIT vs TTC; đưa biến vĩ mô vào hazard và chứng minh độ nhạy ECL theo kịch bản; nối sang stress testing (satellite model). Rất ít luận văn tiếng Việt làm mảng này ở mức survival + multistate.

**Liên kết môn học:** Phương pháp ngẫu nhiên (Markov/hazard), Mô hình hóa thống kê, Nhập môn suy diễn thống kê.

**GV khả dĩ (từ danh sách trường):** TS. Phạm Đình Tùng (chuỗi thời gian & cảnh báo nợ — #127, #129), TS. Trịnh Quốc Anh (mô hình Bayes cho chuỗi thời gian — #63), TS. Nguyễn Thịnh (mô hình tự hồi quy — #69).

**Tài liệu mồi:** Botha et al., *"Approaches for modelling the term-structure of default risk under IFRS 9: a tutorial using discrete-time survival analysis"* (arXiv 2507.15441); *"Modelling the term-structure… within a multistate regression framework"* (arXiv 2502.14479, có mã R trên GitHub); Ptak-Chmielewska & Gonzalez về Cox PH cho IFRS 9 (MDPI JRFM); Oracle *Multi-State Markov Modeling of IFRS9 PD term structure*. Cộng với bộ tài liệu bạn đã có (EBA GL 2017/16, EY, KPMG).

**Điểm:** Signature ★★★★★ · Khả thi dữ liệu ★★★★☆ · Chiều sâu ★★★★★ · Phù hợp bạn ★★★★★ · Tính mới ★★★★☆

---

## Đề tài 2 — Benchmark mô hình LGD: OLS vs Beta regression vs two-stage (Logit+OLS) vs ML, kèm downturn adjustment (IRB) và PIT (IFRS 9)

**Bài toán & vì sao "signature":** LGD có phân phối lưỡng đỉnh (bimodal) khét tiếng khó, nơi OLS thất bại và nơi calibration quan trọng hơn discrimination. Đây là phần bạn đã học ở Block 2 và có sẵn paper Loterman et al. — biến nó thành nghiên cứu benchmark hoàn chỉnh.

**Mô hình cốt lõi:** OLS (baseline & để chỉ ra hạn chế); Beta regression / fractional response; two-stage (Logit phân loại LGD≈0 / LGD>0, rồi OLS/Beta cho phần liên tục); XGBoost/LightGBM; so sánh calibration (bias, độ lệch trung bình) vs discrimination.

**Dữ liệu:** Lending Club (recoveries, charge-off) để dựng workout LGD; hoặc dữ liệu thế chấp có tài sản đảm bảo.

**Điểm mới để bảo vệ:** tái hiện & mở rộng xếp hạng của Loterman trên dữ liệu mới; làm rõ khác biệt LGD downturn (IRB) vs LGD PIT forward-looking (IFRS 9) — điểm phân biệt "người hành nghề" vs "người học lý thuyết".

**Liên kết môn học:** Mô hình hóa thống kê, Tối ưu hóa (ước lượng).

**GV khả dĩ:** PGS.TS Lê Hoàng Sơn (#34, #54), TS. Nguyễn Thịnh (#26).

**Tài liệu mồi:** Loterman et al. (bạn đã có); EBA GL 2017/16 phần LGD; CRE36.

**Điểm:** Signature ★★★★☆ · Khả thi ★★★★☆ · Chiều sâu ★★★★☆ · Phù hợp bạn ★★★★★ · Tính mới ★★★☆☆

---

## Đề tài 3 — EAD/CCF cho hạn mức tín dụng quay vòng (revolving) và mô hình prepayment

**Bài toán & vì sao "signature":** EAD/CCF trên thẻ tín dụng & hạn mức quay vòng là mảng "khó và ít người làm chuẩn" — người vay rút thêm hạn mức khi tiến gần vỡ nợ. Bạn đã có sẵn paper PwC về revolving facilities và tài liệu revolving credit + ECL.

**Mô hình cốt lõi:** ước lượng CCF theo cohort/vintage; ba cách tiếp cận CCF (fixed-horizon, cohort, momentum); mô hình hồi quy cho CCF (Beta/fractional); mô hình prepayment (survival cạnh tranh rủi ro — competing risks).

**Dữ liệu:** dữ liệu hành vi thẻ tín dụng dạng chuỗi thời gian (kiểu AMEX Default Prediction — 458k khách hàng, 190 biến hành vi B_/S_/P_/D_/R_), hoặc dữ liệu line-of-credit.

**Điểm mới để bảo vệ:** rất ít luận văn chạm tới EAD/CCF; competing-risks cho prepayment là "đất" phương pháp đẹp.

**Liên kết môn học:** Mô hình hóa thống kê, Phương pháp ngẫu nhiên.

**GV khả dĩ:** TS. Nguyễn Thịnh (thiết kế kho dữ liệu #85), PGS.TS Tạ Công Sơn.

**Tài liệu mồi:** PwC *Revolving credit facilities and ECL* (bạn đã có); EBA GL 2017/16 phần EAD.

**Điểm:** Signature ★★★☆☆ · Khả thi ★★★☆☆ · Chiều sâu ★★★★☆ · Phù hợp bạn ★★★★★ · Tính mới ★★★★★

---

# TẦNG B — Chấm điểm tín dụng (PD): signature, nhiều nghiên cứu, khả thi cao

## Đề tài 4 — So sánh Scorecard (Logistic + WoE) vs GBDT (XGBoost/LightGBM/CatBoost) vs Deep tabular, dưới ràng buộc giải thích được + ổn định + hiệu chỉnh

**Bài toán & vì sao "signature":** Đây là bài toán được nghiên cứu NHIỀU NHẤT trong domain — nhưng chính vì thế, góc "chính xác vs giải thích vs ổn định dưới góc nhìn pháp lý (EBA/Basel)" mới là phần tạo giá trị, thay vì chỉ so AUC.

**Mô hình cốt lõi:** Logistic + Weight-of-Evidence + scorecard (chuẩn ngành, giải thích được); XGBoost/LightGBM/CatBoost; TabNet/MLP; SHAP để giải thích; PSI để đo ổn định; reliability diagram + Platt/Isotonic để hiệu chỉnh xác suất.

**Dữ liệu (rất phong phú):** Home Credit Default Risk (Kaggle, ứng dụng + bureau), AMEX Default Prediction, Give Me Some Credit, German Credit (UCI), HELOC/FICO xML Challenge.

**Điểm mới để bảo vệ:** khung đánh giá 3 chiều (accuracy–interpretability–stability); "glass-box" model (EBM/reduced feature) đạt gần bằng black-box với ít đặc trưng hơn nhiều — hướng đang nóng.

**Liên kết môn học:** Mô hình hóa thống kê, Tối ưu hóa nâng cao (chọn đặc trưng, siêu tham số).

**GV khả dĩ:** TS. Nguyễn Thịnh (đề tài #26 trùng khớp gần như tuyệt đối), PGS.TS Lê Hoàng Sơn (#34, #54).

**Tài liệu mồi:** *Enhancing ML Interpretability for Credit Scoring* (arXiv 2509.11389); tổng quan hệ thống JRFM 2026 về Traditional/ML/DL; bộ SHAP/EBM.

**Lưu ý:** đề tài "đông người làm" → bắt buộc phải có góc riêng (ràng buộc pháp lý, hiệu chỉnh, hoặc concept drift) để bảo vệ tốt.

**Điểm:** Signature ★★★★★ · Khả thi ★★★★★ · Chiều sâu ★★★☆☆ · Phù hợp bạn ★★★★☆ · Tính mới ★★★☆☆

---

## Đề tài 5 — Reject inference & xử lý mất cân bằng lớp trong chấm điểm tín dụng

**Bài toán & vì sao "signature":** Mọi mô hình scorecard thực tế đều bị thiên lệch vì chỉ quan sát được khách đã *được duyệt* (accepted). Reject inference là bài toán thống kê đẹp và cực kỳ thực chiến mà giới học thuật VN ít chạm.

**Mô hình cốt lõi:** reweighting, parcelling, augmentation; mô hình Heckman (selection bias); bán giám sát (self-training, label propagation); so sánh với các kỹ thuật mất cân bằng (SMOTE, class weights, focal loss).

**Dữ liệu:** Lending Club (có cả khoản bị từ chối ở một số phiên bản), hoặc dựng kịch bản rejected từ ngưỡng duyệt.

**Điểm mới để bảo vệ:** định lượng "selection bias" ảnh hưởng ra sao đến PD và ECL — góc rất ít người làm.

**Liên kết môn học:** Nhập môn suy diễn thống kê (bias, missing-not-at-random), Mô hình hóa thống kê.

**GV khả dĩ:** PGS.TS Lê Hoàng Sơn, TS. Phạm Đình Tùng.

**Điểm:** Signature ★★★☆☆ · Khả thi ★★★☆☆ · Chiều sâu ★★★★☆ · Phù hợp bạn ★★★★☆ · Tính mới ★★★★★

---

## Đề tài 6 — Hồi quy logistic Bayes / phân cấp (hierarchical) cho xếp hạng tín dụng doanh nghiệp, có định lượng bất định

**Bài toán & vì sao "signature":** Với dữ liệu doanh nghiệp (ít quan sát, nhiều ngành), cách tiếp cận Bayes cho phép ước lượng PD kèm khoảng tin cậy (credible interval) — điều regulator rất thích và mô hình tần suất khó cho.

**Mô hình cốt lõi:** logistic Bayes; mô hình phân cấp theo ngành/quy mô (partial pooling); so sánh với logistic tần suất & XGBoost; MCMC / variational inference (PyMC, Stan, NumPyro).

**Dữ liệu:** báo cáo tài chính doanh nghiệp (đây đúng domain FiinGroup của bạn — lợi thế lớn); hoặc bộ Altman corporate default.

**Điểm mới để bảo vệ:** uncertainty quantification cho PD doanh nghiệp; shrinkage cho ngành thiếu dữ liệu.

**Liên kết môn học:** Nhập môn suy diễn thống kê (Bayes), Phương pháp ngẫu nhiên (MCMC).

**GV khả dĩ:** TS. Trịnh Quốc Anh (đề tài #98 trùng khớp: *"Hồi quy logistic Bayes trong xếp hạng tín dụng doanh nghiệp"*), PGS.TS Trần Mạnh Cường (mạng Bayes #62).

**Điểm:** Signature ★★★☆☆ · Khả thi ★★★★☆ · Chiều sâu ★★★★★ · Phù hợp bạn ★★★★★ · Tính mới ★★★★☆

---

# TẦNG C — Giám sát danh mục & cảnh báo sớm (nối trực tiếp JD Mcredit)

## Đề tài 7 — Hệ thống cảnh báo sớm phát sinh nợ: phân loại thứ bậc (ordinal) trạng thái delinquency bằng transition matrix + ordinal ML

**Bài toán & vì sao "signature":** Đây là bài toán MIS/surveillance đúng kiểu vai trò CVCC ở Mcredit bạn từng phân tích, và trùng khớp gần như hoàn toàn với đề tài #127 của trường (*"hệ thống cảnh báo phát sinh nợ tại một ngân hàng Việt Nam"*). Nó cũng nối thẳng vào roll rate / flow rate / marginal PD bạn đã học.

**Mô hình cốt lõi:** ma trận chuyển trạng thái (transition/roll-rate matrix); ordinal logistic regression (proportional odds); gradient boosting cho bài toán thứ bậc; đối chiếu tính vững Fisher (Fisher consistency) của hàm mất mát cho phân loại thứ bậc; nối sang marginal PD.

**Dữ liệu:** dữ liệu delinquency dạng bucket (0/30/60/90+ DPD) theo thời gian — AMEX behavioral, Freddie Mac performance, hoặc mô phỏng từ dự án của bạn.

**Điểm mới để bảo vệ:** rất "đắt" cho phỏng vấn/nghề — thể hiện mối liên hệ transition matrix ↔ marginal PD và phân biệt coincident vs lagged delinquency.

**Liên kết môn học:** Mô hình hóa thống kê, Phương pháp ngẫu nhiên (Markov).

**GV khả dĩ:** TS. Phạm Đình Tùng (#126 cảnh báo sớm Fintech, #127 cảnh báo nợ, #128 phân loại đa lớp) — gần như là "người của đề tài này".

**Điểm:** Signature ★★★★☆ · Khả thi ★★★★☆ · Chiều sâu ★★★★☆ · Phù hợp bạn ★★★★★ · Tính mới ★★★★☆

---

# TẦNG D — Ngoài tín dụng (signature toàn ngành, rất nhiều nghiên cứu)

## Đề tài 8 — Phát hiện gian lận giao dịch / rửa tiền (AML) bằng Graph Neural Network

**Bài toán & vì sao "signature":** Rửa tiền là bài toán quan hệ (mule accounts, layering) — vô hình ở cấp giao dịch đơn lẻ nhưng lộ ra ở cấu trúc đồ thị. Đây là mảng bùng nổ nghiên cứu 2023–2026 với dataset benchmark chuẩn.

**Mô hình cốt lõi:** GCN / GraphSAGE / Graph Attention Network; baseline Gradient Boosted Trees + graph feature preprocessing; xử lý mất cân bằng cực đoan; đồ thị thời gian (temporal graph).

**Dữ liệu (benchmark thật):** IBM Transactions for AML (Kaggle, Altman 2023 — bộ NeurIPS 2023, có HI/LI Small–Medium–Large); IBM AMLSim (GitHub); Elliptic Bitcoin; Credit Card Fraud ULB (Kaggle, kinh điển cho imbalanced).

**Điểm mới để bảo vệ:** so sánh biểu diễn "giao dịch là node" vs "giao dịch là edge"; GNN vs GBT+graph features; giải thích (xFraud).

**Liên kết môn học:** Toán rời rạc & thuật toán (đồ thị), Phương pháp số đại số tuyến tính (spectral/GCN), Tối ưu hóa.

**GV khả dĩ:** PGS.TS Tạ Công Sơn & TS. Nguyễn Thịnh (Graph Data Science #109), TS. Nguyễn Hải Vinh (#112, #118).

**Tài liệu mồi:** Weber et al. *Scalable Graph Learning for AML*; Altman et al. *Realistic Synthetic Financial Transactions for AML* (NeurIPS 2023); *A Review on GNN Methods in Financial Applications*.

**Điểm:** Signature ★★★★★ · Khả thi ★★★★★ · Chiều sâu ★★★★☆ · Phù hợp bạn ★★★☆☆ · Tính mới ★★★★☆

---

## Đề tài 9 — Financial NLP: phân tích sắc thái & trích xuất thông tin từ báo cáo/tin tức tài chính bằng LLM (FinBERT vs GPT), ứng dụng tạo tín hiệu rủi ro

**Bài toán & vì sao "signature":** Mảng NLP tài chính đang cực nóng và trường bạn có rất nhiều GV mạnh mảng này (đề tài #4, #13, #17, #24, #93, #119, #123, #124). Điểm khác biệt: làm cho **tiếng Việt** và nối tín hiệu sang cảnh báo rủi ro tín dụng/đầu tư.

**Mô hình cốt lõi:** FinBERT (fine-tune); so sánh với LLM tổng quát dạng zero-/few-shot + prompt engineering; đánh giá look-ahead bias; (mở rộng) trích xuất bảng số liệu từ ảnh báo cáo (OCR + layout).

**Dữ liệu:** Financial PhraseBank (Malo 2014), FiQA, dữ liệu tin tài chính tiếng Việt tự thu thập; mô hình nền FinBERT trên HuggingFace.

**Điểm mới để bảo vệ:** benchmark FinBERT vs LLM cho tiếng Việt; nối sentiment → tín hiệu default/biến động — cầu nối NLP × rủi ro.

**Liên kết môn học:** Mô hình hóa thống kê; (ít trùng hơn nhưng bù bằng độ nóng).

**GV khả dĩ:** PGS.TS Lê Hồng Phương (#13, #52, #123, #124), TS. Nguyễn Thị Minh Huyền (NER tài chính #4), TS. Nguyễn Thị Bích Thủy (#17, #24), TS. Đỗ Thanh Hà (#119), TS. Vũ Tiến Dũng (#93).

**Tài liệu mồi:** Araci *FinBERT* (2019); Lee et al. *A Survey of LLMs in Finance (FinLLMs)*; repo adlnlp/FinLLMs.

**Điểm:** Signature ★★★★☆ · Khả thi ★★★★☆ · Chiều sâu ★★★☆☆ · Phù hợp bạn ★★★☆☆ · Tính mới ★★★★☆

---

## Đề tài 10 — Tối ưu hóa danh mục & chiến lược giao dịch: Markowitz/robust + ML dự báo + (tùy chọn) Reinforcement Learning

**Bài toán & vì sao "signature":** Nhóm đề tài được trường hướng dẫn nhiều nhất (#6, #47, #53, #57, #101, #102, #111, #116, #117). Đây là "đất" tối ưu hóa và phương pháp ngẫu nhiên thuần chất, hợp với môn Tối ưu hóa nâng cao.

**Mô hình cốt lõi:** Markowitz mean-variance (quadratic programming) → robust/Black-Litterman; ML dự báo lợi suất/biến động (LSTM, XGBoost); RL (DQN/PPO) cho phân bổ tài sản như một MDP; thuật toán di truyền cho phân bổ.

**Dữ liệu:** giá cổ phiếu qua yfinance / dữ liệu chứng khoán VN.

**Điểm mới để bảo vệ:** so sánh tối ưu hóa cổ điển vs RL trên chi phí giao dịch & drawdown; robustness khi hiệp phương sai ước lượng sai.

**Liên kết môn học:** Tối ưu hóa nâng cao (QP/convex), Phương pháp ngẫu nhiên (MDP).

**GV khả dĩ:** TS. Đặng Thị Thu Hiền (#47, #53, #117), PGS.TS Trần Trọng Hiếu (#102, #111), TS. Vũ Tiến Dũng (#101), PGS.TS Trần Thị Xuân Anh (robo-advisor #57).

**Lưu ý:** đông người làm & xa domain rủi ro tín dụng của bạn → chọn nếu muốn đổi hướng, không phải để tận dụng thế mạnh sẵn có.

**Điểm:** Signature ★★★★★ · Khả thi ★★★★★ · Chiều sâu ★★★★☆ · Phù hợp bạn ★★☆☆☆ · Tính mới ★★★☆☆

---

# Ma trận so sánh nhanh

| # | Đề tài | Signature | Khả thi DL | Chiều sâu | Hợp bạn | Tính mới |
|---|--------|:---:|:---:|:---:|:---:|:---:|
| 1 | Lifetime PD term-structure (survival) ⭐ | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ |
| 2 | Benchmark LGD | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| 3 | EAD/CCF revolving | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★★★ |
| 4 | Scorecard vs GBDT + XAI | ★★★★★ | ★★★★★ | ★★★☆☆ | ★★★★☆ | ★★★☆☆ |
| 5 | Reject inference | ★★★☆☆ | ★★★☆☆ | ★★★★☆ | ★★★★☆ | ★★★★★ |
| 6 | PD doanh nghiệp Bayes | ★★★☆☆ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ |
| 7 | Cảnh báo sớm nợ (ordinal) | ★★★★☆ | ★★★★☆ | ★★★★☆ | ★★★★★ | ★★★★☆ |
| 8 | AML / fraud bằng GNN | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| 9 | Financial NLP / LLM | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★☆☆ | ★★★★☆ |
| 10 | Danh mục / RL trading | ★★★★★ | ★★★★★ | ★★★★☆ | ★★☆☆☆ | ★★★☆☆ |

---

# Khuyến nghị chọn hướng luận văn

**Lựa chọn số 1 — Đề tài 1 (Lifetime PD term-structure bằng survival analysis).** Vì: (a) nối thẳng vào dự án `credit-risk-ifrs9` và bộ tài liệu bạn đã có → tiết kiệm thời gian nền; (b) có literature 2025–2026 rất mới và có mã nguồn tái lập; (c) chiều sâu toán (hazard, Markov, multistate) khớp trọn vẹn với môn Phương pháp ngẫu nhiên + Suy diễn thống kê; (d) khan hiếm ở VN → dễ tạo đóng góp mới; (e) tận dụng đúng thế mạnh nghề của bạn.

**Hai lựa chọn thay thế mạnh:**
- **Đề tài 7 (cảnh báo sớm nợ, ordinal)** — nếu bạn muốn luận văn "bắc cầu thẳng sang thị trường việc làm" (Mcredit và tương tự), vì nó vừa là nghiên cứu vừa là năng lực phỏng vấn.
- **Đề tài 6 (PD doanh nghiệp Bayes)** — nếu bạn muốn khai thác dữ liệu doanh nghiệp (đúng sân FiinGroup) và thể hiện năng lực suy diễn thống kê Bayes.

**Chiến lược 2 lớp gợi ý:** dùng **Đề tài 4** (hoặc 8) làm *dự án thực hành ngắn* để build portfolio nhanh trên dữ liệu Kaggle công khai; dùng **Đề tài 1** (hoặc 7) làm *luận văn* có chiều sâu.

---

# Đề tài dự bị (honorable mentions, hợp môn Đại số tuyến tính số / Tối ưu hóa)

- **Phương pháp ngẫu nhiên hóa (randomized) trong tính toán ma trận lớn** áp dụng vào ước lượng hiệp phương sai / PCA cho danh mục rủi ro (khớp #42, #49, #121 và môn Phương pháp số ĐSTT).
- **Định giá chứng khoán phái sinh qua biến đổi Fourier** (khớp #97, TS. Nguyễn Ngọc Phan) — thiên quant/toán tài chính.
- **Bài toán thời điểm dừng tối ưu (optimal stopping) trong đầu tư bằng AI** (khớp #79, TS. Phạm Văn Khánh).

---

# Bước tiếp theo (khi bạn đã chọn)

1. Chốt 1 đề tài chính + 1 dự án thực hành ngắn.
2. Tôi giúp bạn: thu hẹp phạm vi (scope) đủ cho luận văn Thạc sĩ, chốt bộ dữ liệu, viết đề cương (research questions + phương pháp + kế hoạch chương), và dựng repo khởi động.
3. Với Đề tài 1/2/3/7: ta có thể tái dùng kiến trúc dữ liệu 4 bảng (`loan_master`, `loan_performance`, `default_recovery`, `macro_scenario`) đã thiết kế.

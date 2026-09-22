# CHƯƠNG 2: CƠ SỞ LÝ THUYẾT

Chương này trình bày các kết quả lý thuyết làm nền tảng cho mô hình. Các ký hiệu được thống nhất như sau: $(\Omega, \mathcal{F}, \mathbb{P})$ là không gian xác suất; $\{S_t\}_{t \ge 0}$ là quá trình trạng thái của một khoản vay với $t$ là chỉ số tháng; $\mathcal{S}$ là không gian trạng thái hữu hạn gồm $K$ phần tử; ma trận được ký hiệu bằng chữ in hoa ($P, Q, R, N, B$), vectơ dòng được ký hiệu bằng chữ Hy Lạp ($\pi, \mu$).

## 2.1. Xích Markov rời rạc thời gian

### 2.1.1. Định nghĩa

Một dãy biến ngẫu nhiên $\{S_t\}_{t = 0, 1, 2, \dots}$ nhận giá trị trong tập hữu hạn $\mathcal{S}$ được gọi là **xích Markov rời rạc thời gian** nếu với mọi $t \ge 0$ và mọi $i_0, \dots, i_{t-1}, i, j \in \mathcal{S}$ sao cho biến cố điều kiện có xác suất dương:

$$\mathbb{P}(S_{t+1} = j \mid S_t = i, S_{t-1} = i_{t-1}, \dots, S_0 = i_0) = \mathbb{P}(S_{t+1} = j \mid S_t = i). \tag{2.1}$$

Đẳng thức (2.1) là **tính chất Markov**: khi đã biết trạng thái hiện tại $S_t$, trạng thái tương lai $S_{t+1}$ độc lập có điều kiện với toàn bộ quá khứ $(S_0, \dots, S_{t-1})$. Trong bối cảnh tín dụng, giả thiết này có nghĩa là: để dự báo tháng sau khoản vay sẽ ở mức quá hạn nào, chỉ cần biết tháng này khoản vay đang ở mức quá hạn nào, còn việc khoản vay đã đến mức đó bằng con đường nào là không quan trọng.

Xích Markov được gọi là **thuần nhất theo thời gian** (time-homogeneous) nếu xác suất chuyển ở (2.1) không phụ thuộc vào $t$:

$$\mathbb{P}(S_{t+1} = j \mid S_t = i) = p_{ij}, \quad \forall t \ge 0. \tag{2.2}$$

Đây là giả thiết thứ hai của mô hình: quy luật dịch chuyển giữa các mức quá hạn là như nhau bất kể giai đoạn kinh tế. Cả hai giả thiết (2.1) và (2.2) đều sẽ được kiểm định ở mục 2.6 và Chương 4.

### 2.1.2. Ma trận chuyển và phân phối trạng thái

Các xác suất chuyển một bước được sắp xếp thành **ma trận chuyển** $P = (p_{ij})_{i,j \in \mathcal{S}}$ kích thước $K \times K$, trong đó hàng $i$ là phân phối xác suất của trạng thái tháng sau khi tháng này đang ở trạng thái $i$. Do đó $P$ là một **ma trận ngẫu nhiên** (stochastic matrix):

$$p_{ij} \ge 0 \quad \forall i, j, \qquad \sum_{j \in \mathcal{S}} p_{ij} = 1 \quad \forall i. \tag{2.3}$$

Gọi $\mu^{(t)} = \big(\mathbb{P}(S_t = i)\big)_{i \in \mathcal{S}}$ là vectơ dòng phân phối trạng thái tại thời điểm $t$ và $\mu = \mu^{(0)}$ là phân phối ban đầu. Theo công thức xác suất toàn phần:

$$\mu^{(t+1)}_j = \sum_{i \in \mathcal{S}} \mu^{(t)}_i \, p_{ij} \quad \Longleftrightarrow \quad \mu^{(t+1)} = \mu^{(t)} P, \qquad \text{do đó } \mu^{(t)} = \mu P^t. \tag{2.4}$$

Hơn nữa, áp dụng liên tiếp quy tắc nhân xác suất và tính chất Markov, xác suất của một quỹ đạo cụ thể là:

$$\mathbb{P}(S_0 = i_0, S_1 = i_1, \dots, S_T = i_T) = \mu_{i_0} \, p_{i_0 i_1} \, p_{i_1 i_2} \cdots p_{i_{T-1} i_T}. \tag{2.5}$$

Công thức (2.5) cho thấy phân phối đồng thời của toàn bộ quỹ đạo được xác định hoàn toàn bởi cặp $(\mu, P)$, và là cơ sở để xây dựng hàm hợp lý ở mục 2.2.

### 2.1.3. Phân loại trạng thái

- Trạng thái $j$ **đến được** từ trạng thái $i$ (ký hiệu $i \to j$) nếu tồn tại $n \ge 0$ sao cho $\mathbb{P}(S_n = j \mid S_0 = i) > 0$. Hai trạng thái **liên thông** nếu $i \to j$ và $j \to i$.
- Xích Markov là **tối giản** (irreducible) nếu mọi cặp trạng thái đều liên thông.
- Trạng thái $i$ là **hồi quy** (recurrent) nếu xuất phát từ $i$, xích quay lại $i$ với xác suất 1; ngược lại $i$ là **tạm thời** (transient).
- Trạng thái $i$ là **hấp thụ** (absorbing) nếu $p_{ii} = 1$, tức một khi đã vào $i$ thì ở lại mãi mãi. Xích Markov được gọi là **xích hấp thụ** nếu có ít nhất một trạng thái hấp thụ và từ mọi trạng thái đều đến được một trạng thái hấp thụ.

### 2.1.4. Không gian trạng thái của bài toán

Trong báo cáo, không gian trạng thái gồm $K = 6$ trạng thái được rời rạc hóa từ số ngày quá hạn (Days Past Due — DPD), với **hai** trạng thái hấp thụ (lý do dùng hai thay vì một trạng thái hấp thụ được trình bày ở mục 2.5.5; quy tắc ánh xạ dữ liệu → trạng thái ở mục 3.2.1):

| Ký hiệu | Trạng thái | Ý nghĩa |
|---|---|---|
| 0 | Current | Trả nợ đúng hạn hoặc quá hạn dưới 30 ngày |
| 1 | 30 DPD | Quá hạn từ 30 đến 59 ngày |
| 2 | 60 DPD | Quá hạn từ 60 đến 89 ngày |
| 3 | 90+ DPD | Quá hạn từ 90 ngày trở lên, chưa bị xử lý như vỡ nợ |
| 4 | Default/Foreclosure | Vỡ nợ, tịch biên hoặc xử lý tài sản bảo đảm |
| 5 | Prepaid | Trả hết nợ trước hạn hoặc đáo hạn |

Trạng thái 4 và 5 là hai trạng thái hấp thụ ($p_{44} = 1$, $p_{55} = 1$); bốn trạng thái 0–3 là các trạng thái tạm thời vì từ mỗi trạng thái này đều có xác suất dương đi vào một trong hai trạng thái hấp thụ và không bao giờ quay lại. Ma trận chuyển có dạng:

$$P = \begin{pmatrix}
p_{00} & p_{01} & p_{02} & p_{03} & p_{04} & p_{05} \\
p_{10} & p_{11} & p_{12} & p_{13} & p_{14} & p_{15} \\
p_{20} & p_{21} & p_{22} & p_{23} & p_{24} & p_{25} \\
p_{30} & p_{31} & p_{32} & p_{33} & p_{34} & p_{35} \\
0 & 0 & 0 & 0 & 1 & 0 \\
0 & 0 & 0 & 0 & 0 & 1
\end{pmatrix}. \tag{2.6}$$

Về mặt cơ chế, số ngày quá hạn chỉ có thể tăng thêm tối đa khoảng 30 ngày sau mỗi tháng, nên các chuyển "nhảy cóc" lên mức quá hạn nặng hơn (ví dụ từ Current sang 60 DPD trong một tháng) về nguyên tắc có xác suất rất nhỏ hoặc bằng 0. Ngược lại, khoản vay có thể phục hồi từ bất kỳ mức quá hạn nào về Current nếu bên vay trả hết số tiền còn thiếu. Các ô bằng 0 do cơ chế này được gọi là **số không cấu trúc** (structural zeros) và cần được tính đến khi xác định bậc tự do của các kiểm định ở mục 2.6.

## 2.2. Ước lượng hợp lý cực đại cho ma trận chuyển

### 2.2.1. Hàm hợp lý

Giả sử quan sát được $M$ quỹ đạo độc lập (mỗi quỹ đạo là một khoản vay), quỹ đạo thứ $m$ là $(s^{(m)}_0, s^{(m)}_1, \dots, s^{(m)}_{T_m})$. Ký hiệu

$$n_{ij} = \sum_{m=1}^{M} \sum_{t=0}^{T_m - 1} \mathbf{1}\{s^{(m)}_t = i, \; s^{(m)}_{t+1} = j\}, \qquad n_i = \sum_{j \in \mathcal{S}} n_{ij}, \tag{2.7}$$

trong đó $n_{ij}$ là **tổng số lần chuyển** từ trạng thái $i$ sang trạng thái $j$ quan sát được trên toàn bộ dữ liệu, $n_i$ là tổng số lần xuất phát từ trạng thái $i$, và $\mathbf{1}\{\cdot\}$ là hàm chỉ thị. Ma trận $(n_{ij})$ được gọi là **ma trận đếm chuyển** (transition count matrix).

Theo (2.5) và tính độc lập giữa các khoản vay, hàm hợp lý có điều kiện theo trạng thái ban đầu là:

$$L(P) = \prod_{m=1}^{M} \prod_{t=0}^{T_m-1} p_{s^{(m)}_t s^{(m)}_{t+1}} = \prod_{i \in \mathcal{S}} \prod_{j \in \mathcal{S}} p_{ij}^{\,n_{ij}}, \tag{2.8}$$

và hàm log-hợp lý là

$$\ell(P) = \ln L(P) = \sum_{i \in \mathcal{S}} \sum_{j \in \mathcal{S}} n_{ij} \ln p_{ij}. \tag{2.9}$$

Nhận xét quan trọng: hàm hợp lý chỉ phụ thuộc vào dữ liệu thông qua ma trận đếm $(n_{ij})$, nghĩa là $(n_{ij})$ là **thống kê đủ** cho $P$.

### 2.2.2. Nghiệm hợp lý cực đại

Bài toán ước lượng là cực đại hóa (2.9) với ràng buộc (2.3). Do ràng buộc tổng hàng tách rời theo từng hàng $i$, ta xét hàm Lagrange

$$\mathcal{L}(P, \lambda) = \sum_{i} \sum_{j} n_{ij} \ln p_{ij} - \sum_{i} \lambda_i \Big( \sum_{j} p_{ij} - 1 \Big).$$

Lấy đạo hàm riêng theo $p_{ij}$ và cho bằng 0: $\dfrac{n_{ij}}{p_{ij}} - \lambda_i = 0$, suy ra $p_{ij} = n_{ij} / \lambda_i$. Thay vào ràng buộc $\sum_j p_{ij} = 1$ được $\lambda_i = n_i$. Vì $\ell$ là hàm lõm theo $P$ trên tập lồi xác định bởi (2.3), điểm dừng này là cực đại toàn cục. Vậy **ước lượng hợp lý cực đại (MLE)** của xác suất chuyển là:

$$\boxed{\hat{p}_{ij} = \frac{n_{ij}}{n_i} = \frac{n_{ij}}{\sum_{k \in \mathcal{S}} n_{ik}}} \tag{2.10}$$

tức là tỷ lệ số lần chuyển từ $i$ sang $j$ trên tổng số lần xuất phát từ $i$. Đây chính là cách tính ma trận roll-rate theo tần suất trong thực hành, và (2.10) cho thấy cách tính quen thuộc đó có cơ sở là một ước lượng hợp lý cực đại. Với hàng hấp thụ, ta giữ nguyên $\hat{p}_{44} = 1$ theo định nghĩa.

### 2.2.3. Tính chất tiệm cận

Với mỗi hàng $i$, khi cố định $n_i$, vectơ $(n_{i0}, \dots, n_{i,K-1})$ có phân phối đa thức với tham số $(n_i; p_{i0}, \dots, p_{i,K-1})$. Do đó (Anderson & Goodman, 1957):

- $\hat{p}_{ij}$ là ước lượng **vững** của $p_{ij}$ khi $n_i \to \infty$;
- $\sqrt{n_i}\,(\hat{p}_{ij} - p_{ij})$ hội tụ theo phân phối về phân phối chuẩn với

$$\operatorname{Var}(\hat{p}_{ij}) \approx \frac{p_{ij}(1 - p_{ij})}{n_i}, \qquad \operatorname{Cov}(\hat{p}_{ij}, \hat{p}_{ik}) \approx -\frac{p_{ij}\,p_{ik}}{n_i} \; (j \ne k); \tag{2.11}$$

- các hàng khác nhau của $\hat{P}$ độc lập tiệm cận.

Hệ quả thực tiễn của (2.11): độ chính xác của từng hàng phụ thuộc vào số quan sát $n_i$ của hàng đó. Trong dữ liệu tín dụng, phần lớn quan sát rơi vào trạng thái Current, nên các hàng 60 DPD và 90+ DPD — vốn quan trọng nhất đối với cảnh báo sớm — lại có ít quan sát nhất và sai số ước lượng lớn nhất. Điểm này cần được lưu ý khi diễn giải kết quả ở Chương 4.

## 2.3. Phương trình Chapman–Kolmogorov

### 2.3.1. Phát biểu và chứng minh

Ký hiệu $p^{(n)}_{ij} = \mathbb{P}(S_{t+n} = j \mid S_t = i)$ là xác suất chuyển sau $n$ bước và $P^{(n)} = (p^{(n)}_{ij})$. **Phương trình Chapman–Kolmogorov** phát biểu rằng với mọi $m, n \ge 0$:

$$p^{(m+n)}_{ij} = \sum_{k \in \mathcal{S}} p^{(m)}_{ik}\, p^{(n)}_{kj} \quad \Longleftrightarrow \quad P^{(m+n)} = P^{(m)} P^{(n)}. \tag{2.12}$$

*Chứng minh.* Theo công thức xác suất toàn phần với hệ đầy đủ $\{S_{t+m} = k\}_{k \in \mathcal{S}}$:

$$p^{(m+n)}_{ij} = \sum_{k} \mathbb{P}(S_{t+m+n} = j \mid S_{t+m} = k, S_t = i)\; \mathbb{P}(S_{t+m} = k \mid S_t = i).$$

Theo tính chất Markov, $\mathbb{P}(S_{t+m+n} = j \mid S_{t+m} = k, S_t = i) = \mathbb{P}(S_{t+m+n} = j \mid S_{t+m} = k) = p^{(n)}_{kj}$, và theo tính thuần nhất đại lượng này không phụ thuộc $t$. Thay vào ta được (2.12). $\blacksquare$

### 2.3.2. Hệ quả

Áp dụng quy nạp (2.12) với $P^{(1)} = P$ ta được $P^{(n)} = P^n$: **ma trận chuyển $n$ bước bằng lũy thừa bậc $n$ của ma trận chuyển một bước**. Hai hệ quả trực tiếp được sử dụng trong báo cáo:

- Ma trận chuyển theo quý suy ra từ ma trận theo tháng là $P^{(3)} = P^3$.
- Vì trạng thái 4 là hấp thụ, $p^{(n)}_{i4} = \mathbb{P}(S_{t+n} = 4 \mid S_t = i)$ chính là **xác suất vỡ nợ lũy kế trong vòng $n$ tháng** của một khoản vay đang ở trạng thái $i$ — đại lượng tương ứng với cấu trúc kỳ hạn của PD (ví dụ PD 12 tháng, PD trọn đời) trong IFRS 9.

### 2.3.3. Ý nghĩa đối với việc kiểm chứng mô hình

Phương trình (2.12) là hệ quả **tất yếu** của giả thiết Markov và thuần nhất. Do đó nếu dữ liệu tuân theo mô hình, thì ma trận chuyển ba tháng ước lượng **trực tiếp** từ dữ liệu,

$$\hat{P}^{(3)}_{\text{trực tiếp}} = \left( \frac{n^{(3)}_{ij}}{\sum_k n^{(3)}_{ik}} \right), \qquad n^{(3)}_{ij} = \#\{(m, t): s^{(m)}_t = i,\; s^{(m)}_{t+3} = j\},$$

phải xấp xỉ ma trận **suy ra từ mô hình** $\hat{P}^3$. Mức độ sai lệch được định lượng bằng chuẩn Frobenius

$$\big\| \hat{P}^3 - \hat{P}^{(3)}_{\text{trực tiếp}} \big\|_F = \sqrt{\sum_{i} \sum_{j} \Big( (\hat{P}^3)_{ij} - (\hat{P}^{(3)}_{\text{trực tiếp}})_{ij} \Big)^2}, \tag{2.13}$$

cùng với sai lệch tuyệt đối lớn nhất theo từng ô. Sai lệch lớn có hệ thống (ví dụ mô hình đánh giá thấp xác suất vẫn ở 90+ DPD sau ba tháng) là dấu hiệu cho thấy quá trình có "trí nhớ" dài hơn một tháng hoặc không thuần nhất — bổ sung cho các kiểm định hình thức ở mục 2.6.

## 2.4. Phân phối dừng

### 2.4.1. Định nghĩa

Vectơ dòng $\pi = (\pi_i)_{i \in \mathcal{S}}$ được gọi là **phân phối dừng** của xích Markov với ma trận chuyển $P$ nếu

$$\pi P = \pi, \qquad \pi_i \ge 0, \qquad \sum_{i \in \mathcal{S}} \pi_i = 1. \tag{2.14}$$

Theo (2.4), nếu phân phối ban đầu là $\pi$ thì $\mu^{(t)} = \pi$ với mọi $t$: phân phối trạng thái không thay đổi theo thời gian. Về mặt đại số, $\pi$ là **vectơ riêng trái** của $P$ ứng với giá trị riêng 1, được chuẩn hóa để tổng các thành phần bằng 1.

### 2.4.2. Sự tồn tại, duy nhất và hội tụ

- Mọi xích Markov trên không gian trạng thái hữu hạn đều có ít nhất một phân phối dừng.
- Nếu xích **tối giản**, phân phối dừng là **duy nhất** và $\pi_i = 1/\mathbb{E}_i[\tau_i]$, trong đó $\tau_i$ là thời điểm quay lại $i$ lần đầu.
- Nếu xích tối giản và **không tuần hoàn** (aperiodic), thì với mọi phân phối ban đầu $\mu$, $\mu P^t \to \pi$ khi $t \to \infty$ (định lý ergodic cho xích hữu hạn).

### 2.4.3. Cách tính

Hệ (2.14) tương đương với hệ tuyến tính $(P^\top - I)\,\pi^\top = 0$ kèm điều kiện $\mathbf{1}^\top \pi^\top = 1$. Vì hệ $(P^\top - I)\pi^\top = 0$ có hạng không đầy đủ, ta thay một phương trình bất kỳ bằng điều kiện chuẩn hóa và giải hệ tuyến tính thu được; hoặc tương đương, tính vectơ riêng của $P^\top$ ứng với giá trị riêng 1 rồi chuẩn hóa.

### 2.4.4. Phân phối dừng của xích có trạng thái hấp thụ

Xích Markov của bài toán **không tối giản** vì trạng thái 4 là hấp thụ. Khi đó kết quả ở mục 2.4.2 không áp dụng trực tiếp, và ta có nhận xét sau:

> Nếu xích có đúng một trạng thái hấp thụ $a$ và từ mọi trạng thái đều đến được $a$, thì phân phối dừng là duy nhất và **suy biến** tại $a$: $\pi = e_a = (0, \dots, 0, 1)$.

*Giải thích.* Từ (2.14), hạn chế trên các trạng thái tạm thời ta có $\pi_T Q = \pi_T$ (với $Q$ là khối chuyển giữa các trạng thái tạm thời, xem mục 2.5), mà $Q^n \to 0$ nên $\pi_T = \pi_T Q^n \to 0$, suy ra $\pi_T = 0$ và toàn bộ khối lượng xác suất nằm tại trạng thái hấp thụ. $\blacksquare$

Ý nghĩa: về dài hạn tuyệt đối, mô hình dự báo mọi khoản vay còn "sống" trong danh mục cuối cùng đều bị hấp thụ. Điều này **không mâu thuẫn** với dữ liệu, trong đó phần lớn khoản vay vẫn ở trạng thái Current, vì dữ liệu chỉ quan sát trong một cửa sổ thời gian hữu hạn và các khoản vay còn rời khỏi danh mục bằng những con đường khác (trả hết nợ trước hạn, đáo hạn). Vì vậy khi so sánh phân phối dừng với phân phối thực nghiệm ở Chương 4, báo cáo phân biệt rõ:

- phân phối dừng lý thuyết của toàn xích (suy biến tại trạng thái hấp thụ);
- phân phối trạng thái mô hình dự báo sau một số kỳ hữu hạn $\mu P^t$ theo (2.4);
- và phân phối trạng thái thực tế quan sát được, trong đó việc đối chiếu hai đại lượng sau là phép so sánh có ý nghĩa thực nghiệm.

Một khái niệm liên quan trong tài liệu là **phân phối tựa dừng** (quasi-stationary distribution — Darroch & Seneta, 1965): phân phối giới hạn của trạng thái **với điều kiện chưa bị hấp thụ**, xác định bởi vectơ riêng trái của $Q$ ứng với giá trị riêng lớn nhất (giá trị riêng Perron–Frobenius). Đại lượng này mô tả "cơ cấu ổn định" của phần danh mục chưa vỡ nợ và có thể so sánh trực tiếp với cơ cấu quá hạn quan sát được.

## 2.5. Xích Markov hấp thụ

### 2.5.1. Dạng chuẩn của ma trận chuyển

Xét xích hấp thụ có $s$ trạng thái tạm thời và $r$ trạng thái hấp thụ. Sắp xếp lại thứ tự trạng thái sao cho các trạng thái tạm thời đứng trước, ma trận chuyển có **dạng chuẩn** (canonical form):

$$P = \begin{pmatrix} Q & R \\ \mathbf{0} & I_r \end{pmatrix}, \tag{2.15}$$

trong đó:

- $Q \in \mathbb{R}^{s \times s}$: xác suất chuyển giữa các trạng thái tạm thời;
- $R \in \mathbb{R}^{s \times r}$: xác suất chuyển từ trạng thái tạm thời vào trạng thái hấp thụ;
- $\mathbf{0} \in \mathbb{R}^{r \times s}$: ma trận không (không thể rời trạng thái hấp thụ);
- $I_r$: ma trận đơn vị cấp $r$.

Với bài toán của báo cáo, $s = 4$ (Current, 30 DPD, 60 DPD, 90+ DPD) và $r = 2$ (Default/Foreclosure, Prepaid); $Q$ là khối $4 \times 4$ phía trên bên trái và $R$ là khối $4 \times 2$ gồm hai cột cuối (cột 5 và 6) của ma trận (2.6).

### 2.5.2. Lũy thừa của ma trận dạng chuẩn

Bằng quy nạp theo $n$, ta có

$$P^n = \begin{pmatrix} Q^n & \big(I + Q + Q^2 + \dots + Q^{n-1}\big) R \\ \mathbf{0} & I_r \end{pmatrix}. \tag{2.16}$$

Vì từ mọi trạng thái tạm thời đều đến được trạng thái hấp thụ, tồn tại $n_0$ và $c < 1$ sao cho xác suất chưa bị hấp thụ sau $n_0$ bước nhỏ hơn hoặc bằng $c$ với mọi trạng thái xuất phát; do đó xác suất chưa bị hấp thụ sau $k n_0$ bước không vượt quá $c^k \to 0$. Suy ra $Q^n \to \mathbf{0}$, hay bán kính phổ của $Q$ nhỏ hơn 1.

### 2.5.3. Ma trận cơ bản

Vì $Q^n \to \mathbf{0}$, chuỗi Neumann hội tụ và ma trận $I - Q$ khả nghịch:

$$N = (I - Q)^{-1} = \sum_{k=0}^{\infty} Q^k. \tag{2.17}$$

Ma trận $N$ được gọi là **ma trận cơ bản** (fundamental matrix). Ý nghĩa của phần tử $n_{ij}$: xuất phát từ trạng thái tạm thời $i$, số lần kỳ vọng xích ghé thăm trạng thái tạm thời $j$ trước khi bị hấp thụ. Thật vậy,

$$\mathbb{E}_i\Big[\sum_{t=0}^{\infty} \mathbf{1}\{S_t = j\}\Big] = \sum_{t=0}^{\infty} \mathbb{P}_i(S_t = j) = \sum_{t=0}^{\infty} (Q^t)_{ij} = n_{ij}.$$

Hệ quả: vectơ **thời gian kỳ vọng đến khi bị hấp thụ** là $\tau = N \mathbf{1}$, với $\tau_i$ là số tháng kỳ vọng mà một khoản vay xuất phát từ trạng thái $i$ còn ở các trạng thái tạm thời. Trong bài toán tín dụng, $\tau_i$ diễn giải là "thời gian sống kỳ vọng" của khoản vay trước khi vỡ nợ theo mô hình.

### 2.5.4. Ma trận xác suất hấp thụ

Gọi $b_{ik}$ là xác suất xích xuất phát từ trạng thái tạm thời $i$ cuối cùng bị hấp thụ tại trạng thái hấp thụ $k$, và $B = (b_{ik}) \in \mathbb{R}^{s \times r}$. **Phân tích bước đầu tiên** (first-step analysis): ở bước đầu tiên, xích hoặc đi thẳng vào $k$ (xác suất $r_{ik}$), hoặc đi sang một trạng thái tạm thời $j$ (xác suất $q_{ij}$) rồi từ đó bị hấp thụ tại $k$ (xác suất $b_{jk}$), nên

$$b_{ik} = r_{ik} + \sum_{j} q_{ij}\, b_{jk} \quad \Longleftrightarrow \quad B = R + QB \quad \Longleftrightarrow \quad (I - Q) B = R,$$

và do đó

$$\boxed{B = N R = (I - Q)^{-1} R}. \tag{2.18}$$

Cũng có thể thu được (2.18) bằng cách cho $n \to \infty$ ở khối trên bên phải của (2.16).

### 2.5.5. Nhận xét quan trọng: xác suất hấp thụ khi chỉ có một trạng thái hấp thụ, và xác suất vỡ nợ trong kỳ hạn hữu hạn

Nếu xích chỉ có **một** trạng thái hấp thụ ($r = 1$), vì mỗi hàng của $(Q \;\; R)$ có tổng bằng 1 nên $R = (I - Q)\mathbf{1}$, suy ra

$$B = N R = (I - Q)^{-1}(I - Q)\mathbf{1} = \mathbf{1}.$$

Nghĩa là: trong mô hình năm trạng thái với Default là trạng thái hấp thụ duy nhất, **xác suất hấp thụ trọn đời bằng 1 cho mọi trạng thái xuất phát** — một kết quả đúng về mặt toán học nhưng không mang thông tin phân biệt rủi ro. Nguyên nhân là mô hình chưa tính đến việc khoản vay có thể **rời khỏi danh mục một cách "an toàn"** (trả hết nợ trước hạn, đáo hạn). Có hai cách tiếp cận để xác suất hấp thụ có ý nghĩa cảnh báo sớm:

**(a) Bổ sung trạng thái hấp thụ thứ hai** "Trả hết nợ" (Prepaid/Matured). Khi đó $r = 2$, $R$ có hai cột, và $b_{i,\text{Default}}$ là xác suất khoản vay ở trạng thái $i$ cuối cùng vỡ nợ **trước khi** trả hết nợ — hai kết cục cạnh tranh (competing outcomes), và $b_{i,\text{Default}} + b_{i,\text{Prepaid}} = 1$.

**(b) Xác suất vỡ nợ trong kỳ hạn hữu hạn $H$ tháng.** Theo (2.16), xác suất bị hấp thụ trong vòng $H$ bước là

$$\mathrm{PD}_i(H) = \Big[\big(I + Q + \dots + Q^{H-1}\big) R\Big]_i = \Big[(I - Q^H)\, N R\Big]_i, \tag{2.19}$$

trong đó đẳng thức sau suy ra từ $\sum_{k=0}^{H-1} Q^k = (I - Q^H)(I - Q)^{-1}$. Công thức (2.19) liên kết trực tiếp ma trận cơ bản $N$, ma trận $R$ và phương trình Chapman–Kolmogorov, đồng thời cho ra đại lượng có thể so sánh với tỷ lệ vỡ nợ quan sát được trong một cửa sổ kiểm định có độ dài hữu hạn.

Báo cáo này chọn **phương án (a)** — bổ sung trạng thái hấp thụ thứ hai "Prepaid" — làm không gian trạng thái chính thức của mô hình (sáu trạng thái, xem mục 3.2.1), để $B = NR$ giữ nguyên dạng (2.18) và phản ánh đúng bản chất cạnh tranh giữa vỡ nợ và trả hết nợ, thay vì phải kiểm duyệt quỹ đạo. Công thức kỳ hạn hữu hạn (2.19) vẫn được dùng ở mục 4.5, nhưng áp dụng cho cột Default của $R$ (hai cột) thay vì cho một xích chỉ có một trạng thái hấp thụ.

## 2.6. Kiểm định giả thiết cho xích Markov

### 2.6.1. Nhắc lại về kiểm định tỷ số hợp lý và kiểm định $\chi^2$

Xét mô hình tham số với giả thuyết $H_0: \theta \in \Theta_0$ lồng trong $H_1: \theta \in \Theta_1$, $\Theta_0 \subset \Theta_1$. **Thống kê tỷ số hợp lý** là

$$\Lambda = -2 \ln \frac{\sup_{\theta \in \Theta_0} L(\theta)}{\sup_{\theta \in \Theta_1} L(\theta)} = 2\big(\hat{\ell}_1 - \hat{\ell}_0\big),$$

trong đó $\hat{\ell}_0, \hat{\ell}_1$ là log-hợp lý cực đại dưới $H_0$ và $H_1$. Theo **định lý Wilks**, dưới $H_0$ và các điều kiện chính quy, $\Lambda$ hội tụ theo phân phối về $\chi^2_{d}$ với $d = \dim \Theta_1 - \dim \Theta_0$. Bác bỏ $H_0$ ở mức ý nghĩa $\alpha$ nếu $\Lambda > \chi^2_{d, 1-\alpha}$ (phân vị mức $1 - \alpha$), hay tương đương p-value $= \mathbb{P}(\chi^2_d > \Lambda) < \alpha$. Thống kê **Pearson** $\chi^2 = \sum (O - E)^2 / E$ tương đương tiệm cận với $\Lambda$ và cùng phân phối giới hạn.

Với xích Markov, Anderson & Goodman (1957) và Billingsley (1961) đã chứng minh các kết quả tiệm cận này vẫn đúng khi số lần chuyển quan sát $n_i \to \infty$, dù các quan sát trong cùng một quỹ đạo không độc lập.

### 2.6.2. Kiểm định tính thuần nhất theo thời gian

Chia thời gian quan sát thành $G$ giai đoạn con $g = 1, \dots, G$ (ví dụ theo năm). Gọi $n_{ij}(g)$ là số lần chuyển từ $i$ sang $j$ xảy ra trong giai đoạn $g$, $n_i(g) = \sum_j n_{ij}(g)$, và $\hat{p}_{ij}(g) = n_{ij}(g)/n_i(g)$ là MLE riêng của giai đoạn $g$; $\hat{p}_{ij} = \sum_g n_{ij}(g) / \sum_g n_i(g)$ là MLE gộp.

- $H_0$: $p_{ij}(1) = p_{ij}(2) = \dots = p_{ij}(G) = p_{ij}$ với mọi $i, j$ (ma trận chuyển không đổi theo thời gian).
- $H_1$: tồn tại $i, j$ và $g \ne g'$ sao cho $p_{ij}(g) \ne p_{ij}(g')$.

Thống kê tỷ số hợp lý:

$$\Lambda_{\text{TN}} = 2 \sum_{g=1}^{G} \sum_{i} \sum_{j} n_{ij}(g) \ln \frac{\hat{p}_{ij}(g)}{\hat{p}_{ij}}, \tag{2.20}$$

hoặc dạng Pearson tương đương tiệm cận:

$$\chi^2_{\text{TN}} = \sum_{g=1}^{G} \sum_{i} \sum_{j} \frac{\big(n_{ij}(g) - n_i(g)\,\hat{p}_{ij}\big)^2}{n_i(g)\,\hat{p}_{ij}}, \tag{2.21}$$

với $n_i(g)\hat{p}_{ij}$ là số lần chuyển kỳ vọng trong giai đoạn $g$ nếu $H_0$ đúng. Tổng lấy trên các ô có $\hat{p}_{ij} > 0$ và bỏ qua hàng hấp thụ (hàng tất định). Dưới $H_0$, thống kê có phân phối xấp xỉ $\chi^2$ với bậc tự do

$$d_{\text{TN}} = (G - 1) \sum_{i \in \mathcal{T}} (c_i - 1), \tag{2.22}$$

trong đó $\mathcal{T}$ là tập trạng thái tạm thời và $c_i$ là số ô dương trong hàng $i$ của $\hat{P}$ (khi không có số không cấu trúc, $c_i = K$ và $d_{\text{TN}} = (G-1)\,s\,(K-1)$).

Kiểm định có thể thực hiện cho **toàn bộ** $G$ giai đoạn cùng lúc, và cho **từng cặp** giai đoạn ($G = 2$) để xác định giai đoạn nào khác biệt. Khi thực hiện nhiều kiểm định cặp, mức ý nghĩa cần được hiệu chỉnh (ví dụ hiệu chỉnh Bonferroni $\alpha / \text{số cặp}$) để kiểm soát sai lầm loại I tổng thể.

### 2.6.3. Kiểm định bậc của xích Markov

Xích Markov **bậc 2** cho phép trạng thái tương lai phụ thuộc vào hai trạng thái gần nhất:

$$p_{hij} = \mathbb{P}(S_{t+1} = j \mid S_t = i, S_{t-1} = h).$$

Với $n_{hij}$ là số bộ ba liên tiếp $(h, i, j)$ quan sát được và $n_{hi} = \sum_j n_{hij}$, MLE (lập luận tương tự mục 2.2.2) là $\hat{p}_{hij} = n_{hij} / n_{hi}$. Xích bậc 1 là trường hợp riêng khi $p_{hij} = p_{ij}$ với mọi $h$.

- $H_0$: xích là bậc 1, tức $p_{hij} = p_{ij}$ với mọi $h, i, j$.
- $H_1$: xích là bậc 2.

Thống kê tỷ số hợp lý (Anderson & Goodman, 1957):

$$\Lambda_{\text{bậc}} = 2 \sum_{h} \sum_{i} \sum_{j} n_{hij} \ln \frac{\hat{p}_{hij}}{\hat{p}_{ij}}, \qquad \hat{p}_{ij} = \frac{\sum_h n_{hij}}{\sum_h n_{hi}}, \tag{2.23}$$

trong đó $\hat{p}_{ij}$ được ước lượng **trên cùng tập bộ ba** để hai mô hình dùng chung dữ liệu. Dưới $H_0$, $\Lambda_{\text{bậc}}$ có phân phối xấp xỉ $\chi^2$ với bậc tự do

$$d_{\text{bậc}} = \sum_{i \in \mathcal{T}} (a_i - 1)(c_i - 1), \tag{2.24}$$

với $a_i$ là số trạng thái $h$ có $n_{hi} > 0$ (số "quá khứ" khác nhau dẫn đến $i$) và $c_i$ là số ô dương trong hàng $i$. Khi không có số không cấu trúc, $d_{\text{bậc}} = K(K-1)^2$ (Anderson & Goodman, 1957).

Diễn giải trong bối cảnh tín dụng: bác bỏ $H_0$ nghĩa là, chẳng hạn, một khoản vay đang ở 30 DPD sau khi vừa **phục hồi** từ 60 DPD có xác suất chuyển khác biệt đáng kể so với một khoản vay ở 30 DPD sau khi vừa **trượt** từ Current — tức "con đường" dẫn đến trạng thái hiện tại mang thông tin dự báo.

### 2.6.4. Lưu ý khi áp dụng trên cỡ mẫu lớn

Với hàng triệu lần chuyển, kiểm định có **lực rất lớn**: những khác biệt rất nhỏ, không có ý nghĩa thực tiễn, vẫn có thể dẫn đến bác bỏ $H_0$. Vì vậy, bên cạnh p-value, báo cáo đánh giá thêm **độ lớn của sai lệch** (ví dụ chuẩn Frobenius giữa các ma trận giai đoạn, hay chênh lệch tuyệt đối lớn nhất giữa các ô tương ứng) để phân biệt ý nghĩa thống kê với ý nghĩa thực tiễn. Ngoài ra, các kiểm định trên giả định các khoản vay độc lập với nhau; trong thực tế các khoản vay chịu chung cú sốc vĩ mô, nên kết quả cần được diễn giải thận trọng.

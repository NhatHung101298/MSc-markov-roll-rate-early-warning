# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Planning files — READ FIRST every session

Before doing anything, read both:
- `plans/master_plan.md` — bức tranh tổng của cả dự án: mục tiêu, kế hoạch 6 buổi, Definition of Done, ràng buộc phạm vi.
- `plans/active_plan.md` — buổi / bước ĐANG làm, checklist hiện tại, blocker, việc chờ HUNG quyết định.

Also relevant:
- `plans/logs.md` — nhật ký thời gian thực: quyết định của HUNG, thay đổi phạm vi, kết quả kiểm tra artifact, tiến độ làm report. Ghi 1 entry mỗi khi có quyết định, xong 1 task, hoặc phát hiện rủi ro/phạm vi.

Khi xong 1 buổi: cập nhật `active_plan.md` (chép checklist buổi kế từ `master_plan.md`), ghi 1 dòng vào `logs.md`. `master_plan.md` chỉ sửa khi phạm vi hoặc thứ tự buổi thay đổi. `PROJECT_BRIEF.md` vẫn là spec gốc — đọc full trước khi code.

## Project status

No implementation code exists yet. The repo currently contains only:
- `PROJECT_BRIEF.md` — the full spec for this project (read it in full before writing any code)
- `plans/` — master plan, active plan, logs (xem phần trên)
- `docs/` — reference materials, including `10_de_tai_du_an_ngan_hang_data_science.md` (a *different*, unrelated list of future thesis topic ideas — do not treat it as scope for this project)
- `stochastic/` — an empty Python 3.11 venv (no packages installed yet)

When code is added, expect it to land under directories like `scripts/`, `data/`, `outputs/` per the user's global conventions (see `~/.claude/CLAUDE.md`) — but nothing has been created yet, so don't assume a structure exists until you check.

## What this project is

Final assignment (not a thesis) for **MAT6206 — Các phương pháp ngẫu nhiên và ứng dụng** (Master of Data Science, VNU-HUS). Builds a discrete-time, finite-state Markov chain roll-rate model for early warning of loan default, using the Freddie Mac Single-Family Loan-Level Dataset (fallback: Kaggle "American Express Default Prediction").

Estimated scope: ~6 work sessions. **Read `PROJECT_BRIEF.md` in full before implementing anything** — it is the authoritative spec. Key points to hold onto:

- **States (6, two absorbing):** `Current (0) → 30 DPD → 60 DPD → 90+ DPD` are transient; `Default/Foreclosure` and `Prepaid` (paid off early/matured) are both absorbing. Decided 2026-09-22 (see `plans/logs.md`): a single-absorbing-state chain makes `B=NR=1` for every starting state (mathematically correct but useless for the §4.5 backtest), so a second absorbing state "Prepaid" was added — `R` has two columns, `B` gives competing-risk probabilities (default vs. prepay) that differ meaningfully by starting state.
- **Split by time, not randomly** — e.g. first 80% of periods for parameter estimation, last 20% for validation/backtesting. This is loan-level time-series data.
- **Must implement the Markov math by hand** (transition matrix MLE, Chapman–Kolmogorov, stationary distribution, fundamental matrix `N=(I-Q)^-1`, absorption probabilities `B=NR`) using `pandas`/`numpy`/`scipy.stats` only.
- **Do not use** `hmmlearn`, `lifelines`, `scikit-survival`, or any HMM/survival/hazard library — that is explicitly out of scope for this assignment (see brief §6).
- Two required hypothesis tests: time-homogeneity of the transition matrix across sub-periods (χ²), and Markov order 1 vs 2 (likelihood ratio test). Both need explicit accept/reject conclusions, not just a printed statistic.
- §4.5 (comparing predicted absorption probabilities against *actual observed* default rates on the validation set) is a mandatory backtest step — never skip or stub it out.
- Final report: Vietnamese, LaTeX-annotated formulas, Markdown/HTML output.

## Scope discipline (important)

`PROJECT_BRIEF.md` §6 lists explicit non-goals: no HMM/Baum-Welch/Viterbi, no Cox PH / discrete-time hazard / survival analysis, no multistate/semi-Markov regression, no ML model comparison (Random Survival Forest, XGBoost-AFT), no trading-style backtest strategy, no customer-segment-level transition matrices, no bootstrap confidence intervals for π or B — unless the user explicitly asks for one of these. If an extension seems like a good idea mid-implementation, stop and ask before adding it rather than expanding scope silently.

## Coding conventions — ngôn ngữ docstring/comment

- Tên biến/hàm/file: tiếng Anh (theo `~/.claude/CLAUDE.md`).
- **Docstring và comment trong code: tiếng Việt có dấu đầy đủ** (không viết tiếng Việt không dấu kiểu "cong thuc", "tra ve"). Lý do: tránh lỗi encoding dấu tiếng Việt lẫn code review khó đọc — đã xảy ra ở Phase 0 (`scripts/utils/markov.py`, sửa lại 2026-09-22).
- Docstring hàm Markov nên nối lại đúng số công thức Ch.2 (`PROJECT_BRIEF.md`/báo cáo), ví dụ: `"""p_hat_ij = n_ij / sum_k n_ik -- công thức (2.10)."""`.
- Trước khi commit code mới: rà lại docstring/comment xem còn sót tiếng Việt không dấu không.

## Environment

- `stochastic/` is a Python 3.11 venv, currently empty (no packages installed). Activate with `stochastic\Scripts\activate` (PowerShell: `stochastic\Scripts\Activate.ps1`) before installing/running anything.
- Expected libraries per the brief: `pandas`, `numpy`, `scipy`, `matplotlib`/`seaborn` — none are installed yet, so `pip install` will be needed before first run.

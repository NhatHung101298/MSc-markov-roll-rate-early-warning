# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

No implementation code exists yet. The repo currently contains only:
- `PROJECT_BRIEF.md` — the full spec for this project (read it in full before writing any code)
- `docs/` — reference materials, including `10_de_tai_du_an_ngan_hang_data_science.md` (a *different*, unrelated list of future thesis topic ideas — do not treat it as scope for this project)
- `stochastic/` — an empty Python 3.11 venv (no packages installed yet)

When code is added, expect it to land under directories like `scripts/`, `data/`, `outputs/` per the user's global conventions (see `~/.claude/CLAUDE.md`) — but nothing has been created yet, so don't assume a structure exists until you check.

## What this project is

Final assignment (not a thesis) for **MAT6206 — Các phương pháp ngẫu nhiên và ứng dụng** (Master of Data Science, VNU-HUS). Builds a discrete-time, finite-state Markov chain roll-rate model for early warning of loan default, using the Freddie Mac Single-Family Loan-Level Dataset (fallback: Kaggle "American Express Default Prediction").

Estimated scope: ~6 work sessions. **Read `PROJECT_BRIEF.md` in full before implementing anything** — it is the authoritative spec. Key points to hold onto:

- **States (5, absorbing at the end):** `Current (0) → 30 DPD → 60 DPD → 90+ DPD → Default/Foreclosure`. Default/Foreclosure is absorbing.
- **Split by time, not randomly** — e.g. first 80% of periods for parameter estimation, last 20% for validation/backtesting. This is loan-level time-series data.
- **Must implement the Markov math by hand** (transition matrix MLE, Chapman–Kolmogorov, stationary distribution, fundamental matrix `N=(I-Q)^-1`, absorption probabilities `B=NR`) using `pandas`/`numpy`/`scipy.stats` only.
- **Do not use** `hmmlearn`, `lifelines`, `scikit-survival`, or any HMM/survival/hazard library — that is explicitly out of scope for this assignment (see brief §6).
- Two required hypothesis tests: time-homogeneity of the transition matrix across sub-periods (χ²), and Markov order 1 vs 2 (likelihood ratio test). Both need explicit accept/reject conclusions, not just a printed statistic.
- §4.5 (comparing predicted absorption probabilities against *actual observed* default rates on the validation set) is a mandatory backtest step — never skip or stub it out.
- Final report: Vietnamese, LaTeX-annotated formulas, Markdown/HTML output.

## Scope discipline (important)

`PROJECT_BRIEF.md` §6 lists explicit non-goals: no HMM/Baum-Welch/Viterbi, no Cox PH / discrete-time hazard / survival analysis, no multistate/semi-Markov regression, no ML model comparison (Random Survival Forest, XGBoost-AFT), no trading-style backtest strategy, no customer-segment-level transition matrices, no bootstrap confidence intervals for π or B — unless the user explicitly asks for one of these. If an extension seems like a good idea mid-implementation, stop and ask before adding it rather than expanding scope silently.

## Environment

- `stochastic/` is a Python 3.11 venv, currently empty (no packages installed). Activate with `stochastic\Scripts\activate` (PowerShell: `stochastic\Scripts\Activate.ps1`) before installing/running anything.
- Expected libraries per the brief: `pandas`, `numpy`, `scipy`, `matplotlib`/`seaborn` — none are installed yet, so `pip install` will be needed before first run.

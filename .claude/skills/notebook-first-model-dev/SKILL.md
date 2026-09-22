---
name: notebook-first-model-dev
description: Use when about to write, smoke-test, run full, or "freeze" a scripts/0X_*.ipynb pipeline step for this Markov roll-rate model (Phase 1 onward — ETL, estimation, hypothesis tests, stationary/absorption, backtest) — before running it beyond a small SUFFIX="smoke" run, and before marking any such notebook's output as final.
---

# Notebook-first Model Dev

## Overview

Pipeline scripts in this project (Phase 1+ of `master_plan.md` §6) pass through three states — **DRAFT → REVIEWED → FROZEN** — and Claude never advances a notebook past REVIEWED on its own. HUNG must physically open the file and explore it by hand before it becomes official. This exists because he cannot verify a Markov model pipeline by reading a final summary alone — he needs to see intermediate data, the way a notebook would show it, at a point where he can still change course.

**Format decision (2026-09-22):** pipeline steps are real Jupyter notebooks (`.ipynb`), not `.py` files with `# %%` cell markers — HUNG found the `# %%` script format hard to read and hard to work through interactively. This applies from Phase 2 onward; Phase 1's `.py` scripts were not converted retroactively.

**Not for:** `scripts/utils/markov.py`, `scripts/utils/transitions.py` (pure formulas/data-transform helpers, each has its own unit-style smoke test), `report/report.ipynb` (separate deliverable, not a pipeline step).

## The three states (same file, one path: `scripts/0X_ten_phase.ipynb`)

| State | What it means | Who acts |
|---|---|---|
| DRAFT | Notebook written with a plain variable (e.g. `SUFFIX = "smoke"`) instead of CLI args — a notebook has no argv — split per logical step | Claude writes |
| REVIEWED | Claude ran the notebook with `SUFFIX = "smoke"` (small data), reported the summary, then **stopped** | Claude runs smoke pass, then stops |
| FROZEN | Exploratory/debug cells removed, `SUFFIX` switched to `"full"` and executed, artifact checked, `logs.md` updated | Claude does this only after HUNG says so |

Claude runs a notebook headlessly with `jupyter nbconvert --to notebook --execute --inplace scripts/0X_ten_phase.ipynb` (venv: `stochastic\Scripts\python.exe -m jupyter nbconvert ...`) so real cell outputs (tables, plots) are saved into the `.ipynb` file itself — HUNG then opens it in VS Code and sees actual output, not just console text.

## Required cell structure (DRAFT/REVIEWED)

Load input → one cell per logical transform step → an inspection cell after each important transform (`.shape`, `.value_counts()`, head rows, plots) → save artifact. **Last cell, mandatory, markdown:** `Quyết định: ... / Lý do: ...` — even when the phase is purely mechanical (e.g. MLE formula), write `Quyết định: Không có quyết định chủ quan ở bước này`. Never leave this cell out or blank. REVIEWED → FROZEN is blocked without it; if missing, tell HUNG instead of freezing anyway.

## Hard gate: no auto-escalation past REVIEWED

**Silence is not consent. There is no timeout that turns into permission.** After reporting the smoke-test summary, stop completely — do not run full data, do not strip `# %%`, do not start the next phase — regardless of Auto Mode, deadline pressure, or how cleanly the last N phases went.

| Rationalization | Reality |
|---|---|
| "HUNG chưa trả lời, chờ 20–30 phút rồi tự chạy `SUFFIX=\"full\"`, ghi lại giả định trong log" | Self-imposed timeout is still Claude deciding on HUNG's behalf. Waiting doesn't create consent; only HUNG's own message does. |
| "Deadline gấp tối nay, chạy full trước rồi review sau cho kịp" | The gate exists *because* of judgment calls under pressure — pressure is not a reason to skip it, it is the exact scenario the gate is for. |
| "Smoke test sạch quá, chắc không có gì để khai phá" | A clean smoke test on `--limit` data says nothing about full-scale behavior (memory, edge-case states, rare transitions) — that's the point of letting HUNG look. |
| "Auto Mode đang bật, nguyên tắc là cứ làm tiếp" | Auto Mode governs *clarifying questions*, not this project's explicit REVIEWED→FROZEN gate — a deliberate, narrower boundary HUNG set for this workflow, stricter than default Auto Mode. |
| "2 phase trước chạy trơn tru, phase này chắc cũng vậy" | Each phase's REVIEWED gate is independent; past smoothness isn't evidence for this phase's correctness. |

## What to do instead while waiting

Keep working on anything that does **not** advance this script past REVIEWED: draft the report chapter skeleton for this phase, prep the next phase's DRAFT cells if the design is already settled, or read back other project files. Send one clear status message once (smoke test summary + what's needed from HUNG) — do not re-send or nudge on a timer.

## Freezing (only after HUNG signals — no fixed keyword required)

1. Re-read the file — HUNG may have edited it by hand.
2. Verify the `Quyết định/Lý do` cell exists; if not, stop and ask.
3. Remove exploratory/debug cells not needed for the pipeline.
4. Switch `SUFFIX` to `"full"`, run via `jupyter nbconvert --to notebook --execute --inplace`, check artifact (schema, row counts, sane values).
5. Write the `logs.md` entry **from the `Quyết định/Lý do` cell content directly** — don't re-derive it from memory, to avoid drifting from what HUNG actually approved.
6. If that content is a methodology decision, run result, or conclusion, sync it into the matching chapter in `outputs/TranNhatHung_MAT6206_BaoCaoCuoiKy/noi_dung_chi_tiet/` per the existing CLAUDE.md rule — same turn, not deferred.

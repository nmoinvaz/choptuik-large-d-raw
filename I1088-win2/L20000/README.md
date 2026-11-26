# I1088-win2/L20000: D 20000 held at L = 20, direct solve (#1088)

Machine win2 (Windows 11, Core Ultra 7 265K, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1088. Written 2026-11-26 02:56 UTC, **before the run**. **The run starts only on the coordinator's word "A" or "B".**

## Order (coordinator t5, hc, 26 Nov ~02:55 UTC), verbatim
"#1088, win2's solve is D 2x10^4. Prepare it now; START ONLY ON MY WORD "A" or "B" (expected ~04:00 UTC, after the D 10^4 ks check).
1. The build worktree at 1ccd32ab or later (Python-only changes since ab2446b8: check the diff of hp/src, the Cargo files, pyproject and build.sh as you did; if Rust changed, say so before running).
2. Make RAW/I1088-win2/L20000/ with a README.md whose first line is "# I1088-win2/L20000: D 20000 held at L = 20, direct solve (#1088)", then the machine and the issue URL, and both commands below verbatim. The guess is RAW/I1088-mac-a/form_s/g20000L20/guess_D20000.0000.npz (raw f922c922; fetch, pin by blob, copy into the folder, point --state at the copy).
3. From hp/, with OPENBLAS_NUM_THREADS=1 (the AGENTS.md Windows rule; J is only 577x577), through WMI, BelowNormal, cap 12 h by exact pid:
A: python -u form_s_lastnode.py solvestate RAW/I1088-win2/L20000 --state <copy> --ks 11416 --threads 16 --ladder dd,qd --it_max 2 --it_hi 2 --chord 1 --step_est 5400,900 --delta_tol 1e-15 --tc 1.64441243858130260:1.77e-9 --commit 1ccd32ab > RAW/I1088-win2/L20000/lastnode.log 2>&1
B: the same with --ks 26018 --step_est 7200,3000
4. Bars, written before the run:
   - Delta's first-order bound <= 1e-15;
   - the tails at the solved state (ks + 200, kc + 20, halved steps) each <= 1e-25, and theta's top harmonic reported;
   - Track C 1.64441243858 +- 1.77e-9 printed. Expect about -8e-10, as the held values at D 2000-10^4 sat 5-8e-10 below; outside +-1.77e-9 gets reported.
5. Read the log at each step's predicted end yourself and send me each step's line. Push from a separate raw worktree."

## Set-up
| item | value |
|---|---|
| the guess | `I1088-mac-a/form_s/g20000L20/guess_D20000.0000.npz` at raw commit f922c922 (an ancestor of the raw repo's origin/main f1c07c241; the macOS runner's `guess.log`: D 20000, x_l 0.706753, ks 11416, 2659 Taylor steps, the guess's max \|F\| per block 1.6e-12 1.9e-12 3.4e-12 5.7e-12 1.0e-11 4.0e-11 5.1e-18, horizon over largest other 3.841, 45 s). Read with `git show f922c922:<path>` from the push worktree, **copied into this folder** as `guess_D20000.0000.npz`, 255,350 bytes, **blob 1f63b72b** (= `git rev-parse f922c922:<path>` = 1f63b72bbfb3d3fde0d94450031af328064b3aec); `--state` points at this copy. `guess_mac.log` is the Mac's log. The driver refuses any other blob. |
| code | `D:\choptuik-formsq` (detached) at origin/wip/large-d-form-s **1ccd32ab** (the head now; the commits since the build's ab2446b8: 7bf304b1 and 4f5eaf69 and 1ccd32ab, `hp/form_s.py` and `hp/form_s_lastnode.py` only: 34 insertions and 12 deletions). **No Rust change:** `git diff --stat ab2446b8 1ccd32ab -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml hp/build.sh` is empty (the driver checks it before the checkout), so the hpkernel built at ab2446b8 in `venv-formsq` stays valid. The worktree is at ab2446b8 until the run starts (the form-S selftests of the build run on ab2446b8). |
| variants | **A**: `--ks 11416 --step_est 5400,900` (the guess's own ks). **B**: `--ks 26018 --step_est 7200,3000`. Same flags otherwise. `OUTDIR` is the order's `RAW/I1088-win2/L20000` for both, so a second variant needs the first's files moved into a subfolder first (the driver refuses when `lastnode.log` exists). |
| command run | the order's A or B, with `RAW/I1088-win2/L20000` = `D:/choptuik-i935-raw/I1088-win2/L20000` and `<copy>` = `D:/choptuik-i935-raw/I1088-win2/L20000/guess_D20000.0000.npz`, `--commit 1ccd32ab`; `OPENBLAS_NUM_THREADS=1` (also `PYTHONDONTWRITEBYTECODE=1`, `PYTHONFAULTHANDLER=1`); from `D:\choptuik-formsq\hp` with venv-formsq's python; started through `kc71_leap/cim_start.ps1` (WMI), BelowNormal, cap 43,200 s (12 h) by the exact root pid (`crun`, which kills the tree only after a command-line check); stdout and stderr into `lastnode.log`, whose first line is the exact command. |
| driver | `run_L20000.sh A|B` (DRY=1: the pins and the state of the build and selftests only) |

## Gates (before the word is acted on)
The driver refuses unless (1) the guess is blob 1f63b72b, (2) `checks_gate.py` is blob 72ece674 and its own selftest reads 0 (registered readings pass, each of five broken cases is refused) and `--mutate` 1, (3) the hp build ended with exit 0 (`hp_form_s_build/build.times`), (4) the form-S selftests finished (`checks.done`) and read as registered (`checks_gate.py`: `floor_stop_check.py` PASS, `--stale` PASS, `--mutate=nofloor` fails, `form_s.py check` converged with |Delta_S - Delta_A| <= 1e-20, its `--mutate flux` control moved Delta; the readings were written in `hp_form_s_build/README.md` before they ran), (5) hp/src and the Cargo files are unchanged between ab2446b8 and 1ccd32ab. Dry run 02:55 UTC: pins ok, gate selftest 0 and 1, **the build has not exited yet** (compiling `hpkernel`, 1 h 46 min in at 02:55 UTC, rustc 36.8 GB, commit headroom 1.0 GB, no failure), so a start now would be refused.

## Readings and bars (the coordinator's, fixed before the run)
- **Delta's first-order bound <= 1e-15** (`--delta_tol 1e-15`).
- **The tails at the solved state** (ks + 200, kc + 20, halved steps) **each <= 1e-25**, and **theta's top harmonic** reported (the script's discretization-tails report).
- **Track C 1.64441243858 +- 1.77e-9 printed** (`--tc 1.64441243858130260:1.77e-9`, the error the coordinator's given figure, not an enclosure). **Expected Delta - Track C about -8e-10** (the held values at D 2000 to 10^4 sat 5 to 8e-10 below); a value outside +-1.77e-9 is reported.
- Stop rules built in: at most 2 dd steps and 2 qd chord steps (`--it_max 2 --it_hi 2`), floor stop, then the od check, the discretization tails and the Hamiltonian check; `direct_s.jsonl` only if converged. Each step prints its start and predicted end; I read the log at each step's predicted end and send each step's line to the coordinator.
- Times from a clock (`date -u`), never guessed; the memory of the solve is small (J is 577 x 577); the commit headroom matters only while the build runs.

## Status
- 2026-11-26 02:56 UTC: folder, README, driver and the pinned guess written; the driver passes its dry run. Nothing computes. Waiting for the build (compiling) and its selftests, then for the coordinator's "A" or "B".
- 2026-11-26 03:38 UTC: **MOVED to the Mac mini, no run on win2.** The coordinator (hc ~03:38 UTC): "D 2x10^4 moves to the Mac mini (4-5x faster per step, free after its D 8000 checks); disarm your L20000 driver by exact pid (keep the folder, note the move). Let the build finish; your next solve is decided when it ends (likely a release or D 5x10^4)." The driver `run_L20000.sh` was never started (it runs only on the coordinator's word A or B), so there was no process to stop: the process table at 03:37 UTC holds no `run_L20000.sh`, no `L20000.cmd` and no `form_s_lastnode.py`; there is no `lastnode.log`, no `L20000.done`, no checkout of 1ccd32ab (the build worktree stays at ab2446b8). The folder keeps the pinned guess (blob 1f63b72b), the driver and the gate for the record.

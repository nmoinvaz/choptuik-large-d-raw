# I1088-win2/L8000: D 8000 held at L = 20, direct solve (#1088)

Machine win2 (Windows 11, Core Ultra 7 265K, 20 logical CPUs, 95.5 GB RAM; runner win2 claude-me2, Sonnet 5.5). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1088. Written 2026-11-26 01:36 UTC, **before the run**.

## Order (coordinator t5, hc, 26 Nov ~01:30 UTC), verbatim
"#1088 (the quest), queued after your hp build and its selftests pass: D 8000 by direct solve.
1. In the build worktree D:\choptuik-formsq, check out origin/wip/large-d-form-s at 4f5eaf69 or later. It changes only Python files since your build's ab2446b8 (no hp/src or Cargo changes), so keep the built hpkernel.
2. Make RAW/I1088-win2/L8000/ (RAW = your raw clone) with a README.md whose first line is "# I1088-win2/L8000: D 8000 held at L = 20, direct solve (#1088)", then the machine and https://github.com/nmoinvaz/choptuik-large-d/issues/1088. The guess is RAW/I1088-mac-a/form_s/g8000L20/guess_D8000.0000.npz (raw 7c2b9983; fetch, pin by blob).
3. From hp/, with OPENBLAS_NUM_THREADS=2, started through WMI, BelowNormal, cap 8 h:
python -u form_s_lastnode.py solvestate RAW/I1088-win2/L8000 --state RAW/I1088-mac-a/form_s/g8000L20/guess_D8000.0000.npz --threads 16 --ladder dd,qd --it_max 2 --it_hi 2 --chord 1 --step_est 3000,600 --delta_tol 1e-15 --tc 1.64519021245138076:1.66e-9 --commit 4f5eaf69 > RAW/I1088-win2/L8000/lastnode.log 2>&1
4. Stop rules are built in (at most 2 dd steps and 2 qd chord steps, floor stop, then the od check, discretization tails and the Hamiltonian check; the direct_s.jsonl record only if converged). Each step prints its start and predicted end. Expect 3-4 h in all.
5. Report each step's line. The bar, written before the run: Delta's first-order bound <= 1e-15. Delta against Track C 1.64519021245 +- 1.66e-9 is printed.
6. Push from a separate worktree of the raw clone while the job writes into the live folder.
The precision check stays stopped until D 8000 ends."

## Set-up
| item | value |
|---|---|
| raw clone | `D:\choptuik-i935-raw` (my live raw worktree; the folder is `I1088-win2/L8000/`); pushes from `D:/choptuik-large-d-raw-743p` through `kc71_leap/push_dir.sh` (a separate worktree) |
| the guess | `RAW/I1088-mac-a/form_s/g8000L20/guess_D8000.0000.npz` at the raw repo's origin/main 7c2b99835 (the macOS runner's `guess.log`: D 8000, x_l 0.706222, ks 10418, 1099 Taylor steps, the guess's max \|F\| per block 2.9e-12 3.5e-12 6.2e-12 1.0e-11 1.9e-11 7.1e-11 1.7e-18, horizon over largest other 3.783). Read with `git show origin/main:<path>` from the push worktree (my live clone is not pulled) and **copied into this folder** as `guess_D8000.0000.npz`, 129,766 bytes, **blob 2c59ff47** = the raw repo's blob (`git ls-tree` 2c59ff47d694728c930b92f94578f1faf06936c2); `--state` points at this copy. The driver refuses any other blob. `guess_mac.log` is the Mac's log of the guess. |
| code | `D:\choptuik-formsq` (detached) at origin/wip/large-d-form-s **4f5eaf69** (the head on 26 Nov ~01:30 UTC; two commits since the build's ab2446b8: `form_s.py` 20 lines and `form_s_lastnode.py` 9 lines; `git diff ab2446b8 4f5eaf69 -- hp/src hp/Cargo.toml hp/Cargo.lock hp/pyproject.toml hp/build.sh` is empty, which the driver checks), the hpkernel built at ab2446b8 in `venv-formsq` (`../../I1025-win2/hp_form_s_build/`) |
| command | the order's, with `$WOUT` = `D:/choptuik-i935-raw/I1088-win2/L8000` for RAW's folder and the guess's copy for `--state`; `OPENBLAS_NUM_THREADS=2`, `PYTHONDONTWRITEBYTECODE=1`; started through `kc71_leap/cim_start.ps1` (WMI, BelowNormal), cap 28,800 s (8 h) by the exact root pid (`crun`, which kills the tree only after a command-line check); stdout and stderr into `lastnode.log` |
| driver | `run_L8000.sh` |

## When it starts (the queue), and what gates it
The order queues D 8000 **after the hp build and its selftests pass**. The build (started 01:09 UTC) is at its LTO peak (36.6 GB, commit headroom 1.2 GB at 01:35 UTC), the selftest chain `run_formsq_checks.sh` waits for it. `run_L8000.sh` waits for `hp_form_s_build/checks.done`, then reads the five selftests with **`checks_gate.py`** (blob 72ece674; the readings registered in `hp_form_s_build/README.md` before they ran: `floor_stop_check.py` exit 0 and PASS, `--stale` exit 0 and PASS, `--mutate=nofloor` non-zero and FAIL, `form_s.py check` converged with |Delta_S - Delta_A| <= 1e-20, and its `--mutate flux` control not converged or |diff| >= 1e-12). The gate has its own selftest (planted logs: the registered readings pass, each of the five broken once is refused; `--mutate` makes it accept everything and the selftest then exits 1; dry run 01:35 UTC: 0 and 1). If a reading is not as registered, the driver does **not** start D 8000, writes `L8000_refused.txt` and I report it. It then checks out 4f5eaf69 (after the selftests, which run on ab2446b8) and starts the solve. The memory of the solve is small (577 unknowns), the commit headroom matters only while the build runs.

## Readings and bar (the coordinator's, fixed before the run)
- The bar: **Delta's first-order bound <= 1e-15** (`--delta_tol 1e-15`). Delta against Track C 1.64519021245 +- 1.66e-9 is printed by the script (`--tc`).
- Stop rules built in: at most 2 dd steps and 2 qd chord steps (`--it_max 2 --it_hi 2`), floor stop, then the od check, the discretization tails and the Hamiltonian check; `direct_s.jsonl` is written only if converged.
- Each step's line (its start and predicted end, then its result) is reported as it lands. Expected 3-4 h in all (the coordinator).
- Error bars named: Track C's 1.66e-9 is the coordinator's given figure (`--tc ... source given`); nothing here is an enclosure.

## Status
- 2026-11-26 01:36 UTC: folder, README, driver, gate and the pinned guess written; the driver (waiting for the selftests) starts next. Nothing computes yet.
- 2026-11-26 02:52 UTC: **CANCELLED, no run on win2.** The coordinator (hc ~02:50 UTC): "change of plan: D 8000 moved to the new Mac mini, which built in 21 min and starts it now. Cancel your queued D 8000 driver by exact pid (keep the folder and README; note the move). After your build and its selftests pass, report and wait: your solve will be D 2x10^4 or 5x10^4, from a guess the quest subagent is preparing." The waiting driver was stopped after command-line checks: `taskkill /T /F` on bash 62244 (`run_L8000.sh`) at 02:52:0x UTC and on the launcher conhost 57624 (tree: cmd 55392, bash 58124, 37936). Nothing had been computed: no `lastnode.log`, no `L8000.done`, no `direct_s.jsonl`, the checkout of 4f5eaf69 had not been made (the driver was still waiting for `hp_form_s_build/checks.done`; the build worktree stays at ab2446b8). The D 8000 result is the Mac mini's, not here. The folder keeps its pinned guess (blob 2c59ff47), the driver and the gate script for the record; the selftest chain of the build (`run_formsq_checks.sh`) is still waiting for the build and is unaffected.

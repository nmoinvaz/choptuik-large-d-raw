# I1098-mm5/m48_1000: D 1000 harmonics 17-23 re-released at M 48 (#1098)

Machine: macmini-m5-pro (Apple M5 Pro, 18 cores, 48 GB, macOS 27.2.1), runner `choptuik-mm5-i1088-me2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1098

The jump agent's M 48 test at D 1000, queued by coordinator t5 to start the moment `../kfree1000od/` ends (its 9 threads; L50000 keeps its
own). Purpose: decide whether D 1000's harmonic tail stalling near 1e-20 (h19 +1.13137e-20 in od and qd, h21 +1.4329e-20 in qd) is M 32's
angular truncation or real. At D 300, M 48 moved Delta by only -7.6e-25.

## The bar, written by the jump agent before the run (relayed by the coordinator; recorded here 2026-11-26 10:40 UTC, before the run)

If M 32 drives the stall, h21 and h23 at M 48 fall well below 1e-20 (as D 300's fell to 3.7e-21, then 5e-24), and the h17 step's shift
(M 32 -> 48 with harmonics up to 17 free) is about 1e-20 or more. If they stay near 1e-20, the tail is real and M is not the cause.

Reported beside M 32's (kfree1000od, od residual, from the same h17 state): the h17 step's Delta shift, and each harmonic's change.
Stop and report on an exception, or an outer step 3x past the first one's time. Each outer step should take about 3-4x the M 32 one,
roughly 15 min; about 1.5 h in all.

## Inputs and code

- `input/release_ls_h17_D1000.0000.npz`: git blob 884f4df86701ba198d5745881250a4097013df7a (verified), the h17 state of `../kfree1000qd/`
  (M 32; Delta 1.654240854145891722271520081395140087424).
- `tools/resample_m.py`: git blob 4de5c3174ad1bad3a5a311f909db9d3ecec64b5b from `I1098-mac-a/` of this repository (verified); its
  hard-coded `sys.path.insert` path does not exist on this machine, so hp/ goes on PYTHONPATH.
- Kernel: the relaxed-horizon release build in `~/Source/fastmul3-site` (../fastmul3-build/, 34ca1745; form S at M 48 instantiated by
  b9a2954b, which it contains), `HP_HORIZON_RELAXED=1`.
- **form_s.py**: fastmul3's copy (34ca1745) does **not** have the qq acceptance fix (dfccf920, "accept a qq trial whose inner solve stopped
  far below the target") nor 3c2af3dd (the kernel recorded in each direct record). A wholesale copy of form_s.py from
  wip/large-d-form-s at dfccf920 would drop fastmul3's `HP_HORIZON_RELAXED` hook (`set_horizon_relaxed`), so the run would not use the
  relaxed sums. So a new worktree `~/Source/choptuik-m48` (leaving `~/Source/choptuik-fastmul3`, which kfree1000od still runs from, as it is)
  holds 34ca1745 with 3c2af3dd and dfccf920 cherry-picked (clean, local commits 31f90e12 and c263c636; form_s.py is the only file
  they touch). Both the relaxed hook (line 71) and the qq fix (line 1296) are in its form_s.py. The records' `--commit` is dfccf920, as ordered.
- Steps, from `~/Source/choptuik-m48/hp`, `~/venv-314`'s python, nice 10, detached, `timeout 4h` on the release, 9 threads:

      PYTHONPATH=~/Source/fastmul3-site:~/Source/choptuik-m48/hp python tools/resample_m.py input/release_ls_h17_D1000.0000.npz h17_M48.npz 48
      PYTHONPATH=~/Source/fastmul3-site HP_HORIZON_RELAXED=1 python -u form_s.py release_ls h17_M48.npz <this folder> --harm 17,19,21,23 --kmax 31 \
        --jac_by 17:qq,19:qq,21:qq,23:qq --res od --tol 1e-48 --tol_h 1e-44 --threads 9 --outer 6 --commit dfccf920 > rls.log

The queue script waits for kfree1000od's python (pid 21327) to exit, then runs both. Delta's change per harmonic is computed by `diff_delta.py`
on the log's digits (mpmath), never by hand.

## Results (2026-11-26 11:48 UTC)

Started 10:47:43 UTC, ended 11:42:02 UTC (54 min; `queue.txt`: resample exit 0, release_ls exit 0). The log's first line shows the kernel: `hpkernel /Users/nathan/Source/fastmul3-site/hpkernel/__init__.py HP_HORIZON_RELAXED 1` (fastmul3's build; form S at M 48 is in it). All numbers below are by script from the logs' digits (mpmath, 50 digits); the M 32 values are from `../kfree1000od/` (h19, h21; od).

| harmonic | M 48: outer steps, change in Delta (time) | M 32 (od) | M 48 / M 32 |
|---|---|---|---|
| h17 (shift M 32 -> 48, from the M 32 h17 state) | outer 0 -1.9684e-25 (347 s), outer 1 +1.3884e-19 (452 s), outer 2 -1.7856e-22 (324 s), outer 3 released; total **+1.38661e-19** | (the M 32 state itself) | |
| h19 | outer 0 +1.2092e-19 (537 s), outer 1 released | +1.13137e-20 | 10.7 |
| h21 | outer 0 -3.4847e-21 (645 s), outer 1 released | +1.43289e-20 (the stall) | -0.24 |
| h23 | outer 0 -1.5134e-21 (534 s): **the inner solve converged** (|F| 8.56e-49); outer 1 released | floor: the inner solve stopped at 1.71e-40 against 2.77e-46 | |

- Delta after h23 at M 48: 1.654240854145891722526108246523219277594. Delta after h21, M 48 minus M 32: +2.3046e-19.
- Against the bar (the jump agent's): h21 and h23 fall below 1e-20 at M 48 (h21 -3.5e-21, h23 -1.5e-21) and the h17 shift is 1.4e-19, above 1e-20: the case in which M 32 drives the stall.
  h19 at M 48 is +1.2e-19, larger than at M 32, which neither case of the bar expected.
- The h23 inner stall is the system's at M 32 (the same floor in od and qd), and it disappears at M 48.
- Files: `rls.log`, `release_ls.jsonl`, `release_ls_h<k>_D1000.0000.npz` (the state after each harmonic), `h17_M48.npz`, `resample.log`, `queue.txt`, `diff_delta.py`.

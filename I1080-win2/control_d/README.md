# I1080-win2/control_d: the control walk d on win2 (zero_mp.py M = 5 from the fundamental's M = 3 zero), dh370's command

Machine win2 (Windows 11, Intel Core Ultra 7 265K, 20 logical cores, shared with other runners). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1080. Order by hc from the coordinator t5, 2026-11-25 about 10:13 UTC: run the same control walk as dh370's walk d (raw `I1080-dh370/README.md`, step 2) on win2, 3 processes, BelowNormal, started by WMI, cap 24 h. Whichever of the two walks finishes first counts. This README is written before the run.

## Command

From `solver/inner_stokes` of a detached worktree `D:\choptuik-i1080d` at feat/inner-mp **73dcf243** (the commit of dh370's walk d), venv `C:\Users\nathan\source\venv-i962` (Python 3.14.10, mpmath 1.3.0, python backend, no gmpy2, as dh370's):

    python -u zero_mp.py 2.726475885672135 1.0156030949093042 - control_d/control_walk_d.jsonl --M=5 --v0=0.14617320927726193,0.014239435701575993,0.008040315603426431,0.0013895510043319215 --procs=3 --iters=8

The only change from dh370's command is `--procs=3` (it used 5 at nice 10). The start (A, w/w_inf) is the fundamental's M = 3 zero, and v0 is the float64 M = 5 start of dh370's step 1 (`hier_nb.py` at main 68b563f9, |r3| 3.75e-8, |r5| 2.6e-10), copied from its `hier_nb_start_x.json`.

Launcher `run_control_d.ps1` (`run_control_d.cmd` by WMI, BelowNormal, cap 86400 s then `taskkill /T /F /PID`). Pins it checks first, and stops if any differs: HEAD 73dcf243; blobs (`git hash-object --no-filters`) zero_mp.py **1077ea0e**, value_mp.py **56bb4856**, inner_mp.py **563bc062**; `control_check.py` **483e9871** (copied from `I1080-dh370/`, same blob). Then three selftests: `zero_mp.py selftest` (0 wanted), `zero_mp.py selftest --mutate=sign` (1 wanted), `control_check.py selftest` (0 wanted; a pass and three planted failures). My x2 walk ran on feat/inner-mp 6b807830, whose zero_mp.py is the same blob and whose value_mp.py (94efd416) differs from 56bb4856 only by the `VALUE_MP_PROGRESS` print (`git diff 73dcf243 6b807830`).

## Pass rule, written before the run (dh370's README, the coordinator's)

The control **passes** when the walk ends **"located"** (zero_mp's own rule) and its last row's (A, w/w_inf) is within 1e-10, in each coordinate, of Theorem A(5)'s box centre (2.71857918921174, 0.999228403206568): `control_check.py log rows` exits 0. It **fails** when the walk ends NOT located after the 8 iterations, or located elsewhere. Then I stop, report the rows, and start nothing else. By the coordinator's rule a reading of the excited zeros counts only if the control passes.

One addition of mine, to tell a wrong pin from a verdict: iteration 0 must reproduce dh370's row 0 (R = +76.31561223482653 + 113.29510720116296 i, step (-4.6015e-3, -1.4641e-2), orientation +1) to a relative 1e-6 in R. If it does not, I stop and report that, not a verdict.

## Cost, written before the run

My x2 walk, 5 processes: centre 2276 s, offsets 768 to 777 s each, 1 to 1.5 h an iteration on this machine at its current load. With 3 processes the four offsets run in two waves, so about 1 to 1.5 h an iteration. The start is 8e-3 and 1.6e-2 from the box centre, so I expect quadratic convergence and an end by iteration 3 to 5, but that is not a prediction. At most 8 iterations, so at most about 8 to 12 h; the cap is 24 h.

## Status

Written as the run goes.
- 2026-11-25 10:18:46 UTC: started (`steps_control_d.txt`): pins 73dcf243 1077ea0e 56bb4856 563bc062 483e9871 accepted, `zero_mp.py selftest` exit 0, `--mutate=sign` exit 1, `control_check.py selftest` exit 0; walk main pid 35324, BelowNormal, cap 86400 s. Criteria posted in comment 7159510595.
- 2026-11-25 12:12:19 UTC, iteration 0 row (`control_walk_d.jsonl` line 1, 6813 s after the start; centre 2878.6 s, offsets 2344.8, 1643.2, 2314.8, 2290.2 s): equal to dh370's row 0 in R, sigma, J, the step and F3's 42 digits (no difference at all), so the reproduction check (bar 1e-6 relative) **passes**. R = +76.31561223482653 + 113.29510720116296 i, |R|/sigma_mp 1.81e18, orientation +1, step (-4.6015e-3, -1.4641e-2) (58% and 89% of the way to the box centre). Not located.

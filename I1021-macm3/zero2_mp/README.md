# zero2_mp: the new zero of the M = 3 multiplier near (3.5265, 0.2115) located by Newton on value_mp's extended-precision values

Part of `I1021-macm3`. Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b), 5 processes, `nice -n 10`,
1 thread per BLAS. Issues https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and
https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Task from the coordinator (hc of 2026-11-23, after the sheet check's
acceptance): locate pass 3's new zero in extended precision. Written 2026-11-23 09:36 UTC, before the checks and the run. The
prediction and the pass rules are the coordinator's.

## Code

Worktree `~/Source/choptuik-inner-mp` of choptuik-large-d, detached at **c234fb8aebae4dd9719cfd4bd989a08807962d2b** ("zero_mp: a zero of
the M = 3 multiplier located by Newton in (A, w_f) on value_mp's values (#1076)"), `git status --porcelain -- solver` empty.
`git show --stat c234fb8a`: only `solver/inner_stokes/zero_mp.py` (102 insertions, blob 8bc34282). Since pass 3's code (6b5a7f79) the branch
has 4 commits (argcount `--m3mp`, two `m3mp_check` commits, `zero_mp`); `value_mp.py` (blob fe46e834) is the same as in pass 3
(`git diff 6b5a7f79 c234fb8a -- solver/inner_stokes/value_mp.py` is empty), and `zero_mp.py` imports `value_mp` and numpy only.
Python `~/Source/venv-macm3-1058b/bin/python` (3.14.3, numpy 2.5.4, mpmath 1.3.0).

## What the script does (its docstring)

R_1(A, w_f) at xi1 0.17 is `value_mp.value_point` (34 and 42 digits, chord steps), started from the F_3 of the nearest valued cache record and then
from the previous point's tuned F_3. Each iteration evaluates the centre and four points of central differences (A +- 1e-7,
w_f +- 1e-8), 5 evaluations in parallel (`--procs=5`); the Jacobian J is formed from them and the step is dx = -J^-1 R. It
stops when |R| < 10^3 sigma_mp, when |dx| < 1e-13, or after `--iters` steps (the iterations are numbered 0 to 5). A row per
iteration: A, w_f, R, sigma_mp, |R|/sigma_mp, J, orientation = sign(det J), dx. Exit 0 iff the last |R| is below 10^3
sigma_mp ("located"). The cache is opened for reading only; the script writes only its OUT file. `sigma_mp` is the solve's own
estimate of its numerical error, not an enclosure.

## Inputs

| role | path | lines | sha256 |
|---|---|---|---|
| cache (read only) | `I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl` of the live clone `~/Source/choptuik-large-d-raw-749p` | 3605 | 8d7cb73287cc733afd332103d2081dab3bd8a4ebdfc88d03b3f0266316d3e331 |

This is the cache after pass 3 that the sheet check (`I1021-macm3/sheet_fu022mp_p3/sha256.txt`) read; the run's end checks that it is unchanged.
The start point is the coordinator's (3.526538, 0.211482). Pass 3's count (`m3/count_M3_fu022mp_pass3_r0.17.json`) located the zero,
sign +1, at (A 3.5265378505668146, wf 0.2114823267002827) at xi1 0.17 (|F| 220.5 against a floor of 195.9) and at
(3.5264730600555, 0.21149799583702278) at xi1 0.2 (|F| 0.092 against 0.545), argcount's floats.

## Checks (before the run)

| # | command (from `solver/inner_stokes`) | required exit | log |
|---|---|---|---|
| 1 | `zero_mp.py selftest` | 0 | `logs/selftest.log` |
| 2 | `zero_mp.py selftest --mutate=sign` | 1 | `logs/selftest_sign.log` |

The selftest runs the same Newton on a planted analytic map with a zero at (3.5265381234, 0.2114823456), starting at
(3.5265, 0.2115), and passes when it lands within 1e-10 with orientation +1; the control flips the Jacobian's sign. A control that
exits 0 stops the work.

## Run

From `solver/inner_stokes`, in its own session (`launch_1070.py`: double fork and `setsid`, parent launchd) under `caffeinate -is`, with
`OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1` and `nice -n 10`:

    python -u zero_mp.py 3.526538 0.211482 <raw-749p>/I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl <OUT>/zero2_newton.jsonl --procs=5 --iters=5

with OUT = `<raw-749p>/I1021-macm3/zero2_mp`. Output: `zero2_newton.jsonl` (a row per iteration), `logs/zero2_run.log` (the script's lines),
`logs/steps.txt` (my wrapper's record of the command, start, end and exit). About 25 to 50 min an iteration (5 value_mp evaluations in parallel).
Memory and disk: alerts only to the coordinator (available memory under 2 GiB, free memory under 8%, disk under 3 GiB); nothing is stopped.

## Prediction and report (the coordinator's, written before the run)

|R| falls below 1e3 sigma_mp within 3 to 4 iterations, at a point within 1e-4 of (3.526538, 0.211482), with orientation +1
(argcount's sign of the zero). Reported: each iteration's line, the final point to 15 digits, |R|/sigma_mp and the orientation. If
the script ends without locating, or the point is further than 1e-4, or the orientation is not +1, the prediction failed and the
README's results say so.

## Results (run 2026-11-23 09:37:02 to 11:14:25 UTC, 5843 s, code c234fb8aebae4dd9719cfd4bd989a08807962d2b)

Checks first: `zero_mp.py selftest` exit 0 (landed at 3.526538123400, 0.211482345600), `selftest --mutate=sign` exit 1 (`logs/checks.txt`).
The run: **exit 1, "NOT located"** (`logs/zero2_run.log`, `logs/steps.txt`): the script stopped after the row of iteration 2 because the next
step was below 1e-13 (|dA| 8.30e-14, |dwf| 7.80e-14), with |R| above 1e3 sigma_mp. All 5 evaluations of each iteration were valued.
The cache is unchanged (3605 lines, sha256 8d7cb732..., checked after the run).

| it | A | w_f | \|R\| | sigma_mp | \|R\|/sigma_mp | orientation | dA | dwf |
|---|---|---|---|---|---|---|---|---|
| 0 | 3.526538000000000 | 0.211482000000000 | 205.1 | 4.39e-17 | 4.67e+18 | +1 | -6.4850e-05 | +1.6015e-05 |
| 1 | 3.526473150128684 | 0.211498014607490 | 0.2788 | 6.48e-17 | 4.30e+15 | +1 | -9.3433e-08 | -3.3216e-08 |
| 2 | 3.526473056695798 | 0.211497981391137 | 2.932e-07 | 3.34e-17 | 8.78e+09 | +1 | -8.3003e-14 | +7.8015e-14 |

- **Final point** (the last row, as the script prints it; the floats are A 3.5264730566957985, wf 0.2114979813911374): A **3.526473056695798**, w_f
  **0.211497981391137**; R = 2.7695e-07 + 9.626e-08i, |R| 2.932e-07, sigma_mp 3.34e-17, **|R|/sigma_mp 8.78e+09**, orientation (sign det J, det J 3.598e+12) **+1**.
  The Newton step not applied (it stopped on it) points to A 3.526473056695715, w_f 0.211497981391215.
- |R| fell by 736 and then by 9.5e5 per iteration; the Jacobian is the same to 5 digits in iterations 1 and 2.
- Against argcount's float64 locations of pass 3's count: the final point is (-6.479e-05, +1.565e-05) from its xi1 0.17 location (3.526538, 0.211482),
  6.67e-05 away, and (-3.36e-09, -1.445e-08) from its xi1 0.2 location (3.526473, 0.211498), 1.48e-08 away.

**The prediction** (written before): 
- |R| below 1e3 sigma_mp within 3 to 4 iterations: **not met**: 3 iterations (rows 0 to 2) and |R|/sigma_mp 8.78e+09; the script's "located" test failed (exit 1).
- A point within 1e-4 of (3.526538, 0.211482): met, 6.69e-05.
- Orientation +1: met in all three rows.

Why the stop test cannot be met here (arithmetic on the last row's J and the float64 spacing; no new run): sigma_mp is 3.34e-17, so 1e3 sigma_mp
is 3.34e-14 in |R|. One ulp of A (4.44e-16) changes R by 1.36e-09 and one ulp of w_f (2.78e-17) by 3.37e-11, and the cell of the float64 lattice
in the R plane has area 4.4e-20; the disc of radius 1e3 sigma_mp has 7.9e-08 of it. A float64 (A, w_f) lands in that disc only by chance, so the
test needs coordinates finer than float64 (or a looser threshold). The last step (8.3e-14) is 187 ulp of A, and would have brought |R| to the
float64 spacing's size (about 1e-9, 3e7 sigma_mp at best), not to 1e3 sigma_mp. I did not run it.

Time per iteration (evaluations in parallel, 5 workers): 1599 to 1979 s, 1524 to 2126 s, 1246 to 1737 s (sum 25498 s of evaluations);
iteration 0 ended 10:10:22, iteration 1 at 10:45:33, the run at 11:14:25 UTC.

# zero1_mp: the first zero of the M = 3 multiplier near (3.4462, 0.3476) located by Newton on value_mp's extended-precision values

Part of `I1021-macm3`. Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b), 5 processes, `nice -n 10`,
1 thread per BLAS. Issues https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and
https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Task from the coordinator (hc of 2026-11-23, after the second zero's run
`../zero2_mp/`): the same for the first zero in the box. Written 2026-11-23 11:18 UTC, before the checks and the run. The prediction is the
coordinator's.

## Code

Worktree `~/Source/choptuik-inner-mp` of choptuik-large-d, detached at **2dada6c475470843f476235758da91853b31d059** ("zero_mp: located also when the
next step is below the float64 coordinate grid and |R| is what it removes"), `git status --porcelain -- solver` empty. Since the zero2 run's c234fb8a the
branch has 2 commits: `f860d30e` (argcount `--m3mp` and `m3mp_check`, not used here) and `2dada6c4` (`zero_mp.py` only, 14 lines changed, blob 69e5fb3a);
`value_mp.py` (blob fe46e834) is the same as in pass 3 and the zero2 run (`git diff 6b5a7f79 HEAD -- solver/inner_stokes/value_mp.py` is empty).
Python `~/Source/venv-macm3-1058b/bin/python` (3.14.3, numpy 2.5.4, mpmath 1.3.0).

## What the script does (its docstring, with the new rule)

R_1(A, w_f) at xi1 0.17 is `value_mp.value_point` (34 and 42 digits, chord steps), started from the F_3 of the nearest valued cache record and then
from the previous point's tuned F_3. Each iteration evaluates the centre and four points of central differences (A +- 1e-7, w_f +- 1e-8), 5 evaluations
in parallel (`--procs=5`), forms J and the step dx = -J^-1 R. It stops when |R| < 10^3 sigma_mp, when |dx| < 1e-13, or after `--iters` steps
(iterations 0 to 5), one row per iteration (A, w_f, R, sigma_mp, |R|/sigma_mp, J, orientation = sign det J, dx). **A zero is "located"** (exit 0) when the last
|R| is below 10^3 sigma_mp, or when the next step is below the float64 coordinate grid (1e-13) and the last |R| is what that step would remove: |R| <= 10 times
the norm of J dx (the new rule). The cache is opened for reading only. sigma_mp is the solve's own error estimate, not an enclosure.

## Inputs

| role | path | lines | sha256 |
|---|---|---|---|
| cache (read only) | `I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl` of the live clone `~/Source/choptuik-large-d-raw-749p` | 3605 | 8d7cb73287cc733afd332103d2081dab3bd8a4ebdfc88d03b3f0266316d3e331 |

The cache is the one after pass 3 (the sheet check's and the zero2 run's); the run's end checks that it is unchanged. The start point is the coordinator's
(3.446204, 0.347602). Pass 3's count (`m3/count_M3_fu022mp_pass3_r0.17.json`, the zero of the cell A 3.4435956 to 3.4592206, wf 0.34404321 to 0.35029321, sign +1)
located it at xi1 0.17 at (A 3.446204430851929, wf 0.3476018025467941) (|F| 16.8 against a floor of 36.1) and at xi1 0.2 at (A 3.4462179745523085, wf 0.347606798417216)
(|F| 0.0423 against 0.0411), argcount's floats. The start is 4.74e-07 from the first and 1.48e-05 from the second; the two locations are 1.44e-05 apart.

## Checks (before the run)

| # | command (from `solver/inner_stokes`) | required exit | log |
|---|---|---|---|
| 1 | `zero_mp.py selftest` | 0 | `logs/selftest.log` |
| 2 | `zero_mp.py selftest --mutate=sign` | 1 | `logs/selftest_sign.log` |

(The selftest runs the same Newton on a planted analytic map; the control flips the Jacobian's sign. A control that exits 0 stops the work.)

## Run

From `solver/inner_stokes`, own session (`launch_1070.py`: double fork and `setsid`, parent launchd) under `caffeinate -is`, `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1`, `nice -n 10`:

    python -u zero_mp.py 3.446204 0.347602 <raw-749p>/I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl <OUT>/zero1_newton.jsonl --procs=5 --iters=5

with OUT = `<raw-749p>/I1021-macm3/zero1_mp`. Output: `zero1_newton.jsonl` (a row per iteration), `logs/zero1_run.log` (the script's lines), `logs/steps.txt` (my wrapper's
record of the command, start, end, exit and the cache's sha256 before and after). The zero2 run took about 30 to 35 min an iteration. Memory and disk: alerts only to the
coordinator; nothing is stopped.

## Prediction and report (the coordinator's, written before the run)

The zero is located (the script's exit 0 under the rule above) within 1e-4 of (3.446204, 0.347602) and within 1e-7 of argcount's xi1 0.2 location
(A 3.4462179745523085, wf 0.347606798417216; the coordinator gave it as 3.446218, 0.347607, printed to 6 digits), with orientation +1 (argcount's sign). Reported: each iteration's line,
the last row's point to 15 digits and the point after the unapplied step, |R|/sigma_mp, the orientation, and each part of the prediction as met or not met.

## Results (run 2026-11-23 11:18:28 to 13:08:08 UTC, 6580 s, code 2dada6c475470843f476235758da91853b31d059)

Checks first: `zero_mp.py selftest` exit 0, `selftest --mutate=sign` exit 1 (`logs/checks.txt`). The run: **exit 0, "located"** (`logs/zero1_run.log`,
`logs/steps.txt`): after the row of iteration 2 the next step was below the float64 coordinate grid (1.49e-16 in A, 1.34e-17 in w_f) and |R| 5.518e-11 equals the
step's 5.518e-11 (the new rule; |R| is not below 1e3 sigma_mp = 1.18e-15). All 5 evaluations of each iteration were valued. The cache is unchanged (3605 lines, sha256 8d7cb732...).

| it | A | w_f | \|R\| | sigma_mp | \|R\|/sigma_mp | orientation | dA | dwf |
|---|---|---|---|---|---|---|---|---|
| 0 | 3.446204000000000 | 0.347602000000000 | 2.600 | 4.46e-18 | 5.83e+17 | +1 | +1.4246e-05 | +4.9647e-06 |
| 1 | 3.446218246464588 | 0.347606964686522 | 2.896e-04 | 1.20e-18 | 2.41e+14 | +1 | -9.7861e-11 | +5.3089e-10 |
| 2 | 3.446218246366727 | 0.347606965217407 | 5.518e-11 | 1.18e-18 | 4.69e+07 | +1 | +1.4904e-16 | -1.3364e-17 |

- **Final point** (the last row, as the script prints it; the floats are A 3.446218246366727, wf 0.3476069652174074): A **3.446218246366727**, w_f **0.347606965217407**;
  R = -5.06e-13 - 5.5175e-11i, |R| 5.518e-11, sigma_mp 1.18e-18, **|R|/sigma_mp 4.69e+07**, orientation (sign det J, det J 5.997e+10) **+1** in all three rows. The unapplied step
  (0.34 ulp of A, 0.24 ulp of w_f) points to A 3.4462182463667271717, w_f 0.347606965217407402: the last row's point is the float64 grid point nearest the Newton root.
- |R| fell by 8977 and then by 5.25e6 per iteration; the steps fell from 1.4e-05 to 5.3e-10 to 1.5e-16.
- Against argcount's float64 locations of pass 3's count: (+1.382e-05, +5.163e-06) from its xi1 0.17 location (3.446204430851929, 0.3476018025467941), 1.475e-05 away
  (there |F| 16.8 against a floor of 36.1), and **(+2.718e-07, +1.668e-07) from its xi1 0.2 location (3.4462179745523085, 0.347606798417216), 3.189e-07 away** (there |F| 0.0423 against a floor of 0.0411).

**The prediction** (written before):
- Located (exit 0) at the script's rule: **met**.
- Within 1e-4 of (3.446204, 0.347602): **met**, 1.51e-05.
- Within 1e-7 of argcount's xi1 0.2 location: **not met**, 3.19e-07 (the full-precision floats of the count file; the 6-digit print (3.446218, 0.347607) cannot resolve 1e-7, and the final point rounds to the same 6 digits).
- Orientation +1: **met** in every row.

I draw no conclusion about why the xi1 0.2 location differs by 3.2e-07; it is argcount's float64 location at xi1 0.2, and the zero_mp point is at xi1 0.17.

Time per iteration (5 workers): 2136 to 2360 s, 1666 to 2170 s, 1289 to 2050 s (sum 29311 s of evaluations); iteration 0 ended 11:58:00, iteration 1 at 12:34:10, the run at 13:08:08 UTC.

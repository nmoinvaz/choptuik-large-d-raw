# zero0_cert: the M = 3 multiplier's zero at Theorem A(M=3)'s certified box located by Newton on value_mp's extended-precision values

Part of `I1021-macm3`. Machine: macm3 (Apple M3, 8 CPUs, 24 GB, macOS 26.3.1, arm64; runner macm3b), 5 processes, `nice -n 10`,
1 thread per BLAS. Issues https://github.com/nmoinvaz/choptuik-large-d/issues/1076 and
https://github.com/nmoinvaz/choptuik-large-d/issues/1021. Task from the coordinator (hc of 2026-11-23, after the zero1 run's acceptance; his #1076
comment of 13:20 UTC): the check against Theorem A(M=3)'s certified zero. Written 2026-11-23 13:11 UTC, before the checks and the run. The prediction is the coordinator's.

## Code

Worktree `~/Source/choptuik-inner-mp` of choptuik-large-d, detached at **90d914e93307cf199c738d7ac58005094fd44706** ("zero_mp: --f3=RE,IM, an explicit start for a zero
outside the cache's box (#1076)"), `git status --porcelain -- solver` empty. Since the zero1 run's 2dada6c4 the branch has this one commit, which changes only
`solver/inner_stokes/zero_mp.py` (11 insertions, 1 deletion, blob 64faa46d); `value_mp.py` (blob fe46e834) is the same as in pass 3 and the earlier zero runs
(`git diff 6b5a7f79 HEAD -- solver/inner_stokes/value_mp.py` is empty). Python `~/Source/venv-macm3-1058b/bin/python` (3.14.3, numpy 2.5.4, mpmath 1.3.0).

## The certified box (`solver/proof/logs/A_M_krawczyk_M3_1e-10.log`, blob e0e1f4e6 at the code commit)

"Krawczyk M = 3: K(X) in int X: True; relative margins +0.994, +0.997, +0.778, +0.778", box of the run h = 1e-10, w = 4e-16. The log's enclosures:

| quantity | enclosure | radius |
|---|---|---|
| A | [2.72647588563032, 2.72647588563144] | 5.59e-13 |
| w/w_inf (the cache's `wf`) | [1.01560309485743, 1.01560309485804] | 2.98e-13 |
| B3 | [0.144419478469924, 0.144419478470230] | 1.53e-13 |
| C3 | [0.0110874258881079, 0.0110874258881255] | 8.75e-15 |

F_3 = (C3 - i B3)/2 (the coordinator's relation): Re F_3 in [0.00554371294405395, 0.00554371294406275], Im F_3 in [-0.072209739235115, -0.072209739234962]; midpoints 0.00554371294405835 and -0.0722097392350385, which are the
`--f3` values below (0.00554371294405835, -0.0722097392350385). The start (A 2.72647588563088, w/w_inf 1.01560309485774) is inside the box in both coordinates, 0.0e-13 from the box's A center and
5.0e-15 from its w/w_inf center. The box is a Krawczyk enclosure (rigorous given the log's stated lemma) of the zero of the system with its own (A, w/w_inf, B3, C3) unknowns; this run does not check it.
The box's A is outside the cache's box (A 3.16 to 3.91), hence `--f3`.

## What the script does (its docstring)

R_1(A, w_f) at xi1 0.17 is `value_mp.value_point` (34 and 42 digits, chord steps), started here from the given F_3 and then from the previous point's tuned F_3.
Each iteration evaluates the centre and four points of central differences (A +- 1e-7, w_f +- 1e-8), 5 evaluations in parallel (`--procs=5`), forms J and the step
dx = -J^-1 R. It stops when |R| < 10^3 sigma_mp, when |dx| < 1e-13, or after `--iters` steps (iterations 0 to 5), one row per iteration (A, w_f, R, sigma_mp, |R|/sigma_mp, J, orientation = sign det J, dx).
"Located" (exit 0): the last |R| below 10^3 sigma_mp, or the next step below the float64 coordinate grid (1e-13) with |R| within 10 times the norm of J dx. The cache is not read
with `--f3` (the argument is still required); the run writes only its OUT file. **The rows and the printed lines carry no F_3**: the tuned F_3 of each evaluation is passed to the next
iteration but not written, so the prediction's F_3 clause cannot be read from this run's files (see the prediction).

## Inputs

| role | path | lines | sha256 |
|---|---|---|---|
| cache (argument only; `--f3` skips its use) | `I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl` of the live clone `~/Source/choptuik-large-d-raw-749p` | 3605 | 8d7cb73287cc733afd332103d2081dab3bd8a4ebdfc88d03b3f0266316d3e331 |

## Checks (before the run)

| # | command (from `solver/inner_stokes`) | required exit | log |
|---|---|---|---|
| 1 | `zero_mp.py selftest` | 0 | `logs/selftest.log` |
| 2 | `zero_mp.py selftest --mutate=sign` | 1 | `logs/selftest_sign.log` |

## Run

From `solver/inner_stokes`, own session (`launch_1070.py`: double fork and `setsid`, parent launchd) under `caffeinate -is`, `OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
MKL_NUM_THREADS=1`, `nice -n 10`:

    python -u zero_mp.py 2.72647588563088 1.01560309485774 <raw-749p>/I1021-macm3/fu022mp/m3/points_M3_r0.17.jsonl <OUT>/zero0_cert.jsonl --f3=0.00554371294405835,-0.0722097392350385 --procs=5 --iters=5

with OUT = `<raw-749p>/I1021-macm3/zero0_cert`. Output: `zero0_cert.jsonl` (a row per iteration), `logs/zero0_run.log` (the script's lines), `logs/steps.txt` (my wrapper's record of the command,
start, end, exit and the cache's sha256 before and after). The zero1 run took 36 to 40 min an iteration. Memory and disk: alerts only to the coordinator; nothing is stopped.

## Prediction and report (the coordinator's, written before the run)

The final point lies inside the certified box, A in [2.72647588563032, 2.72647588563144] and w/w_inf in [1.01560309485743, 1.01560309485804]; its tuned F_3 matches (C3 - i B3)/2 = 0.005543712944 - 0.072209739235i to about 1e-11.
Reported: each iteration's line; the final point to 15 digits (the last row's, and the point after the unapplied step); inside or outside for each coordinate, with the distance to the nearer
edge; |R|/sigma_mp and the orientation. The F_3 clause: the files of this run do not hold the tuned F_3, so it is reported as **not read** unless the coordinator orders a
single `value_mp.py point` run at the final point (its row has `F3re`, `F3im`; one process, about 30 to 40 min), which I do not start on my own.

## Follow-up order (the coordinator's, hc of 2026-11-23 after the F_3 gap; written before the point run)

After `zero_mp.py` ends, one point at its final location, 1 process, the same session rules (own session under caffeinate, `nice -n 10`, 1 thread per BLAS):

    python -u value_mp.py point <A_final> <wf_final> 0.00554371294405835 -0.0722097392350385

(`<A_final>`, `<wf_final>` are the floats of the last row of `zero0_cert.jsonl`, taken as `repr` by `zero0_point.sh`, which waits for `zero0.sh` to finish and then runs this;
output `zero0_point.json`, `logs/steps_point.txt`.) The CLI's default `--iters` is 8 (the Newton cap of the inner solve), where `zero_mp.py`'s evaluations use `value_point`'s default 12; the command
is the coordinator's, unchanged. Reported: the row's `F3re` and `F3im` (the tuned F_3 at that point; `F3re = C3/2`, `F3im = -B3/2` by `value_point`'s `v = (B3, C3)`) beside (C3 - i B3)/2 from the
certified enclosures, inside or outside each:

| quantity | enclosure from the log's B3 and C3 |
|---|---|
| Re F_3 = C3/2 | [0.00554371294405395, 0.00554371294406275] |
| Im F_3 = -B3/2 | [-0.072209739235115, -0.072209739234962] |

and the difference from the enclosure's midpoint (0.00554371294405835, -0.0722097392350385), against the prediction's "about 1e-11".

## Results of the zero_mp run (13:11:37 to 13:23:52 UTC, 735 s, code 90d914e93307cf199c738d7ac58005094fd44706)

Checks first: `zero_mp.py selftest` exit 0, `selftest --mutate=sign` exit 1 (`logs/checks.txt`). The run: **exit 0, "located"** at iteration 0 (`logs/zero0_run.log`, `logs/steps.txt`): the next step
(+3.73e-17 in A, -6.70e-15 in w/w_inf) was below the float64 coordinate grid rule's 1e-13 and |R| 6.744e-11 equals the step's (the rule of 2dada6c4; |R| is not below 1e3 sigma_mp = 9.4e-21 here).
All 5 evaluations were valued (576 to 735 s each). The cache is unchanged (3605 lines, sha256 8d7cb732...).

| it | A | w_f (= w/w_inf) | \|R\| | sigma_mp | \|R\|/sigma_mp | orientation | dA | dwf |
|---|---|---|---|---|---|---|---|---|
| 0 | 2.726475885630880 | 1.015603094857740 | 6.744e-11 | 9.36e-24 | 7.21e+12 | +1 | +3.73e-17 | -6.70e-15 |

R = 2.2171e-11 + 6.3687e-11i; J = [[4149.86, 3330.21], [-4997.25, 9471.99]], det J 5.595e+07 (orientation +1). The final point is the start point (no step was applied: the step is 0.08 ulp of A and 30 ulp of w_f).

**Inside the certified box** (A in [2.72647588563032, 2.72647588563144], w/w_inf in [1.01560309485743, 1.01560309485804]; exact decimals of the floats):

| point | A | inside? (nearest edge) | w/w_inf | inside? (nearest edge) |
|---|---|---|---|---|
| the last row (the start) | 2.726475885630880 | **inside** (5.60e-13) | 1.015603094857740 | **inside** (3.00e-13) |
| after the unapplied step | 2.726475885630880 (2.72647588563087998) | **inside** (5.60e-13) | 1.015603094857733 (1.01560309485773321) | **inside** (3.03e-13) |

The box centers are A 2.72647588563088 and w/w_inf 1.015603094857735: the last row is -5.3e-17 and +4.9e-15 from them, the unapplied-step point -1.5e-17 and -1.8e-15; the box's radii are 5.59e-13 and 2.98e-13.
The prediction's first clause (inside the certified box, both coordinates): **met**. Its F_3 clause: see the point run below (the files of `zero_mp.py` do not hold the tuned F_3).

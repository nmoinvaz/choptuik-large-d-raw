# I974-rpi5: the inner selection, stage 3: M = 9 without the stalled floor, its rtol control, xi1 0.14's noise

Machine rpi5 (Raspberry Pi 5, 4 cores, 8 GB, aarch64), runner. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/974 (follows #965, #964).
Code: worktree `~/Source/choptuik-large-d-964` fast-forwarded to origin/main 5e603e30 (hier.py prints K by level at verbose 2), venv
`~/Source/venv-choptuik` (numba 0.68.1). Started 2026-11-18 22:24 UTC (run 1). Contents are filled in as the runs finish.

Runs (nice 10, 3 h caps): 1 and 3 side by side, then 2.
1. M = 9 without `--floor`, `INNER_NB_RTOL=1e-13`, verbose 2: `logs/hier_nb_M9_nofloor_rpi5.log`
2. M = 9 with `--floor`, rtol 1e-12 (control): `logs/hier_nb_M9_rtol12_rpi5.log`
3. xi1 0.14 zero solves repeated at rtol 1e-13 from Job A's end state, then `m7_outer.py --local`

Scripts `run_cap.py`, `run_job.py`, `affine_all.py`, `summarize.py`, `summarize_M9.py` are copied from `I965-rpi5/`.

## Run 3, as planned before the perturbed starts (written 2026-11-18 22:40 UTC, before any of them ran)

Literal reading, `run_repeat.py` without `--perturb`: three zero solves at xi1 0.14, rtol 1e-13, each from the previous one's end state, the
first from Job A's zero solve's. Result: all three print r_1 +0.3177+1.4043i and |r_3| 1.6e-6 (none passes), identical to I965's
`zero_repeat_endstate` and to each other, because the end state printed at 9 decimals is a fixed point of the solve (numba solves are deterministic,
#964) and every zero solve at xi1 0.14, 0.15 and 0.16 prints the same end state 0.1489782, 0.014770826, 0.008424259, 0.001511207, 0.00047421,
0.000121682. A chain of repeats gives one new sample, not three.
Added, labelled as such: `--perturb 1e-7 --rngseed 974 --max 8 --want 2`: each repeat starts from that end state with every harmonic
multiplied by 1 + 1e-7 u (u uniform in (-1, 1), `random.Random(974)`), so that the solve ends at a new draw of its floor noise; it stops at two
solves with |r_3| < 1e-6 or after 8, then `m7_outer.py --local` with every centre solve. Logs `..._pert<k>.log` (`_r3high` when above the bar).

## Run 3 result: xi1 0.14, rtol 1e-13, the centre solve's noise and the zero's error estimate (finished 22:36 UTC)

Every row is one zero solve at (A, w/w_inf) = (2.719219, 1.000022), xi1 0.14, S of #964, `INNER_NB_RTOL=1e-13`, about 60 to 70 s each.

| solve | start | r_1 | \|r_3\| | bar 1e-6 |
|---|---|---|---|---|
| `zero` (Job A, I965) | Z_X | -0.7512 -0.3201i | 7.2e-7 | passes |
| `zero_repeat_r3high` (I965) | none (pretune only) | -3.7310 -2.2424i | 1.7e-6 | no |
| `zero_repeat_endstate_r3high` (I965), `rep1` to `rep3` | Job A's end state | +0.3177 +1.4043i | 1.6e-6 | no, all four identical |
| `pert1` | end state, harmonics x (1 + 1e-7 u) | +0.2059 -0.2675i | 1.9e-6 | no |
| `pert2` | same | -1.0901 +5.2847i | 1.9e-6 | no |
| `pert3` | same | -1.9466 +2.7441i | 5.7e-7 | **passes** |
| `pert4` | same | -0.1390 -0.3906i | 1.4e-6 | no |
| `pert5` | same | +0.1086 +0.0420i | 1.6e-6 | no |
| `pert6` | same | +1.3677 +0.8311i | 8.2e-7 | **passes** |

Three passing centre solves (`zero`, `pert3`, `pert6`), with Job A's `dA_endstate` (9.3e-7) and `dw_endstate` (8.8e-7), `logs/m7_outer_rpi5_rtol13_xi014_pert.txt`:

| | xi1 0.14 (this run) | xi1 0.15 (I965 Job 0) |
|---|---|---|
| centre r_1 | -0.4434 +1.0851i from 3 solves | -0.0874 +0.0127i from 2 |
| noise (half range of the centre's r_1) | 1.657 | 0.021 |
| \|r_3\| of the centre solves | 5.7e-7 to 8.2e-7 | 3.0e-8, 4.5e-8 |
| zero (A, w/w_inf) | 2.719332, 0.999994 | 2.719236, 1.000028 |
| error estimate (`m7_outer --local`, a sum of the noise and J terms) | 1.2e-3 (3.7e-4 noise, 8.5e-4 J) | 5.8e-6 |

Difference of the zeros, xi1 0.14 minus 0.15: **+9.6e-5 in A, -3.4e-5 in w/w_inf**, that is 0.08 and 0.03 of the xi1 0.14 error estimate, far below the 3 estimates
the issue sets for a radius dependence. The estimate is itself 60 times the 2e-5 of Lemma R, so this run cannot confirm or refute the radius independence at 2e-5.
It shows that the xi1 0.14 zero is known to about 1e-3, because its level 3 does not get below |r_3| of about 6e-7 to 2e-6 while xi1 0.15's reaches 3e-8,
and r_1's noise follows |r_3| (1.7 / 7e-7 = 2.4e6 at 0.14, 0.021 / 3e-8 = 7e5 at 0.15, against the 1e5 to 1e6 of B_tail_M7.md 2).

What the repeats show:
- The literal command, three solves each from the previous one's end state, gives one new sample, not three: the 9-decimal end state is a fixed point and the solve is
  deterministic (#964), so `rep1`, `rep2`, `rep3` and I965's `zero_repeat_endstate` are the same solve. All end states of every xi1 0.14, 0.15 and 0.16 zero solve
  print 0.1489782, 0.014770826, 0.008424259, 0.001511207, 0.00047421, 0.000121682, so the solves differ only in digits the log does not print.
- The perturbed starts (relative 1e-7, `random.Random(974)`, written before they ran) are an addition to the issue's command, to get new draws of the floor noise.
  2 of 6 pass the bar, 3 of 9 centre solves overall.
- `m7_outer.py --fit` through the same five passing solves gives the same zero (2.719332, 0.999994, `logs/m7_outer_rpi5_rtol13_xi014_fit.txt`), so it adds nothing.

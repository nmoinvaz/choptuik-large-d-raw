# I974-rpi5: the inner selection, stage 3: M = 9 without the stalled floor, its rtol control, xi1 0.14's noise

Machine rpi5 (Raspberry Pi 5, 4 cores, 8 GB, aarch64), runner. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/974 (follows #965, #964).
Code: worktree `~/Source/choptuik-large-d-964` fast-forwarded to origin/main 5e603e30 (hier.py prints K by level at verbose 2), venv
`~/Source/venv-choptuik` (numba 0.68.1). Started 2026-11-18 22:24 UTC, last run ended 23:38 UTC. Run order: 1 and 3 side by side, then 2, then 4 (added by the coordinator), all at nice 10 with 3 h caps.

Answer in four lines (details below):
- Run 1 (M = 9, no `--floor`, rtol 1e-13): level 5's first solve ends at |r_5| 42.7 as in #965, its approach solve (xi 0.1188) stopped at |g| 19.6; the floor rule is not the cause. Level 3 never iterates, final |r_3| 5.2e5.
- Run 2 (M = 9, `--floor`, rtol 1e-12): the same stall (35.7, approach 15.7), final |r_3| 3.9e5; T36's growth to 6e4 is not reproduced (no growth, no decrease).
- Run 3 (xi1 0.14): zero (2.719332, 0.999994), error estimate 1.2e-3, 0.08 of it from xi1 0.15's zero.
- Run 4 (xi1 0.15, three perturbed starts): zero (2.719236, 1.000026), error estimate 9.9e-6, consistent with the +-2e-5.

Files: `logs/hier_nb_M9_nofloor_rpi5.log` (run 1), `logs/hier_nb_M9_rtol12_rpi5.log` (run 2), `logs/hier_nb_M7_rpi5_rtol13_xi014_*` and `logs/m7_outer_rpi5_rtol13_xi014_pert.txt` (run 3),
`logs/hier_nb_M7_rpi5_rtol13_xi015_pert?.log` and `logs/m7_outer_rpi5_rtol13_xi015_pert.txt` (run 4), `logs/*Kcontrol*` (M = 7 reference for K), `logs/M9_*_summary.txt`, driver logs `logs/run974_*`.
Scripts `run_cap.py`, `run_job.py`, `affine_all.py`, `summarize.py`, `summarize_M9.py` are copied from `I965-rpi5/` (`summarize_M9.py` adds the K table and the level 7 solves);
`run_repeat.py` is new (selftest `python3 run_repeat.py --selftest`, mutations `--mutate=r3|count|endstate|pert` each exit 1).

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

## Run 4 (added by the coordinator after run 3): xi1 0.15 with perturbed starts, planned before it ran (2026-11-18 23:40 UTC)

Question: is the quoted M = 7 zero's +-2e-5 (from repeats at xi1 0.15) too small? Same probe as run 3: `run_repeat.py --xi1 0.15 --tag rtol13_xi015 --seed
<Job 0's zero log> --dA <Job 0's dA_endstate> --dw <Job 0's dw_endstate> --perturb 1e-7 --rngseed 974 --max 3 --want 3`, rtol 1e-13: three zero solves at xi1
0.15 from the seed's end state with each harmonic times 1 + 1e-7 u. With the same rng seed, these three starts are the same three as `pert1` to `pert3` at
xi1 0.14, so the two radii are paired. Then `m7_outer.py --local` with the seed (Job 0's `zero`) and the perturbed solves that pass the bar, and Job 0's dA and dw.
Verdict rule, fixed now: error estimate <= 1e-5 is consistent with +-2e-5; >= 1e-4 means +-2e-5 is too small (the coordinator's "near 1e-3 as at 0.14" is a case
of this); in between is reported as is. The M = 7 zero is the one of `I965-rpi5` Job 0 (2.719236, 1.000028; estimate 5.8e-6 from 2 centre solves, `zero` and `zero_repeat_endstate`).
Also added, not in the issue: the M = 7 xi1 0.15 zero solve of I965's Job 0 (same command, rtol 1e-13) rerun at `--verbose=2` so that the K table has an M = 7 reference
(`logs/hier_nb_M7_rpi5_rtol13_xi015_Kcontrol_verbose2.log`); its r_1 must equal Job 0's `zero` log (-0.0874 scale, deterministic solve), which checks that verbose does not change the numbers.

## Run 4 result: the zero at xi1 0.15 from perturbed starts (finished 23:38 UTC)

Same three starts as `pert1` to `pert3` at xi1 0.14 (same rng seed), rtol 1e-13, 63 to 77 s each. All three pass the bar, so does Job 0's `zero`
(`logs/m7_outer_rpi5_rtol13_xi015_pert.txt`, centre solves `zero`, `pert1`, `pert2`, `pert3`, offsets Job 0's `dA_endstate`, `dw_endstate`):

| xi1 | start | r_1 | \|r_3\| |
|---|---|---|---|
| 0.15 | `zero` (Z_X) | -0.0718 -0.0079i | 3.0e-8 |
| 0.15 | `pert1` | -0.0661 +0.0271i | 6.4e-9 |
| 0.15 | `pert2` | -0.1051 +0.0506i | 8.9e-8 |
| 0.15 | `pert3` | -0.0915 +0.0624i | 3.3e-8 |
| 0.14 | `pert1` to `pert3` (run 3) | +0.2059 -0.2675i, -1.0901 +5.2847i, -1.9466 +2.7441i | 1.9e-6, 1.9e-6, 5.7e-7 |

| | xi1 0.15, 4 centre solves | xi1 0.15 of I965 (2 solves) | xi1 0.14 (run 3, 3 solves) |
|---|---|---|---|
| noise (half range of the centre's r_1) | 0.035 | 0.021 | 1.657 |
| zero A, w/w_inf | 2.719236, 1.000026 | 2.719236, 1.000028 | 2.719332, 0.999994 |
| error estimate (`m7_outer --local`) | **9.9e-6** (7.3e-6 noise, 2.6e-6 J) | 5.8e-6 | 1.2e-3 |

Verdict by the rule fixed before the run: 9.9e-6 is at most 1e-5, consistent with the quoted M = 7 zero's +-2e-5 (A 2.719236 is the same to 6 digits as before, w/w_inf
moves by 2e-6). The estimate grows from 5.8e-6 to 9.9e-6 with four centre solves instead of two, and is 120 times smaller than at xi1 0.14; it is the same estimator,
the sum of the noise and J terms of `m7_outer.py` (not a bound, and from at most 4 solves). The difference between the two radii's zeros, 9.6e-5 in A, is 10 estimates of
xi1 0.15's, and 0.08 of xi1 0.14's: it is carried by the noisy radius.

## Runs 1 and 2: M = 9 (`logs/hier_nb_M9_nofloor_rpi5.log`, 6029 lines, 4040 s; `logs/hier_nb_M9_rtol12_rpi5.log`, 814 s; both ended by themselves, exit 0)

Commands as in the issue, through `run_cap.py 3` (nice 10), main 5e603e30: run 1 `INNER_NB_RTOL=1e-13`, no `--floor`; run 2 `INNER_NB_RTOL` unset (1e-12, checked in `/proc/<pid>/environ`), with `--floor`.
Tables: `logs/M9_nofloor_summary.txt`, `logs/M9_rtol12_summary.txt` (`summarize_M9.py`, the I974 copy).

| | #965 (rtol 1e-13, `--floor`) | run 1 (rtol 1e-13, no floor) | run 2 (rtol 1e-12, `--floor`) |
|---|---|---|---|
| level 5, first solve, \|r_5\| (its approach solve, xi 0.1188, stops at \|g\|) | 42.7 (19.6), 2150 residuals, 404 s | 42.7 (19.6), 2150 residuals, 407 s | 35.7 (not logged), 1317 residuals, 218 s |
| level 5, second solve | 42.7 (19.7) | 42.7 (19.7) | 31.4 (15.7) |
| level 5, later solves | 0.23, 6e-3, 8e-3, 6e-2, 1.7e-2, 2.9e-2, 1.4e-2, 14.5, 14.4, 1.8, 1.8 | 47.7, 45.2, 44.0, 43.3, 43.0, 42.9 | 140, 196, 191, 178, 169, 167 |
| level 3 iterations printed | 3 (2570, 77.5, 17.4) | none | none |
| final \|r_3\| | 17 | 5.2e5 | 3.9e5 |
| FIXED-A r_1 | 4.4e4 + 1.1e4i | 3.9e9 + 2.5e9i | 2.4e9 + 2.3e9i |
| wall time | 2758 s | 4040 s | 814 s |

- **Level 5 stalls without the floor rule.** Run 1's first two solves end at 42.7 exactly as #965's (the floor is first recorded after solve 1, so solve 1 is the same code), and its six later
  solves stay at 43 to 48, each with its approach solve at |g| 20 to 24. The floor rule is not what stalls level 5. Run 2 at rtol 1e-12 stalls the same way (35.7, 31.4; approach 15.7).
- **Which inner level stalls.** Within level 5's first solve (run 1, log lines up to 756) the nested level 9 solves to 2e-10 to 5e-9 in 1 to 20 residuals, level 7 stops at |r_7| 7e-6 to 2.6e-4 ("noise floor", K not yet computed),
  and level 5's own approach solve (xi 0.1188) stops at |g| 19.6, then its polish solve at 42.7. It is level 5 itself, at its approach radius, that does not converge (acceptance 1: not below 1e-6).
- **Level 3 never iterates in runs 1 and 2.** `hier.py` prints a level 3 iteration only for an accepted trial. After the two level-5 solves (initial |r_3|), a silent 1110 s in run 1 (776 to 1886 s: presumably the finite-difference Jacobian
  of level 3, which runs in the workers at verbose 0), and the six trial solves lam = 1, 1/2, ..., 1/32 are the six later level-5 solves of the table, whose x[2:4] steps shrink by half each (x[3] 0.014770713 + 1.5e-6, 7.4e-7, 3.7e-7, ...)
  and whose |r_5| falls back toward 42.7; none decreases |r_3|, so the level stops at "|g| 5.23e+05 (noise floor)". #965's accepted trial moved x[2], x[3] by -2.7e-6, -1.1e-5 and its level 5 then solved to 0.23.
  Neither run reproduces that, and in run 1 the whole path to the first trial is the same code except for the floor rule (run 2 differs in rtol). The log does not print |r_3| at rejected trials.
- **T36's growth to 6e4 (acceptance 2) is not seen as a growth.** At rtol 1e-12 (run 2) |r_3| is 3.9e5 at the start and no trial lowers it or raises it above that, so 6e4 is not reproduced and there is no growth to report; the value is 6 times T36's. At rtol 1e-13 without the floor it is 5.2e5.
  So rtol 1e-13 does not matter much for level 5's stall here (run 1 against run 2), and #965's drop to 17 came from one lucky accepted trial, not from rtol or the floor rule alone.
- **K by level** (hier.py 5e603e30, verbose 2, max |entry| of the block of rows r_l against the unknowns of level nu, printed once, line 758 of run 1; run 2's agrees to within 1%, e.g. K[3,5] 4.28e19):

| rows \ columns | nu 1 | nu 3 | nu 5 | nu 7 | nu 9 |
|---|---|---|---|---|---|
| l 1 | 4.03e21 | 1.29e22 | 3.16e23 | 1.31e25 | 2.49e26 |
| l 3 | 7.32e17 | 1.76e18 | 4.29e19 | 1.76e21 | 3.63e22 |
| l 5 | 9.44e13 | 2.64e14 | 6.70e15 | 2.76e17 | 5.88e18 |
| l 7 | 1.38e10 | 3.66e10 | 9.27e11 | 3.81e13 | 8.08e14 |
| l 9 | 1.79e5 | 4.20e5 | 9.88e6 | 4.07e8 | 7.76e9 |

  The M = 7 reference (`logs/hier_nb_M7_rpi5_rtol13_xi015_Kcontrol_verbose2.log`: I965's Job 0 zero solve rerun at verbose 2, same r_1 -7.1796e-2 -7.8775e-3i and 747 residuals as the original, so verbose does not change the numbers) has
  K[3,5] 5.61e15, K[5,5] 7.36e11, K[3,7] 9.34e16, K[7,7] 9.17e8. Every block is larger at M = 9 by 8e3 to 4e4 (K[3,5] 7.6e3, K[5,5] 9.1e3, K[3,7] 1.9e4, K[5,7] 2.3e4, K[7,7] 4.2e4), while K[3,5] / K[5,5] is 7.6e3 at M = 7
  and 6.4e3 at M = 9. Read as a ratio of block maxima (crude, an order of magnitude at most), a level-5 residual of 43 corresponds to about 2.8e5 in r_3, as observed (3.9e5 to 5.2e5), and one of 1e-9 to about 6e-6.
  If level 5's floor scaled with K (a factor 1e4), it would go from 6e-10 to about 6e-6, not to 20 to 43, so it does not explain the stall by itself.
- **Not tested:** a new approach radius for level 5, a better seed for x[4:6] (level 5's unknowns), or a different matching radius; these runs only show that the stall is level 5's approach solve and is independent of the floor rule and of rtol 1e-13 against 1e-12.

## Recommended tasks (one line each; the coordinator files them)

1. **M = 9 level 5, approach radius pilot.** Run level 5's solve alone (levels 7 and 9 nested as in hier) at several approach radii and seeds for x[4:6], from the M = 7 zero's state, until |g| at the approach drops below 1e-3 or the radii are exhausted; acceptance: a radius at which level 5's first solve ends below 1e-6, or the scan shows none does. Depends on #974.
2. **hier.py: print |r_3| (and |r_5|) of each rejected trial at verbose 2**, so that level 3's trials, now silent, can be read (run 1's six trials are only visible as level 5 solves). Acceptance: a trial line per lam in a rerun of run 2 with the rtol and floor as before. Depends on #974.
3. **xi1 0.14 below the bar by a margin.** Rerun the three solves with `--h3=1e-5` (and rtol 1e-14), to bring |r_3| from 6e-7..2e-6 to under 1e-7 so that the zero's estimate at xi1 0.14 falls toward 1e-5; acceptance: an estimate of at most 1e-5 at xi1 0.14, or |r_3| stays at 1e-6. Depends on #974 (run 3: 1.2e-3).

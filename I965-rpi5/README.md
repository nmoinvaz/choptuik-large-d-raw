# I965-rpi5: the inner selection, stages 1b and 2: M = 7 at three radii with rtol 1e-13, then the M = 9 diagnostic

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, Ubuntu aarch64, Python 3.13.7), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/965 (coordinator task, follows #964, toward #355). Code: the #964 worktree of
origin/main 0fc2fab0 (branch `wip/i964-rpi5`, no commits), venv `~/Source/venv-choptuik` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4,
scipy 1.18.1. `run_job.py`, `affine_all.py` and `summarize.py` are #964's (`I964-rpi5/`, 84782909); `run_job.py` here differs by one line
that writes `INNER_NB_RTOL` into the driver log.

Started 2026-11-18 17:26 UTC (stage 1b), stage 2 17:39 to 18:25 UTC. Contents are filled in as the runs finish.

## Stage 1b: M = 7 at three radii with `INNER_NB_RTOL=1e-13` (17:26 to 17:39 UTC)

`run_job.py XI1 rtol13_xiNNN --cap_h 3` (the #964 driver: the four solves of `proof/B_tail_M7.md` 3.1, a repeat from the end state of a
solve with |r_3| > 1e-6, `_r3high` if it stays above, then `m7_outer.py --local`), three jobs side by side at nice 10, `--procs 2` each,
the environment variable verified in the main and the spawn workers (`/proc/<pid>/environ`), 4.9 to 5.6 GB available, about 180 MB per
process. Wall 9.0 min (0.14), 10.2 min (0.15), 12.1 min (0.16) from 17:26:41 UTC, the 3 h cap not near. No Traceback before a FIXED-A line (the BytesIO one at
exit is in every log).

**Job 0 (xi1 0.15, control): reproduces the zero.** `m7_outer.py --local` (output `logs/m7_outer_rpi5_rtol13_xi015.txt`): zero
A 2.719236, w/w_inf 1.000028, error estimate 5.8e-6 (4.2e-6 from the centre's noise, 1.5e-6 from J), J singular values 1.06e4, 4.85e3.
Against (2.71922, 1.000022): +1.6e-5 in A, +6e-6 in w/w_inf, inside the 2e-5 of the issue. The first attempts of dA, dw and
zero_repeat ended at |r_3| 1.5e-5, 4.6e-6, 5.8e-6 (above the bar) and the repeats from the end state at 2.0e-8, 2.3e-8, 4.5e-8.

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.0718 -0.0079i | 3.0e-08 | 747 | 91 |
| `dA` | 2.719419000 | 1.000022000 | +0.7692 -1.5751i | 1.5e-05 (above) | 839 | 98 |
| `dA_endstate` | 2.719419000 | 1.000022000 | +0.7755 -0.7857i | 2.0e-08 | 553 | 63 |
| `dw` | 2.719219000 | 1.000122000 | +0.6623 +0.9913i | 4.6e-06 (above) | 842 | 102 |
| `dw_endstate` | 2.719219000 | 1.000122000 | +0.1409 +0.9963i | 2.3e-08 | 632 | 71 |
| `zero_repeat` | 2.719219000 | 1.000022000 | +0.6249 -0.0130i | 5.8e-06 (above) | 902 | 109 |
| `zero_repeat_endstate` | 2.719219000 | 1.000022000 | -0.1030 +0.0332i | 4.5e-08 | 649 | 65 |

**Job A (xi1 0.14): the solves pass the bar, the zero is 9.0e-5 from Job 0's in A, a finding.** `m7_outer.py --local` prints a zero
(`logs/m7_outer_rpi5_rtol13_xi014.txt`): A 2.719326, w/w_inf 1.000042, J singular values 2.1e4, 6.1e3, **error estimate nan** (one centre
solve under the bar, `zero` at 7.2e-7, so no half-range; the two repeats of the zero stayed above, 1.7e-6 and 1.6e-6). Against Job 0:
+9.0e-5 in A (4.5 times the 2e-5), +1.4e-5 in w/w_inf; against (2.71922, 1.000022): +1.06e-4 and +2.0e-5. Caveat, not a result of it:
the three solves used are at 7.2e-7, 9.3e-7 and 8.8e-7, within 28% of the bar, and the same point's two rejected repeats have r_1 = -3.73 - 2.24i
and +0.318 + 1.404i against -0.751 - 0.320i for the accepted one, 3.6 and 2.0 away from it and 5.4 from each other, which over the smallest
singular value 6.1e3 is 3e-4 to 6e-4 in the zero, larger than the 9.0e-5. So the difference is not distinguished from the noise of r_1 at this |r_3|, and the bar of 1e-6 is too
loose at this radius for a 2e-5 comparison. Against rtol 1e-12 (#964) 1 of the 4 roles passed at 0.14 (dw) and 3 of 4 do here (zero, dA, dw); the final |r_3| are 7.2e-7 to 1.7e-6 against 7.7e-7 to 3.3e-6.

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.7512 -0.3201i | 7.2e-07 | 732 | 82 |
| `dA` | 2.719419000 | 1.000022000 | -0.5805 -4.8395i | 6.1e-06 (above) | 757 | 86 |
| `dA_endstate` | 2.719419000 | 1.000022000 | +0.4546 -0.5131i | 9.3e-07 | 640 | 70 |
| `dw` | 2.719219000 | 1.000122000 | -0.5422 +0.2020i | 1.5e-06 (above) | 710 | 77 |
| `dw_endstate` | 2.719219000 | 1.000122000 | -0.2170 +1.7553i | 8.8e-07 | 620 | 70 |
| `zero_repeat_r3high` | 2.719219000 | 1.000022000 | -3.7310 -2.2424i | 1.7e-06 (above) | 698 | 74 |
| `zero_repeat_endstate_r3high` | 2.719219000 | 1.000022000 | +0.3177 +1.4043i | 1.6e-06 (above) | 597 | 69 |

**Job B (xi1 0.16): the bar is still missed, no zero.** All eight solves end at |r_3| 1.2e-5 to 2.2e-5 (rtol 1e-12 in #964: 8.2e-6 to
5.9e-5), so rtol 1e-13 does not lower the floor at 0.16 and its integration noise is not what sets it. `m7_outer.py --local` refuses
(exit 1). Labelled affine zeros of all four solves (`affine_all.py`, `logs/affine_all_rpi5_rtol13_xi016.txt`), **not accepted by the
1e-6 bar**: first attempts A 2.719217, w/w_inf 1.000015 (J singular values 1.3e4, 4.0e3); after the end-state repeat A 2.719193,
w/w_inf 1.000025 (9.5e3, 4.9e3; two of the four are the same point). Against Job 0: -1.9e-5 and -4.3e-5 in A, -1.3e-5 and -3e-6
in w/w_inf.

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero_r3high` | 2.719219000 | 1.000022000 | -0.0331 +0.2107i | 2.2e-05 (above) | 761 | 92 |
| `zero_endstate_r3high` | 2.719219000 | 1.000022000 | +0.1240 -0.1075i | 2.0e-05 (above) | 671 | 79 |
| `dA_r3high` | 2.719419000 | 1.000022000 | +0.8157 -1.0114i | 1.2e-05 (above) | 857 | 111 |
| `dA_endstate_r3high` | 2.719419000 | 1.000022000 | +1.1037 -0.7305i | 2.1e-05 (above) | 713 | 88 |
| `dw_r3high` | 2.719219000 | 1.000122000 | +0.1116 +1.2922i | 2.0e-05 (above) | 866 | 112 |
| `dw_endstate_r3high` | 2.719219000 | 1.000122000 | +0.2070 +0.7822i | 2.2e-05 (above) | 689 | 75 |
| `zero_repeat_r3high` | 2.719219000 | 1.000022000 | +0.0628 -0.0508i | 1.2e-05 (above) | 942 | 90 |
| `zero_repeat_endstate_r3high` | 2.719219000 | 1.000022000 | +0.1240 -0.1075i | 2.0e-05 (above) | 671 | 65 |

## Stage 2: the M = 9 diagnostic (`logs/hier_nb_M9_diag_rpi5.log`, 3816 lines, the whole verbose=2 log; exit file `.exit`)

The issue's command unchanged, run through `run_cap.py 3 LOG EXIT -- CMD` (nice 10, a kill of the process group at 3 h):
`INNER_NB_RTOL=1e-13 python -u hier_nb.py 9 2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168
--xi1=0.15 --pretune --fixA --schur --predict --floor --procs 2 --h3=1e-4 --verbose=2`. It ended by itself at 2758 s (46 min, 15232
residuals, 181 MB for the main process), nowhere near the cap, with the FIXED-A line **r_1 = +4.4382e4 + 1.1429e4i, |r_3| 1.7e+1**
(F_3/F_1 = +0.054786 + 0.005428i). Tables by `summarize_M9.py` (`logs/M9_summary.txt`).

**Where it breaks: level 5, before level 3.** Levels 9 and 7 converge; level 5 does not, and level 3 then inherits it.

1. *Pretune of F_9* (B_9, C_9 only, harmonics 1 to 7 at the M = 7 zero): approach radius xi 0.0919, |r_9| 1.476e+2 to 3.5e-6 in 3 steps, no decrease
   after; polish radius **xi 0.1246** (not 0.15), 7.1e-4 to 7.4e-11 in 5 steps. B_9, C_9 = 2.660298503485e-05, 8.947854197796e-06 (B_7, C_7
   are 4.742e-4, 1.2168e-4). The main solve's start residual is |r_9| 6.6e-5, and r_1, r_3, r_5, r_7 print as 0 at the start
   (not evaluated yet, as in the M = 7 logs).
2. *Levels 9 and 7:* level 9 solves to 8e-11 to 5e-9 in 1 to 20 residuals each time (1584 solves in all, its floor recorded as 4.19e-10);
   level 7's first solves end at 7e-6 to 2.6e-4 (to 409 s), then at 3e-8 to 1e-6 after K is computed (413 s), its floor recorded as 3.11e-8
   (129 solves), against 6.6e-10 at M = 7 (`logs/hier_nb_M7_rpi5_fit3_repeat.log`). So level 7 converges to 1e-7 to 1e-6, not 1e-9.
3. *Level 5:* its first solve takes 404 s and 2150 residuals and stops at **|r_5| = 42.7**, "stop at |g| 4.27e+01 (noise floor)", against 2.6e-6
   in 23 s and then 5.7e-10 at M = 7 (`logs/hier_nb_M7_rpi5_fit3_repeat.log`). The noise-floor rule then records **"floor of level 5:
   |r_5| ~ 4.27e+01 (stop at 3x from now on)"** (line 1239), so from the second solve on a level-5 residual up to 128 counts as converged. Its
   later solves end at 0.23, 6e-3, 8e-3, 6e-2, 1.7e-2, 2.9e-2, 1.4e-2, then 14.5, 14.4, 1.78, 1.81 (table). Its approach-radius (xi 0.1188) solve
   stops at |g| 0.7 to 20 each time (the M = 7 logs at verbose 1 do not print this).
4. *Level 3:* the first |r_3| printed is 2.570e+3 (after the level-5 solve at 0.23), then 77.5 and 17.4 (table); no further iteration is printed
   and the level stops at "|g| 1.74e+01 (noise floor)" after another 1385 s of nested solves. **|r_3| does not grow in this log**: it falls by
   2.2 orders and stalls at 17.4, 7 orders above the 1e-6 bar. T36's growth to 6e4 (rtol 1e-12) is not reproduced, and this run has no rtol
   1e-12 control, so whether rtol 1e-13 matters here is not known.
5. *K:* the leakage Jacobian is not printed at verbose=2: the log says only "Jacobian K computed (10 residuals) [413 s]" (line 757). Its
   entries into r_3 from levels 5, 7 and 9 need a print added to `hier.py` (not changed here).

| time (s) | level 5 solve, \|r_5\| | its approach-radius (xi 0.1188) solve stopped at \|g\| | residuals | seconds in it |
|---|---|---|---|---|
| 409 | 4.27e+01 | 1.96e+01 | 2150 | 404 |
| 704 | 4.27e+01 | 1.97e+01 | 1559 | 291 |
| 1086 | 2.29e-01 | 2.05e+00 | 620 | 123 |
| 1219 | 6.02e-03 | 2.78e+00 | 662 | 133 |
| 1366 | 8.20e-03 | 7.21e-01 | 751 | 147 |
| 1500 | 6.06e-02 | 2.12e+00 | 676 | 134 |
| 1631 | 1.74e-02 | 1.19e+00 | 634 | 131 |
| 1764 | 2.94e-02 | 3.91e+00 | 663 | 132 |
| 1899 | 1.36e-02 | 5.41e+00 | 698 | 135 |
| 2001 | 1.45e+01 | not logged | 535 | 102 |
| 2139 | 1.44e+01 | 6.03e+00 | 686 | 138 |
| 2659 | 1.78e+00 | not logged | 734 | 142 |
| 2757 | 1.81e+00 | not logged | 488 | 98 |

| level 3 iteration | \|r_3\| | time (s), residuals so far |
|---|---|---|
| 0 (lam 1) | 2.570e+03 | 1086, 6324 |
| 1 (lam 1) | 7.747e+01 | 1219, 6986 |
| 2 (lam 1) | 1.743e+01 | 1366, 7737 |

Reading, not established: with level 5 stalled at 1e-2 to 40, the Schur-corrected r_1 (error about 1e5 to 1e6 times |r_3|, B_tail_M7.md 2) is
about 2e6 to 2e7 here, so 4.4e4 carries no information, and r_1^[9](p_7) is not obtained. What M = 9 needs is a convergent level 5 first:
the candidates the issue names are harmonic 9's own polish radius (0.1246 here against 0.15 for levels 1 to 7), a better seed for F_9, or another
matching radius; this log says level 5 is where each would have to act, and that its "floor" is a stall.

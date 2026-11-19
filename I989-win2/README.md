# I989-win2: M = 7 at xi1 0.145 and 0.155, a closer radius pair for Lemma R

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session, runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/989 (coordinator task, follows #981).

Code: worktree `D:\choptuik-inner` (the session's own), moved from 5e603e30 to origin/main b081fbb2; the only change under `solver/inner_stokes` since
5e603e30 is hier.py's `--approach` (default off). venv `C:\Users\nathan\Source\venv-i962` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4,
scipy 1.18.1. win2b's ks_chain2 and #945 run beside it; nothing is run from or changed in `D:\choptuik-i962`.

## Written down before the runs (2026-11-19 00:43 UTC)

- Control first (`control989.py`): the `zero` solve at xi1 0.15, rtol 1e-14, `--h3=1e-4` (Z and S of #964) from b081fbb2 must reproduce #976's log from
  5e603e30 line by line apart from seconds and memory addresses. If it differs the chain stops and nothing else runs until the cause is known. Its
  mutation (`--mutate=ref`, against #975's rtol 1e-13 log) must differ.
- Then Job A of #975 (four fixed-(A, w) solves: zero, dA = A + 2e-4, dw = w/w_inf + 1e-4, zero_repeat; Z and S as in #964) at xi1 0.145 and then at 0.155,
  `INNER_NB_RTOL=1e-14`, `--h3=1e-4`, `--procs 2`, BelowNormal, 3 h cap each, one at a time (`chain989.py`, exits in `exits_989.txt`), driver
  `run_job981.py` (#981's, unchanged; its driver logs are named `run981_<tag>.driver.log`). A solve with |r_3| not under 1e-6 (two printed digits) is
  repeated from its first end state with every harmonic times 1 + 1e-7 u (`random.Random(976)`, one generator per job), up to 3 repeats, stopping at the
  first under the bar. Then `m7_outer.py --local`, and where it refuses a labelled affine zero (`affine_all.py`, not accepted).
- Report: per radius every solve (|r_3|, r_1, residuals, seconds), the zero and its estimate (`zero_digits977.py`, which fails when its numbers differ
  from m7_outer's print), and the distance from the 0.15 zero in units of each estimate and of their sum. The 0.15 references: Z14c of #977
  (2.719234224, 1.000024742, estimate 9.12e-6; same rtol, h3 and rule) and the zero the issue names, (2.71924, 1.000025) with the notes' 1e-5.
- Acceptance (the issue): both estimates at most 3e-5, then the zeros within the combined estimates of 0.15's support Lemma R's radius independence
  over xi1 0.145 to 0.155 and a larger distance is a finding; if an estimate is larger, the floors are reported.

## The control: it fired once, the cause, and the refined version (2026-11-19 00:45 to 00:51 UTC)

The control as written above ran in the chain at 00:43:27 (solve 138 s) and **fired at 00:45:46: 37 lines against #976's 42**. The cause is the
exit-time `BytesIO` Traceback block (5 lines after the FIXED-A line in #976's log, from `multiprocessing.Pool.__del__` at interpreter exit): every
line up to and including FIXED-A and the lines after it are identical, r_1 -0.0850 + 0.0552i, |r_3| 6.0e-8 (`logs/control989_v1_fired_diff.txt`). That block
is present in some logs of identical code and absent in others (#981: 9 of 9 logs of run 1 had it, 0 of 11 of run 2), so the strict comparison was
too strict. The chain stopped as written. I then refined the comparison (`control989.py` v2, the first version is `control989_v1_strict.py`) to drop
that block after FIXED-A from both logs, which is a change made after seeing the diff, and reran the control cleanly at 00:49:23 UTC with the correct
environment: **37 and 37 lines identical, r_1 -0.085043+0.055245i, |r_3| 6e-08, exit 0; its mutation against #975's rtol 1e-13 log differs, exit 1**
(`logs/control989_v2.log`). So origin/main b081fbb2 gives the same bits as 5e603e30 for this solve.

My mistake in between: after the patch of the control failed on a docstring mismatch, my script ran the unmodified file with `--compare-only`, which that
version ignored, so it re-ran the control solve twice (00:46:31 to 00:48:19 and a third start killed at about 00:48:50 by `taskkill /T` on its own
tree), in the default environment (no `INNER_NB_RTOL`, `RUN_SRC` pointing at `D:\choptuik-i962\solver\inner_stokes`, read only, no bytecode written).
Their logs are in `void_mistaken_reruns/` and no number from them is used; nothing was written in `D:\choptuik-i962`. The two Jobs start only after
the clean control: `chain989b.py` (Jobs only; `chain989.py` is the original with the control, which stopped itself).

## Results (Job A at 0.145 00:51:54 to 01:06:15 UTC, 862 s; at 0.155 01:06:15 to 01:44:30 UTC, 2295 s; both driver exits 0)

No Traceback in any log (the exit-time `BytesIO` block is absent from all 22). Files: `logs/m7_outer_win2_rtol14_xi01{45,55}.txt`,
`logs/zero_digits_win2_rtol14_xi0145.txt`, `logs/pairs989.md`, `logs/affine_all_win2_rtol14_xi0155.txt`.

**xi1 0.145: all four roles under the bar after at most one repeat, and the estimate is 1.9e-4.** `m7_outer.py --local` zero A 2.719313276, w/w_inf 0.999998856,
estimate 1.94e-4 (6.6e-5 the centre's noise, 1.28e-4 J), centre r_1 = -0.2614+0.0100i from 2 solves, noise (half range) 0.164, J singular values 1.29e4 and 2.5e3.
The estimate is `m7_outer`'s noise plus J estimate from two centre solves, not an enclosure.

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.4254 +0.0216i | 2.8e-07 | 706 | 146 |
| `dA` | 2.719419000 | 1.000022000 | +3.4314 -3.5696i | 1.3e-05 (above) | 692 | 102 |
| `dA_pert1` | 2.719419000 | 1.000022000 | +0.5162 +0.5495i | 1.8e-07 | 776 | 109 |
| `dw` | 2.719219000 | 1.000122000 | -0.5499 +3.4134i | 6.6e-06 (above) | 729 | 133 |
| `dw_pert1` | 2.719219000 | 1.000122000 | +0.1928 +1.1521i | 3.5e-07 | 577 | 108 |
| `zero_repeat` | 2.719219000 | 1.000022000 | +0.0824 +0.1311i | 1.4e-06 (above) | 671 | 115 |
| `zero_repeat_pert1` | 2.719219000 | 1.000022000 | -0.0975 -0.0016i | 2.9e-07 | 646 | 125 |

**xi1 0.155: one solve of 15 under the bar, `m7_outer.py --local` refuses** ("not enough solves with |r_3| < 1e-6", exit 1): only `dw_pert2` (5.4e-7) is under it; the centres stay at
5.0e-6 to 1.2e-5 (`zero`) and 1.3e-6 to 2.5e-5 (`zero_repeat`), `dA` at 1.4e-6 to 1.5e-5.

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero_r3high` | 2.719219000 | 1.000022000 | -0.0509 +0.1040i | 1.1e-05 (above) | 832 | 158 |
| `zero_pert1_r3high` | 2.719219000 | 1.000022000 | +0.1517 -0.0328i | 1.2e-05 (above) | 953 | 170 |
| `zero_pert2_r3high` | 2.719219000 | 1.000022000 | -0.0621 +0.0858i | 1.0e-05 (above) | 671 | 136 |
| `zero_pert3_r3high` | 2.719219000 | 1.000022000 | +0.1230 +0.0033i | 5.0e-06 (above) | 853 | 160 |
| `dA_r3high` | 2.719419000 | 1.000022000 | +0.6293 -0.6119i | 1.5e-05 (above) | 911 | 193 |
| `dA_pert1_r3high` | 2.719419000 | 1.000022000 | +0.6384 -1.1645i | 1.4e-05 (above) | 815 | 165 |
| `dA_pert2_r3high` | 2.719419000 | 1.000022000 | +0.9475 -0.7321i | 1.4e-05 (above) | 759 | 123 |
| `dA_pert3_r3high` | 2.719419000 | 1.000022000 | +0.8653 -0.8691i | 1.4e-06 (above) | 857 | 161 |
| `dw` | 2.719219000 | 1.000122000 | -0.4204 +1.0772i | 2.5e-05 (above) | 682 | 178 |
| `dw_pert1` | 2.719219000 | 1.000122000 | +0.2162 +1.1409i | 2.2e-05 (above) | 702 | 135 |
| `dw_pert2` | 2.719219000 | 1.000122000 | +0.2249 +0.9687i | 5.4e-07 | 741 | 96 |
| `zero_repeat_r3high` | 2.719219000 | 1.000022000 | -0.2700 +0.3418i | 1.3e-06 (above) | 774 | 126 |
| `zero_repeat_pert1_r3high` | 2.719219000 | 1.000022000 | -0.0773 +0.0633i | 1.4e-05 (above) | 841 | 135 |
| `zero_repeat_pert2_r3high` | 2.719219000 | 1.000022000 | -0.0416 -0.0342i | 9.9e-06 (above) | 982 | 187 |
| `zero_repeat_pert3_r3high` | 2.719219000 | 1.000022000 | +0.0736 -0.5747i | 2.5e-05 (above) | 612 | 128 |

**Distances from the xi1 0.15 zero** (`pairs977.py`, norm in (A, w/w_inf), in units of each estimate and of their sum):

| zero i | zero j | distance | in est i | in est j | in est i + est j |
|---|---|---|---|---|---|
| Z14c of #977 (0.15, estimate 9.12e-6) | Z145 (0.145, estimate 1.94e-4) | 8.32e-5 (dA +7.9e-5, dw -2.6e-5 from 0.15 to 0.145) | 9.12 | 0.43 | 0.41 |
| notes' zero (2.71924, 1.000025, 1e-5) | Z145 | 7.78e-5 | 7.78 | 0.40 | 0.38 |

Labelled affine zeros at xi1 0.155, **not accepted by the 1e-6 bar** (`logs/affine_all_win2_rtol14_xi0155.txt`): first attempts (2.719254, 1.000013), J singular values 1.0e4 and 2.2e3, the two
same-point solves miss the model by 0.16; the lowest |r_3| per role (2.719240, 1.000014), 9.5e3 and 5.6e3, miss 0.26. Against Z14c: +2e-5 and +6e-6 in A. Over the smallest singular
value a miss of 0.2 is 1e-4 in the zero.

**Floor by radius** (|r_3| as printed, bar 1e-6; the 0.14 and 0.15 rows are the same knobs, rtol 1e-14, h3 1e-4, perturbed repeats, seed 976, from #981 run 1 and #976 / #977):

| xi1 | attempts | under the bar | first attempts (zero, dA, dw, zero_repeat) | solves under the bar | perturbed repeats under the bar |
|---|---|---|---|---|---|
| 0.15 (#976, #977 run 1) | 7 | 4 | 6.0e-8, 7.4e-6, 9.4e-6, 3.3e-6 | 3.4e-9 to 6.0e-8 | 3 of 3 |
| 0.145 | 7 | 4 | 2.8e-7, 1.3e-5, 6.6e-6, 1.4e-6 | 1.8e-7 to 3.5e-7 | 3 of 3 |
| 0.14 (#981 run 1) | 9 | 3 | 5.5e-7, 6.7e-6, 1.2e-6, 2.9e-6 | 4.2e-7 to 5.5e-7 | 2 of 5 |
| 0.155 | 15 | 1 | 1.1e-5, 1.5e-5, 2.5e-5, 1.3e-6 | 5.4e-7 | 1 of 11 |

The centre solves of xi1 0.145 differ in r_1 by 0.33 at |r_3| 2.8e-7 and 2.9e-7, which is 5.6e5 times |r_3| (0.15: 0.021 over 3e-8, 7e5 in #965).

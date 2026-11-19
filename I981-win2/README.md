# I981-win2: M = 7 at xi1 0.14 with a lower level-3 floor, rtol 1e-14 and --h3=1e-5

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session, runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/981 (coordinator task, follows #977, rpi5's recommendation 3 in #974).

Code: worktree `D:\choptuik-i962` at 5e603e30 (as #975 to #977; origin/main ed5e0c32 only adds hier.py's `--approach`, default off, not used
here), venv `C:\Users\nathan\Source\venv-i962` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1. win2b's ks_chain2 and
#945 run beside it.

## Written down before the runs (2026-11-18 23:53 UTC)

- Job A of #975: the four fixed-(A, w) solves at xi1 0.14 (zero, dA, dw, zero_repeat; Z and S as in #964), `--procs 2`, BelowNormal, 3 h cap,
  `INNER_NB_RTOL=1e-14`, one run at a time (`chain981.py`, exits in `exits_981.txt`). Driver `run_job981.py` = #976's `run_job976.py` plus
  `RUN_H3` for `--h3` (diff: the docstring, the `H3` line, the driver-log name). A solve with |r_3| not under 1e-6 (as printed with two
  digits) is repeated from its first end state with every harmonic times 1 + 1e-7 u (`random.Random(976)`, one generator per job in
  solve order), up to 3 repeats per solve, stopping at the first under the bar. Then `m7_outer.py --local`.
  1. `--h3=1e-4`, tag `rtol14_h3e4_xi014`.
  2. `--h3=1e-5`, tag `rtol14_h3e5_xi014`.
- Where m7_outer refuses (a solve above the bar after the repeats) a labelled affine zero of the final solves is given
  (`affine_all.py`, not accepted by the bar), as in #964 and #975.
- The floor per knob: |r_3| of every solve and the lowest |r_3| per role. The reference zero at xi1 0.15 is Z14c of #977 (2.719234224,
  1.000024742, estimate 9.12e-6, rtol 1e-14, h3 1e-4); distances are given in units of each estimate and of their sum. The matched
  0.15 reference for h3 1e-5 is not run here.
- Acceptance (the issue): a run brings the 0.14 estimate to 3e-5 or below, then the radius test reads one way or the other, or the floors
  are reported per knob.

## Where the runs ran (added 2026-11-19 00:20 UTC)

Run 1 (`--h3=1e-4`) ran 23:53:22 to 00:12:01 UTC from `D:\choptuik-i962` at 5e603e30 (clean, nothing checked out or changed there; the
solver read only). At about 00:15 the coordinator's rule arrived: win2b's ks_chain2 runs from that checkout, so inner-selection tasks use
the runner's own worktree. Run 2's first attempt (started 00:12:03 from `D:\choptuik-i962`) was stopped at 00:16:31 after 4 min by killing
my own chain's process tree (taskkill /T on its launcher pid 27652; nothing of win2b's), its partial logs are in `aborted_run2_in_i962/`
and no number from them is used. Run 2 restarted from `D:\choptuik-inner`, a worktree of the same commit 5e603e30 (so the same code
as #975 to #977 and run 1; origin/main ed5e0c32 only adds `--approach`, default off), with `chain981b.py`. The solves are deterministic, so
this changes the start time only.

## Results (run 1 23:53:22 to 00:12:01 UTC, 1120 s; run 2 00:17:01 to 00:38:43 UTC, 1302 s; both driver exits 0)

No Traceback before a FIXED-A line in any log. Run 1's logs each end with the exit-time `BytesIO` Traceback of the other runs, run 2's have none
(not looked into). Files: `logs/m7_outer_win2_*.txt`, `logs/affine_all_win2_rtol14_xi014.txt`, `logs/m7_outer_win2_rtol14_xi014_explore_mixed_h3.txt`.

**Neither run gets an estimate.** Run 1: `m7_outer.py --local` prints a zero from one centre solve (`zero`, 5.5e-7), so its estimate is nan.
Run 2: `m7_outer.py --local` refuses (exit 1), `dA` stays above the bar in all four attempts. In each run one role misses
(run 1 `zero_repeat`, run 2 `dA`).

Run 1 (rtol 1e-14, `--h3=1e-4`, from `D:\choptuik-i962` at 5e603e30), `m7_outer`: zero A 2.719360, w/w_inf 1.000079, estimate nan (J singular values 7.9e3
and 2.8e3):

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.7299 +0.9334i | 5.5e-07 | 818 | 160 |
| `dA` | 2.719419000 | 1.000022000 | +1.5919 +1.4733i | 6.7e-06 (above) | 659 | 140 |
| `dA_pert1` | 2.719419000 | 1.000022000 | +0.0608 -0.4264i | 5.3e-07 | 748 | 115 |
| `dw` | 2.719219000 | 1.000122000 | +0.1550 +2.0496i | 1.2e-06 (above) | 648 | 96 |
| `dw_pert1` | 2.719219000 | 1.000122000 | -0.4323 +0.9833i | 4.2e-07 | 687 | 124 |
| `zero_repeat_r3high` | 2.719219000 | 1.000022000 | -4.1810 -0.4194i | 2.9e-06 (above) | 760 | 138 |
| `zero_repeat_pert1_r3high` | 2.719219000 | 1.000022000 | +0.1080 +0.8816i | 2.4e-06 (above) | 555 | 104 |
| `zero_repeat_pert2_r3high` | 2.719219000 | 1.000022000 | -0.2447 +0.4300i | 1.5e-06 (above) | 556 | 109 |
| `zero_repeat_pert3_r3high` | 2.719219000 | 1.000022000 | -1.7448 +4.0761i | 1.6e-06 (above) | 553 | 100 |

Run 2 (rtol 1e-14, `--h3=1e-5`, from `D:\choptuik-inner` at 5e603e30), `m7_outer` refuses:

| log | A | ω/ω∞ | r₁ | \|r₃\| | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.2476 +1.4631i | 3.2e-06 (above) | 698 | 148 |
| `zero_pert1` | 2.719219000 | 1.000022000 | +0.2179 +0.9345i | 6.5e-08 | 589 | 104 |
| `dA_r3high` | 2.719419000 | 1.000022000 | -1.2980 -3.6076i | 7.5e-06 (above) | 628 | 115 |
| `dA_pert1_r3high` | 2.719419000 | 1.000022000 | +0.4774 -1.5102i | 2.6e-06 (above) | 609 | 130 |
| `dA_pert2_r3high` | 2.719419000 | 1.000022000 | +1.2258 +0.1338i | 1.5e-06 (above) | 498 | 87 |
| `dA_pert3_r3high` | 2.719419000 | 1.000022000 | +1.1435 -1.6161i | 2.2e-06 (above) | 707 | 99 |
| `dw` | 2.719219000 | 1.000122000 | +0.6174 +3.2315i | 5.8e-06 (above) | 650 | 96 |
| `dw_pert1` | 2.719219000 | 1.000122000 | +0.1508 +0.1663i | 3.1e-06 (above) | 560 | 112 |
| `dw_pert2` | 2.719219000 | 1.000122000 | -2.4369 +0.1514i | 4.0e-07 | 780 | 153 |
| `zero_repeat` | 2.719219000 | 1.000022000 | +2.3407 +0.9087i | 2.1e-06 (above) | 865 | 139 |
| `zero_repeat_pert1` | 2.719219000 | 1.000022000 | +0.3630 +0.8129i | 4.7e-07 | 723 | 87 |

**Floor per knob** (|r_3| as printed, bar 1e-6):

| knob | attempts | under the bar | lowest | first attempts (zero, dA, dw, zero_repeat) | median first attempt |
|---|---|---|---|---|---|
| rtol 1e-14, h3 1e-4 | 9 | 3 (zero, dA_pert1, dw_pert1) | 4.2e-7 | 5.5e-7, 6.7e-6, 1.2e-6, 2.9e-6 | 2.1e-6 |
| rtol 1e-14, h3 1e-5 | 11 | 3 (zero_pert1, dw_pert2, zero_repeat_pert1) | 6.5e-8 | 3.2e-6, 7.5e-6, 5.8e-6, 2.1e-6 | 4.5e-6 |

Perturbed repeats under the bar: 2 of 5 at h3 1e-4, 3 of 7 at h3 1e-5. For comparison at xi1 0.14: rpi5 #965 (rtol 1e-13, h3 1e-4) first attempts
7.2e-7, 6.1e-6, 1.5e-6, 1.7e-6 and #975 (1e-13) 1.1e-6, 6.9e-6, 4.7e-6, 2.0e-6; at xi1 0.15 the centre solves reach 3e-8 to 6e-8.

**Labelled affine zeros of the solves, not accepted by the bar** (`affine_all.py`, `logs/affine_all_win2_rtol14_xi014.txt`; the two centre solves of a
set disagree by the residual given):

| set | A | w/w_inf | J singular values | centre residual |
|---|---|---|---|---|
| run 1, first attempts | 2.719468 | 0.999923 | 3.8e4, 5.4e3 | 1.85 |
| run 1, lowest \|r_3\| per role | 2.719382 | 1.000096 | 6.7e3, 1.7e3 | 0.35 |
| run 2, first attempts | 2.719296 | 1.000055 | 3.2e4, 1.1e4 | 1.32 |
| run 2, lowest \|r_3\| per role | 2.719380 | 1.000060 | 2.8e4, 4.7e3 | 0.095 |

**Exploratory, outside the rule written before the runs:** `m7_outer.py --local` over the three centre solves under the bar of both runs (run 1
`zero`, run 2 `zero_pert1` and `zero_repeat_pert1`, which mixes the two h3 values) with run 1's passing offsets: zero A 2.719355, w/w_inf 1.000029,
estimate 5.6e-4 (1.5e-4 from the centre noise 0.546, 4.1e-4 from J).

**Reference at xi1 0.15:** Z14c of #977, (2.719234224, 1.000024742), estimate 9.12e-6. Run 1's zero is +1.26e-4 in A from it, with no estimate to put
that in units of. The affine lines are 6.2e-5 to 2.3e-4 above it in A, over a spread of 1.7e-4 between the four.

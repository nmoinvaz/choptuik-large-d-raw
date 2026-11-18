# I977-win2: M = 7 at xi1 0.15, rtol 1e-13 and 1e-14 under one repeat rule

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session, runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/977 (coordinator task, follows #975 and #976).

Code: worktree `D:\choptuik-i962` at origin/main 5e603e30 (as #975, #976), venv `C:\Users\nathan\Source\venv-i962` with numba 0.68.1,
llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1. win2b's ks_chain2 and #945 run beside it.

## Written down before the runs (2026-11-18 23:18 UTC)

- Driver: `run_job976.py`, unchanged from #976's (sha256 equal, its driver logs are named `run976_<tag>.driver.log`). Job 0 at xi1 0.15,
  Z and S of #964, `--procs 2`, BelowNormal, 3 h cap each, one run at a time (`chain977.py`, exits in `exits_977.txt`). A solve whose
  |r_3| is not under 1e-6 is repeated from its first end state with every harmonic times 1 + 1e-7 u (uniform in (-1, 1), one
  `random.Random(seed)` per job in solve order), up to 3 repeats, stopping at the first under the bar.
  1. `INNER_NB_RTOL=1e-14`, seed 977, tag `rtol14_s977_xi015`.
  2. `INNER_NB_RTOL=1e-13`, seed 976, tag `rtol13_s976_xi015` (#976's rule at #975's rtol).
- Zeros compared (A, w/w_inf, estimate = `m7_outer.py --local`'s noise plus J estimate, read with 9 digits by `zero_digits977.py`, which
  fails when its numbers differ from m7_outer's print):
  - Z13e: #975's 1e-13 zero with end-state repeats (2.719240421, 1.000025476, 4.1e-6), and rpi5's #965 (2.719236, 1.000028, 5.8e-6).
  - Z13p: run 2 alone.
  - Z14a: #976's 1e-14 zero (2.719232205, 1.000022996, 7.71e-6), seed 976, 2 centre solves.
  - Z14b: run 1 alone.
  - Z14c, the 1e-14 zero of this issue: `m7_outer.py --local` with every centre solve under the bar from #976 (zero,
    zero_repeat_pert1) and run 1 (all its centre attempts), and the offsets dA and dw of run 1 (`combine977.py`). Its variant Z14c' uses
    #976's offsets, to show the dependence on the Jacobian's offsets.
- Acceptance test, as the issue words it: Z13p and Z14c agree when their distance (norm in (A, w/w_inf)) is at most the sum of their
  estimates. The report gives the distance of every pair among Z13e, Z13p, Z14a, Z14b, Z14c (rpi5 too) in units of each estimate and of
  their sum (`pairs977.py`, whose selftest passes and fails under `--mutate=norm` and `--mutate=swap`).

## Results (23:18:46 to 23:47:28 UTC; run 1 1024 s, run 2 698 s, both driver exits 0, no Traceback before a FIXED-A line)

Files: `logs/m7_outer_win2_*.txt` (m7_outer outputs), `logs/zeros977.json`, `logs/pairs977.md` (every zero and every pair, from
`analyze977.py`), `logs/controls977.log`, `summarize.py` tables below. `zero_digits977.py` agrees with m7_outer's own print for every zero.

**First attempts are the same solves as in #975 and #976.** The solves are deterministic, so run 1's `zero`, `dA`, `dw`, `zero_repeat`
equal #976's and run 2's equal #975's (same r_1, |r_3| and residual counts; the logs agree line by line once seconds and memory
addresses are stripped). The new samples are the perturbed repeats only. So #976's `zero` and run 1's `zero` are one solve, and the
combined centre set Z14c holds 3 distinct solves (#976 `zero`, #976 `zero_repeat_pert1`, run 1 `zero_repeat_pert1`), not 4. Z14c+dup
counts the duplicate twice, for the record. The offsets of the 1e-13 zeros Z13e and Z13p differ only in their repeats, and
both use the same `zero` and `zero_repeat` solves.

Run 1 (rtol 1e-14, seed 977):

| log | A | w/w_inf | r_1 | abs r_3 | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.0850 +0.0552i | 6.0e-08 | 668 | 172 |
| `dA` | 2.719419000 | 1.000022000 | +4.1140 -1.9765i | 7.4e-06 (above) | 683 | 113 |
| `dA_pert1` | 2.719419000 | 1.000022000 | +0.7672 -0.7776i | 1.1e-08 | 657 | 115 |
| `dw` | 2.719219000 | 1.000122000 | +0.1659 +0.9073i | 9.4e-06 (above) | 776 | 143 |
| `dw_pert1` | 2.719219000 | 1.000122000 | +0.1378 +1.0083i | 1.5e-08 | 914 | 168 |
| `zero_repeat` | 2.719219000 | 1.000022000 | -1.7917 +1.4313i | 3.3e-06 (above) | 715 | 138 |
| `zero_repeat_pert1` | 2.719219000 | 1.000022000 | -0.0940 +0.0162i | 1.8e-08 | 1020 | 153 |

Run 2 (rtol 1e-13, seed 976):

| log | A | w/w_inf | r_1 | abs r_3 | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.0994 +0.0509i | 3.0e-08 | 929 | 112 |
| `dA` | 2.719419000 | 1.000022000 | +1.8714 -0.1443i | 4.6e-05 (above) | 769 | 115 |
| `dA_pert1` | 2.719419000 | 1.000022000 | +0.7757 -0.7655i | 4.2e-08 | 867 | 136 |
| `dw` | 2.719219000 | 1.000122000 | +2.8819 +3.7933i | 6.1e-06 (above) | 860 | 147 |
| `dw_pert1` | 2.719219000 | 1.000122000 | +0.1532 +1.0274i | 3.7e-08 | 511 | 82 |
| `zero_repeat` | 2.719219000 | 1.000022000 | -0.1313 +0.0687i | 5.0e-07 | 652 | 93 |

Zeros (A, w/w_inf; estimate is `m7_outer.py --local`'s noise plus J estimate from the centre solves, not an enclosure):

| zero | A | w/w_inf | estimate | centre solves |
|---|---|---|---|---|
| Z13e #975, 1e-13, end-state repeats | 2.719240421 | 1.000025476 | 4.08e-06 | 2 |
| Z13p run 2, 1e-13, perturbed repeats | 2.719242554 | 1.000025865 | 4.59e-06 | 2 |
| rpi5 #965, 1e-13 (printed values) | 2.719236 | 1.000028 | 5.8e-06 | 2 |
| Z14a #976, 1e-14, seed 976 | 2.719232205 | 1.000022996 | 7.71e-06 | 2 |
| Z14b run 1 alone, 1e-14, seed 977 | 2.719237695 | 1.000026145 | 5.60e-06 | 2 |
| **Z14c** #976 + run 1 centres, run 1 offsets | 2.719234224 | 1.000024742 | 9.12e-06 | 3 |
| Z14c' same centres, #976 offsets | 2.719234100 | 1.000024630 | 9.03e-06 | 3 |

Acceptance test written before the runs: Z13p and Z14c, distance 8.41e-6 (dA 8.33e-6, dw 1.12e-6), estimates 4.59e-6 and 9.12e-6.
In units: 1.83 of Z13p's estimate, 0.92 of Z14c's, 0.61 of their sum (13.7e-6), 0.82 of their quadrature sum (10.2e-6). It agrees
within the combined estimates. Every pair among the 1e-13 and 1e-14 zeros is within the sum of its two estimates (largest 0.87,
Z13p against Z14a); the whole table is in `logs/pairs977.md`.

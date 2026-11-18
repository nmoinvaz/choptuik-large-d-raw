# I976-win2: M = 7 at xi1 0.15 at rtol 1e-14, the zero's convergence in the integrator tolerance

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session, runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/976 (coordinator task, follows #975).

Code: worktree `D:\choptuik-i962` at origin/main 5e603e30 (as #975), venv `C:\Users\nathan\Source\venv-i962` with numba 0.68.1,
llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1. win2b's ks_chain2 and #945 run beside it. The numba backend applies
`INNER_NB_RTOL` as given (`inner_nb.py` lines 299-300, atol stays 1e-16), without scipy's clamp of rtol to 100 eps = 2.2e-14.

## Written down before the runs (2026-11-18 22:59 UTC, before the launch at 22:59:53)

- Job 0 of #975 (four solves at xi1 0.15 with Z and S of #964, `--procs 2`, BelowNormal, 3 h cap) with `INNER_NB_RTOL=1e-14`, then
  `m7_outer.py --local`. Driver `run_job976.py` (#975's `run_job.py` with the repeat rule below), tag `rtol14_xi015`.
- A solve whose |r_3| is not under 1e-6 (as printed with two digits, m7_outer's rule) is not repeated from its own end state (a
  fixed point, #974 run 3). Its repeats start from its FIRST attempt's end state with every harmonic times 1 + 1e-7 u, u uniform in
  (-1, 1) from `random.Random(976)`, one generator for the job drawn in solve order (zero, dA, dw, zero_repeat), at most 3 repeats
  per solve, stopping at the first one under the bar. Logs `<name>.log`, `<name>_pert1.log` .... A role with none under the bar
  gets `_r3high` on all its logs.
- The driver's selftest (`selftest_run_job976.log`) passes and fails under `--mutate=r3`, `--endstate`, `--pert`. A run of the
  driver against a stub `hier_nb.py` that replays #975's logs checked the repeat starts (perturbed, different, from the first end
  state), the stop at the first pass, the `_r3high` renaming and the `m7_outer` arguments.
- Acceptance (the issue): the zero at 1e-14 lies within its error estimate of 1e-13's (2.719240421, 1.000025476, estimate
  4.1e-6, #975), else the move is reported as the integrator's share of the error.

## Result (22:59:53 to 23:14:54 UTC, 901 s, driver exit 0, no Traceback before a FIXED-A line)

`m7_outer.py --local` (`logs/m7_outer_win2_rtol14_xi015.txt`, digits by `zero_digits.py` in `logs/zero_digits_win2_rtol14_xi015.txt`):
zero A 2.719232205, w/w_inf 1.000022996, error estimate 7.7e-6 (6.1e-6 the centre's noise, 1.6e-6 J), centre r_1 = -0.0571+0.0447i from
2 solves (`zero` and `zero_repeat_pert1`), noise 0.028, J singular values 1.08e4 and 4.6e3. The estimate is `m7_outer`'s noise
estimate from two centre solves, not an enclosure and not a spread over fit choices.

| log | A | w/w_inf | r_1 | abs r_3 | residuals | seconds |
|---|---|---|---|---|---|---|
| `zero` | 2.719219000 | 1.000022000 | -0.0850 +0.0552i | 6.0e-08 | 668 | 133 |
| `dA` | 2.719419000 | 1.000022000 | +4.1140 -1.9765i | 7.4e-06 (above) | 683 | 141 |
| `dA_pert1` | 2.719419000 | 1.000022000 | +0.7782 -0.7834i | 3.4e-09 | 818 | 147 |
| `dw` | 2.719219000 | 1.000122000 | +0.1659 +0.9073i | 9.4e-06 (above) | 776 | 114 |
| `dw_pert1` | 2.719219000 | 1.000122000 | +0.1347 +1.0470i | 3.0e-08 | 594 | 77 |
| `zero_repeat` | 2.719219000 | 1.000022000 | -1.7917 +1.4313i | 3.3e-06 (above) | 715 | 113 |
| `zero_repeat_pert1` | 2.719219000 | 1.000022000 | -0.0291 +0.0342i | 2.2e-08 | 866 | 155 |

The three first attempts above the bar each passed at the first perturbed repeat (1e-7), so no second repeat was drawn. The
first attempt's end state was perturbed, and the `x` of each repeat is in the driver log.

| rtol | zero (A, w/w_inf) | error estimate | from the 1e-14 zero (A, w/w_inf, norm) |
|---|---|---|---|
| 1e-12 (stored, quoted) | (2.71922, 1.000022) | 2e-5 (quoted) | +1.22e-5, +1.0e-6, 1.22e-5 |
| 1e-13 win2 (#975) | (2.719240421, 1.000025476) | 4.1e-6 | -8.2e-6, -2.5e-6, 8.6e-6 |
| 1e-13 rpi5 (#965) | (2.719236, 1.000028) | 5.8e-6 | -3.8e-6, -5.0e-6, 6.3e-6 |
| 1e-14 win2 (#976) | (2.719232205, 1.000022996) | 7.7e-6 | |

Distance of the 1e-14 zero from win2's 1e-13 zero, 8.6e-6 in the norm: 1.1 times the 1e-14 estimate, 2.1 times the 1e-13
estimate, 0.73 times their sum (11.8e-6). Steps in A: 1e-12 to 1e-13 +2.0e-5, 1e-13 to 1e-14 -8.2e-6.

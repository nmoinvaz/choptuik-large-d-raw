# I999-win2: M = 9, level 5's polish radius scanned

Machine win2 (desktop-pc, Core Ultra 7 265K, Windows 11, Python 3.14.10), the win2 build session, runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/999 (coordinator task, rpi5's recommendation in #980, toward #355 and #996).

Code: worktree `D:\choptuik-inner` (the session's own) fast-forwarded to origin/main efad7afd (`hier.py --polish=NU:XI`, passed to the spawn workers as
`--approach` is), venv `C:\Users\nathan\Source\venv-i962` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4, scipy 1.18.1. win2b's ks_chain2 and #945 run
beside it; nothing is run from or changed in `D:\choptuik-i962`.

## Written down before the runs (2026-11-19 01:54 UTC)

- #980's command (rpi5's, which is #974 run 1's with an approach option), with `--polish=5:XI` for XI in 0.12, 0.13 and 0.14, the approach at hier.py's
  default (0.1188), `--floor` not given:
  `INNER_NB_RTOL=1e-13 python -u hier_nb.py 9 2.719219 1.000022 --x=0.148977988,0.014770713,0.008424206,0.001511189,0.000474205,0.00012168 --xi1=0.15
  --pretune --fixA --schur --predict --procs 2 --h3=1e-4 --verbose=2 --polish=5:XI`, BelowNormal, one process group per run, two runs side by side
  (0.12 and 0.13) and the third (0.14) when one ends, 1 h cap each (`chain999.py`: the cap kills the whole process tree with `taskkill /T /F`; its
  selftest passes and fails under `--mutate=nokill`, `logs/selftest_chain999.txt`). Logs `logs/hier_nb_M9_polish5_<XI>_win2.log`, `.exit` files, driver log
  `logs/run999.driver.log`.
- Each log's 'level radii' line is checked with `check_polish.py LOG XI` (r_5's polish radius, the number after the arrow, equals XI; `--mutate` must exit 1).
- Report per XI (`summarize_polish5.py`, #980's summarizer): level 5's first solve (|r_5| at its end, the approach solve's and the polish solve's stop |g|,
  residuals, seconds) and level 3's first iterations if reached, beside #980's table for the default polish radius 0.15 (|r_5| 42.5 to 42.8 at the approach radii
  0.095 to 0.125, 19.6 at 0.105).
- Acceptance (the issue): an XI that takes level 5's first solve below 1e-6, or the table of |r_5| against XI. If one works, the M = 9 zero solve with it, 3 h cap.

## The scan changed (coordinator hc, 2026-11-19 about 02:06 UTC; written 02:08 UTC, before the new runs start)

Level 5's first solves of the XI 0.12 and 0.13 runs (6.47 and 18.9, against 42.5 to 42.8 at the default 0.15) were seen before this change, which the coordinator
made after them: the runs for 0.12 and 0.13 stay as started (01:54:46 UTC), **XI 0.14 is dropped**, and after both have ended two more runs go side by side with the
same command, 1 h cap each, and the approach radius kept below the polish radius:

- `--polish=5:0.11 --approach=5:0.105` and `--polish=5:0.10 --approach=5:0.095` (`chain999b.py`; logs `hier_nb_M9_polish5_<XI>_approach5_<AP>_win2.log`).
- If a run's level 5's first solve ends below 1e-6 it goes on to the M = 9 zero solve with a 3 h cap: the same computation, so the run's cap is extended to 3 h from its
  start once a `level 5 solved` line shows |r_5| < 1e-6 (the driver does it and logs it). The same rule is not applied to the 0.12 and 0.13 runs (their first solves are far above 1e-6).
- Mechanics: the first scheduler (`chain999.py`, which would have started 0.14 when a slot freed) was stopped at 02:07:07 UTC by killing its own two processes (pids 10020, 10848) without the
  tree; the two running solves (launcher pids 5992 and 15464) went on. A relaunch of the cap watcher failed once (PowerShell split its date argument on a space; the 1 h cap was not
  due until 02:54:46), and `adopt999.py` has watched both since 02:07:41 UTC. It kills the run's tree at the 1 h cap and writes the `.exit` files, whose exit code is "not captured". Selftests of
  `adopt999.py` and `chain999b.py` pass and fail under their mutations (`logs/selftest_*.txt`).

## Results (runs 0.12 and 0.13 from 01:54:46 UTC, 0.11/0.105 and 0.10/0.095 from 02:55:10 UTC; ended 02:33:50, 02:54:56, 03:33:00, 03:12:50 UTC)

Written 06:3x UTC 19 Nov: the session was relaunched under another account after 03:33, so the last two runs sat unread for about 3 h. No Traceback in any log (the exit-time
`BytesIO` block is absent). Nothing of this task runs. Per-solve tables from `summarize_polish5.py` are in `logs/summary_polish5.txt`; exit files in `logs/*.exit`
(the 0.12 and 0.13 runs were adopted by `adopt999.py` after their scheduler was replaced, so their exit codes are "not captured": 0.13 ended by itself with a FIXED-A line, 0.12 was killed at the 3600 s cap).

**Table of level 5's |r_5| against the polish radius XI** (approach radius AP of level 5; rtol 1e-13, no `--floor`; XI and AP changed together from 0.11 on, as the coordinator set):

| XI | AP | first level-5 solve (residuals, s) | later level-5 solves | lowest | level 3 | end of the run |
|---|---|---|---|---|---|---|
| 0.15 (default, #974/#980) | 0.1188 | 42.7 (2150, 407) | 42.5 to 42.8 at other AP | 19.6 (AP 0.105) | \|r_3\| 5.2e5 (stop at \|g\| 5.2e5) | no zero |
| 0.13 | 0.1188 | 18.9 (1055, 334) | 14.5, 22.7, 11.1 | 11.1 | solved at 2.02e5 (8838 residuals, 2330 s) | 2344 s, FIXED-A, r_1 -1.45e9 |
| 0.12 | 0.1188 | 6.47 (1681, 557) | 4.49, 6.81, 1.86 | 1.86 | one iteration, 5.965e4 at 3430 s | killed at the 3600 s cap |
| **0.11** | 0.105 | 7.43 (1184, 234) | **1.17e-4**, 6.73e-4, 3.92e-4, 3.37e-4 | **1.17e-4** | solved at 7.57 (12297 residuals, 2255 s) | 2270 s, FIXED-A, r_1 +5.74e5 - 8.9e4 i |
| 0.10 | 0.095 | 11.4 (1239, 245) | 10.9, 7.85 | 7.85 | solved at 2.92e5 (6201 residuals, 1046 s) | 1060 s, FIXED-A, r_1 +2.7e10 |

No XI takes level 5's first solve below 1e-6, so the M = 9 zero solve (3 h cap) was not started (the driver's cap extension never fired).

At XI 0.11 with approach 0.105 level 5 does converge to a floor: its second solve, started after the leakage Jacobian K is computed (245 s), takes six accepted iterations
2.96, 0.92, 4.5e-3, 1.2e-3, 3.6e-4, 1.2e-4 and stops at |g| 1.17e-4 (polish solve, 342 s); the three later solves end at 3.4e-4 to 6.7e-4. That is 5 orders below
the default's 42.5 and 2 orders above M = 7's level-5 floor (2.6e-6 in #974). At the end of that run r_3 7.6, r_5 3.4e-4, r_7 3.0e-8, r_9 2.2e-10; the level-7 stops range 1.2e-8 to 7e-5
(7.7e-8 and below after K) and level 9's solves 1.8e-11 to 6.6e-9, so levels 7 and 9 sit well below level 5's floor. No `level 3 it` line was printed in that run or the 0.10 run.

**What the table cannot separate:** XI and AP changed together from 0.12 to 0.11 (AP 0.1188 to 0.105), so the drop from 6.47 to 1.2e-4 is not attributed to either. At XI 0.15 AP 0.105 was the lowest AP
in #980 (19.6) and AP 0.095 the highest (42.8), so AP matters at the default XI too. Each radius is one run, and the first-solve numbers come from the same start, so there is no scatter estimate.
The "straight line through three points reaches zero near 0.115" is not seen in the first solve (XI 0.11 gives 7.43, XI 0.10 gives 11.4); |r_5| is a norm, so a crossing would show as a minimum, which the
later solves at 0.11 may be.

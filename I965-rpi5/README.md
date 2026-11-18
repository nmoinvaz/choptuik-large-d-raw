# I965-rpi5: the inner selection, stages 1b and 2: M = 7 at three radii with rtol 1e-13, then the M = 9 diagnostic

Machine rpi5 (Raspberry Pi 5, Cortex-A76 x 4, 8 GB, Ubuntu aarch64, Python 3.13.7), runner. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/965 (coordinator task, follows #964, toward #355). Code: the #964 worktree of
origin/main 0fc2fab0 (branch `wip/i964-rpi5`, no commits), venv `~/Source/venv-choptuik` with numba 0.68.1, llvmlite 0.50.0, numpy 2.5.4,
scipy 1.18.1. `run_job.py`, `affine_all.py` and `summarize.py` are #964's (`I964-rpi5/`, 84782909); `run_job.py` here differs by one line
that writes `INNER_NB_RTOL` into the driver log.

Started 2026-11-18 17:26 UTC (stage 1b), stage 2 from 17:39 UTC. Contents are filled in as the runs finish.

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

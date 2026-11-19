# I1004-rpi5: the M = 7 zero at xi1 0.145 with 32 centre solves

Machine rpi5 (Raspberry Pi 5, 4 cores, 8 GB, aarch64), runner. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1004 (#1002's recommendation; #996), assigned by the coordinator by message on 2026-11-19.
Code: worktree `~/Source/choptuik-large-d-964` at origin/main e7119e72 (`solver/inner_stokes` unchanged since 4cff2747, #1002's code), venv `~/Source/venv-choptuik` (numba 0.68.1, numpy 2.5.4),
`INNER_NB_RTOL=1e-14` (checked in the processes' environ), `--procs 2`, nice 10, two solves side by side. Scripts copied from `I1002-rpi5/`. Started 2026-11-19 02:48 UTC.

## Written down before the runs

- 24 centre solves at xi1 0.145, (A, w/w_inf) = (2.719219, 1.000022), S and Z of #964, each from a 1e-7 relative perturbation of I989-win2's xi1 0.145 `zero` log end state
  (`0.1489782, 0.014770826, 0.008424259, 0.001511207, 0.00047421, 0.000121682`, the same source as #1000's), one `random.Random(seed)` per solve, seeds 1050 to 1073, `run_pert1002.py` unchanged
  (tag `rtol14_xi0145_zero`, logs `logs/hier_nb_M7_rpi5_rtol14_xi0145_zero_s<seed>.log`). A solve counts when its printed |r_3| is under 1e-6.
- Analysis: `analyze1002.py` unchanged, with the centre group at 0.145 the 32 counted solves (#1000's eight, seeds 980 to 987, and the 24 new), the dA and dw groups at both radii and the 0.15 centre group
  from #1002 (`I1002-rpi5/logs`, same code and settings). Standard error with J's noise, d = |Delta| / combined SE, **resolved if d > 3, absent if d < 1, undecided between**; d_w alone beside it (the issue's "d_omega").
- Checks reported beside: the 24 new solves against #1000's eight (their r_1 means and sigmas, since the zero's SE assumes one distribution), the SE at 32 against #1002's projection (4.70e-6 for the 0.145 SE, 4.97e-6 combined),
  and the pooled variant with win2's counted solves added to each group (as in #1002).

## Result (24 solves finished 03:04 UTC, 15 min, all under the bar: 24 of 24)

`analyze1002.py` unchanged (`logs/analyze1004_rtol14.txt`; its selftest passes), centre group at 0.145 = the 32 counted solves, the other five groups as in #1002. Checks beside it: `logs/checks1004.txt` (`checks1004.py`).

| | xi1 0.145, 32 centre solves | xi1 0.15 (#1002, unchanged) | 0.145 in #1002 (8 centre) |
|---|---|---|---|
| counted solves (centre, dA, dw) | 32, 8, 8 | 8, 8, 8 | 8, 8, 8 |
| centre mean r_1; sigma (trace form) | -0.1135 -0.0079i; 0.292 | -0.0879 +0.0395i; about 0.033 | -0.1890 +0.0184i; 0.272 |
| zero (A, w/w_inf) | **2.719237890, 1.000030668** | 2.719236758, 1.000025616 | 2.719248303, 1.000032951 |
| standard error with J's noise (bootstrap robust) | **6.34e-6** (A 5.86e-6, w 2.43e-6; 6.33e-6) | 1.64e-6 (A 1.52e-6, w 6.0e-7) | 9.14e-6 |

| comparison | A | w/w_inf | norm |
|---|---|---|---|
| Delta = Z(0.145) - Z(0.15) | +1.132e-6 | +5.052e-6 | 5.177e-6 |
| combined SE (quadrature) | | 2.508e-6 | 6.550e-6 |
| **d** | +0.19 | **+2.01** (w/w_inf alone) | **0.79** |

**Verdict by the rule written before the run: absent** (d = 0.79 < 1). The w/w_inf component alone is undecided (d_w = 2.01, between 1 and 3), and the Mahalanobis distance with the summed covariances is 2.01 (all of it from w/w_inf).
Against #996's 1.1e-5: Delta in w/w_inf is +5.1e-6 with a combined SE of 2.5e-6, so a radius systematic of 1.1e-5 in the same sense lies 2.4 combined SE above what was measured.

Checks (`logs/checks1004.txt`):
- The 24 new solves against #1000's eight: mean r_1 -0.0883 -0.0166i (sigma 0.299) against -0.1890 +0.0184i (0.272); the means differ by 0.11, 0.9 of their combined SE, so one distribution is not contradicted.
- SE at 32: 6.34e-6 against #1002's projection of 4.70e-6 (combined 6.55e-6 against 4.97e-6): the scatter is 7% higher than the eight's, and the coefficients moved with the centre mean (c_0 -0.82 against -0.74, c_a -0.094, c_w -0.087).
- **The verdict rests on one solve.** Seed 1072 has r_1 +0.7479 -0.7845i (|r_3| 3.7e-7), Mahalanobis distance 4.62 from the 32's mean (the next is 3.99; for 32 Gaussian points the expected maximum is about 2.9); it looks like the dA solves' r_1 (+0.85 -0.80i) but its A is the centre's.
  Without it (31 solves) the zero is (2.719242544, 1.000030511), SE 4.10e-6, **d = 1.72 (undecided)**, d_w +1.94, Mahalanobis 2.28. The outlier inflates the SE (6.34e-6 against 4.10e-6) and pulls the zero toward 0.15's. The tail seen in #1002 (win2's dA solve) is also here, on rpi5.
- **Exploratory, not in the plan: r_1's noise follows |r_3|.** The Spearman correlation of |r_1 - median| with |r_3| over the 32 is +0.72, the median deviation over |r_3| is 7.8e5 (B_tail_M7.md 2: 1e5 to 1e6); the 16 solves under the median |r_3| (1.9e-7) have sigma 0.095, the 16 above it 0.402.
  So the Gaussian-with-one-sigma model in the SE is wrong in the direction of too large an error for the good solves. Cutting the 0.145 groups to |r_3| below a value, 0.15 as measured (its solves are all under 1e-7):

| cut | n centre, dA, dw | zero (A, w/w_inf) | SE | d | d_w | Mahalanobis |
|---|---|---|---|---|---|---|
| 1.0e-06 (the primary) | 32, 8, 8 | (2.719237890, 1.000030668) | 6.34e-06 | 0.79 | +2.01 | 2.01 |
| 3.0e-07 | 28, 5, 6 | (2.719241750, 1.000029132) | 3.83e-06 | 1.47 | +1.35 | 1.79 |
| 2.0e-07 | 16, 3, 6 | (2.719239444, 1.000026627) | 2.98e-06 | 0.84 | +0.51 | 1.02 |
| 1.5e-07 | 12, 2, 4 | (2.719237376, 1.000025712) | 3.18e-06 | 0.17 | +0.05 | 0.21 |

  The dA and dw groups shrink to 2 to 6 solves under the cuts, so their covariances are poor and the SEs unreliable; the table shows only that the 0.145 zero moves toward 0.15's as the cut tightens, not a result.

Not established: whether the radius dependence is absent or small. The primary verdict is "absent" at d = 0.79, the w/w_inf component alone is at 2.0 sigma, and one solve moves d to 1.72.

## Recommended tasks (one line each; the coordinator files them)

1. **A weighted analysis from the stored solves.** r_1's error follows |r_3| (Spearman +0.72): analyze the 80 solves of #1002 and #1004 with weights 1/|r_3|^2 (or a per-solve error 8e5 |r_3|), planted truth first (a synthetic set whose r_1 noise is proportional to |r_3| and whose weighted SE is checked against its bootstrap); acceptance: d and d_w with the weights, and whether they differ from 0.79 and 2.01 by more than their SE. No new solves. Depends on #1004.
2. **win2's dA and dw at 0.145** (already waiting): eight perturbed dA and eight dw solves, same seeds as 1000 to 1017, to measure the cross-build difference seen in #1002. Depends on #1004.

## The 32 centre solves at xi1 0.145

| group | seed | r_1 | \|r_3\| | under 1e-6 | residuals | seconds |
|---|---|---|---|---|---|---|
| 0.145 centre (#1000) | 980 | -0.0783 -0.0414i | 8.9e-8 | yes | 567 | 64 |
| 0.145 centre (#1000) | 981 | -0.1444 -0.0207i | 3.7e-8 | yes | 581 | 68 |
| 0.145 centre (#1000) | 982 | -0.1169 +0.0999i | 7.4e-8 | yes | 944 | 106 |
| 0.145 centre (#1000) | 983 | -0.4090 +0.2547i | 3.2e-7 | yes | 568 | 63 |
| 0.145 centre (#1000) | 984 | -0.1523 +0.1283i | 1.4e-7 | yes | 568 | 66 |
| 0.145 centre (#1000) | 985 | -0.0072 +0.0233i | 1.3e-7 | yes | 491 | 52 |
| 0.145 centre (#1000) | 986 | -0.0890 +0.1366i | 2.8e-7 | yes | 595 | 68 |
| 0.145 centre (#1000) | 987 | -0.5149 -0.4339i | 2.0e-7 | yes | 567 | 65 |
| 0.145 centre (#1004) | 1050 | -0.3369 -0.2782i | 4.3e-7 | yes | 534 | 60 |
| 0.145 centre (#1004) | 1051 | -0.0613 -0.0518i | 2.0e-7 | yes | 803 | 89 |
| 0.145 centre (#1004) | 1052 | -0.0088 -0.1022i | 2.2e-7 | yes | 660 | 79 |
| 0.145 centre (#1004) | 1053 | -0.2677 +0.2324i | 2.1e-7 | yes | 977 | 107 |
| 0.145 centre (#1004) | 1054 | -0.0251 +0.0688i | 1.3e-7 | yes | 955 | 101 |
| 0.145 centre (#1004) | 1055 | -0.2172 -0.1448i | 1.9e-7 | yes | 651 | 75 |
| 0.145 centre (#1004) | 1056 | -0.2032 +0.2053i | 2.8e-7 | yes | 586 | 63 |
| 0.145 centre (#1004) | 1057 | -0.0960 +0.0484i | 8.2e-8 | yes | 596 | 77 |
| 0.145 centre (#1004) | 1058 | -0.1502 +0.0332i | 2.5e-7 | yes | 547 | 57 |
| 0.145 centre (#1004) | 1059 | -0.1297 +0.1213i | 1.4e-8 | yes | 577 | 70 |
| 0.145 centre (#1004) | 1060 | -0.3913 -0.0092i | 2.9e-7 | yes | 503 | 57 |
| 0.145 centre (#1004) | 1061 | -0.1622 +0.1338i | 1.6e-7 | yes | 566 | 63 |
| 0.145 centre (#1004) | 1062 | -0.0308 +0.0134i | 2.9e-7 | yes | 537 | 60 |
| 0.145 centre (#1004) | 1063 | -0.1247 +0.1445i | 2.7e-7 | yes | 549 | 63 |
| 0.145 centre (#1004) | 1064 | -0.0867 +0.0109i | 8.7e-8 | yes | 653 | 75 |
| 0.145 centre (#1004) | 1065 | +0.0035 -0.0042i | 2.5e-7 | yes | 614 | 71 |
| 0.145 centre (#1004) | 1066 | -0.0454 +0.0699i | 3.1e-8 | yes | 596 | 68 |
| 0.145 centre (#1004) | 1067 | +0.1031 -0.3615i | 3.8e-7 | yes | 628 | 73 |
| 0.145 centre (#1004) | 1068 | -0.1844 +0.0310i | 6.5e-8 | yes | 549 | 62 |
| 0.145 centre (#1004) | 1069 | -0.1197 +0.1328i | 1.9e-7 | yes | 684 | 79 |
| 0.145 centre (#1004) | 1070 | -0.1953 +0.0936i | 2.0e-7 | yes | 498 | 56 |
| 0.145 centre (#1004) | 1071 | -0.0655 -0.0026i | 1.5e-7 | yes | 744 | 87 |
| 0.145 centre (#1004) | 1072 | +0.7479 -0.7845i | 3.7e-7 | yes | 536 | 57 |
| 0.145 centre (#1004) | 1073 | -0.0706 +0.0013i | 9.6e-8 | yes | 488 | 57 |

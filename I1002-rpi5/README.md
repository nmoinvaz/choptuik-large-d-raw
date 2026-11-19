# I1002-rpi5: the M = 7 zero at xi1 0.145 and 0.15 with every input sampled (centre, dA and dw)

Machine rpi5 (Raspberry Pi 5, 4 cores, 8 GB, aarch64), runner. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1002 (rpi5's recommendation in #1000; #996's tension), assigned by the coordinator by
message on 2026-11-19. Code: worktree `~/Source/choptuik-large-d-964` at origin/main 4cff2747 (`solver/inner_stokes` unchanged since acb4b6a8, #1000's code, so #1000's eight centre solves are the same code),
venv `~/Source/venv-choptuik` (numba 0.68.1, numpy 2.5.4). `INNER_NB_RTOL=1e-14` (checked in the processes' environ), `--procs 2`, nice 10, two solves side by side. Started 2026-11-19 02:16 UTC.

## Written down before the runs

- Forty fixed-(A, w/w_inf) solves, each the S of #964 (`--pretune --fixA --schur --predict --floor --procs 2 --h3=1e-4`, Z of #964) from a start of 1e-7 relative perturbation of a source end state,
  one `random.Random(seed)` per solve, six draws in the harmonics' order (`run_pert1002.py`, #1000's driver with `--A` and `--w`); the logs are `logs/hier_nb_M7_rpi5_<tag>_s<seed>[_r3high].log`.
  The end state is the 9-decimal x of the last `level 3 it` line of the source log:

| group | xi1 | point (A, w/w_inf) | source end state | seeds | tag |
|---|---|---|---|---|---|
| 0.145 dA | 0.145 | 2.719419, 1.000022 | I989-win2 `hier_nb_M7_win2_rtol14_xi0145_dA.log` | 1000 to 1007 | `rtol14_xi0145_dA` |
| 0.145 dw | 0.145 | 2.719219, 1.000122 | I989-win2 `..._xi0145_dw.log` | 1010 to 1017 | `rtol14_xi0145_dw` |
| 0.15 centre | 0.15 | 2.719219, 1.000022 | I977-win2 `hier_nb_M7_win2_rtol14_s977_xi015_zero.log` | 1020 to 1027 | `rtol14_xi0150_zero` |
| 0.15 dA | 0.15 | 2.719419, 1.000022 | I977-win2 `..._s977_xi015_dA.log` | 1030 to 1037 | `rtol14_xi0150_dA` |
| 0.15 dw | 0.15 | 2.719219, 1.000122 | I977-win2 `..._s977_xi015_dw.log` | 1040 to 1047 | `rtol14_xi0150_dw` |

  (The 0.145 centre group is #1000's eight solves, seeds 980 to 987, rtol 1e-14, same code, `I1000-rpi5/logs/hier_nb_M7_rpi5_rtol14_xi0145_s98?.log`.)
  The source end states are the I989-win2 and I977-win2 raw logs in place (raw clone worktree, I989-win2 at ea7df927, I977-win2 as of the pull of 2026-11-19).
- A solve counts when its printed |r_3| is under 1e-6 (`m7_outer`'s rule); the others are kept and renamed `_r3high`.
- `analyze1002.py`, per radius: group means r_0, r_a, r_w of r_1 over the counted solves, J = [(r_a - r_0)/2e-4, (r_w - r_0)/1e-4], zero z = (2.719219, 1.000022) - J^-1 r_0 (`m7_outer.py --local`'s formula
  with group means; cross-checked against `m7_outer.py --local` run on the first counted offsets, with a mutation). Standard error with J's noise, to first order (the derivation is in the script's docstring):
  Cov z = J^-1 (c_0^2 S_0/n_0 + c_a^2 S_a/n_a + c_w^2 S_w/n_w) J^-T, S the group's sample covariance (ddof 1), SE = sqrt(trace Cov z), with the A and w/w_inf components beside it;
  a parametric bootstrap (20000 draws) is its check. The script's selftest plants a known J, zero and noise, and a mutation drops the J terms and must fail.
- Radius comparison: Delta = Z(0.145) - Z(0.15); combined SE = sqrt(SE_145^2 + SE_150^2) (quadrature sum of the two SEs, each sqrt(trace Cov)); d = |Delta| / combined SE.
  **Resolved if d > 3, absent if d < 1, undecided between** (the issue). Reported beside it: the components, the Mahalanobis distance with the summed covariances, and the w/w_inf component alone with its own d_w and the same thresholds.
- Variants beside the primary (not replacing it): the pools with win2's counted solves added to each group (#989's and #977's), if their numbers differ.

## Result (all 40 solves finished 02:42 UTC, 26 min; every solve under the bar: 8 of 8 in each of the five groups)

`analyze1002.py` (`logs/analyze1002_rtol14.txt`; selftest and its three mutations pass, and its zero equals `m7_outer.py --local`'s on the first counted offsets at both radii, `logs/m7_outer_rpi5_rtol14_xi0145_firstoffsets.txt`
and `..._xi0150_firstoffsets.txt`). All numbers rpi5, rtol 1e-14; the 0.145 centre group is #1000's eight solves. Per-solve table `logs/solves_table.md` (48 rows, below).

| | xi1 0.145 | xi1 0.15 |
|---|---|---|
| counted solves (centre, dA, dw) | 8, 8, 8 | 8, 8, 8 |
| \|r_3\| of the solves | 2.2e-8 to 3.6e-7 | 6.7e-9 to 9.5e-8 |
| centre mean r_1; sigma of the centre's r_1 (trace form) | -0.1890 +0.0184i; 0.272 | -0.0879 +0.0395i; about 0.033 |
| J (Re/Im rows; A, w/w_inf), singular values | [[5222, 3287], [-4099, 9291]], 10217, 6068 | [[4483, 2296], [-4210, 9740]], 10617, 5023 |
| zero (A, w/w_inf) | **2.719248303, 1.000032951** | **2.719236758, 1.000025616** |
| standard error with J's noise (first-order; bootstrap robust scale) | **9.14e-6** (A 6.38e-6, w/w_inf 6.54e-6; 9.16e-6) | **1.64e-6** (A 1.52e-6, w/w_inf 6.0e-7; 1.63e-6) |
| centre only, J fixed (#1000's bound / propagated) | 1.58e-5 / 1.22e-5 | 2.32e-6 / 1.68e-6 |
| `m7_outer --local` with the first counted dA and dw (its estimate, noise + J term) | (2.719247, 1.000033), 8.5e-5 | (2.719237, 1.000026), 1.0e-5 |

| comparison | A | w/w_inf | norm / combined |
|---|---|---|---|
| Delta = Z(0.145) - Z(0.15) | +1.154e-5 | +7.335e-6 | 1.368e-5 |
| combined SE (quadrature of 9.14e-6 and 1.64e-6; components 6.57e-6 for w) | | 6.57e-6 | 9.29e-6 |
| **d = \|Delta\| / combined SE** | +1.76 per component | **+1.12** (w/w_inf alone) | **1.47** |

**Verdict by the rule written before the run: undecided** (1 < d = 1.47 < 3); the w/w_inf component alone is also undecided (d_w = 1.12). Mahalanobis distance with the summed covariances 1.81.
Variant beside it (not the primary): pooling win2's counted solves of #989 and #977 into each group (10, 9, 9 at both radii; `logs/analyze1002_rtol14_pooled_win2.txt`) gives zeros (2.719252120, 1.000031851) and (2.719236868, 1.000025709),
d = 1.93, Mahalanobis 2.37, A component +2.28, w/w_inf +1.16: also undecided.

What changed against #1000, and why it matters:
- The 0.15 zero here, (2.719236758, 1.000025616), agrees with Z14c (2.719234224, 1.000024742) to 2.5e-6 in A and 0.9e-6 in w/w_inf.
- The 0.145 zero moves from #1000's (2.719293175, 1.000003005) to (2.719248303, 1.000032951): **-4.5e-5 in A and +3.0e-5 in w/w_inf**. Only J changed (same centre solves). #1000's J used win2's single dA solve from #989, `dA_pert1` at 0.145,
  r_1 +0.5162 +0.5495i (|r_3| 1.8e-7), while the eight rpi5 dA solves from perturbed starts of the same end state have r_1 mean about +0.85 -0.80i, spread 0.1 to 0.15 per component. So the dA column of J in #1000 was
  (3526, 2656) and is (5222, -4099) here, and the #1000 move of w/w_inf, -2.2e-5 from Z14c, was an artifact of that one solve; the move is now +7.3e-6, under #996's 1.1e-5 and inside its SE (d_w 1.12).
- The same solve on rpi5: I reran win2's exact `dA_pert1` start (x 0.1490081795, 0.01477309871, 0.008427080476, 0.001511649065, 0.0004744319802, 0.0001217340021, from `run981_rtol14_xi0145.driver.log`) at 0.145, rtol 1e-14:
  r_1 **+0.8233 -0.6340i**, |r_3| 2.4e-7 (`logs/hier_nb_M7_rpi5_rtol14_xi0145_dA_win2start.log`), in line with rpi5's eight, not with win2's +0.5162 +0.5495i. The logs differ from the first pretune iteration
  (|r_7| 1.861e-6 on win2 against 4.045e-6 on rpi5 at `it 0` of the approach), so the two builds' rounding differs and the nested solves end at different draws of their floor noise. At 0.15 win2's `dA_pert1`
  (+0.7672 -0.7776i) agrees with rpi5's group (+0.78 -0.77i). So one win2 solve at 0.145 lies at Mahalanobis distance 11 from rpi5's dA group (its own covariance: 5 sigma in Re, 11 sigma in Im); it cannot be said from one solve whether win2's 0.145 solves differ systematically or this is a tail event.
- Which input dominates now: at 0.145 the centre's scatter (sigma 0.272, eight times 0.15's) gives 9.1e-6 of the 9.3e-6 combined SE. Projection (not a measurement; it assumes the same Delta and scatters, 0.15 as measured, with c_0, c_a and c_w as measured):

| 0.145 centre solves, dA, dw | SE at 0.145 | combined SE | d for the same Delta |
|---|---|---|---|
| 8, 8, 8 (measured) | 9.14e-6 | 9.29e-6 | 1.47 |
| 16, 8, 8 | 6.52e-6 | 6.73e-6 | 2.03 |
| 32, 8, 8 | 4.70e-6 | 4.97e-6 | 2.75 |
| 64, 8, 8 | 3.44e-6 | 3.81e-6 | 3.59 |

Not established: whether Delta (+1.2e-5 in A, +7e-6 in w/w_inf, both positive) is a radius dependence or noise; it is 1.5 combined SEs. The noise model is Gaussian scatter of r_1 from eight solves per group, and the win2 outlier above shows a tail that eight solves would not show.

## Recommended tasks (one line each; the coordinator files them)

1. **More centre solves at 0.145.** 24 more perturbed centre solves at xi1 0.145 (seeds 1050 to 1073, 32 in all; 56 for 64), rtol 1e-14, same code; acceptance: the combined SE of the radius comparison at or under 5e-6 (projection above: 4.97e-6) and d reported against 1 and 3, or the scatter does not shrink as 1/sqrt(n).
2. **Which 0.145 offset is right on win2.** Eight perturbed dA solves at 0.145 on win2 (x86), the same seeds as 1000 to 1007, so that the cross-build difference seen in `dA_pert1` is measured, not inferred from one solve; acceptance: win2's dA mean r_1 and spread against rpi5's (+0.85 -0.80i, 0.1 to 0.15), and the same for dw. Depends on #1002.

## The 48 solves

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
| 0.145 dA | 1000 | +0.9119 -0.7760i | 3.2e-7 | yes | 594 | 62 |
| 0.145 dA | 1001 | +0.7771 -0.7501i | 1.5e-7 | yes | 591 | 66 |
| 0.145 dA | 1002 | +0.8528 -0.7780i | 3.1e-7 | yes | 564 | 70 |
| 0.145 dA | 1003 | +0.8450 -0.7155i | 2.3e-7 | yes | 623 | 74 |
| 0.145 dA | 1004 | +0.7738 -0.8366i | 1.1e-7 | yes | 563 | 61 |
| 0.145 dA | 1005 | +0.9810 -1.0898i | 2.3e-7 | yes | 532 | 59 |
| 0.145 dA | 1006 | +0.8203 -0.7502i | 3.3e-7 | yes | 669 | 73 |
| 0.145 dA | 1007 | +0.8817 -0.7148i | 7.5e-8 | yes | 581 | 58 |
| 0.145 dw | 1010 | +0.1693 +0.8838i | 8.5e-8 | yes | 516 | 60 |
| 0.145 dw | 1011 | +0.0767 +1.1015i | 1.6e-7 | yes | 547 | 62 |
| 0.145 dw | 1012 | +0.2951 +0.6341i | 3.8e-8 | yes | 509 | 59 |
| 0.145 dw | 1013 | +0.0698 +1.0223i | 3.6e-7 | yes | 720 | 79 |
| 0.145 dw | 1014 | +0.1210 +1.1132i | 2.2e-8 | yes | 694 | 77 |
| 0.145 dw | 1015 | +0.1128 +0.8177i | 1.3e-7 | yes | 607 | 66 |
| 0.145 dw | 1016 | +0.2207 +1.0624i | 1.8e-7 | yes | 572 | 63 |
| 0.145 dw | 1017 | +0.0517 +0.9448i | 3.3e-7 | yes | 593 | 70 |
| 0.15 centre | 1020 | -0.0816 +0.0681i | 1.2e-8 | yes | 1005 | 102 |
| 0.15 centre | 1021 | -0.0836 +0.0199i | 1.8e-8 | yes | 579 | 68 |
| 0.15 centre | 1022 | -0.0765 +0.0058i | 7.6e-8 | yes | 772 | 86 |
| 0.15 centre | 1023 | -0.0943 +0.0376i | 4.9e-8 | yes | 726 | 82 |
| 0.15 centre | 1024 | -0.1188 +0.0413i | 5.6e-8 | yes | 700 | 82 |
| 0.15 centre | 1025 | -0.0597 +0.0107i | 7.8e-8 | yes | 601 | 67 |
| 0.15 centre | 1026 | -0.0758 +0.0553i | 4.9e-8 | yes | 736 | 80 |
| 0.15 centre | 1027 | -0.1131 +0.0775i | 2.9e-8 | yes | 576 | 63 |
| 0.15 dA | 1030 | +0.7732 -0.7718i | 1.5e-8 | yes | 721 | 82 |
| 0.15 dA | 1031 | +0.7780 -0.7669i | 2.5e-8 | yes | 618 | 74 |
| 0.15 dA | 1032 | +0.7931 -0.7719i | 2.8e-8 | yes | 565 | 61 |
| 0.15 dA | 1033 | +0.7933 -0.7924i | 9.8e-9 | yes | 984 | 104 |
| 0.15 dA | 1034 | +1.0584 -1.0583i | 6.1e-8 | yes | 780 | 94 |
| 0.15 dA | 1035 | +0.7584 -0.7489i | 9.2e-9 | yes | 604 | 69 |
| 0.15 dA | 1036 | +0.7527 -0.7411i | 5.8e-8 | yes | 638 | 75 |
| 0.15 dA | 1037 | +0.7628 -0.7679i | 5.8e-8 | yes | 677 | 79 |
| 0.15 dw | 1040 | +0.1615 +1.0289i | 8.0e-8 | yes | 728 | 81 |
| 0.15 dw | 1041 | +0.1439 +1.0204i | 3.9e-8 | yes | 855 | 92 |
| 0.15 dw | 1042 | +0.1285 +1.0096i | 5.1e-8 | yes | 631 | 70 |
| 0.15 dw | 1043 | +0.1377 +1.0266i | 6.7e-9 | yes | 768 | 86 |
| 0.15 dw | 1044 | +0.1337 +1.0259i | 6.6e-8 | yes | 724 | 87 |
| 0.15 dw | 1045 | +0.1252 +1.0252i | 4.1e-8 | yes | 736 | 82 |
| 0.15 dw | 1046 | +0.1413 +0.9953i | 5.6e-8 | yes | 573 | 61 |
| 0.15 dw | 1047 | +0.1617 +0.9760i | 9.5e-8 | yes | 737 | 85 |

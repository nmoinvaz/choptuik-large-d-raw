# I1025-macm3/kc135_d230625: k_c 135 at D 23.0625, regridded from my accepted k_c 127 state there, with its scan and secant

Machine macm3 (Apple M3, 24 GB; runner macm3b, session me2). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1025. Written 2026-11-26 18:12 UTC, **before the regrid or any scan of this folder**.

## Order (coordinator t5, hc 26 Nov, 18:08 UTC by t5's clock), verbatim
"Next lane: k_c 135 at D 23.0625, from your accepted k_c 127 state there. dh610 had it queued at the lowest priority on a loaded box; I'm stopping that copy, since you are about 5x faster. Inputs, pinned by blob: raw I1025-macm3/kc127_d230625/in/sol_l1kc127macm3d230625_D23.0625.npy (7aae10c6) and l1kc127macm3d230625.jsonl (85a685f1). The source check is kc127_syscheck_1025.py (898ebefa); the acceptance check is kc135_syscheck_1025.py at raw 576050bfc (b353d466). Folder raw I1025-macm3/kc135_d230625/, README registration first. Regrid: ell_refine.py l1kc127macm3d230625 127 l1kc135macm3d230625 135 1 23.0625 2.0990016035 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma. Then the kc135 check (exit 0, controls 1 1, the kc127 check refuses), the new scanner at lambda 0.000, 0.005, 0.010, 0.015 plus a repeat of 0.010 (2 processes), and the secant (tol 1e-5). One k_c 135 job at a time (the k_c 127 regrid peaked at 7.5 GiB). My registered prediction: +0.008 +- 0.004. If the k_c 135 root at D 23.0625 is positive, its zero also lies above 23.0625, and a leg to 23.125 follows, with win2's D 23.0 k_c 135 state as the second seed. Stop rules as before."

## Inputs (copies in `in/`; `in_blobs.txt`; the lane refuses any other blob)
| item | source | blob |
|---|---|---|
| my accepted k_c 127 state at D 23.0625 (the source) | raw `I1025-macm3/kc127_d230625/in/sol_l1kc127macm3d230625_D23.0625.npy` | 7aae10c6 |
| its record (1 row: D 23.0625, |F| 3.0829e-10, 4180 steps, psi-constraint 1.5567e-3, Delta 1.176171291295) | `l1kc127macm3d230625.jsonl` | 85a685f1 |
| source check: the k_c 127 check (accepts); refusing: the k_c 119 check and the k_c 135 check | raw `I1025-mac/checks` | 898ebefa; fc6e0dd6; b353d466 (raw 576050bfc) |
| acceptance check of the result | `kc135_syscheck_1025.py` (the k_c 111 check with 111 changed to 135 and a header comment line, as the k_c 127 check; `diff` against the k_c 127 check: the header line and three lines changed from 127 to 135, rebuilt by the lane) | b353d466 |
| readers, scanner, helpers | `read_lower.py` 89309d3c, `repeat_check.py` aaf598a9, `d18_hybsign.py` e089207a (the lane's pin only), `d185_scan_read.py` 7c9d400f, `capped_run.py` 11f0647b, `launch_1070.py` 56d15f60; scanner `d18_secant.py` eb1396ad of wip/ell1-speed 92b9bf53 (worktree `~/Source/choptuik-large-d-1025s2`); regrid worktree `~/Source/choptuik-large-d-1025m2` at 48c36355 (`ell_refine.py` 631e5801, `ell_delta.py` fde699f5; the source state and record sit in its `data/` at these blobs) | as listed |

## What differs from the k_c 127 lane (`lane135.sh` from `kc127_d230625/lane127.sh`)
(1) The one-step shift of the resolutions (111 -> 119, 119 -> 127, 127 -> 135 in every name, number and message; `diff` of the two lanes shows only that and the header comment, lines 8 on). (2) The scan: lambda 0.000, 0.005, 0.010, 0.015 plus a repeat of 0.010 (`scan_plan.env`: process 0 gets 0.010, 0.005, 0.000, process 1 the repeat of 0.010 and 0.015; 3 rounds). (3) **`summarize_point.py` here is a copy of the pinned a4da8dc4 with the lambda labels printed to 3 decimals (`%.3f` for `%.2f` in four label lines) and the repeated lambda listed once without the hard-coded -0.04** (`diff_summarize_point.txt`, base kept as `diff_base_summarize_point_a4da8dc4.py`; blob 62c57e1a): at the scan's 0.005 step the old labels would print 0.005, 0.010 and 0.015 as 0.01, 0.01 and 0.01 (the readers `read_lower.py` and `repeat_check.py` already use 3 decimals or the exact lambda and are unchanged). Checked on the k_c 127 D 23.125 data: the old and new outputs differ only in those four label lines, the old output equals the stored `point_D23.125_summary.txt`, and a mutation of the new file (a label back to `%.2f`) is detected by the same comparison. (4) The wait for memory (8 GiB available) and the 28800 s cap of the regrid are unchanged; the k_c 127 regrid peaked at 7.51 GiB, so k_c 135 may reach 9 to 10 GiB (the machine has 24 GB; alert only, as before).
Stop and report (hc to t5): a source or result not accepted, an exception (an array limit at k_c 135 included), no robust change or more than one, any step over 8 h, a secant exit other than 0 or 4 (exit 4 stands as the robust bracket, t5's ruling). Chain held (`HOLD_low2.txt`, `HOLD_refine.txt`; `scan_chain.sh` pid 99672). One k_c 135 job at a time.

## Registered (mine, information; t5's: lambda_1(135, 23.0625) = +0.008 +- 0.004, and if positive a leg to 23.125 follows)
Reference data from the files (`reg135.py` -> `reg135_output.txt`; regrid and scan numbers of the k_c 111, 119, 127 lanes at this D):
```
roots at D 23.0625: 95 -0.05862410 103 -0.02851243 111 -0.01247909 119 -0.00351666 127 +0.00364182
steps: +0.030112 +0.016033 +0.008962 +0.007158 ratios: 0.5325 0.5590 0.7987
root-step ratio 0.5: k_c 135 root +0.007221
root-step ratio 0.6: k_c 135 root +0.007937
root-step ratio 0.7: k_c 135 root +0.008653
root-step ratio 0.8: k_c 135 root +0.009369
root-step ratio 0.9: k_c 135 root +0.010084
zeros (the posted table): {87: 22.97893, 95: 23.00808, 103: 23.03011, 111: 23.04627, 119: 23.05757, 127: 23.0675} steps +0.02915 +0.02203 +0.01616 +0.01130 +0.00993 ratios 0.7557 0.7335 0.6993 0.8788
zero-step ratio 0.50: zero of k_c 135 23.07247, root at D 23.0625 by the k_c 127 slope -0.72880: +0.007262
zero-step ratio 0.60: zero of k_c 135 23.07346, root at D 23.0625 by the k_c 127 slope -0.72880: +0.007986
zero-step ratio 0.70: zero of k_c 135 23.07445, root at D 23.0625 by the k_c 127 slope -0.72880: +0.008710
zero-step ratio 0.80: zero of k_c 135 23.07544, root at D 23.0625 by the k_c 127 slope -0.72880: +0.009434
zero-step ratio 0.88: zero of k_c 135 23.07624, root at D 23.0625 by the k_c 127 slope -0.72880: +0.010013
```
| | k_c 111 | k_c 119 | k_c 127 |
|---|---|---|---|
| regrid wall | 2102 s | 2663 s | 2853 s |
| regrid peak RSS (60 s samples) | 4.78 GiB | 5.62 GiB | 7.51 GiB |
| steps ratio to the source | 1.078 | 1.071 | 1.067 |
| constraint ratio to the source | 0.694 | 0.623 | 0.686 |
| Delta shift | -6.46e-6 | -1.375e-6 | -1.878e-6 |
| secant seconds per evaluation | 391 | 480 | 581 |
| scan seconds per evaluation (2 processes) | 1469 to 1518 (4 processes) | 485 to 624 | 587 to 763 |
**The regrid.** Accepted by the k_c 135 check (exit 0, controls 1 1, the k_c 127 check refuses) 95%; no exception, no array limit 92%; steps 4443 (4180 x 1.063), within 15 of that 70%; psi-constraint about 1.0e-3, in (0.8e-3, 1.4e-3) 70%, below 1e-2 99%; |F| below 5e-10 90%; Delta shift in (-3.0e-6, -1.0e-6) 60% (the shifts have not fallen steadily); wall 2900 to 3800 s 70%; **peak RSS in (8.5, 11) GiB 70%**, above the k_c 127 regrid's 7.51 GiB 90%, below 12 GiB 90%; no memory alert (available below 2 GiB) 85%.
**lambda_1(135, 23.0625).** The ratios of the step of the root at D 23.0625 were 0.5325, 0.5590, 0.7987 and the ratios of the steps of the zero 0.7557, 0.7335, 0.6993, 0.8788 (ratios 0.5 to 0.88 give +0.0072 to +0.0101 in the file above). **My register: +0.0087 +- 0.003** (an interval from the arithmetic above, not an enclosure): within 0.003 of it 70%; positive 95% (then the k_c 135 zero lies above D 23.0625, near 23.0745 for the zero-step ratio 0.7, 23.0725 to 23.0762 over 0.5 to 0.88); exactly one robust change in 0.000 to 0.015 90% (none 5%, two or more 5%), its bracket (0.005, 0.010) 60%, (0.010, 0.015) 33%, (0.000, 0.005) 3%; all 5 evaluations noise-robust 85%; the repeat of 0.010 bit-identical 90%; the float64 sign equal to the hybrid sign at all 5: 50%; scan seconds per evaluation 700 to 950 65% (k_c 127: 587 to 763; the ratio of the last two lanes' times 1.2); scan wall 35 to 55 min 65%; peak RSS per scan process in (5.3, 6.8) GiB 65%, below 7 GiB 85%. The secant: exit 0 within 10 evaluations 55% (exit 4 40%; noise constants dln x distance at k_c 127 were 1.1e-8 to 1.8e-8), its root inside the scan's estimator range 80%, per evaluation 650 to 800 s 65% (391, 480, 581 at k_c 111, 119, 127), wall 75 to 120 min 60%, peak RSS below 7 GiB 90%.

## Status
- 2026-11-26 18:12 UTC: folder, README (registration), lane and pins written; next: pushed first, then the dry run (pins, selftests, the source check), then the lane.

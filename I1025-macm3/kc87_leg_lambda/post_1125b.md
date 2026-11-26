**#1025 macm3, threshold table: lambda_1 at D 23.0 and 23.0625 for k_c 87, 95 and 103 (secant values), the zeros by linear interpolation, the steps in k_c; with the k_c 87 scans of D 22.5 to 23.0, part c2's stop, the k_c 103 regrid, scan and leg (2026-11-26 02:11 UTC).** One comment for everything since the 12:00 UTC post (7161793986), as ordered (t5, hc 26 Nov: "post on #1025 the threshold table: lambda_1 at D 23.0 and 23.0625 for k_c 87, 95 and 103 (all secant values), the zero by linear interpolation per k_c, and the steps in k_c"). Positions are the reader's printed brackets with the det-linear estimate; the estimator range is a spread over interpolation choices, not an enclosure; the printed orientation is the sign order in that state, and the sign convention differs between states (freeze orientation), so only the places of changes are compared across states.

### lambda_1 of my k_c 87 leg at D 22.25 and from D 22.5 to 23.0 (reading B, t5's ruling)


t5's ruling (hc ~18:50 UTC, quoted): "lambda_1 runs 0.4425 (22.25), 0.216 (22.75), 0.167 (22.8125), 0.128 (22.875), 0.056 (22.9375), -0.0215 (23.0) ... The newcomer runs >0.50 (22.8125), 0.162 (22.875), -0.226 (22.9375), slopes < -5.4 and -6.2, a steady fast dive like S." D 22.5 and D 22.625 are labeled lambda_1 by continuity (t5, ~21:05 UTC: "D 22.625 is lambda_1 (0.296, by continuity)"). `roots87.txt` holds one F line per D (read by the chain) and `#N` comment lines for the newcomer.


| D | lambda_1 (scan det-linear; the secant values of D 22.9375 and 23.0 are in the threshold table below) | bracket | newcomer (`#N`) |
|---|---|---|---|
| 22.25 | **0.442516** | 0.440 to 0.445 |  |
| 22.5 | **0.339638** | 0.300 to 0.340 |  |
| 22.625 | **0.296107** | 0.260 to 0.300 |  |
| 22.75 | **0.216086** | 0.210 to 0.220 |  |
| 22.8125 | **0.166991** | 0.160 to 0.170 | above 0.50 (no root up to 0.50) |
| 22.875 | **0.127834** | 0.120 to 0.130 | 0.162334 (bracket 0.160 to 0.170) |
| 22.9375 | **0.056199** | 0.040 to 0.060 | -0.226429 (bracket -0.260 to -0.220) |
| 23.0 | **-0.021546** | -0.040 to -0.020 |  |


Slopes of lambda_1 per unit D between consecutive rows: 22.25 to 22.5: -0.412, 22.5 to 22.625: -0.348, 22.625 to 22.75: -0.640, 22.75 to 22.8125: -0.786, 22.8125 to 22.875: -0.627, 22.875 to 22.9375: -1.146, 22.9375 to 23.0: -1.244.


**Zero of lambda_1 at k_c 87 by arithmetic on the last two rows (a straight line, not a result):** D 22.9827 (slope -1.2439 over 22.9375 to 23.0). The leg's guard stopped part c2 at D 23.0 (below).


### What was scanned, and what each scan read


All on the pinned k_c 87 states of my leg (raw `I1025-macm3/kc87_leg2/c/`, `c2/`, `b2/`), `d18_hybsign.py` e089207a, `read_lower.py` 89309d3c, repeats by `repeat_check.py` aaf598a9 (the repeat check passes in all 27 readings of these folders, own and merged). Each row is the folder's own window; the second table is the merged reading when scans of one D were joined (the extension rule: a window without a robust change is extended by its width on the side the orientation read at the nearest scanned point of the same part points to; t5, hc ~12:10 and ~14:43 UTC).


| scan folder (`kc87_leg_lambda/`) | D | lambda window | evaluations | noise-robust | robust changes of its own window: bracket, orientation as printed, det-linear (estimator range) |
|---|---|---|---|---|---|
| `22.875` | 22.875 | 0.1 to 0.16 | 8 | 8 | (0.120, 0.130), - to +, **0.127834** ([0.123345, 0.127834]) |
| `22.875_wide` | 22.875 | -0.1 to 0.3 | 16 | 16 | none |
| `22.875_F` | 22.875 | 0.17 to 0.19 | 4 | 4 | none |
| `22.875_up` | 22.875 | 0.3 to 0.5 | 7 | 7 | none |
| `22.8125` | 22.8125 | 0.17 to 0.23 | 8 | 8 | (0.160, 0.170), - to +, **0.166991** ([0.163666, 0.166991]) |
| `22.8125_ext` | 22.8125 | 0.11 to 0.16 | 7 | 7 | none |
| `22.8125_F` | 22.8125 | 0.24 to 0.4 | 10 | 10 | none |
| `22.8125_F2` | 22.8125 | 0.42 to 0.5 | 6 | 6 | none |
| `22.75` | 22.75 | 0.18 to 0.24 | 8 | 8 | (0.210, 0.220), - to +, **0.216086** ([0.212991, 0.216086]) |
| `22.75_both` | 22.75 | -0.1 to 0.5 | 32 | 32 | (0.200, 0.220), - to +, **0.218419** ([0.204115, 0.218419]) |
| `22.9375` | 22.9375 | -0.1 to 0.3 | 22 | 22 | (0.040, 0.060), + to -, **0.056199** ([0.043573, 0.056199]) |
| `22.9375_low` | 22.9375 | -0.5 to -0.1 | 12 | 12 | (-0.260, -0.220), - to +, **-0.226429** ([-0.259451, -0.226429]) |
| `23.0` | 23.0 | -0.1 to 0.3 | 22 | 22 | (-0.040, -0.020), + to -, **-0.021546** ([-0.035344, -0.021546]) |
| `23.0_low` | 23.0 | -0.5 to -0.1 | 12 | 12 | none |
| `22.5_both` | 22.5 | -0.1 to 0.5 | 17 | 17 | (0.300, 0.340), + to -, **0.339638** ([0.301631, 0.339638]) |
| `22.625_both` | 22.625 | -0.1 to 0.5 | 17 | 17 | (0.260, 0.300), + to -, **0.296107** ([0.260787, 0.296107]) |


**Merged readings per D (the readings the labels rest on):**


| merged reading (`read_lower_merged.txt` of) | folders merged | window | points | robust changes: bracket, orientation as printed, det-linear (estimator range) | sign pattern |
|---|---|---|---|---|---|
| `22.875_wide` | 22.875, 22.875_wide (24 evaluations) | -0.100 to 0.300 | 22 | (0.120, 0.130), - to +, **0.127834** ([0.123345, 0.127834]); (0.160, 0.200), + to -, **0.171403** ([0.161208, 0.171403]) | -[-0.100..0.120] +[0.130..0.160] -[0.200..0.300] |
| `22.875_F` | 22.875, 22.875_wide, 22.875_F (28 evaluations) | -0.100 to 0.300 | 25 | (0.120, 0.130), - to +, **0.127834** ([0.123345, 0.127834]); (0.160, 0.170), + to -, **0.162334** ([0.161448, 0.162334]) | -[-0.100..0.120] +[0.130..0.160] -[0.170..0.300] |
| `22.875_up` | 22.875, 22.875_wide, 22.875_F, 22.875_up (35 evaluations) | -0.100 to 0.500 | 30 | (0.120, 0.130), - to +, **0.127834** ([0.123345, 0.127834]); (0.160, 0.170), + to -, **0.162334** ([0.161448, 0.162334]) | -[-0.100..0.120] +[0.130..0.160] -[0.170..0.500] |
| `22.8125_ext` | 22.8125, 22.8125_ext (15 evaluations) | 0.110 to 0.230 | 13 | (0.160, 0.170), - to +, **0.166991** ([0.163666, 0.166991]) | -[0.110..0.160] +[0.170..0.230] |
| `22.8125_F` | 22.8125, 22.8125_ext, 22.8125_F (25 evaluations) | 0.110 to 0.400 | 22 | (0.160, 0.170), - to +, **0.166991** ([0.163666, 0.166991]) | -[0.110..0.160] +[0.170..0.400] |
| `22.8125_F2` | 22.8125, 22.8125_ext, 22.8125_F, 22.8125_F2 (31 evaluations) | 0.110 to 0.500 | 27 | (0.160, 0.170), - to +, **0.166991** ([0.163666, 0.166991]) | -[0.110..0.160] +[0.170..0.500] |
| `22.75_both` | 22.75, 22.75_both (40 evaluations) | -0.100 to 0.500 | 34 | (0.210, 0.220), - to +, **0.216086** ([0.212991, 0.216086]) | -[-0.100..0.210] +[0.220..0.500] |
| `22.9375_low` | 22.9375, 22.9375_low (34 evaluations) | -0.500 to 0.300 | 31 | (-0.260, -0.220), - to +, **-0.226429** ([-0.259451, -0.226429]); (0.040, 0.060), + to -, **0.056199** ([0.043573, 0.056199]) | -[-0.500..-0.260] +[-0.220..0.040] -[0.060..0.300] |
| `23.0_low` | 23.0, 23.0_low (34 evaluations) | -0.500 to 0.300 | 31 | (-0.040, -0.020), + to -, **-0.021546** ([-0.035344, -0.021546]) | +[-0.500..-0.040] -[-0.020..0.300] |
| `22.5_both` | 22.5_both (17 evaluations) | -0.100 to 0.500 | 16 | (0.300, 0.340), + to -, **0.339638** ([0.301631, 0.339638]) | +[-0.100..0.300] -[0.340..0.500] |
| `22.625_both` | 22.625_both (17 evaluations) | -0.100 to 0.500 | 16 | (0.260, 0.300), + to -, **0.296107** ([0.260787, 0.296107]) | +[-0.100..0.260] -[0.300..0.500] |


### The two-root story (what I got wrong, and how it was resolved)


Several labelings were tried before reading B. (1) By order: the lower root of a pair as L and the upper as F; the wide scan at D 22.875 showed two roots there (merged table) and one at D 22.8125, so "upper = F" was wrong. (2) The direction of an extension came from a template: the first extension chosen that way (D 22.8125, up) was wrong and was cancelled by exact pids, and the rule now reads the orientation of the nearest scanned point of the same part (t5, hc ~14:43 UTC). (3) The registered orientations of D 23.0, D 22.9375, D 22.875 (narrow), D 22.8125 (extension) and D 22.5 were wrong, because the sign convention differs between states. (4) t5's hypothesis that lambda_1 is the lower track was tested by the D 22.75 both-roots scan (one root, 0.216086) and the negative scans of D 22.9375 (the newcomer at -0.226429) and D 23.0 (no change in -0.50 to -0.10, as expected with the newcomer below -0.5); it became reading B. Labels by order are off (`LABELS_FROZEN.txt`); later roots are labeled by continuity and t5 rules pairs.


### Part c2 (k_c 87, past the 1e-2 psi-constraint bar, `--cmax 2e-2`): rows and the guard's stop


| D | Delta | dDelta/dD | sigma_reg | J+dF/dn | h | next h | constraint | F | steps | s | n_null | cutoff | max cos_t_reg |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 22.9375 | 1.172558374817 | 0.029444 | 2.9851e-11 | 0.9931 | 0.0625 | 0.0625 | 1.021e-02 | 3.551e-10 | 2865 | 2292 | 79 | 1.673e-11 | 0.4243 |
| 23 | 1.174405949373 | 0.029561 | 3.5796e-11 | 0.9798 | 0.0625 | 0.0625 | 1.050e-02 | 3.497e-10 | 2864 | 1374 | 79 | 1.685e-11 | 0.5096 |

**Guard (`leap_guard.py` f1fe7c7c, unchanged):** `STOP at D 23: max cos_t_reg 0.5096 >= 0.5; leap root pid 73104: killed; 2026-11-25 12:02:42 UTC` Both rows are above the 1e-2 bar: **REDUCED QUALITY** (1.021e-2 and 1.050e-2). The max cos_t_reg is on the third regular mode, as lambda_1 neared zero; win2's k_c 95 leg stopped by the same rule at D 23.0625 (cos 0.5997).


### k_c 103 at D 23.0 (t5's order, hc ~21:05 UTC): regrid of win2's k_c 95 state, scan -0.06 to 0.06, secant refinement


Raw `I1025-macm3/kc103_d23/` (README first, raw 74ae248c5; scored entries in it). Source: win2's accepted k_c 95 state at D 23.0 (raw `I1025-win2/kc95_d23`, blob 096f1cc0, record e3fff23f; **REDUCED QUALITY lineage**, k_c 95 constraint 7.67e-3). Regrid (`ell_refine.py` 631e5801, dh170's recipe, 6 threads): accepted 21:42:31 UTC by `kc103_syscheck_1025.py` (3ab58d16; controls `--mutate=F` and `--mutate=steps` exit 1 1; the k_c 95 check refuses the result): |F| 3.2905e-10, 3389 steps, psi-constraint 5.0299e-03 (below 1e-2), Delta 1.174332548928 (k_c 95 source 1.174346963414: shift -1.4414e-05), wall 1391 s (registered 4000 to 6500 s: the one miss of the lane).


**lambda_1 at D 23.0 by k_c from the scans alone (det-linear, before the refinements below; k_c 87: my scan `23.0`; k_c 95: win2's, ruled by t5, comment 7173193613; k_c 103: this scan):**

| k_c | scan det-linear | bracket and estimator range |
|---|---|---|
| 87 | **-0.021546** | (-0.040, -0.020), range [-0.035344, -0.021546] |
| 95 | **0.015921** | win2: (0.000, 0.020), range [0.002668, 0.015921] |
| 103 | **0.028275** (scan, det-linear) | (0.020, 0.030), range [0.023982, 0.028275] |


**Scan (14 evaluations, 4 processes, 66.6 min; `score_scan.py`):**
```
evaluations 14, noise-robust 14
float64 sign equals the hybrid sign at 14 of 14
repeat of 0.00 bit-identical (ln, f64_ln, sign): True
signs by lambda: -0.06- -0.05- -0.04- -0.03- -0.02- -0.01- 0.00- 0.00- 0.01- 0.02- 0.03+ 0.04+ 0.05+ 0.06+
ln|det| by lambda: 0.00:-2937.303 0.00:-2937.303 0.01:-2938.724 0.02:-2940.601 0.03:-2942.169 0.04:-2941.765 0.05:-2942.158 0.06:-2942.751
memory: 248 samples, lowest available 9.4 GiB (alert below 2 GiB, alert.log exists: False), peak RSS per process GiB {'98706': 5.23, '98738': 6.35, '98746': 3.78, '98764': 3.97}
scan wall 3996 s = 66.6 min (2026-11-25 21:42:43 to 2026-11-25 22:49:19 UTC)
root k_c 103: bracket (0.020, 0.030), - to +, det-linear 0.028275, estimator range [0.023982, 0.028275] (a spread, not an enclosure)
k_c 87 -0.021546, k_c 95 0.015921, k_c 103 0.028275: steps 87->95 +0.037467, 95->103 +0.012354, ratio 0.3297
arithmetic only, not a result: room below +0.03 is 0.001725, i.e. 0.140 of the last step; a geometric tail of the observed ratio would end at 0.0344
predictions: root in (0.016,0.060): True; in (-0.030,0.030): True; |root-0.030|<0.015: True; step positive: True; step below +0.0374: True
```


**Secant refinement of the k_c 103 bracket (0.020, 0.030)** (`d18_secant.py` a3d90cd5 of wip/ell1-speed 6010e37b, controls as in SPEED_ELL1.md: selftest exit 0, `half`, `norobust`, `nosigncheck` exit 1 each; `--tol=1e-5 --maxev=10`, one process; venv-macm3-1058b stands in for `venv-1025dd`, which is not on this machine, t5 accepted it):
```
status tol (-), tol 1e-05, evaluations 7 (the two ends included), run wall 3077 s
root bracket [0.02650441, 0.02650941], width 5.000e-06, signs [-1.0, 1.0], robust [True, True]
root (det-linear inside the final bracket) 0.02650535; Brent's last point 0.02650441
scan reading: det-linear 0.028275, estimator range [0.023982, 0.028275]
root inside the estimator range [0.023982, 0.028275] (bracket and det-linear root): True; whole final bracket inside: True; below the scan's det-linear 0.028275: True
evals: 0.02000000 -1 ln -2940.601239 dln 7.17e-06 robust True 319 s [26, 288, 5]; 0.03000000 +1 ln -2942.169471 dln 1.29e-05 robust True 409 s [27, 375, 7]; 0.02827531 +1 ln -2942.686438 dln 2.56e-05 robust True 440 s [46, 387, 7]; 0.02600917 -1 ln -2943.743597 dln 9.21e-05 robust True 450 s [42, 401, 7]; 0.02659350 +1 ln -2945.526842 dln 5.17e-04 robust True 441 s [46, 389, 7]; 0.02650941 +1 ln -2948.595204 dln 1.12e-02 robust True 474 s [46, 421, 8]; 0.02650441 -1 ln -2950.061810 dln 4.99e-02 robust True 544 s [67, 469, 8]
ends: lambda 0.02: secant ln -2940.601239 sign -1, scan ln -2940.601242 sign -1, |d ln| 3.026e-06 (the float64 M by ell_fastm against the complex step; SPEED_ELL1.md saw 2.7e-5 and 1.5e-3 at k_c 103)
ends: lambda 0.02 float64 sign -1 (scan -1)
ends: lambda 0.03: secant ln -2942.169471 sign +1, scan ln -2942.169471 sign +1, |d ln| 7.238e-07 (the float64 M by ell_fastm against the complex step; SPEED_ELL1.md saw 2.7e-5 and 1.5e-3 at k_c 103)
ends: lambda 0.03 float64 sign -1 (scan +1)
dln largest 4.989e-02, per evaluation seconds [319, 409, 440, 450, 441, 474, 544], mean 440 s
memory: 104 samples, lowest available 11.9 GiB, peak RSS 3.45 GiB, alert.log absent
```


### lambda_1 at D 23.0 at three k_c (the three-k_c table, t5's order)

Same tool (`d18_secant.py` a3d90cd5), `--tol=1e-5 --maxev=10`, one process per case, pinned by blob (README `kc_d23_secant/`, registered first, raw df6eaf448; k_c 103 in `kc103_d23/`). k_c 87 is my part c2 state (**REDUCED QUALITY**, psi-constraint 1.0496e-2); k_c 95 is win2's accepted state (source lineage reduced quality, k_c 95 constraint 7.67e-3); k_c 103 is my regrid of it (5.03e-3).

| k_c | scan det-linear | scan estimator range (a spread) | secant root (det-linear in the final bracket) | final bracket (width) | evaluations, wall | inside the range |
|---|---|---|---|---|---|---|
| 87 | -0.021546 | [-0.035344, -0.021546] | **-0.02540417** | [-0.02540491, -0.02539991] (5.0e-06) | 8, 3212 s | True |
| 95 | 0.015921 | [0.002668, 0.015921] | **0.00870734** | [0.00796052, 0.00873919] (7.8e-04) | 7, 3453 s | True |
| 103 | 0.028275 | [0.023982, 0.028275] | **0.02650535** | [0.02650441, 0.02650941] (5.0e-06) | 7, 3077 s | True |

Refined steps in k_c: 87 to 95 +0.034112, 95 to 103 +0.017798 (ratio 0.522); the unrefined det-linear numbers gave +0.037467 and +0.012354 (ratio 0.330). Arithmetic only, not a result: a geometric tail with the refined ratio would end at 0.0459 (t5's register: a converged lambda_1 between -0.03 and +0.03).


**k_c 95 stands as a robust bracket, not a root to 1e-5.** Its tool exit was 4 (status nonrobust): the 7th evaluation, 2.1e-6 from the det-linear root, had sign + with both noise signs +, but dln 0.26 above the tool's bar 0.1, so the run stopped on **[0.00796052, 0.00873919]** (width 7.787e-4, both ends robust). t5's ruling (hc, 26 Nov, after both readings): "no rerun with --dln=inf or a smaller eps: that would accept a sign the noise test rejects. The k_c 95 result stands as the robust bracket [0.00796, 0.00874] (width 7.8e-4), which is far below the k_c steps of 1.8e-2 that matter." The k_c 95 row of the table is the det-linear root inside that bracket and carries its width. t5's note says the hybrid sign is noise-limited within about 4e-4 of the root at k_c 95. From the files (`kc_d23_secant/noise_vs_distance.txt`, below), dln times the distance from the root is constant to 2% in each case, so dln reaches the bar 0.1 about 4e-7 from the root at k_c 95 (7e-8 at k_c 87, 4.6e-7 at k_c 103); the bracket is 7.8e-4 wide because Brent's last interior point fell inside that zone, and 3.9e-4 is the bracket's half-width. Both statements are recorded; the ruling is followed as given.


**Secant refinement at k_c 87, D 23.0:**
```
scan: 22 evaluations, 22 noise-robust; robust changes 1: (-0.040, -0.020) + to - det-linear -0.021546 range [-0.035344, -0.021546]
signs by lambda: -0.10+ -0.08+ -0.06+ -0.04+ -0.02- 0.00- 0.02- 0.04- 0.06- 0.08- 0.10- 0.10- 0.12- 0.14- 0.16- 0.18- 0.20- 0.22- 0.24- 0.26- 0.28- 0.30-
float64 sign equals the hybrid sign at 22 of 22
repeat of 0.10 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.10:-2331.335 -0.08:-2333.128 -0.06:-2335.066 -0.04:-2337.413 -0.02:-2339.893 0.00:-2339.833 0.02:-2340.742 0.04:-2341.868 0.06:-2343.094 0.08:-2344.377 0.10:-2345.699 0.10:-2345.699 0.12:-2347.048 0.14:-2348.417 0.16:-2349.803 0.18:-2351.201 0.20:-2352.610 0.22:-2354.028 0.24:-2355.454 0.26:-2356.887 0.28:-2358.326 0.30:-2359.770
secant: status tol (-), tol 1e-05, evaluations 8 (the two ends included), run wall 3212 s
secant root bracket [-0.02540491, -0.02539991], width 5.000e-06, signs [1.0, -1.0], robust [True, True]; det-linear root -0.02540417; Brent's last point -0.02540491
scan reading: bracket (-0.040, -0.020), det-linear -0.021546, estimator range [-0.035344, -0.021546]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda -0.04: secant ln -2337.413233 sign +1, scan ln -2337.413236 sign +1, |d ln| 2.472e-06
end lambda -0.02: secant ln -2339.892814 sign -1, scan ln -2339.892813 sign -1, |d ln| 4.553e-07
evals: -0.04000000 +1 ln -2337.413233 dln 2.39e-07 robust True 408 s; -0.02000000 -1 ln -2339.892814 dln 1.73e-06 robust True 411 s; -0.02154604 -1 ln -2340.114861 dln 2.30e-06 robust True 403 s; -0.02737327 +1 ln -2340.354341 dln 3.45e-06 robust True 407 s; -0.02480688 -1 ln -2341.738014 dln 1.27e-05 robust True 407 s; -0.02532123 -1 ln -2343.674286 dln 8.98e-05 robust True 397 s; -0.02540491 +1 ln -2348.386187 dln 1.01e-02 robust True 405 s; -0.02539991 -1 ln -2346.630034 dln 1.73e-03 robust True 375 s
dln largest 1.007e-02, mean seconds per evaluation 402
secant memory: 107 samples, lowest available 10.4 GiB, peak RSS 2.86 GiB
```


**Secant refinement at k_c 95, D 23.0:**
```
scan: 20 evaluations, 20 noise-robust; robust changes 1: (0.000, 0.020) + to - det-linear 0.015921 range [0.002668, 0.015921]
signs by lambda: -0.06+ -0.04+ -0.02+ 0.00+ 0.02- 0.04- 0.06- 0.08- 0.10- 0.10- 0.12- 0.14- 0.16- 0.18- 0.20- 0.22- 0.24- 0.26- 0.28- 0.30-
float64 sign equals the hybrid sign at 20 of 20
repeat of 0.10 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.06:-2630.607 -0.04:-2632.565 -0.02:-2634.711 0.00:-2637.523 0.02:-2638.885 0.04:-2639.491 0.06:-2640.623 0.08:-2641.923 0.10:-2643.306 0.10:-2643.306 0.12:-2644.740 0.14:-2646.209 0.16:-2647.702 0.18:-2649.215 0.20:-2650.743 0.22:-2652.283 0.24:-2653.833 0.26:-2655.392 0.28:-2656.959 0.30:-2658.532
secant: status nonrobust (not robust at 0.008705218053500247), tol 1e-05, evaluations 7 (the two ends included), run wall 3453 s
secant root bracket [0.00796052, 0.00873919], width 7.787e-04, signs [1.0, -1.0], robust [True, True]; det-linear root 0.00870734; Brent's last point 0.00873919
scan reading: bracket (0.000, 0.020), det-linear 0.015921, estimator range [0.002668, 0.015921]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda 0.00: secant ln -2637.523314 sign +1, scan ln -2637.523344 sign +1, |d ln| 2.978e-05
end lambda 0.02: secant ln -2638.885112 sign -1, scan ln -2638.885102 sign -1, |d ln| 9.493e-06
evals: 0.00000000 +1 ln -2637.523314 dln 4.63e-06 robust True 526 s; 0.02000000 -1 ln -2638.885112 dln 3.24e-06 robust True 522 s; 0.01592103 -1 ln -2639.002143 dln 5.18e-06 robust True 523 s; 0.00796052 +1 ln -2640.627222 dln 5.21e-05 robust True 518 s; 0.00927007 -1 ln -2641.010278 dln 6.83e-05 robust True 522 s; 0.00873919 -1 ln -2643.782141 dln 1.14e-03 robust True 517 s; 0.00870522 +1 ln -2649.341267 dln 2.60e-01 robust False 325 s
dln largest 2.605e-01, mean seconds per evaluation 493
secant memory: 115 samples, lowest available 10.1 GiB, peak RSS 2.91 GiB
```


**Noise against distance, all three refinements:**
```
dln (largest change of ln|det| under the 1e-15 noise test) against the distance of each evaluation from the det-linear root of its final bracket; robust = noise signs equal and dln <= 0.1
k_c 87: root -0.02540417 (tol)
   lambda -0.02540491 distance 7.36e-07 dln 1.01e-02 robust True
   lambda -0.02539991 distance 4.26e-06 dln 1.73e-03 robust True
   lambda -0.02532123 distance 8.29e-05 dln 8.98e-05 robust True
   lambda -0.02480688 distance 5.97e-04 dln 1.27e-05 robust True
   lambda -0.02737327 distance 1.97e-03 dln 3.45e-06 robust True
   lambda -0.02154604 distance 3.86e-03 dln 2.30e-06 robust True
   lambda -0.02000000 distance 5.40e-03 dln 1.73e-06 robust True
   lambda -0.04000000 distance 1.46e-02 dln 2.39e-07 robust True
k_c 95: root 0.00870734 (nonrobust)
   lambda 0.00870522 distance 2.12e-06 dln 2.60e-01 robust False
   lambda 0.00873919 distance 3.18e-05 dln 1.14e-03 robust True
   lambda 0.00927007 distance 5.63e-04 dln 6.83e-05 robust True
   lambda 0.00796052 distance 7.47e-04 dln 5.21e-05 robust True
   lambda 0.01592103 distance 7.21e-03 dln 5.18e-06 robust True
   lambda 0.00000000 distance 8.71e-03 dln 4.63e-06 robust True
   lambda 0.02000000 distance 1.13e-02 dln 3.24e-06 robust True
k_c 103: root 0.02650535 (tol)
   lambda 0.02650441 distance 9.37e-07 dln 4.99e-02 robust True
   lambda 0.02650941 distance 4.06e-06 dln 1.12e-02 robust True
   lambda 0.02659350 distance 8.81e-05 dln 5.17e-04 robust True
   lambda 0.02600917 distance 4.96e-04 dln 9.21e-05 robust True
   lambda 0.02827531 distance 1.77e-03 dln 2.56e-05 robust True
   lambda 0.03000000 distance 3.49e-03 dln 1.29e-05 robust True
   lambda 0.02000000 distance 6.51e-03 dln 7.17e-06 robust True
```


### The k_c 103 leg (t5's order, step 2)


Raw `I1025-macm3/kc103_leg/` (README with the registration first, raw 817384bb7; scored entries in it). `ell_leap.py` (5816d7b3, worktree edf49057) at k_c 103 from winb's accepted D 22.875 state (raw `I1025-win/kc103_d22875`, blob 28051531; record blob 8559e6ab, the LF form of his marker's f623d3e6) and my D 23.0 state (845e92a5), h 0.0625, to D 23.125, `--tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold`, 6 threads, guard `leap_guard.py` f1fe7c7c unchanged. Both seeds accepted by the k_c 103 check (controls 1 1) and refused by the k_c 95 and k_c 87 checks. Started 2026-11-25 23:05:27 UTC. **The guard stopped the leg at its first point** (t5's rule: scan that point and stop there):
```
D 23.0625: Delta 1.176181006312 (Delta_pred 1.176170963495), dDelta/dD 0.029575, |F| 3.2018e-10 (F_start 5.767e-05), steps 3390, psi-constraint 5.2472e-03, n_null 95, h 0.0625, leap seconds 1822, tan_norm 1.1283
  weak regular values ['2.0169e-11', '6.1525e-11', '1.2096e-10', '6.1027e-10'], tangent cosines ['0.2335', '0.0980', '0.5776', '0.2221'] (largest on the regular mode #3), delta_reg ['0.0106', '0.0109', '0.0081', '0.2957']
  seeds' slope dDelta/dD 0.029415 (A to B); Delta in [1.17612, 1.17624]: True; dDelta/dD in [0.0292, 0.0300]: True; constraint in (4.9e-3, 5.8e-3): True, below 1e-2: True; steps within 15 of 3391: True; |F| <= 5e-10: True; n_null == 95: True, within 2: True; seconds in [2000, 6000]: False
STOP file: STOP at D 23.0625: max cos_t_reg 0.5776 >= 0.5; leap root pid 19389: killed; 2026-11-25 23:39:05 UTC
leap exit 137 (137 = killed by the guard's exact-pid stop), wall 2093 s, Tracebacks 0, halvings: none (h stays 0.0625)
memory: 34 samples, lowest available 12.5 GiB, peak RSS of the leap 4.09 GiB, alert.log exists: False
```


**D 23.0625 at k_c 103: scan -0.10 to 0.02 by 0.02 plus a repeat of -0.04 (`kc87_leg_lambda/23.0625_kc103/`), then the secant refinement of its bracket** (the point was accepted first: `kc103_syscheck_1025.py` exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the k_c 95 and k_c 87 checks refuse it):
```
scan: 8 evaluations, 8 noise-robust; robust changes 1: (-0.040, -0.020) - to + det-linear -0.022006 range [-0.037553, -0.022006]
signs by lambda: -0.10- -0.08- -0.06- -0.04- -0.04- -0.02+ 0.00+ 0.02+
float64 sign equals the hybrid sign at 8 of 8
repeat of -0.04 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.10:-2918.244 -0.08:-2920.464 -0.06:-2922.848 -0.04:-2925.750 -0.02:-2927.944 0.00:-2928.630 0.02:-2929.995
secant: status tol (-), tol 1e-05, evaluations 9 (the two ends included), run wall 2927 s
secant root bracket [-0.02851654, -0.02851154], width 5.000e-06, signs [-1.0, 1.0], robust [True, True]; det-linear root -0.02851243; Brent's last point -0.02851154
scan reading: bracket (-0.040, -0.020), det-linear -0.022006, estimator range [-0.037553, -0.022006]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda -0.04: secant ln -2925.750103 sign -1, scan ln -2925.750103 sign -1, |d ln| 5.206e-07
end lambda -0.02: secant ln -2927.944059 sign +1, scan ln -2927.944064 sign +1, |d ln| 4.499e-06
evals: -0.04000000 -1 ln -2925.750103 dln 5.11e-06 robust True 391 s; -0.02000000 +1 ln -2927.944059 dln 6.38e-06 robust True 318 s; -0.02200589 +1 ln -2928.022758 dln 8.42e-06 robust True 318 s; -0.03100295 -1 ln -2928.130873 dln 2.28e-05 robust True 317 s; -0.02674736 +1 ln -2928.878242 dln 3.16e-05 robust True 316 s; -0.02811508 +1 ln -2930.239819 dln 1.41e-04 robust True 316 s; -0.02853533 -1 ln -2933.053284 dln 2.46e-03 robust True 317 s; -0.02851154 +1 ln -2936.308891 dln 6.15e-02 robust True 317 s; -0.02851654 -1 ln -2934.776892 dln 1.38e-02 robust True 317 s
dln largest 6.153e-02, mean seconds per evaluation 325
secant memory: 97 samples, lowest available 12.9 GiB, peak RSS 4.01 GiB
```


**lambda_1 at k_c 103 against D (secant roots):** D 23.0 0.02650535, D 23.0625 -0.02851243; slope -0.8803 per unit D (t5's register: about -0.8, 0.028 at 23.0, lambda_1(23.0625) about -0.022); the straight line through them crosses zero at **D 23.0301** (arithmetic on two points, not a result; t5's register: between 23.0 and 23.0625; k_c 87 by the same arithmetic on its unrefined scanned rows: D 22.9827; its secant roots give the value in the threshold table below).


### Threshold table: lambda_1 at two D for k_c 87, 95 and 103 (secant values), the zero by linear interpolation, the steps in k_c (t5's order)


Every root is the det-linear root inside the final bracket of `d18_secant.py` (a3d90cd5, `--tol=1e-5 --maxev=10`, pinned by blob, one process per case, venv-macm3-1058b); the bracket is in square brackets (k_c 95 at D 23.0 and at D 23.0625 stopped on a non-robust interior point, exit 4, so they are robust brackets, widths 7.8e-4 and 1.4e-3, by t5's ruling; the other four brackets are 5e-6 wide). The zero is the straight line through the two roots (arithmetic on two points, not a result); its range is the spread over the bracket ends (not an enclosure). k_c 87 has no state at D 23.0625 (my part c2 ended at D 23.0 by the guard), so its second D is D 22.9375 (t5's order).


| k_c | D pair used | lambda_1 (secant root [final bracket]) at the two D | slope per unit D | zero in D | range of the zero over the bracket ends |
|---|---|---|---|---|---|
| 87 | **22.9375 and 23.0** | D 22.9375: **0.04995785** [0.04995608, 0.04996108]; D 23.0: **-0.02540417** [-0.02540491, -0.02539991] | -1.20579 | **22.97893** | 22.97893 to 22.97893 |
| 95 | **23.0 and 23.0625** | D 23.0: **0.00870734** [0.00796052, 0.00873919]; D 23.0625: **-0.05862410** [-0.06000000, -0.05857558] | -1.07730 | **23.00808** | 23.00732 to 23.00811 |
| 103 | **23.0 and 23.0625** | D 23.0: **0.02650535** [0.02650441, 0.02650941]; D 23.0625: **-0.02851243** [-0.02851654, -0.02851154] | -0.88028 | **23.03011** | 23.03011 to 23.03011 |


**Steps in k_c of the zero:** 87 to 95 +0.02915 in D, 95 to 103 +0.02203 (ratio 0.756; arithmetic only, not a result: the same ratio for every later step of 8 in k_c would put the limit of the zero at D 23.0982). At D 23.0 (the common D) the roots step +0.034112 (87 to 95) and +0.017798 (95 to 103), ratio 0.522; at D 23.0625 only 95 to 103 exists: +0.030112.


**Secant refinement at k_c 87 at D 22.9375 (my part c2 state, REDUCED QUALITY, psi-constraint 1.0213e-2; exit 0):**
```
scan: 22 evaluations, 22 noise-robust; robust changes 1: (0.040, 0.060) + to - det-linear 0.056199 range [0.043573, 0.056199]
signs by lambda: -0.10+ -0.08+ -0.06+ -0.04+ -0.02+ 0.00+ 0.02+ 0.04+ 0.06- 0.08- 0.10- 0.10- 0.12- 0.14- 0.16- 0.18- 0.20- 0.22- 0.24- 0.26- 0.28- 0.30-
float64 sign equals the hybrid sign at 22 of 22
repeat of 0.10 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.10:-2338.785 -0.08:-2340.323 -0.06:-2341.899 -0.04:-2343.521 -0.02:-2345.203 0.00:-2346.979 0.02:-2348.937 0.04:-2351.491 0.06:-2352.940 0.08:-2353.308 0.10:-2354.265 0.10:-2354.265 0.12:-2355.400 0.14:-2356.624 0.16:-2357.902 0.18:-2359.216 0.20:-2360.558 0.22:-2361.920 0.24:-2363.298 0.26:-2364.690 0.28:-2366.093 0.30:-2367.506
secant: status tol (-), tol 1e-05, evaluations 8 (the two ends included), run wall 1834 s
secant root bracket [0.04995608, 0.04996108], width 5.000e-06, signs [1.0, -1.0], robust [True, True]; det-linear root 0.04995785; Brent's last point 0.04995608
scan reading: bracket (0.040, 0.060), det-linear 0.056199, estimator range [0.043573, 0.056199]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda 0.04: secant ln -2351.490750 sign +1, scan ln -2351.490751 sign +1, |d ln| 6.546e-07
end lambda 0.06: secant ln -2352.940456 sign -1, scan ln -2352.940455 sign -1, |d ln| 9.987e-07
evals: 0.04000000 +1 ln -2351.490750 dln 7.19e-07 robust True 236 s; 0.06000000 -1 ln -2352.940456 dln 1.90e-06 robust True 233 s; 0.05619906 -1 ln -2353.138563 dln 2.70e-06 robust True 233 s; 0.04809953 +1 ln -2353.759327 dln 6.49e-06 robust True 236 s; 0.05093119 -1 ln -2354.612447 dln 1.41e-05 robust True 236 s; 0.05008515 -1 ln -2356.584861 dln 1.04e-04 robust True 235 s; 0.04995608 +1 ln -2360.851844 dln 7.48e-03 robust True 227 s; 0.04996108 -1 ln -2360.255385 dln 4.09e-03 robust True 198 s
dln largest 7.475e-03, mean seconds per evaluation 229
secant memory: 61 samples, lowest available 12.5 GiB, peak RSS 2.89 GiB
```


**Secant refinement at k_c 95 at D 23.0625 (win2's accepted leg state, raw `I1025-win2/kc95_leg`, blob 696bd814; exit 4, nonrobust, a robust bracket by t5's ruling):**
```
scan: 10 evaluations, 10 noise-robust; robust changes 1: (-0.060, -0.040) + to - det-linear -0.054541 range [-0.059502, -0.054541]
signs by lambda: -0.10+ -0.08+ -0.06+ -0.04- -0.04- -0.02- 0.00- 0.02- 0.04- 0.06-
float64 sign equals the hybrid sign at 9 of 10
repeat of -0.04 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.10:-2620.012 -0.08:-2622.300 -0.06:-2626.676 -0.04:-2625.696 -0.02:-2626.598 0.00:-2627.813 0.02:-2629.154 0.04:-2630.562 0.06:-2632.014
secant: status nonrobust (not robust at -0.05863020692677942), tol 1e-05, evaluations 6 (the two ends included), run wall 1753 s
secant root bracket [-0.06000000, -0.05857558], width 1.424e-03, signs [1.0, -1.0], robust [True, True]; det-linear root -0.05862410; Brent's last point -0.05857558
scan reading: bracket (-0.060, -0.040), det-linear -0.054541, estimator range [-0.059502, -0.054541]
secant root inside the scan's estimator range: True; whole final bracket inside: False; root below the scan's det-linear: True
end lambda -0.06: secant ln -2626.675563 sign +1, scan ln -2626.675636 sign +1, |d ln| 7.292e-05
end lambda -0.04: secant ln -2625.695821 sign -1, scan ln -2625.695819 sign -1, |d ln| 1.994e-06
evals: -0.06000000 +1 ln -2626.675563 dln 4.33e-05 robust True 267 s; -0.04000000 -1 ln -2625.695821 dln 2.97e-06 robust True 296 s; -0.05454114 -1 ln -2626.027057 dln 1.42e-05 robust True 295 s; -0.05812583 -1 ln -2627.828398 dln 1.17e-04 robust True 299 s; -0.05857558 -1 ln -2630.020317 dln 1.09e-03 robust True 298 s; -0.05863021 +1 ln -2635.016896 dln 1.50e-01 robust False 297 s
dln largest 1.499e-01, mean seconds per evaluation 292
secant memory: 59 samples, lowest available 12.8 GiB, peak RSS 2.40 GiB
```


### Registrations and scoring
Every scan's and every refinement's registration (grid or bracket, reading, weights) was written in a README before its run (`kc87_leg_lambda/README.md`, `kc103_d23/README.md`, `kc103_leg/README.md`, `kc_d23_secant/README.md`, each pushed first) and its log entry scores it. What missed, from those entries: the regrid wall of k_c 103 at D 23.0 (1391 s against 4000 to 6500 s); the secant of k_c 103 at D 23.0 (per evaluation 5.3 to 9.1 min against 8 to 25, wall 51 min against 60 to 150, and the float64 sign differing from the hybrid at 3 of 7 evaluations where I registered agreement at 80%); the leg's first point (1822 s against 2000 to 6000 s); k_c 95 at D 23.0 and at D 23.0625 (exit 4, a non-robust interior point, where I registered exit 0 at 80% and 60%; their per-evaluation and wall times); k_c 87 at D 22.9375 (per evaluation 3.3 to 3.9 min against 4.5 to 7); the orientation registrations of the k_c 87 scans listed above.

Chain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672); nothing of mine is running for this issue now. Open: the k_c 87 values at D 22.9375 and 23.0 are of reduced quality (psi-constraint 1.02e-2 and 1.05e-2), and win2's k_c 95 states descend from them; the k_c 103 states are below 1e-2 (4.6e-3 to 5.2e-3).

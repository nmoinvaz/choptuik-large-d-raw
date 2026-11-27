**#1025 macm3, k_c 135 at D 23.125: lambda_1 = -0.03629764, bracket [-0.03629955, -0.03629455], width 5.000e-06, both ends robust; the zero of k_c 135 at D 23.07535, +0.00785 beyond the k_c 127 zero (27 Nov 01:36 UTC).** t5's order (hc 26 Nov 20:09 UTC, the seed rule): D 23.125 at k_c 135 as at D 23.0625, a regrid from my accepted k_c 127 leg state there (state blob e1dccb3c, record 58d3b080), `ell_refine.py l1kc127Lmacm3 127 l1kc135macm3d23125 135 1 23.125 2.0987860107 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, the kc135 check, the new scanner at lambda -0.045 to -0.025 plus a repeat of -0.035 (2 processes) and the secant (tol 1e-5, `d18_secant.py run --maxev=10`, one process, `venv-macm3-1058b`). t5's rulings: the scan's one robust change accepted as the bracket (hc 26 Nov 22:56 UTC), the point accepted (hc 27 Nov 01:32 UTC). Roots are the det-linear root inside the final bracket, read by position. **Every tail sum below is arithmetic only, not a result.**

### The regrid (raw `I1025-macm3/kc135_d23125/`, README with the two registration entries first)


| k_c 135 at | wall (s) | peak RSS (GiB, 60 s samples) | steps | steps ratio | constraint ratio | Delta shift |
|---|---|---|---|---|---|---|
| D 23.0625 | 4124 | 7.423 | 4442 | 1.063 | 0.678 | -3.7646e-06 |
| D 23.125 | 3574 | 6.609 | 4445 | 1.063 | 0.678 | -2.5188e-06 |


The D 23.125 regrid ran 21:07:46 to 22:07:20 UTC on 26 Nov (exit 0, `capped_run` wall 3574 s, 6 threads, nice 10). Acceptance (22:07:25 UTC): the kc135 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the kc127 check refuses the result. Record (blob f22d1e21; state ac01e477): |F| 2.9625e-10 (source 2.9775e-10), steps 4445 (source 4182), psi-constraint 1.1211e-03 (source 1.6537e-03), Delta 1.178024074501 (source 1.178026593320). No traceback; lowest available memory 11.2 GiB. The lane's hc line printed `regrid wall 3585 s`; that is the time to the hc line (it includes the checks and the push), the wall is 3574 s.

### The scan (new scanner `d18_secant.py scan`, eb1396ad of wip/ell1-speed 92b9bf53) and the secant


Scan 22:07:36 to 22:56:31 UTC (48.9 min, 2 processes, 970 to 975 s per evaluation, peak RSS 5.95 GiB per process); secant 22:56:39 to 01:32:37 UTC (26 to 27 Nov), **exit 0** (tol):

```
scan: 6 evaluations, 6 noise-robust; robust changes 1: (-0.040, -0.035) + to - det-linear -0.035791 range [-0.036874, -0.035791]
signs by lambda: -0.045+ -0.040+ -0.035- -0.035- -0.030- -0.025-
float64 sign equals the hybrid sign at 2 of 6
repeat of -0.035 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.045:-4184.732 -0.040:-4186.210 -0.035:-4187.882 -0.030:-4186.926 -0.025:-4186.965
secant: status tol (-), tol 1e-05, evaluations 6 (the two ends included), run wall 9346 s
secant root bracket [-0.03629955, -0.03629455], width 5.000e-06, signs [1.0, -1.0], robust [True, True]; det-linear root -0.03629764; Brent's last point -0.03629955
scan reading: bracket (-0.040, -0.035), det-linear -0.035791, estimator range [-0.036874, -0.035791]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda -0.040: secant ln -4186.210268 sign +1, scan ln -4186.210268 sign +1, |d ln| 0.000e+00
end lambda -0.035: secant ln -4187.882158 sign -1, scan ln -4187.882158 sign -1, |d ln| 0.000e+00
evals: -0.04000000 +1 ln -4186.210268 dln 9.77e-06 robust True 1468 s; -0.03500000 -1 ln -4187.882158 dln 2.35e-05 robust True 1657 s; -0.03579086 -1 ln -4188.723784 dln 6.20e-05 robust True 1592 s; -0.03634506 +1 ln -4191.023663 dln 6.76e-04 robust True 1588 s; -0.03629455 -1 ln -4193.760511 dln 1.04e-02 robust True 1542 s; -0.03629955 +1 ln -4194.239367 dln 1.66e-02 robust True 1499 s
dln largest 1.659e-02, mean seconds per evaluation 1558
secant memory: 311 samples, lowest available 9.9 GiB, peak RSS 5.36 GiB
```


**Noise of the sign near the root (k_c 135 at D 23.125):** k_c 135 D 23.125   tol   5.000e-06   1.7e-02 (at 1.91e-06 from the root)   3.2e-08 to 3.2e-08   3.2e-07 (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The secant ended on tol with all six evaluations robust, as the k_c 127 secant at D 23.125 did; the D 23.0625 secant of k_c 135 stopped on a non-robust point (exit 4).

### lambda_1 at k_c 127 and 135, D 23.0625 and 23.125, and the zero of k_c 135


| k_c | D 23.0625 (secant root [final bracket]) | D 23.125 (secant root [final bracket]) | slope per unit D | zero in D |
|---|---|---|---|---|
| 127 | **+0.00364182** [0.00323094, 0.00364870] | **-0.04190846** [-0.04191237, -0.04190737] | -0.72880 | **23.06750** |
| 135 | **+0.00939087** [0.00937845, 0.00965440] | **-0.03629764** [-0.03629955, -0.03629455] | -0.73102 | **23.07535** |


The shift of the root from k_c 127 to k_c 135 is **+0.005749** at D 23.0625 and **+0.005611** at D 23.125 (a growth factor 0.976; the shifts between k_c 95 and 119 grew by 1.63 to 1.77 from D 23.0 to 23.0625, and this one fell). The slope of the root in D over D 23.0625 to 23.125 is -0.73102 at k_c 135 and -0.72880 at k_c 127: its size rose by 0.00221. The zero by the line through the two roots, over the four bracket-end combinations (23.07533 to 23.07563), is **D 23.07535**; the k_c 127 zero by the same pair of D is 23.06750. The arithmetic is `kc135_d23125/zero_arithmetic_135.txt` (script `zero135.py`; its `--mutate=sign` control exits 1).

### The threshold table at seven k_c


| k_c | D pair used | lambda_1 at the two D (secant root [final bracket]) | slope per unit D | zero in D | zero over the bracket ends |
|---|---|---|---|---|---|
| 87 | **22.9375 and 23.0** | D 22.9375: **+0.04995785** [0.04995608, 0.04996108]; D 23.0: **-0.02540417** [-0.02540491, -0.02539991] | -1.20579 | **22.97893** | 22.97893 to 22.97893 |
| 95 | **23.0 and 23.0625** | D 23.0: **+0.00870734** [0.00796052, 0.00873919]; D 23.0625: **-0.05862410** [-0.06000000, -0.05857558] | -1.07730 | **23.00808** | 23.00732 to 23.00811 |
| 103 | **23.0 and 23.0625** | D 23.0: **+0.02650535** [0.02650441, 0.02650941]; D 23.0625: **-0.02851243** [-0.02851654, -0.02851154] | -0.88028 | **23.03011** | 23.03011 to 23.03011 |
| 111 | **23.0 and 23.0625** | D 23.0: **+0.03556371** [0.03538070, 0.03558301]; D 23.0625: **-0.01247909** [-0.01248264, -0.01247764] | -0.76868 | **23.04627** | 23.04620 to 23.04627 |
| 119 | **23.0 and 23.0625** | D 23.0: **+0.04106103** [0.04105978, 0.04106478]; D 23.0625: **-0.00351666** [-0.00351815, -0.00351315] | -0.71324 | **23.05757** | 23.05757 to 23.05757 |
| 127 | **23.0625 and 23.125** | D 23.0625: **+0.00364182** [0.00323094, 0.00364870]; D 23.125: **-0.04190846** [-0.04191237, -0.04190737] | -0.72880 | **23.06750** | 23.06697 to 23.06751 |
| 135 | **23.0625 and 23.125** | D 23.0625: **+0.00939087** [0.00937845, 0.00965440]; D 23.125: **-0.03629764** [-0.03629955, -0.03629455] | -0.73102 | **23.07535** | 23.07533 to 23.07563 |


**Steps of the zero in k_c:** +0.02915, +0.02203, +0.01616, +0.01130, +0.00993, +0.00785 (87 to 95, 95 to 103, 103 to 111, 111 to 119, 119 to 127, 127 to 135); ratios 0.7556, 0.7334, 0.6997, 0.8782, 0.7907. **Arithmetic only, not a result:** a geometric tail of the last ratio (0.7907) would put the limit of the zero at D 23.1050 (the previous ratio, 0.8782, at D 23.1320). The zeros of k_c 127 and 135 are lines through roots 0.0625 apart in D at the **same pair** (D 23.0625 and 23.125), so their step +0.00785 is like for like; the zeros of k_c 87 to 119 are lines through the pairs D 22.9375 and 23.0 (k_c 87) or D 23.0 and 23.0625, and the k_c 119 quadratic through its three D gives 23.05777, so the step 119 to 127 mixes pairs (with the quadratic the last two steps are +0.00973 and +0.00785, arithmetic only). **The zeros of k_c 127 and k_c 135 are not yet bracketed by a third D:** winb's D 23.0 secant of k_c 127 (`I1025-win/kc127_d23`, scan det-linear 0.048098, secant started 19:50:17 UTC) and win2's D 23.0 secant of k_c 135 (`I1025-win2/kc135_d23`, scan det-linear 0.049763, the latest commit: the first interior point 0.049763 is -, bracket (0.045, 0.049763)) were not finished in the raw repository at my fetch (5c918fa94); with their roots the three-point (quadratic) zeros follow.


D-slopes of lambda_1 (per unit D, over each k_c's pair): 87 -1.2058, 95 -1.0773, 103 -0.8803, 111 -0.7687, 119 -0.7132, 127 -0.7288, 135 -0.7310.

### Registrations and scoring
The registration was written in `kc135_d23125/README.md` before the regrid (first entry 20:13 UTC, second entry 21:07 UTC, from the D 23.0625 secant's final root) and its status entries score it item by item (regrid, scan and secant; `zero_arithmetic_135.txt`). **Met:** the regrid accepted; no exception or array limit; Delta shift in (-7.0e-6, -1.0e-6) (-2.5188e-06); steps ratio in (1.055, 1.072) (1.0630), steps within 25 of 4445 (4445); constraint in (1.0e-3, 1.25e-3) (1.1211e-03) and below 1e-2; |F| below 5e-10; peak RSS below 9 GiB (6.609 GiB); no memory alert; exactly one robust change in (-0.045, -0.025) (90%), its bracket (-0.040, -0.035) (33%); all 6 evaluations noise-robust; the repeat of -0.035 bit-identical; per evaluation 970 to 975 s in (700, 1050); scan wall 38 to 52 min (48.9); scan peak RSS per process below 6 GiB (5.953 GiB); **the zero of k_c 135 in (23.0745, 23.0770) (65%; read 23.07535)**. **Misses:** regrid wall 3800 to 4700 s (65%; 3574 s); regrid peak RSS in (7.0, 8.0) GiB (70%; 6.609 GiB); the float64 sign equal to the hybrid sign at all 6 (15%; at 2 of 6); scan peak RSS per process in (5.0, 5.3) GiB (65%; 5.953 GiB); the bracket (-0.035, -0.030) (50%; the read bracket is the 33% one); **the root in (-0.03623, -0.03248) (60%; read -0.03629764, below the lower end by 6.35e-05, t5 confirmed)**; the slope magnitude below k_c 127's 0.7288 (75%; 0.73102). **t5's root** (the rule alone, -0.036159; he quotes -0.0362): read minus it -0.000138 (minus -0.0362: -0.000098). **Recorded, not registered:** the secant's evaluations took 1468 to 1657 s (mean 1558 s) against 714 to 717 s at D 23.0625, and its wall 9346 s against 3573 s, while the k_c 87 chain (HOLD_low2 released 22:57:09 UTC on t5's order, 4-process scans at nice 20) ran beside it: its scans of D 21.4375, 21.84375, 21.90625, 21.96875, 22.03125 and 22.0625 finished at 23:20, 23:43, 00:05, 00:28, 00:50 and 01:13 UTC; the chain is the one difference I know of and the slowdown is not isolated (no control run). The secant's peak RSS was 5.36 GiB and the lowest available memory 9.9 GiB; no memory alert.

### Next
No further step is registered in `kc135_d23125/README.md`. The quadratic zeros wait for winb's D 23.0 root of k_c 127 and win2's D 23.0 root of k_c 135. The k_c 87 chain (pid 99672) runs on its own (HOLD_low2 released); nothing else of mine runs for this issue. Next: t5's order.


Raw: `I1025-macm3/kc135_d23125/` and `I1025-macm3/kc87_leg_lambda/23.125_kc135/` at 5c918fa94.

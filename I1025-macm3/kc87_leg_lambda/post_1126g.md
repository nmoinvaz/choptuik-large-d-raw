**#1025 macm3, k_c 135 at D 23.0625: lambda_1 = +0.00939087, robust bracket [0.00937845, 0.00965440], width 2.759e-04; both registered predictions met; the secant stopped on a non-robust interior point, so the bracket stands (2026-11-26 21:09 UTC).** t5's order (hc 26 Nov 18:08 UTC): k_c 135 at D 23.0625 from my accepted k_c 127 state there (state blob 7aae10c6, record 85a685f1), `ell_refine.py l1kc127macm3d230625 127 l1kc135macm3d230625 135 1 23.0625 2.0990016035 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`; the kc135 check (`kc135_syscheck_1025.py` b353d466; exit 0, controls 1 1, the kc127 check refuses); the new scanner at lambda 0.000, 0.005, 0.010, 0.015 plus a repeat of 0.010 (2 processes); the secant, tol 1e-5. t5's ruling (hc 21:06 UTC): the robust bracket stands (exit 4). Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position. **Every tail sum below is arithmetic only, not a result.**

### The regrid (raw `I1025-macm3/kc135_d230625/`, README with the registration first)


| lane | wall (s) | peak RSS (GiB, 60 s samples) | steps | steps ratio | constraint ratio | Delta shift |
|---|---|---|---|---|---|---|
| k_c 111 | 2102 | 4.781 | 3656 | 1.078 | 0.694 | -6.4617e-06 |
| k_c 119 | 2663 | 5.619 | 3916 | 1.071 | 0.623 | -1.3753e-06 |
| k_c 127 | 2853 | 7.513 | 4180 | 1.067 | 0.686 | -1.8781e-06 |
| k_c 135 | 4124 | 7.423 | 4442 | 1.063 | 0.678 | -3.7646e-06 |


The k_c 135 regrid ran 18:13:22 to 19:22:06 UTC (exit 0, `capped_run` wall 4124 s, 6 threads, nice 10). Acceptance (19:22:12 UTC): the kc135 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the kc127 check refuses the result. Record: |F| 3.0630e-10 (source 3.0829e-10), steps 4442 (source 4180), psi-constraint 1.0549e-03 (source 1.5567e-03), Delta 1.176167526704. No traceback; lowest available memory 11.3 GiB. The lane's hc line printed `regrid wall 4135 s`; that is the time to the hc line (it includes the checks and the push), the wall is 4124 s.

### The scan (new scanner `d18_secant.py scan`, eb1396ad of wip/ell1-speed 92b9bf53) and the secant


Scan 19:22:22 to 20:06:36 UTC (44.2 min, 2 processes, 711 to 970 s per evaluation, peak RSS 5.13 GiB per process); secant 20:06:50 to 21:06:33 UTC, **exit 4** (non-robust interior point):


```
scan: 5 evaluations, 5 noise-robust; robust changes 1: (0.005, 0.010) + to - det-linear 0.009654 range [0.008872, 0.009654]
signs by lambda: 0.000+ 0.005+ 0.010- 0.010- 0.015-
float64 sign equals the hybrid sign at 3 of 5
repeat of 0.010 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: 0.000:-4201.265 0.005:-4202.651 0.010:-4205.251 0.015:-4203.657
secant: status nonrobust (not robust at 0.009390867386883738), tol 1e-05, evaluations 5 (the two ends included), run wall 3573 s
secant root bracket [0.00937845, 0.00965440], width 2.759e-04, signs [1.0, -1.0], robust [True, True]; det-linear root 0.00939087; Brent's last point 0.00937845
scan reading: bracket (0.005, 0.010), det-linear 0.009654, estimator range [0.008872, 0.009654]
secant root inside the scan's estimator range: True; whole final bracket inside: False; root below the scan's det-linear: True
end lambda 0.005: secant ln -4202.650856 sign +1, scan ln -4202.650856 sign +1, |d ln| 0.000e+00
end lambda 0.010: secant ln -4205.251127 sign -1, scan ln -4205.251127 sign -1, |d ln| 0.000e+00
evals: 0.00500000 +1 ln -4202.650856 dln 1.08e-05 robust True 717 s; 0.01000000 -1 ln -4205.251127 dln 6.23e-05 robust True 714 s; 0.00965440 -1 ln -4206.044923 dln 1.46e-04 robust True 714 s; 0.00937845 +1 ln -4209.100286 dln 3.23e-03 robust True 714 s; 0.00939087 -1 ln -4212.586745 dln 1.11e-01 robust False 714 s
dln largest 1.113e-01, mean seconds per evaluation 715
secant memory: 119 samples, lowest available 12.3 GiB, peak RSS 5.62 GiB
```


**Noise of the sign near the root (k_c 135 at D 23.0625):** k_c 135 D 23.0625   nonrobust   2.759e-04   1.1e-01 (at 0.00e+00 from the root)   4.0e-08 to 4.0e-08   4.0e-07 (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The non-robust point is the det-linear root itself (dln 0.111 against the bar 0.1), so its distance from the root is 0 and the row's constant reads the bracket ends; the k_c 127 row at D 23.0625 was 1.1e-08 to 1.2e-08. The two ends of the robust bracket are robust (dln 3.2e-03 and 1.5e-04).

### lambda_1 at D 23.0625 by k_c, and the step of the root


| k_c | lambda_1 at D 23.0625 (secant root [final bracket]) | step from the previous k_c | ratio of the steps |
|---|---|---|---|
| 95 | **-0.05862410** [-0.06000000, -0.05857558] |  |  |
| 103 | **-0.02851243** [-0.02851654, -0.02851154] | +0.030112 |  |
| 111 | **-0.01247909** [-0.01248264, -0.01247764] | +0.016033 | 0.5325 |
| 119 | **-0.00351666** [-0.00351815, -0.00351315] | +0.008962 | 0.5590 |
| 127 | **+0.00364182** [0.00323094, 0.00364870] | +0.007158 | 0.7987 |
| 135 | **+0.00939087** [0.00937845, 0.00965440] | +0.005749 | 0.8031 |


The k_c 135 root exceeds the k_c 127 root by **+0.005749**; the ratios of the steps are 0.5325, 0.5590, 0.7987, 0.8031 (the last two, 0.7987 and 0.8031, are nearly equal; my register took ratios 0.5 to 0.9, which give +0.0072 to +0.0101, and the read ratio is inside). The k_c 135 zero in D by the k_c 127 slope (-0.72880 per unit D, the pair 23.0625 to 23.125) is 23.07539 (**arithmetic only, not a result**); the zero by two k_c 135 roots waits for the D 23.125 point, whose lane started 21:07:46 UTC.

### Registrations and scoring
The registration was written in `kc135_d230625/README.md` before the regrid (18:12 UTC) and its status entries score it item by item (regrid, scan and secant). **Predictions on the final bracket's det-linear root +0.00939087:** t5's +0.008 +- 0.004 **met** (difference +0.001391); mine +0.0087 +- 0.003 **met** (difference +0.000691). **Met:** the regrid accepted; no exception or array limit; steps within 15 of 4443 (4442); constraint in (0.8e-3, 1.4e-3) and below 1e-2; |F| below 5e-10; peak RSS below 12 GiB; no memory alert; exactly one robust change (90%), its bracket (0.005, 0.010) (60%); all 5 evaluations noise-robust; the repeat of 0.010 bit-identical; scan wall 35 to 55 min (44.2); scan peak RSS below 7 GiB; the secant's root inside the scan's estimator range; per evaluation 650 to 800 s (714 to 717 s); peak RSS below 7 GiB (5.62 GiB). **Misses:** the regrid's Delta shift in (-3.0e-6, -1.0e-6) (60%; -3.7646e-6); regrid wall 2900 to 3800 s (70%; 4124 s); regrid peak RSS in (8.5, 11) GiB and above k_c 127's 7.51 GiB (70% and 90%; 7.423 GiB); the float64 sign equal to the hybrid sign at all 5 (50%; 3 of 5, it is -1 everywhere and the hybrid sign is needed at 0.000 and 0.005); scan seconds per evaluation 700 to 950 (65%; 711 to 970); scan peak RSS per process in (5.3, 6.8) GiB (65%; 5.13 GiB); the secant exit 0 within 10 evaluations (55%; exit 4 after 5, the registered 40% outcome); the secant wall 75 to 120 min (60%; 59.5 min).

### Next
t5's seed rule (hc 20:09 UTC): D 23.125 at k_c 135 by a regrid from my accepted k_c 127 leg state there (blob e1dccb3c, record 58d3b080), with the scan and the secant, in `kc135_d23125/` (README with the registration first, raw ea00c37f2, second entry e820fafbb). Registered there before the regrid: the scan at lambda -0.045 to -0.025 by 0.005 plus a repeat of -0.035, and the root at D 23.125 as 0.00939087 minus 0.0625 times a slope magnitude of 0.70 +- 0.03, i.e. -0.034359 +- 0.001875 (t5's rule alone: -0.036159); the zero of k_c 135 by the line through its two roots then, and with win2's D 23.0 later by the quadratic. The regrid started 21:07:46 UTC. HOLD_low2 stays held; I release it when that scan ends and only its secant runs (t5's order of 20:35 UTC).


Raw: `I1025-macm3/kc135_d230625/` and `I1025-macm3/kc87_leg_lambda/23.0625_kc135/` at dd67541d7.

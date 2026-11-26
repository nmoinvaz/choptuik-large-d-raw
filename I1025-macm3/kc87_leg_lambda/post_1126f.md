**#1025 macm3, k_c 127 leg step to D 23.125: the guard did not fire; lambda_1(23.125) = -0.04190846, bracket 5e-6; the zero of k_c 127 at D 23.0675 (2026-11-26 18:08 UTC).** t5's order (hc 26 Nov): one leap step of k_c 127 from two seeds (winb's accepted D 23.0 state, blob 7a1b150c, record eea03461, and my D 23.0625 state, blobs 7aae10c6 and 85a685f1) to D 23.125 at h 0.0625 with `ell_leap.py` and `leap_guard.py` (stop at max cos_t_reg >= 0.5); the kc127 check on the new state; the new scanner at lambda -0.06 to -0.02 plus a repeat of -0.04 (2 processes); the secant on the robust bracket, tol 1e-5; "Post on #1025 when the secant ends." t5 registered lambda_1(23.125) = -0.040 +- 0.010 (zero near D 23.068); I registered -0.039 +- 0.006. **Both are met.** Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position. **Every tail sum below is arithmetic only, not a result.**

### The leap (raw `I1025-macm3/kc127_leg/`, README with the registration first)


`ell_leap.py l1kc127Lmacm3 1 127 <seed A> 23.0 <seed B> 23.0625 23.125 0.0625 --tol 1e-12 --fmax 1e-8 --cmax 2e-2 --fold`, 6 threads, `capped_run.py` 43200 s. Both seeds were first accepted on this machine (the k_c 127 check exit 0, controls `--mutate=F` and `--mutate=steps` exit 1 1, the k_c 119 and k_c 111 checks refuse them). Leap 15:30:44 to 16:17:15 UTC, exit 0, wall 2753 s, no halving, no memory alert, leap peak RSS 6.22 GiB, lowest available memory 12.1 GiB. **The guard did not fire** (no `leg_STOP.txt`).


| D | Delta | dDelta/dD | \|F\| | steps | psi-constraint | n_null | point seconds | max cos_t_reg |
|---|---|---|---|---|---|---|---|---|
| 23.125 | 1.178026593320 | +0.029685 | 2.977e-10 | 4182 | 1.654e-03 | 122 | 2373 | 0.2860 |


The table's dDelta/dD is the difference quotient from the D 23.0625 record (Delta 1.176171291295); the guard's own slope (`leg_points.txt`) is 0.029685. Weak regular values 1.4646e-10, 1.4651e-10, 5.6594e-10, 3.5366e-09 with tangent cosines 0.0205, 0.0229, 0.2130, 0.2860 (delta_reg 0.0014, 0.0009, 0.3208, 0.6915). The largest cosine, 0.2860, is on the **fourth** regular mode and below the bar 0.5; the k_c 87, 95 and 103 legs fired at 0.5096, 0.5997 and 0.5776 on the third, as lambda_1 neared its zero. This leg crosses the k_c 127 zero (D 23.0675) and does not fire, with the third cosine at 0.2130.


Acceptance (16:17:42 UTC): `kc127_syscheck_1025.py` exit 0 (state |F| 2.9774808995e-10 equal to the record's, `freeze_from` 4182 steps equal to the record's), controls exit 1 1, the k_c 119 and k_c 111 checks refuse the state. Raw 9a6827edf: state blob e1dccb3c, record blob 58d3b080.


### The scan and the secant at D 23.125 (new scanner `d18_secant.py scan`, eb1396ad of wip/ell1-speed 92b9bf53)


Scan 16:17:47 to 16:56:11 UTC (38.4 min, 2 processes, 754 to 777 s per evaluation, peak RSS 4.97 GiB per process); secant 16:56:18 to 18:04:12 UTC, exit 0:


```
scan: 6 evaluations, 6 noise-robust; robust changes 1: (-0.050, -0.040) + to - det-linear -0.040691 range [-0.046207, -0.040691]
signs by lambda: -0.06+ -0.05+ -0.04- -0.04- -0.03- -0.02-
float64 sign equals the hybrid sign at 6 of 6
repeat of -0.04 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.06:-3865.699 -0.05:-3867.660 -0.04:-3870.262 -0.03:-3869.587 -0.02:-3870.134
secant: status tol (-), tol 1e-05, evaluations 7 (the two ends included), run wall 4066 s
secant root bracket [-0.04191237, -0.04190737], width 5.000e-06, signs [1.0, -1.0], robust [True, True]; det-linear root -0.04190846; Brent's last point -0.04190737
scan reading: bracket (-0.050, -0.040), det-linear -0.040691, estimator range [-0.046207, -0.040691]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda -0.05: secant ln -3867.660448 sign +1, scan ln -3867.660448 sign +1, |d ln| 0.000e+00
end lambda -0.04: secant ln -3870.261537 sign -1, scan ln -3870.261537 sign -1, |d ln| 0.000e+00
evals: -0.05000000 +1 ln -3867.660448 dln 1.60e-06 robust True 582 s; -0.04000000 -1 ln -3870.261537 dln 1.05e-05 robust True 581 s; -0.04069068 -1 ln -3870.630944 dln 1.60e-05 robust True 581 s; -0.04216088 +1 ln -3872.034573 dln 7.18e-05 robust True 580 s; -0.04187089 -1 ln -3873.973382 dln 4.89e-04 robust True 581 s; -0.04190737 -1 ln -3877.506649 dln 1.67e-02 robust True 580 s; -0.04191237 +1 ln -3876.227053 dln 4.69e-03 robust True 581 s
dln largest 1.666e-02, mean seconds per evaluation 581
secant memory: 135 samples, lowest available 12.9 GiB, peak RSS 4.22 GiB
```


**Noise of the sign near the root (k_c 127 at D 23.125):** k_c 127 D 23.125   tol   5.000e-06   1.7e-02 (at 1.09e-06 from the root)   1.8e-08 to 1.8e-08   1.8e-07 (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). This is the first of my k_c 127 secants that ended on tol (D 23.0625 stopped on a non-robust point): its seven evaluations are all robust and the bracket ends lie 1.1e-6 and 3.9e-6 from the root.


### The zero of k_c 127 and the threshold table at six k_c


| k_c | D pair used | lambda_1 at the two D (secant root [final bracket]) | slope per unit D | zero in D | zero over the bracket ends |
|---|---|---|---|---|---|
| 87 | **22.9375 and 23.0** | D 22.9375: **+0.04995785** [0.04995608, 0.04996108]; D 23.0: **-0.02540417** [-0.02540491, -0.02539991] | -1.20579 | **22.97893** | 22.97893 to 22.97893 |
| 95 | **23.0 and 23.0625** | D 23.0: **+0.00870734** [0.00796052, 0.00873919]; D 23.0625: **-0.05862410** [-0.06000000, -0.05857558] | -1.07730 | **23.00808** | 23.00732 to 23.00811 |
| 103 | **23.0 and 23.0625** | D 23.0: **+0.02650535** [0.02650441, 0.02650941]; D 23.0625: **-0.02851243** [-0.02851654, -0.02851154] | -0.88028 | **23.03011** | 23.03011 to 23.03011 |
| 111 | **23.0 and 23.0625** | D 23.0: **+0.03556371** [0.03538070, 0.03558301]; D 23.0625: **-0.01247909** [-0.01248264, -0.01247764] | -0.76868 | **23.04627** | 23.04620 to 23.04627 |
| 119 | **23.0 and 23.0625** | D 23.0: **+0.04106103** [0.04105978, 0.04106478]; D 23.0625: **-0.00351666** [-0.00351815, -0.00351315] | -0.71324 | **23.05757** | 23.05757 to 23.05757 |
| 127 | **23.0625 and 23.125** | D 23.0625: **+0.00364182** [0.00323094, 0.00364870]; D 23.125: **-0.04190846** [-0.04191237, -0.04190737] | -0.72880 | **23.06750** | 23.06697 to 23.06751 |


**Steps of the zero in k_c:** +0.02915, +0.02203, +0.01616, +0.01130, +0.00993 (87 to 95, 95 to 103, 103 to 111, 111 to 119, 119 to 127); ratios 0.7556, 0.7334, 0.6997, 0.8782. **Arithmetic only, not a result:** a geometric tail of the last ratio would put the limit of the zero at D 23.1391 (the previous ratio would put it at D 23.0906). The zero of k_c 127 is the line through two roots 0.0625 apart in D, with the zero 0.005 from the nearer one; the k_c 119 zero is the line through D 23.0 and 23.0625 (the quadratic through its three D gives 23.05777, +0.00020), so the last ratio moves to 0.8455 if the quadratic is used for k_c 119 (arithmetic only). **The k_c 127 zero is not yet bracketed by a third D:** winb's D 23.0 scan and secant of k_c 127 were not in the raw repository at my fetch (18:08 UTC); with that root the three-point (quadratic) zero follows.


D-slopes of lambda_1 (per unit D, over each k_c's pair): 87 -1.2058, 95 -1.0773, 103 -0.8803, 111 -0.7687, 119 -0.7132, 127 -0.7288. The pairs are not at one D: k_c 119's own slope grows in size with D (-0.61531 over D 22.875 to 23.0, -0.71324 over 23.0 to 23.0625), so the k_c 127 value, over the higher pair D 23.0625 to 23.125, is not comparable with the earlier ones; winb's D 23.0 root of k_c 127 will give its slope over 23.0 to 23.0625. My register compared slopes at different D; that is the miss in the scoring below.


### Registrations and scoring
The registration was written in `kc127_leg/README.md` before the leap (15:29 UTC) and its status entries score it item by item; the zero arithmetic is `zero_arithmetic_127.txt` (script `zero127.py`; its `--mutate=sign` control exits 1). **Misses:** the guard fired (registered 65%; it did not: max cos_t_reg 0.2860); n_null exactly 119 (50%; 122, within 3 yes); max cos_t_reg in (0.3, 0.75) (80%; 0.2860, just below); the leap's point wall 2500 to 6000 s (65%; 2373 s, just below); the D-slope of lambda_1 (registered -0.65 to -0.72, read -0.7288). **Met:** the leap converged without halving; Delta in [1.17801, 1.17804]; constraint in (1.6e-3, 1.85e-3); steps within 10 of 4181; |F| below 5e-10; peak RSS below 10 GiB and no memory alert; exactly one robust change, in (-0.050, -0.040) (35%); all 6 evaluations robust; the repeat bit-identical; the float64 sign equal to the hybrid sign at 6 of 6 (45%); scan wall 35 to 60 min; the root within 0.006 of -0.039 (read -0.041908, difference -0.002908) and in t5's band; the secant exit 0 within 10 evaluations (55%; 7 evaluations); its root inside the scan's estimator range; per evaluation 9 to 14 min (581 s); wall 55 to 110 min (4066 s); peak RSS below 7 GiB (4.22 GiB); the zero in 23.066 to 23.070 (read 23.06750; t5's 23.068 differs by -0.00050).


Raw: `I1025-macm3/kc127_leg/` and `I1025-macm3/kc87_leg_lambda/23.125_kc127/` at raw 2b4f16d34 for kc127_leg (the scan folder was pushed with the point). Chain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672); nothing of mine runs for this issue now. Next: t5's order.

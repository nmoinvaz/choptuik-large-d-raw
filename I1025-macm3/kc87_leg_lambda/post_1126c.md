**#1025 macm3, k_c 119 at D 23.0625 and the threshold zero at five resolutions: zeros 22.97893, 23.00808, 23.03011, 23.04627, 23.0576 (2026-11-26 10:42 UTC).** t5's order (hc 26 Nov): k_c 119 at D 23.0625 from my k_c 111 state there "to give k_c 119's threshold zero today"; t5 registered the root at -0.004 +- 0.005 and the zero near D 23.057. Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position, brackets in square brackets; the zero of each k_c is the straight line through its two roots (arithmetic on two points, not a result). **Every tail sum below is arithmetic only, not a result.**

### The threshold table: lambda_1 at two D per k_c, the zero in D, and the D pair each k_c uses


| k_c | D pair used | lambda_1 at the two D (secant root [final bracket]) | slope per unit D | zero in D | zero over the bracket ends |
|---|---|---|---|---|---|
| 87 | **22.9375 and 23.0** | D 22.9375: **0.04995785** [0.04995608, 0.04996108]; D 23.0: **-0.02540417** [-0.02540491, -0.02539991] | -1.20579 | **22.97893** | 22.97893 to 22.97893 |
| 95 | **23.0 and 23.0625** | D 23.0: **0.00870734** [0.00796052, 0.00873919]; D 23.0625: **-0.05862410** [-0.06000000, -0.05857558] | -1.07730 | **23.00808** | 23.00732 to 23.00811 |
| 103 | **23.0 and 23.0625** | D 23.0: **0.02650535** [0.02650441, 0.02650941]; D 23.0625: **-0.02851243** [-0.02851654, -0.02851154] | -0.88028 | **23.03011** | 23.03011 to 23.03011 |
| 111 | **23.0 and 23.0625** | D 23.0: **0.03556371** [0.03538070, 0.03558301]; D 23.0625: **-0.01247909** [-0.01248264, -0.01247764] | -0.76868 | **23.04627** | 23.04620 to 23.04627 |
| 119 | **23.0 and 23.0625** | D 23.0: **0.04106103** [0.04105978, 0.04106478]; D 23.0625: **-0.00351666** [-0.00351815, -0.00351315] | -0.71324 | **23.05757** | 23.05757 to 23.05757 |


**Steps of the zero in k_c:** +0.02915, +0.02203, +0.01616, +0.01130 (87 to 95, 95 to 103, 103 to 111, 111 to 119); ratios 0.7556, 0.7334, 0.6997. **Arithmetic only, not a result:** a geometric tail of the last ratio would put the limit of the zero at D 23.0839. t5's register for k_c 119 (zero near D 23.057): read 23.05757.


**Roots at D 23.0:** -0.02540417, +0.00870734, +0.02650535, +0.03556371, +0.04106103; steps +0.034112, +0.017798, +0.009058, +0.005497; ratios 0.5218, 0.5090, 0.6069 (a geometric tail of the last ratio would end at 0.0495, arithmetic only). **Roots at D 23.0625:** -0.05862410, -0.02851243, -0.01247909, -0.00351666 for k_c 95, 103, 111, 119; steps +0.030112, +0.016033, +0.008962; ratios 0.5325, 0.5590 (tail 0.0078, arithmetic only). k_c 87 has no state at D 23.0625 (my part c2 ended at D 23.0 by the guard); its pair is D 22.9375 and 23.0.


### k_c 119 at D 23.0625: regrid, scan with the new scanner, secant (raw `I1025-macm3/kc119_d230625/`, README with the registration first, raw efdd1c937)


Source: my accepted k_c 111 state at D 23.0625 (blob 871f58c2, record 29448608). The k_c 111 check accepted it (controls 1 1; the k_c 103 and k_c 119 checks refused it); `kc119_syscheck_1025.py` (fc6e0dd6) accepted the result (controls 1 1; the k_c 111 check refused it). `ell_refine.py` 631e5801, 6 threads, `capped_run.py` 28800 s. k_c 119 record: D 23.0625 |F| 3.1113e-10 steps 3916 psi-constraint 2.2703e-03 Delta 1.176173169384 (k_c 111 source: |F| 3.1386e-10 steps 3656 constraint 3.6419e-03 Delta 1.176174544639); Delta shift -1.3753e-06, steps ratio 1.071, constraint ratio 0.623. Wall 2663 s; peak RSS 5.62 GiB. **The scan used the new scanner** (t5's change, hc 26 Nov): `d18_secant.py scan` of wip/ell1-speed 92b9bf53, blob eb1396ad, whose selftest exits 0 and `--mutate=half`, `norobust`, `nosigncheck` exit 1 (logged in the README before the scan); my driver `kc87_leg_lambda/pointnew.sh` was tested first on the k_c 119 D 23.0 state against the old record at 0.04 (|d ln| 2.57e-5, sign equal, the repeat bit-identical, `_test_pointnew/`). Plan: lambda -0.04, -0.02, 0.00, 0.02 plus a repeat of -0.02, at most 2 processes; then `d18_secant.py run`:

```
scan: 5 evaluations, 5 noise-robust; robust changes 1: (-0.020, 0.000) + to - det-linear -0.000483 range [-0.017664, -0.000483]
signs by lambda: -0.04+ -0.02+ -0.02+ 0.00- 0.02-
float64 sign equals the hybrid sign at 5 of 5
repeat of -0.02 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.04:-3559.501 -0.02:-3562.450 -0.02:-3562.450 0.00:-3566.150 0.02:-3566.404
secant: status tol (-), tol 1e-05, evaluations 8 (the two ends included), run wall 3862 s
secant root bracket [-0.00351815, -0.00351315], width 5.000e-06, signs [1.0, -1.0], robust [True, True]; det-linear root -0.00351666; Brent's last point -0.00351815
scan reading: bracket (-0.020, 0.000), det-linear -0.000483, estimator range [-0.017664, -0.000483]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda -0.02: secant ln -3562.450100 sign +1, scan ln -3562.450100 sign +1, |d ln| 0.000e+00
end lambda 0.00: secant ln -3566.149663 sign -1, scan ln -3566.149663 sign -1, |d ln| 0.000e+00
evals: -0.02000000 +1 ln -3562.450100 dln 2.74e-06 robust True 484 s; 0.00000000 -1 ln -3566.149663 dln 9.08e-06 robust True 480 s; -0.00048275 -1 ln -3566.245307 dln 1.06e-05 robust True 482 s; -0.00518681 +1 ln -3566.335453 dln 2.12e-05 robust True 484 s; -0.00294072 -1 ln -3567.642066 dln 5.88e-05 robust True 483 s; -0.00341926 -1 ln -3569.367813 dln 3.51e-04 robust True 484 s; -0.00351815 +1 ln -3573.541864 dln 2.28e-02 robust True 482 s; -0.00351315 -1 ln -3572.677627 dln 9.78e-03 robust True 483 s
dln largest 2.285e-02, mean seconds per evaluation 483
secant memory: 129 samples, lowest available 12.9 GiB, peak RSS 5.04 GiB
```


**Noise of the sign near the root (k_c 119 at D 23.0625):** k_c 119 D 23.0625   tol   5.000e-06   2.3e-02 (at 1.48e-06 from the root)   3.4e-08 to 3.4e-08   3.4e-07 (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1).


### Registrations and scoring
The registration was written in `kc119_d230625/README.md` before the regrid and its log entries score it (regrid, scan and secant). Nothing registered for this lane missed (the regrid, the scan and the secant are all scored there); the root was registered at -0.0027 (t5 -0.004 +- 0.005) and read at -0.00352, the zero registered near D 23.0586 (t5 23.057) and read at 23.05757.

Chain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672); nothing of mine is running for this issue now. dh370's Linux run of the same point is the cross-check. Next (t5's order): the third D for k_c 119, D 22.875, regridded from dh610's accepted k_c 111 state there (raw `I1025-dh610/kc111_d22875`, blobs a8fe443e and 5233ffe8), the new scanner at lambda 0.10 to 0.13, then the secant; t5 registers 0.122 +- 0.006.

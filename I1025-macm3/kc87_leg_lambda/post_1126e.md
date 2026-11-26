**#1025 macm3, k_c 127 at D 23.0625 (the sixth resolution): lambda_1 = +0.00364182, robust bracket [0.00323094, 0.00364870]; regrid, scan with the new scanner, secant (2026-11-26 15:24 UTC).** t5's order (hc 26 Nov): "Post it on #1025." t5's ruling: exit 4 with a non-robust interior point stands as the robust bracket; both registrations are met (t5 +0.003 +- 0.004, mine +0.002 +- 0.003). Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position. **Every tail sum below is arithmetic only, not a result.**

### lambda_1 at D 23.0625 by k_c (secant roots)


| k_c | state | root at D 23.0625 [final bracket] | tool exit | step from the previous k_c | ratio of successive steps |
|---|---|---|---|---|---|
| 95 | win2's leg state (reduced-quality lineage) | **-0.05862410** [-0.06000000, -0.05857558] | 4 (nonrobust; width 1.4e-03) |  |  |
| 103 | my leg point (the guard stopped the leg there) | **-0.02851243** [-0.02851654, -0.02851154] | 0 (tol 1e-5) | +0.030112 |  |
| 111 | my regrid of my k_c 103 state | **-0.01247909** [-0.01248264, -0.01247764] | 0 (tol 1e-5) | +0.016033 | 0.5325 |
| 119 | my regrid of my k_c 111 state | **-0.00351666** [-0.00351815, -0.00351315] | 0 (tol 1e-5) | +0.008962 | 0.5590 |
| 127 | my regrid of my k_c 119 state (psi-constraint 1.56e-3) | **+0.00364182** [0.00323094, 0.00364870] | 4 (nonrobust; width 4.2e-04) | +0.007158 | 0.7987 |


Steps +0.030112, +0.016033, +0.008962, +0.007158; ratios 0.5325, 0.5590, 0.7987. The ratio of the last step, 0.7987, is the largest of the three (t5 registered about 0.72, I registered 0.6). **Arithmetic only, not a result:** a geometric tail of that ratio would end at +0.0320. The root is positive at D 23.0625, so the zero of k_c 127 lies above D 23.0625: with D 23.0 it needs a second D for k_c 127 (winb's regrid at D 23.0 is pending); t5 expects the extrapolated zero near D 23.068.

### k_c 127 at D 23.0625: regrid, scan, secant (raw `I1025-macm3/kc127_d230625/`, README with the registration first, raw 22839e56d)


Source: my accepted k_c 119 state at D 23.0625 (blob 57f67269, record 659c62e5). The k_c 119 check accepted it (controls 1 1; the k_c 111 and k_c 127 checks refused it); `kc127_syscheck_1025.py` (raw `I1025-mac/checks` at d1baa986c, blob 898ebefa: the k_c 111 check with 111 changed to 127 and a header comment line) accepted the result (controls 1 1; the k_c 119 check refused it). `ell_refine.py` 631e5801, lambda_0(23.0625) = 2.0990016035, 6 threads, `capped_run.py` 28800 s. k_c 127 record: D 23.0625 |F| 3.0829e-10 steps 4180 psi-constraint 1.5567e-03 Delta 1.176171291295 (k_c 119 source: |F| 3.1113e-10 steps 3916 constraint 2.2703e-03 Delta 1.176173169384); Delta shift -1.8781e-06, steps ratio 1.067, constraint ratio 0.686. Wall 2853 s; **peak RSS 7.51 GiB (the k_c 119 regrids reached 5.5 to 5.6)**, no memory alert, no array limit at k_c 127. The scan used the new scanner (`d18_secant.py scan`, 92b9bf53, eb1396ad): lambda -0.02, -0.01, 0.00, 0.01 plus a repeat of 0.00 on 2 processes (peak RSS per scan process 5.04 GiB); then `d18_secant.py run`:

```
scan: 5 evaluations, 5 noise-robust; robust changes 1: (0.000, 0.010) + to - det-linear 0.006462 range [0.001861, 0.006462]
signs by lambda: -0.02+ -0.01+ 0.00+ 0.00+ 0.01-
float64 sign equals the hybrid sign at 4 of 5
repeat of 0.00 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.02:-3880.582 -0.01:-3882.292 0.00:-3884.772 0.00:-3884.772 0.01:-3885.375
secant: status nonrobust (not robust at 0.003641475054483363), tol 1e-05, evaluations 7 (the two ends included), run wall 4070 s
secant root bracket [0.00323094, 0.00364870], width 4.178e-04, signs [1.0, -1.0], robust [True, True]; det-linear root 0.00364182; Brent's last point 0.00364870
scan reading: bracket (0.000, 0.010), det-linear 0.006462, estimator range [0.001861, 0.006462]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda 0.00: secant ln -3884.772377 sign +1, scan ln -3884.772377 sign +1, |d ln| 0.000e+00
end lambda 0.01: secant ln -3885.374699 sign -1, scan ln -3885.374699 sign -1, |d ln| 0.000e+00
evals: 0.00000000 +1 ln -3884.772377 dln 2.26e-06 robust True 580 s; 0.01000000 -1 ln -3885.374699 dln 2.84e-06 robust True 580 s; 0.00646187 -1 ln -3885.777301 dln 5.16e-06 robust True 582 s; 0.00323094 +1 ln -3887.329781 dln 2.77e-05 robust True 582 s; 0.00379547 -1 ln -3888.375785 dln 7.73e-05 robust True 581 s; 0.00364870 -1 ln -3891.419686 dln 1.63e-03 robust True 582 s; 0.00364148 +1 ln -3897.552512 dln 1.39e+00 robust False 581 s
dln largest 1.392e+00, mean seconds per evaluation 581
secant memory: 135 samples, lowest available 12.7 GiB, peak RSS 5.11 GiB
```


**Noise of the sign near the root (k_c 127 at D 23.0625):** k_c 127 D 23.0625   nonrobust   4.178e-04   1.4e+00 (at 3.44e-07 from the root)   1.1e-08 to 1.2e-08   1.1e-07 (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The evaluation that stopped the tool lay 3.4e-7 from the det-linear root of its bracket with dln 1.39; the two robust evaluations nearest the root give dln x distance 1.1e-8 and 1.2e-8.


### Registrations and scoring
The registration was written in `kc127_d230625/README.md` before the regrid and its log entries score it. Misses: the regrid's Delta shift (registered -1.4e-6 to -0.4e-6, read -1.878e-6: the shifts did not keep falling); the float64 sign equal to the hybrid sign at all 5 scan points (it differed at 0.01); the secant exit (registered exit 0 at 55%, exit 4 at 40%: it stopped on the non-robust point, which stands as the robust bracket by t5's ruling); the regrid's peak RSS was above my 6.5 GiB (7.51 GiB, inside the registered 8 GiB). The root: +0.002 registered (t5 +0.003), +0.003642 read.

Chain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672). Next (t5's order): one leg step of k_c 127 from this state to D 23.125 with the guard (`leap_guard.py`, stop at max cos_t_reg >= 0.5), to bracket the zero; t5 registers lambda_1(23.125) = -0.040 +- 0.010.

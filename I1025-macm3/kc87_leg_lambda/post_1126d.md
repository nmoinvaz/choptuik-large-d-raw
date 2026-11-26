**#1025 macm3, k_c 119 at D 22.875: lambda_1 = +0.11797426, bracket 5e-6; k_c 119 at three D, the zero by a line and by a quadratic (2026-11-26 12:50 UTC).** t5's order (hc 26 Nov): "Post it on #1025." t5's register for the root: 0.122 +- 0.006; mine 0.120 +- 0.006; both are met. Roots are the det-linear root inside the final bracket of `d18_secant.py` (`--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position.

### k_c 119 at three D (secant roots)


| D | state | root [final bracket] | tool exit | scanner of the scan |
|---|---|---|---|---|
| 22.875 | my regrid of dh610's k_c 111 state (psi-constraint 1.91e-3) | **+0.11797426** [0.11797019, 0.11797519] | 0 (tol 1e-5) | `d18_secant.py scan` eb1396ad |
| 23.0 | my regrid of dh170's k_c 111 state (2.14e-3) | **+0.04106103** [0.04105978, 0.04106478] | 0 (tol 1e-5) | `d18_hybsign.py` e089207a |
| 23.0625 | my regrid of my k_c 111 state (2.27e-3) | **-0.00351666** [-0.00351815, -0.00351315] | 0 (tol 1e-5) | `d18_secant.py scan` eb1396ad |


**The zero of k_c 119 (arithmetic on three points, not a result; `kc119_d22875/zero_arithmetic.txt`):**
```
k_c 119 roots: D 22.875 0.11797426, D 23.0 0.04106103, D 23.0625 -0.00351666
slopes per unit D: -0.61531 (22.875 to 23.0), -0.71324 (23.0 to 23.0625)
zero by the line through D 23.0 and 23.0625: 23.05757
quadratic through the three roots: coefficients [-0.52233 -0.6806   0.04106]; zero near D 23.06: 23.05777 (difference from the line +0.00020)
```
The quadratic puts the zero 0.00020 above the line; the earlier zeros (k_c 87 to 111) are lines through two D (the post of comment 7189722079), so the line value 23.05757 is the one that compares with them.

### k_c 119 at D 22.875: regrid, scan, secant (raw `I1025-macm3/kc119_d22875/`, README with the registration first, raw 5dfbfe396)


Source: dh610's accepted k_c 111 state at D 22.875 (raw `I1025-dh610/kc111_d22875` at 33c6c6fb, blob a8fe443e, record 5233ffe8, tag l1kc111dh610d22875; dh610's regrid of winb's k_c 103 state). The k_c 111 check accepted it (controls 1 1; the k_c 103 and k_c 119 checks refused it); `kc119_syscheck_1025.py` (fc6e0dd6) accepted the result (controls 1 1; the k_c 111 check refused it). `ell_refine.py` 631e5801, lambda_0(22.875) = 2.0996545550, 6 threads, `capped_run.py` 28800 s. k_c 119 record: D 22.875 |F| 3.3918e-10 steps 3912 psi-constraint 1.9119e-03 Delta 1.170649372619 (k_c 111 source: |F| 3.4195e-10 steps 3651 constraint 3.1812e-03 Delta 1.170650517783); Delta shift -1.1452e-06, steps ratio 1.071, constraint ratio 0.601. Wall 2272 s; peak RSS 5.51 GiB. The scan used the new scanner (`d18_secant.py scan`, wip/ell1-speed 92b9bf53, eb1396ad; selftest and the three mutations logged in the README before the scan): lambda 0.10, 0.11, 0.12, 0.13 plus a repeat of 0.12 on 2 processes; then `d18_secant.py run`:

```
scan: 5 evaluations, 5 noise-robust; robust changes 1: (0.110, 0.120) + to - det-linear 0.119211 range [0.114090, 0.119211]
signs by lambda: 0.10+ 0.11+ 0.12- 0.12- 0.13-
float64 sign equals the hybrid sign at 3 of 5
repeat of 0.12 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: 0.10:-3605.431 0.11:-3607.331 0.12:-3609.788 0.12:-3609.788 0.13:-3609.095
secant: status tol (-), tol 1e-05, evaluations 7 (the two ends included), run wall 3403 s
secant root bracket [0.11797019, 0.11797519], width 5.000e-06, signs [1.0, -1.0], robust [True, True]; det-linear root 0.11797426; Brent's last point 0.11797519
scan reading: bracket (0.110, 0.120), det-linear 0.119211, estimator range [0.114090, 0.119211]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda 0.11: secant ln -3607.330679 sign +1, scan ln -3607.330679 sign +1, |d ln| 0.000e+00
end lambda 0.12: secant ln -3609.788395 sign -1, scan ln -3609.788395 sign -1, |d ln| 0.000e+00
evals: 0.11000000 +1 ln -3607.330679 dln 2.65e-06 robust True 487 s; 0.12000000 -1 ln -3609.788395 dln 6.97e-06 robust True 486 s; 0.11921124 -1 ln -3610.195889 dln 1.19e-05 robust True 485 s; 0.11772778 +1 ln -3611.647672 dln 6.38e-05 robust True 486 s; 0.11800924 -1 ln -3613.630974 dln 4.44e-04 robust True 486 s; 0.11797519 -1 ln -3617.253925 dln 1.69e-02 robust True 486 s; 0.11797019 +1 ln -3615.777369 dln 3.81e-03 robust True 487 s
dln largest 1.685e-02, mean seconds per evaluation 486
secant memory: 113 samples, lowest available 12.3 GiB, peak RSS 4.59 GiB
```


**Noise of the sign near the root (k_c 119 at D 22.875):** k_c 119 D 22.875   tol   5.000e-06   1.7e-02 (at 9.30e-07 from the root)   1.6e-08 to 1.6e-08   1.6e-07 (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1).


### Registrations and scoring
The registration was written in `kc119_d22875/README.md` before the regrid and its log entries score it. One item missed: the float64 sign equal to the hybrid sign at all 5 scan evaluations (registered 55%; it differed at both evaluations of 0.12, where the hybrid sign is -). Everything else held, including the steps of the regrid (3912 registered, 3912 read). The root: 0.120 registered (t5 0.122), +0.11797 read.

Chain held (`HOLD_low2.txt`, `HOLD_refine.txt`, `scan_chain.sh` pid 99672). Next (t5's order): k_c 127 at D 23.0625 from my k_c 119 state there (raw `I1025-macm3/kc127_d230625/`), with winb's k_c 127 at D 23.0 to give k_c 127's threshold; t5 registers the root at +0.003 +- 0.004.

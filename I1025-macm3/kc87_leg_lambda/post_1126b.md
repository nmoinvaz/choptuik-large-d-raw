**#1025 macm3, k_c 119 at D 23.0 (the fifth resolution): lambda_1 = +0.04106103, bracket 5e-6, regrid, scan and secant (2026-11-26 08:23 UTC).** t5's order (hc 26 Nov): "Post it on #1025, with any tail sum labeled arithmetic only." t5's register: the root at D 23.0 is +0.040 +- 0.003 (the last step 0.009058 times a ratio near 0.51); it is met. Roots are the det-linear root inside the final bracket of `d18_secant.py` (a3d90cd5, `--tol=1e-5 --maxev=10`, one process, `venv-macm3-1058b`), read by position.

### lambda_1 at D 23.0 by k_c (secant roots)


| k_c | state | root at D 23.0 [final bracket] | tool exit | step from the previous k_c | ratio of successive steps |
|---|---|---|---|---|---|
| 87 | my part c2 state (REDUCED QUALITY, psi-constraint 1.0496e-2) | **-0.02540417** [-0.02540491, -0.02539991] | 0 (tol 1e-5) |  |  |
| 95 | win2's accepted state (reduced-quality lineage, 7.67e-3) | **0.00870734** [0.00796052, 0.00873919] | 4 (nonrobust; width 7.8e-04) | +0.034112 |  |
| 103 | my regrid of it (5.03e-3) | **0.02650535** [0.02650441, 0.02650941] | 0 (tol 1e-5) | +0.017798 | 0.5218 |
| 111 | dh170's regrid of my k_c 103 state (3.48e-3) | **0.03556371** [0.03538070, 0.03558301] | 4 (nonrobust; width 2.0e-04) | +0.009058 | 0.5090 |
| 119 | my regrid of dh170's k_c 111 state (2.14e-3) | **0.04106103** [0.04105978, 0.04106478] | 0 (tol 1e-5) | +0.005497 | 0.6069 |


Steps +0.034112, +0.017798, +0.009058, +0.005497; ratios 0.5218, 0.5090, 0.6069. **Arithmetic only, not a result:** a geometric tail of the last ratio (0.6069) would end at 0.0495; the ratio is not constant (0.5218, 0.5090, 0.6069), so the tail is a guide to the size of the remaining steps and no more. t5's register for a converged lambda_1 is between -0.03 and +0.03; the D 23.0 roots now sit at +0.041 and are still rising.

### k_c 119 at D 23.0: regrid, scan, secant (raw `I1025-macm3/kc119_d23/`, README with the registration first, raw aa7da4fbf)


Source: dh170's accepted k_c 111 state at D 23.0 (raw `I1025-dh170/kc111_d23`, blob c0edd3c1, record 74d49790). The k_c 111 check accepted it (controls 1 1; the k_c 103 and k_c 119 checks refused it). `kc119_syscheck_1025.py` (raw `I1025-mac/checks` at 0d6db56f4, blob fc6e0dd6: the k_c 111 check with 111 changed to 119 and one added header comment line) accepted the result (controls 1 1; the k_c 111 check refused it). `ell_refine.py` 631e5801, 6 threads, `capped_run.py` 28800 s in place of `timeout` (macOS has none). k_c 119 record: D 23.0 |F| 3.2080e-10 steps 3914 psi-constraint 2.1389e-03 Delta 1.174324968657 (k_c 111 source: |F| 3.2561e-10 steps 3653 constraint 3.4835e-03 Delta 1.174326550481); Delta shift -1.5818e-06, steps ratio 1.071, constraint ratio 0.614. Wall 2282 s; peak RSS 5.64 GiB. The scan: -0.02 to 0.06 by 0.02 plus a repeat of 0.04 (the scan driver requires a repeat), run on 2 processes in 3 rounds (t5's change: about 7 GiB per k_c 119 process), `d18_hybsign.py` e089207a (the scan started before the scanner change); then the secant:

```
scan: 6 evaluations, 6 noise-robust; robust changes 1: (0.040, 0.060) + to - det-linear 0.046539 range [0.040232, 0.046539]
signs by lambda: -0.02+ 0.00+ 0.02+ 0.04+ 0.04+ 0.06-
float64 sign equals the hybrid sign at 4 of 6
repeat of 0.04 bit-identical (ln, f64_ln, sign): True
ln|det| by lambda: -0.02:-3571.332 0.00:-3573.888 0.02:-3576.715 0.04:-3581.863 0.04:-3581.863 0.06:-3581.141
secant: status tol (-), tol 1e-05, evaluations 7 (the two ends included), run wall 3390 s
secant root bracket [0.04105978, 0.04106478], width 5.000e-06, signs [1.0, -1.0], robust [True, True]; det-linear root 0.04106103; Brent's last point 0.04105978
scan reading: bracket (0.040, 0.060), det-linear 0.046539, estimator range [0.040232, 0.046539]
secant root inside the scan's estimator range: True; whole final bracket inside: True; root below the scan's det-linear: True
end lambda 0.04: secant ln -3581.863302 sign +1, scan ln -3581.863276 sign +1, |d ln| 2.573e-05
end lambda 0.06: secant ln -3581.141205 sign -1, scan ln -3581.141206 sign -1, |d ln| 5.074e-07
evals: 0.04000000 +1 ln -3581.863302 dln 2.70e-05 robust True 486 s; 0.06000000 -1 ln -3581.141205 dln 7.53e-07 robust True 483 s; 0.04653863 -1 ln -3580.927976 dln 4.39e-06 robust True 484 s; 0.04184288 -1 ln -3582.367651 dln 3.50e-05 robust True 483 s; 0.04114900 -1 ln -3584.477363 dln 3.17e-04 robust True 486 s; 0.04105978 +1 ln -3588.723695 dln 2.22e-02 robust True 485 s; 0.04106478 -1 ln -3587.632324 dln 7.55e-03 robust True 484 s
dln largest 2.216e-02, mean seconds per evaluation 484
secant memory: 113 samples, lowest available 12.9 GiB, peak RSS 5.03 GiB
```


**Noise of the sign near the root (k_c 119):** k_c 119 D 23.0   tol   5.000e-06   2.2e-02 (at 1.26e-06 from the root)   2.8e-08 to 2.8e-08   2.8e-07 (columns: case, tool status, bracket width, largest dln and its distance from the root, dln x distance, distance where dln reaches the bar 0.1). The product is constant to a few percent over the evaluations within 2e-4 of the root, as in the earlier cases (k_c 87 7.4e-9, k_c 95 3.6e-8 to 5.3e-8, k_c 103 4.5e-8 to 5.7e-8, k_c 111 5.8e-8 to 7.1e-8).


### Registrations and scoring
The registration was written in `kc119_d23/README.md` before the regrid and its log entries score it. Misses: the regrid's psi-constraint (registered 2.5e-3 from a ratio 0.72 that the earlier ratios 0.656, 0.693 did not support; the file has 2.139e-3, ratio 0.614); the float64 sign differing from the hybrid sign at 2 of the 6 scan evaluations and at 4 of the 7 secant evaluations (the double-double block 12 decides the sign near the root); the scan wall (50.6 min against 70 to 150: two processes ran 17 min per round). Everything else registered held, including the root: +0.0401 registered (t5 +0.040 +- 0.003), +0.04106 read.

**Scanner change (t5, hc 26 Nov):** scans that have not started use `d18_secant.py scan` (wip/ell1-speed 92b9bf53, blob eb1396ad); this scan was already running and keeps `d18_hybsign.py`. The new scanner's selftest exits 0 and `--mutate=half`, `norobust`, `nosigncheck` exit 1 (logged in the READMEs; the next folder `kc119_d230625/` uses it). **Running now:** k_c 119 at D 23.0625 from my k_c 111 state there (raw `I1025-macm3/kc119_d230625/`), to give k_c 119's threshold zero (t5 registers the root at -0.004 +- 0.005 and the zero near D 23.057; dh370 runs the same point on Linux as the cross-check). Chain held.

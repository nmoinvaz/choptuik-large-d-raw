M = 1 zeros read: 25, sum of orientations -1 (inputs/zeros_M1.md)

| zero | xi1 | converged (A, w/w_inf) | \|r1\| | \|r3\| | \|r5\| | solves | Newton step | M3 -> 5 shift (dA, dw), norm | \|F5\|/\|F3\| |
|---|---|---|---|---|---|---|---|---|---|
| x1 | 0.2 | not converged | | | | | | | |
| x1 | 0.25 | not converged | | | | | | | |
| x2 | 0.2 | not converged | | | | | | | |
| x2 | 0.25 | not converged | | | | | | | |

Start solve of each walk (A, w/w_inf and the harmonics at the M = 3 zero; F_nu/F_1 from the solve; the walk goes on only when |r_3|, |r_5| are under 1e-6)

| walk | xi1 | \|r1\| | \|r3\| | \|r5\| | \|F3\| | \|F5\| | \|F5\|/\|F3\| | walk |
|---|---|---|---|---|---|---|---|---|
| control | 0.2 | 1.21e+02 | 2.7e-08 | 3.8e-10 | 0.0539 | 0.0030 | 0.0556 | converged, 7 solves |
| control | 0.25 | 4.53e+07 | 8.3e+03 | 1.2e-10 | 0.0520 | 0.0028 | 0.0548 | start solve not converged |
| x1 | 0.2 | 7.88e+07 | 2.1e+05 | 1.9e-06 | 0.2525 | 0.0839 | 0.3321 | start solve not converged |
| x1 | 0.25 | 6.66e+06 | 1.9e+05 | 1.0e-05 | 0.2553 | 0.0851 | 0.3333 | start solve not converged |
| x2 | 0.2 | 1.81e+06 | 3.3e+05 | 2.4e+03 | 0.3290 | 0.1775 | 0.5395 | start solve not converged |
| x2 | 0.25 | 4.03e+07 | 1.0e+06 | 1.2e+05 | 0.3263 | 0.2114 | 0.6479 | start solve not converged |

x1: M = 3 zero (3.446218246, 0.347606965); M = 1 partner (+1) (3.307235, 0.367124) located at xi1 0.2, M1 -> 3 shift (+0.13898, -0.01952), distance 0.14035; bar 0.14035
    VERDICT x1: FAILS (xi1 0.2: no converged walk (the start solve did not converge: |r_3| 2.1e+05 |r_5| 1.9e-06 not under 1e-06); xi1 0.25: no converged walk (the start solve did not converge: |r_3| 1.9e+05 |r_5| 1.0e-05 not under 1e-06))
x2: M = 3 zero (3.526473057, 0.211497981); M = 1 partner (+1) (3.674531, 0.360326) located at xi1 0.2, 0.25, M1 -> 3 shift (-0.14806, -0.14883), distance 0.20993; bar 0.20993
    VERDICT x2: FAILS (xi1 0.2: no converged walk (the start solve did not converge: |r_3| 3.3e+05 |r_5| 2.4e+03 not under 1e-06); xi1 0.25: no converged walk (the start solve did not converge: |r_3| 1.0e+06 |r_5| 1.2e+05 not under 1e-06))

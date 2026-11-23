M = 1 zeros read: 25, sum of orientations -1 (inputs/zeros_M1.md)

| zero | xi1 | converged (A, w/w_inf) | \|r1\| | \|r3\| | \|r5\| | solves | Newton step | M3 -> 5 shift (dA, dw), norm | \|F5\|/\|F3\| |
|---|---|---|---|---|---|---|---|---|---|
| x1 | 0.2 | not converged | | | | | | | |
| x1 | 0.25 | not converged | | | | | | | |
| x2 | 0.2 | not converged | | | | | | | |
| x2 | 0.25 | not converged | | | | | | | |

x1: M = 3 zero (3.446218246, 0.347606965); M = 1 partner (+1) (3.307235, 0.367124) located at xi1 0.2, M1 -> 3 shift (+0.13898, -0.01952), distance 0.14035; bar 0.14035
    VERDICT x1: FAILS (xi1 0.2: no converged walk (the start solve did not converge: |r_3| 2.1e+05 |r_5| 1.9e-06 not under 1e-06); xi1 0.25: no converged walk (the start solve did not converge: |r_3| 1.9e+05 |r_5| 1.0e-05 not under 1e-06))
x2: M = 3 zero (3.526473057, 0.211497981); M = 1 partner (+1) (3.674531, 0.360326) located at xi1 0.2, 0.25, M1 -> 3 shift (-0.14806, -0.14883), distance 0.20993; bar 0.20993
    VERDICT x2: FAILS (xi1 0.2: no converged walk (the start solve did not converge: |r_3| 3.3e+05 |r_5| 2.4e+03 not under 1e-06); xi1 0.25: no converged walk (the start solve did not converge: |r_3| 1.0e+06 |r_5| 1.2e+05 not under 1e-06))

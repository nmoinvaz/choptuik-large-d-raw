D3.425_M128_r2: D 3.425, M 128, F after the polish 2.613e-30, guess lam 3.234107724 (gamma guess 0.309204), sign changes 1, determinants 6, lam 3.2341078267095367, gamma 0.3092042855656502, own seconds 1243.6

polish lines:
- newton 0: |F| 2.61e-30 converged (last |dz| 1.2e-25) Delta 3.383586550373866

| lam | sign | ln\|det\| | pivots | s |
|---|---|---|---|---|
| 3.234007723755 | -1 | 1379.034911 | 9.32e-04..8.75e+01 | 165.9 |
| 3.234107723755 | -1 | 1372.224936 | 9.32e-04..8.75e+01 | 172.3 |
| 3.234107819785 | -1 | 1369.525716 | 9.32e-04..8.75e+01 | 203.3 |
| 3.234107826705 | -1 | 1362.282893 | 7.53e-06..8.75e+01 | 225.4 |
| 3.234107826710 | +1 | 1357.668930 | 7.47e-08..8.75e+01 | 220.7 |
| 3.234207723755 | +1 | 1379.172234 | 9.32e-04..8.85e+01 | 165.7 |

bracket scanned: lam 3.234008 .. 3.234208, gamma 0.309195 .. 0.309214; signs [-1, 1]
seconds per determinant: mean 192.2, min 165.7, max 225.4; sum 1153 of the run's 1244 s

root lam 3.2341078267095367 (brentq, xtol 1e-11), gamma 0.3092042855656502; sign -1 below the root, +1 above: 3.2340077238:-1, 3.2341077238:-1, 3.2341078198:-1, 3.2341078267:-1, 3.2341078267:+1, 3.2342077238:+1
local slope d ln|det| / d ln|lam - lam*| between the points with |lam - lam*| > 1e-9 (a simple zero gives 1):
- |lam - lam*| 1.001e-04 -> 9.990e-05: ln|det| 1379.034911 -> 1379.172234, slope -66.691
- |lam - lam*| 9.990e-05 -> 1.030e-07: ln|det| 1379.172234 -> 1372.224936, slope 1.010
- |lam - lam*| 1.030e-07 -> 6.925e-09: ln|det| 1372.224936 -> 1369.525716, slope 1.000
lam_guess(3.5) = 3.092124 against 1/gamma(3.5) = 3.101876 (#628's M 128 gamma 0.3223855827556097): the guess misses by -0.009751 at D 3.5

M128: D 3.15, M 128, F after the polish 1.103e-28, guess lam 3.713742062 (gamma guess 0.269270), sign changes 0, determinants 9, lam None, gamma None, own seconds 3070.0

polish lines:
- newton 0: |F| 6.69e-26 |dz| 2.10e-22 lam 1 dDelta +1.49e-31 Delta 2.961319687827138 piv 2.2e-04..9.3e+00  t 141.2s
- newton 1: |F| 1.29e-28 |dz| 9.18e-27 lam 1 dDelta -7.57e-31 Delta 2.961319687827138 piv 2.2e-04..9.3e+00  t 294.6s

| lam | sign | ln\|det\| | pivots | s |
|---|---|---|---|---|
| 3.673742062090 | -1 | 2230.826596 | 2.65e-04..2.90e+02 | 337.1 |
| 3.703742062090 | -1 | 2254.866799 | 2.65e-04..3.16e+02 | 308.7 |
| 3.712742062090 | -1 | 2262.078488 | 2.64e-04..3.24e+02 | 296.9 |
| 3.713642062090 | -1 | 2262.799647 | 2.68e-04..3.25e+02 | 252.8 |
| 3.713742062090 | -1 | 2262.879776 | 2.68e-04..3.25e+02 | 299.9 |
| 3.713842062090 | -1 | 2262.959904 | 2.68e-04..3.25e+02 | 282.8 |
| 3.714742062090 | -1 | 2263.681061 | 2.68e-04..3.26e+02 | 306.1 |
| 3.723742062090 | -1 | 2270.892530 | 2.67e-04..3.35e+02 | 322.2 |
| 3.753742062090 | -1 | 2294.929397 | 2.67e-04..3.65e+02 | 368.1 |

bracket scanned: lam 3.673742 .. 3.753742, gamma 0.266401 .. 0.272202; signs [-1]
d ln|det| / d lam between neighbouring points: min 801.2, max 801.3 (ln|det| rises with lam at every pair: True)
seconds per determinant: mean 308.3, min 252.8, max 368.1; sum 2775 of the run's 3070 s
lam_guess(3.5) = 3.092124 against 1/gamma(3.5) = 3.101876 (#628's M 128 gamma 0.3223855827556097): the guess misses by -0.009751 at D 3.5

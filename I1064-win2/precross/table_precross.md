| state | order | exit, wall | gate | start max\|F\| (step 0) | od steps | last od line max\|F\| | how it stopped |
|---|---|---|---|---|---|---|---|
| D 260.0073 | 293 | exit 0, 62 s | converged | 3.97e-36 | 1 | 4.0e-36, converged | on 0: |F| 3.97e-36 converged, Delta 1.68339065769672547 +7.7616e-18 |
| D 260.0073 | 315 | exit 0, 2883 s | failed | 9.54e-12 | 3 | 5.7e-11, not converged | on 2: |F| 5.67e-11, |dz| 4.02e-20: no trial step accepted, stopping |
| D 259.4568 | 293 | exit 0, 62 s | converged | 2.51e-36 | 1 | 2.5e-36, converged | on 0: |F| 2.51e-36 converged, Delta 1.68347350066287960 -4.2264e-17 |
| D 259.4568 | 315 | exit 0, 2625 s | failed | 1.57e-11 | 2 | 2.7e-11, not converged | on 1: |F| 2.71e-11, |dz| 2.91e-20: no trial step accepted, stopping |

gate lines:
- D 260.0073 ks 293: converged: last octo-double Newton line 1 steps, max|F| 4.0e-36, converged, base saved True
- D 260.0073 ks 315: failed: last octo-double Newton line 3 steps, max|F| 5.7e-11, not converged, base saved False
- D 259.4568 ks 293: converged: last octo-double Newton line 1 steps, max|F| 2.5e-36, converged, base saved True
- D 259.4568 ks 315: failed: last octo-double Newton line 2 steps, max|F| 2.7e-11, not converged, base saved False

start max|F| at order 315 for comparison:
- D 261.0721 (dh610's ks 315, `I1064-dh610/ks315.log`): 1.36e-11
- D 261.0721 (dh610's ks 295, `I1064-dh610/ks295.log`; the figure in the hc): 1.35e-11
- D 261.6229 (the first arm on win2, `../ks315.log`): 1.15e-08

READING: no ks 315 converged: compare the start |F| above with D 261.0721's and D 261.6229's (the coordinator's reading)

delta information (Delta(b) - Delta(a)):
- _D259.4568_ctl_vs_state: 0.0 (same D True, ok True)
- _D260.0073_ctl_vs_state: 0.0 (same D True, ok True)
  delta1064_D260.0073_ctl_vs_state: exit 0, xcheck exit 0: D 260.0072663205446736; Delta(b) - Delta(a) = 0.0
  delta1064_D259.4568_ctl_vs_state: exit 0, xcheck exit 0: D 259.4567664040657674; Delta(b) - Delta(a) = 0.0

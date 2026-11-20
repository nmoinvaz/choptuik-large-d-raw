# #1033 run 3 and run 4: Delta - Delta(384) against the plans (plan_vs_delta_1033.py)

Delta(384) = T82-win's stored M 384 state, Delta 2.4660121465217122, stored plan 1623 steps; Delta(320) = its stored M 320 state, stored plan 1619 steps; |Delta(384) - Delta(320)| = 3.771e-11. Start state of every solve: the stored M 384 state (T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M384.npz) interpolated in double-double onto the arctan map (L, M', s0), the state itself at L 1, M' 384, and its truncation at L 1, M' 320.

Plan columns: start = the start state's own plan (the stored M 384 plan, split as the gate label says, then re-planned at the start state); pass 2 = the plan of the pass-1 state, the plan the final solve to |F| < 1e-28 ran on (the L 1 identity skips pass 1, so it ran on its start plan); own = the plan of the converged state, made after the solve (a size measure, not used to solve). rho = own / 1623.

| run | L | M' | start state | plan source (gate) | start | pass 2 | own | rho | converged | Delta - Delta(384) | group | own class |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 1 | 384 | stored M 384 itself | stored plan; pass 1 skipped (start below tol1) | 2317 | 2317 | 2842 | 1.751 | yes | +1.128e-30 | lo | far |
| 4B | 1 | 320 | stored M 384, truncated | stored plan | 4235 | 2136 | 1618 | 0.997 | yes | +3.771e-11 | hi | near |
| 4A | 0.9 | 320 | stored M 384, interpolated | stored plan | 3918 | 1797 | 1437 | 0.885 | yes | +2.910e-12 | other | near |
| 4A | 0.8 | 320 | stored M 384, interpolated | stored plan split 2 | 3736 | 1973 | 1885 | 1.161 | yes | -1.738e-13 | lo | near |
| 4A | 0.8 | 256 | stored M 384, interpolated | stored plan | 3151 | 1888 | 1779 | 1.096 | yes | +3.813e-11 | hi | near |
| 4A | 0.7 | 320 | stored M 384, interpolated | stored plan split 2 | 3510 | 2189 | 2063 | 1.271 | yes | -3.193e-13 | lo | inter |
| 4A | 0.7 | 256 | stored M 384, interpolated | stored plan | 3027 | 1991 | 1888 | 1.163 | yes | +6.474e-13 | lo | near |
| 4B | 0.6 | 256 | stored M 384, interpolated | stored plan split 2 | 2939 | 1900 | 1900 | 1.171 | **no** | -2.947e-13 | lo | near |
| 4B | 0.6 | 192 | stored M 384, interpolated | stored plan | 2325 | 1643 | 1516 | 0.934 | yes | +3.763e-11 | hi | near |
| 4B | 0.5 | 256 | stored M 384, interpolated | stored plan split 2 | 2964 | 1702 | 1561 | 0.962 | yes | -3.211e-13 | lo | near |
| 3 | 0.5 | 192 | stored M 384, interpolated | stored plan | 2302 | 1388 | 1292 | 0.796 | yes | +5.127e-13 | lo | near |
| 4B | 0.5 | 160 | stored M 384, interpolated | stored plan | 1964 | 1313 | 1188 | 0.732 | yes | +5.581e-11 | other | short |
| 3 | 0.4 | 192 | stored M 384, interpolated | stored plan split 2 | 2400 | 1355 | 1234 | 0.760 | yes | -1.932e-13 | lo | near |
| 4B | 0.4 | 160 | stored M 384, interpolated | stored plan | 2093 | 1218 | 1083 | 0.667 | yes | +8.359e-12 | other | short |
| 4B | 0.3 | 160 | stored M 384, interpolated | stored plan split 2 | 2308 | 1226 | 1058 | 0.652 | yes | -3.227e-13 | lo | short |
| 4B | 0.3 | 128 | stored M 384, interpolated | stored plan split 2 | 1850 | 1083 | 922 | 0.568 | yes | +1.672e-12 | other | short |
| 4B | 0.2 | 160 | stored M 384, interpolated | stored plan split 2 (failed: pass 1: line search) | 3192 | - | - | - | **failed** | none recorded | failed | - |
| 4B | 0.2 | 128 | stored M 384, interpolated | stored plan split 2 (failed: pass 1: no |F| below tol1 in it1 calls) | 2591 | - | - | - | **failed** | none recorded | failed | - |

Groups: hi = 3.6e-11 to 4.0e-11, lo = |d| < 1e-12, other = neither, failed = no Delta. Own class: far = rho >= 1.5, near = 0.75 to 1.25, inter = 1.25 to 1.5, short < 0.75.

## The prediction

- as ordered (near 0.75 to 1.25, all solves): **fails**. P1, hi group with a far own plan: 0 of 3. P2, lo group with a near own plan: 6 of 9.
- unconverged solves dropped: **fails**. P1, hi group with a far own plan: 0 of 3. P2, lo group with a near own plan: 5 of 8.
- wider near band 0.6 to 1.4: **fails**. P1, hi group with a far own plan: 0 of 3. P2, lo group with a near own plan: 8 of 9.

hi group (3): L 1 M' 320: own 1618, pass 2 2136, start 4235, +3.771e-11; L 0.8 M' 256: own 1779, pass 2 1888, start 3151, +3.813e-11; L 0.6 M' 192: own 1516, pass 2 1643, start 2325, +3.763e-11.
lo group (9), own plan steps: 1058 (L 0.3 M' 160), 1234 (L 0.4 M' 192), 1292 (L 0.5 M' 192), 1561 (L 0.5 M' 256), 1885 (L 0.8 M' 320), 1888 (L 0.7 M' 256), 1900 (L 0.6 M' 256, unconverged), 2063 (L 0.7 M' 320), 2842 (L 1 M' 384).
other (4): L 0.9 M' 320: own 1437, +2.910e-12; L 0.5 M' 160: own 1188, +5.581e-11; L 0.4 M' 160: own 1083, +8.359e-12; L 0.3 M' 128: own 922, +1.672e-12.
- start plan steps: hi group 2325 to 4235, lo group 2302 to 3736 (the ranges overlap: no threshold separates the groups).
- pass-2 plan steps: hi group 1643 to 2136, lo group 1226 to 2317 (the ranges overlap: no threshold separates the groups).
- own plan steps: hi group 1516 to 1779, lo group 1058 to 2842 (the ranges overlap: no threshold separates the groups).

## Is Delta moved by the plan? The two identity solves

Each starts from a stored T82-win state and solves on a plan longer than the stored one; Delta - Delta(own state) after the solve:

| solve | stored plan | plan the solve ran on | Delta - stored Delta of that state |
|---|---|---|---|
| L 1, M' 384 (from M 384) | 1623 | 2317 (pass 1 skipped) | +1.13e-30 |
| L 1, M' 320 (M 384 truncated; Delta compared with the stored M 320 state) | 1619 | 2136 (start plan 4235) | +6.15e-29 |

## Delta - Delta(384) against M' at each L (converged solves; the largest M' of each L is the last row)

| L | M' : Delta - Delta(384) |
|---|---|
| 1 | 320: +3.77e-11, 384: +1.13e-30 |
| 0.9 | 320: +2.91e-12 |
| 0.8 | 256: +3.81e-11, 320: -1.74e-13 |
| 0.7 | 256: +6.47e-13, 320: -3.19e-13 |
| 0.6 | 192: +3.76e-11, 256: -2.95e-13 (unconverged) |
| 0.5 | 160: +5.58e-11, 192: +5.13e-13, 256: -3.21e-13 |
| 0.4 | 160: +8.36e-12, 192: -1.93e-13 |
| 0.3 | 128: +1.67e-12, 160: -3.23e-13 |
| 0.2 | 128: failed, 160: failed |

|Delta - Delta(384)| does not increase with M' in 6 of 6 L ladders with two or more converged M' (L 0.3, 0.4, 0.5, 0.7, 0.8, 1).

Converged solves between -3.3e-13 and -3.1e-13 (different L and M'): L 0.7 M' 320 -3.193e-13, L 0.5 M' 256 -3.211e-13, L 0.3 M' 160 -3.227e-13; spread 3.4e-15.

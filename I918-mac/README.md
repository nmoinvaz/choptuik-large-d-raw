# I918-mac: the sigma-model kernel's mode matrix and growth rates

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/918. Code: branch `wip/sa-918`
(`matter/sigma_ms`: `src/model.rs`, `src/python.rs`, `smdriver.py`, `mode_check.py`, `mode_lam.py`, `mode_table.py`).
The kernel module was built from that branch into a new site directory (`out/build.log`: 10 min 12 s, peak 9.8 GB;
the site of #652 is untouched) and run with python 3.14, one process with 2 threads at nice 10. Every run starts
behind a gate on the 1-minute load, below 31 (`out/gate.log`, and the `load` and `waiting` lines of the logs). Local
paths are removed from the copies here.

This file is the pilot's state. It is rewritten when the runs end.

## The build at rate zero (`bitcheck.py`)

The residual and the Newton step of two states (D 4 at eta 1, D 10.5 at eta 0.3) are the same bits in the new build
and in the build of #652 (hashes 142b2dc23343b621 and a210bd14cc91971a in both).

## The checks at D 9, eta 1, M 32 (`out/check_D9_eta1*.txt`, `.json`)

The state is #652's chain's (`I652-mac/out/sm_eta1_D9_M32.npz`, max |F| 4.2e-29).

| check | bound | result | verdict |
|---|---|---|---|
| (1) M(0) against the Jacobian's leading block | 1e-28 of the largest entry | 0 (the same bits) | PASS |
| (2) dM/dlambda at 1.7, real rates against a complex one | 1e-7 | 5.1e-11 | PASS |
| (3) the tau-translation mode, \|M(0) v\| over \|M(0)\|_F \|v\| | 1e-9 | 1.0e-13 | PASS |
| (4) the gauge root against lambda_g = 0.824242706019437 | 1e-10 | det M changes sign between lambda_g and lambda_g + 5.0e-14 | PASS |

Each mutation exits 1 (`out/mutations.txt`, from the statuses in `out/gate.log`):

| mutation | check | what the check then reads |
|---|---|---|
| sigma_h | (1) | difference 3.3e-10 of the largest entry |
| real_solve | (2) | 4.6e-2 |
| vtau | (3) | 1.2e-2 |
| rate_horizon | (4) | no sign change within lambda_g (1 -+ 1e-2) |
| rate_lu | (4) | no sign change within lambda_g (1 -+ 1e-2) |
| rate_centre | (4) | the root 3.4e-3 below lambda_g |
| rate_steps | (4) | no sign change within lambda_g (1 -+ 1e-2) |

## The checks at D 4, eta 1, M 32 (`out/check_D4_eta1.txt`)

(1) the same bits and (2) 1.1e-10 pass. (3) reads 3.6e-7 and (4) puts the root 1.32e-6 below lambda_g =
0.898137277266780: both fail their bounds. The tau resolution at D 4 is far coarser than at D 9: the centre datum's
top harmonic is 1.5e-4 at M 32 (2.4e-13 at D 9), and Delta(32) is 5.9e-8 from Delta(48) at eta = inf (1e-23 at
D 10.5). The M 48 state at D 4 tests this reading.

## Growth rates (`out/sm_lam.jsonl`, `out/lam_*.txt`, `out/mode_table.txt`)

State at 2026-11-16 21:00 UTC: both chains done at M 32, the other M at eta 0.3 done (M 48 at eta 1, the scan, D 4 at
M 48 and the 27-node state are running). `out/mode_table.txt` is `matter/sigma_ms/mode_table.py <raw clone>`:

```
(1) the gauge root at the 17 states with D >= 9: largest distance from lambda_g 5.0e-14 (<= 1e-10): PASS
      validation state eta inf, D 4, M 32, 21 nodes: 1.5e-04 (outside 1e-10)
      validation state eta 1, D 4, M 32, 21 nodes: 1.3e-06 (outside 1e-10)
      validation state eta 1, D 6, M 32, 21 nodes: 5.0e-14 (within 1e-10)
(2) against sigdss:
      eta 1, D 4: kernel 8.646844471, sigdss k_c 15 8.648383723, difference -1.54e-03 (<= 8.6e-03 in size, k_c 15 - 23 at eta inf, D 4): PASS
      eta inf, D 4: kernel 8.410188780, l = 1 solver, k_c 23 8.410420010, difference -2.31e-04 (<= 8.6e-03 in size, k_c 15 - 23 at eta inf, D 4): PASS
      eta 1, D 6: kernel 3.806221096, sigdss k_c 23 3.806221595, difference -4.99e-07 (<= 2.6e-06 in size, k_c 15 - 23 there): PASS
      eta 1, D 9: kernel 3.048323164, sigdss k_c 23 3.048509322, difference -1.86e-04 (<= 4.2e-04 in size, k_c 15 - 23 there): PASS
      eta 0.3, D 9: kernel 3.175331722, sigdss k_c 15 3.175316160, difference +1.56e-05 (<= 4.2e-04 in size, k_c 15 - 23 at eta 1, D 9): PASS
lambda(D) at eta 0.3, M 32, D 9 to 11: 9: 3.175331722, 9.5: 3.112288835, 10: 3.057696912, 10.25: 3.033019318, 10.5: 3.009854092, 10.75: 2.988055282, 11: 2.967495609
    slopes d lambda / dD up to each D: 9.5: -0.12609, 10: -0.10918, 10.25: -0.09871, 10.5: -0.09266, 10.75: -0.08720, 11: -0.08224
    lambda falls at every step, by 0.207836 in all and by 0.020560 over the last one
    resolution: D 10.5, M 24, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    resolution: D 10.5, M 48, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    resolution: D 11, M 24, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    resolution: D 11, M 48, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    largest 5.2e-14
lambda(D) at eta 1, M 32, D 9 to 11: 9: 3.048323164, 10: 2.943442641, 10.475: 2.902932743, 10.75: 2.881573903, 11: 2.863317652
    slopes d lambda / dD up to each D: 10: -0.10488, 10.475: -0.08528, 10.75: -0.07767, 11: -0.07303
    lambda falls at every step, by 0.185006 in all and by 0.018256 over the last one
    resolution: D 10.475, M 24, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    largest 5.2e-14

| η | D | M, nodes | λ_g | gauge root's distance | λ | γ = 1/λ | sigdss's λ | kernel minus sigdss |
|---|---|---|---|---|---|---|---|---|
| inf | 4 | 32, 21 | 0.8952991749 | 1.5e-04 | 8.4101887800 | 0.1189033952 | 8.410420 (l = 1 solver, k_c 23) | -2.3e-04 |
| 1 | 4 | 32, 21 | 0.8981372773 | 1.3e-06 | 8.6468444707 | 0.1156491253 | 8.648384 (lam_d4b, k_c 15) | -1.5e-03 |
| 1 | 6 | 32, 21 | 0.8484953915 | 5.0e-14 | 3.8062210963 | 0.2627277751 | 3.806224 (m1up, k_c 15) | -3.1e-06 |
| 1 | 6 | 32, 21 | 0.8484953915 | 5.0e-14 | 3.8062210963 | 0.2627277751 | 3.806222 (refine_kc23, k_c 23) | -5.0e-07 |
| 1 | 9 | 32, 21 | 0.8242427060 | 5.0e-14 | 3.0483231643 | 0.3280492081 | 3.048927 (m1up, k_c 15) | -6.0e-04 |
| 1 | 9 | 32, 21 | 0.8242427060 | 5.0e-14 | 3.0483231643 | 0.3280492081 | 3.048509 (refine_kc23, k_c 23) | -1.9e-04 |
| 1 | 10 | 32, 21 | 0.8225574978 | 5.0e-14 | 2.9434426411 | 0.3397382324 | 2.919800 (m1up, k_c 15) | +2.4e-02 |
| 1 | 10 | 32, 21 | 0.8225574978 | 5.0e-14 | 2.9434426411 | 0.3397382324 | 2.919835 (refine_kc23, k_c 23) | +2.4e-02 |
| 1 | 10.475 | 24, 21 | 0.8223798899 | 5.0e-14 | 2.9029327426 | 0.3444792176 |  |  |
| 1 | 10.475 | 32, 21 | 0.8223798899 | 5.0e-14 | 2.9029327426 | 0.3444792176 |  |  |
| 1 | 10.75 | 32, 21 | 0.8224256353 | 5.0e-14 | 2.8815739028 | 0.3470325710 |  |  |
| 1 | 11 | 32, 21 | 0.8225512961 | 5.0e-14 | 2.8633176520 | 0.3492452188 |  |  |
| 0.3 | 9 | 32, 21 | 0.8080057588 | 5.0e-14 | 3.1753317225 | 0.3149277264 | 3.175316 (m03up, k_c 15) | +1.6e-05 |
| 0.3 | 9.5 | 32, 21 | 0.8082675083 | 5.0e-14 | 3.1122888346 | 0.3213069394 |  |  |
| 0.3 | 10 | 32, 21 | 0.8089333660 | 5.0e-14 | 3.0576969120 | 0.3270435327 | 3.081424 (m03up, k_c 15) | -2.4e-02 |
| 0.3 | 10 | 32, 21 | 0.8089333660 | 5.0e-14 | 3.0576969120 | 0.3270435327 | 3.081100 (refine_kc23, k_c 23) | -2.3e-02 |
| 0.3 | 10.25 | 32, 21 | 0.8093913761 | 5.0e-14 | 3.0330193184 | 0.3297044611 |  |  |
| 0.3 | 10.5 | 24, 21 | 0.8099211399 | 5.0e-14 | 3.0098540917 | 0.3322420189 |  |  |
| 0.3 | 10.5 | 32, 21 | 0.8099211399 | 5.0e-14 | 3.0098540917 | 0.3322420189 | 3.068528 (m03hi, k_c 15) | -5.9e-02 |
| 0.3 | 10.5 | 32, 21 | 0.8099211399 | 5.0e-14 | 3.0098540917 | 0.3322420189 | 3.068523 (refine_kc23, k_c 23) | -5.9e-02 |
| 0.3 | 10.5 | 48, 21 | 0.8099211399 | 5.0e-14 | 3.0098540917 | 0.3322420189 |  |  |
| 0.3 | 10.75 | 32, 21 | 0.8105151692 | 5.0e-14 | 2.9880552818 | 0.3346658297 |  |  |
| 0.3 | 11 | 24, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 |  |  |
| 0.3 | 11 | 32, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 | 3.112655 (m03hi, k_c 15) | -1.5e-01 |
| 0.3 | 11 | 32, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 | 3.112436 (refine_kc23, k_c 23) | -1.4e-01 |
| 0.3 | 11 | 48, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 |  |  |

MODE TABLE: PASS
```

The gate of 31 was dropped at 16:50 UTC for the remaining runs (the issue's comment of that time); the load at each
start is in the logs' start lines. One determinant takes 33 to 80 s at M 32, depending on the load.

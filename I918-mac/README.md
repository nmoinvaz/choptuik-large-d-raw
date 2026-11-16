# I918-mac: the sigma-model kernel's mode matrix and its growth rates from D 9 to 11

Machine: mac (Apple M5 Mac). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/918. Code: branch `wip/sa-918`
(`matter/sigma_ms`: `src/model.rs`, `src/python.rs`, `smdriver.py`, `mode_check.py`, `mode_lam.py`, `mode_table.py`).
The kernel module was built from that branch into a new site directory (`out/build.log`: 10 min 12 s, peak 9.8 GB;
the site of #652 is untouched) and run with python 3.14, one process with 2 threads at nice 10. Local paths are
removed from the copies here.

The load gate. The build, the checks, the mutations and the first growth rate (D 9, eta 1) started behind the gate
of 31 on the 1-minute load (`out/gate.log`: 20.1 to 28.0 at those starts). From 16:33 UTC the load was 90 to 144
from jobs outside this task, the next run waited 17 minutes (`out/waited/`), and at 16:50 UTC the coordinator
dropped the gate for the remaining runs (the issue's comment of that time). Their loads at the start are in the
`start` lines of `out/lam_*.txt` (14 to 97) and in `out/gate.log`.

## The build at rate zero (`bitcheck.py`)

The residual and the Newton step of two states (D 4 at eta 1, D 10.5 at eta 0.3) are the same bits in the new build
and in the build of #652 (hashes 142b2dc23343b621 and a210bd14cc91971a in both).

## The checks at D 9, eta 1, M 32 (`run_check.sh`, `run_mut.sh`, `out/check_D9_eta1*.txt`, `.json`)

The state is #652's chain's (`I652-mac/out/sm_eta1_D9_M32.npz`, max |F| 4.2e-29). The bounds are in `mode_check.py`'s
header and were fixed before its first run.

| check | bound | result | verdict |
|---|---|---|---|
| (1) M(0) against the Jacobian's leading block | 1e-28 of the largest entry | 0 (the same bits) | PASS |
| (2) dM/dlambda at 1.7, real rates against a complex one | 1e-7 | 5.1e-11 | PASS |
| (3) the tau-translation mode, \|M(0) v\| over \|M(0)\|_F \|v\| | 1e-9 | 1.0e-13 | PASS |
| (4) the gauge root against lambda_g = 0.824242706019437 | 1e-10 | det M changes sign between lambda_g and lambda_g + 5.0e-14 | PASS |

Each mutation exits 1 (`out/mutations.txt`, from the statuses in `out/gate.log`; `run_mut.sh`'s first version logged
`date`'s status instead, see its header):

| mutation | check | what the check then reads |
|---|---|---|
| sigma_h | (1) | difference 3.3e-10 of the largest entry |
| real_solve | (2) | 4.6e-2 |
| vtau | (3) | 1.2e-2 |
| rate_horizon | (4) | no sign change within lambda_g (1 -+ 1e-2) |
| rate_lu | (4) | no sign change within lambda_g (1 -+ 1e-2) |
| rate_centre | (4) | the root 3.4e-3 below lambda_g |
| rate_steps | (4) | no sign change within lambda_g (1 -+ 1e-2) |

## Growth rates (`run_pilot.sh`, `run_full.sh`, `run_extra.sh`, `run_extra2.sh`; `out/sm_lam.jsonl`, `out/lam_*.txt`)

`mode_lam.py` on each state: the gauge root, then the root nearest the guess. The states are #652's and #917's chain
at eta 1 (`I652-mac/out/`, `I917-mac/out/`), #916's at eta 0.3 (`I916-mac/out/`), #915's at M 24 and 48
(`I915-mac/out/`), #639's at eta inf (`I639-mac/data/`), and three made here in `out/`: D 11, eta 0.3 at M 24 and 48
(`run_eta_M.sh`, the recipe of #915: Delta(24) - Delta(32) = +2.1e-21 and Delta(48) - Delta(32) = +3.2e-23), and
#916's 27-node state at D 10.5 with its Taylor steps planned (`plan_state.py`, max |F| 1.2e-31).

`out/mode_table.txt` is `python3 matter/sigma_ms/mode_table.py <raw clone> --csv matter/sigma_ms/data/lam_D.csv`:

```
(1) the gauge root at the 19 states with D >= 9: largest distance from lambda_g 5.0e-14 (<= 1e-10): PASS
      validation state eta inf, D 4, M 32, 21 nodes: 1.5e-04 (outside 1e-10)
      validation state eta inf, D 4, M 48, 21 nodes: 1.5e-09 (outside 1e-10)
      validation state eta inf, D 4, M 64, 21 nodes: 5.1e-11 (within 1e-10)
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
    resolution: D 10.5, M 32, 27 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    resolution: D 11, M 24, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    resolution: D 11, M 48, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    largest 5.2e-14
lambda(D) at eta 1, M 32, D 9 to 11: 9: 3.048323164, 10: 2.943442641, 10.475: 2.902932743, 10.75: 2.881573903, 11: 2.863317652
    slopes d lambda / dD up to each D: 10: -0.10488, 10.475: -0.08528, 10.75: -0.07767, 11: -0.07303
    lambda falls at every step, by 0.185006 in all and by 0.018256 over the last one
    resolution: D 10.475, M 24, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    resolution: D 10.475, M 48, 21 nodes: lambda minus the base's +0.0e+00 +- 5e-14 (the two sign changes' half widths)
    largest 5.2e-14

| η | D | M, nodes | λ_g | gauge root's distance | λ | γ = 1/λ | sigdss's λ | kernel minus sigdss |
|---|---|---|---|---|---|---|---|---|
| inf | 4 | 32, 21 | 0.8952991749 | 1.5e-04 | 8.4101887800 | 0.1189033952 | 8.410420 (l = 1 solver, k_c 23) | -2.3e-04 |
| inf | 4 | 48, 21 | 0.8952991909 | 1.5e-09 | 8.4101578779 | 0.1189038321 |  |  |
| inf | 4 | 64, 21 | 0.8952991909 | 5.1e-11 |  |  |  |  |
| 1 | 4 | 32, 21 | 0.8981372773 | 1.3e-06 | 8.6468444707 | 0.1156491253 | 8.648384 (lam_d4b, k_c 15) | -1.5e-03 |
| 1 | 6 | 32, 21 | 0.8484953915 | 5.0e-14 | 3.8062210963 | 0.2627277751 | 3.806224 (m1up, k_c 15) | -3.1e-06 |
| 1 | 6 | 32, 21 | 0.8484953915 | 5.0e-14 | 3.8062210963 | 0.2627277751 | 3.806222 (refine_kc23, k_c 23) | -5.0e-07 |
| 1 | 9 | 32, 21 | 0.8242427060 | 5.0e-14 | 3.0483231643 | 0.3280492081 | 3.048927 (m1up, k_c 15) | -6.0e-04 |
| 1 | 9 | 32, 21 | 0.8242427060 | 5.0e-14 | 3.0483231643 | 0.3280492081 | 3.048509 (refine_kc23, k_c 23) | -1.9e-04 |
| 1 | 10 | 32, 21 | 0.8225574978 | 5.0e-14 | 2.9434426411 | 0.3397382324 | 2.919800 (m1up, k_c 15) | +2.4e-02 |
| 1 | 10 | 32, 21 | 0.8225574978 | 5.0e-14 | 2.9434426411 | 0.3397382324 | 2.919835 (refine_kc23, k_c 23) | +2.4e-02 |
| 1 | 10.475 | 24, 21 | 0.8223798899 | 5.0e-14 | 2.9029327426 | 0.3444792176 |  |  |
| 1 | 10.475 | 32, 21 | 0.8223798899 | 5.0e-14 | 2.9029327426 | 0.3444792176 |  |  |
| 1 | 10.475 | 48, 21 | 0.8223798899 | 5.0e-14 | 2.9029327426 | 0.3444792176 |  |  |
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
| 0.3 | 10.5 | 32, 27 | 0.8099211399 | 5.0e-14 | 3.0098540917 | 0.3322420189 |  |  |
| 0.3 | 10.75 | 32, 21 | 0.8105151692 | 5.0e-14 | 2.9880552818 | 0.3346658297 |  |  |
| 0.3 | 11 | 24, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 |  |  |
| 0.3 | 11 | 32, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 | 3.112655 (m03hi, k_c 15) | -1.5e-01 |
| 0.3 | 11 | 32, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 | 3.112436 (refine_kc23, k_c 23) | -1.4e-01 |
| 0.3 | 11 | 48, 21 | 0.8111668002 | 5.0e-14 | 2.9674956093 | 0.3369844919 |  |  |

30 rows -> matter/sigma_ms/data/lam_D.csv

MODE TABLE: PASS
```

Its mutations `gauge` and `sigdss` each exit 1.

What the table shows:

- lambda(D) falls at every step from D 9 to 11 at both couplings. sigdss's rise from 3.0685 (D 10.5) to 3.1124
  (D 11) at eta 0.3 is not on the kernel.
- The gauge root lies within 5.0e-14 of lambda_g at the 20 states from D 6 to 11.
- The rate does not depend on M (24, 32, 48) or on the node set (21, 27) beyond the root search's 5e-14.
- The scan (`out/lam_eta0.3_D11_scan.txt`): at D 11, eta 0.3, det M changes sign twice on 0.2 <= lambda <= 7 (35
  rates, 0.2 apart), in (0.8, 1.0) at the gauge rate and in (2.8, 3.0) at lambda.

## D 4 and the tau resolution

At D 4 the gauge root misses the bound of 1e-10 at M 32, and check (3) reads 3.6e-7 there
(`out/check_D4_eta1.txt`). The centre datum's top harmonic at eta inf is 5.5e-4 at M 32, 1.9e-6 at M 48 and 4.4e-8
at M 64 (`I639-mac`'s records), against 2.4e-13 at D 9, M 32.

| eta | M | lambda_g | gauge root minus lambda_g | lambda |
|---|---|---|---|---|
| 1 | 32 | 0.898137277267 | -1.32e-6 | 8.646844470746 |
| inf | 32 | 0.895299174899 | +1.457e-4 | 8.410188780024 |
| inf | 48 | 0.895299190857 | +1.503e-9 | 8.410157877871 |
| inf | 64 | 0.895299190854 | -5.07e-11 | not run (the gauge root only) |

From M 32 to 48 the top harmonic falls by 290 and the distance by 9.7e4, its square. From M 48 to 64 it falls by 43 and the distance by 30. So the gauge root's distance at D 4 is the tau resolution's, and the bound of 1e-10 is met there at M 64 only.

## Runs that did not count

- `out/waited/`: the D 6 run's log while it waited at the gate (16:33 to 16:50 UTC), before it was restarted.
- `out/failed/`: `plan_state.py`'s first version failed on the 27-node state's empty list of steps, so the run
  after it found no state; both logs are there, and the run was repeated. The M 64 run that had started meanwhile was
  stopped after 30 s and started again after it.
- One determinant of the M 48 run at D 10.5 took 1921 s instead of about 110 s, with the machine's load near 100.

## Cost

`mode_lam.py`: 25 records, 354 determinants, 7.1 hours of one process with 2 threads. Seconds per determinant, by the load:

| M | D | seconds |
|---|---|---|
| 24 | 6 to 11 | 12 to 15 |
| 32 | 6 to 11 | 28 to 49 |
| 32 | 4 | 88 to 92 |
| 48 | 6 to 11 | 137 to 331 |
| 48 | 4 | 227 to 227 |
| 64 | 4 | 710 to 710 |

The checks and mutations took 10 runs of `mode_check.py`, about 35 minutes. Memory was not measured. The mode
matrix's four double-double parts take 0.4 GB at M 32 and 1.6 GB at M 64.

## Recommended tasks

1. **The kernel's growth rate below D 9 and past D 11.** What: `mode_lam.py` on #652's chain states at eta 1 from
   D 4 to 9 (every 0.5), and the kernel's chains at eta 0.3 and 1 carried past D 11 with `chain.py` and the band
   solver (steps of 0.0625, to D 13 or the chain's stop), with their rates. Why: sections 5 and 7 of
   matter/SIGMA_DSS.md take lambda(D) and gamma(D) above D 9 from sigdss, which is 0.02 to 0.15 off the kernel
   there, and the large-D reading rests on those points. Acceptance: every state's gauge root within 1e-10 of
   lambda_g, or the state named with its distance; `chain_table.py`'s checks on each extended chain;
   `mode_table.py` passes and its two mutations exit 1; lambda(D) reported with its slopes. Cost: about 10 minutes
   per chain point and 8 per rate at M 32. Depends on #918.
2. **The count of unstable modes by the winding of det M.** What: `Solver.mode_logdet` takes complex rates now. Count
   the zeros of det M in the strip of height 2 omega (section 6) over 0.2 <= Re lambda <= 7 by the argument
   principle, at D 6 and D 11, eta 0.3 and 1, as notes/MODE_COUNT.md does for the scalar field. Why: section 6 lists
   complex growth rates as not checked, and sigdss's count was too expensive. The real scan here found two real roots
   at D 11. Acceptance: planted counts first (a contour around the gauge root alone gives 1, around lambda alone 1,
   around a region of the real scan without a sign change 0); the argument's step between neighbouring points stays
   below pi/2; the mutation `real_solve` (`set_mutate(15)`) changes a count or breaks that step condition. Depends on
   #918.
3. **The mode matrix in the opposite parity sector.** What: perturbations that break u(tau + Delta/2) = -u(tau) have
   the other harmonics in every field, so they need the even operator for p, m, psi and the odd one for a, c in
   `model.rs`'s tangents. Why: section 6 lists real rates of that sector as not checked. Acceptance: at D 6, eta 1
   the count of real roots in that sector on 0.2 <= lambda <= 7, with a check that the sector's matrix at rate 0
   annihilates no translation mode (its translation mode is in the background's sector) and a planted check of the
   two operators. Depends on #918. This is a change to the kernel's Rust and needs a build.

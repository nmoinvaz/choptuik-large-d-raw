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

## Growth rates (`out/sm_lam.jsonl`, `out/lam_*.txt`)

State at 2026-11-16 18:45 UTC, the eta 0.3 chain done at M 32 (the other M, eta 1 at D 10 to 11, the scan and D 4 at
M 48 are running). sigdss's value is its k_c 23 one at eta 1 (D 6, 9), its k_c 15 one elsewhere, and the l = 1
solver's at eta inf.

| eta | D | M | lambda_g | gauge root's distance | lambda | gamma = 1/lambda | sigdss | kernel minus sigdss |
|---|---|---|---|---|---|---|---|---|
| 1 | 9 | 32 | 0.824242706019 | 5.0e-14 | 3.048323164261 | 0.328049208077 | 3.048509 | -1.9e-04 |
| 1 | 6 | 32 | 0.848495391500 | 5.0e-14 | 3.806221096314 | 0.262727775054 | 3.806222 | -5.0e-07 |
| 1 | 4 | 32 | 0.898137277267 | 1.3e-06 | 8.646844470746 | 0.115649125341 | 8.648384 | -1.5e-03 |
| inf | 4 | 32 | 0.895299174899 | 1.5e-04 | 8.410188780024 | 0.118903395174 | 8.410420 | -2.3e-04 |
| 0.3 | 9 | 32 | 0.808005758845 | 5.0e-14 | 3.175331722462 | 0.314927726425 | 3.175316 | +1.6e-05 |
| 0.3 | 9.5 | 32 | 0.808267508337 | 5.0e-14 | 3.112288834615 | 0.321306939407 |  |  |
| 0.3 | 10 | 32 | 0.808933365985 | 5.0e-14 | 3.057696912012 | 0.327043532690 | 3.081424 | -2.4e-02 |
| 0.3 | 10.25 | 32 | 0.809391376068 | 5.0e-14 | 3.033019318405 | 0.329704461139 |  |  |
| 0.3 | 10.5 | 32 | 0.809921139867 | 5.0e-14 | 3.009854091669 | 0.332242018896 | 3.068528 | -5.9e-02 |
| 0.3 | 10.75 | 32 | 0.810515169160 | 5.0e-14 | 2.988055281843 | 0.334665829671 |  |  |
| 0.3 | 11 | 32 | 0.811166800229 | 5.0e-14 | 2.967495609278 | 0.336984491864 | 3.112655 | -1.5e-01 |

lambda(D) at eta 0.3 falls from D 9 to 11 on the kernel, with slopes -0.126, -0.109, -0.099, -0.093, -0.087 and
-0.082 per unit D. sigdss's rise from 3.0685 at D 10.5 to 3.1127 at D 11 is not there.

The gate of 31 was dropped at 16:50 UTC for the remaining runs (the issue's comment of that time); the load at each
start is in the logs' start lines. One determinant takes 33 to 80 s at M 32, depending on the load.

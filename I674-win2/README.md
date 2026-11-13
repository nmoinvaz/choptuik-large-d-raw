# I674-win2: the strong-row chord (--od_strong 4) on #603's class A refusals, A/B

Machine win2 (Windows 11 desktop, Intel Core Ultra 7 265K, 20 threads, 96 GB), 9 threads per run. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/674 (queued by the coordinator on the agent-msg channel, message 1794568351271-0, 2026-11-13: after #664, before #657).
Code: worktree `D:\choptuik-i674` at origin/main 58628d94 ("octo_corrector: a strong-row chord after the corrector's first step"); venv-i600 (the #600 build, hpkernel sha256 4ede9afe..., the kernel #603 runs on; the change is Python only). #603's chain is read in place and left running.
Runs (`run_674.sh`, one after the other): `anm_run.py ... --steps 1 --a0 <a> --od_accept natural [--od_strong 4]` from `I603-win2/chain/anm_pin3_D<base>.npz`, #603's other flags, at #603's own a for the attempt (attempt 0 of the step in its `anm_run.jsonl`, exact):

| attempt (class A) | base state | a0 | arms |
|---|---|---|---|
| 244.637 -> 245.637 | D244.6366 | 1.0 | A (chord), B (control: natural only) |
| 247.043 -> 248.019 | D247.0429 | 0.9765625 | A, B |
| 248.630 -> 249.393 | D248.6298 | 0.762939453125 | A; B is #644's natural run (`../I644-win2/natural/`) |
| 251.886 -> 252.613 | D251.8859 | 0.7275957614183426 | A, B |

Arm A: `--od_accept natural --od_strong 4`; arm B: `--od_accept natural`. A refused first attempt halves a and the run goes on to the retry. Outputs `<attempt>_armA/`, `<attempt>_armB/`, logs `<attempt>_armA.log`, `<attempt>_armB.log`, starts and exits in `exits_674.txt`.

Report (#674, the coordinator's message): per attempt and arm, the chord lines ("on 0 chord j: max|F| ..., |dw| ...") and its verdict line, then each Newton step's |F| and |dz|, converged or refused, and the seconds; where arm A converges, its Delta against #603's state at the same D_str to 1e-40, or the task fails. Acceptance of #674: `hp/newton_od_toy.py` passes with the chord on and its controls fire (the coordinator's); on each refused attempt max|F| <= 1e-60 at the attempt's D, or the task reports where the chord or the following Newton steps stop.

Results follow when the runs end.

## Results (2026-11-13 12:58:29 to 16:21:30 UTC)

`exits_674.txt`: seven runs, every exit 0, 3 h 23 min. `compare_674.py TAG ARM TARGET_FILE` (output in `compare_<attempt>_arm<A|B>.txt`) prints each arm's first attempt and, where converged, compares the saved state at the attempt's target D with #603's state of the same name (D_str, Delta, the eight parts summed exactly, zh, zl). Arm A is `--od_accept natural --od_strong 4`, arm B (the control) `--od_accept natural`; 248.630's arm B is #644's natural run (`../I644-win2/natural.log`, refused at the first Newton step in 63 s).

| attempt (a, exact) | arm A (chord) | arm B (natural only) | arm A's Delta against #603's state at the same D_str |
|---|---|---|---|
| 244.637 -> 245.637 (1.0) | **converged**: 3 chord steps (1.43e-24, 2.57e-42, 1.54e-52) + 4 Newton steps, 4.5e-75, 433 s | refused: 2 steps, stalled at 1.4e-27, 193 s | D_str equal, difference 3.3e-53, zh and zl bit for bit |
| 247.043 -> 248.019 (0.9765625) | **converged**: 3 chord steps (4.87e-22, 1.88e-37, 4.74e-49) + 8 Newton steps, 1.6e-79, 658 s | refused: 4 steps, stalled at 4.2e-26, 292 s | equal, difference 0.0, bit for bit |
| 248.630 -> 249.393 (0.762939453125) | **converged**: 3 chord steps (4.89e-25, 1.57e-41, 5.70e-52) + 4 Newton steps, 2.3e-67, 376 s | (#644) refused at the first step, 63 s | equal, difference 4.1e-49, bit for bit |
| 251.886 -> 252.613 (0.7275957614183426) | **refused**: 5 chord steps (6.90e-21, 5.51e-33, 4.11e-45, 3.64e-45, 3.52e-45; theta 3.05e-2, accepted) then 12 Newton steps at lam 0.5, max|F| 3.8e-48 at the cap, 1626 s | refused at the first step ("no trial step accepted", 1.7e-31, 56 s) | not applicable |

**The chord converged 3 of the 4 class A starts (244.637, 247.043, 248.630), each to #603's own state (differences 3.3e-53, 0.0 and 4.1e-49, against the 1e-40 required); natural alone refused all four.** The fourth, 251.886, is refused by the chord arm, not converged.

**What the 251.886 arm shows.** The chord's first three steps work as at the other attempts (6.9e-21 to 4.1e-45), then it stops improving: chords 2, 3 and 4 give 4.11e-45, 3.64e-45, 3.52e-45 with |dw| equal to |F| (2.6e-45, 2.4e-45, 3.0e-45): the strong rows are solved and the remainder does not fall, so at this start the weak equations are not affine to the chord's accuracy (the premise of the chord, #528). The Newton steps that follow are the same crawl as in #603's chain (a = 0.111 at D 253.64, chain_nat's a = 0.0556, chain_ns's a = 0.0543): at every step the trial at lam 1 is refused (ratio 3.5e4 to 6e5) and lam 0.5 is accepted with the simplified correction / |dz| = **5.000e-01 to four digits**, max|F| and |dz| both halving (3.91e-45 -> 1.91e-48 over 11 steps, |dz| 6.4e-29 -> 3.1e-32): along the step F is affine (a half step removes half the correction, as a linear residual does) while the full step jumps by 1e-25. The halving ladder tries lam 1 and 0.5 and nothing between.

Builds: worktree `D:\choptuik-i674` at origin/main 58628d94, venv-i600 (the #600 build); `newton_od_toy.py`'s check and its planted control are the coordinator's (the Mac).

# I710-win: the full system's corrector stall past D 99, A/B with `--elim_switch 0` from #682's own states

Machine win (Surface Laptop 4, i7-1185G7, 32 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/710 (the coordinator's message `1794601719695-0` on the `choptuik-large-d` channel, and its comment "the cause to test", 2026-11-13 20:28 UTC; recommended by #682, raw `I682-win/` 0e9206ac, whose states `cont2/` and `cont3/` are the starts here). Worktree `choptuik-i710` at main 5249c432 (`anm_run.py --elim_switch` reaches the quad-double corrector's ElimQ), venv-t151 (Python 3.10; hpkernel from before #523, multidouble 0.1.0), quad-double, `OPENBLAS_NUM_THREADS=1`, BelowNormal, 4 threads. #682's runs used main d0cc0b2a, so run A0 is also the control that the newer anm_run reproduces them. Raw output to `I710-win/`.

## Plan, written before the runs: the coordinator's hypothesis, flags and acceptance (comment on #710), verbatim

Coordinator: the cause to test, and the commands, written before any run (2026-11-13).

**Hypothesis.** In every refused attempt of `I682-win/logs/cont3.log`, ElimQ skipped every projection (`'skipped': 13`, `u0q` 0), because the start's |F| (about 2e-35) lies below its switch of 1e-15. So the corrector runs unprojected Newton on the full system. Its first step leaves the horizon rows' second-order term (|F| 1e-24). Then λ = 1/2 is accepted at exactly half the residual, and the full step is refused. That is #700's signature, where the projection removed that term and two full steps converged. `anm_run.py --elim_switch 0` (main 5249c432) now reaches ElimQ too. With `--reseed_q 1` its projection is quad-double, so it does not hold points at the double-double floor.

**Flags** (#682's): `--kfreeze 13 --N 24 --eps 1e-14 --D_max 400 --corrector qd --tol_qd 1e-44 --qd_it 12 --jet_q 1 --pred_q 1 --reseed 2 --reseed_q 1 --save_pred 1 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --threads 4`

| run | start | step | switch | what it tests |
|---|---|---|---|---|
| A0 | `I682-win/cont3/anm_pin13_D99.7500.npz` | `--h_max 0.125 --a0 0.125 --steps 1` | default | control: reproduces cont3's refusal (qn 0 2.08e-35 → 1.06e-24, λ 0.5, then no trial accepted) |
| A1 | the same | the same | `--elim_switch 0` | the a = 1/8 attempt converges |
| B0 | `I682-win/cont3/anm_pin13_D99.9531.npz` | `--h_max 0.09765625 --a0 0.09765625 --steps 1` | default | control: the second refusal |
| B1 | the same | the same | `--elim_switch 0` | that attempt converges |
| C | `I682-win/cont2/anm_pin13_D99.6250.npz` | `--h_max 1.0 --a0 0.5 --steps 6` | `--elim_switch 0` | the a the full system takes past D 100 |

**Acceptance** (each can fail):
- A0 and B0 reproduce cont3's refused attempts, with the same qn lines to 3 digits;
- A1 and B1 converge to qd max|F| ≤ 1e-44 within 8 steps, with `u0q` > 0 and `skipped` 0 in their projection counts;
- A1's Δ at D 99.875 matches cont3's `anm_pin13_D99.8750.npz` (reached by two steps of 1/16) to 1e-30, and B1's Δ matches cont3's state at D 100.0508 the same way;
- C: the a of each accepted step is reported, with every refusal.

If A1 still stalls, the hypothesis is refuted. Report the qn lines and stop. This replaces the issue's displaced-prediction control: matching Δ at the same D along a different path is the check that can fail.

## Choices fixed here, 2026-11-13 20:30 UTC, before any run (win)

1. **Order and gate.** `run_710.py A0 A1 B0 B1 C`, one at a time, 4 threads, BelowNormal, one BLAS thread. After A1 the driver stops if A1's first attempt (the block after its first re-seed line) is not "converged" in at most 8 quad-double steps with max|F| at most 1e-44, which the issue calls a refuted hypothesis; B0, B1 and C then do not run, and the qn lines of A0 and A1 are reported.
2. **"Reproduces to 3 digits"** (A0, B0): the numbers of every `qn k [full]` line of the first attempt (|F| before and after, |dz| before and after, lam) and the "no trial step accepted" line are equal, as printed (3 significant digits), to those of the corresponding attempt of `I682-win/logs/cont3.log`: A0 against its step 1's first attempt (a 0.125 from D 99.75), B0 against step 4's first attempt (a 0.0977 from D 99.953125). The pivot ranges and the timings are not compared. `table_710.py` does it and its selftest must fail on a planted change of one digit.
3. **"Converges within 8 steps"** (A1, B1): the first attempt's corrector says converged, with at most 8 quad-double steps and qd max|F| at most 1e-44, and its `elim projections` line has `u0q` > 0 and `skipped` 0.
4. **Delta checks** (A1, B1): Delta of an accepted state is the sum of the last entry of each of the four parts in arb at 400 bits. A1's state at D 99.875 against `I682-win/cont3/anm_pin13_D99.8750.npz`, B1's at D 100.05078125 against `cont3/anm_pin13_D100.0508.npz`, bar 1e-30. If A1 or B1's first attempt is refused and a later (smaller) attempt is accepted, the Delta check is made on the state at its own D only if a cont3 state exists there, and is otherwise reported as not made.
5. **C**: every attempt's a, D and outcome from the record and the log, accepted and refused.
6. **Not done**: the issue's displaced-prediction control (replaced by the Delta match, as the coordinator says), any change of flags beyond `--elim_switch 0`, and any run beyond the five.

## Run record

`run_710.py A0 A1 B0 B1 C` in one driver (`logs/run_710.log`), 4 threads, BelowNormal, one BLAS thread, all exit 0, the gate after A1 did not fire:

| run | start | step | switch | wall |
|---|---|---|---|---|
| A0 | cont3 D 99.75 | a 0.125, 1 step | default | 318 s |
| A1 | cont3 D 99.75 | a 0.125, 1 step | `--elim_switch 0` | 219 s |
| B0 | cont3 D 99.953125 | a 0.09765625, 1 step | default | 340 s |
| B1 | cont3 D 99.953125 | a 0.09765625, 1 step | `--elim_switch 0` | 231 s |
| C | cont2 D 99.625 | a0 0.5, h_max 1.0, 6 steps | `--elim_switch 0` | 1397 s |

20:30:29 UTC to 21:12:13 UTC. `table_710.txt` is the output of `table_710.py` (its selftest passes: an attempt equals itself, a changed digit in a qn line or in the tail differs, a different attempt differs).

## Results

**1. A0 and B0 reproduce cont3's refusals to the printed digits (README choice 2): yes, both.** A0's first attempt (a 0.125, D 99.875): qn 0 |F| 2.08e-35 to 1.06e-24 (|dz| 3.6e-24, lam 1), qn 1 1.06e-24 to 5.29e-25 (|dz| 7.6e-25, lam 0.5), "no trial step accepted" at qn 2 (|F| 5.29e-25, |dz| 7.6e-25), elim counts `skipped` 13, `u0q` 0. B0's (a 0.0977, D 100.05078125): 2.93e-35 to 2.78e-24 (lam 1), 2.78e-24 to 1.39e-24 (lam 0.5), no trial at qn 2 (1.39e-24, 4.4e-24), `skipped` 13. Both are the lines of `I682-win/logs/cont3.log`, so main 5249c432 reproduces #682's d0cc0b2a here. After each refusal anm_run halved and accepted (A0: a 0.0625 to D 99.8125, 3 steps, 4.4e-45; B0: a 0.0488 to D 100.001953125, 6 steps, 4.2e-49).

**2. A1 and B1 converge to 1e-44 within 8 steps with `u0q` > 0 and `skipped` 0 (choice 3): yes, both, at the first attempt, no halving.**

| run | a | D | qn 0 |F| (start to after the full step) | qn 1 | steps | final qd max abs F | elim counts |
|---|---|---|---|---|---|---|---|
| A0 (default) | 0.125 | 99.875 | 2.08e-35 to 1.06e-24 | 1.06e-24 to 5.29e-25 (lam 0.5), then no trial | 3, refused | 5.3e-25 | `u0q` 0, `skipped` 13 |
| A1 (`--elim_switch 0`) | 0.125 | 99.875 | 2.08e-35 to 3.71e-31 | 3.71e-31 to 6.21e-49 (lam 1) | 3 | 6.2e-49 | `u0q` 3, `skipped` 0 |
| B0 (default) | 0.0977 | 100.05078125 | 2.93e-35 to 2.78e-24 | 2.78e-24 to 1.39e-24 (lam 0.5), then no trial | 3, refused | 1.4e-24 | `u0q` 0, `skipped` 13 |
| B1 (`--elim_switch 0`) | 0.0977 | 100.05078125 | 2.93e-35 to 9.06e-31 | 9.06e-31 to 5.04e-49 (lam 1) | 3 | 5.0e-49 | `u0q` 3, `skipped` 0 |

The residual after the first full step falls to 3.5e-7 (A) and 3.3e-7 (B) of its unprojected value with the projection. Without it, the post-step |F| scales as a squared on the same base: 2.59e-25 at a = 1/16 against 1.06e-24 at 1/8 (ratio 4.1, from A0's second attempt and first), 6.76e-25 at a = 0.0488 against 2.78e-24 at 0.0977 (ratio 4.1, B0).

**3. Delta against cont3's state at the same D (choice 4, bar 1e-30): MISSED, both.**

| run | Delta (30 digits) | cont3's | abs diff |
|---|---|---|---|
| A1 at D 99.875 | 1.74515002816449925294435292335 | 1.74515002816449925294435289364 | 2.971e-26 |
| B1 at D 100.05078125 | 1.74497638097564202815972016295 | 1.74497638097564202815972006272 | 1.002e-25 |

Both differ from cont3's state by four to five orders more than the bar. This is a result of the pre-registered check and the bar is not moved here. What the states themselves show (read from the stored arrays, not a new run): the A1 state and cont3's D 99.875 state have the same leading double in 760 of 769 entries and differ by at most 1.97e-18 (median 3.0e-21, largest relative 7.5e-16), those of B1 and cont3's D 100.0508 in 766 of 769 and by at most 1.20e-18 (median 2.1e-21). A1 and cont3's D 99.875 state have qd max|F| 6.2e-49 and 3.9e-49, so two states 2.0e-18 apart satisfy the system to about 1e-48, which bounds the gain of its weakest direction by about 5e-31 (|F| / |dz|, in the linearization). B1 has 5.0e-49 and cont3's D 100.0508 state 8.1e-46, a bound of about 7e-28. At such gains |F| of 1e-48 to 1e-45 does not fix the root to 1e-30, so the bar of 1e-30 lies below what these |F| resolve. That reading is mine and untested; the issue's displaced-prediction control it replaced is not run.

**4. C (`--elim_switch 0` from D 99.625): six steps, none refused, each converged in 3 steps to 1e-47 or better.**

| step | from D | a | to D | qd max abs F | elim counts |
|---|---|---|---|---|---|
| 0 | 99.625 | 0.5 | 100.125 | 3.5e-49 | `u0q` 3, `skipped` 0 |
| 1 | 100.125 | 0.625 | 100.75 | 6.4e-49 | same |
| 2 | 100.75 | 0.78125 | 101.53125 | 9.6e-49 | same |
| 3 | 101.53125 | 0.9765625 | 102.5078125 | 9.9e-49 | same |
| 4 | 102.5078125 | 1.0 | 103.5078125 | 1.4e-48 | same |
| 5 | 103.5078125 | 1.0 | 104.5078125 | 5.7e-48 | same |

The a grows by anm_run's `--a_grow 1.25` from 0.5 and reaches the `h_max` of 1.0 at the fifth step, against 0.05 to 0.08 around D 100 with the default switch in #682. The post-first-step |F| rises with D and a, from 2.7e-30 (a 0.5, D 100.125) to 3.7e-26 (a 1.0, D 104.5078), four orders in six steps; I did not run past D 104.5.

## Verdict on the issue's acceptance

- the stall is attributed to one measured cause: **supported by the A/B**: the same attempts (same start, a and flags) converge in 3 steps with `--elim_switch 0` and stall without it, the stalls reproduce cont3's lines, and the counts show every refused attempt skipped all projections (`skipped` 13, `u0q` 0); the cause measured is the projection switch of 1e-15, which lies above the start's |F| of 1e-35, in line with #700;
- the change makes the a = 1/8 attempt converge to 1e-44: **yes** (6.2e-49, 3 steps);
- the replacement control (Delta at the same D along another path, bar 1e-30): **missed** (2.971e-26 and 1.002e-25).

## Recommended tasks (for the coordinator)

1. **Calibrate the Delta bar.** What: the a = 1/16 step from `I682-win/cont3/anm_pin13_D99.7500.npz` with `--elim_switch 0` (to D 99.8125), and Delta of its state against `cont3/anm_pin13_D99.8125.npz` (converged with the default switch), and the same a = 1/16 pair from D 99.8125 to 99.875 against `cont3/anm_pin13_D99.8750.npz`. Acceptance (can fail): the two |Delta differences| at a = 1/16 are below 1e-30 (then A1's 3e-26 belongs to the large step) or at the 1e-26 scale of A1 and B1 (then the bar was below what two converged roots resolve, and the weak direction sets it). Depends on #710. About 10 min.
2. **Continue the full system with `--elim_switch 0`.** What: `run_710.py C`'s command from `I710-win/C/anm_pin13_D104.5078.npz`, first one step of a = 0.4921875 (to D 105 exactly), then `--h_max 1.0 --steps 15` (to D 120). Acceptance: each step converges to 1e-44 or the stop rule (three refusals at one D) fires and its history is posted; Delta_full - Delta_held and its ratio to the err at each integer D from 105 to 120 (the held chain's states `T138-win2/chain/anm_pin3_D<D>.0000.npz` exist for D 100 to 121 at least, checked on the stage checkout). Depends on #710 and #682. About 1 h at 4 threads (3.9 min per step in C).

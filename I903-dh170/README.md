# I903-dh170: the fixed-order chain at horizon order 150 from D 200 toward the fold, on dh170

Machine dh170 (Fedora 45, i7-7700, 8 threads, 31 GB), issue https://github.com/nmoinvaz/choptuik-large-d/issues/903.
Command: the coordinator's of 2026-11-16 (`--ks 150`, 8 threads, nice 10, `--D_max 262`), launcher `run903.sh`, exits in
`exits_903.txt`. Nothing else runs on this machine.

Stage 1, `p150_200/` (`p150_200.log`): the base polish of T138's D 200 state (`T138-win2/chain_o/anm_pin3_D200.0000.npz`)
at order 150, `--steps 0 --save_base 1 --keep_plan 0`. The launcher's gate starts stage 2 only if its last octo-double
Newton line reads converged with max|F| <= 1e-60 (checked against dh610's p130 and p160 logs, and failing on a
not-converged line, on max|F| 1.8e-59 and on a log with no such line).

Stage 2, `chain_k150/` (`chain_k150.log`): the chain from `p150_200/base_pin3_D200.0000.npz` with `--keep_plan 1
--steps 400`.

Code: Python and `hp/data` from a worktree of main at 7f88c5bb (`hp/` is unchanged since 5897ee28); hpkernel from the
checkout's venv, built and checked in #920 (it has `Solver.series_o`, so the series are formed one order at a time).
The reference rung is dh610's `I903-dh610/p130_200` (p130 at D 200 is 1.7e-12).

## Rung: order 150 against order 130 at D 200

`rungs_p150.md` (dh610's `rungs903.py` over `p130_200` and `p160_200` of `I903-dh610/` and this folder's `p150_200`).
p is the lowest pivot of the first octo-double Jacobian, two digits as the log prints it. Delta_130 is dh610's re-polish
of T138's D 200 state at order 130.

| rung | octo-double steps | final max\|F\| | p first Jacobian | ln(p_K/p_130) | Delta_K - Delta_130 |
|---|---|---|---|---|---|
| p130_200 (dh610) | 4 converged | 3.1e-76 | 1.7e-12 | 0.0 | 0.0 |
| p150_200 (dh170) | 8 converged | 6.6e-74 | 3.3e-09 | 7.571 | 8.39e-14 |
| p160_200 (dh610) | 8 converged | 1.8e-74 | 2.1e-08 | 9.422 | 9.04e-14 |

`p150_200` took 2332 s on dh170's 8 threads (the first full Newton step 1747 s, dh610's 480 s on 20 threads). Its
launcher gate passed and `chain_k150` started at 20:13:26 UTC.

### Discrepancy in the order-130 reference pivot (reported, not resolved)

Both pivots in the rung table have two digits, so ln(p150/p130) is good to about 0.03 at best. The order-130 pivot at
the same D 200 state is 1.7e-12 in dh610's `p130_200` (first Jacobian of the polish) and 2.3e-12 in T138's
`chain_o.log` (`step 29: D 200.0, pivots 2.3e-12..1.2e+28`, the base's series), a 35% difference, with the same largest
pivot 1.2e+28. At orders 150 and 160 the polish's first-Jacobian pivot and the chain's step 0 pivot agree to two digits
(3.3e-09 and 3.3e-09 here; 2.1e-08 and 2.1e-08 on dh610). So the rung is +7.571 against dh610's p130 and +7.27 against
T138's record. The chain's per-step ratios to T138's p_min (as in dh610's `pmin_k160.md`) use T138's record.

Decision (coordinator, 2026-11-16): dh610's `p130_200` is the reference, so the rung +7.571 stands. It was polished with
the same flags, code and plan as `p150_200` and `p160_200`, while T138's `chain_o` reached the state with its own
corrector, plan and flags of 2026-11-07, so its pivot is not like-for-like. The cause is not pursued.

## Stop rule for chain_k150 (coordinator, 2026-11-17)

Stop the chain, killing its process tree, when inside one attempt the octo-double Newton's accepted iterations have
lam <= 1/32 for 3 in a row, or when one attempt runs past 2 h. Every state and log is kept, the folder is pushed, and
the stop is posted on #903 with the last accepted D, the base p_min and Delta moved. Reason: dh610's order-160 chain
crawled at lam 1/128 near D 234 (its `exits_903.txt`).

`watchdog903.py` implements it over `chain_k150.log` (started 06:14 UTC, events in `watchdog.log`, a stop adds a line
to `exits_903.txt`). Its checks: `--selftest` (nine synthetic cases, three of which must trigger), `--selftest
--mutate` (lam threshold 1e-9, must fail and does, exit 1), `--replay` of `chain_k150.log` (0 triggers, 8 refused
trials inside iterations included) and of dh610's `chain_k160.log` (0 triggers with n 3, since its pushed log has one
crawling iteration, line 603 at lam 0.0078125, which `--n 1` finds). The 3-in-a-row detection is therefore tested on
synthetic cases only. The 2 h timer starts at an attempt's `re-seeded` line, so it does not time the series.

## Stopped (coordinator, 2026-11-17 11:23:43 UTC)

`chain_k150` was stopped by hand on the coordinator's order (SIGTERM to its process, exit 143, wall 54617 s = 15 h 10 min,
no child processes), since where order 150 stalls is known and the crawl past D 233.125 costs about 120 h. The watchdog
was stopped after it. Last accepted D 233.125 (33 full steps and one of 0.125). The base at D 233.125 has no series record
(`step 34` was never written, the kill came during its series); its state is `chain_k150/anm_pin3_D233.1250.npz`. The
lowest pivot of the Jacobian of the a 0.125 attempt, at its start point (the prediction at D 233.125), was 4.1e-22; the
D 233.0 base's p_min is 6.3e-22.

Steps past D 228 (`chain_k150.log`; "od steps" are octo-double Newton iterations, the time is the attempt's):

| attempt | a | od steps | result | time | Delta moved |
|---|---|---|---|---|---|
| to D 229 | 1.000 | 4 | accepted | 1323 s | 2.7e-19 |
| to D 230 | 1.000 | 5 | accepted | 1217 s | 4.7e-18 |
| to D 231 | 1.000 | 9 | accepted | 2241 s | 1.4e-17 |
| to D 232 | 1.000 | 8 | accepted | 1331 s | 2.2e-16 |
| to D 233 | 1.000 | 15 | accepted (9 refused trials, 7 failed projections) | 3719 s | 1.2e-15 |
| to D 234 | 1.000 | 0 | start projection failed, attempt stopped | 107 s | 0 |
| to D 233.5 | 0.5 | 3 | stalled (lam <= 0.04 twice), lam 0.0625, 0.03125, 0.03125 | 3223 s | 6.3e-16 |
| to D 233.25 | 0.25 | 2 | stalled (lam <= 0.04 twice), lam 1/256 twice | 3708 s | 4.8e-16 |
| to D 233.125 | 0.125 | 16 | accepted (11 refused trials, 9 failed projections) | 4470 s | 1.4e-15 |

Bases (`step N` records): D 229 p_min 9.5e-17, D 230 3.6e-18, D 231 2.1e-19 (|z_N| 1.8e-29, a_max 3.111), D 232 1.5e-20,
D 233 6.3e-22 (|z_N| 2.05e-27, a_max 2.531). Kept for #937: the base `anm_pin3_D233.0000.npz` with its series
`jet_pin3_D233.0000.npz`, the predictions `pred_pin3_D234.0000`, `D233.5000`, `D233.2500`, `D233.1250`, and
`anm_pin3_D233.1250.npz`. `watchdog.log` holds the watchdog's events (it never fired).

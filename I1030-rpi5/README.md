# I1030-rpi5: P6 route 3's certificates (#990's remainder bound, #1015's head) reproduced on aarch64

Machine: rpi5 (Raspberry Pi 5, aarch64, 4 cores, 8 GB, Linux 6.17.0-1021-raspi), agent claude-me2. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1030 (follows #990, #1015; as #1024 did for P2). Task named by the coordinator by message, 2026-11-19.

Code: main 82f87a33 (contains 4a056a28, the commit the issue names), worktree `~/Source/choptuik-large-d-964`, `solver/proof/`. Python 3.13.7 (venv-choptuik), python-flint 0.9.0, FLINT 3.6.0, mpmath 1.3.0, sympy 1.14.0, numpy 2.5.4, scipy 1.18.1. The Mac's runs used venv-314 (python-flint 0.9.0, FLINT 3.6.0, sympy 1.14.0 per notes/P6_route3.md §10.1). One process at a time, `nice -n 10`.

## Written down before the runs (the issue's pass criteria, verbatim)

- Each run's own verdict passes, and every control (`--mutate=...`) exits 1.
- `route3_bound.py --constants` prints C_(ν−2), C_ν, C_(ν+2) = 28.45, 56.87, 4.77×10⁶, and with `--J0=100` 1.60, 3.17, 3.63×10⁵, as quoted in §10.
- `route3_head.py`: every printed line equals I1015-mac's log of the same command (raw f30c95b0) with timings masked. Use or adapt `I1024-rpi5/compare1024.py`, and keep its control (a changed line must be reported).
- Any difference is reported with its size and left unfixed. Certified bounds built from upper bounds may differ in last digits between machines and still both pass (#111); say whether the conclusion is the same.

Decision it informs: agreement sends route 3's bound to its independent review with two machines' runs behind it; a control that passes, or a bound that fails on aarch64, reopens the certificate before any review.

## Runs (`run1030.sh`, the commands of notes/P6_route3.md §10.6 and §11.6, from `solver/proof/`)

Each log ends with a line `exit N` (as I1015-mac's); `logs/times.txt` has each run's wall seconds. The expected exit is 0 for the verdict runs and 1 for the five controls (plant and psi of the bound, demix of the tuned run, plant and gsmall of the head).

| log | command | expected exit |
|---|---|---|
| route3_bound_lemmas | `route3_bound.py --lemmas` | 0 |
| route3_bound_constants | `route3_bound.py --constants` | 0 |
| route3_bound_constants_J0100 | `route3_bound.py --constants --J0=100` | 0 |
| route3_bound_check | `route3_bound.py --check` | 0 |
| route3_bound_check_plant | `route3_bound.py --check --mutate=plant` | 1 |
| route3_bound_check_psi | `route3_bound.py --check --mutate=psi` | 1 |
| route3_tuned_7_800 | `route3_tuned.py 7 800` | 0 |
| route3_tuned_7_800_demix | `route3_tuned.py 7 800 --mutate=demix` | 1 |
| route3_head_scope | `route3_head.py --scope` | 0 |
| route3_head_lemmas | `route3_head.py --lemmas` | 0 |
| route3_head_check | `route3_head.py --check` | 0 |
| route3_head_check_plant | `route3_head.py --check --mutate=plant` | 1 |
| route3_head_check_gsmall | `route3_head.py --check --mutate=gsmall` | 1 |
| route3_head_certify | `route3_head.py --certify` | 0 |

Estimate: 55 min on the Mac by §10-11's times, so about 3 h here (a guess).

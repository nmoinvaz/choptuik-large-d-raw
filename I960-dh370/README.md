# I960-dh370: kernel pilots of anm_run.py --a_rule reseed at leg 7's states (D 229.0509 and 230.5643)

Machine dh370 (Fedora 45, i7-8700, 12 threads, 31 GB, 8 GB zram swap), 10 threads at nice 10. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/960

## Build

Worktree `~/Source/choptuik-large-d-957` at PR #956's 954eadcb (holds #950's `--a_rule` and `step_rule_check.py`), its own `.venv`
(Python 3.14.10, hpkernel from `.venv/lib/python3.14/site-packages/hpkernel`, multidouble 4.8.2 crate, Python package 482c6835). Not main's
checkout: main has #953's kernel changes this build lacks. `build960.txt` logs `hpkernel.__file__` at the start.

## Inputs

`L = I903-win2/ks_chain/leg07_D222.0000_ks240` of this repository (`jet_pin3_D229.0509.npz`, `jet_pin3_D230.5643.npz`,
`anm_pin3_D229.0509.npz`, `anm_pin3_D230.5643.npz`, all on origin).

## Files

`run960.sh` runs the stages in the issue's order (`p0`, `p1`, `p2`, then `bits` if time allows), `exits_960.txt` holds each stage's exit,
`mem960.log` the memory and cpu samples (a watcher that only logs and alerts), one log and one jsonl per stage.

## Results (2026-11-18, all stages exit 0, no Traceback, no memory alert)

| stage | result |
|---|---|
| P0a, D 229.0509, N 24 | a 0.70 and the rule's 0.7387 re-seed, 0.9313 and 1.0 fail (the control): pass (`p0a.log`) |
| P0b, D 230.5643, N 24 | 0.66, 0.70 and the rule's 0.7257 re-seed, the logged 0.7276 refusal reproduces at level 0.0763: pass (`p0b.log`) |
| P1, one N 31 step with `--a_rule reseed` | a 1.2899 accepted on the first attempt, rule level 0.0715, re-seed ok in 23 its (`p1.log`, `n31/`) |
| P2, N 31 re-seeds | a 0.75, 1.0, 1.15, 1.25 and the rule's 1.2899 re-seed, 1.4 (level 1.02) fails: pass (`p2.log`, `pilot_n31.jsonl`) |
| bits pair | every numeric array of the state, the series and both predictions bit-identical; the series' meta differs in `t_coef` only, the jsonl records in the key `base_lu` only (`bits_cmp.log`, exit 1 as written, see the issue's closing comment) |

`bits_anm_run_main/` ran `anm_run_main.py` (origin/main 045a54c3's `anm_run.py`, sha1 c30de8b31040), which printed "base_lu_o: this hpkernel has no
Solver.olu_pivots_at" and formed the series base's octo-double LU, `bits_anm_run/` the build's `anm_run.py` (954eadcb, sha1 d71067ab474e).
`bits_cmp960.py --selftest` plants a one-ulp change and a changed record value, both must be reported.

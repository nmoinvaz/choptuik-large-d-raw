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

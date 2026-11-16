# I898-dh610: the octo-double series' jets at lane counts 8, 12, ..., 32, their bits and time

Machine dh610 (Fedora 45, i7-12700). Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/898

Branch `hp/jet-lanes` at ed6a0523 in the worktree `choptuik-large-d-898` with its own venv. Scripts, written by the
coordinator, run in order: `build.sh` (worktree, venv, `hp/build.sh`; `build.log`), `tests.sh` (hp's octo-double Rust
tests; `tests.log`), `check.sh` (`hp/jet_lanes_check.py` on #608's stored series at D 253.338 and its control;
`check.log`, `control.log`, `lanes.jsonl`, `lanes_mutate1.jsonl`). Each script ends with an "exit N" line.

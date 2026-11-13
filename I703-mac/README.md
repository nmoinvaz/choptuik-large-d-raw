# I703-mac: #667's two-set plants and #684's far-end plants with the zero factor at the real zero (#703)

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/703

Code: `solver/inner_amp/pade_second_zero.py` (branch `wip/i703-subagent` of nmoinvaz/choptuik-large-d), criteria frozen
at 47a37bfa in `FROZEN` and `notes/PADE_FAR_END.md` §15.2. The zero is #702's located zero (`I702-mac/real.json`).

- `selftest*.log`: the selftest and its mutation `gn`.
- `control.*`: R1–R5, J+ and J−; `control_mutate_{zero,bzero,judge}.*`: the controls' mutations.
- `far.*`: #684's K1 and far-end plants with the zero at ZLOC, and the statements S1–S3; `far_mutate_farend.*`.
- `grid.jsonl`: one record per plant and node; `grid.log`, `grid.json`: the run and its verdict, S4 and S5.

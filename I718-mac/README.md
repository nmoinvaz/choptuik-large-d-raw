# I718-mac: a ring of second-set positions, lengths and exponents near P0 + κ⋆, with the zero at ZLOC (#718)

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/718

Code: `solver/inner_amp/pade_second_zero.py` (#703's script, unchanged) and `solver/inner_amp/pade_second_ring.py`
(branch `wip/i718-subagent` of nmoinvaz/choptuik-large-d). The grid and the location rule are frozen in the ring
script's `FROZEN` and in `notes/PADE_FAR_END.md` §16 before the ring ran.

- `selftest*.log`: #703's selftest and its mutation `gn`.
- `control.*`: #703's R1–R5, J+ and J− rerun; `control_mutate_{zero,bzero,judge}.*`: their mutations.
- `far.*`, `far_mutate_farend.*`: #703's far stage and its mutation.
- `ring_selftest*.log`: the ring script's selftest (R7) and its mutations `secmom`, `len` and `window`.
- `pilot.*`: R6, R8, J+ and J− through the ring's path; `pilot_mutate_{len,window}.*`: their mutations.
- `ring.jsonl`: one `g` record per position, shape and α, and one record per plant and node; `ring.log`, `ring.json`,
  `ring.stdout`: the ring's run, its position verdicts and its location verdict.

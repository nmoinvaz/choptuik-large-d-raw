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

The ring's first run (started 20:37 UTC on 2026-11-13) was killed at 22:40 UTC with its session, after 17 of the 42
lattice positions. `ring.jsonl` ended on a complete line (2293 records, every line parses), so nothing was set aside,
and the ring was resumed at 22:44 UTC with the same command and code (7cadfcfd; its ring stage is a2a6deb6's,
unchanged), reading those records. The resumed run appends to `ring.log`, after a second `run` line, where it repeats
the 17 positions' lines from the stored records; `ring.stdout` is the first run's output and `ring_resume.stdout` the
resumed run's. `ring.json` is rewritten by the resumed run. `report.*` is the report stage (written after the freeze,
judges nothing).

The resumed ring finished the lattice at 02:57 UTC on 2026-11-14 with exit 0 (5967 plant records, 5392 of them at
ω∞; R8 and C1 pass). No lattice position is a candidate, so stage 2 ran no diagonal point. `report.log`,
`report.json` and `report.stdout` are the report stage's maps and counts, run right after.

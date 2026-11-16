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

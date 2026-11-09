# I254-mac: truncation of the centre and horizon series on the states of the high-M paths (gamma_dd --M48, M >= 48 on the large-D layout)

Machine: mac (Apple M5, 10 cores, 32 GB, macOS 27), shared with another session (#252, 2 processes).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/254
Code: branch wip/i254 of the code repository (worktree from main 09a5264), `hp/series_truncation.py`.
Versions: Python 3.14.7, numpy 2.5.4, mpmath 1.3.0; hpkernel 0.1.0 (the venv-314 build of 2026-11-08 16:24 PST).
All runs from the worktree root with /Users/nathan/venv-314/bin/python, nice 10, caffeinate -i, 1 thread, at most
2 processes.

## Files

- `scripts/`: the run scripts (`run_*.sh`), the inventory of every npz state of both repositories (`inventory.py`),
  the per-group state lists (`manifest.py`, written to `lists/`, duplicates by content in `lists/dups.txt`), and the
  table (`tabulate.py`).
- `logs/`: one log per run; `selftest.log` and `selftest_mutate_half.log` are the control (exit 0 and exit 1).
- `*.jsonl`: one record per state (hp/series_truncation.py); `table.csv` every state and layout.
- `states/`: the M 48 states re-converged as gamma_dd.py --M48 does (gamma_dd.py does not save them).

## Coverage

- Own M (no solve), every state in `lists/`: `modecount` (M >= 48 mode-count states of the raw folders, first node
  0.15 or 0.3), `gamma_own` (hp/data/states and hp/data/seeds, the states gamma_batch.py takes), `lowD_x002` (M >= 48
  with first node 0.01-0.02, low D), `large_d` (hp/data/large_d, M 32), `chains` (the chains delta_all.csv cites,
  T138-win2 chain and chain_o and I19-win2 crawl, and T73's pinned states; M 32, four parts read as double-double).
- `lowD_small` (first node below 0.01, M 48-384) was started and stopped after its first state (exit 143): the Taylor
  plan of an M 256 state takes more than 3 minutes, and these layouts are outside the issue's scope.
- Re-converged at M 48 as gamma_dd.py --M48 does: the four states of its records (D 20.04, 30.07, 40.02, 50.01).
- Separately: the M >= 48 runs on the large-D layout that did not save their states, re-converged as gamma_dd.py does
  on their layouts (review R2 at D 60; hp/data/large_d's checks at D 65.01 and m48_diag at D 67.72 with ks 200), and
  hp/resolution_check.py's states resampled to M 48 without a solve (`scripts/run_other_m48.sh`).

## The chains: the double-double measure does not apply

The chains (T138-win2, I19-win2, quad- and octo-double states, M 32) read as double-double give horizon truncations
that grow with D (below 1e-17 to D 150, 5.6e-10 at 169, 8.3e-5 at 186, divergent at 190 and from 214.6). That is the
double-double horizon series' rounding, not the chains' series: `logs/chain_od_residual.log` (scripts/chain_od_residual.py)
evaluates the same states' horizon block in double-double, quad-double and octo-double. At D 150 the m, a and c rows
are 3e-10 to 2e-9 in double-double and 7e-36 to 1e-31 in quad- and octo-double; at D 200 0.03 to 0.15 against 8e-35
to 2e-30. (The p rows' 1.3e-3 and 9.6e-4 are the held harmonics, which the pinned system replaces.) So
`sweep_chains.jsonl` is not a measurement of the chains' truncation above D ~ 150, and the kernel has no quad-double
series accessor to make one. The I19-win2 crawl's states (D 214.6 to 215.03) give |F| 2.6e23 in all three precisions on
the plain layout: that crawl ran with --reseed 2 and --od_junk 4 (its README), a different system, and is not measured.

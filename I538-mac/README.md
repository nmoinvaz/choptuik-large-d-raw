# I538-mac: the horizon series' radius in B = 1/a² and C = c a² for data off the solution (hp/pole_bc.py)

Machine: the Apple M5 Mac (a subagent of the coordinator), 2026-11-12. Issue:
https://github.com/nmoinvaz/choptuik-large-d/issues/538. Code: `hp/pole_bc.py` on branch `wip/i538-subagent` of the
code repository. The main and mutation runs used commit f825e80, and the `--ks` runs used 4923871, which only adds that
option. python-flint 0.9.0 with FLINT 3.6.0, at 256 bits.

The states are the nine of notes/QUAD_DOUBLE.md 13.6. These are `hp/data/states/up7_D40.0201`, `up7_D45.0507`,
`up8_D50.0075`, `up10_D55.0351` and `up13_D60.0020` of the code repository, and `T73/t73/pin7_D67.7422`,
`T84-mac/pin7_D70.5000`, `T75/pin7_D72.4000` and `T75/pin7_D73.2657` of this one. The tenth state is
`I461-win2/crawlJ/anm_pin3_D242.3642`, read as its top two parts. At each state a_h is scaled by 1 + δ, for δ = 0 and
1e-8 to 1e-2. The kernel's double-double horizon series is then computed in both horizon_alpha modes, and B, C and
b = a² are formed from its a and c series by series arithmetic.

- `planted.log`, `planted_mutate_b.log`: the estimator on planted series, `pole_bc.py planted` (exit 0) and
  `planted --mutate=b` (exit 1, the control firing).
- `pole_bc.jsonl`, `.log`: the ten states (exit 1, from controls 1 and 2's band at D 40.02). Each record holds one state
  and δ, with every variable's radius, its reliable orders K and window W, the estimator range, R136 (13.6's estimator)
  against route1-mac/pole_test.jsonl, and the where-test on the real axis. One record per state holds the fits.
- `pole_bc_mutate_b.jsonl`, `.log`: the same run with `--mutate=b`, where B := b (exit 1 at D 40.02 and 45.05).
- `pole_bc_ks130_D40_45.*`, `pole_bc_ks160_D40_45.*`: D 40.02 and 45.05 with the series carried to 130 and 160 orders
  (`--ks`), the diagnostic of the control failures (exit 0).
- `*_summary.log`: `pole_bc.py summary` on each jsonl (code commit 15b853e), giving the per-state fits and the
  where-test's ranges per δ that the issue quotes.

Commands, run from the code repository's hp/ with RAW pointing at this repository:

    python3 pole_bc.py planted [--mutate=b]
    python3 pole_bc.py RAW/I538-mac/pole_bc.jsonl data/states/up7_D40.0201.npz data/states/up7_D45.0507.npz \
      data/states/up8_D50.0075.npz data/states/up10_D55.0351.npz data/states/up13_D60.0020.npz \
      RAW/T73/t73/pin7_D67.7422.npz RAW/T84-mac/pin7_D70.5000.npz RAW/T75/pin7_D72.4000.npz \
      RAW/T75/pin7_D73.2657.npz RAW/I461-win2/crawlJ/anm_pin3_D242.3642.npz --threads 1 \
      --ref RAW/route1-mac/pole_test.jsonl [--mutate=b]
    python3 pole_bc.py RAW/I538-mac/pole_bc_ks130_D40_45.jsonl data/states/up7_D40.0201.npz \
      data/states/up7_D45.0507.npz --ks 130 --threads 1

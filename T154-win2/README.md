# T154-win2: the release step with 2 and 3 junk directions frozen, on the degree-6, 8 and 10 states at D 120 and 130

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at 79d3e84 (octo-double build;
Python only; no rebuild). venv-t126. 18 threads, below normal. Comms entry: 2026-11-07 17:18 UTC cloud to win2.

T148 part 2 found the release step's first-step dDelta is flat from junk 2 to 3 and inflates ~4-5x at junk 5/6, where
the frozen set takes in directions with sigma near 8e-21 that carry Delta content. With junk 2 or 3 the degree-6 pair at
D 100 comes closer to the planted difference than with junk 4. T154 repeats the junk-2 and junk-3 release at D 120 and
130, where the three fits differ more, to see whether the stable step stays fit-faithful.

12 runs, one at a time, each to release_<d6|d8|d10>_D<D>_j<w>.log:
  full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk <w> --it 1 --threads 18
  w = 2, 3;  D = 120, 130;  STATE = T140-win/chain_d6/anm_pin3_D<D>.0000.npz, T138-win2/chain/anm_pin3_D<D>.0000.npz,
  T140-win/chain_d10/anm_pin3_D<D>.0000.npz.
Each run is capped at 1 h (killed and skipped if it exceeds). Post once at the end with each run's final line.

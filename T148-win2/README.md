# T148-win2: the release step's response per held coefficient at D 100, and its dependence on the frozen junk

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at 79d3e84 (Python only past
ecf6f6c: release_planted.py's --part; no rebuild). venv-t126. 18 threads, below normal. Comms entry: 2026-11-07 15:21
UTC cloud to win2.

T147 found the junk-frozen step returns 97-99% of the degree-6/10 offsets, with a one-sign remainder (harmonic 5's
cosine alone came back to 1e-5). T148 isolates the remainder: per held coefficient (part 1) and by varying the number
of frozen junk directions (part 2). A ratio far from 1 is the result, not a stop.

Part 1 (per-coefficient response), each to planted_D100_<harm><a|b>.log (a = cos, b = sin), state
T138-win2/chain/anm_pin3_D100.0000.npz:
  release_planted.py <raw> <STATE> --harm <H> --part <cos|sin> --delta 1e-11 --octo 1 --junk 4 --it 1 --threads 18
  for (H, part) = (5,sin) (7,cos) (7,sin) (9,cos) (9,sin) (11,cos) (13,cos).
Part 2 (junk dependence), full_release.py with --junk 2,3,5,6 on each of the d6, d8 (chain_fit), d10 states, to
release_<d6|d8|d10>_D100_j<w>.log:
  full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk <w> --it 1 --threads 18
  STATE = T140-win/chain_d6/D100, T138-win2/chain/D100, T140-win/chain_d10/D100.
Stop a run after 1 h. Post after part 1 (each result line), after part 2 (each final line).

# T137-win2: the held-harmonic bias of Delta, by full_release.py

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at origin/main 579e403 (Python
only past 80d928f, the T126 octo-double build, no rebuild). venv-t126. 18 threads, below normal. Comms entry:
2026-11-07 00:18 UTC cloud to win2.

The goal changed from higher D to more digits of Delta. Past D 75 the digits are limited by the held harmonics' bias
(about 5e-8 at D 80 growing to ~3e-6 at D 200), not by how far the chain reaches. full_release.py measures that bias:
with the full system's Delta-free (junk) weak directions frozen, one octo-double Newton step from a pinned state moves
Delta by the bias (at D 79.77 it gives +5.03e-8, matching the full-system series +5.00e-8). The first step's dDelta is
the number that matters.

Per state, one after another, each to its own log:
  python -u full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk 4 --it 6 --threads 18
States:
  anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz   (check: first dDelta must be +5.0e-8)
  T110-win/chain/anm_pin3_D100.1184.npz
  T116-win2/chain/anm_pin3_D149.5559.npz
  T129-win2/chain4/anm_pin3_D200.2746.npz
  T129-win2/chain5/anm_pin3_D214.8840.npz
Post per state: the "od: N junk directions frozen (...)" line and each "on k:" line (|F|, |dz|, lam, dDelta). Stop a
state after 6 steps or 2 h. Logs release_D<D>.log.

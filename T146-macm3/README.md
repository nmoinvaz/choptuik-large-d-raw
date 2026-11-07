# T146-macm3: planted test of the release step, the re-solve by continuation

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), the T133 build (venv-macm3,
hpkernel NEON, multidouble 4.0.0), main 2d9eb711, whose hp/ code equals ecf6f6c's (only hp/data/*.csv differ; Python
only past 8f9dbfa, no rebuild). Comms entry: 2026-11-07 13:36 UTC cloud to win2, macm3 (T146).

From hp/ with venv-macm3, nice 10 under caffeinate -i, 6 threads, one run at a time, each to planted_D<D>_<n>.log
(planted_D<D>_<n>.cmd has the exact line; exits.txt how each ended):
  1. release_planted.py <raw> T138-win2/chain/anm_pin3_D80.0000.npz --delta 1e-10 --ls F --octo 1 --junk 4 --it 1 --threads 6
  2. release_planted.py <raw> T138-win2/chain/anm_pin3_D100.0000.npz --delta 3e-11,1e-10 --sub 1e-11 --octo 1 --junk 4 --it 1 --threads 6
A run stops after 3 h. Its first release (the state itself) must print the same first line, od line and on 0 line as
T141-win2/release_D<D>.log, apart from timings; the runner compares them when on 0 is out and stops the run if not.

Both runs ended with exit 0 and passed: run 1 (D 80, delta 1e-10) with ratio 0.9999998, run 2 (D 100, deltas 3e-11
and 1e-10, moves of 1e-11, 7 Newton steps each) with ratios 1.0000061 and 1.0000071. Each first release matched
T141-win2's. The "result" lines in the logs have every number.

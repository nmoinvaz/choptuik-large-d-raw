# T148-macm3: the release step's response per held coefficient at D 100, and its dependence on the frozen junk

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), the T133 build (venv-macm3,
hpkernel NEON, multidouble 4.0.0), main 451b1b56, whose hp/ code equals 79d3e84's but for the added plot_error_methods.py and
two SVGs (Python only past ecf6f6c, no
rebuild). Comms entries: 2026-11-07 15:21 UTC cloud to win2, macm3 (T148, queued for win2), 15:24 UTC cloud to win2
(part 1 adds 11 and 13's sines), 15:44 UTC cloud to win2, macm3 (macm3 takes T148 after T149, --threads 6, skipping
what win2 posted). win2 posted part 1's 5b, 7a, 7b, 9a, 9b, 11a and 13a at 15:49 UTC (T148-win2/), so they are not
rerun here.

From hp/ with venv-macm3, nice 10 under caffeinate -i, 6 threads, one run at a time, in this order; each run's .cmd file
has the exact line, exits.txt how it ended; a run stops after 2 h.
 Part 1, to planted_D100_<harm><a|b>.log (a the cosine, b the sine), for (H, part) = (11, sin), (13, sin):
   release_planted.py <raw> T138-win2/chain/anm_pin3_D100.0000.npz --harm <H> --part <cos|sin> --delta 1e-11 --octo 1 --junk 4 --it 1 --threads 6
 Part 2, to release_<d6|d8|d10>_D100_j<w>.log, for each state and then --junk 2, 3, 5, 6:
   full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk <w> --it 1 --threads 6
   STATE: T140-win/chain_d6/anm_pin3_D100.0000.npz (d6), T138-win2/chain/anm_pin3_D100.0000.npz (d8),
   T140-win/chain_d10/anm_pin3_D100.0000.npz (d10)
In part 1 each run's first release is compared with T141-win2/release_D100.0000.log's first, od and on 0 lines apart
from timings, and exits.txt says whether they match.

Part 2 was not run here: the 16:37 UTC entry moved it to win2. Both part 1 runs ended with exit 1, the delta failing,
which is a result: 11b ratio 1.394 (bias -3.06e-17), 13b ratio 0.644 (bias +7.24e-18). Both first releases matched
T141-win2's. 11b's first release spent 1771.82 s on its on 0 step; the other three releases here took 442-450 s.

Sleep note (added 2026-11-08, from I125-macm3/pmset_sleep.log): the Mac was asleep during parts of some runs, so wall times
in this folder overstate compute time where it says so below. caffeinate -i did not prevent these sleeps ("Maintenance
Sleep", "Dark Wake Thermal Emergency", and once a clamshell sleep).
  11b: wall 2770 s, asleep 1680 s, awake 1090 s, so its 1771.82 s on 0 step was mostly sleep. 13b: no sleep, 1161 s awake.

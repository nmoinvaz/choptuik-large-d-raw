# T149-macm3: the release step's response per held coefficient at D 80

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), the T133 build (venv-macm3,
hpkernel NEON, multidouble 4.0.0), main 0917e99e, whose hp/ code equals 79d3e84's (Python only past ecf6f6c, no
rebuild). Comms entry: 2026-11-07 15:21 UTC cloud to win2, macm3 (T149).

From hp/ with venv-macm3, nice 10 under caffeinate -i, 6 threads, one run at a time, in this order, each to
planted_D80_<harm><a|b>.log (a the cosine, b the sine; planted_D80_<harm><a|b>.cmd has the exact line; exits.txt how
each ended):
  release_planted.py <raw> T138-win2/chain/anm_pin3_D80.0000.npz --harm <H> --part <cos|sin> --delta 1e-11 --octo 1 --junk 4 --it 1 --threads 6
  for (H, part) = (5, sin), (7, sin), (7, cos).
A run stops after 2 h. Each run's first release (the state itself) is compared with T141-win2/release_D80.0000.log's
first, od and on 0 lines apart from timings, and exits.txt says whether they match.

All three runs ended with exit 0 and passed: 5b ratio 1.0000001, 7b 1.0000048, 7a 0.99991. Each first release matched
T141-win2's, and every release, of the state and of the three moved ones, ends at the same Delta, 1.7695679142833771.
Run 1 took 1553 s, 21 min of it before its first release's on 0 line; runs 2 and 3 took 440 s and 460 s, about 3 min
to that line, with the same code and state. No cache file was written, and the cause is not known.

Sleep note (added 2026-11-08, from I125-macm3/pmset_sleep.log): the Mac was asleep during parts of some runs, so wall times
in this folder overstate compute time where it says so below. caffeinate -i did not prevent these sleeps ("Maintenance
Sleep", "Dark Wake Thermal Emergency", and once a clamshell sleep).
  5b: wall 1553 s, asleep 1117 s, awake 436 s, against 440 s and 460 s awake for 7b and 7a, which did not sleep. This
  replaces "the cause is not known" above.

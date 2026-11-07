# T146-win2: planted test of the release step, the re-solve by continuation

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at ecf6f6c (Python only past
8f9dbfa: hp/release_planted.py fixed, new hp/release_steps.py; no rebuild). venv-t126. 18 threads, below normal. Comms
entry: 2026-11-07 13:36 UTC cloud to win2.

T144 showed the junk-frozen step returns the planted bias (ratio 1.00000) wherever the moved state re-solves, but the
re-solve stalled for larger delta / higher D. ecf6f6c fixes the re-solve: --sub makes the move in steps (each solved
from the last, continuation), --ls F the residual line search, --pin od the octo-double pinned solve. Only the first
step matters, so --it 1. A FAIL on a delta is a result.

Runs (one at a time, each to its own log; the first release of each must match T141/T143's first line, od, on 0 apart
from timings):
  1. planted_D150_1.log:  release_planted.py <raw> T138-win2/chain/anm_pin3_D150.0000.npz --delta 1e-11,3e-11,1e-10 --sub 1e-11 --octo 1 --junk 4 --it 1 --threads 18
  2. planted_D200_2.log:  release_planted.py <raw> T138-win2/chain_o/anm_pin3_D200.0000.npz --delta 1e-11,3e-11 --sub 1e-11 --pin od --octo 1 --junk 4 --it 1 --threads 18
  3. control_D200.log (must FAIL, exit 1): run 2 with --delta 1e-11 --mutate 1 in place of its --delta.
Post each run's result lines + last line, with cpu and memory. Stop a run after 3 h.

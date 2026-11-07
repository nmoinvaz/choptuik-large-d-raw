# T144-win2: planted test of the junk-frozen full-system step at small biases

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at 8f9dbfa (Python only past
31da699: hp/full_release.py factored into functions with its output unchanged, and the new hp/release_planted.py; no
rebuild). venv-t126. 18 threads, below normal. Comms entry: 2026-11-07 11:41 UTC cloud to win2.

release_planted.py solves a chain_fit state's pinned system again with held harmonic 5's cosine moved by delta (3e-9,
1e-9, 1e-10, 1e-11), which moves the pinned Delta by a known bias b, and checks that the step from the moved state adds
b less than the step from the state itself, within 2%. (Mac: quad-double D 80, delta 1e-9 passed with ratio 1.0002.)

Runs, one at a time, each to its own log:
  control (must FAIL, exit 1), control_D200.0000.log:
    release_planted.py <raw> T138-win2/chain_o/anm_pin3_D200.0000.npz --delta 1e-9 --mutate 1 --octo 1 --junk 4 --it 6 --threads 18
  real runs, planted_D<D>.log, for D 200, 100, 80 in order:
    release_planted.py <raw> <STATE> --octo 1 --junk 4 --it 6 --threads 18
    STATE = chain_o/anm_pin3_D200.0000.npz, chain/anm_pin3_D100.0000.npz, chain/anm_pin3_D80.0000.npz
Checks: in every log the first release (the state itself) must equal T141-win2/release_D<D>.log line for line (apart
from timings); if not, stop and post. The control must end FAIL (exit 1); if it passes, stop and post. A real run may
end FAIL on some deltas -- that is a result, not a stop; post as is. Stop a run after 2 h.

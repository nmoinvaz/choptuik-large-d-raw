# T147-win2: the junk-frozen step on T140's degree-6 and degree-10 states

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at ecf6f6c (same as T146, no
change; full_release.py). venv-t126. 18 threads, below normal. Comms entry: 2026-11-07 14:31 UTC cloud to win2.

A planted test with no re-solve. T140's chains are converged pinned states at the same D as chain_fit, with the
harmonics held on the degree-6 and degree-10 fits (instead of the 1/n fit of T138). The full system holds nothing, so
the junk-frozen step from a T140 state must differ from chain_fit's step at the same D by the known difference of the
pinned Deltas (1e-12 to 1e-11 here).

Per state, one at a time, each to release_<d6|d10>_D<D>.log:
  python -u full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk 4 --it 1 --threads 18
States, in order (all under T140-win/): chain_d6/D100, chain_d10/D100, chain_d6/D130, chain_d10/D130, chain_d6/D110,
chain_d10/D110, chain_d6/D120, chain_d10/D120 (anm_pin3_D*.npz). Stop a state after 1 h. Post once at the end with each
state's first line and final line.

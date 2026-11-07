# T145-win2: the junk-frozen full-system step on chain_fit states, T142's grid

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at 8f9dbfa (same as T144; no
checkout change; full_release.py output unchanged from T141/T143's build). venv-t126. 18 threads, below normal. Comms
entry: 2026-11-07 13:19 UTC cloud to win2.

win2 takes macm3's T142 grid (the even-D states) at its octo speed. With T141 (D 80/100/150/200/215) and T143 (the odd
5's), T145 fills D 90..209 so the full set covers every 5 in D. The first-step dDelta is the bias; T141/T143 showed it
is ~1e-14..3e-12 for chain_fit (bias removed). No control this run (T144's control on 8f9dbfa matched T141).

Per state, one at a time, each to release_D<D>.log:
  python -u full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk 4 --it 6 --threads 18
States, in order (all under T138-win2/): chain/anm_pin3_D{90,110,120,130,140,160,170}.0000.npz,
chain_o/anm_pin3_D{180,190,205,209}.0000.npz. Stop a state after 1 h. Post once at the end with each state's on 0 and
final line.

# T143-win2: the junk-frozen full-system step on chain_fit states, the D between T141's and T142's

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at origin/main 31da699 (same as
T141, no checkout change; full_release.py unchanged). venv-t126. 18 threads, below normal. Comms entry: 2026-11-07
11:19 UTC cloud to win2.

T141 (D 80/100/150/200/215) and macm3's T142 measure the held-harmonic bias of the bias-free (chain_fit) states with
T137's tool. T143 fills the D between them, so T141 + T142 + T143 cover every 5 in D. If the 1/n held fit is right, the
first-step dDelta is near zero (T141 gave +1.2e-14 at D 80 to -3.1e-12 at D 215, vs the pinned chain's +5e-8 to +3.4e-6).

Per state, one at a time, each to its own log release_D<D>.log:
  python -u full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk 4 --it 6 --threads 18
States, in order:
  anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz   (control; its log must equal T141's control apart from timings)
  T138-win2/chain/anm_pin3_D{85,95,105,115,125,135,145,155,165}.0000.npz
  T138-win2/chain_o/anm_pin3_D{175,185}.0000.npz, D195.5000, D212.5000
Stop a state after 6 steps or 1 h. Post every 3 states (first line, od, on 0, final line of each, cpu and memory).

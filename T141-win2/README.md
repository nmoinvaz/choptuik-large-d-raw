# T141-win2: does the 1/n held fit remove the bias? (full_release.py on T138's own states)

Machine: win2 (Intel Core Ultra 7 265K, 20 cores, AVX2). Worktree `..\choptuik-t126` at origin/main 31da699 (no
checkout change since T138; full_release.py unchanged since T137). venv-t126. 18 threads, below normal. Comms entry:
2026-11-07 08:20 UTC cloud to win2.

T137 measured the pinned chain's held-harmonic bias (first-step dDelta +5e-8 at D 80 to +3.4e-6 at D 215). T138 reran
the chain bias-free, holding the harmonics on a 1/n fit. T141 runs T137's tool (full_release.py, no fit, no series) on
T138's OWN states: if the fit's held values are right, the first-step dDelta is near zero (vs the pinned chain's large
bias).

Per state, one after another, each to its own log (release_D<D>.log):
  python -u full_release.py <raw> <STATE> --kfreeze 13 --octo 1 --junk 4 --it 6 --threads 18
States, in order:
  anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz   (control, T137 state 1; first-step dDelta must be +5.03e-8 +/- 2%)
  T138-win2/chain/anm_pin3_D80.0000.npz
  T138-win2/chain/anm_pin3_D100.0000.npz
  T138-win2/chain/anm_pin3_D150.0000.npz
  T138-win2/chain_o/anm_pin3_D200.0000.npz
  T138-win2/chain_o/anm_pin3_D215.0000.npz   (chain_o's last state; stopped at 2026-11-07 08:51 UTC, Delta
                                              1.69155955750601894)
Per state post the first line (pinned residual, Delta), the od: line, the on 0: line, and the final line (pinned -
series, released - series). Control first, then each state. Stop a state after 6 steps or 1 h.

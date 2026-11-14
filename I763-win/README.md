# I763-win: the joint and single effects of the last segment's two plan nodes on Delta at D 99.875

Machine win (surface-laptop-4, 8 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/763.

Scripts (written by the coordinator, from #754's):
- `make_763.py` writes `states/N1_05, N1_10, N2_05, N2_10, P_05, P_10.npz`, which are cont3's arrays with
  `segs[3][1]`, `segs[3][2]` or both moved by 0.5 or 1.0 times A1's shift. Its `--selftest` plants five wrong copies,
  which must be flagged.
- `run_754.py`'s copy `run_763.py` runs the octo-double base polish, with #754's flags, threads from `threads.txt`, and
  each job capped at 2400 s.
- `analyze_763.py` gives the effects against X2c's root, the cross term and the linearity.

Criteria, written before the run: (control) P_10, the plan of #754's LA, reproduces LA's Delta to 1e-40; the cross term
P − N1 − N2 is quoted with its ratio to P at both scales; a node's effect is linear in its shift when
|eff(0.5) / eff(1.0) − 0.5| ≤ 0.05. On the coordinator's copy of the states, P_10's two nodes equal LA's bit for bit.

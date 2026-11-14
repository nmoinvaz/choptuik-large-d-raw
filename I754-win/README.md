# I754-win: cont3's D 99.875 state polished with the last segment, or the rest, at A1's and X2's plan nodes

Machine win (surface-laptop-4, 8 threads), issue https://github.com/nmoinvaz/choptuik-large-d/issues/754.

Scripts (written by the coordinator):
- `make_754.py` writes `states/LA, CA, LX, CX, R_LX.npz`. These are cont3's arrays (A1's for R_LX) with only
  meta["segs"] changed. In L<P> segment 3's interior nodes are plan P's, and in C<P> those of segments 0 to 2 are.
  Its `--selftest` plants seven wrong copies, which must be flagged.
- `run_754.py` is #751's `run_751.py` with only the states and the log name changed. It is the octo-double base polish
  (`--steps 0 --elim_switch 0 --save_base 1`, kfreeze 13) from the worktree choptuik-i710 with venv-t151, its threads
  from `threads.txt`, and each job capped at 2400 s.
- `analyze_754.py` gives the effects against X2c's root and the criteria.

Criteria, written before the run: (1) L<P> reproduces P's offset (Delta of P's own state minus the root) to 10%;
(2) C<P> stays below 1e-30; (3) R_LX reproduces LX's Delta to 1e-40. The coordinator's dry run reproduced #727's
offsets, +2.9709e-26 (A1) and -1.6580e-25 (X2).

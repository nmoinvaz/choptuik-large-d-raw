# I1080-win2: an M = 5 start at #1080's second excited zero x2, by continuation in (A, w/w_inf), and its walk

Machine win2 (desktop-pc, Windows 11, 20 cores, 95 GB). Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1080.
Coordinator t5's order by hc, 2026-11-24 17:21 UTC. Runner: hc terminal t24.

## Code and environment

- Branch `wip/i1080-x2` (from feat/inner-mp 6b807830), worktree `D:\choptuik-i1080x2`; new script
  `solver/inner_stokes/start_path.py` (commit dd00111a). value_mp.py, zero_mp.py, inner_mp.py, hier.py, hier_nb.py
  unchanged from 6b807830.
- venv `C:\Users\nathan\source\venv-i962`: Python 3.14.10, numpy 2.5.4, scipy 1.18.1, mpmath 1.3.0 (backend
  python, no gmpy2), numba 0.68.1. One BLAS thread per process.

## Files

Written as the work goes; see the Status list.

## Status

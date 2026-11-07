# held-harmonics-mac: holding the chain's harmonics on a 1/n fit of the full-system states (notes/HELD_HARMONICS.md)

Machine: the Mac (Apple M5), 2026-11-06/07, a subagent of the coordinator session in its own worktree (branch
wip/held-harmonics, merged into main), quad-double and octo-double kernels, 2 threads, nice 10. chain_fit73/ and its log
are the chain held on the fit from T81's full-system state at 73.0 (8 quad-double steps to 79.83); chain_wrong5/ the
control (harmonic 5 1% wrong); sens_*.json the held-value sensitivities dDelta/dh per state (one LU each; the 200 row
from the octo-double LU); schur_*.log the Schur-complement study (its resolution check failed at harmonic 13, as the
notes record); series_*.txt and chain_fit73_vs_series.txt the comparisons with the full-system series; planted_*.txt
the planted-truth tests at 68.5-73. The scripts here are the scratch ones; the kept ones are hp/held_fit.py and
hp/held_schur.py.

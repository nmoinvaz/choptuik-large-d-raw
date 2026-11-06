# T136-mac: the held harmonics' bias at large D, measured by releasing them in octo-double

Machine: the Mac (Apple M5), run by the coordinator session, main's Python (full_release.py --octo 1) on the
octo-double kernel build, 3 threads, nice 10, under caffeinate -i. Why: above D 80 the chain's Delta lies below
arXiv:2611.07007's table by an amount that grows to 7.4e-6 at D 200 (hp/data/delta_published_compare.csv), the size
and sign of the held harmonics' bias measured at D 79-96 (notes/QUAD_DOUBLE.md 13.19). Releasing them measures it.

Order and criteria (fixed before the run):
1. Control, the chain's own system (--kfreeze 3) at 79.7657: residual at the floor, Delta moved by less than 1e-30.
2. Planted truth, the release (--kfreeze 13) at 79.7657 (anm-mac/run_trend_pin3_qd3): converged, and Delta within
   1e-9 of the 1/D series (degree 20, D <= 67.77), which lies 5.0e-8 above the chain there. The quad-double release
   stalled on a near-null direction (13.19). If this fails, the large-D runs below are not read.
3. The release at 100.1184 (T110-win/chain), 149.5559 (T116-win2/chain) and 200.2746 (T129-win2/chain4): the released
   minus the pinned Delta is the bias at that D.

  python3 full_release.py <raw> <state> --kfreeze 13 --octo 1 --it 10 --threads 3   (log release.log)

# I249-macm3: the crossing pair followed through D 56.01, 57.03, 58.01 and 59.03 at M 48, kf 23

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon rebuilt on 1bad14fd, modecount_cx for 3.14 with B = 5), main ae0efafd.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/249. Beside I231-macm3's D 61 M 40 count and its D 55.04 M 40 circles.

Per D (T = D56.0117, D57.0333, D58.0060, D59.0250; states up11_D56.0117, up12_D57.0333, up12_D58.0060, up12_D59.0250, M 32 native), run_count.sh T S [LAM] (caffeinate -is, nice 10, one thread, the four at once): hp/gamma_dd.py <raw>/I249-macm3/T/gamma.jsonl hp/data/states/S.npz
(skipped for D 58.0060: lam 2.045529761477777), then hp/modecount_wind.py hp/data/states/S.npz --M=48 --kf=23 --h0=0.6 --lam=<lam> --aLL=-0.096 --aL=0.124 --fmax=1e-15 --resolve=last --tag=T_M48_kf23 --data=<raw>/I249-macm3/T/data (#241's fixed left column).
No M 48 kf 23 state or cache for these D is in hp/data or --data at the start (hp_data_before.txt). Afterwards by hand, as in #238: hp/modecount_moment.py on each box that winds, then a circle (R 0.2 or less, n0 20) at the pair's position and a lam_phys control circle, on the saved kf 23 state loaded from hp/data.

Written before the run. Gates: gamma_dd's own gate (--fmax 1e-20; a skip is reported and that D is not counted), then setup |F| <= 1e-15 (a miss is a stop for that D, reported). Table: the 8 boxes at each D with both mismatch counts per edge.
The pair: located when a box (B0, B1a, B1b ...) winds +2 and its moment gives an upper-half zero, then confirmed by a circle winding +1 (a winding 0 widens the circle, 2 means two zeros; no tuning beyond that). If the moment tool refuses a winding such as 1.000002 as not an integer,
the circle is centred from a neighbouring box or D and that is said. The lam_phys circle (R 0.2) must wind +1 at each D, else that D's circles are not read. Re lambda of the pair against D is tabulated from 54.04 (-0.0220), 55.04 (+0.1996) (I238) to 59.03.
"Reaches the real axis": the pair's Im lambda from the circle is zero within the circle's own estimate (the estimate is not a bound), with the real-axis sign changes of the count (printed in each log: only (0.5, 1.0) and (2.0, 2.5) so far) gaining two extra sign changes as an independent indication.
Not located: zeros of other boxes unless a box that is nonzero needs it. Estimator ranges are not bounds.

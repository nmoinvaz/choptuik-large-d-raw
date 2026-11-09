# I240-macm3: D 54.04 counted at M 48, kf 23, inside the onset bracket (53.79, 55.04]

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main 25b50d1d. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/240. Beside I231-macm3's two M 40 counts.

Commands (gamma.cmd, count.cmd, caffeinate -is, nice 10, one thread): python3 hp/gamma_dd.py <raw>/I240-macm3/gamma.jsonl hp/data/states/up10_D54.0414.npz (lam_phys is not in hp/data/gamma_dd.jsonl, its default layout is
the kf 13 cut from D 35 on), then python3 hp/modecount_wind.py hp/data/states/up10_D54.0414.npz --M=48 --kf=23 --h0=0.6 --lam=<lam of the record> --fmax=1e-15 --resolve=last --tag=D54.0414_M48_kf23 --data=<raw>/I240-macm3/data.
The state is M 32 native, so setup resamples to M 48 and re-converges (as I232, I237). No D 54.04 kf 23 state or cache is in hp/data or --data (hp_data_before.txt).

Written before the run. Gate: gamma_dd's own residual gate (--fmax 1e-20; a skip is reported and the count is not run), then setup |F| <= 1e-15 (a miss is a stop, reported). Table: the 8 boxes with both mismatch counts per edge,
beside D 53.79 (all 0) and D 55.04 (B0 +2, U0 +1, U +1, full +2). Reading rule, fixed now: extras "present" when wind(g) is nonzero in any resolved box, "absent" when 0 in all; absent narrows the onset bracket to
(54.04, 55.04], present to (53.79, 54.04]; the boxes where they appear say whether they enter through the left column (B0, U0) as D 55's do. An unresolved edge is "not a count" and its boxes are not read.

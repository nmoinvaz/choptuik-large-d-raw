# I232-macm3: the D scan at M 48, kf 23 for the onset of the D 61 extra zeros (D 50.01 and D 55.04)

Machine: macm3 (Apple M3, 4 performance + 4 efficiency cores, 24 GB RAM, macOS 26.3.1), venv-macm3-314 (Python 3.14.3 from Homebrew, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx for 3.14),
main d28566c0. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/232 (its body says I230-macm3 by mistake, the coordinator's correction: I232). Two counts at once, one thread each, beside #220's short run.

Commands (D50/count.cmd and D55/count.cmd, caffeinate -is, nice 10, from the repository root): python3 hp/modecount_wind.py hp/data/states/up8_D50.0075.npz --M=48 --kf=23 --h0=0.6 --lam=2.051843756433441
--fmax=1e-15 --resolve=last --tag=D50.0075_M48_kf23 --data=<raw>/I232-macm3/D50/data, and hp/data/states/up10_D55.0351.npz with --lam=2.04768412771239, tag D55.0351_M48_kf23, --data=<raw>/I232-macm3/D55/data.
No D 50 or D 55 M 48 kf 23 state is in hp/data and both --data folders are empty at the start (hp_data_before.txt), so setup resamples/re-converges and every determinant is fresh.

Written before the run. Table: the 8 boxes at each D beside #211 (D 45: all 0) and #212 (D 61: B1b +6, B1c +2, B1 +8, U +8, full +24, I212-macm3). Gate: each setup's |F| <= 1e-15 (setup raises above --fmax: a stop for that D,
|F| reported, the state it saves moved out of hp/data). Both mismatch counts per edge (all passes and the last pass). Onset reading, fixed now: the extras are "absent" at a D when wind(g) is 0 in every resolved box,
"present" when any box is nonzero; the outcomes are absent at both, present at both, or present at D 55 only (the issue's list); anything else (present at D 50 only) is reported as it is. An unresolved edge is "not a count"
and its boxes are not read. A zero with Re lambda > 0 beyond the expected ones would be an extra growth rate: this task counts, it does not locate.

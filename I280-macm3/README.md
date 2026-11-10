# I280-macm3: the five D 61.03 M 48 circles at kf 27 (lam_phys, the row's three zeros from their kf 25 positions, the pair's disc at 3.0196)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main bfe5fd54 (origin/main d2a75f4 differs in no file of hp/ that these runs read).
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/280. Beside #271's script and I282, I285, I286.

Command (kf27/circles.cmd, caffeinate -is, nice 10, one thread): the issue's command as written. The seed is M 32 native, and no M 48 kf 27 state is
in hp/data at the start (hp_data_before_all.txt), so setup re-converges (resample, Newton, Levenberg-Marquardt) and the cache starts empty.

Written before the run. Stop: setup |F| above 1e-15, or the lam_phys circle (first) not winding +1 within 1e-5 of 2.043532530673; then report and stop.
Report: each winding and position as a kf 27 column of #244's table. Estimates are the circles' own ranges, not bounds.

## Results

Stopped under the stop rule (macm3, 2026-11-10 05:34:19 UTC, exit 143 from the kill). Setup passed (|F| 1.3e-19, series 1.0e-104 and 6.1e-38).
The lam_phys circle winds +1 with 0 mismatches and 0 alias bisections, zero 2.043502736 -0.000013053i, estimate 1.3e-05: 3.25e-05 from the kf 23
value 2.043532530673, outside 1e-5. The four other circles are not read; 12 determinants of the second circle are in the cache (42 lines).
The kf 27 state is in hp_data_after/ and hp/data is back without it.

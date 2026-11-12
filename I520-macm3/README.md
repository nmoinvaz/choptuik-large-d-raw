# I520-macm3: is the kf 27 zero's response to one ulp linear, and which entries of dh matter? (R 0.0075, kf 27, D 61.03, M 48)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118 (the hp build is the older one, no rebuild). Prepared 2026-11-11 22:39 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/520.

ulp_circle.py is #506's wrapper (I506-macm3/ulp_circle.py) with one change: the shift may be any integer from -4 to 4 (repeated np.nextafter), where #506's took -1, 0 and +1 (the issue asks for +2 ulps). Everything else is unchanged; the diff is the docstring, the assertion, the shift loop (for _ in range(abs(shift))) and the printed ulp count. Unit-checked on a synthetic matrix: shift +2 changes one entry by exactly 2 ulps, -1 by 1 ulp down, 0 nothing. Runs (run_520.sh, one after the other, 1 thread, nice 10, caffeinate -is, an empty cache each) at kf 27, circle 2.043532530673195,0,0.0075, --M=48 --n0=20 --fmax=1e-15: ulp_m1 (dh[10,11] -1 ulp), ulp_p2 (dh[10,11] +2 ulps), e3_8 (dh[3,8] +1 ulp), e30_31 (dh[30,31] +1 ulp). Reference (#506): plain 2.0435315123 - 7.6e-7i; dh[10,11] +1 ulp 2.0435449255 - 1.5e-11i, shift +1.343e-5.

Written before the run (the issue's). The -1 ulp shift is -1.34e-5 within 5%, and the +2 ulp shift is 2.7e-5 within 5%; otherwise the response is not linear. The other two entries' shifts and estimates are tabled.

## Results

Runs (run_520.sh, started 23:13:50 UTC on 2026-11-11, one after the other, an empty cache each; exits.txt): ulp_m1 exit 0 at 23:39:35, ulp_p2 at 00:05:24, e3_8 at 00:32:17, e30_31 at 01:00:33 UTC on 2026-11-12. Every circle: R 0.0075, kf 27, n0 20, winding +1, 28 points (+2 for beta), 0 verification mismatches, 0 alias bisections. Shifts are from the plain zero 2.0435315123 - 7.606e-7i (I506-macm3/kf27_plain).

| change | dh entry before -> after | zero | shift (Re) | miss from lambda_phys | estimate |
|---|---|---|---|---|---|
| dh[10,11] -1 ulp | 15.289788298678511 -> 15.28978829867851 | 2.0435564000 + 1.0e-11i | +2.489e-5 | 2.39e-5 | 1.1e-9 |
| dh[10,11] +1 ulp (I506) | -> 15.289788298678513 | 2.0435449255 - 1.5e-11i | +1.341e-5 | 1.24e-5 | 4.6e-11 |
| dh[10,11] +2 ulps | -> 15.289788298678515 | 2.0435377288 - 3.0e-12i | +6.217e-6 | 5.2e-6 | 1.1e-11 |
| dh[30,31] +1 ulp | 15.289788298678511 -> 15.289788298678513 | 2.0435548158 - 7.7e-12i | +2.330e-5 | 2.23e-5 | 7.2e-12 |
| dh[3,8] +1 ulp | 3.111005672737984 -> 3.1110056727379845 | 2.0479965696 + 3.2e-9i | +4.465e-3 | 4.46e-3 | 2.5e-5 |

Acceptance: the -1 ulp shift is +2.489e-5, not -1.34e-5 within 5%; the +2 ulp shift is +6.2e-6, not 2.7e-5 within 5%. Both fail: the response to an ulp of dh[10,11] is not linear, and not monotonic (-1, +1 and +2 ulps all move the zero up, by 2.5e-5, 1.3e-5 and 6.2e-6; the plain zero is below the three).
Entries: the same value and the same ulp in a different place, dh[30,31] against dh[10,11], moves the zero by 2.33e-5 against 1.34e-5; dh[3,8] (3.11) moves it by 4.465e-3, 330 times dh[10,11]'s, and its circle is the only rougher one (estimate 2.5e-5).
Reading (mine, not tested further): an ulp of one entry moves the kf 27 zero by 1e-5 to 4e-3 depending on the entry, in no simple order. An entry of the double-double matrix is held to about 1e-32 relative, 1e16 times smaller than an ulp of the high part. The response is not linear, so I cannot scale the shifts down to that size; it is unlikely, but not shown, that the matrix's own representation error is the source of the plain kf 27 miss of 1.27e-6 (350 times kf 22's).
Diff of ulp_circle.py against I506-macm3/ulp_circle.py: the docstring line on SHIFT (now "an integer from -4 to 4 ... by repeated np.nextafter"), the assertion (abs(shift) <= 4 for shift in (-1, 0, 1)), the shift step (a loop for _ in range(abs(shift)) of np.nextafter on the running value, where #506's did one nextafter on the old value), and the printed line (adds the ulp count). Nothing else.

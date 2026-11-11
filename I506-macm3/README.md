# I506-macm3: is the kf 27 control's noise the double-double matrix? One ulp in one entry at R 0.0075 (kf 27 and kf 22 states, D 61.03, M 48)

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, FLINT 3.6.0, hpkernel cp314 neon, modecount_cx with B = 5), main checkout at de63a118. Prepared 2026-11-11 20:49 UTC. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/506.

Method. `ulp_circle.py` (this folder) runs hp/modecount_circle.py unchanged after replacing the module attribute modecount_cx.CSolver by a function that hands the solver a copy of the double-double differentiation matrix with dh[10, 11] (15.29, the largest entry of the odd matrix) changed by one ulp (np.nextafter, high part only; the low part is as it is). `ulp_circle.py I J SHIFT -- <circle arguments>`; SHIFT 0 passes the matrix as it is. It changes no repository file. The hook was checked on a synthetic matrix: exactly one entry changes, by exactly one ulp. Runs (run_ulp.sh, one after the other, 1 thread, nice 10, caffeinate -is), each with an empty cache of its own (so every determinant is computed): kf27_ulp (kf 27, shift +1), kf27_plain (kf 27, shift 0, the control of the wrapper: it must reproduce #500's R 0.0075 n0 20 zero 2.043531512 - 7.606e-7i bit for bit), kf22_plain and kf22_ulp (the control state). The circle is 2.043532530673195,0,0.0075 with --M=48 --n0=20 --fmax=1e-15.

Written before the run (the issue's). If the zero at R 0.0075 moves by 5e-7 or more under the one-ulp change, the noise is the matrix's. If it moves by less than 1e-7, the noise is elsewhere. The same one-ulp change at the kf 22 state is the control.

## Results

Runs (run_ulp.sh, started 20:50:33 UTC, 2026-11-11, one after the other, an empty cache each; exits.txt): kf27_ulp exit 0 at 21:15:28, kf27_plain exit 0 at 21:40:41, kf22_plain exit 0 at 22:07:16, kf22_ulp exit 0 at 22:34:09. Every circle: R 0.0075 around lambda_phys 2.043532530673195, n0 20, winding +1, 28 points (+2 for beta), largest step 0.353, 0 verification mismatches, 0 alias bisections. dh[10,11] = 15.289788298678511 goes to 15.289788298678513 in the ulp runs (one entry changed; the plain runs print "shift +0, entries changed 0").

| run | zero | offset from lambda_phys (Re, Im) | miss | estimate (n0 against n0/2) |
|---|---|---|---|---|
| kf 27 plain | 2.0435315123 - 7.6058e-7i | (-1.018e-6, -7.606e-7) | 1.271e-6 | 1.9e-7 |
| kf 27 +1 ulp | 2.0435449255 - 1.5e-11i | (+1.239e-5, -1.5e-11) | 1.239e-5 | 4.6e-11 |
| kf 22 plain | 2.0435325298 + 3.4e-9i | (-9.1e-10, +3.4e-9) | 3.55e-9 | 1.7e-9 |
| kf 22 +1 ulp | 2.0435456117 + 6.0e-13i | (+1.308e-5, +6.0e-13) | 1.308e-5 | 1.8e-11 |

Wrapper control: kf27_plain (shift 0) reproduces #500's R 0.0075 n0 20 circle bit for bit: all 30 determinants equal in ln|det M| and arg (0 of 30 differ, largest difference 0.0), and the zero, its n0/2 value and the point count are identical to every bit.
Shift under +1 ulp: kf 27 1.343e-5 (Re 1.341e-5, Im 7.6e-7), kf 22 1.308e-5 (Re 1.308e-5, Im -3.4e-9); ratio 1.03. By the rule written before the run the kf 27 zero moves by 5e-7 or more (by 1.34e-5, 27 times), so "the noise is the matrix's". Reading (mine): the response is a smooth displacement, not scatter (the perturbed circles are smoother than the plain ones: estimates 4.6e-11 and 1.8e-11 against 1.9e-7 and 1.7e-9), and it is the same at kf 22 (1.31e-5) as at kf 27 (1.34e-5), so the zero's sensitivity to dh[10,11] is a property of the matrix and not of the state. The plain kf 27 miss (1.27e-6) is ten times smaller than one ulp's effect and 350 times the plain kf 22 miss, so the sensitivity to the matrix does not explain why kf 27 misses more than kf 22. An entry of the double-double matrix is held to about 1e-32 relative, a perturbation of 1e-16 is 1e16 times that; I did not test other entries, a -1 ulp change or 2 ulps.
What ulp_circle.py replaces: only the module attribute modecount_cx.CSolver, by a function that calls the original with a copy of the high part dh in which entry [10, 11] is moved by SHIFT ulps (np.nextafter); every other argument (low part dl, phase weights, nodes, segments, thread count) is passed on unchanged, and hp/modecount_circle.py is run unchanged with runpy. With SHIFT 0 it passes an equal copy (checked above). No repository file is changed.

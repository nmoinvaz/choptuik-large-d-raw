# I1098-mac-a/closed_form: integer-relation searches for the provisional Delta_inf of the 15-record fit

Coordinator (t5), Mac, 2026-11-27 19:47 UTC. Issue https://github.com/nmoinvaz/choptuik-large-d/issues/1098.
Value 1.643893745125357513722888 +- 6.3e-23 (I1098-mac-a/fit15, provisional: its leave-one-out check could not run).

- `closed_form.py` (mpmath 60 digits): PSLQ on [f(x), 1, basis] for 8 transforms f (x, x^2, 1/x, exp(x), log(x), x/pi,
  x pi, exp(x/2)) and 7 bases of classical constants (pi, pi^2, log 2, log 3, zeta(3), Euler's gamma, Catalan's G, e,
  sqrt 2, sqrt 3), tol 10 x bar relative, height bound 10^(P/n)/10 with P = 22.4 digits and n numbers.
- Controls (each must behave): `--planted` (x = (3 pi^2 - 7 log 2)/11 + 0.37 bar) recovers the relation, height 11, exit 0
  (`ctlplanted.log`); `--random` finds none, exit 0 (`ctlrandom.log`).
- Result (`real.log`): no relation in any of the 56 searches. Height bounds: about 4e4 (n 4), 3e3 (n 5), 160 (n 7).
  mpmath.identify at tol 1e-20: none. Nearest simple constant: zeta(2) = pi^2/6, which differs by -1.04e-3.
- `algebraic.py` (2026-11-27 19:55 UTC): PSLQ on [1, x, ..., x^d], d = 2..8, the same tol and height rule. Controls:
  `--planted` (the real root of 2x^3 - 3x^2 - 2x - 1 plus 0.37 bar) is recovered at d = 3, height 3 (`algplanted.log`);
  `--random` gives none (`algrandom.log`). Result (`alg.log`): no polynomial; heights ruled out up to 3e6 (d 2),
  4e4 (3), 3e3 (4), 544 (5), 159 (6), 63 (7), 30 (8).
- (2026-11-27 21:25 UTC) Both scripts reject a relation with fewer than two nonzero coefficients: at a2's 14 digits
  and |a2|^8 near 3e13, PSLQ returned [1, 0, ..., 0], which only says the constant term is below the precision.
  closed_form.py takes log|x| (a2 < 0). Rerun with both fixes (`coeffs/`; c_ the constants search, g_ the algebraic
  one; each with its planted and random controls, all exit 0): Delta_inf, and the Taylor coefficients a1 =
  10.37528562845395538737 (+-1.6e-17) and a2 = -49.168737490066284 (+-2.5e-13) of I1098-mac-a/singularities: no
  relation, no polynomial.

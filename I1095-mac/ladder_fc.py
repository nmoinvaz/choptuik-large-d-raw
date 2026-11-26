"""Feasibility scan (not a result): weighted least-squares polynomial fits in x = 1/(D-2) of degree K to the planted
truth (track_c.readme_formula) on direct ladders only, with Gaussian noise sigma; the fit's value at x = 0 against the
truth's limit. Ladders: D 1000-1e5 (11 points, today's plan) and D 1000-1e6 (13 points)."""
import random, sys
sys.argv = [sys.argv[0], "real"]
import mpmath as mp
import track_c as T
mp.mp.dps = 60
lim = T.readme_formula(mp.mpf("1e40"))
lad = [1000.0, 1414.0, 2000.0, 2828.4271247461903, 4000.0, 5656.854249492381, 8000.0, 10000.0, 20000.0, 50000.0, 1e5]
lad2 = lad + [3e5, 1e6]
rng = random.Random(3)
for name, L in (("1000-1e5", lad), ("1000-1e6", lad2)):
    for sg in (1e-13, 1e-16, 1e-21):
        best = []
        for K in range(1, min(9, len(L) - 2)):
            xs = [1 / (mp.mpf(d) - 2) for d in L]
            ys = [T.readme_formula(mp.mpf(d)) + mp.mpf(rng.gauss(0, sg)) for d in L]
            A = mp.matrix([[x ** k for k in range(K + 1)] for x in xs])
            c = mp.lu_solve(A.T * A, A.T * mp.matrix(ys))
            res = max(abs(sum(c[k] * x ** k for k in range(K + 1)) - y) for x, y in zip(xs, ys))
            best.append((K, float(abs(c[0] - lim)), float(res)))
        print(name, "sigma %.0e:" % sg, "; ".join("K %d err %.1e (max resid %.0e)" % b for b in best))

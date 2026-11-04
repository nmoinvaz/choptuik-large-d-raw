# Poles of the stored rational formula, its Taylor radius in e = 1/(D-2), and where its Taylor series fails.
import json, numpy as np
C = json.load(open('/Users/nathan/Source/choptuik-large-d/solver/data/formula_coefficients.json'))
a = np.array([float(v) for v in C['a']]); b = np.r_[1, [float(v) for v in C['b']]]
e_ = np.array([float(v) for v in C['e']]); f = np.r_[1, [float(v) for v in C['f']]]
for nm, P, Q in (('Delta', a, b), ('gamma', e_, f)):
    r = np.roots(Q[::-1]); print(nm, 'denominator roots in e:', r, ' D =', 2 + 1 / r, ' Taylor radius in e', abs(r).min(),
                                  ' -> Taylor series converges only for D >', 2 + 1 / abs(r).min())
    # Taylor coefficients of P/Q in e
    N = 30; t = np.zeros(N); Pp = np.r_[P, np.zeros(N)]
    for k in range(N):
        t[k] = Pp[k] - sum(Q[j] * t[k - j] for j in range(1, min(k, len(Q) - 1) + 1))
    print('  Taylor coeffs t0..t8', t[:9]); print('  ratios t_k/t_{k-1}, k=20..24', t[20:25] / t[19:24])
    rat = lambda x: np.polyval(P[::-1], x) / np.polyval(Q[::-1], x)
    for D in (4, 5, 6, 8, 10, 15, 20, 30):
        x = 1 / (D - 2); s = sum(t[k] * x ** k for k in range(N))
        print(f'  D={D}: formula {rat(x):.10f}  its Taylor series to e^29 {s:.6e}  diff {s - rat(x):.1e}')

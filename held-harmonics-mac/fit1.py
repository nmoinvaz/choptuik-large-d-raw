import json
import numpy as np
OUT = '/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/43f19197-40d3-4ad8-aa26-db5322fa8689/scratchpad/held_harmonics/'
A = np.load(OUT + 'harm_rows.npy')
meta = json.load(open(OUT + 'harm_rows.json'))
KS = list(range(1, 15, 2))
col = {}
for i, k in enumerate(KS):
    col[(k, 'a')] = 1 + 2 * i
    col[(k, 'b')] = 2 + 2 * i
grp = np.array([g for g, D, p in meta])
D = A[:, 0]
full = ((grp == 'dd_full') & (D >= 30)) | (grp == 'qd_full')
chain = grp == 'chain'
sens79 = {(5, 'a'): 9.1968e-03, (5, 'b'): 7.2503e-03, (7, 'a'): 1.5930e-04, (7, 'b'): -8.7862e-04, (9, 'a'): 9.0179e-06,
          (9, 'b'): 2.9683e-05, (11, 'a'): -6.1133e-06, (11, 'b'): -5.5206e-06, (13, 'a'): 7.0449e-07, (13, 'b'): 9.6647e-07}
sens73 = {(5, 'a'): 8.4896e-03, (5, 'b'): 7.1471e-03, (7, 'a'): 1.2375e-04, (7, 'b'): -8.5841e-04, (9, 'a'): 1.3535e-05,
          (9, 'b'): 3.7784e-05, (11, 'a'): -6.2676e-06, (11, 'b'): -6.6819e-06, (13, 'a'): 7.5636e-07, (13, 'b'): 1.1062e-06}


def fit_pred(Dfit, yfit, Dq, deg):
    n = Dfit - 2.0
    x = 1.0 / n
    y = np.sqrt(n) * yfit
    c = np.polynomial.chebyshev.Chebyshev.fit(x, y, deg)
    nq = Dq - 2.0
    return c(1.0 / nq) / np.sqrt(nq), np.max(np.abs(c(x) - y))


for deg in (4, 6, 8):
    # planted: fit on full points with D <= 71.0, predict 72.8 and 73.0
    for Dcut, Dq_list in ((71.0, (72.8, 73.0)), (73.0, None)):
        m = full & (D <= Dcut + 1e-9)
        tot = {}
        print(f'degree {deg}, fit on {m.sum()} full points D <= {Dcut}')
        targets = [(Dq, A[(grp == 'qd_full') & (np.abs(D - Dq) < 1e-6)][0]) for Dq in Dq_list] if Dq_list else \
            [(Dc, A[chain & (np.abs(D - Dc) < 1e-3)][0]) for Dc in (79.7657, 82.7188, 84.4688)]
        for Dq, row in targets:
            bias = 0.0
            parts = []
            for kk in (5, 7, 9, 11, 13):
                for ab in 'ab':
                    pred, res = fit_pred(D[m], A[m, col[(kk, ab)]], Dq, deg)
                    dh = row[col[(kk, ab)]] - pred
                    s = (sens73 if Dq_list else sens79)[(kk, ab)]
                    bias += s * dh
                    parts.append(f'{kk}{ab} {s*dh:+.1e}')
            print(f'   D {Dq}: sum s*(h_target - h_fit) = {bias:+.3e}   [' + ', '.join(parts) + ']')

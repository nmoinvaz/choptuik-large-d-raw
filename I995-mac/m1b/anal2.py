import json, sys, numpy as np
from collections import defaultdict
G = defaultdict(list)
for l in open(sys.argv[1]):
    r = json.loads(l); G[(r["A"], r["r1"])].append(r)
for (A, r1), rs in sorted(G.items()):
    rs.sort(key=lambda r: r["wf"])
    wf = np.array([r["wf"] for r in rs]); R = np.array([r["re"] + 1j * r["im"] for r in rs])
    mx = np.array([r["mx"] for r in rs])
    d = np.abs(np.diff(np.log(np.abs(R)))) + np.abs(np.angle(R[1:] / R[:-1]))
    sp = []
    for k in range(len(d)):
        nb = max(d[k - 1] if k > 0 else 0, d[k + 1] if k + 1 < len(d) else 0)
        if d[k] > 4 * nb and d[k] > 0.05:
            sp.append(k)
    # second difference of log R relative to first: smooth curves have |d2| << |d1|
    lr = np.log(R); lr = lr.real + 1j * np.unwrap(lr.imag)
    d2 = np.abs(np.diff(lr, 2)); d1 = np.abs(np.diff(lr))[:-1] + 1e-12
    bad = np.where(d2 > 0.5 * d1 + 0.02)[0]
    big = wf[mx > 1e2]
    print(f"A {A:.3f} r1 {r1}: n {len(rs)} spikes {len(sp)} " + ", ".join(f"{wf[k]:.3f}({d[k]:.2f},|Y|{mx[k]:.0e}/{mx[k+1]:.0e})" for k in sp[:6])
          + f" | d2-bad {len(bad)}" + (f" first {wf[bad[0]]:.3f}" if len(bad) else "")
          + (f" | max|Y|>1e2 from wf {big.min():.3f}" if len(big) else f" | max|Y| <= {mx.max():.0f}"))

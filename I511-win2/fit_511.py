#!/usr/bin/env python3
"""#511: the two-rate fit of the equilibrated ln sigma_1 against D, with a break at each candidate D.
usage: python fit_511.py LOG [LOG ...]       (near_null_eq.py logs; the D is the state file name's; sorted by D here)
       python fit_511.py --selftest          (a planted break must be found, a smooth curve must be called gradual)
Model for a break b: ln sigma_1(D) = c + s1 (D - b) for D <= b and c + s2 (D - b) for D >= b (continuous, 3 parameters for a given b; the rate is -s). Candidates b are the states' D with at least
two states on each side. Reading rule of #511, written before the run: if the best break leaves all residuals below 0.02 in ln sigma_1 and is best by a factor of 2 in the sum of squares over the second best
candidate, that D is the onset; otherwise the steepening is gradual. Also printed: the one-rate fit, the best b over a fine grid (0.05), the rates on both sides."""
import math, os, sys
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "I505-win2"))
from table_505 import parse  # noqa: E402

def fit_break(D, y, b):
    X = np.column_stack([np.ones_like(D), np.minimum(D - b, 0.0), np.maximum(D - b, 0.0)])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    r = y - X @ beta
    return beta, r

def analyse(D, y, out=print):
    n = len(D)
    one = np.polyfit(D, y, 1)
    r1 = y - np.polyval(one, D)
    out(f"one-rate fit: rate {-one[0]:.4f} per unit of D, sum of squares {np.sum(r1 ** 2):.4e}, max |residual| {np.max(np.abs(r1)):.4f}")
    rows = []
    for k in range(2, n - 2):
        b = D[k]
        beta, r = fit_break(D, y, b)
        rows.append((b, -beta[1], -beta[2], float(np.sum(r ** 2)), float(np.max(np.abs(r)))))
    out("| break D | rate below | rate above | sum of squares | max abs residual |")
    out("|---|---|---|---|---|")
    for b, s1, s2, ss, mx in rows:
        out(f"| {b:.4f} | {s1:.3f} | {s2:.3f} | {ss:.3e} | {mx:.4f} |")
    order = sorted(range(len(rows)), key=lambda i: rows[i][3])
    best, second = rows[order[0]], rows[order[1]]
    grid = np.arange(D[2], D[-3] + 1e-9, 0.05)
    gb = min(grid, key=lambda b: float(np.sum(fit_break(D, y, b)[1] ** 2)))
    gbeta, gr = fit_break(D, y, gb)
    out(f"best candidate break D {best[0]:.4f}: sum of squares {best[3]:.3e}, max |residual| {best[4]:.4f}, rates {best[1]:.3f} below and {best[2]:.3f} above; second best D {second[0]:.4f} ({second[3]:.3e}), ratio second / best {second[3] / best[3]:.2f}")
    out(f"best break on a 0.05 grid: D {gb:.2f}, sum of squares {np.sum(gr ** 2):.3e}, max |residual| {np.max(np.abs(gr)):.4f}, rates {-gbeta[1]:.3f} and {-gbeta[2]:.3f}")
    sharp = best[4] < 0.02 and second[3] / best[3] >= 2.0
    out(f"reading rule: max |residual| < 0.02: {'yes' if best[4] < 0.02 else 'NO'}; best by a factor 2 in the sum of squares: {'yes' if second[3] / best[3] >= 2.0 else 'NO'}; "
        + (f"=> the onset is D {best[0]:.4f}" if sharp else "=> the steepening is gradual (no sharp onset by the rule)"))
    return sharp, best

def selftest():
    D = np.array([216.1312, 220.1312, 224.1312, 228.1312, 229.1312, 230.1312, 231.1312, 232.1312, 232.6312, 233.1312, 234.1312, 235.1312, 236.1312, 237.1312, 239.5375, 241.1244, 242.3642])
    b0 = 232.1312
    y = -(np.where(D <= b0, 1.0 * (D - b0), 1.3 * (D - b0))) - 120.0
    sink = []
    sharp, best = analyse(D, y, out=sink.append)
    ok1 = sharp and abs(best[0] - b0) < 1e-9 and best[4] < 1e-9
    y2 = -(1.0 * (D - 216) + 0.012 * (D - 216) ** 2) - 110.0     # a smooth drift of the rate from 1.0 to 1.3
    sink = []
    sharp2, best2 = analyse(D, y2, out=sink.append)
    ok2 = not sharp2
    print("selftest: ok" if ok1 and ok2 else f"selftest FAILED: planted break found {ok1}, smooth curve called gradual {ok2}")
    return 0 if ok1 and ok2 else 1

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rows = sorted((parse(p) for p in sys.argv[1:]), key=lambda r: r["D"])
    D = np.array([r["D"] for r in rows])
    y = np.array([math.log({x["i"]: x["sigma"] for x in r["sig"]}[1]) for r in rows])
    print(f"{len(D)} states, D {D[0]:.4f} to {D[-1]:.4f}")
    for d, v in zip(D, y):
        print(f"  D {d:.4f}  ln sigma_1 {v:.6f}")
    analyse(D, y)

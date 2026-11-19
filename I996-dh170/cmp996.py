#!/usr/bin/env python3
"""#996: compare the sigma_k of two amp_trunc_hiermodel.py logs at every k both reached.
    python cmp996.py LOG_A LOG_B [--tol-from-resid]      (a line looks like `k 7: sigma_3 = (re + imj)  fit resid 9.3e-60  [834s]`)
Prints, per k, the relative difference |sigma_A - sigma_B| / |sigma_A| and the larger of the two fit residuals, and whether the difference is within 1e-14 (the
15 digits a log prints) and within the fit residual. The log prints 15 digits, so a comparison to a residual below 1e-15 cannot be made from the logs; the JSONs
(20 digits) are compared with --json A.json B.json, which is as far as the files go. Controls: --selftest plants a 1e-12 change and must find it (exit 1 if not)."""
import json
import re
import sys

PAT = re.compile(r"^k (\d+): sigma_(\d+) = \(([^ ]+) ([+-] ?[^ ]+)j\)\s+fit resid ([\d.e+-]+)")


def read(path):
    out = {}
    for line in open(path):
        m = PAT.match(line)
        if m:
            k = int(m.group(1))
            re_, im_ = float(m.group(3)), float(m.group(4).replace(" ", ""))
            out[k] = (complex(re_, im_), float(m.group(5)))
    return out


def compare(a, b):
    rows = []
    for k in sorted(set(a) & set(b)):
        sa, ra = a[k]
        sb, rb = b[k]
        d = abs(sa - sb) / abs(sa)
        rows.append((k, d, max(ra, rb)))
    return rows


def main():
    if "--selftest" in sys.argv:
        a = {3: (complex(0.5, 0.25), 1e-60)}
        b = {3: (complex(0.5, 0.25) * (1 + 1e-12), 1e-60)}
        r = compare(a, b)[0]
        ok = abs(r[1] - 1e-12) < 1e-13 and r[1] > 1e-14
        print("selftest:", "pass" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    if "--json" in sys.argv:
        x, y = [json.load(open(p)) for p in sys.argv[sys.argv.index("--json") + 1:][:2]]
        worst = 0.0
        for i, (p, q) in enumerate(zip(x["sigma_str"], y["sigma_str"])):
            a, b = complex(float(p[0]), float(p[1])), complex(float(q[0]), float(q[1]))
            pa, pb = [__import__("mpmath").mpc(*map(__import__("mpmath").mpf, t)) for t in (p, q)]
            d = abs(pa - pb) / abs(pa)
            worst = max(worst, float(d))
            print(f"sigma_{i}: {x['sigma_str'][i][0]} {x['sigma_str'][i][1]}  against  {y['sigma_str'][i][0]} {y['sigma_str'][i][1]}: relative difference {float(d):.2e}")
        print(f"JSON, dps {x.get('dps', 60)} against {y.get('dps', 60)}: worst relative difference {worst:.2e} (20 stored digits)")
        return
    a, b = read(sys.argv[1]), read(sys.argv[2])
    rows = compare(a, b)
    worst = 0.0
    for k, d, r in rows:
        worst = max(worst, d)
        print(f"k {k:2d} sigma_{(k - 1) // 2}: relative difference {d:.2e}, larger fit residual {r:.1e}: {'within the 15 printed digits (1e-14)' if d <= 1e-14 else 'DIFFERS'}")
    print(f"{len(rows)} k's in common, worst relative difference {worst:.2e}")


main()

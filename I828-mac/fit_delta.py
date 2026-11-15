#!/usr/bin/env python3
"""#828: the horizon rows' response to w0's Delta part at fixed horizon data, from diag_828.log. Per horizon field
(p, m, a, 4th), the max-norm changes f at moves d = D0, 1e-3 D0, 1e-6 D0 (D0 = w0's Delta part) are fitted by
f = s d + c d^2 through the first two moves, s / c is the move where the two terms are equal, and the third move is
predicted against its measurement (the fit's check: it fails when off by more than a factor 2). Max norms over a
field's rows, so s and c are scales, not one row's derivatives.
usage: python3 fit_delta.py diag_828.log      (exit 1 when a prediction is off by more than 2)"""
import re
import sys


def main(path):
    txt = open(path).read()
    D0 = float(re.search(r"w0 by block.*Delta ([0-9.e+-]+)", txt).group(1))
    rows = {}
    for tag, scale in (("Delta", 1.0), ("1e-3 Delta", 1e-3), ("1e-6 Delta", 1e-6)):
        ln = re.search(r"F\(P\(z0\) \+ " + re.escape(tag) + r"\) - F\(P\(z0\)\).*", txt).group(0)
        rows[scale] = {f: float(re.search(r"horizon " + f + r" ([0-9.e+-]+)", ln).group(1)) for f in "pma4"}
    ok = True
    print(f"w0's Delta part D0 = {D0:.3e}")
    for f in "pma4":
        d1, d2, d3 = D0, 1e-3 * D0, 1e-6 * D0
        f1, f2, f3 = rows[1.0][f], rows[1e-3][f], rows[1e-6][f]
        c = (f1 - f2 * d1 / d2) / (d1 * d1 - d2 * d1)
        s = (f2 - c * d2 * d2) / d2
        pred = s * d3 + c * d3 * d3
        good = 0.5 < pred / f3 < 2
        ok &= good
        print(f"  horizon {f}: s {s:.2e}, c {c:.2e}, s / c {s / c:.2e}; at {d3:.2e}: predicted {pred:.2e}, measured "
              f"{f3:.2e} ({'ok' if good else 'OFF'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))

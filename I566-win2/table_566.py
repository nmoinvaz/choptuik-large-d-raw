#!/usr/bin/env python3
"""#566: the weakest sigma at x_last = 0.96 ... 0.995 with its mode, the largest entry of J, the maximum of the weakest equilibrated sigma, and the reproducibility control (near_null_vec.py and near_null_eq_vec.py on 0.96 and 0.98
against the logged near_null.py and near_null_eq.py of #559). usage: python table_566.py (run from I566-win2 after the lanes; reads nnv_*.log, eqv_*.log here and ../I559-win2 logs)
The maximum: the layouts are 0.01 apart from 0.96 to 0.99 (0.005 for the last), the weakest equilibrated sigma is read at each, the maximum is the largest tabulated value and its location is bracketed by its two
neighbours (located to within 0.01 if both neighbours are lower and within 0.01); a parabola in ln sigma through the maximum and its neighbours gives an estimate."""
import math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I554-win2"))
import ladder_554 as l  # noqa: E402
LAY = [(0.96, "old096", ("I559-win2", "last096")), (0.97, "last097", None), (0.98, "old098", ("I559-win2", "last098")), (0.99, "last099", None), (0.995, "last0995", None)]


def jmax(path):
    m = re.search(r"\|J\| entries [0-9.e+-]+\.\.([0-9.e+-]+)", open(path, encoding="utf-8").read())
    return float(m.group(1))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    rows, allok = [], True
    for x, tag, old in LAY:
        r, ok1 = l.raw(os.path.join(HERE, f"nnv_{tag}.log"))
        e, ok2 = l.eq(os.path.join(HERE, f"eqv_{tag}.log"))
        allok = allok and ok1 and ok2
        rows.append((x, r, e, jmax(os.path.join(HERE, f"eqv_{tag}.log"))))
    print("| x_last | raw sigma_1..4 | equilibrated sigma_1..4 | weakest equilibrated sigma | its mode (top scaled component) | largest abs J_ij |\n|---|---|---|---|---|---|")
    for x, r, e, jm in rows:
        w = min(e, key=lambda t: t[1])
        print(f"| {x:g} | " + ", ".join(f"{s:.3e} ({c})" for _, s, c in r) + " | " + ", ".join(f"{s:.3e}" for _, s, c in e) + f" | {w[1]:.4e} | {w[2]} | {jm:.2e} |")
    xs = [x for x, *_ in rows]
    ws = [min(e, key=lambda t: t[1])[1] for _, _, e, _ in rows]
    i = int(np.argmax(ws))
    print(f"\nthe weakest equilibrated sigma is largest at x_last = {xs[i]:g} ({ws[i]:.4e}); neighbours {ws[i - 1]:.4e} ({xs[i - 1]:g}) and {ws[i + 1]:.4e} ({xs[i + 1]:g})" if 0 < i < len(xs) - 1 else f"\nthe weakest equilibrated sigma is largest at x_last = {xs[i]:g}, at the end of the tabulated range")
    if 0 < i < len(xs) - 1:
        a, b, c = (math.log(ws[i - 1]), math.log(ws[i]), math.log(ws[i + 1]))
        h = xs[i + 1] - xs[i]
        hl = xs[i] - xs[i - 1]
        # parabola through three points with unequal spacing
        A = np.array([[xs[k] ** 2, xs[k], 1.0] for k in (i - 1, i, i + 1)])
        co = np.linalg.solve(A, np.array([a, b, c]))
        xv = -co[1] / (2 * co[0])
        print(f"parabola in ln sigma through the three: vertex x_last = {xv:.4f}; bracket {xs[i - 1]:g} to {xs[i + 1]:g} (spacings {hl:g}, {h:g}): located to within 0.01 if the maximum is interior and the spacings are 0.01: {'yes' if max(h, hl) <= 0.0101 else 'no'}")
        print(f"the values at {xs[i - 1]:g} and {xs[i]:g} differ by {abs(ws[i - 1] / ws[i] - 1) * 100:.2f}%, at {xs[i + 1]:g} by {(ws[i + 1] / ws[i] - 1) * 100:+.1f}%")
    print("\nreproducibility control (relative differences of sigma, near_null_vec.py / near_null_eq_vec.py against the logged ones of #559)")
    for x, tag, old in LAY:
        if old is None:
            continue
        d, t = old
        r1, _ = l.raw(os.path.join(HERE, f"nnv_{tag}.log"))
        r0, _ = l.raw(os.path.join(HERE, "..", d, f"nn_{t}.log"))
        e1, _ = l.eq(os.path.join(HERE, f"eqv_{tag}.log"))
        e0, _ = l.eq(os.path.join(HERE, "..", d, f"eq_{t}.log"))
        rr = max(abs(a[1] / b[1] - 1) for a, b in zip(r1, r0))
        re_ = max(abs(a[1] / b[1] - 1) for a, b in zip(e1, e0))
        print(f"  x_last {x:g}: raw {rr:.1e}, equilibrated {re_:.1e}")
    print("all check lines pass" if allok else "a check line is not pass")

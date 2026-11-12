#!/usr/bin/env python3
"""#572: the weakest equilibrated sigma at x_last = 0.95, 0.97, 0.98, 0.99 for crawlI's D 237.1312, with its mode, beside D 242.36's (#566, #559: 0.96 ... 0.995), and the maximum.
usage: python table_572.py [--selftest]       (run from I572-win2 after the lanes; reads nn_*.log and eq_*.log here, ../I566-win2 and ../I559-win2 for D 242.36)
The maximum: the largest tabulated weakest equilibrated sigma; located to within 0.01 when it is interior and both neighbours are within 0.01 (here the layouts are 0.01 apart except 0.95-0.97, 0.02); a parabola in ln sigma through
the maximum and its neighbours gives an estimate. Acceptance of #572: the table with modes; the maximum located to within 0.01 or the end of the range stated, with D 242.36's 0.975 beside it (the check fails if the maximum at
D 237.13 lies more than 0.02 from 0.975 and the report does not say so); renode checks pass and the sign control exits 1 once.
--selftest: a planted series with a peak is located and a parabola recovers its vertex."""
import math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "I554-win2"))
import ladder_554 as l  # noqa: E402
LAY = [(0.95, "last095"), (0.97, "last097"), (0.98, "last098"), (0.99, "last099")]
REF = [(0.96, "I559-win2", "nn_last096.log", "eq_last096.log"), (0.97, "I566-win2", "nnv_last097.log", "eqv_last097.log"), (0.98, "I559-win2", "nn_last098.log", "eq_last098.log"),
       (0.99, "I566-win2", "nnv_last099.log", "eqv_last099.log"), (0.995, "I566-win2", "nnv_last0995.log", "eqv_last0995.log")]


def vertex(xs, ys):
    A = np.array([[x * x, x, 1.0] for x in xs])
    c = np.linalg.solve(A, np.array(ys))
    return -c[1] / (2 * c[0])


def selftest():
    xs = [0.95, 0.97, 0.98, 0.99]
    ys = [-(x - 0.972) ** 2 * 3000 + 5 for x in xs]
    i = int(np.argmax(ys))
    v = vertex(xs[i - 1:i + 2], ys[i - 1:i + 2])
    ok = xs[i] == 0.97 and abs(v - 0.972) < 1e-6
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


def jmax(path):
    import re
    m = re.search(r"\|J\| entries [0-9.e+-]+\.\.([0-9.e+-]+)", open(path, encoding="utf-8").read())
    return float(m.group(1))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rows, allok = [], True
    for x, tag in LAY:
        if not os.path.exists(os.path.join(HERE, f"eq_{tag}.log")) or "check:" not in open(os.path.join(HERE, f"eq_{tag}.log"), encoding="utf-8").read():
            continue
        r, o1 = l.raw(os.path.join(HERE, f"nn_{tag}.log"))
        e, o2 = l.eq(os.path.join(HERE, f"eq_{tag}.log"))
        allok = allok and o1 and o2
        rows.append((x, r, e, jmax(os.path.join(HERE, f"eq_{tag}.log"))))
    print("D 237.13\n| x_last | raw sigma_1..4 | equilibrated sigma_1..4 | weakest equilibrated sigma | its mode (top scaled component) | largest abs J_ij |\n|---|---|---|---|---|---|")
    for x, r, e, jm in rows:
        w = min(e, key=lambda t: t[1])
        print(f"| {x:g} | " + ", ".join(f"{s:.3e} ({c})" for _, s, c in r) + " | " + ", ".join(f"{s:.3e}" for _, s, c in e) + f" | {w[1]:.4e} | {w[2]} | {jm:.2e} |")
    xs = [x for x, *_ in rows]
    ws = [min(e, key=lambda t: t[1])[1] for _, _, e, _ in rows]
    if len(xs) >= 3:
        i = int(np.argmax(ws))
        if 0 < i < len(xs) - 1:
            v = vertex(xs[i - 1:i + 2], [math.log(w) for w in ws[i - 1:i + 2]])
            print(f"\nD 237.13: the weakest equilibrated sigma is largest at x_last = {xs[i]:g} ({ws[i]:.4e}); neighbours {ws[i - 1]:.4e} ({xs[i - 1]:g}), {ws[i + 1]:.4e} ({xs[i + 1]:g}); parabola vertex in ln sigma {v:.4f}")
            print(f"located to within 0.01: {'yes' if max(xs[i + 1] - xs[i], xs[i] - xs[i - 1]) <= 0.0101 else 'bracket ' + format(xs[i + 1] - xs[i - 1], 'g') + ' wide'}; distance of the maximum from D 242.36's 0.975: {abs(xs[i] - 0.975):.3f} (vertex {abs(v - 0.975):.3f})")
        else:
            print(f"\nD 237.13: the weakest equilibrated sigma is largest at x_last = {xs[i]:g}, at the end of the tabulated range")
    print("\nD 242.36 for comparison (#559, #566)\n| x_last | weakest equilibrated sigma | mode |\n|---|---|---|")
    for x, d, nn, eqf in REF:
        e, _ = l.eq(os.path.join(HERE, "..", d, eqf))
        w = min(e, key=lambda t: t[1])
        print(f"| {x:g} | {w[1]:.4e} | {w[2]} |")
    print("all check lines pass" if allok else "a check line is not pass")

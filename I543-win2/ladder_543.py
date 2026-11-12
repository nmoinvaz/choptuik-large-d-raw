#!/usr/bin/env python3
"""#543: ln sigma against x_last at D 242.36, layouts 0.3, 0.4, 0.5, 0.6, x_last (x_last = 0.66 ... 0.80) beside #537's 0.70 (baseline) and 0.72.
usage: python ladder_543.py [--selftest] [--predict]       (run from I543-win2 after the lanes; needs ../I537-win2/ and the logs of this folder)
Raw sigma from nn_<tag>.log (`near_null.py`), equilibrated (Curtis-Reid + Ruiz) from eq_<tag>.log (`near_null_eq.py`). The shift is ln sigma_i(x_last) - ln sigma_i(0.70).
Fits of the shift of ln sigma_3 (both readings) by a + b x and a + b ln x, over the points with x_last <= 0.76 (--predict uses only these and prints the prediction for x_last = 0.80, which is also the law's value for
#502's six-node 0.3-0.8 layout if the law is about the last node), then over all points. The better of the two forms is the one with the smaller rms residual. Acceptance of #543: the equilibrated residual of the better form is at
most 0.1 (the check fails if neither reaches it); the prediction is written on the issue before the comparison with the 0.80 point and with #502's layout (equilibrated ln sigma_3 +11.56, raw -20.2 against the 0.3-0.7 state).
--selftest: a planted a + b ln x (a = 0.3, b = 40) with noise 0.02 is named log and recovered to 2% in b, a planted a + b x (b = -30) is named linear, and a planted law with noise 0.5 fails the 0.1 check."""
import math, os, re, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
TAGS = {0.66: "last066", 0.68: "last068", 0.69: "last069", 0.71: "last071", 0.74: "last074", 0.76: "last076", 0.80: "last080"}
OLD = {0.70: "base", 0.72: "last072"}          # from I537-win2
I502 = {"raw": math.log(6.968e-35 / 4.392e-26), "eq": math.log(2.7718e-54 / 2.6498e-59)}


def read(path):
    return open(path, encoding="utf-8").read()


def raw(path):
    s = read(path)
    v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    return [v[i] for i in (1, 2, 3, 4)], "check: pass" in s


def eq(path):
    s = read(path)
    v = {int(m.group(1)): float(m.group(2)) for m in re.finditer(r"^\s+Curtis-Reid \+ Ruiz sigma_(\d) ([0-9.e+-]+) \(converged", s, re.M)}
    return [v[i] for i in (1, 2, 3, 4)], bool(re.search(r"^check: pass", s, re.M))


def collect(maxx=9.9):
    pts, ok = {}, True
    for x, tag in sorted({**{k: (HERE, v) for k, v in TAGS.items()}, **{k: (os.path.join(HERE, "..", "I537-win2"), v) for k, v in OLD.items()}}.items()):
        d, t = tag
        if x > maxx or not os.path.exists(os.path.join(d, f"eq_{t}.log")):
            continue
        r, o1 = raw(os.path.join(d, f"nn_{t}.log"))
        e, o2 = eq(os.path.join(d, f"eq_{t}.log"))
        pts[x] = (r, e)
        ok = ok and o1 and o2
    return pts, ok


def fit(x, y, form):
    X = np.column_stack([np.ones_like(x), x if form == "linear" else np.log(x)])
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ beta
    return beta, float(np.sqrt(np.mean(res ** 2))), float(np.max(np.abs(res)))


def pred(beta, form, x):
    return beta[0] + beta[1] * (x if form == "linear" else math.log(x))


def selftest():
    x = np.array([0.66, 0.68, 0.69, 0.70, 0.71, 0.72, 0.74, 0.76])
    rng = np.random.default_rng(3)
    ok = True
    y = 0.3 + 40 * np.log(x / 0.7) + rng.normal(0, 0.02, len(x))
    fl, fg = fit(x, y, "linear"), fit(x, y, "log")
    good = fg[1] < fl[1] and abs(fg[0][1] - 40) <= 0.8
    print(f"planted log law: linear rms {fl[1]:.4f}, log rms {fg[1]:.4f}, b {fg[0][1]:.2f} (planted 40): {'pass' if good else 'FAIL'}")
    ok = ok and good
    y = 0.3 - 30 * (x - 0.7) + 40 * (x - 0.7) ** 2 * 0 + rng.normal(0, 0.02, len(x))
    fl, fg = fit(x, y, "linear"), fit(x, y, "log")
    good = fl[1] < fg[1] and abs(fl[0][1] + 30) <= 0.9
    print(f"planted linear law: linear rms {fl[1]:.4f}, log rms {fg[1]:.4f}, b {fl[0][1]:.2f} (planted -30): {'pass' if good else 'FAIL'}")
    ok = ok and good
    y = 0.3 + 40 * np.log(x / 0.7) + rng.normal(0, 0.5, len(x))
    best = min(fit(x, y, "linear")[1], fit(x, y, "log")[1])
    good = best > 0.1
    print(f"planted law with noise 0.5: best rms {best:.3f} (must exceed 0.1, so the acceptance fails): {'pass' if good else 'FAIL'}")
    ok = ok and good
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    predict = "--predict" in sys.argv
    pts, allok = collect(maxx=0.76 if predict else 9.9)
    xs = np.array(sorted(pts))
    if 0.70 not in pts:
        raise SystemExit("no baseline")
    print("| x_last | reading | ln sigma_1 shift | ln sigma_2 | ln sigma_3 | ln sigma_4 |\n|---|---|---|---|---|---|")
    sh = {}
    for x in xs:
        for k, nm in ((0, "raw"), (1, "equilibrated")):
            d = [math.log(pts[x][k][i] / pts[0.70][k][i]) for i in range(4)]
            sh[(x, nm)] = d
            print(f"| {x:.2f} | {nm} | " + " | ".join(f"{v:+.3f}" for v in d) + " |")
    print()
    fits = {}
    for nm in ("raw", "equilibrated"):
        y = np.array([sh[(x, nm)][2] for x in xs])
        for form in ("linear", "log"):
            beta, rms, mx = fit(xs, y, form)
            fits[(nm, form)] = (beta, rms, mx)
            print(f"{nm}, ln sigma_3 shift = a + b {'x' if form == 'linear' else 'ln x'} over {len(xs)} points x_last {xs[0]:.2f} to {xs[-1]:.2f}: a {beta[0]:+.3f}, b {beta[1]:+.3f}, rms residual {rms:.4f} (max {mx:.4f})")
    print()
    for nm in ("raw", "equilibrated"):
        bf = min(("linear", "log"), key=lambda f: fits[(nm, f)][1])
        print(f"{nm}: the better form is {bf} (rms {fits[(nm, bf)][1]:.4f} against {fits[(nm, 'log' if bf == 'linear' else 'linear')][1]:.4f})")
    bfe = min(("linear", "log"), key=lambda f: fits[("equilibrated", f)][1])
    print(f"acceptance (equilibrated residual of the better form at most 0.1): {'pass' if fits[('equilibrated', bfe)][1] <= 0.1 else 'FAIL'}")
    print()
    # the prediction always comes from the points with x_last <= 0.76 only
    sub = np.array([x for x in xs if x <= 0.76 + 1e-9])
    for nm, key in (("raw", "raw"), ("equilibrated", "eq")):
        y = np.array([sh[(x, nm)][2] for x in sub])
        f2 = {form: fit(sub, y, form) for form in ("linear", "log")}
        bf = min(f2, key=lambda f: f2[f][1])
        other = "log" if bf == "linear" else "linear"
        line = (f"{nm}: fit over the {len(sub)} points x_last <= 0.76: better form {bf} (rms {f2[bf][1]:.4f}, {other} {f2[other][1]:.4f}); prediction of the shift of ln sigma_3 at x_last = 0.80 "
                f"(five nodes 0.3 ... 0.6, 0.8 and, if the law is about the last node, #502's six-node 0.3-0.8 layout): {pred(f2[bf][0], bf, 0.80):+.2f} by the {bf} form, {pred(f2[other][0], other, 0.80):+.2f} by the {other} form")
        if not predict and 0.80 in pts:
            line += f"; measured five-node 0.80: {sh[(0.80, nm)][2]:+.2f}; #502's six-node layout: {I502[key]:+.2f}"
        print(line)
    print("all check lines pass" if allok else "a check line is not pass")

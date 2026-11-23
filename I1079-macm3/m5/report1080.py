#!/usr/bin/env python3
"""report1080.py args NAME | report [--dir walks] [--inputs inputs] | selftest: #1080's inputs and its reading.
args NAME   print "A w B3 C3" (x1 or x2) from the certified M = 3 box centre in inputs/ (B3, C3 to 10 decimals, as #1026's walks take them).
report      one table from walks/walk_{x1,x2}_xi{0.2,0.25}.json and inputs/zeros_M1.md. The reading, fixed before the run (#1080):
            a zero PERSISTS at M = 5 when both hold: (1) its walks converge (|r_3|, |r_5| below 1e-6, #1026's bar) at xi1 0.2 and 0.25,
            to the same (A, w/w_inf) within 1e-5; (2) its M = 3 -> 5 shift is smaller than its M = 1 -> 3 shift (Euclidean norm in
            (A, w/w_inf)); if no M = 1 partner lies within 0.3, the bar is 0.1. It FAILS when a walk does not converge, or the shift is larger.
            The M = 1 partner is the nearest zero of orientation +1 in inputs/zeros_M1.md (#995's located list).
partners    the two zeros' M = 3 centres and M = 1 partners, before any run.
selftest    synthetic walks through the same code: a smaller shift persists, and each of five breakages (larger shift, an unconverged walk,
            radii 1e-4 apart, |r_3| 2e-6, no partner within 0.3 with a shift above 0.1) must fail; the parser must read 25 zeros of sum -1."""
import json
import math
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
BOXES = dict(x1="A_M_box_M3x1E2_h1e-12_w1e-13.json", x2="A_M_box_M3x2E2_h1e-12_w1e-12.json")
STORED5 = (2.718579189, 0.999228404)        # the known zero's M = 5 zero (inputs/hier_M5_full_schur.log)
BAR_R, AGREE, NEAR, FAR_BAR = 1e-6, 1e-5, 0.3, 0.1
RADII = ("0.2", "0.25")


def box_centre(name, inputs):
    p = json.load(open(os.path.join(inputs, BOXES[name])))["p"]
    return float(p[0]), float(p[1]), float(p[2]), float(p[3])


def m1_zeros(inputs):
    z = []
    for line in open(os.path.join(inputs, "zeros_M1.md")):
        c = [t.strip() for t in line.strip().strip("|").split("|")]
        if c and c[0] in ("-1", "+1"):
            z.append((int(c[0]), float(c[1]), float(c[2]), c[4]))
    return z


def partner(z, A, w, sign=+1):
    return min((q for q in z if q[0] == sign), key=lambda q: math.hypot(q[1] - A, q[2] - w))


def judge(name, walks, centre, z):
    """walks: {xi: verdict dict}. Returns (verdict, reasons, row dict)."""
    A3, w3 = centre[0], centre[1]
    q = partner(z, A3, w3)
    d31 = math.hypot(A3 - q[1], w3 - q[2])
    bar = d31 if d31 <= NEAR else FAR_BAR
    why, row = [], dict(partner=q, d31=d31, bar=bar, xi={})
    for xi in RADII:
        v = walks.get(xi)
        if v is None or not v.get("converged"):
            why.append(f"xi1 {xi}: no converged walk ({'not run' if v is None else v.get('why')})")
            continue
        s53 = math.hypot(v["A"] - A3, v["w"] - w3)
        F3, F5 = math.hypot(*v["F3"]), math.hypot(*v["F5"])
        row["xi"][xi] = dict(A=v["A"], w=v["w"], r1=math.hypot(*v["r1"]), r3=v["r3"], r5=v["r5"], s53=s53, d53=(v["A"] - A3, v["w"] - w3),
                             F5F3=F5 / F3, solves=v["points"], step=v["newton_step"], known=math.hypot(v["A"] - STORED5[0], v["w"] - STORED5[1]))
        if not (v["r3"] < BAR_R and v["r5"] < BAR_R):
            why.append(f"xi1 {xi}: |r_3| {v['r3']:.1e} or |r_5| {v['r5']:.1e} not under {BAR_R:g}")
        if not s53 < bar:
            why.append(f"xi1 {xi}: M3 -> 5 shift {s53:.4f} not below the bar {bar:.4f}")
    if len(row["xi"]) == 2:
        a, b = row["xi"][RADII[0]], row["xi"][RADII[1]]
        if not (abs(a["A"] - b["A"]) <= AGREE and abs(a["w"] - b["w"]) <= AGREE):
            why.append(f"the radii disagree: ({a['A'] - b['A']:+.2e}, {a['w'] - b['w']:+.2e}) against {AGREE:g}")
    return ("FAILS" if why else "PERSISTS"), why, row


def load_walks(d, name):
    out = {}
    for xi in RADII:
        p = os.path.join(d, f"walk_{name}_xi{xi}.json")
        if os.path.exists(p):
            out[xi] = json.load(open(p))["verdict"]
    return out


def report(d, inputs):
    z = m1_zeros(inputs)
    print(f"M = 1 zeros read: {len(z)}, sum of orientations {sum(q[0] for q in z):+d} (inputs/zeros_M1.md)\n")
    res = {}
    for name in ("x1", "x2"):
        c = box_centre(name, inputs)
        res[name] = judge(name, load_walks(d, name), c, z)
    print("| zero | xi1 | converged (A, w/w_inf) | \\|r1\\| | \\|r3\\| | \\|r5\\| | solves | Newton step | M3 -> 5 shift (dA, dw), norm | \\|F5\\|/\\|F3\\| |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for name in ("x1", "x2"):
        row = res[name][2]
        for xi in RADII:
            r = row["xi"].get(xi)
            if r is None:
                print(f"| {name} | {xi} | not converged | | | | | | | |")
                continue
            print(f"| {name} | {xi} | ({r['A']:.9f}, {r['w']:.9f}) | {r['r1']:.2e} | {r['r3']:.1e} | {r['r5']:.1e} | {r['solves']} | ({r['step'][0]:+.1e}, {r['step'][1]:+.1e}) | "
                  f"({r['d53'][0]:+.5f}, {r['d53'][1]:+.5f}), {r['s53']:.5f} | {r['F5F3']:.3f} |")
    print()
    for name in ("x1", "x2"):
        c = box_centre(name, inputs)
        v, why, row = res[name]
        q = row["partner"]
        print(f"{name}: M = 3 zero ({c[0]:.9f}, {c[1]:.9f}); M = 1 partner (+1) ({q[1]:.6f}, {q[2]:.6f}) located at xi1 {q[3]}, "
              f"M1 -> 3 shift ({c[0] - q[1]:+.5f}, {c[1] - q[2]:+.5f}), distance {row['d31']:.5f}; bar {row['bar']:.5f}" + ("" if row["d31"] <= NEAR else " (no partner within 0.3)"))
        if len(row["xi"]) == 2:
            a, b = row["xi"][RADII[0]], row["xi"][RADII[1]]
            print(f"    xi1 0.2 against 0.25: dA {a['A'] - b['A']:+.2e}, dw {a['w'] - b['w']:+.2e}; distance to the known zero's M = 5 zero {a['known']:.4f}")
        print(f"    VERDICT {name}: {v}" + ("" if not why else " (" + "; ".join(why) + ")"))
    return 0


def partners(inputs):
    z = m1_zeros(inputs)
    for name in ("x1", "x2"):
        c = box_centre(name, inputs)
        q = partner(z, c[0], c[1])
        d = math.hypot(c[0] - q[1], c[1] - q[2])
        print(f"{name}: M = 3 zero ({c[0]:.9f}, {c[1]:.9f}), M = 1 partner ({q[1]:.6f}, {q[2]:.6f}) located at xi1 {q[3]}, "
              f"shift ({c[0] - q[1]:+.5f}, {c[1] - q[2]:+.5f}), distance {d:.5f}, bar {d if d <= NEAR else FAR_BAR:.5f}")


def synth(dirn, name, c, shift, conv=(True, True), r3=1e-8, gap=0.0):
    for i, xi in enumerate(RADII):
        A, w = c[0] + shift[0] + (gap if i else 0.0), c[1] + shift[1]
        v = dict(converged=conv[i], why="the start solve did not converge") if not conv[i] else dict(
            converged=True, A=A, w=w, r1=[1e-5, 0.0], r3=r3, r5=1e-8, F3=[0.3, 0.1], F5=[0.01, 0.02], newton_step=[1e-7, 1e-7], points=9, xi1=xi)
        json.dump(dict(name=name, xi1=xi, verdict=v), open(os.path.join(dirn, f"walk_{name}_xi{xi}.json"), "w"))


def selftest():
    z = m1_zeros(os.path.join(HERE, "inputs"))
    ok = len(z) == 25 and sum(q[0] for q in z) == -1
    print(f"selftest: parser read {len(z)} zeros, sum {sum(q[0] for q in z):+d} (expect 25, -1): {'ok' if len(z) == 25 and sum(q[0] for q in z) == -1 else 'FAIL'}")
    c = box_centre("x1", os.path.join(HERE, "inputs"))
    d31 = partner(z, c[0], c[1])
    d31 = math.hypot(c[0] - d31[1], c[1] - d31[2])
    far = [(+1, 9.0, 9.0, "0.2")]                     # a list with no partner within 0.3
    cases = [("smaller shift", dict(shift=(0.5 * d31, 0.0)), z, "PERSISTS"),
             ("larger shift", dict(shift=(1.5 * d31, 0.0)), z, "FAILS"),
             ("unconverged walk", dict(shift=(0.5 * d31, 0.0), conv=(True, False)), z, "FAILS"),
             ("radii 1e-4 apart", dict(shift=(0.5 * d31, 0.0), gap=1e-4), z, "FAILS"),
             ("|r_3| 2e-6", dict(shift=(0.5 * d31, 0.0), r3=2e-6), z, "FAILS"),
             ("no partner, shift 0.2", dict(shift=(0.2, 0.0)), far, "FAILS"),
             ("no partner, shift 0.05", dict(shift=(0.05, 0.0)), far, "PERSISTS")]
    for label, kw, zz, want in cases:
        with tempfile.TemporaryDirectory() as t:
            synth(t, "x1", c, **kw)
            got = judge("x1", load_walks(t, "x1"), c, zz)[0]
        good = got == want
        ok &= good
        print(f"selftest: {label}: {got} (expect {want}): {'ok' if good else 'FAIL'}")
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    opt = lambda k, dflt: a[a.index(k) + 1] if k in a else dflt
    if a[:1] == ["args"]:
        c = box_centre(a[1], opt("--inputs", os.path.join(HERE, "inputs")))
        print(f"{c[0]!r} {c[1]!r} {c[2]:.10f} {c[3]:.10f}")
        sys.exit(0)
    if a[:1] == ["report"]:
        sys.exit(report(opt("--dir", os.path.join(HERE, "walks")), opt("--inputs", os.path.join(HERE, "inputs"))))
    if a[:1] == ["partners"]:
        partners(opt("--inputs", os.path.join(HERE, "inputs")))
        sys.exit(0)
    if a[:1] == ["selftest"]:
        sys.exit(selftest())
    print(__doc__)
    sys.exit(2)

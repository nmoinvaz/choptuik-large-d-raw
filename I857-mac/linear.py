"""I857-mac check: at D 240.1244, Newton's step returns a pure Delta move linearly, as the move itself.

Reads FOLDER/power.json (`step_spread.py power --json`) and the moves from FOLDER/dl_D240_r<k>.json. Passes when
power's same-start check passed, the reading is linear (both p in [0.9, 1.1]) and |dev| / move is in [0.99, 1.01] at
each rel. Its control is #850's folder I850-mac, which must FAIL (quadratic, |dev| / move 6.5e13 and more).

--noise P.json reads a power.json that also holds seed 3 at the smallest rel, whose Delta sign is opposite to seed 1's
(FOLDER/dl_D240_r<k>_s3.json). Their devs' linear parts cancel in the sum, so n = |dev(1) + dev(3)| / (2 move) is the
part of dev that does not flip with the move (the quadratic term and rounding). Passes when n < 1e-3, a tenth of the
ratio's tolerance. Its control --mutate samesign sums dev(1) - dev(3), so n reads about 1 and must FAIL.

Run: python3 linear.py FOLDER [--noise P.json] [--mutate samesign], or python3 linear.py --selftest (planted: a linear
return passes, one 2% off fails on the ratio, and a floor of 1e-2 of the move fails on n). Exits 1 when a check fails.
"""
import json
import math
import os
import sys


def group(pw, seed):
    return next(g for g in pw["groups"] if g["D_str"].startswith("240.1") and g["blocks"] == ["Delta"]
                and g["seed"] == seed)


def check(pw, moves, pn=None, moves3=None, mutate=""):
    g = group(pw, 1)
    lo, hi = pw["lin"]
    devs = sorted(g["devs"], key=lambda t: -t[0])
    print(f"linear: D {g['D_str'][:12]}, seed 1, reading {g.get('reading', 'planted')}")
    r_ok = True
    for rel, dev in devs:
        ratio = abs(dev) / moves[rel]
        r_ok &= 0.99 <= ratio <= 1.01
        print(f"  rel {rel:.0e}: move {moves[rel]:.6e}, dev {dev:+.6e}, |dev| / move {ratio:.6g}")
    ps = g["p"]
    checks = [("same start", g["same_start"], "power's same-start check"),
              ("linear", len(ps) == 2 and all(p is not None and lo <= p <= hi for p in ps),
               "p " + ", ".join("none" if p is None else f"{p:.4f}" for p in ps) + f" in [{lo}, {hi}]"),
              ("ratio", r_ok, "|dev| / move in [0.99, 1.01] at each rel")]
    if pn:
        rel = devs[-1][0]
        d1, d3 = dict(group(pn, 1)["devs"])[rel], dict(group(pn, 3)["devs"])[rel]
        s = d1 - d3 if mutate == "samesign" else d1 + d3
        n = abs(s) / (moves[rel] + moves3[rel])
        print(f"  noise at rel {rel:.0e}: dev(1) {d1:+.6e}, dev(3) {d3:+.6e}, moves {moves[rel]:.6e}, "
              f"{moves3[rel]:.6e}, sum {s:+.6e}{' (mutate samesign)' if mutate == 'samesign' else ''}")
        checks.append(("noise", n < 1e-3, f"n = |dev(1) + dev(3)| / (2 move) {n:.3e} (< 1e-3)"))
    for name, ok, what in checks:
        print(f"  check {name}: {what}: {'pass' if ok else 'FAIL'}")
    return all(c[1] for c in checks)


def planted(scale, floor):
    # dev = scale move + q rel^2 + floor move(1e-85), with seed 3's move of the opposite sign
    rels, q, D = [1e-83, 1e-84, 1e-85], 1.1027e81, "240.1244140625000000350414"
    moves = {r: 1.6866 * r for r in rels}
    dv = {s: [[r, s * scale * moves[r] + q * r * r + floor * moves[1e-85]] for r in rels] for s in (1, -1)}
    ps = [math.log(dv[1][i][1] / dv[1][i + 1][1]) / math.log(10) for i in range(2)]
    gr = [dict(D_str=D, blocks=["Delta"], seed=1, devs=dv[1], p=ps, same_start=True),
          dict(D_str=D, blocks=["Delta"], seed=3, devs=dv[-1][2:], p=[], same_start=True)]
    return dict(lin=[0.9, 1.1], groups=gr), moves


def load(d, tag=""):
    out = {}
    for k in (83, 84, 85):
        f = os.path.join(d, f"dl_D240_r{k}{tag}.json")
        if os.path.exists(f):
            js = json.load(open(f))
            r = next(r for r in js["runs"] if r["seed"] is not None and not r["control"])
            out[js["rel"]] = r["move"]
    return out


argv = sys.argv[1:]
if argv[0] == "--selftest":
    res = []
    for scale, floor, w in [(1.0, 0.0, True), (1.02, 0.0, False), (1.0, 1e-2, False)]:
        print(f"planted: scale {scale}, floor {floor} (want {'pass' if w else 'FAIL'})")
        pw, moves = planted(scale, floor)
        res.append(check(pw, moves, pw, moves) == w)
    ok = all(res)
    print(f"linear selftest: {'PASS' if ok else 'FAIL'}")
else:
    d = argv[0]
    mutate = argv[argv.index("--mutate") + 1] if "--mutate" in argv else ""
    noise = argv[argv.index("--noise") + 1] if "--noise" in argv else ""
    print(f"linear {d}{' --noise ' + noise if noise else ''}{' --mutate ' + mutate if mutate else ''}")
    moves = load(d)
    if not moves:
        # #850's folder, the control: its rels 1e-65 .. 1e-67
        for k in (65, 66, 67):
            js = json.load(open(os.path.join(d, f"dl_D240_r{k}.json")))
            moves[js["rel"]] = next(r for r in js["runs"] if r["seed"] is not None and not r["control"])["move"]
    ok = check(json.load(open(os.path.join(d, "power.json"))), moves,
               json.load(open(noise)) if noise else None, load(d, "_s3"), mutate)
    print(f"linear: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)

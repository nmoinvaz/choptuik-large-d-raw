"""I899-mac check: at D 252.6135, Newton's step returns a pure Delta move linearly, as the move itself.

Reads FOLDER/power.json (`step_spread.py power --json` over seed 1 at rel 1e-93, 1e-94, 1e-95 and seed 3 at 1e-95)
and the moves from FOLDER/dl_D252_r<k>.json. The seeds' Delta signs are opposite, so at the smallest rel
L = |dev(1) - dev(3)| / (move(1) + move(3)) is the odd part of the return and n = |dev(1) + dev(3)| / (move(1) +
move(3)) the even part (the quadratic term, #856's q, and any floor), as in I857-mac/tables.py. Passes when power's
same-start check passed, L is in [0.99, 1.01] and n < 1e-3. Reported: |dev| / move at each rel and power's reading.
The control --mutate samesign swaps the two (L from the sum, n from the difference), so n reads about 1 and must FAIL.

Run: python3 oddeven.py FOLDER [--mutate samesign], or python3 oddeven.py --selftest (planted: a linear return passes,
one 2% off fails on L, and a floor of 1e-2 of the move fails on n). Exits 1 when a check fails.
"""
import json
import os
import sys


def check(pw, moves, mutate=""):
    g = {x["seed"]: x for x in pw["groups"] if x["blocks"] == ["Delta"]}
    g1 = g[1]
    print(f"oddeven: D {g1['D_str'][:12]}, power's reading of seed 1 {g1.get('reading', 'planted')}, p "
          + (", ".join("none" if p is None else f"{p:.4f}" for p in g1["p"]) or "-"))
    for rel, dev in sorted(g1["devs"], key=lambda t: -t[0]):
        mv = moves[(1, rel)]
        print(f"  rel {rel:.0e}: move {mv:.6e}, dev {dev:+.6e}, |dev| / move {abs(dev) / mv:.6g}")
    rel = min(r for r, _ in g1["devs"])
    d1, d3 = dict(g1["devs"])[rel], dict(g[3]["devs"])[rel]
    m = moves[(1, rel)] + moves[(3, rel)]
    odd, even = abs(d1 - d3) / m, abs(d1 + d3) / m
    if mutate == "samesign":
        odd, even = even, odd
    print(f"  at rel {rel:.0e}: dev(1) {d1:+.10e}, dev(3) {d3:+.10e}, L {odd:.10f}, L - 1 {odd - 1:+.4e}, n {even:.6e}"
          + (" (mutate samesign)" if mutate == "samesign" else ""))
    same = all(x["same_start"] for x in g.values())
    checks = [("same start", same, "power's same-start check, each seed"),
              ("odd", 0.99 <= odd <= 1.01, f"L {odd:.6f} in [0.99, 1.01]"),
              ("even", even < 1e-3, f"n {even:.3e} (< 1e-3)")]
    for name, ok, what in checks:
        print(f"  check {name}: {what}: {'pass' if ok else 'FAIL'}")
    return all(c[1] for c in checks)


def planted(scale, floor):
    # dev = scale move + q rel^2 + floor move(1e-95), seed 3's move of the opposite sign; q is #856's
    rels, q, D = [1e-93, 1e-94, 1e-95], -2.686175e89, "252.6134675651790"
    moves = {(s, r): 1.6845 * r for s in (1, 3) for r in rels}
    dv = {s: [[r, s * scale * moves[(1, r)] + q * r * r + floor * moves[(1, 1e-95)]] for r in rels] for s in (1, -1)}
    gr = [dict(D_str=D, blocks=["Delta"], seed=1, devs=dv[1], p=[], same_start=True),
          dict(D_str=D, blocks=["Delta"], seed=3, devs=dv[-1][2:], p=[], same_start=True)]
    return dict(groups=gr), moves


def load(d):
    moves = {}
    for k in (93, 94, 95):
        js = json.load(open(os.path.join(d, f"dl_D252_r{k}.json")))
        for r in js["runs"]:
            if r["seed"] is not None and not r["control"]:
                moves[(r["seed"], r["rel"])] = r["move"]
    return moves


argv = sys.argv[1:]
if argv[0] == "--selftest":
    res = []
    for scale, floor, w in [(1.0, 0.0, True), (1.02, 0.0, False), (1.0, 1e-2, False)]:
        print(f"planted: scale {scale}, floor {floor} (want {'pass' if w else 'FAIL'})")
        res.append(check(*planted(scale, floor)) == w)
    ok = all(res)
    print(f"oddeven selftest: {'PASS' if ok else 'FAIL'}")
else:
    d = argv[0]
    mutate = argv[argv.index("--mutate") + 1] if "--mutate" in argv else ""
    print(f"oddeven {d}{' --mutate ' + mutate if mutate else ''}")
    ok = check(json.load(open(os.path.join(d, "power.json"))), load(d), mutate)
    print(f"oddeven: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)

"""I900-mac check: the cross term of a start off the root is linear in the offset (D 240.1244).

Each start z_s = u2 + s (truth - u2) has one step_spread.py run, seeds 1 and 3 at rel 1e-85 on the Delta block
(dl_D240_s<s>.json), and its power.json (p_s<s>.json, dev = dDelta(seed) - dDelta(unperturbed) from eight parts).
The seeds' Delta signs are opposite, so L = |dev(1) - dev(3)| / (move(1) + move(3)) is the odd part of the return and
n = |dev(1) + dev(3)| / (move(1) + move(3)) the even part, as in I857-mac/tables.py. c = L - 1 of the stored truth
from #857's runs (I857-mac/truth/, +8.324447e-02).

Passes when, for s = 1/2 and 1/4, (L_s - 1) / (s c) is within 1% of 1, and the planted s = 1 gives the truth's L to
1e-12 of it. Reported: the fit L - 1 = c1 s + c2 s^2 through s = 1/2 and 1 and its value at 1/4, and n at each s.

Run: python3 cross.py FOLDER I857FOLDER [--mutate swap], or python3 cross.py --selftest (planted: L - 1 linear in s
passes; one with a part in s^2 of a tenth of c fails; an s = 1 off the truth's L by 1e-9 fails). The control --mutate
swap reads s = 1/2's runs as 1/4's and the reverse, and must FAIL. Exits 1 when a check fails.
"""
import json
import os
import sys

SS = (0.5, 0.25)


def odd_even(pw, moves):
    """(L, n, dev(1), dev(3)) from a power.json with seeds 1 and 3 at one rel, and the seeds' moves"""
    g = {x["seed"]: x for x in pw["groups"] if x["blocks"] == ["Delta"]}
    (r1, d1), = g[1]["devs"]
    (r3, d3), = g[3]["devs"]
    if r1 != r3:
        raise SystemExit(f"cross.py: the seeds' rels differ, {r1} and {r3}")
    m = moves[1] + moves[3]
    return abs(d1 - d3) / m, abs(d1 + d3) / m, d1, d3


def check(L, n, Lt):
    """L, n: by s (1/2, 1/4, 1); Lt: the truth's L"""
    c = Lt - 1
    print(f"cross: the truth's L {Lt:.10f}, c = L - 1 {c:+.6e}")
    checks = []
    for s in sorted(L, reverse=True):
        print(f"  s {s:g}: L {L[s]:.10f}, L - 1 {L[s] - 1:+.6e}, s c {s * c:+.6e}, (L - 1) / (s c) "
              f"{(L[s] - 1) / (s * c):.6f}, n {n[s]:.6e}")
    for s in SS:
        r = (L[s] - 1) / (s * c)
        checks.append((f"linear s {s:g}", abs(r - 1) <= 0.01, f"(L - 1) / (s c) {r:.6f} (within 0.01 of 1)"))
    checks.append(("planted s 1", abs(L[1.0] / Lt - 1) <= 1e-12,
                   f"L {L[1.0]!r} against the truth's {Lt!r}: {L[1.0] / Lt - 1:+.3e} (|.| <= 1e-12)"))
    y1, yh = L[1.0] - 1, L[0.5] - 1
    c2 = 2 * (y1 - 2 * yh)
    c1 = y1 - c2
    yq = c1 / 4 + c2 / 16
    print(f"  fit through s 1/2 and 1: L - 1 = c1 s + c2 s^2, c1 {c1:+.6e}, c2 {c2:+.6e} (c2 / c1 {c2 / c1:+.3e}); "
          f"at s 1/4 {yq:+.6e}, measured {L[0.25] - 1:+.6e}, {(L[0.25] - 1) / yq - 1:+.3e} of it")
    for name, ok, what in checks:
        print(f"  check {name}: {what}: {'pass' if ok else 'FAIL'}")
    return all(c[1] for c in checks)


def planted(c, c2, d1):
    """L - 1 = (c - c2) s + c2 s^2 with an even part q, through odd_even; s 1 off by d1"""
    q, m, L, n = 1.1027e-89, 1.6866e-85, {}, {}
    for s in SS + (1.0,):
        y = (c - c2) * s + c2 * s * s + (d1 if s == 1.0 else 0.0)
        pw = dict(groups=[dict(blocks=["Delta"], seed=1, devs=[[1e-85, m * (1 + y) + q]]),
                          dict(blocks=["Delta"], seed=3, devs=[[1e-85, -m * (1 + y) + q]])])
        L[s], n[s] = odd_even(pw, {1: m, 3: m})[:2]
    return L, n, 1 + c


def load(d, s):
    js = json.load(open(os.path.join(d, f"dl_D240_s{s:g}.json")))
    moves = {r["seed"]: r["move"] for r in js["runs"] if r["seed"] is not None and not r["control"]}
    return odd_even(json.load(open(os.path.join(d, f"p_s{s:g}.json"))), moves)


argv = sys.argv[1:]
if argv[0] == "--selftest":
    res = []
    for c2, d1, want in [(0.0, 0.0, True), (8.324447e-03, 0.0, False), (0.0, 1e-9, False)]:
        print(f"planted: c2 {c2:g}, s 1 off by {d1:g} (want {'pass' if want else 'FAIL'})")
        res.append(check(*planted(8.324447e-02, c2, d1)) == want)
    ok = all(res)
    print(f"cross selftest: {'PASS' if ok else 'FAIL'}")
else:
    d, d857 = argv[0], argv[1]
    swap = "--mutate" in argv and argv[argv.index("--mutate") + 1] == "swap"
    print(f"cross {d} {d857}{' --mutate swap' if swap else ''}")
    L, n = {}, {}
    for s in SS + (1.0,):
        L[s], n[s] = load(d, s)[:2]
    if swap:
        L[0.5], L[0.25] = L[0.25], L[0.5]
    t = os.path.join(d857, "truth")
    mv = {}
    for k, f in ((1, "dl_D240_r85.json"), (3, "dl_D240_r85_s3.json")):
        js = json.load(open(os.path.join(t, f)))
        mv[k] = next(r["move"] for r in js["runs"] if r["seed"] == k and not r["control"])
    pw = json.load(open(os.path.join(t, "power_s3.json")))
    g = {x["seed"]: x for x in pw["groups"]}
    pw = dict(groups=[dict(g[1], devs=[[r, v] for r, v in g[1]["devs"] if r == 1e-85]), g[3]])
    ok = check(L, n, odd_even(pw, mv)[0])
    print(f"cross: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)

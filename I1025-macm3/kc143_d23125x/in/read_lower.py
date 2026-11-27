"""#1025 lower_root (dh170): the reading of a k_c 63 hybrid sign scan at one D, laid out as dh370's read_d19.py (blob 13bd4997) with xfkappa's change
finder unchanged (d185_scan_read.changes, blob 7c9d400f). Changed against read_d19.py: lambda keys and prints to three decimals (a 0.005 grid collides at
two), and the ln|det| minimum finder is written here (d18c_read.minima matches 'beside a change' after rounding to two decimals, which mislabels minima on a 0.005
grid): a minimum is an interior point whose ln|det| is below both neighbours', 'beside a change' when its lambda is an endpoint of some change's bracket (1e-9).
Reads every scan_*_p*.jsonl of the folder. Prints the points, the not noise-robust ones, the hybrid signs, the float64 differences, the repeated points (a repeat
must agree in sign, noise signs, float64 sign and ln|det| within 1e-6), every robust change (bracket, orientation as printed, det-linear estimate, estimator range),
changes touching a non-robust point (not counted), ln|det| minima without a sign change, the endpoint signs.
usage: read_lower.py SCAN_DIR LO HI   |   read_lower.py selftest [--mutate=shift|round2]   (exit 0 only if every planted case reads as written)
mutations (each must make the selftest exit 1): shift (the change finder's estimates move by 0.003), round2 (the minimum finder's two-decimal matching)"""
import sys, os, glob, json
import numpy as np
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
D18 = os.environ.get("D18_DIR", os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"] + (["--mutate=shift"] if MUT == "shift" else [])   # d185_scan_read reads its mutation control from argv
sys.path.insert(0, D18)
import d185_scan_read as rd
sg = lambda s: "+" if s > 0 else "-"
K = lambda x: round(x, 4)


def load(files):
    rows = {}
    for f in files:
        for l in open(f):
            if l.strip():
                r = json.loads(l)
                rows.setdefault(K(r["lam"]), []).append(r)
    return rows


def beside(lam, chs):
    if MUT == "round2":
        return round(lam, 2) in {round(v, 2) for c in chs for v in c["br"]}
    return any(abs(lam - v) < 1e-9 for c in chs for v in c["br"])


def minima(W, chs):
    return [dict(lam=W[i]["lam"], depth=min(W[i - 1]["ln"], W[i + 1]["ln"]) - W[i]["ln"], beside=beside(W[i]["lam"], chs))
            for i in range(1, len(W) - 1) if W[i]["ln"] < W[i - 1]["ln"] and W[i]["ln"] < W[i + 1]["ln"]]


def read(rows, lo, hi, out=print):
    W = sorted((v[0] for k, v in rows.items() if lo - 1e-9 <= k <= hi + 1e-9), key=lambda r: r["lam"])
    out(f"points {len(W)} in {lo:.3f}-{hi:.3f}; not noise-robust: {[r['lam'] for r in W if not r['noise_robust']] or 'none'}")
    out("hybrid signs: " + " ".join("%.3f%s" % (r["lam"], sg(r["sign"])) for r in W))
    dis = [(r["lam"], sg(r["sign"]), sg(r["f64_sign"])) for r in W if r["sign"] != r["f64_sign"]]
    out(f"float64 sign differs from the hybrid sign at: {dis or 'none'}")
    rep = []
    for k, v in rows.items():
        for r in v[1:]:
            a = v[0]
            rep.append((k, a["sign"] == r["sign"] and a["noise"] == r["noise"] and a["f64_sign"] == r["f64_sign"] and abs(a["ln"] - r["ln"]) <= 1e-6))
    out(f"repeated points: {[(k, 'agree' if a else 'DISAGREE') for k, a in rep] or 'none'}")
    rob, non = rd.changes(W)
    by = {K(r["lam"]): r for r in W}
    for c in rob:
        o = f"{sg(by[K(c['br'][0])]['sign'])} to {sg(by[K(c['br'][1])]['sign'])}"
        out(f"  robust change ({c['br'][0]:.3f}, {c['br'][1]:.3f}), {o}, det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
    out(f"robust changes: {len(rob)}; touching a non-robust point (not counted): {[c['br'] for c in non] or 'none'}")
    free = [m for m in minima(W, rob + non) if not m["beside"]]
    out(f"ln|det| local minima without a sign change: {[(round(m['lam'], 3), round(m['depth'], 4)) for m in free] or 'none'}")
    out(f"endpoint signs: {sg(W[0]['sign'])} at {W[0]['lam']:.3f}, {sg(W[-1]['sign'])} at {W[-1]['lam']:.3f}")
    return dict(rob=rob, non=non, rep=rep, dis=dis, free=free)


def selftest():
    def rows(grid, f, nr=()):
        return {K(l): [dict(lam=l, sign=1.0 if f(l) > 0 else -1.0, ln=float(np.log(abs(f(l)))), noise=[1.0, 1.0], noise_robust=(l not in nr), f64_sign=1.0)]
                for l in grid}
    q = lambda s: None
    ga = [round(1.20 + 0.02 * i, 2) for i in range(18)]
    gb = [round(1.47 + 0.005 * i, 3) for i in range(17)]
    ok = []
    a = 1.2865                                                      # case 1, lane A's grid: one planted root, det nearly linear through it
    r1 = read(rows(ga, lambda l: (l - a) * (1 + 0.5 * (l - 1.4))), 1.20, 1.54, q)
    ok.append(len(r1["rob"]) == 1 and r1["rob"][0]["br"] == (1.28, 1.3) and abs(r1["rob"][0]["lin"] - a) < 5e-4 and not r1["free"])
    a1, a2 = 1.4954, 1.5293                                         # case 2, lane B's grid: two planted roots 0.034 apart
    f2 = lambda l: (l - a1) * (l - a2) * 40 * (1 + 0.3 * (l - 1.5))
    r2 = read(rows(gb, f2), 1.47, 1.55, q)
    ok.append(len(r2["rob"]) == 2 and [c["br"] for c in r2["rob"]] == [(1.495, 1.5), (1.525, 1.53)]
              and abs(r2["rob"][0]["lin"] - a1) < 1e-3 and abs(r2["rob"][1]["lin"] - a2) < 1e-3 and not r2["free"])
    r3 = read(rows(gb, f2, nr=(1.5,)), 1.47, 1.55, q)               # case 3: a non-robust point at a change leaves it uncounted
    ok.append(len(r3["rob"]) == 1 and len(r3["non"]) == 1)
    f4 = lambda l: (l - 1.4975) * ((l - 1.505) ** 2 + 2e-7)         # case 4: a change in (1.495, 1.500) and a deep minimum WITHOUT a change at 1.505,
    r4 = read(rows(gb, f4), 1.47, 1.55, q)                          # whose two-decimal rounding equals the change's endpoints' (1.5)
    ok.append(len(r4["rob"]) == 1 and r4["rob"][0]["br"] == (1.495, 1.5) and [round(m["lam"], 3) for m in r4["free"]] == [1.505])
    f5 = lambda l: (l - 1.505) ** 2 + 1e-5                          # case 5: no change, one minimum without a change
    r5 = read(rows(gb, f5), 1.47, 1.55, q)
    ok.append(len(r5["rob"]) == 0 and [round(m["lam"], 3) for m in r5["free"]] == [1.505])
    rr = rows(ga, lambda l: (l - a) * (1 + 0.5 * (l - 1.4)))        # case 6: a repeat that agrees, then one that does not
    rr[1.3].append(dict(rr[1.3][0])); r6 = read(rr, 1.20, 1.54, q)
    rr[1.3][1]["ln"] += 1e-3; r7 = read(rr, 1.20, 1.54, q)
    ok.append(r6["rep"] == [(1.3, True)] and r7["rep"] == [(1.3, False)])
    print(f"planted: lane A grid root {a} -> {r1['rob'][0]['lin'] if r1['rob'] else None}; lane B grid roots {a1}, {a2} -> {[round(c['lin'], 5) for c in r2['rob']]}; "
          f"non-robust control robust {len(r3['rob'])} non {len(r3['non'])}; minimum beside/without: {[round(m['lam'], 3) for m in r4['free']]}, {[round(m['lam'], 3) for m in r5['free']]}; "
          f"repeat agree/disagree {r6['rep']} {r7['rep']}")
    return all(ok), ok


if args and args[0] == "selftest":
    good, ok = selftest()
    print("selftest", "passes" if good else f"FAILS (cases {ok})")
    sys.exit(0 if good else 1)
d, lo, hi = args[0], float(args[1]), float(args[2])
read(load(sorted(glob.glob(os.path.join(d, "scan_*_p*.jsonl")))), lo, hi)

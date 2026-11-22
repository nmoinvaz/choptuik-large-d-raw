"""#1025 dh370: the reading of the k_c 63 hybrid sign scan at one D, with xfkappa's change finder and minima finder unchanged
(d185_scan_read.changes, d18c_read.minima; blobs 7c9d400f and the one in raw I1025-mac/d18). Reads every scan_*_p*.jsonl of the scan folder,
and the timing run's file as repeat points: a repeated lambda must agree in sign. Prints the signs, each robust change (bracket, orientation,
det-linear estimate, estimator range), changes that touch a non-robust point, ln|det| minima without a sign change, and the points where
the float64 sign differs from the hybrid one.
usage: read_d19.py SCAN_DIR LO HI [REPEAT.jsonl,...]    |    read_d19.py selftest [--mutate=shift]"""
import sys, os, glob, json
import numpy as np
MUTSHIFT = "--mutate=shift" in sys.argv
D18 = os.environ.get("D18_DIR", "/home/nathan/Source/choptuik-large-d-raw-push960/I1025-mac/d18")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"] + (["--mutate=shift"] if MUTSHIFT else [])   # the modules read their mutation control from argv
sys.path.insert(0, D18)
import d185_scan_read as rd
import d18c_read as rc
sg = lambda s: "+" if s > 0 else "-"


def load(files):
    rows = {}
    for f in files:
        for l in open(f):
            if l.strip():
                r = json.loads(l)
                rows.setdefault(round(r["lam"], 2), []).append(r)
    return rows


def read(rows, lo, hi, repeats=(), out=print):
    W = sorted((v[0] for k, v in rows.items() if lo - 1e-9 <= k <= hi + 1e-9), key=lambda r: r["lam"])
    out(f"points {len(W)} in {lo:.2f}-{hi:.2f}; not noise-robust: {[r['lam'] for r in W if not r['noise_robust']] or 'none'}")
    out("hybrid signs: " + " ".join("%.2f%s" % (r["lam"], sg(r["sign"])) for r in W))
    dis = [(r["lam"], sg(r["sign"]), sg(r["f64_sign"])) for r in W if r["sign"] != r["f64_sign"]]
    out(f"float64 sign differs from the hybrid sign at: {dis or 'none'}")
    rep = []
    for k, v in rows.items():
        for r in v[1:]:
            rep.append((k, r["sign"] == v[0]["sign"]))
    for f in repeats:
        for k, v in load([f]).items():
            if k in rows:
                rep.append((k, v[0]["sign"] == rows[k][0]["sign"]))
    out(f"repeated points: {[(k, 'agree' if a else 'DISAGREE') for k, a in rep] or 'none'}")
    rob, non = rd.changes(W)
    by = {round(r["lam"], 2): r for r in W}
    for c in rob:
        o = f"{sg(by[round(c['br'][0], 2)]['sign'])} to {sg(by[round(c['br'][1], 2)]['sign'])}"
        out(f"  robust change ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {o}, det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
    out(f"robust changes: {len(rob)}; touching a non-robust point (not counted): {[c['br'] for c in non] or 'none'}")
    free = [m for m in rc.minima(W, rob + non) if not m["beside"]]
    out(f"ln|det| local minima without a sign change: {[(round(m['lam'], 2), round(m['depth'], 4)) for m in free] or 'none'}")
    return dict(rob=rob, non=non, rep=rep, dis=dis)


def selftest():
    a = 1.5337                                      # planted root, det linear through it
    lam = [round(1.40 + 0.01 * i, 2) for i in range(21)]
    mk = lambda l, nr=True: dict(lam=l, sign=1.0 if (l - a) * (1 + 0.5 * (l - 1.5)) > 0 else -1.0,
                                 ln=float(np.log(abs((l - a) * (1 + 0.5 * (l - 1.5))))), noise_robust=nr, f64_sign=1.0, sec=1)
    rows = {l: [mk(l)] for l in lam}
    res = read(rows, 1.40, 1.60, out=lambda s: None)
    ok = len(res["rob"]) == 1 and abs(res["rob"][0]["lin"] - a) < 5e-4 and res["rob"][0]["br"] == (1.53, 1.54)
    rows[1.54] = [mk(1.54, nr=False)]               # control: a non-robust point at the change must leave it uncounted
    res2 = read(rows, 1.40, 1.60, out=lambda s: None)
    ok2 = len(res2["rob"]) == 0 and len(res2["non"]) == 1
    print(f"planted root {a}: found {res['rob'][0]['lin'] if res['rob'] else None}; non-robust control: robust {len(res2['rob'])}, non {len(res2['non'])}")
    return ok and ok2


if args and args[0] == "selftest":
    ok = selftest()
    print("selftest", "passes" if ok else "FAILS")
    sys.exit(0 if ok else 1)
d, lo, hi = args[0], float(args[1]), float(args[2])
read(load(sorted(glob.glob(os.path.join(d, "scan_*_p*.jsonl")))), lo, hi, args[3].split(",") if len(args) > 3 else ())

"""#1025 (m) (d18_criteria.log): k_c-stability of the k_c 63 roots at one D. Each k_c 63 robust change in [LO, HI] against the nearest
robust k_c 55 change (det-linear estimates, d185_scan_read.changes): within TOL (0.01) the root there is k_c-stable, else k_c-dependent;
a k_c 55 change touching a non-robust point gives no reading; unmatched k_c 55 changes are listed. Every ln|det| local minimum without a
sign change, in either scan, gets a dip fit (information): over the minimum and up to two points each side,
ln|det| = c + s (lambda - lambda_min) + ln|(lambda - a)^2 + beta|; beta > 0 a complex pair a +- i sqrt(beta), beta < 0 two real roots.
usage: d18k2_read.py D LO HI KC55_SCAN(,...) KC63_SCAN(,...)   |   d18k2_read.py selftest [--mutate=tol|dip]"""
import sys, os, json
import numpy as np
from scipy.optimize import least_squares
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18c_read as rc
import d18d_read as dr
TOL = 0.03 if MUT == "tol" else 0.01                      # control: a tolerance three times the coordinator's
sg = lambda s: "+" if s > 0 else "-"


def dipfit(W, i):
    P = W[max(0, i - 2):i + 3]
    x = np.array([r["lam"] for r in P]); y = np.array([r["ln"] for r in P]); x0 = W[i]["lam"]
    model = lambda p: p[0] + p[1] * (x - x0) + np.log(np.abs((x - p[2]) ** 2 + (abs(p[3]) if MUT == "dip" else p[3])) + 1e-300)
    best = None
    for b0 in (1e-6, 1e-5, 1e-4, -1e-6, -1e-5, -1e-4):     # starts on both sides: a complex pair or a real pair
        for a0 in (x0 - 0.004, x0, x0 + 0.004):
            p0 = [y.min() - np.log(abs(b0)), 0.0, a0, b0]
            try:
                f = least_squares(lambda p: model(p) - y, p0, method="lm", max_nfev=4000)
            except Exception:
                continue
            if best is None or f.cost < best.cost:
                best = f
    a, beta = best.x[2], (abs(best.x[3]) if MUT == "dip" else best.x[3])
    rms = float(np.sqrt(np.mean((model(best.x) - y) ** 2)))
    kind = f"complex pair {a:.6f} +- {np.sqrt(beta):.6f} i" if beta > 0 else f"two real roots {a - np.sqrt(-beta):.6f}, {a + np.sqrt(-beta):.6f}"
    return dict(lam=x0, a=float(a), beta=float(beta), kind=kind, rms=rms, n=len(P))


def scan(S, lo, hi, name, out):
    W = [r for r in S if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    rob, non = rd.changes(W)
    by = {round(r["lam"], 2): r for r in W}
    o = lambda c: f"{sg(by[round(c['br'][0], 2)]['sign'])} to {sg(by[round(c['br'][1], 2)]['sign'])}"
    out(f"{name}: {len(W)} points {W[0]['lam']:.2f}-{W[-1]['lam']:.2f}; not noise-robust: {[r['lam'] for r in W if not r['noise_robust']] or 'none'}")
    out(f"{name} signs: " + " ".join("%.2f%s" % (r["lam"], sg(r["sign"])) for r in W))
    for c in rob:
        out(f"  {name}: ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {o(c)} in its own state, det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
    free = [m for m in rc.minima(W, rob + non) if not m["beside"]]
    fits = []
    for m in free:
        i = next(k for k, r in enumerate(W) if abs(r["lam"] - m["lam"]) < 1e-9)
        d = dipfit(W, i); fits.append(d)
        out(f"  {name}: ln|det| minimum without a sign change at {m['lam']:.2f} (depth {m['depth']:.4f}); dip fit over {d['n']} points: "
            f"a {d['a']:.6f}, beta {d['beta']:+.3e}, {d['kind']}, rms {d['rms']:.1e}")
    if not free:
        out(f"  {name}: ln|det| minima without a sign change: none")
    return rob, [c["br"] for c in non], fits


def read(S55, rep55, S63, lo, hi, out=print):
    r55, n55, f55 = scan(S55, lo, hi, "k_c 55", out)
    r63, _, f63 = scan(S63, lo, hi, "k_c 63", out)
    out(f"k_c 55 repeated points: {[(k, 'agree' if a else 'DISAGREE') for k, a, _ in rep55] or 'none'}")
    if any(not a for _, a, _ in rep55):
        out("STOP-level: a repeated point disagrees; no reading"); return dict(v="repeat disagrees", fits=f55 + f63)
    if n55:
        out(f"no reading: a k_c 55 change touches a non-robust point {n55}; the coordinator rules"); return dict(v="coordinator", fits=f55 + f63)
    if not r63:
        out("no reading: k_c 63 has no robust change in the window; the coordinator rules"); return dict(v="coordinator", fits=f55 + f63)
    vs, used = [], set()
    for a in r63:
        cand = sorted((abs(b["lin"] - a["lin"]), j) for j, b in enumerate(r55) if j not in used)
        if cand and cand[0][0] <= TOL + 1e-12:
            used.add(cand[0][1]); b = r55[cand[0][1]]
            out(f"reading: the k_c 63 root {a['lin']:.6f} has a k_c 55 root at {b['lin']:.6f} ({b['lin'] - a['lin']:+.6f}, within {TOL:g}): k_c-stable there")
            vs.append("stable")
        else:
            near = f"; nearest k_c 55 change {cand[0][0]:.6f} away" if cand else "; no k_c 55 change in the window"
            out(f"reading: the k_c 63 root {a['lin']:.6f} has no k_c 55 root within {TOL:g}{near}: k_c-dependent at this D")
            vs.append("dependent")
    un = [round(b["lin"], 6) for j, b in enumerate(r55) if j not in used]
    out(f"unmatched k_c 55 changes: {un or 'none'}")
    return dict(v=vs[0] if len(set(vs)) == 1 else "mixed", fits=f55 + f63)


def selftest():
    q = lambda *a: None
    g = [round(1.65 + 0.01 * i, 2) for i in range(26)]
    def cplx(roots, pairs):                              # planted ln|det| with real roots and complex pairs (a, b)
        return [dict(r, D=18.125) for r in rc.planted(g, roots, pairs)]
    S63, _ = dr.merge(cplx((1.7720,), ()))
    ok = []
    def case(name, rows, want, check=lambda r: True):
        r = read(*dr.merge(rows), S63, 1.65, 1.90, q)
        good = r["v"] == want and check(r); ok.append(good); print(f"planted: {name}: {'PASS' if good else 'FAIL'} (read {r['v']})")
    case("k_c 55 root at 1.7750: stable", cplx((1.7750,), ()), "stable")
    case("k_c 55 root at 1.7950 (0.023 off): dependent", cplx((1.7950,), ()), "dependent")
    case("no k_c 55 root, a complex pair 1.8023 +- 0.004 i: dependent, the dip fit reads complex near it",
         cplx((1.6712,), ((1.8023, 0.004),)), "dependent",
         lambda r: any(f["beta"] > 0 and abs(f["a"] - 1.8023) < 2e-3 and abs(np.sqrt(f["beta"]) - 0.004) < 2e-3 for f in r["fits"]))
    case("a real pair 1.8012 and 1.8038 inside (1.80, 1.81): the dip fit reads two real roots",
         cplx((1.6712, 1.8012, 1.8038), ()), "dependent",
         lambda r: any(f["beta"] < 0 and abs(f["a"] - 1.8025) < 2e-3 for f in r["fits"]))
    A = cplx((1.7750,), ()); A[12] = dict(A[12], noise_robust=False)    # 1.77, beside the change in (1.77, 1.78)
    case("a non-robust point beside the k_c 55 change: no reading", A, "coordinator")
    print(f"selftest: {'PASS' if all(ok) else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    D, lo, hi = float(args[0]), float(args[1]), float(args[2])
    L = lambda fs: [r for f in fs.split(",") for r in map(json.loads, open(f)) if r["D"] == D]
    R55, R63 = L(args[3]), L(args[4])
    assert R55 and R63 and all(r["kc"] == 55 for r in R55) and all(r["kc"] == 63 for r in R63), "k_c labels are not 55 and 63"
    S55, rep55 = dr.merge(R55); S63, _ = dr.merge(R63)
    print(f"D {D:g}: k_c 55 {len(R55)} records, k_c 63 {len(R63)} records")
    read(S55, rep55, S63, lo, hi)
    W = [r for r in S55 if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    fc = [(a["lam"], b["lam"]) for a, b in zip(W, W[1:]) if a["f64_sign"] != b["f64_sign"]]
    print(f"k_c 55 float64: sign changes {fc or 'none'}; differs from the hybrid at {sum(r['f64_sign'] != r['sign'] for r in W)} of {len(W)} points")

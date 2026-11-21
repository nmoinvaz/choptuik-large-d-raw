"""#1025 (k) (d18_criteria.log): k_c-stability at one D. The k_c 55 scan's robust changes in [LO, HI] against the k_c 63 roots from the
reference scans (same merge and change finder). Stable: exactly two robust changes at k_c 55, each k_c 63 root matched to a distinct
one with det-linear estimates within TOL (0.01); otherwise dependent; a change touching a non-robust point: no reading. Orientations
are listed in each state's own signs only (no sign convention across k_c).
usage: d18k_read.py D LO HI KC55_SCAN(,...) KC63_SCANS(,...)   |   d18k_read.py selftest [--mutate=tol]"""
import sys, os, json
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
sys.argv = [sys.argv[0], "x"]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import d185_scan_read as rd
import d18c_read as rc
import d18d_read as dr
TOL = 0.02 if MUT == "tol" else 0.01                      # control: a tolerance twice the coordinator's
sg = lambda s: "+" if s > 0 else "-"


def ch(S, lo, hi):
    rob, non = rd.changes(S)
    by = {round(r["lam"], 2): r for r in S}
    inw = lambda c: c["br"][0] >= lo - 1e-9 and c["br"][1] <= hi + 1e-9
    o = lambda c: f"{sg(by[round(c['br'][0], 2)]['sign'])} to {sg(by[round(c['br'][1], 2)]['sign'])}"
    return [dict(c, orient=o(c)) for c in rob if inw(c)], [c["br"] for c in non if inw(c)]


def read(S55, rep55, S63, lo, hi, out=print):
    r55, n55 = ch(S55, lo, hi); r63, _ = ch(S63, lo, hi)
    W = [r for r in S55 if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    out(f"k_c 55: {len(W)} points in {lo:.2f}-{hi:.2f}; not noise-robust: {[r['lam'] for r in W if not r['noise_robust']] or 'none'}")
    out("k_c 55 signs: " + " ".join("%.2f%s" % (r["lam"], sg(r["sign"])) for r in W))
    out(f"k_c 55 repeated points: {[(k, 'agree' if a else 'DISAGREE') for k, a, _ in rep55] or 'none'}")
    for name, cs in (("k_c 63", r63), ("k_c 55", r55)):
        for c in cs:
            out(f"  {name}: ({c['br'][0]:.2f}, {c['br'][1]:.2f}), {c['orient']} in its own state, det-linear {c['lin']:.6f}, range [{c['lo']:.6f}, {c['hi']:.6f}]")
    out(f"k_c 55 robust changes: {len(r55)}; touching a non-robust point: {n55 or 'none'}")
    free = [m for m in rc.minima(W, r55) if not m["beside"]]
    out(f"k_c 55 ln|det| local minima without a sign change: {[(round(m['lam'], 2), round(m['depth'], 4)) for m in free] or 'none'}")
    if any(not a for _, a, _ in rep55):
        out("STOP-level: a repeated point disagrees; no reading"); return dict(v="repeat disagrees")
    if n55:
        out("no reading: a change touches a non-robust point; the coordinator rules"); return dict(v="coordinator")
    used, pairs = set(), []
    for a in r63:
        cand = sorted((abs(b["lin"] - a["lin"]), j) for j, b in enumerate(r55) if j not in used)
        if cand and cand[0][0] <= TOL + 1e-12:
            j = cand[0][1]; used.add(j); b = r55[j]
            pairs.append((a, b))
            out(f"  matched: k_c 63 {a['lin']:.6f} and k_c 55 {b['lin']:.6f}: det-linear distance {b['lin'] - a['lin']:+.6f}; ranges "
                f"{max(0.0, max(a['lo'], b['lo']) - min(a['hi'], b['hi'])):.6f} to {max(a['hi'], b['hi']) - min(a['lo'], b['lo']):.6f} apart")
        else:
            out(f"  k_c 63 root {a['lin']:.6f}: no k_c 55 change within {TOL:g}" + (f" (nearest {cand[0][0]:.6f})" if cand else ""))
    if len(r55) == 2 and len(r63) == 2 and len(pairs) == 2:
        out(f"reading: k_c-stable at this D: both changes within {TOL:g}"); return dict(v="stable", pairs=pairs)
    out(f"reading: k_c-dependent at this D: {len(r55)} robust k_c 55 changes, {len(pairs)} of {len(r63)} k_c 63 roots matched within {TOL:g}")
    return dict(v="dependent", pairs=pairs)


def selftest():
    q = lambda *a: None
    g = [round(1.65 + 0.01 * i, 2) for i in range(26)]
    T = lambda roots: rc.planted(g, roots)
    S63, _ = dr.merge(T((1.6990, 1.8675)))
    cases = [("k_c 55 at 1.6995 and 1.8650: stable", (1.6995, 1.8650), "stable"),
             ("k_c 55 at 1.6995 and 1.8810 (0.0135 off): dependent", (1.6995, 1.8810), "dependent"),
             ("k_c 55 one root only: dependent", (1.6995,), "dependent"),
             ("k_c 55 three roots: dependent", (1.6995, 1.7612, 1.8650), "dependent")]
    ok = []
    for name, roots, want in cases:
        S55, rep = dr.merge(T(roots))
        r = read(S55, rep, S63, 1.65, 1.90, q)
        ok.append(r["v"] == want); print(f"planted: {name}: {'PASS' if ok[-1] else 'FAIL'} (read {r['v']})")
    A = T((1.6995, 1.8650)); A[5] = dict(A[5], noise_robust=False)          # 1.70, beside the change in (1.69, 1.70)
    r = read(*dr.merge(A), S63, 1.65, 1.90, q)
    ok.append(r["v"] == "coordinator"); print(f"planted: a non-robust point beside a change: no reading: {'PASS' if ok[-1] else 'FAIL'} (read {r['v']})")
    print(f"selftest: {'PASS' if all(ok) else 'FAIL'}{f' [mutate {MUT}]' if MUT else ''}")
    return 0 if all(ok) else 1


if __name__ == "__main__":
    if args[0] == "selftest":
        sys.exit(selftest())
    D, lo, hi = float(args[0]), float(args[1]), float(args[2])
    L = lambda fs: [r for f in fs.split(",") for r in map(json.loads, open(f)) if r["D"] == D]
    R55, R63 = L(args[3]), L(args[4])
    assert all(r["kc"] == 55 for r in R55) and all(r["kc"] == 63 for r in R63), "k_c labels are not 55 and 63"
    S55, rep55 = dr.merge(R55); S63, _ = dr.merge(R63)
    print(f"D {D:g}: k_c 55 {len(R55)} records, k_c 63 {len(R63)} records")
    read(S55, rep55, S63, lo, hi)
    W = [r for r in S55 if lo - 1e-9 <= r["lam"] <= hi + 1e-9]
    fc = [(a["lam"], b["lam"]) for a, b in zip(W, W[1:]) if a["f64_sign"] != b["f64_sign"]]
    print(f"k_c 55 float64: sign changes {fc or 'none'}; differs from the hybrid at {sum(r['f64_sign'] != r['sign'] for r in W)} of {len(W)} points")

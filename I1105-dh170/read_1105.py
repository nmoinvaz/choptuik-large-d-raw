"""#1105 step 1: reads i1105_u0.py's JSON (u0 x N sweep of the last block's residual of one stored l = 1 state) and prints the
table and t5's four readings (README.md): N, horizon RK (hz2), shape in u0, bands.

usage: read_1105.py JSON
       read_1105.py selftest [--mutate=ref]    planted cases; exit 0 only if each reads as written

dF_last is the NORM of the change of the last block against u0 0.04 at the same N (the sign is not stored), so the shape fit is of magnitudes:
  (a) neighbour slopes d ln|dF| / d ln u0 between 0.02 and 0.03 and between 0.05 and 0.06, and the least-squares log-log slope over the four points;
      equal to p only if e(0.04) is negligible (dF = e(u0) - e(0.04));
  (b) dF = |c| |u0^p - 0.04^p| over u0 in {0.02, 0.03, 0.05, 0.06}, p by a scan on [-2, 45] in steps of 0.005, ln|c| the mean of the log residuals at each p;
      the printed rms is of ln|dF| (a fit of 4 points with 2 parameters: an estimator value, not an error bar).
Both assume the error vector is e(u0) = c(u0) v with a fixed v (parallel vectors)."""
import json
import math
import sys

REF = 0.04
FIT = (0.02, 0.03, 0.05, 0.06)
MUTATE = ""


def fit_b(pts, ref=None):
    """pts: [(u0, dF)], dF > 0 -> (p, rms of ln|dF| residual)"""
    ref = REF if ref is None else ref
    best = None
    n = int(round((45 + 2) / 0.005))
    for i in range(n + 1):
        p = -2 + 0.005 * i
        if abs(p) < 1e-9:
            continue
        try:
            r = [math.log(d) - math.log(abs(u ** p - ref ** p)) for u, d in pts]
        except (ValueError, OverflowError):
            continue
        m = sum(r) / len(r)
        sse = sum((x - m) ** 2 for x in r)
        if best is None or sse < best[1]:
            best = (p, sse)
    return best[0], math.sqrt(best[1] / len(pts))


def slope(a, b):
    (u1, d1), (u2, d2) = a, b
    return math.log(d2 / d1) / math.log(u2 / u1)


def llslope(pts):
    xs = [math.log(u) for u, _ in pts]
    ys = [math.log(d) for _, d in pts]
    mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)


def shape(rows):
    """rows: {u0: dF} at one N -> dict"""
    pts = [(u, rows[u]) for u in FIT if u in rows and rows[u] > 0]
    if len(pts) < 4:
        return None
    p, rms = fit_b(pts)
    return dict(p=p, rms=rms, lo=slope(pts[0], pts[1]), hi=slope(pts[2], pts[3]), ll=llslope(pts))


def main(path):
    R = json.load(open(path))
    sw = R["sweep"]
    Ns = sorted({r["N"] for r in sw})
    u0s = sorted({r["u0"] for r in sw})
    get = {(r["N"], round(r["u0"], 6)): r for r in sw}
    print(f"{R['state']}: D {R['D']}, k_c {R['kc']}, N_record {R['N_record']}, record-system |F| {R['F']:.6e}, last block {R['F_last']:.6e}, "
          f"steps {R['steps']} (horizon {R['h_steps_record']}), sanity {R['sanity']}\n")
    print("| N | u0 | horizon steps | \\|F\\| | \\|F_last\\| | dF_last | band 0-10 | 11-50 | 51-100 | 101+ | seconds |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for N in Ns:
        for u in u0s:
            r = get[(N, round(u, 6))]
            b = r["dF_last_bands"]
            print(f"| {N} | {u:.3f} | {r['h_steps']} | {r['F']:.3e} | {r['F_last']:.3e} | {r['dF_last']:.3e} | "
                  f"{b[0]:.1e} | {b[1]:.1e} | {b[2]:.1e} | {b[3]:.1e} | {r['sec']} |")
    print("\nThe reference at u0 0.04 (|F_last| per N): " + ", ".join(f"N {N}: {get[(N, 0.04)]['F_last']:.3e}" for N in Ns))
    print("dF_last at a given N is a difference against that N's reference; where the reference's own last-block residual is large against dF, "
          "the difference is not the u0 effect alone.")
    print("\nExtra runs (N_record, u0 0.02):")
    for k, v in R["extra"].items():
        print(f"- {k}: horizon steps {v['h_steps']}, |F_last| {v['F_last']:.3e}, dF_last {v['dF_last']:.3e} (against the record system), bands "
              + " ".join(f"{x:.1e}" for x in v["dF_last_bands"]))
    print("\n## Readings")
    N0 = R["N_record"]
    d = {N: get[(N, 0.02)]["dF_last"] for N in Ns}
    print("- N: dF_last at u0 0.02: " + ", ".join(f"N {N}: {d[N]:.3e}" for N in Ns))
    if 816 in d and 1088 in d:
        ch = abs(d[1088] - d[816]) / d[816]
        print(f"  change 816 -> 1088 = {ch:.1%}: " + ("below 20%: that limit is the u0 effect proper, and the part that falls with N is aliasing"
                                                      if ch < 0.2 else "20% or more: not settled by N 816 -> 1088"))
    h = R["extra"].get("hz2")
    if h:
        ch = abs(h["dF_last"] - d[N0]) / d[N0]
        print(f"- Horizon RK: hz2 dF_last {h['dF_last']:.3e} against the sweep's {d[N0]:.3e} at u0 0.02, N {N0}: change {ch:.1%}: "
              + ("below 10%: the horizon segment's RK is not the cause" if ch < 0.1 else "10% or more: the horizon RK is a cause"))
    k = R["extra"].get("Ks45")
    if k:
        ch = abs(k["dF_last"] - d[N0]) / d[N0]
        print(f"- Series cut: Ks45 dF_last {k['dF_last']:.3e} against {d[N0]:.3e}: change {ch:.1%}")
    print("- Shape in u0 (points u0 0.02, 0.03, 0.05, 0.06; the reference 0.04 has dF = 0):")
    for N in Ns:
        s = shape({u: get[(N, round(u, 6))]["dF_last"] for u in u0s})
        if s:
            print(f"  N {N}: (a) slope 0.02-0.03 {s['lo']:+.2f}, slope 0.05-0.06 {s['hi']:+.2f}, log-log fit {s['ll']:+.2f}; (b) p = {s['p']:.3f} (rms of ln|dF| {s['rms']:.2f})")
    print("- Bands (norm by tau harmonic, 0-10, 11-50, 51-100, 101+):")
    for N in Ns:
        for u in (0.02, 0.06):
            b = get[(N, u)]["dF_last_bands"]
            print(f"  N {N} u0 {u}: " + " ".join(f"{x:.2e}" for x in b) + f"; largest: band {['0-10', '11-50', '51-100', '101+'][b.index(max(b))]}")
    return 0 if R.get("sanity") else 1


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)
    for p in (0.5, 4.5, 30.0):
        ref_used = 0.05 if MUTATE == "ref" else REF             # the mutation plants with another reference than the fit assumes
        pts = [(u, 3.7 * abs(u ** p - ref_used ** p)) for u in FIT]
        got, rms = fit_b(pts)
        chk(f"planted p = {p}: (b) recovers p to 1e-2 (got {got:.3f}, rms {rms:.1e})", abs(got - p) < 1e-2 and rms < 1e-6)
    # the naive slope is not p on the low side for p = 30 (dF flat below the reference): the reason for (b)
    pts = [(u, abs(u ** 30 - REF ** 30)) for u in FIT]
    chk("p = 30: the neighbour slope 0.02-0.03 is about 0, not 30", abs(slope(pts[0], pts[1])) < 0.1)
    chk("p = 30: the neighbour slope 0.05-0.06 is far above 4", slope(pts[2], pts[3]) > 10)
    # a planted JSON through main(): N rule and hz2 rule read as written
    import io
    import contextlib
    import os
    import tempfile
    def planted(chN, hz):
        sw = []
        for N, d02 in ((408, 2.0e-8), (816, 1.4e-8), (1088, 1.4e-8 * (1 + chN))):
            for u in (0.01, 0.015, 0.02, 0.03, 0.04, 0.05, 0.06):
                dF = 0.0 if u == 0.04 else (d02 if u == 0.02 else 1e-9 * u)
                sw.append(dict(u0=u, N=N, h_steps=1000, F=1e-9, F_last=1e-9, dF_last=dF, dF_last_bands=[dF, 0, 0, 0], sec=1))
        return dict(state="plant", D=23.0, kc=135, N_record=408, steps=1, h_steps_record=1, F=1e-9, F_last=1e-9, sweep=sw,
                    extra={"hz2": dict(h_steps=2, F_last=1e-9, dF_last=2.0e-8 * (1 + hz), dF_last_bands=[0, 0, 0, 0]),
                           "Ks45": dict(h_steps=1, F_last=1e-9, dF_last=2.0e-8, dF_last_bands=[0, 0, 0, 0])}, sanity=True)
    for chN, hz, wantN, wantH in ((0.1, 0.05, "below 20%", "below 10%"), (0.3, 0.2, "20% or more", "10% or more")):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(planted(chN, hz), f); f.close()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            main(f.name)
        os.unlink(f.name)
        t = buf.getvalue()
        chk(f"planted N change {chN:.0%}: reads '{wantN}'", wantN in t)
        chk(f"planted hz2 change {hz:.0%}: reads '{wantH}'", wantH in t)
    print("selftest:", "FAIL " + "; ".join(bad) if bad else "all cases read as written")
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--mutate="):
            MUTATE = a.split("=", 1)[1]
    if not args:
        sys.exit(__doc__)
    sys.exit(selftest() if args[0] == "selftest" else main(args[0]))

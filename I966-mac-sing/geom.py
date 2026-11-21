"""#966 diagnostic, outside the criteria: the root-test radius of Delta's series at each base of legs 10, 13 and 14
(261.1415 once, as leg 14's) against the distance from the base to the nearer of two fixed pairs, P1 and P2, each the
median over the bases of locate's stable pole nearest to it (within 0.05). If those two pairs are the nearest
singularities, the root test follows min(|D0 - P1|, |D0 - P2|)."""
import json, statistics, sys
R = []
for f in sys.argv[1:]:
    R += json.load(open(f))
R = sorted({round(r["D0"], 4): r for r in R}.values(), key=lambda r: r["D0"])   # later files win: leg 14's 261.1415
def med(ref):
    pts = [min((p for p in r["pade"] if abs(p["D_re"] - ref[0]) <= 0.05 and abs(p["D_im"] - ref[1]) <= 0.05),
               key=lambda p: abs(complex(p["D_re"], p["D_im"]) - complex(*ref)), default=None) for r in R]
    pts = [p for p in pts if p]
    return complex(statistics.median(p["D_re"] for p in pts), statistics.median(p["D_im"] for p in pts)), len(pts)
(P1, n1), (P2, n2) = med((262.078, 0.973)), med((258.36, 2.269))
print(f"P1 {P1.real:.4f} +- {P1.imag:.4f}i (median of {n1} bases), P2 {P2.real:.4f} +- {P2.imag:.4f}i (median of {n2})")
worst = 0
for r in R:
    d1, d2 = abs(P1 - r["D0"]), abs(P2 - r["D0"])
    d = min(d1, d2)
    e = r["root_radius"] / d - 1
    worst = max(worst, abs(e))
    print(f"D0 {r['D0']:.4f}: root test {r['root_radius']:.4f}, |D0 - P1| {d1:.4f}, |D0 - P2| {d2:.4f}, nearer "
          f"{'P1' if d1 < d2 else 'P2'}: root/distance - 1 {e:+.2%}")
print(f"{len(R)} bases; largest |root/distance - 1| {worst:.2%}")

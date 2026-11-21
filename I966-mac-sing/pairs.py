"""#966: the locate reading, as fixed in the README before the run. Per base (leg 13 then leg 14 in order of D; the
shared base 261.1415 once, as leg 14's), the nearest stable Pade pole with D_im > 0.05, its D_re, D_im, |s| against the
root-test radius; then the ranges over every run of three or more consecutive bases. Controls, each must exit 1:
--mutate=drift adds 0.03 i to D_re at the i-th base (any three consecutive bases then span 0.06 > 0.05); --mutate=root
scales the root-test radius by 1.1 (|s| then misses it by about 9%). The first form of the control, which shifted the
last base alone, could not fail while the other seven held; it was replaced after its first run."""
import json, sys
mut = next((a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")), None)
L13, L14 = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
rows = [r for r in L13 if abs(r["D0"] - 261.1415) > 1e-3] + L14
rows.sort(key=lambda r: r["D0"])
pts = []
for i, r in enumerate(rows):
    p = next((q for q in r["pade"] if q["D_im"] > 0.05), None)
    if p and mut == "drift":
        p = dict(p, D_re=p["D_re"] + 0.03 * i)
    root = r["root_radius"] * (1.1 if mut == "root" else 1.0)
    ok = p is not None and abs(p["abs"] / root - 1) <= 0.05
    pts.append((r["D0"], p, r["root_radius"], ok))
    print(f"D0 {r['D0']:.4f}: " + (f"D* {p['D_re']:.4f} +- {p['D_im']:.4f}i, |s| {p['abs']:.4f}, arg {p['arg_deg']:.1f}, n {p['n']}, "
          f"spread {p['spread']:.1e}; root test {root:.4f}, |s|/root - 1 {p['abs'] / root - 1:+.2%}"
          if p else "no stable pole off the axis") + f" -> {'match' if ok else 'no match'}")
best = None
for a in range(len(pts)):
    for b in range(a + 3, len(pts) + 1):
        run = pts[a:b]
        if not all(x[3] for x in run):
            continue
        re = [x[1]["D_re"] for x in run]; im = [x[1]["D_im"] for x in run]
        good = max(re) - min(re) <= 0.05 and max(im) - min(im) <= 0.05
        if good and (best is None or b - a > best[1] - best[0]):
            best = (a, b, max(re) - min(re), max(im) - min(im))
whole = [x for x in pts if x[3]]
if whole:
    re = [x[1]["D_re"] for x in whole]; im = [x[1]["D_im"] for x in whole]
    print(f"all {len(whole)} matching bases: D_re {min(re):.4f} to {max(re):.4f} (range {max(re) - min(re):.4f}), "
          f"D_im {min(im):.4f} to {max(im):.4f} (range {max(im) - min(im):.4f})")
if best:
    a, b, dr, di = best
    print(f"longest stable run: D0 {pts[a][0]:.4f} to {pts[b - 1][0]:.4f}, {b - a} bases, ranges D_re {dr:.4f}, D_im {di:.4f}: "
          f"pair CONFIRMED{f' (--mutate={mut})' if mut else ''}")
else:
    print(f"no run of three or more bases meets the reading: pair not confirmed{f' (--mutate={mut})' if mut else ''}")
sys.exit(0 if best else 1)

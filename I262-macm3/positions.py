"""I262-macm3: the circles at the D 61.03 M 40 zero positions of #231 for kf 21, 23 and 25, tabulated per zero.    python3 positions.py"""
import re
circ = re.compile(r"circle \|lam - \(([-+0-9.]+) ([-+0-9.]+)i\)\| = ([0-9.]+): winding of det M ([-+0-9.]+),.*?verification mismatches (\d+)(?:.*?)(?:; zeros inside ([-+0-9.]+) ([-+0-9.]+)i \(estimate ([0-9.e+-]+)\))?$")
names = {"(2.04259, 1.15073)": "(a) 2.0426 + 1.1507 i", "(2.7626, 0.6308)": "(b) 2.7626 + 0.6308 i", "(2.9141, 1.5885)": "(c) 2.9141 + 1.5885 i", "(0.0319, 3.0855)": "(d) 0.0319 + 3.0855 i",
         "(2.043533, 0.0)": "lam_phys control"}
res = {}
for kf, path in ((21, "kf21/circles.log"), (23, "kf23/circles.log"), (25, "kf25/circles.log")):
    for ln in open(path):
        m = circ.search(ln.rstrip())
        if m:
            cr, ci, R, w, mm, zr, zi, est = m.groups()
            key = f"({float(cr):g}, {float(ci):g})"
            res.setdefault(key, {})[kf] = (int(round(float(w))), f"{float(zr):+.4f} {float(zi):+.4f}i" if zr else "-", est)
print("| M 40 zero of #231 (kf 23) | kf 21 | kf 23 | kf 25 |\n|---|---|---|---|")
for key, row in res.items():
    cells = []
    for kf in (21, 23, 25):
        c = row.get(kf)
        cells.append("not run (#231: +1)" if c is None else f"winding {c[0]:+d}, {c[1]}" + (f" ({c[2]})" if c[2] else ""))
    print(f"| {names.get(key, key)} | " + " | ".join(cells) + " |")

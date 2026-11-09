"""I238-macm3: the circles' zero positions (modecount_circle.py logs) beside the moment positions, as a table.    python3 positions.py"""
import json, re

circ = re.compile(r"circle \|lam - \(([-+0-9.]+) ([-+0-9.]+)i\)\| = ([0-9.]+): winding of det M ([-+0-9.]+),.*?verification mismatches (\d+)(?:; zeros inside ([-+0-9.]+) ([-+0-9.]+)i \(estimate ([0-9.e+-]+)\))?")
print("| D | circle centre | R | winding | mismatches | zero inside | estimate |\n|---|---|---|---|---|---|---|")
for D, logs in (("54.04", ["D54/circles.log"]), ("55.04", ["D55/circles.log", "D55/circles_U0.log"])):
    for lg in logs:
        for ln in open(lg):
            m = circ.search(ln)
            if m:
                cr, ci, R, w, mm, zr, zi, est = m.groups()
                zero = f"{float(zr):+.6f} {float(zi):+.6f}i" if zr else "-"
                print(f"| {D} | {float(cr):+.5f} {float(ci):+.5f}i | {R} | {float(w):+.0f} | {mm} | {zero} | {est or '-'} |")
print()
print("moments (spread is an estimator range): ")
for name, f, box in (("D 54.04 auto", "D54/moments.json", "B0"), ("D 54.04 auto", "D54/moments.json", "U0"), ("D 55.04 auto", "D55/moments.json", "B0"), ("D 55.04 auto", "D55/moments.json", "U"),
                     ("D 55.04 fixed", "D55fixed/moments.json", "B1a"), ("D 55.04 fixed", "D55fixed/moments_U0_U.json", "U0"), ("D 55.04 fixed", "D55fixed/moments_U0_U.json", "U"),
                     ("D 54.04 fixed", "D54fixed/moments.json", "B0"), ("D 54.04 fixed", "D54fixed/moments.json", "U0")):
    recs = [json.loads(l) for l in open(f) if l.strip()]
    for r in recs:
        if r.get("box") == box:
            print(name, box, "ok" if r.get("ok") else "NOT LOCATED", r.get("roots") or r.get("why"), "spread", r.get("spread"))

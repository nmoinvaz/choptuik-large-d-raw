"""#966 leg 10: is the pair of legs 13 and 14 (262.078 +- 0.973i) seen from before the crossing (260.85)? Reading
fixed in the README before the run.
    python pairs10.py LOCATE_LEG10.json [--mutate=plant|move]
Per base, the stable poles of locate (the four it keeps) with D_im > 0.05; the same pair is one within 0.05 of the
reference in D_re and in D_im. Exit 0 when it is seen at three or more consecutive bases; 2 when no base shows it
(appears past 260.85), and also when a pole off the axis, stable to 0.05 over three or more consecutive bases, sits more
than 0.05 from it (moved); 3 otherwise (undecided). --mutate=plant adds the reference pole to every base (must give
0); --mutate=move moves the reference by 0.1 in D_re (must give nonzero when the plain run gives 0)."""
import json
import sys

TOL, REF = 0.05, (262.078, 0.973)
mut = next((a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")), None)
ref = (REF[0] + 0.1, REF[1]) if mut == "move" else REF
rows = sorted(json.load(open(sys.argv[1])), key=lambda r: r["D0"])
seen = []
offaxis = []
for r in rows:
    ps = [p for p in r["pade"] if p["D_im"] > 0.05]
    if mut == "plant":
        ps = ps + [dict(D_re=REF[0], D_im=REF[1], n=0, abs=float("nan"), arg_deg=float("nan"))]
    hit = [p for p in ps if abs(p["D_re"] - ref[0]) <= TOL and abs(p["D_im"] - ref[1]) <= TOL]
    seen.append(bool(hit))
    offaxis.append(ps)
    print(f"D0 {r['D0']:.4f}: root test {r['root_radius']:.4f}; poles off the axis "
          + ("; ".join(f"{p['D_re']:.4f} +- {p['D_im']:.4f}i (n {p['n']})" for p in ps) or "none")
          + f" -> {'the pair' if hit else 'not the pair'}")


def longest(flags):
    best = cur = 0
    for f in flags:
        cur = cur + 1 if f else 0
        best = max(best, cur)
    return best


run = longest(seen)
# a stable pole off the axis elsewhere: a chain of poles, one per base, each within 0.05 of the first, over 3+ bases
moved = None
for i in range(len(rows)):
    for p in offaxis[i]:
        if abs(p["D_re"] - ref[0]) <= TOL and abs(p["D_im"] - ref[1]) <= TOL:
            continue
        j = i + 1
        while j < len(rows) and any(abs(q["D_re"] - p["D_re"]) <= TOL and abs(q["D_im"] - p["D_im"]) <= TOL
                                    for q in offaxis[j]):
            j += 1
        if j - i >= 3 and (moved is None or j - i > moved[2]):
            moved = (p["D_re"], p["D_im"], j - i, rows[i]["D0"], rows[j - 1]["D0"])
if moved:
    print(f"stable pole off the axis away from the pair: {moved[0]:.4f} +- {moved[1]:.4f}i over {moved[2]} bases "
          f"({moved[3]:.4f} to {moved[4]:.4f})")
code = 0 if run >= 3 else 2 if not any(seen) else 3
kind = {0: "SEEN before the crossing: it does not come from the crossing",
        2: "NOT SEEN before the crossing: it appears" + (" (or moved; see the stable pole above)" if moved else "")
           + " only past 260.85, tied to the crossing",
        3: "UNDECIDED: the pair at one or two bases only"}[code]
print(f"the pair {ref[0]:.3f} +- {ref[1]:.3f}i at {sum(seen)} of {len(rows)} bases, longest consecutive run {run}: {kind}"
      + (f" (--mutate={mut})" if mut else ""))
sys.exit(code)

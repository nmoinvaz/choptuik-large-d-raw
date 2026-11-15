"""I852-mac tables: Newton's contraction of an m_h, a_h move at D 240.1244, from the runs' JSONs.

e_k = max|z_k - u_k| / max|z_h| (u_k the unperturbed path's k-th iterate), e_0 = move / max|z_h|. The gain e_1 / e_0
is the first step's factor on the move. The excess at the largest rel, (gain(largest) - gain(smallest)) / largest rel,
is the part of e_1 / rel^2 beyond a gain linear in rel, from max norms (not a fit by component); #840's quadratic part
read max|dz| / rel^2 7.5565e92 at rel 1e-65..1e-67 (I840-mac/tables.md). C5 sets the unperturbed path's own step
max|u_k - u_(k-1)| / max|z_h| against each rel.

Run: python3 tables.py [folder], default the folder of this script. Writes tables.md beside it.
"""
import json
import os
import sys

d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
out = ["# I852-mac tables (tables.py)", ""]


def es(r, zh):
    return [r["move"] / zh] + [h["e_pair"] for h in r["hist"]]


st = json.load(open(os.path.join(d, "steps_D240.json")))
zh = st["zh"]
u = next(r for r in st["runs"] if r["run"] == "unperturbed")
seeds = [r for r in st["runs"] if r["run"] != "unperturbed"]
rels = sorted({r["rel"] for r in seeds}, reverse=True)
out += [f"max|z_h| {zh:.10g}; {len(u['hist'])} steps", "",
        "## The unperturbed path (C5)", "",
        "| k | max\\|u_k − u_(k−1)\\| / max\\|z_h\\| | max\\|F\\| before | "
        + " | ".join(f"below {x:.0e}" for x in rels) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in rels) + " |"]
for h in u["hist"]:
    out.append(f"| {h['k']} | {h['dz_rel']:.4e} | {h['F_before']:.4e} | "
               + " | ".join("yes" if h["dz_rel"] < x else "no" for x in rels) + " |")
out += ["", f"max|F| at u_{len(u['hist'])}: {u['F_end']:.4e}", "",
        "## The perturbed paths (C4)", "",
        "| run | e_0 | " + " | ".join(f"e_{h['k']}" for h in u["hist"]) + " | gain e_1 / e_0 | reading |",
        "| --- | --- | " + " | ".join("---" for _ in u["hist"]) + " | --- | --- |"]
gain = {}
for r in seeds:
    e = es(r, zh)
    gain[r["rel"]] = e[1] / e[0]
    out.append(f"| {r['run']} | " + " | ".join(f"{x:.4e}" for x in e) + f" | {e[1] / e[0]:.4e} | "
               + ("contracts" if r["contracts"] else "does NOT contract") + " |")
hi, lo = rels[0], rels[-1]
out += ["", f"excess at rel {hi:.0e}: (gain({hi:.0e}) - gain({lo:.0e})) / {hi:.0e} = {(gain[hi] - gain[lo]) / hi:.4e}"]
late = [h["e_pair"] for r in seeds for h in r["hist"] if h["k"] >= 2]
out += [f"e_k at k >= 2 over all rels: {min(late):.4e} .. {max(late):.4e}; the unperturbed step at k = "
        f"{u['hist'][-1]['k']}: {u['hist'][-1]['dz_rel']:.4e}", "", "## The controls (C2, C3)", "",
        "| run | e_0 | e_1 | e_2 | reading |", "| --- | --- | --- | --- | --- |"]
for name in ("ctl_nostep_D240", "ctl_centre_D240"):
    js = json.load(open(os.path.join(d, name + ".json")))
    for r in js["runs"]:
        if r["run"] != "unperturbed":
            out.append(f"| {name}: {r['run']} | " + " | ".join(f"{x:.4e}" for x in es(r, js["zh"])) + " | "
                       + ("contracts" if r["contracts"] else "does NOT contract") + " |")
txt = "\n".join(out)
open(os.path.join(d, "tables.md"), "w").write(txt + "\n")
print(txt)

"""I875-mac tables: Newton's contraction of an m_h, a_h move at D 240.1244 from #874's root, beside #852's.

e_k = max|z_k - u_k| / max|z_h| (u_k the unperturbed path's k-th iterate), e_0 = move / max|z_h|, gain e_1 / e_0, as
in I852-mac/tables.py. e_1 / e_0^2 is the first step's quadratic part where e_1 is above the floor; #852's excess was
7.5556e92 (I852-mac/tables.md). C4 sets the unperturbed path's own steps max|u_k - u_(k-1)| / max|z_h| against each
rel. The last table sets each rel's gain from #874's state beside #852's from the stored truth
(I852-mac/steps_D240.json).

Run: python3 tables.py [folder [I852 folder]], default the folder of this script and ../I852-mac. Writes tables.md
beside it.
"""
import json
import os
import sys

d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
d852 = sys.argv[2] if len(sys.argv) > 2 else os.path.join(d, "..", "I852-mac")
out = ["# I875-mac tables (tables.py)", ""]


def es(r, zh):
    return [r["move"] / zh] + [h["e_pair"] for h in r["hist"]]


def gains(js):
    return {r["rel"]: es(r, js["zh"])[1] / es(r, js["zh"])[0] for r in js["runs"] if r["run"] != "unperturbed"}


st = json.load(open(os.path.join(d, "steps_u2.json")))
zh = st["zh"]
u = next(r for r in st["runs"] if r["run"] == "unperturbed")
seeds = sorted((r for r in st["runs"] if r["run"] != "unperturbed"), key=lambda r: -r["rel"])
rels = [r["rel"] for r in seeds]
out += [f"{st['state']}: max|z_h| {zh:.10g}; {len(u['hist'])} steps", "",
        "## The unperturbed path (C4)", "",
        "| k | max\\|u_k − u_(k−1)\\| / max\\|z_h\\| | max\\|F\\| before | "
        + " | ".join(f"below {x:.0e}" for x in rels) + " |",
        "| --- | --- | --- | " + " | ".join("---" for _ in rels) + " |"]
for h in u["hist"]:
    out.append(f"| {h['k']} | {h['dz_rel']:.4e} | {h['F_before']:.4e} | "
               + " | ".join("yes" if h["dz_rel"] < x else "no" for x in rels) + " |")
out += ["", f"max|F| at u_{len(u['hist'])}: {u['F_end']:.4e}", "",
        "## The perturbed paths (C3)", "",
        "| run | e_0 | " + " | ".join(f"e_{h['k']}" for h in u["hist"]) + " | gain e_1 / e_0 | e_1 / e_0² | reading |",
        "| --- | --- | " + " | ".join("---" for _ in u["hist"]) + " | --- | --- | --- |"]
for r in seeds:
    e = es(r, zh)
    out.append(f"| {r['run']} | " + " | ".join(f"{x:.4e}" for x in e) + f" | {e[1] / e[0]:.4e} | "
               f"{e[1] / e[0] ** 2:.4e} | " + ("contracts" if r["contracts"] else "does NOT contract") + " |")
g2 = gains(st)
s852 = json.load(open(os.path.join(d852, "steps_D240.json")))
g1 = gains(s852)
out += ["", "## The gain from the two starts", "", f"#852: {s852['state']}; #875: {st['state']}", "",
        "| rel | gain, #852 (stored truth) | gain, #875 (u2) | #852 less #875 | #852 / #875 |",
        "| --- | --- | --- | --- | --- |"]
for rl in rels:
    if rl in g1:
        out.append(f"| {rl:.0e} | {g1[rl]:.4e} | {g2[rl]:.4e} | {g1[rl] - g2[rl]:+.4e} | {g1[rl] / g2[rl]:.4e} |")
txt = "\n".join(out)
open(os.path.join(d, "tables.md"), "w").write(txt + "\n")
print(txt)

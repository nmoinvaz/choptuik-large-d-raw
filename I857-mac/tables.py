"""I857-mac tables: the Delta move's return at D 240.1244 from the two starts, and the cross term.

Reads each start's power_s3.json (seed 1 at rel 1e-83..1e-85 and seed 3 at 1e-85, dev = dDelta(seed) -
dDelta(unperturbed) from eight parts) and its dl_D240_r<k>.json (the moves and the unperturbed step). At rel 1e-85 the
seeds' Delta signs are opposite, so the odd part L = |dev(1) - dev(3)| / (2 move) is the part of dev that flips with
the move and the even part n = |dev(1) + dev(3)| / (2 move) the part that does not. The cross term (C5) is the truth's
|dev| / move less u2's at each rel, and the truth's L less u2's; "per unit step" divides it by the truth's
max|d0| / max|z_h| (max norms, a scale, not a fitted coefficient). The last line sets u2's n against #850's quadratic
q = dev / rel^2 at rel 1e-67 (I850-mac/power.json), 18 orders above.

Run: python3 tables.py [folder [I850 folder]], default the folder of this script and ../I850-mac. Writes tables.md
beside it.
"""
import json
import math
import os
import sys

d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
out = ["# I857-mac tables (tables.py)", ""]
starts = {}
for t in ("truth", "u2"):
    pw = json.load(open(os.path.join(d, t, "power_s3.json")))
    g = {x["seed"]: x for x in pw["groups"] if x["blocks"] == ["Delta"]}
    mv, un = {}, None
    for k in ("83", "84", "85", "85_s3"):
        js = json.load(open(os.path.join(d, t, f"dl_D240_r{k}.json")))
        u = next(r for r in js["runs"] if r["run"] == "unperturbed")
        r = next(r for r in js["runs"] if r["seed"] is not None and not r["control"])
        mv[(r["seed"], js["rel"])] = r["move"]
        un = un or dict(state=js["state"], dD=u["dDelta"], d0=u["dz"] / js["zh"], zh=js["zh"])
    rel = min(rl for rl, _ in g[1]["devs"])
    d1, d3 = dict(g[1]["devs"])[rel], dict(g[3]["devs"])[rel]
    m2 = mv[(1, rel)] + mv[(3, rel)]
    starts[t] = dict(un=un, g1=g[1], mv=mv, rel=rel, L=abs(d1 - d3) / m2, n=abs(d1 + d3) / m2, d1=d1, d3=d3,
                     ratio={rl: abs(v) / mv[(1, rl)] for rl, v in g[1]["devs"]})

out += ["## The starts", "", "| start | state | unperturbed dΔ | max\\|d0\\| / max\\|z_h\\| |",
        "| --- | --- | --- | --- |"]
for t, s in starts.items():
    out.append(f"| {t} | {s['un']['state']} | {s['un']['dD']:.10e} | {s['un']['d0']:.4e} |")
out += ["", "## Seed 1 at each rel", "", "| start | rel | move | dev | \\|dev\\| / move |",
        "| --- | --- | --- | --- | --- |"]
for t, s in starts.items():
    for rl, v in sorted(s["g1"]["devs"], key=lambda x: -x[0]):
        out.append(f"| {t} | {rl:.0e} | {s['mv'][(1, rl)]:.6e} | {v:+.6e} | {s['ratio'][rl]:.6f} |")
out += ["", "## Odd and even parts at the smallest rel (seeds 1 and 3)", "",
        "| start | rel | p | dev(1) | dev(3) | odd L | L − 1 | even n |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |"]
for t, s in starts.items():
    ps = ", ".join(f"{p:.4f}" for p in s["g1"]["p"])
    out.append(f"| {t} | {s['rel']:.0e} | {ps} | {s['d1']:+.10e} | {s['d3']:+.10e} | {s['L']:.10f} | "
               f"{s['L'] - 1:+.4e} | {s['n']:.6e} |")
T, U = starts["truth"], starts["u2"]
diff = {rl: T["ratio"][rl] - U["ratio"][rl] for rl in T["ratio"]}
dl = T["L"] - U["L"]
out += ["", "## The cross term (C5): truth less u2", "", "| rel | \\|dev\\| / move, truth | u2 | difference |",
        "| --- | --- | --- | --- |"]
for rl in sorted(diff, reverse=True):
    out.append(f"| {rl:.0e} | {T['ratio'][rl]:.6f} | {U['ratio'][rl]:.6f} | {diff[rl]:+.6e} |")
sp = max(diff.values()) - min(diff.values())
out += ["", f"difference over the rels: {min(diff.values()):+.6e} .. {max(diff.values()):+.6e}, spread over rels "
        f"{sp:.3e}",
        f"odd part L at {T['rel']:.0e}: truth {T['L']:.10f}, u2 {U['L']:.10f}, difference {dl:+.6e}",
        f"even part n at {T['rel']:.0e}: truth {T['n']:.6e}, u2 {U['n']:.6e}, difference {T['n'] - U['n']:+.3e}",
        f"per unit step: L's difference / (truth's max|d0| / max|z_h| {T['un']['d0']:.4e}) = "
        f"{dl / T['un']['d0']:.4e}"]
# #850's quadratic: q = dev / rel^2 at its smallest rel (I850-mac/power.json, the truth, rel 1e-65..1e-67)
p850 = os.path.join(sys.argv[2] if len(sys.argv) > 2 else os.path.join(d, "..", "I850-mac"), "power.json")
g850 = next(x for x in json.load(open(p850))["groups"] if x["D_str"].startswith("240.1") and x["blocks"] == ["Delta"])
r850, v850 = min(g850["devs"], key=lambda x: x[0])
q = v850 / (r850 * r850)
pred = q * U["rel"] ** 2 / U["mv"][(1, U["rel"])]
out += [f"#850's quadratic: q = dev / rel^2 at rel {r850:.0e} {q:.6e}; its n at {U['rel']:.0e}, q rel^2 / move, "
        f"{pred:.6e}; u2's n less it {U['n'] - pred:+.3e} ({U['n'] / pred - 1:+.2e} of it)"]
# dev = q r^2 (1 + c r): p(10 r, r) = 2 + log10((1 + 10 c r) / (1 + c r)), so c r = (p - 2) ln 10 / 9 to first order
cr = (g850["p"][-1] - 2) * math.log(10) / 9
eps = 2.0 ** -53 * (abs(U["d1"]) + abs(U["d3"])) / abs(U["d1"] + U["d3"])
out += [f"#850's cubic at rel {r850:.0e} from its last p {g850['p'][-1]!r}: c rel {cr:+.4e}; u2's n less "
        f"q / (1 + c rel)'s n, as a part of it: {U['n'] / (pred / (1 + cr)) - 1:+.2e}; the rounding of n from the "
        f"stored doubles dev(1), dev(3) is at most {eps:.1e} of it (a bound)"]
txt = "\n".join(out)
open(os.path.join(d, "tables.md"), "w").write(txt + "\n")
print(txt)

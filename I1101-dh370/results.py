"""#1101 follow-up: the table of the four evaluations (two states x lambda 0.045, 0.050), the det-linear root from each state's two points, their difference (the root's solve scatter)
and |Delta_B - Delta_A| from the records. Reads scan_A/, scan_B/ and the two records; prints markdown. The det-linear root is the zero of the straight line through f = sign * exp(ln|det| - ref),
ref the larger of the two ln|det|, between the two lambda; defined only when the two hybrid signs differ."""
import json, math, re, sys
O = "/home/nathan/Source/choptuik-large-d-raw-wt613/I1101-dh370"
REC = {"A": O + "/inputs/A/l1kc127wind23.jsonl", "B": O + "/inputs/B/l1kc127k070w2.jsonl"}
LAMS = (0.045, 0.050)
def rows(x):
    r = {}
    for l in open(f"{O}/scan_{x}/scan_D23.0_p0.jsonl"):
        if l.strip():
            w = json.loads(l); r[round(w["lam"], 6)] = w
    return r
def lin(r1, r2):
    if r1["sign"] == r2["sign"]:
        return None
    ref = max(r1["ln"], r2["ln"])
    f1 = r1["sign"] * math.exp(r1["ln"] - ref); f2 = r2["sign"] * math.exp(r2["ln"] - ref)
    return r1["lam"] + (r2["lam"] - r1["lam"]) * f1 / (f1 - f2)
root = {}; ok = True
print("| state | lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\\|det\\| | seconds |")
print("|---|---|---|---|---|---|---|---|---|")
for x in "AB":
    R = rows(x)
    for lam in LAMS:
        w = R[round(lam, 6)]
        ok = ok and bool(w["noise_robust"]) and bool(w.get("robust"))
        print(f"| {x} | {lam:.3f} | {w['sign']:+.0f} | {w['noise_robust']} | {w.get('robust')} | {w['dln']:.2e} | {w['f64_sign']:+.0f} | {w['ln']:.10f} | {w['sec']} |")
    root[x] = lin(R[round(LAMS[0], 6)], R[round(LAMS[1], 6)])
print()
for x in "AB":
    print(f"- state {x}: det-linear root from the two points: {root[x] if root[x] is None else format(root[x], '.9f')}" + ("" if root[x] is not None else " (the two hybrid signs are equal: no root between the points)"))
if root["A"] is not None and root["B"] is not None:
    d = root["B"] - root["A"]
    print(f"- **root scatter, root_B - root_A = {d:+.3e}** (|.| = {abs(d):.3e})")
    print(f"- against t5's reading: below 1e-4 {'YES' if abs(d) < 1e-4 else 'no'}; above 1e-3 {'YES' if abs(d) > 1e-3 else 'no'}; between {'YES' if 1e-4 <= abs(d) <= 1e-3 else 'no'}")
a = json.loads(open(REC["A"]).read().strip().splitlines()[-1]); b = json.loads(open(REC["B"]).read().strip().splitlines()[-1])
print(f"- Delta_A {a['Delta']!r}, Delta_B {b['Delta']!r}, **|Delta_B - Delta_A| = {abs(b['Delta'] - a['Delta']):.4e}**; |F| A {a['F']:.6e}, B {b['F']:.6e}; steps {a['steps']}, {b['steps']}; psi-constraint {a['constraint']:.6e}, {b['constraint']:.6e}")
print(f"- all four points noise-robust and robust: {ok}")

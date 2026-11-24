#!/usr/bin/env python3
"""#1025 kc87_d21 (dh610) summarize_kc87d21.py [--mutate] | selftest [--mutate]: the regrid and the scan of k_c 87 at D 21.0 beside win2's k_c 79 leg record and the k_c 79 scan of the same D (../kc79_leg/D21.0), from regrid/, scan/, in/, read_lower.txt,
exits_kc87_d21.txt. No number is typed by hand beyond the registered bars. usage (from this folder): python3 -I summarize_kc87d21.py > summary_kc87d21.txt
Control: the two-point det-linear formula on the k_c 79 rows at 0.905 and 0.910 must give that scan's reader value (in/k79_read_lower_D21.0.txt, 0.909538) within 1e-5, else exit 1 and no table is trusted; --mutate flips the sign of the
exponent, which must make the control fail (exit 1, "control FIRED"). selftest: the formula on planted rows with a known root (ln|det| linear in lambda across a sign change: root recovered to 1e-12); --mutate (sign flip) must fail it (exit 1)."""
import json, glob, math, re, statistics, sys, datetime

mut = "--mutate" in sys.argv


def root(a, b, flip=False):
    sgn = -1 if flip else 1
    return a["lam"] + (b["lam"] - a["lam"]) / (1 + math.exp(sgn * (b["ln"] - a["ln"])))


def selftest(flip):
    # |det| = |c (lam - r)| near the root: ln|det| = ln|c| + ln|lam - r|; rows at r -+ d1, r + d2 give the det-linear estimate of r in the limit of the linear model
    r, c = 0.9095, 7.0
    ok = True
    for d1, d2 in ((0.002, 0.003), (0.0025, 0.0025), (0.001, 0.004)):
        a = dict(lam=r - d1, ln=math.log(c * d1)); b = dict(lam=r + d2, ln=math.log(c * d2))
        got = root(a, b, flip)
        good = abs(got - r) < 1e-12
        ok &= good
        print(f"  planted root {r}, rows at -{d1} and +{d2}: {got:.12f} ({'ok' if good else 'WRONG'})")
    print("selftest" + (" --mutate" if flip else ""), "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__" and sys.argv[1:2] == ["selftest"]:
    sys.exit(selftest("--mutate" in sys.argv))

rd = lambda f: [json.loads(l) for l in open(f) if l.strip()]
r87 = rd("regrid/l1kc87dh610e.jsonl")[-1]
r79 = [x for x in rd("in/l1kc79Lw1025f.jsonl") if abs(x["D"] - 21.0) < 1e-9][-1]
print("| record | k_c 87 (regrid, this machine) | k_c 79 source (win2's leap) | k_c 87 minus k_c 79 |")
print("|---|---|---|---|")
for k in ("F_start", "F", "steps", "constraint", "Delta", "seconds"):
    a, b = r87[k], r79[k]
    print(f"| {k} | {a!r} | {b!r} | {'' if k == 'seconds' else format(a - b, '+.3e')} |")
print(f"| steps ratio | {r87['steps'] / r79['steps']:.4f} | | |")
print()
rows = sorted((x for f in sorted(glob.glob("scan/scan_D21.0_p*.jsonl")) for x in rd(f)), key=lambda x: (x["lam"], x["sec"]))
ref = rd("in/ref_k79_leg_scan_D21.0.jsonl")
sg = lambda v: "+" if v > 0 else "-"
print("| lambda | hybrid sign (k_c 87 mine, k_c 79 leg) | noise signs (robust) | float64 sign | ln of abs det (k_c 87 mine, k_c 79 leg) | seconds |")
print("|---|---|---|---|---|---|")
for x in rows:
    v = next((q for q in ref if abs(q["lam"] - x["lam"]) < 1e-9), None)
    print(f"| {x['lam']:.3f} | {sg(x['sign'])}, {sg(v['sign']) if v else 'n/a'} | {''.join(sg(n) for n in x['noise'])} ({x['noise_robust']}) | {sg(x['f64_sign'])} | {x['ln']:.6f}, {format(v['ln'], '.6f') if v else 'n/a'} | {x['sec']} |")
t = [x["sec"] for x in rows]
print()
print(f"scan points: {len(rows)} evaluations, seconds per point min {min(t)}, median {statistics.median(t):.0f}, max {max(t)}, sum {sum(t)}; outside 1500 to 3500 s: {[(round(x['lam'], 3), x['sec']) for x in rows if not 1500 <= x['sec'] <= 3500]}")
f64 = [round(x["lam"], 3) for x in rows if x["f64_sign"] != x["sign"]]
print(f"float64 sign differs from the hybrid at: {f64 or 'none'}; not noise-robust: {[round(x['lam'], 3) for x in rows if not x['noise_robust']] or 'none'}")
txt79 = open("in/k79_read_lower_D21.0.txt").read()
ref79 = float(re.search(r"det-linear (\d\.\d+)", txt79).group(1))
a, b = (next(q for q in ref if abs(q["lam"] - x) < 1e-9) for x in (0.905, 0.910))
ctl = root(a, b, mut)
okc = abs(ctl - ref79) <= 1e-5
print(f"\ncontrol: the two-point root of the k_c 79 leg rows at 0.905 and 0.910 is {ctl:.6f}; its reader's det-linear is {ref79:.6f}; difference {ctl - ref79:+.2e} (bar 1e-5): {'ok' if okc else 'CONTROL FAILED'}")
txt = open("read_lower.txt").read()
chg = re.findall(r"robust change \((\d\.\d+), (\d\.\d+)\), (.+?), det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]", txt)
print(f"this scan's reader: robust changes {len(chg)}: " + "; ".join(f"({c[0]}, {c[1]}), {c[2]}, det-linear {c[3]}, range [{c[4]}, {c[5]}]" for c in chg))
d = float(chg[0][3]) - ref79 if len(chg) == 1 else None
if d is not None:
    print(f"k_c 87 minus k_c 79 ({ref79}): {d:+.6f}; within 0.002: {abs(d) <= 0.002}; within 0.005: {abs(d) <= 0.005}; within 0.0005: {abs(d) <= 0.0005}")
ex = open("exits_kc87_d21.txt").read()
cs = re.search(r"source check: kc79_syscheck_1025.py exit (\d) .*?--mutate=F exit (\d), --mutate=steps exit (\d) .*?kc87_syscheck_1025.py on it exit (\d)", ex)
ac = re.search(r"acceptance: kc87_syscheck_1025.py exit (\d); controls --mutate=F exit (\d), --mutate=steps exit (\d) .*?kc79_syscheck_1025.py on the result exit (\d)", ex)
wall = re.search(r"ell_refine exit (\d+), wall (\d+) s", ex)
nrec = len(re.findall(r"kc87_d21: p\d: D 21.0 k_c 87: .*: the record system", ex))
pair = re.search(r"pair check of 0.910 .*?exit (\d)", ex)
tm = lambda pat: (lambda m: datetime.datetime.fromisoformat(m[-1]) if m else None)(re.findall(r"== (\S+ \S+) UTC kc87_d21: " + pat, ex))   # the last such line (an earlier dry run writes the first)
t_pins, t_end = tm("pins checked"), tm("scan done")
hrs = (t_end - t_pins).total_seconds() / 3600 if t_pins and t_end else None
print(f"source check exits (kc79 check, controls F, steps, kc87 check): {cs.groups() if cs else None}; acceptance exits (kc87 check, controls F, steps, kc79 check): {ac.groups() if ac else None}; ell_refine {wall.groups() if wall else None}; processes that printed the record system {nrec} of 8; pair check exit {pair[1] if pair else None}; lane {hrs:.2f} h" if hrs else "lane not finished")
ok = lambda c: "right" if c else "WRONG"
sec_ok = all(1500 <= x <= 3500 for x in t)
print("\n| prediction (registered before the run; right = the stated event happened) | result | verdict |")
print("|---|---|---|")
P = [("source accepted by the k_c 79 check (controls 1 1) and refused by the k_c 87 check (92%)", str(cs.groups() if cs else None), bool(cs) and cs.groups() == ("0", "1", "1", "1")),
     ("regrid exit 0 (92%)", str(wall.groups() if wall else None), bool(wall) and wall[1] == "0"),
     ("regrid accepted by the k_c 87 check, controls 1 1, refused by the k_c 79 check (85%)", str(ac.groups() if ac else None), bool(ac) and ac.groups() == ("0", "1", "1", "1")),
     ("steps ratio k_c 87 / k_c 79 between 1.05 and 1.15 (60%)", f"{r87['steps'] / r79['steps']:.4f}", 1.05 <= r87["steps"] / r79["steps"] <= 1.15),
     ("regrid wall 2000 to 4500 s (60%)", str(wall[2] if wall else None), bool(wall) and 2000 <= int(wall[2]) <= 4500),
     ("all 8 scan processes print the record system (90%)", f"{nrec} of 8", nrec == 8),
     ("the repeat of 0.910 agrees (92%)", f"pair check exit {pair[1] if pair else None}", bool(pair) and pair[1] == "0"),
     ("every point noise-robust (85%)", str([round(x['lam'], 3) for x in rows if not x['noise_robust']] or 'none'), all(x["noise_robust"] for x in rows)),
     ("one robust change in the window (80%)", f"{len(chg)}", len(chg) == 1),
     ("the change within 0.002 of 0.909538 (65%)", f"{d:+.6f}" if d is not None else "n/a", d is not None and abs(d) <= 0.002),
     ("within 0.005 (85%)", f"{d:+.6f}" if d is not None else "n/a", d is not None and abs(d) <= 0.005),
     ("within 0.0005 (25%)", f"{d:+.6f}" if d is not None else "n/a", d is not None and abs(d) <= 0.0005),
     ("float64 sign agrees with the hybrid at all 8 evaluations (55%)", str(f64 or "none"), not f64),
     ("scan points 1500 to 3500 s each (65%)", f"{min(t)} to {max(t)}", sec_ok),
     ("the lane ends within 3.0 h of its pins line (65%)", f"{hrs:.2f} h" if hrs else "n/a", hrs is not None and hrs <= 3.0)]
for n, r_, c in P:
    print(f"| {n} | {r_} | {ok(c)} |")
if mut:
    print("mutate: control " + ("FIRED (exit 1)" if not okc else "did NOT fire (exit 3)"))
    sys.exit(1 if not okc else 3)
sys.exit(0 if okc else 1)

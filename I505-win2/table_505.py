#!/usr/bin/env python3
"""#505: tables the Curtis-Reid + Ruiz sigma_1..4 of near_null_eq.py logs against D, their rates ln(sigma(D2)/sigma(D1))/(D2 - D1), and the reading rule's verdict.
usage: python table_505.py LOG [LOG ...]   (logs in increasing D; the D is read from the first line)
       python table_505.py --selftest      (a planted sequence with a known rate must give that rate, and a wrong-rate log must change the verdict)
Reading rule of #505, written before the run: sigma_1 falls by e^0.9 per unit of D (+-0.2): the system's own; by less than e^0.45 per unit: mostly the scale of rows and columns; in between: neither."""
import math, re, sys

BLK = "J, Curtis-Reid + Ruiz ("

def parse(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    m = re.match(r"\S+anm_pin3_D(\S+)\.npz: D (\S+),", lines[0])
    Dtag = m.group(1) if m else "?"
    D = float(Dtag.lstrip("D")) if m else None   # the state file name's D (4 decimals, within 5e-5 of the state's)
    i = next(k for k, ln in enumerate(lines) if ln.strip().startswith(BLK))
    out = []
    j = i + 1
    while j < len(lines) and lines[j].lstrip().startswith("Curtis-Reid + Ruiz sigma_"):
        m = re.match(r"\s+Curtis-Reid \+ Ruiz sigma_(\d) (\S+) \(converged to (\S+)\)", lines[j])
        sc = lines[j + 1].strip()
        zz = lines[j + 2].strip()
        out.append(dict(i=int(m.group(1)), sigma=float(m.group(2)), conv=m.group(3), scaled=sc, z=zz))
        j += 3
    plant = next(ln for ln in lines if "planted, Curtis-Reid + Ruiz:" in ln).strip()
    return dict(D=D, tag=Dtag, sig=out, plant=plant, passed=lines[-1].strip() == "check: pass")

def rate(s1, s2, d1, d2):
    return math.log(s1 / s2) / (d2 - d1)

def verdict(r):
    if abs(r - 0.9) <= 0.2:
        return "the system's own (within e^0.9 +- 0.2 per unit of D)"
    if r < 0.45:
        return "mostly the scale of rows and columns (below e^0.45 per unit of D)"
    return "neither reading (between 0.45 and 0.7, or above 1.1)"

def selftest():
    r = rate(3.0, math.exp(-0.9 * 2.0) * 3.0, 0.0, 2.0)
    ok = abs(r - 0.9) < 1e-12 and verdict(r).startswith("the system's own")
    bad = verdict(rate(1.0, math.exp(-0.2 * 2.0), 0.0, 2.0)).startswith("mostly the scale")
    bad2 = verdict(0.6).startswith("neither")
    print("selftest: ok" if ok and bad and bad2 else f"selftest FAILED: {ok} {bad} {bad2}")
    return 0 if ok and bad and bad2 else 1

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rows = [parse(p) for p in sys.argv[1:]]
    print("| D | sigma_1 | sigma_2 | sigma_3 | sigma_4 | planted check |")
    print("|---|---|---|---|---|---|")
    for r in rows:
        s = {x["i"]: x for x in r["sig"]}
        print(f"| {r['D']:.4f} | " + " | ".join(f"{s[k]['sigma']:.4e}" for k in (1, 2, 3, 4)) + f" | {'pass' if r['passed'] else 'FAIL'} ({r['plant'].split('= ')[-1]}) |")
    print()
    print("| from D to D | ΔD | rate of sigma_1 per unit D | sigma_2 | sigma_3 | sigma_4 |")
    print("|---|---|---|---|---|---|")
    pairs = [(rows[k], rows[k + 1]) for k in range(len(rows) - 1)] + [(rows[0], rows[-1])]
    for a, b in pairs:
        sa = {x["i"]: x["sigma"] for x in a["sig"]}; sb = {x["i"]: x["sigma"] for x in b["sig"]}
        d = b["D"] - a["D"]
        print(f"| {a['D']:.4f} to {b['D']:.4f} | {d:.4f} | " + " | ".join(f"{rate(sa[k], sb[k], a['D'], b['D']):.3f}" for k in (1, 2, 3, 4)) + " |")
    a, b = rows[0], rows[-1]
    sa = {x["i"]: x["sigma"] for x in a["sig"]}; sb = {x["i"]: x["sigma"] for x in b["sig"]}
    r1 = rate(sa[1], sb[1], a["D"], b["D"])
    print(f"\nsigma_1 over the whole range: ratio {sa[1] / sb[1]:.4g}, rate {r1:.3f} per unit of D (e^{r1:.3f}); verdict: {verdict(r1)}")
    print()
    for r in rows:
        print(f"D {r['D']:.4f}:")
        for x in r["sig"]:
            print(f"  sigma_{x['i']} {x['sigma']:.4e} (conv {x['conv']}); {x['scaled']}")
            print(f"    {x['z']}")

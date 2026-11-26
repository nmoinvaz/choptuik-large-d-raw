import re, sys
from mpmath import mp, mpf
mp.dps = 60
L = sys.argv[1]
runs = ["mob_ks800", "mob_ks1000", "mob_a4", "mob_a6", "u_ks706", "u_ks906"]
res = {}
for r in runs:
    txt = open(f"{L}/{r}/rls.log").read().splitlines()
    start = mpf(re.search(r"Delta (1\.\d+),", txt[0])[1])
    steps = []; pend = None; final = start; floor = False
    for l in txt:
        m = re.match(r"\s+h23 outer (\d+): target \|F\| (\S+) -> (\S+), harmonic-23 step (\S+) \(full step's dDelta (\S+)\), lam (\S+), Delta (1\.\d+) \((\S+) s\)", l)
        if m:
            steps.append((int(m[1]), m[4], m[5], mpf(m[7]) - final, m[8])); final = mpf(m[7])
        m = re.match(r"\s+h23 outer (\d+): target \|F\| (\S+), harmonic-23 step (\S+), the step's dDelta (\S+): released", l)
        if m: pend = (int(m[1]), m[3], m[4])
        if "floor" in l: floor = True
    res[r] = dict(start=start, steps=steps, pend=pend, final=final, floor=floor)
    s = res[r]
    print(f"{r}: start {mp.nstr(s['start'],40)}")
    for o, hs, dd, dlt, t in s["steps"]:
        print(f"   o{o} step: harmonic {hs}, logged dDelta {dd}, Delta change by script {mp.nstr(dlt,6)} ({t} s)")
    print(f"   released at o{s['pend'][0]}: harmonic step {s['pend'][1]}, pending dDelta {s['pend'][2]}; floor in log: {s['floor']}")
    print(f"   h23 change (steps) {mp.nstr(s['final']-s['start'],6)}; final {mp.nstr(s['final'],40)}")
u21 = res["u_ks706"]["start"]
for r in runs:
    print(f"{r}: final - u(506) after h21 {mp.nstr(res[r]['final']-u21,6)}")
ref = res["mob_ks800"]["final"]
for r in runs[1:4]:
    print(f"{r} - mob_ks800: {mp.nstr(res[r]['final']-ref,3)}")
print("mob_ks800 final - (u after h21 + u's pending -1.19e-26):", mp.nstr(ref-(u21+mpf('-1.19e-26')),4))

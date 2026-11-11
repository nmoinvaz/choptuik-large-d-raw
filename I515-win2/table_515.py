#!/usr/bin/env python3
"""#515: the first chain against the clean chain at equal D (equilibrated sigma_1..4 of near_null_eq.py logs).
usage: python table_515.py          (run from I515-win2; reads this folder's eq_crawl*.log and the clean chain's logs in ../I510-win2, ../I511-win2, ../I505-win2)
       python table_515.py --selftest   (a planted offset of 0.05 in ln sigma_1 reads as the system's, 0.2 as the chain's)
Rule of #515: the planted check passes at each state; the difference of the two chains' ln sigma_1 at the same D above 0.1 means the scatter is the chain's.
Equal-D pairs: crawlB4 D 228.1312, 229.1312, 230.1312, 231.1312 and crawlB5 D 234.1312, 235.1312 against the clean chain's states at those D; crawlE D 239.8063 against the clean chain interpolated
linearly in ln sigma_1 between D 239.5375 and D 241.1244 (a different, interpolated comparison, flagged as such)."""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "I505-win2"))
from table_505 import parse  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
def sig(r, i): return {x["i"]: x["sigma"] for x in r["sig"]}[i]

PAIRS = [("crawlB4", "D228.1312", "../I510-win2/eq_D228.1312.log"), ("crawlB4", "D229.1312", "../I511-win2/eq_D229.1312.log"),
         ("crawlB4", "D230.1312", "../I511-win2/eq_D230.1312.log"), ("crawlB4", "D231.1312", "../I511-win2/eq_D231.1312.log"),
         ("crawlB5", "D234.1312", "../I511-win2/eq_D234.1312.log"), ("crawlB5", "D235.1312", "../I510-win2/eq_D235.1312.log")]

def compare(first, clean, label):
    return dict(label=label, D=first["D"], fp=first["passed"], cp=clean["passed"], d=[math.log(sig(first, i)) - math.log(sig(clean, i)) for i in (1, 2, 3, 4)],
                lf=math.log(sig(first, 1)), lc=math.log(sig(clean, 1)))

def verdict(maxdiff): return "the chain's (above 0.1)" if maxdiff > 0.1 else "the system's (0.1 or below)"

def selftest():
    f = lambda off: dict(D=1.0, passed=True, sig=[dict(i=k, sigma=math.exp(-10 * k + off)) for k in (1, 2, 3, 4)])
    c = dict(D=1.0, passed=True, sig=[dict(i=k, sigma=math.exp(-10 * k)) for k in (1, 2, 3, 4)])
    a = compare(f(0.05), c, "t")["d"][0]
    b = compare(f(0.2), c, "t")["d"][0]
    ok = abs(a - 0.05) < 1e-12 and verdict(abs(a)).startswith("the system's") and abs(b - 0.2) < 1e-12 and verdict(abs(b)).startswith("the chain's")
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1

if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rows = []
    for chain, dtag, clean_log in PAIRS:
        first = parse(os.path.join(HERE, f"eq_{chain}_{dtag}.log"))
        clean = parse(os.path.join(HERE, clean_log))
        rows.append(compare(first, clean, f"{chain} {dtag}"))
    e = parse(os.path.join(HERE, "eq_crawlE_D239.8063.log"))
    a, b = parse(os.path.join(HERE, "../I505-win2/eq_D239.5375.log")), parse(os.path.join(HERE, "../I505-win2/eq_D241.1244.log"))
    t = (e["D"] - a["D"]) / (b["D"] - a["D"])
    interp = lambda i: (1 - t) * math.log(sig(a, i)) + t * math.log(sig(b, i))
    erow = dict(label="crawlE D239.8063 (interpolated clean)", D=e["D"], fp=e["passed"], cp=True, d=[math.log(sig(e, i)) - interp(i) for i in (1, 2, 3, 4)], lf=math.log(sig(e, 1)), lc=interp(1))
    print("| first-chain state | D | ln sigma_1 first | ln sigma_1 clean | difference (sigma_1) | sigma_2 | sigma_3 | sigma_4 | planted checks (first, clean) |")
    print("|---|---|---|---|---|---|---|---|---|")
    for r in rows + [erow]:
        print(f"| {r['label']} | {r['D']:.4f} | {r['lf']:.4f} | {r['lc']:.4f} | {r['d'][0]:+.4f} | {r['d'][1]:+.4f} | {r['d'][2]:+.4f} | {r['d'][3]:+.4f} | {'pass' if r['fp'] else 'FAIL'}, {'pass' if r['cp'] else 'FAIL'} |")
    eq = [abs(r["d"][0]) for r in rows]
    print(f"\nlargest |difference of ln sigma_1| at equal D (six states): {max(eq):.4f}; at the interpolated crawlE state: {abs(erow['d'][0]):.4f} (the interpolation itself is uncertain by about the local-rate scatter times the distance to the neighbours: 0.2 x 0.27 = 0.05)")
    print(f"verdict by the rule (above 0.1): equal-D states: {verdict(max(eq))}; crawlE: {verdict(abs(erow['d'][0]))}")
    # local rates over the same unit steps
    print("\nlocal rates of sigma_1 per unit of D over the same steps (first chain | clean chain):")
    for k in range(3):
        r1, r2 = rows[k], rows[k + 1]
        dd = r2["D"] - r1["D"]
        print(f"  D {r1['D']:.4f} to {r2['D']:.4f}: {(r1['lf'] - r2['lf']) / dd:.3f} | {(r1['lc'] - r2['lc']) / dd:.3f}   (difference {(r1['lf'] - r2['lf']) / dd - (r1['lc'] - r2['lc']) / dd:+.3f})")
    r1, r2 = rows[4], rows[5]
    dd = r2["D"] - r1["D"]
    print(f"  D {r1['D']:.4f} to {r2['D']:.4f}: {(r1['lf'] - r2['lf']) / dd:.3f} | {(r1['lc'] - r2['lc']) / dd:.3f}   (difference {(r1['lf'] - r2['lf']) / dd - (r1['lc'] - r2['lc']) / dd:+.3f})")

"""I168-macm3: the 8 boxes of the D 61 M 32 kf 21 count against #160 (M 32 kf 13) and #159 (M 48 kf 21), and the shared determinants
of M 32 kf 21 against M 32 kf 13 (same plan of points, different frozen set).
    python3 compare_boxes.py        (from this folder; reads ../I160-macm3 and ../I159-macm3)
"""
import json, math, re

RUNS = [("M32 kf21 (#168)", "data/modecount_D61.0264_M32_kf21.log"), ("M32 kf13 (#160)", "../I160-macm3/data/modecount_D61.0264_M32_kf13.log"),
        ("M48 kf21 (#159)", "../I159-macm3/data/modecount_D61.0264_M48_kf21.log")]
box = re.compile(r"box (\S+)\s+Re .*?: winding of g ([-+0-9.e]+) .*?winding of det M (\S+),.*?max phase step ([0-9.]+) rad")
edge = re.compile(r"edge (.+?): (\d+) points, .*?max step ([0-9.]+) rad.*?verified (\d+) \(mismatch (\d+)\) in (\d+) passes")
res = {}
for name, p in RUNS:
    last = {}
    try:
        txt = open(p).read().splitlines()
    except FileNotFoundError:
        txt = open(p.replace("data/", "")).read().splitlines() if False else []
    for ln in txt:
        m = box.search(ln)
        if m:
            last[m.group(1)] = (m.group(2), m.group(3), m.group(4))
    res[name] = last
names = [n for n, _ in RUNS]
order = ["B0", "U0", "B1a", "B1b", "B1c", "B1", "U", "full"]
print("| box | " + " | ".join(f"wind(g), wind(det M), max step: {n}" for n in names) + " |")
print("|---|" + "---|" * len(names))
for b in order:
    print(f"| {b} | " + " | ".join(("{} / {} / {}".format(*res[n][b]) if b in res[n] else "-") for n in names) + " |")

def load(p):
    d = {}
    for ln in open(p):
        r = json.loads(ln)
        d[(round(r["re"], 9), round(r["im"], 9))] = r
    return d
a = load("data/modecount_D61.0264_M32_kf21_evals.jsonl")
b = load("../I160-macm3/data/modecount_D61.0264_M32_kf13_evals.jsonl")
shared = sorted(set(a) & set(b))
print(f"\npoints: kf21 {len(a)}, kf13 {len(b)}, shared {len(shared)}")
dl = [a[k]["lnabs"] - b[k]["lnabs"] for k in shared]
da = [(a[k]["arg"] - b[k]["arg"] + math.pi) % (2 * math.pi) - math.pi for k in shared]
if shared:
    print(f"ln|det| difference kf21 - kf13: min {min(dl):.3f}, max {max(dl):.3f}, spread {max(dl) - min(dl):.3f}")
    print(f"arg difference (mod 2 pi): max |d| {max(abs(x) for x in da):.3e}, median |d| {sorted(abs(x) for x in da)[len(da) // 2]:.3e}")
    print(f"pivot minimum kf21: min {min(a[k]['pmin'] for k in shared):.1e} max {max(a[k]['pmin'] for k in shared):.1e}; kf13: min {min(b[k]['pmin'] for k in shared):.1e} max {max(b[k]['pmin'] for k in shared):.1e}")

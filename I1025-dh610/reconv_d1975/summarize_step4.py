#!/usr/bin/env python3
"""#1025 reconv_d1975 (dh610) summarize_step4.py: prints the step 4 tables from the rows in scan/ and the reference rows in in/. No number is typed by hand.
usage (from this folder): python3 -I summarize_step4.py > summary_step4.txt"""
import json, glob, math

rd = lambda fs: [json.loads(l) for f in fs for l in open(f) if l.strip()]
SRC = [("dh170's own rows (his machine), state 352107a8", ["in/ref_dh170_scan_D19.75_1025.jsonl"]),
       ("macm3's own rows (macOS), state 5825f5d0", ["in/ref_macm3_scan_D19.75_1025.jsonl"]),
       ("my Linux build on macm3's state (../cross_macm3_d1975)", ["in/ref_cross_linux_on_macm3_D19.75_1025.jsonl"]),
       ("linRe, this step", sorted(glob.glob("scan/lin/scan_D19.75_p*.jsonl"))),
       ("macRe, this step", sorted(glob.glob("scan/mac/scan_D19.75_p*.jsonl")))]
LAMS = [1.32, 1.33, 1.34]
sg = lambda s: "+" if s > 0 else "-"
print("| source | lambda | hybrid sign | noise signs | noise robust | float64 sign | ln of abs det | seconds |")
print("|---|---|---|---|---|---|---|---|")
LN = {}
for name, fs in SRC:
    rows = rd(fs)
    for lam in LAMS:
        for r in [r for r in rows if abs(r["lam"] - lam) < 1e-9][-1:]:
            LN[(name, lam)] = (r["sign"], r["ln"])
            print(f"| {name} | {lam:.2f} | {sg(r['sign'])} | {''.join(sg(x) for x in r['noise'])} | {r['noise_robust']} | {sg(r['f64_sign'])} | {r['ln']:.10f} | {r.get('sec')} |")
print()
print("det-linear root of each source's sign change between neighbours (det = sign x exp(ln), taken relative to the lower point's ln), as the reader's estimate; the same arithmetic as `read_lower.py`'s det-linear value:")
print("| source | bracket | det-linear | ln(upper) - ln(lower) |")
print("|---|---|---|---|")
for name, _ in SRC:
    pts = [(lam, LN[(name, lam)]) for lam in LAMS if (name, lam) in LN]
    for (l1, (s1, n1)), (l2, (s2, n2)) in zip(pts, pts[1:]):
        if s1 != s2:
            d1, d2 = s1, s2 * math.exp(n2 - n1)
            root = l1 + (l2 - l1) * d1 / (d1 - d2)
            print(f"| {name} | ({l1:.2f}, {l2:.2f}) | {root:.6f} | {n2 - n1:+.6f} |")
print()
print("ln of abs det, differences between sources at the same lambda (the first source minus the second):")
print("| pair | 1.32 | 1.33 | 1.34 |")
print("|---|---|---|---|")
names = [n for n, _ in SRC]
for a, b in [(3, 0), (3, 4), (4, 1), (4, 2), (2, 1), (2, 0)]:
    cells = []
    for lam in LAMS:
        ka, kb = (names[a], lam), (names[b], lam)
        cells.append(f"{LN[ka][1] - LN[kb][1]:+.6f}" if ka in LN and kb in LN else "n/a")
    print(f"| {names[a].split(',')[0].split(' (')[0]} minus {names[b].split(',')[0].split(' (')[0]} | " + " | ".join(cells) + " |")

# ln|det| difference per unit of |dz| (L2 of the state difference, Delta included), for the pairs of sources whose states are known
import numpy as np
ST = {k: np.load(f"in/sol_{k}_D19.7500.npy") for k in ["l1kc87dh170d1975", "l1kc87macm3d1975", "l1kc87linRe", "l1kc87macRe"]}
nz = lambda a, b: float(np.linalg.norm(ST[a] - ST[b]))
PAIRS = [("linRe minus macRe (same build)", 3, 4, "l1kc87linRe", "l1kc87macRe", "same build"),
         ("macRe minus Linux build on macm3's state (same build)", 4, 2, "l1kc87macRe", "l1kc87macm3d1975", "same build"),
         ("Linux build on macm3's state minus dh170's own rows (two machines)", 2, 0, "l1kc87macm3d1975", "l1kc87dh170d1975", "two machines"),
         ("macRe minus dh170's own rows (two machines)", 4, 0, "l1kc87macRe", "l1kc87dh170d1975", "two machines"),
         ("linRe minus dh170's own rows (two machines)", 3, 0, "l1kc87linRe", "l1kc87dh170d1975", "two machines")]
print()
print("ln of abs det difference per unit of norm dz (L2 of the state difference, Delta included):")
print("| pair | norm dz | 1.32 | 1.33 | 1.34 |")
print("|---|---|---|---|---|")
for label, ia, ib, sa, sb, _ in PAIRS:
    z = nz(sa, sb)
    cells = []
    for lam in LAMS:
        ka, kb = (names[ia], lam), (names[ib], lam)
        cells.append(f"{(LN[ka][1] - LN[kb][1]) / z:+.3e}" if ka in LN and kb in LN else "n/a")
    print(f"| {label} | {z:.4e} | " + " | ".join(cells) + " |")
# the spread of the root difference over the reader's interpolation choices (not an enclosure)
import re
def rng(f):
    m = re.search(r"det-linear (\d\.\d+), range \[(\d\.\d+), (\d\.\d+)\]", open(f).read())
    return float(m[1]), float(m[2]), float(m[3])
(dl, l0, l1), (dm, m0, m1) = rng("read_lower_lin.txt"), rng("read_lower_mac.txt")
print()
print(f"root difference macRe minus linRe: det-linear {dm - dl:+.6f}; over the two estimator ranges (linRe [{l0:.6f}, {l1:.6f}], macRe [{m0:.6f}, {m1:.6f}]) from {m0 - l1:+.6f} to {m1 - l0:+.6f}")

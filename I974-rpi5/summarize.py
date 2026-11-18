"""#964: one table row per solve log of a radius: python3 summarize.py TAG   (from solver/inner_stokes/; stdlib only)"""
import glob, re, sys
tag = sys.argv[1]
order = {"zero": 0, "dA": 1, "dw": 2, "zero_repeat": 3}
rows = []
for f in glob.glob(f"logs/hier_nb_M7_rpi5_{tag}_*.log"):
    t = open(f).read()
    m = re.findall(r"FIXED-A M \d+: A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i\s+\[(\d+) s, (\d+) residuals\]", t)
    r3 = re.findall(r"F_3/F_1 = .*? r_3 ([0-9.]+e[+-]\d+)", t)
    name = f.split(f"{tag}_", 1)[1][:-4]
    base = name.replace("_endstate", "").replace("_r3high", "")
    A, w, a, b, s, n = m[-1]
    rows.append((order[base], "_endstate" in name, name, A, w, float(a), float(b), float(r3[-1]), int(n), int(s)))
rows.sort()
print("| log | A | ω/ω∞ | r₁ | \\|r₃\\| | residuals | seconds |\n|---|---|---|---|---|---|---|")
for _, _, name, A, w, a, b, r3, n, s in rows:
    print(f"| `{name}` | {A} | {w} | {a:+.4f} {b:+.4f}i | {r3:.1e}{'' if r3 < 1e-6 else ' (above)'} | {n} | {s} |")

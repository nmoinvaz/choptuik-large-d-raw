"""#975 (copy of #964's): one table row per solve log of a radius: python summarize.py TAG   (any directory; stdlib only)"""
import glob, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
tag = sys.argv[1]
logs = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
order = {"zero": 0, "dA": 1, "dw": 2, "zero_repeat": 3}
rows = []
for f in glob.glob(os.path.join(logs, f"hier_nb_M7_win2_{tag}_*.log")):
    t = open(f, encoding="utf-8", errors="replace").read()
    m = re.findall(r"FIXED-A M \d+: A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i\s+\[(\d+) s, (\d+) residuals\]", t)
    r3 = re.findall(r"F_3/F_1 = .*? r_3 ([0-9.]+e[+-]\d+)", t)
    name = os.path.basename(f).split(f"{tag}_", 1)[1][:-4]
    base = name.replace("_endstate", "").replace("_r3high", "")
    A, w, a, b, s, n = m[-1]
    rows.append((order[base], "_endstate" in name, name, A, w, float(a), float(b), float(r3[-1]), int(n), int(s)))
rows.sort()
print("| log | A | ω/ω∞ | r₁ | \\|r₃\\| | residuals | seconds |\n|---|---|---|---|---|---|---|")
for _, _, name, A, w, a, b, r3, n, s in rows:
    print(f"| `{name}` | {A} | {w} | {a:+.4f} {b:+.4f}i | {r3:.1e}{'' if r3 < 1e-6 else ' (above)'} | {n} | {s} |")

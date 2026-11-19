"""#999: check that a log's 'level radii' line shows r_5's polish radius at XI (and its approach radius at AP when given).
    python check_polish.py LOG XI [AP] [--mutate]
Exit 0 when the line is there and r_5's polish radius (the number after '->') is XI to its 4 printed digits, 1 otherwise; --mutate compares
against XI + 0.01 and must exit 1. (From #980's check_radii.py, which checks the approach radius.)"""
import re, sys
args = [t for t in sys.argv[1:] if not t.startswith("--")]
log, xi = args[0], float(args[1])
ap = float(args[2]) if len(args) > 2 else None
if "--mutate" in sys.argv:
    xi += 0.01
    ap = None if ap is None else ap + 0.01
for l in open(log, encoding="utf-8", errors="replace"):
    if l.startswith("level radii"):
        m = re.search(r"r_5 ([0-9.]+) -> ([0-9.]+)", l)
        ok = m is not None and abs(float(m.group(2)) - xi) < 5.1e-5 and (ap is None or abs(float(m.group(1)) - ap) < 5.1e-5)
        print(l.strip()); print(f"r_5 polish {m.group(2) if m else None} (approach {m.group(1) if m else None}) vs XI {xi}{'' if ap is None else f' AP {ap}'}: {'ok' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
print("no 'level radii' line yet"); sys.exit(1)

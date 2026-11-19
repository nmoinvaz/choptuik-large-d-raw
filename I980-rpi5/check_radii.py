"""#980: check that a log's 'level radii' line shows r_5's approach radius at XI.  python3 check_radii.py LOG XI [--mutate]
Exit 0 when the line is there and r_5 is XI (to its 4 printed digits), 1 otherwise; --mutate compares against XI + 0.01 and must exit 1."""
import re, sys
log, xi = sys.argv[1], float(sys.argv[2])
if "--mutate" in sys.argv:
    xi += 0.01
for l in open(log):
    if l.startswith("level radii"):
        m = re.search(r"r_5 ([0-9.]+) -> ([0-9.]+)", l)
        ok = m is not None and abs(float(m.group(1)) - xi) < 5.1e-5
        print(l.strip()); print(f"r_5 approach {m.group(1) if m else None} vs XI {xi}: {'ok' if ok else 'FAIL'}")
        sys.exit(0 if ok else 1)
print("no 'level radii' line yet"); sys.exit(1)

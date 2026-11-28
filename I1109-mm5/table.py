"""#1109 stage 1: the table from the logs of each state (report_*.log, valley_*.log, run_*.log). usage: table.py DIR"""
import re, sys
d = sys.argv[1]
rows = []
for tag, D, kc in (("ctl7.0", 7.0, 31), ("ctl10.5", 10.5, 31), ("D14.5", 14.5, 55), ("D15.0", 15.0, 55), ("D15.5", 15.5, 55),
                   ("D16.0", 16.0, 55), ("D16.5", 16.5, 55)):
    try:
        rep = open(f"{d}/report_{tag}.log").read().splitlines()
        val = open(f"{d}/valley_{tag}.log").read()
        run = open(f"{d}/run_{tag}.log").read()
    except FileNotFoundError:
        continue
    wb = re.search(r"weak band .*?: \[(\d+) (\S+) (\S+)\] \[(\d+) (\S+) (\S+)\]", "\n".join(rep))
    base = [l for l in rep if l.startswith("base (")][0]
    F = float(re.search(r"\|F\| (\S+) =", base)[1])
    utf = [float(x) for x in rep[rep.index(base) + 1].split()[2:4]]
    gn = re.search(r"Gauss-Newton step \|dz\| (\S+), dDelta (\S+);", val)
    tot = int(re.search(r"total (\d+) s", run)[1])
    gauge = re.findall(r"gauge generator h = (\w+\(2 w tau\)): .*? (\S+) \((ok|FAIL)", "\n".join(rep))
    gtxt = ", ".join(f"{n} {v} {s}" for n, v, s in gauge)
    rows.append((D, kc, float(wb[3]), float(wb[6]), utf, F, float(gn[2]), float(gn[1]), tot, gtxt, int(wb[1])))
print("| D | k_c | s/s_max, two weakest non-null | U_w^T F (two) | |F| | GN dDelta (full step) | GN |dz| | seconds | gauge generator at 2 w tau |")
print("|---|---|---|---|---|---|---|---|---|")
for D, kc, s1, s2, u, F, dd, dz, tot, g, i0 in rows:
    print(f"| {D} | {kc} | {s1:.3e}, {s2:.3e} (idx {i0}, {i0+1}) | {u[0]:+.4e}, {u[1]:+.4e} | {F:.4e} | {dd:+.4e} | {dz:.4e} | {tot} | {g} |")
first = [r[0] for r in rows if abs(r[6]) > 1e-6]
print("first D with |dDelta| > 1e-6 (in the order of the rows):", first[:1] if first else "none")

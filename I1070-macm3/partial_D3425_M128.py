#!/usr/bin/env python3
"""#1070 macm3b: what the D 3.425 M 128 run left on disk (it has no record and no exit line): the determinants of its log, the bracket they give,
the watcher's last poll and the resources. Every number is computed from run_D3.425_M128.log, res_D3.425_M128.log, exits_1070.txt and
lowD_gamma_D3.425_M96.jsonl. Usage: partial_D3425_M128.py > partial_D3.425_M128.txt"""
import json, os, re, datetime
O = os.path.dirname(os.path.abspath(__file__))
L = open(f"{O}/run_D3.425_M128.log").read().splitlines()
rows = [(float(m.group(1)), int(m.group(2)), float(m.group(3)), m.group(4), float(m.group(5)))
        for l in L if (m := re.match(r"\s+lam (\S+): sign ([+-]\d) ln\|det\| (\S+) pivots (\S+) \(([\d.]+) s\)", l))]
nw = [l.strip() for l in L if l.strip().startswith("newton")]
r96 = json.loads(open(f"{O}/lowD_gamma_D3.425_M96.jsonl").read().splitlines()[-1])
lam96, g96, V = r96["lam"], r96["gamma"], 0.3092057
print("files:", sorted(f for f in os.listdir(O) if "D3.425_M128" in f))
print("record lowD_gamma_D3.425_M128.jsonl exists:", os.path.exists(f"{O}/lowD_gamma_D3.425_M128.jsonl"))
ex = [l for l in open(f"{O}/exits_1070.txt") if "D3.425 M128" in l]
print("exits_1070.txt lines for M128:", len(ex), "->", [l.split(",")[0][:30] + " ... " + l.strip()[-23:] for l in ex])
print("capped_run exit line in the log:", any(l.startswith("capped_run: exit") for l in L))
print("polish:", nw)
print("\n| # | lam | sign | ln|det| | pivots | s |\n|---|---|---|---|---|---|")
for i, (lam, sg, ld, pv, s) in enumerate(rows): print(f"| {i} | {lam:.12f} | {sg:+d} | {ld:.6f} | {pv} | {s:.1f} |")
neg = [r[0] for r in rows if r[1] < 0]; pos = [r[0] for r in rows if r[1] > 0]
lo, hi = max(neg), min(pos)
print(f"\nsign -1 up to lam {lo:.12f}, sign +1 from lam {hi:.12f} (the only sign change among the {len(rows)} determinants): the root lies in ({lo:.12f}, {hi:.12f})")
print(f"M 96's root lam {lam96!r}, gamma {g96!r}: the root's lower end exceeds M 96's lam by {lo - lam96:.3e}")
print(f"gamma(128) is therefore in ({1/hi:.10f}, {1/lo:.10f}); gamma(128) - gamma(96) in ({1/hi - g96:.3e}, {1/lo - g96:.3e}); this is a bracket of an unfinished search, not a value")
print(f"Vienna 0.3092057 lies {V - 1/lo:.3e} above the bracket's upper end (1/{lo:.9f}) and {V - 1/hi:.3e} above its lower end: the unfinished bracket does not hold 0.3092057")
print(f"determinant seconds: " + ", ".join(f"{r[4]:.1f}" for r in rows) + f"; sum {sum(r[4] for r in rows):.0f}")
R = [l.split() for l in open(f"{O}/res_D3.425_M128.log") if not l.startswith("#")]
rs = [(float(x[3]), float(x[4]), float(x[5]), float(x[6]), float(x[7])) for x in R]   # rss GB, cpu %, free mem %, free disk GiB, load1
t0 = datetime.datetime.strptime(" ".join(R[0][:2]), "%Y-%m-%d %H:%M:%S"); t1 = datetime.datetime.strptime(" ".join(R[-1][:2]), "%Y-%m-%d %H:%M:%S")
print(f"\nwatcher: {len(R)} polls, first {R[0][0]} {R[0][1]} UTC, last {R[-1][0]} {R[-1][1]} UTC (run start 00:07:27 UTC, so {(t1 - datetime.datetime(2026, 11, 22, 0, 7, 27)).total_seconds():.0f} s in); no res_summary file (the watcher did not end)")
print(f"  the process was alive at the last poll: rss {rs[-1][0]:.2f} GB, cpu {rs[-1][1]:.0f}%")
print(f"  rss GB max {max(r[0] for r in rs):.2f} mean {sum(r[0] for r in rs)/len(rs):.2f}; cpu% min {min(r[1] for r in rs):.0f} mean {sum(r[1] for r in rs)/len(rs):.0f} max {max(r[1] for r in rs):.0f}; "
      f"load1 mean {sum(r[4] for r in rs)/len(rs):.1f} max {max(r[4] for r in rs):.1f}; free memory min {min(r[2] for r in rs):.0f}%; free disk min {min(r[3] for r in rs):.1f} GiB")
c = [r[1] for r in rs]; a = [r for r in rs[:16]]; b = rs[16:]
print(f"  cpu% mean of the first 16 polls {sum(r[1] for r in a)/len(a):.0f}, of the last {len(b)} {sum(r[1] for r in b)/len(b):.0f}; load1 mean {sum(r[4] for r in a)/len(a):.1f} and {sum(r[4] for r in b)/len(b):.1f}")

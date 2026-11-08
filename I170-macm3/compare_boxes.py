"""I170-macm3: the 8 boxes of the D 45 M 48 kf 21 count against #70 job 7 (D 45 M 48 kf 13) and #159 (D 61 M 48 kf 21), the real-axis sign changes,
the unresolved-edge check, and the evaluation noise (the corner points each cache holds twice, and the pivot minima).    python3 compare_boxes.py
"""
import collections, json, math, re

RUNS = [("D45 M48 kf21 (#170)", "data/modecount_D45.0507_M48_kf21.log", "data/modecount_D45.0507_M48_kf21_evals.jsonl"),
        ("D45 M48 kf13 (#70)", "../I70-macm3/data/modecount_D45.0507_M48_kf13.log", "../I70-macm3/data/modecount_D45.0507_M48_kf13_evals.jsonl"),
        ("D61 M48 kf21 (#159)", "../I159-macm3/data/modecount_D61.0264_M48_kf21.log", "../I159-macm3/data/modecount_D61.0264_M48_kf21_evals.jsonl")]
box = re.compile(r"box (\S+)\s+Re .*?: winding of g ([-+0-9.e]+) .*?winding of det M (\S+),.*?max phase step ([0-9.]+) rad")
edge = re.compile(r"edge (.+?): (\d+) points, .*?max step ([0-9.]+) rad.*?verified (\d+) \(mismatch (\d+)\) in (\d+) passes")
sc = re.compile(r"sign changes of det M on the real axis: (.*)")
res, edges, signs = {}, {}, {}
for name, lg, _ in RUNS:
    last, ed = {}, []
    for ln in open(lg):
        m = box.search(ln)
        if m:
            last[m.group(1)] = (m.group(2), m.group(3), m.group(4))
        m = edge.search(ln)
        if m:
            ed.append((m.group(1), int(m.group(2)), float(m.group(3)), int(m.group(5)), int(m.group(6))))
        m = sc.search(ln)
        if m:
            signs[name] = re.sub(r"np\.float64\(([^)]*)\)", r"\1", m.group(1))
    res[name], edges[name] = last, ed
names = [n for n, _, _ in RUNS]
order = ["B0", "U0", "B1a", "B1b", "B1c", "B1", "U", "full"]
print("wind(g) / wind(det M) / max step")
print("| box | " + " | ".join(names) + " |")
print("|---|" + "---|" * len(names))
for b in order:
    print(f"| {b} | " + " | ".join(("{} / {} / {}".format(*res[n][b]) if b in res[n] else "-") for n in names) + " |")
print()
for n in names:
    ed = edges[n]
    print(f"{n}: {len(ed)} edges, largest step {max(e[2] for e in ed):.3f} rad, verification mismatches {sum(e[3] for e in ed)}, most passes {max(e[4] for e in ed)}; "
          f"real-axis sign changes {signs.get(n)}")
print()
for n, _, ev in RUNS:
    rows = [json.loads(l) for l in open(ev)]
    g = collections.defaultdict(list)
    for r in rows:
        g[(round(r["re"], 9), round(r["im"], 9))].append(r)
    reps = [v for v in g.values() if len(v) > 1]
    da = [abs((v[0]["arg"] - v[1]["arg"] + math.pi) % (2 * math.pi) - math.pi) for v in reps]
    print(f"{n}: {len(rows)} lines, {len(g)} distinct points, pivot minimum {min(r['pmin'] for r in rows):.1e}..{max(r['pmin'] for r in rows):.1e}, "
          f"{len(reps)} repeated points, max |d arg| {max(da):.1e}")

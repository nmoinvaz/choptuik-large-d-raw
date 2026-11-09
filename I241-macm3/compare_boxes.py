"""I241-macm3: the 8 boxes of the M 48, kf 23 counts at D 53.79, 54.04 and 55.04 with the automatic left edges and with the fixed ones (--aLL=-0.096 --aL=0.124), edge statistics, noise.
    python3 compare_boxes.py
"""
import collections, json, math, re

RUNS = [("D53.79 automatic (#237)", "../I237-macm3/D53/data/modecount_D53.7914_M48_kf23.log", "../I237-macm3/D53/data/modecount_D53.7914_M48_kf23_evals.jsonl"),
        ("D53.79 fixed edges", "D53/data/modecount_D53.7914_M48_kf23.log", "D53/data/modecount_D53.7914_M48_kf23_evals.jsonl"),
        ("D54.04 automatic (#240)", "../I240-macm3/data/modecount_D54.0414_M48_kf23.log", "../I240-macm3/data/modecount_D54.0414_M48_kf23_evals.jsonl"),
        ("D54.04 fixed edges", "D54/data/modecount_D54.0414_M48_kf23.log", "D54/data/modecount_D54.0414_M48_kf23_evals.jsonl"),
        ("D55.04 automatic (#232)", "../I232-macm3/D55/data/modecount_D55.0351_M48_kf23.log", "../I232-macm3/D55/data/modecount_D55.0351_M48_kf23_evals.jsonl"),
        ("D55.04 fixed edges", "D55/data/modecount_D55.0351_M48_kf23.log", "D55/data/modecount_D55.0351_M48_kf23_evals.jsonl")]
box = re.compile(r"box (\S+)\s+Re .*?: winding of g ([-+0-9.e]+) .*?winding of det M (\S+),.*?max phase step ([0-9.]+) rad")
edge = re.compile(r"edge (.+?): (\d+) points, .*?max step ([0-9.]+) rad.*?verified (\d+) \(mismatch (\d+)(?:, last pass (\d+))?\) in (\d+) passes(  UNRESOLVED)?")
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
            ed.append((m.group(1), float(m.group(3)), int(m.group(5)), None if m.group(6) is None else int(m.group(6)), int(m.group(7)), bool(m.group(8))))
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
    lastsum = "n/a (before --resolve=last)" if any(e[3] is None for e in ed) else str(sum(e[3] for e in ed))
    print(f"{n}: {len(ed)} edges, largest step {max(e[1] for e in ed):.3f} rad, mismatches in any pass {sum(e[2] for e in ed)}, in the last pass {lastsum}, most passes {max(e[4] for e in ed)}, "
          f"unresolved edges {sum(e[5] for e in ed)}; real-axis sign changes {signs.get(n)}")
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

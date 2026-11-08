"""I168-macm3: evaluation noise from the four corner points that each cache holds twice (a corner shared by two edges), and the
lowest pivot minima, for M 32 kf 21 (this task), M 32 kf 13 (#160) and M 48 kf 21 (#159).    python3 compare_repeats.py
"""
import collections, json, math

for tag, p in (("M32 kf21 (#168)", "data/modecount_D61.0264_M32_kf21_evals.jsonl"),
               ("M32 kf13 (#160)", "../I160-macm3/data/modecount_D61.0264_M32_kf13_evals.jsonl"),
               ("M48 kf21 (#159)", "../I159-macm3/data/modecount_D61.0264_M48_kf21_evals.jsonl")):
    rows = [json.loads(l) for l in open(p)]
    g = collections.defaultdict(list)
    for r in rows:
        g[(round(r["re"], 9), round(r["im"], 9))].append(r)
    reps = [v for v in g.values() if len(v) > 1]
    da = [abs((v[0]["arg"] - v[1]["arg"] + math.pi) % (2 * math.pi) - math.pi) for v in reps]
    dl = [abs(v[0]["lnabs"] - v[1]["lnabs"]) for v in reps]
    print(f"{tag}: {len(rows)} lines, {len(g)} distinct points, pivot minimum {min(r['pmin'] for r in rows):.1e}..{max(r['pmin'] for r in rows):.1e}; "
          f"{len(reps)} repeated points, max |d arg| {max(da):.1e}, max |d ln|det|| {max(dl):.1e}")

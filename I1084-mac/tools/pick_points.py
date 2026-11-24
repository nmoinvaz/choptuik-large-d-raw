"""list #1076's mp rows of the dh610 cache with their float64 start (the latest earlier record of the key) and the
dh610 seconds from recount.log"""
import json, re, sys
cache, log = sys.argv[1], sys.argv[2]
sec = {}
for line in open(log):
    m = re.search(r"point A ([\d.]+) wf ([\d.]+): extended precision, .* (\d+) s$", line.strip())
    if m:
        sec[(float(m.group(1)), float(m.group(2)))] = int(m.group(3))
last = {}
out = []
for i, line in enumerate(open(cache)):
    r = json.loads(line)
    k = (round(r["A"], 12), round(r["wf"], 12))
    if r.get("fu") == "mp":
        s = last.get(k)
        out.append(dict(line=i + 1, A=r["A"], wf=r["wf"], start=None if s is None else (s["F3re"], s["F3im"]),
                        start_line=None if s is None else s["_line"], valued=r.get("valued"),
                        sec=sec.get((round(r["A"], 7), round(r["wf"], 8))), mp=r))
    else:
        r["_line"] = i + 1
        last[k] = r
out = [o for o in out if o["start"] is not None and o["sec"] is not None]
out.sort(key=lambda o: o["sec"])
for o in out[: int(sys.argv[3]) if len(sys.argv) > 3 else 8]:
    print(json.dumps({k: o[k] for k in ("line", "A", "wf", "start", "start_line", "valued", "sec", "mp")}))

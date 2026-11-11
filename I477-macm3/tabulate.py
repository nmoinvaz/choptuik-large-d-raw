#!/usr/bin/env python3
"""I477's table: the series gate of hp/series_truncation.py on every unique stored state (gate_all.jsonl), the paths each state
is stored under (candidates_sha.txt, first 16 hex digits of the sha256), the tasks those paths belong to (the I<n> folder names),
and those tasks' titles (gh issue view). Run in this folder:  python3 tabulate.py > table.md"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
paths = {}
for line in open(os.path.join(HERE, "candidates_sha.txt")):
    sha, p = line.split(None, 1)
    paths.setdefault(sha, []).append(p.strip())
recs = [json.loads(l) for l in open(os.path.join(HERE, "gate_all.jsonl"))]
sha_of = {}
for sha, ps in paths.items():
    for p in ps:
        sha_of[p] = sha
titles = {}


def title(n):
    if n not in titles:
        r = subprocess.run(["gh", "issue", "view", str(n), "-R", "nmoinvaz/choptuik-large-d", "--json", "title", "--jq", ".title"],
                           capture_output=True, text=True)
        titles[n] = r.stdout.strip() or "(no title)"
    return titles[n]


def task_of(p):
    m = re.search(r"/I(\d+)-[a-z0-9]+/", p)
    if m:
        return "#" + m.group(1)
    if "/hp/data/" in p:
        return "tracked hp/data"
    return os.path.basename(os.path.dirname(p))


rows = []
for r in recs:
    sha = sha_of.get(r["state"], "?")
    where = sorted({task_of(p) for p in paths.get(sha, [r["state"]])})
    c, h = r["tails"][0], r["tails"][1]
    rows.append(dict(sha=sha[:8], name=os.path.basename(r["state"]), D=r["D"], M=r["M"], kf=r["kf"], nodes=r["nodes"], F=r["F"],
                     c=c["tail"], cr=c["ratio"], h=h["tail"], hr=h["ratio"], v=r["verdict"], where=where))
rows.sort(key=lambda x: (x["v"] != "ABOVE", x["D"], x["M"], str(x["kf"])))
fm = lambda x: "inf" if x == float("inf") else f"{x:.1e}"
print("| verdict | state | D | M | kf | nodes | \\|F\\| | centre (ratio) | horizon (ratio) | stored under |")
print("|---|---|---|---|---|---|---|---|---|---|")
for x in rows:
    print(f"| {x['v']} | {x['name']} ({x['sha']}) | {x['D']:.4f} | {x['M']} | {x['kf']} | {len(x['nodes'])}, first {x['nodes'][0]} | {x['F']:.1e} | {fm(x['c'])} ({x['cr']:.3f}) | {fm(x['h'])} ({x['hr']:.3f}) | {', '.join(x['where'])} |")
nums = sorted({int(w[1:]) for x in rows for w in x["where"] if w.startswith("#")})
print()
print("Tasks named above:")
for n in nums:
    print(f"- #{n}: {title(n)}")
print()
print(f"{len(rows)} unique states; ABOVE: {sum(x['v'] == 'ABOVE' for x in rows)}; ok: {sum(x['v'] == 'ok' for x in rows)}; ok with a centre or horizon tail above 1e-17: "
      f"{sum(x['v'] == 'ok' and max(x['c'], x['h']) > 1e-17 for x in rows)}")

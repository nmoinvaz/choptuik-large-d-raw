"""Relative differences between two near_null json records, per number (recursively), largest per top-level key.
usage: python cmp_json.py A.json B.json
"""
import json
import sys


def flat(x, path=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from flat(v, f"{path}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from flat(v, f"{path}[{i}]")
    elif isinstance(x, (int, float)) and not isinstance(x, bool):
        yield path, float(x)
    else:
        yield path, x


a = dict(flat(json.load(open(sys.argv[1]))))
b = dict(flat(json.load(open(sys.argv[2]))))
assert a.keys() == b.keys(), "different structure"
worst = {}
nneq = 0
nnum = 0
other_diff = []
for p in a:
    x, y = a[p], b[p]
    if isinstance(x, float) and isinstance(y, float):
        nnum += 1
        if x != y:
            nneq += 1
            rel = abs(x - y) / max(abs(x), abs(y), 1e-300)
            top = p.split("/")[1].split("[")[0]
            if rel > worst.get(top, (0, ""))[0]:
                worst[top] = (rel, p)
    elif x != y:
        other_diff.append((p, x, y))
print(f"{nnum} numbers, {nneq} differ; non-numeric fields that differ: {len(other_diff)}")
for p, x, y in other_diff[:10]:
    print("  ", p, str(x)[:60], "|", str(y)[:60])
for k, (r, p) in sorted(worst.items()):
    print(f"  largest relative difference under '{k}': {r:.2e} at {p}")

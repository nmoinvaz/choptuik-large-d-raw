#!/usr/bin/env python3
"""compare1050.py OLD.log NEW.log [--mutate]: two highm_check logs row by row. A row is a line `M = <M> <name> ...` (the hash and verdict after the name); the other lines kept are the verdict lines
(PASS, FAIL, control ...). Ignored: the `# ... cmd:` header, `exit N`, and the `M = ... outputs in N s` timing lines. Pass (exit 0): the same rows in the same order, each equal, and the same verdict lines.
Prints every differing row (old / new). --mutate changes the last hex digit of the first hash in NEW, or, where no row has a hash, the first row's verdict (the comparison must then fail, exit 1)."""
import re
import sys

a = sys.argv[1:]
mut = "--mutate" in a


def parse(path):
    rows, other = [], []
    for l in open(path).read().splitlines():
        s = l.strip()
        if not s or s.startswith("#") or re.match(r"^exit \d+$", s) or re.search(r"outputs in \d+ s", s):
            continue
        m = re.match(r"^M\s*=\s*(\d+)\s+(\S+)\s+(.*)$", s)
        if m and "(N =" not in s:
            rows.append((m.group(1), m.group(2), m.group(3)))
        else:
            other.append(s)
    return rows, other


ro, oo = parse(a[0])
rn, on = parse(a[1])
if mut and rn:
    for i, (m, n, t) in enumerate(rn):
        h = re.search(r"\b[0-9a-f]{16}\b", t)
        if h:
            d = h.group(0)
            rn[i] = (m, n, t.replace(d, d[:-1] + ("0" if d[-1] != "0" else "1"), 1))
            break
    else:                                   # no hash in any row (scaled): the first row's verdict changes instead
        m, n, t = rn[0]
        rn[0] = (m, n, t.replace("bit-identical", "DIFFERS", 1))
bad = []
for i in range(max(len(ro), len(rn))):
    x = ro[i] if i < len(ro) else None
    y = rn[i] if i < len(rn) else None
    if x != y:
        bad.append((i, x, y))
for i in range(max(len(oo), len(on))):
    x = oo[i] if i < len(oo) else None
    y = on[i] if i < len(on) else None
    if x != y:
        bad.append((f"line {i}", x, y))
for i, x, y in bad[:40]:
    print(f"DIFF {i}: old {x} / new {y}")
print(f"{a[0].split('/')[-1]} against {a[1].split('/')[-1]}{' (--mutate)' if mut else ''}: {len(ro)} rows old, {len(rn)} new, {len(oo)} verdict lines old, {len(on)} new, {len(bad)} differences: "
      f"{'IDENTICAL' if not bad else 'DIFFERENT'}")
sys.exit(0 if not bad else 1)

#!/usr/bin/env python3
"""table1064.py [DIR]: the readings of #1064 from DIR (default: this folder): per rung (ks<K>.log, exits_1064.txt, delta1064_K<K>.json) the gate's verdict, the
exit and wall seconds, the octo-double Newton iterations of the base polish (the log's 'on N:' lines with their seconds) and, for a converged rung, Delta(K) - Delta(293)."""
import glob
import json
import os
import re
import subprocess
import sys

d = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
exits = "".join(open(f"{d}/{n}").read() for n in ("exits_1064.txt", "exits_1064b.txt", "exits_1064c.txt") if os.path.exists(f"{d}/{n}"))
rows = []
for log in sorted(glob.glob(f"{d}/ks[0-9]*.log"), key=lambda p: int(re.search(r"ks(\d+)\.log", p).group(1))):
    K = int(re.search(r"ks(\d+)\.log", log).group(1))
    text = open(log, errors="replace").read()
    g = subprocess.run([sys.executable, f"{os.path.dirname(os.path.abspath(__file__))}/gate1064.py", log, f"{d}/ks{K}"], capture_output=True, text=True).stdout.strip()
    m = re.search(rf"1064 ks{K} exit (\S+) wall (\d+) s", exits)
    capped = re.search(rf"1064 ks{K} cap ", exits) is not None
    st = re.search(r"^\s*on 0: \|F\| ([0-9.]+e[+-]\d+)", text, re.M)
    its = []
    for ln in text.splitlines():
        s = ln.strip()
        a = re.match(r"on (\d+): \|F\| (\S+) -> (\S+), .*?([0-9.]+) s$", s)
        b = re.match(r"on (\d+): \|F\| (\S+) converged", s)
        c = re.match(r"on 0: (strong chord .*?): (\w+), ([0-9.]+) s$", s)
        if c:
            its.append(f"first {c.group(1)} ({c.group(2)}, {c.group(3)} s)")
        elif a:
            its.append(f"step {a.group(1)}: {a.group(2)} -> {a.group(3)}, {a.group(4)} s")
        elif b:
            its.append(f"step {b.group(1)}: {b.group(2)} converged")
    dj = f"{d}/delta1064_K{K}.json"
    dl = ""
    if os.path.exists(dj):
        j = json.load(open(dj))
        rows_ = j.get("csv_rows") or []
        near = rows_[0] if rows_ else None
        dl = (f"{j['change']:+.6e} (same D {j['same_D']}" + (f"; nearest quoted row D {float(near['D']):.4f}, error {near['err']} ({near['err_kind']})" if near else "") + ")")
    rows.append((K, (m.group(1) if m else "?") + (" (capped)" if capped else ""), m.group(2) if m else "?", st.group(1) if st else "-", g, "; ".join(its) or "no iteration lines", dl))
print("| K | exit | wall s | start max|F| at order K | verdict | iterations (|F| before -> after, seconds) | Delta(K) - Delta(293) |")
print("|---|---|---|---|---|---|---|")
for K, rc, w, f0, g, its, dl in rows:
    print(f"| {K} | {rc} | {w} | {f0} | {g} | {its} | {dl or '-'} |")
print()
print("Wall of ks293 to ks318 (exits_1064.txt) is taken after the whole rung ended, so a run that ended earlier shows its rung's wall; from ks295 on (exits_1064b.txt) it is each run's own, in 30 s polls.")

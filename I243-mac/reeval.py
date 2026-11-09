#!/usr/bin/env python3
"""I243-mac: re-evaluate one count with the alias rule of #242 on a copy of its evaluation cache.

    python3 reeval.py NAME HP_DIR CACHE_SRC          (NAME: a record in records/, CACHE_SRC: its evals file)

The cache is copied into NAME/data/ (once; never written in another task's folder), and hp/modecount_wind.py runs with
the record's own geometry (aLL, aL, a1, a2, aR, Im2, h0, lam passed explicitly, so that every cached point is found
again), M, kfreeze and the tag, under the default alias rule. Its log, record and the extended cache go to NAME/data/.
The cache's line count before and after, and a check that the old lines are unchanged, go to NAME/cache_lines.txt.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
name, hp, src = sys.argv[1:4]
rec = json.loads(open(os.path.join(HERE, "records", name + ".jsonl")).readline())
data = os.path.join(HERE, name, "data")
os.makedirs(data, exist_ok=True)
cache_tag = os.path.basename(src)[len("modecount_"):-len("_evals.jsonl")]
dst = os.path.join(data, os.path.basename(src))
if not os.path.exists(dst):
    shutil.copyfile(src, dst)
old = open(src, "rb").read()
n0 = old.count(b"\n")
states = {"up6_D30.0688.npz": "states", "up7_D45.0507.npz": "states", "up8_D50.0075.npz": "states",
          "up9_D52.0414.npz": "states", "up10_D53.7914.npz": "states", "up10_D54.0414.npz": "states",
          "up10_D55.0351.npz": "states", "up23_D61.0264.npz": "seeds/local", "up2_D16.7600.npz": "states",
          "up_D8.2500.npz": "states"}
state = os.path.join(hp, "data", states[rec["state"]], rec["state"])
kf = "none" if rec["kfreeze"] is None else str(rec["kfreeze"])
cmd = [sys.executable, os.path.join(hp, "modecount_wind.py"), state, f"--M={rec['M']}", f"--kf={kf}",
       f"--h0={rec['h0']}", f"--lam={rec['lam_f']!r}", f"--aLL={rec['aLL']!r}", f"--aL={rec['aL']!r}",
       f"--a1={rec['a1']!r}", f"--a2={rec['a2']!r}", f"--aR={rec['aR']!r}", f"--Im2={rec['y2'] / rec['omega']!r}",
       f"--fmax={max(1e-15, 10 * rec['F'])!r}", f"--tag={rec['tag']}", f"--cache={cache_tag}", f"--data={data}"]
if rec["M"] == 48 and rec["kfreeze"] == 23:
    cmd.append("--resolve=last")
print(" ".join(cmd), flush=True)
with open(os.path.join(HERE, name, "count.cmd"), "w") as fo:
    fo.write(" ".join(cmd) + "\n")
r = subprocess.run(cmd)
new = open(dst, "rb").read()
with open(os.path.join(HERE, name, "cache_lines.txt"), "w") as fo:
    fo.write(f"source {src}: {n0} lines, sha256 {hashlib.sha256(old).hexdigest()}\n"
             f"after: {new.count(b'\n')} lines ({new.count(b'\n') - n0} new); old lines unchanged: {new[:len(old)] == old}\n"
             f"modecount_wind exit {r.returncode}\n")
print(open(os.path.join(HERE, name, "cache_lines.txt")).read(), flush=True)
sys.exit(r.returncode)

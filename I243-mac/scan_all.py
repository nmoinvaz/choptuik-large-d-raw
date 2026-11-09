#!/usr/bin/env python3
"""I243-mac: run alias_scan_I230.py (I230-mac/alias_scan.py, unchanged) and scan_rule.py on every record in records/,
control first, and write scan.log. No determinants.

    python3 scan_all.py          (from this folder)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
names = sorted(f[:-6] for f in os.listdir(os.path.join(HERE, "records")) if f.endswith(".jsonl"))
names.remove("I212_D61.0264_M48_kf23")
names.insert(0, "I212_D61.0264_M48_kf23")          # the control: T's last two intervals must be flagged
with open(os.path.join(HERE, "scan.log"), "w") as fo:
    for n in names:
        p = os.path.join(HERE, "records", n + ".jsonl")
        for script in ("alias_scan_I230.py", "scan_rule.py"):
            r = subprocess.run([sys.executable, "-I", os.path.join(HERE, script), p], capture_output=True, text=True)
            fo.write(f"### {n}: {script} (exit {r.returncode})\n{r.stdout}{r.stderr}")
            print(f"{n:28s} {script:20s} {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:]}")

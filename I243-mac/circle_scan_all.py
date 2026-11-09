#!/usr/bin/env python3
"""I243-mac: circle_scan.py on every circle of #178, #190 and I68, writing circles/circle_scan.log.

    python3 circle_scan_all.py RAW_EXTRACT HP_DATA     (RAW_EXTRACT: the git archive of raw 6d8007f; HP_DATA: main's hp/data)
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
raw, hpdata = sys.argv[1:3]
c178 = [f"{raw}/I178-macm3/data_kf{k}/modecount_D45.0507_M48_kf{k}_circ_evals.jsonl" for k in (13, 15, 17, 19, 21)]
c190 = [f"{raw}/I190-macm3/data_kf{k}/modecount_D45.0507_M48_kf{k}_circ_evals.jsonl" for k in (21, 23, 25, 27)]
jobs = [(f"{raw}/I178-macm3/circles.jsonl", c178),
        (f"{raw}/I178-macm3/circles_locate.jsonl",
         [f"{raw}/I178-macm3/locate_r1/modecount_D45.0507_M48_kf21_locr1_evals.jsonl",
          f"{raw}/I178-macm3/locate_r2/modecount_D45.0507_M48_kf21_locr2_evals.jsonl"]),
        (f"{raw}/I190-macm3/circles.jsonl", c190),
        (f"{HERE}/circles/I68_october_D30_M48.jsonl", [f"{raw}/I68-macm3/october_inputs/modecount_D30.0688_M48_evals.jsonl"]),
        (f"{HERE}/circles/I68_october_D30_M48_kf13.jsonl", [f"{hpdata}/modecount_D30.0688_M48_kf13_evals.jsonl"]),
        (f"{HERE}/circles/I68_fresh_D30_M48.jsonl",
         [f"{raw}/I68-macm3/hp_data_after_control_fresh/modecount_D30.0688_M48_evals.jsonl"])]
with open(os.path.join(HERE, "circles", "circle_scan.log"), "w") as fo:
    for rec, caches in jobs:
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "circle_scan.py"), rec] + caches,
                           capture_output=True, text=True)
        fo.write(f"### {rec.split('/')[-2]}/{rec.split('/')[-1]} (exit {r.returncode})\n{r.stdout}{r.stderr}")
        print(f"### {rec.split('/')[-1]}\n{r.stdout}{r.stderr}", end="")

#!/usr/bin/env python3
"""#1025 (win): k_c 63 leap records (this lane's l1kc63W1025.jsonl) against the Mac's k_c 55 leap records (raw I1025-mac/out/l1kc55F1025.jsonl) at the common D.
usage: python compare_leap_1025.py MINE.jsonl RAWWORKTREE   (reads the Mac's file with git show origin/main:...; prints a table and writes nothing)"""
import json, subprocess, sys
mine = {round(json.loads(l)["D"], 6): json.loads(l) for l in open(sys.argv[1]) if l.strip()}
txt = subprocess.run(["git", "-C", sys.argv[2], "show", "origin/main:I1025-mac/out/l1kc55F1025.jsonl"], capture_output=True, text=True, check=True).stdout
mac = {round(json.loads(l)["D"], 6): json.loads(l) for l in txt.splitlines() if l.strip() and json.loads(l).get("kc") == 55}
print(f"k_c 63 records {len(mine)} (D {min(mine)} to {max(mine)}); Mac's k_c 55 records {len(mac)} (D {min(mac)} to {max(mac)})")
print("D | Delta63 | Delta55 | Delta63-Delta55 | constraint63 | constraint55 | |dD/dF|63 | |dD/dF|55")
for D in sorted(mine):
    a = mine[D]; b = mac.get(D)
    if b is None:
        print(f"{D} | {a['Delta']:.9f} | (no k_c 55 record at this D)"); continue
    print(f"{D} | {a['Delta']:.9f} | {b['Delta']:.9f} | {a['Delta'] - b['Delta']:+.3e} | {a['constraint']:.3e} | {b['constraint']:.3e} | {abs(a['dDelta_dF']):.3e} | {abs(b['dDelta_dF']):.3e}")

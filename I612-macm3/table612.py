#!/usr/bin/env python3
"""I612: the share (non-linear / changed by one ulp) of each #473 position at M 48, 64, 80 (positions 2 to 8: this task's P3 and P2 logs;
position 1 and lambda_phys: also M 32, 40 from I609's logs, and M 48 from I609's and this task's), and whether M 64 is below both
neighbours. Usage: python3 table612.py [I609 dir]"""
import os, re, sys
here = os.path.dirname(os.path.abspath(__file__))
i609 = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..", "I609-macm3")
def share(path):
    if not os.path.exists(path): return None
    t = open(path).read()
    m = re.search(r"entries changed by one ulp (\d+) of", t)
    if not m: return None
    c = int(m.group(1)); b = int(re.search(r"> \|d1\|/2: (\d+)", t).group(1))
    return b, c, 100 * b / c
pos = {1: "0.055758+1.411769i", 2: "3.871717+0.105316i", 3: "4.285793+0.551490i", 4: "4.656327+1.390362i",
       5: "0.847147+4.333559i", 6: "1.057045+2.913917i", 7: "1.978326+3.721021i", 8: "4.070967+2.532063i"}
rows = [("lambda_phys", {32: f"{here}/ctrl_M32_phys.log", 40: f"{i609}/D30_M40_phys.log", 48: f"{i609}/D30_M48_phys_fresh.log",
                         64: f"{i609}/D30_M64_phys.log", 80: f"{here}/P1_D30_M80_phys.log"})]
rows.append(("1 " + pos[1], {32: f"{i609}/D30_M32_pos.log", 40: f"{i609}/D30_M40_pos.log", 48: f"{here}/P3_M48_pos1.log",
                             64: f"{here}/P2_M64_pos1.log", 80: f"{i609}/D30_M80_pos.log"}))
for i in range(2, 9):
    rows.append((f"{i} {pos[i]}", {48: f"{here}/P3_M48_pos{i}.log", 64: f"{here}/P2_M64_pos{i}.log", 80: f"{here}/P3_M80_pos{i}.log"}))
Ms = (32, 40, 48, 64, 80)
print("| point (D 30) | " + " | ".join(f"M {M}" for M in Ms) + " | M 64 below M 48 and M 80 |")
print("|---|" + "---|" * (len(Ms) + 1))
for lab, d in rows:
    s = {M: share(d[M]) if M in d else None for M in Ms}
    cells = [("-" if s[M] is None else f"{s[M][0]} ({s[M][2]:.3g}%)") for M in Ms]
    if all(s[M] is not None for M in (48, 64, 80)):
        dip = "yes" if s[64][2] < s[48][2] and s[64][2] < s[80][2] else "no"
        fac = f", factor {min(s[48][2], s[80][2]) / s[64][2]:.3g}" if dip == "yes" else ""
        dip += fac
    else:
        dip = "-"
    print(f"| {lab} | " + " | ".join(cells) + f" | {dip} |")

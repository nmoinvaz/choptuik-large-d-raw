"""#965 stage 2, #974 runs 1 and 2: tables from the whole verbose=2 log of an M = 9 run: python3 summarize_M9.py LOG (stdlib only).
I974 copy: adds the K-by-level table (hier.py main 5e603e30 prints it at verbose 2) and level 7 solves."""
import re, sys
t = open(sys.argv[1]).read().splitlines()
print("pretune of F_9 (B_9, C_9 only; harmonics 1 to 7 stay at the M = 7 zero's values):")
for l in t[:14]:
    if l.startswith("pretune") or "no decrease" in l or re.match(r"\s+it \d+: \|r_9\|", l):
        m = re.match(r"\s+it (\d+): \|r_9\| (\S+)", l)
        print("  " + (f"it {m.group(1)}: |r_9| {m.group(2)}" if m else l.strip()))
print()
print("| time (s) | level 5 solve, \\|r_5\\| | its approach-radius (xi 0.1188) solve stopped at \\|g\\| | residuals | seconds in it |\n|---|---|---|---|---|")
low = None
for l in t:
    m = re.match(r"\s+level 5 \((low|top)\): stop at \|g\| (\S+)", l)
    if m:
        if m.group(1) == "low":
            low = m.group(2)
        continue
    m = re.match(r"\s+level 5 solved: \|r_5\| (\S+)\s+\((\d+) residuals, (\d+) s\)\s+\[(\d+) s total\]", l)
    if m:
        print(f"| {m.group(4)} | {m.group(1)} | {low or "not logged"} | {m.group(2)} | {m.group(3)} |")
        low = None
print()
print("| level 3 iteration | \\|r_3\\| | time (s), residuals so far |\n|---|---|---|")
for l in t:
    m = re.match(r"level 3 it (\d+): \|r_3\| (\S+)\s+lam (\S+)\s+x \[.*\]\s+\[(\d+) s, (\d+) residuals\]", l)
    if m:
        print(f"| {m.group(1)} (lam {m.group(3)}) | {m.group(2)} | {m.group(4)}, {m.group(5)} |")
for l in t:
    if l.startswith("   level 3 (top)") or l.startswith("   level 3 solved") or l.startswith("FIXED-A") or "F_3/F_1" in l:
        print(l.strip())
print()
print("floors the noise-floor rule recorded:", "; ".join(l.strip() for l in t if "floor of level" in l))
print("K:", "; ".join(l.strip() for l in t if "Jacobian K" in l))
print()
for i, l in enumerate(t):
    if "K by level" in l:
        print("K by level (max |d r_l / d x_nu|), at line", i + 1, ":")
        print("\n".join(x for x in t[i:i + 6]))
        break
else:
    print("K by level: not printed in this log")
print()
print("| time (s) | level 7 solve, \\|r_7\\| | residuals | seconds in it |\n|---|---|---|---|")
for l in t:
    m = re.match(r"\s+level 7 solved: \|r_7\| (\S+)\s+\((\d+) residuals, (\d+) s\)\s+\[(\d+) s total\]", l)
    if m:
        print(f"| {m.group(4)} | {m.group(1)} | {m.group(2)} | {m.group(3)} |")

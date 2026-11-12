"""Line-by-line comparison of two chain logs with the trailing wall times removed.
usage: python cmp_logs.py NEW.log OLD.log [--mutate]
NEW is read from its first 'held values' line to the line before 'done'; OLD from the last 'held values'
line before its first 'step 0:' line, for as many lines as NEW has. --mutate changes one digit in NEW first,
the control that must report a difference.
"""
import re
import sys


def lines(path):
    return [re.sub(r",\s*[\d.]+ s$", "", ln.rstrip("\r\n")) for ln in open(path, errors="replace")]


new = lines(sys.argv[1])
old = lines(sys.argv[2])
i0 = next(i for i, ln in enumerate(new) if ln.startswith("held values from the fit"))
i1 = next(i for i, ln in enumerate(new) if ln == "done")
new = new[i0:i1]
s0 = next(i for i, ln in enumerate(old) if ln.startswith("step 0: D 228.13125"))
j0 = max(i for i, ln in enumerate(old[:s0]) if ln.startswith("held values from the fit"))
old = old[j0:j0 + len(new)]
if "--mutate" in sys.argv:
    k = next(i for i, ln in enumerate(new) if ln.startswith("  on 5: |F| 1.95e-95"))
    new[k] = new[k].replace("1.95e-95", "1.96e-95")
bad = [(i, a, b) for i, (a, b) in enumerate(zip(new, old)) if a != b]
print(f"{len(new)} lines compared, {len(bad)} differ")
for i, a, b in bad[:5]:
    print(f"  line {i}: {a}\n       vs {b}")

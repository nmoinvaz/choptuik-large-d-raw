"""Line-by-line comparison of the step into D 230.13125 in two anm_run logs, trailing wall times removed.
usage: python cmp_logs3.py NEW.log OLD.log [--mutate] [--show]
Each log is read from its 'step N: D 229.13125' line (the series line of the step; N is made the same) to
its 'done' line, or to the next 'step' line. --mutate changes one digit of the last residual in NEW first,
the control that must report a difference. --show lists every differing line (up to 40).
"""
import re
import sys


def lines(path):
    L = [re.sub(r",\s*[\d.]+ s$", "", ln.rstrip("\r\n")) for ln in open(path, errors="replace")]
    i0 = next(i for i, ln in enumerate(L) if re.match(r"step \d+: D 229\.13125", ln))
    out = []
    for ln in L[i0:]:
        if ln == "done" or (out and re.match(r"step \d+: ", ln)):
            break
        out.append(re.sub(r"^step \d+:", "step N:", ln))
    return out


new, old = lines(sys.argv[1]), lines(sys.argv[2])
if "--mutate" in sys.argv:
    k = next(i for i, ln in enumerate(new) if ln.startswith("  on 5: |F| 1.95e-95"))
    new[k] = new[k].replace("1.95e-95", "1.96e-95")
bad = [(i, new[i] if i < len(new) else "<none>", old[i] if i < len(old) else "<none>")
       for i in range(max(len(new), len(old))) if i >= len(new) or i >= len(old) or new[i] != old[i]]
print(f"{len(new)} lines against {len(old)} lines, {len(bad)} differ")
for i, a, b in bad[: 40 if "--show" in sys.argv else 5]:
    print(f"  line {i}: {a}\n       vs {b}")

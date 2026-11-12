"""Line-by-line comparison of two anm_run logs, trailing wall times removed.
usage: python cmp_logs2.py NEW.log OLD.log [--mutate]
Each log is read from its last 'held values from the fit' line to its 'done' line, without the line
'base polish saved as ...' that --save_base 1 adds (it is counted and printed). --mutate changes
one digit of the last residual in NEW first, the control that must report a difference.
"""
import re
import sys


def lines(path):
    L = [re.sub(r",\s*[\d.]+ s$", "", ln.rstrip("\r\n")) for ln in open(path, errors="replace")]
    i0 = max(i for i, ln in enumerate(L) if ln.startswith("held values from the fit"))
    i1 = next(i for i in range(i0, len(L)) if L[i] == "done")
    body = L[i0:i1]
    return [ln for ln in body if not ln.startswith("base polish saved as")], len(body) - len(
        [ln for ln in body if not ln.startswith("base polish saved as")])


(new, dn), (old, do) = lines(sys.argv[1]), lines(sys.argv[2])
if "--mutate" in sys.argv:
    k = next(i for i, ln in enumerate(new) if ln.startswith("  on 5: |F| 2.68e-95"))
    new[k] = new[k].replace("2.68e-95", "2.69e-95")
n = max(len(new), len(old))
bad = [(i, new[i] if i < len(new) else "<none>", old[i] if i < len(old) else "<none>")
       for i in range(n) if i >= len(new) or i >= len(old) or new[i] != old[i]]
print(f"{len(new)} lines against {len(old)} lines ({dn} and {do} 'base polish saved as' lines left out), {len(bad)} differ")
for i, a, b in bad[:5]:
    print(f"  line {i}: {a}\n       vs {b}")

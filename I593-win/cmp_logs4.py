"""Line-by-line comparison of the step D 230.13125 -> 231.13125 in two anm_run logs, wall times removed.
usage: python cmp_logs4.py NEW.log OLD.log [--mutate] [--show]
Each log is read from its 'step N: D 230.13125' line (the series line of the step) to its 'a 1.000 -> D 231.13125' line,
the last line of the step. 'step N:' is made the same. First the lines are compared as printed, then with
the printed tol of the 'a 1.000 -> D' lines made the same (it grows with the distance from the run's start state).
--mutate changes one digit of the last residual in NEW first, the control that must report a difference.
"""
import re
import sys


def lines(path):
    L = [re.sub(r",\s*[\d.]+ s$", "", ln.rstrip("\r\n")) for ln in open(path, errors="replace")]
    i0 = next(i for i, ln in enumerate(L) if re.match(r"step \d+: D 230\.13125", ln))
    out = []
    for ln in L[i0:]:
        out.append(re.sub(r"^step \d+:", "step N:", ln))
        if ln.startswith("    a 1.000 -> D 231.13125"):
            break
    return out


def diff(a, b):
    return [(i, a[i] if i < len(a) else "<none>", b[i] if i < len(b) else "<none>")
            for i in range(max(len(a), len(b))) if i >= len(a) or i >= len(b) or a[i] != b[i]]


new, old = lines(sys.argv[1]), lines(sys.argv[2])
if "--mutate" in sys.argv:
    k = [i for i, ln in enumerate(new) if ln.startswith("  on 4: |F| 3.31e-81")][0]
    new[k] = new[k].replace("3.31e-81", "3.32e-81")
strict = diff(new, old)
loose = diff([re.sub(r"\(tol [\d.e+-]+,", "(tol T,", s) for s in new], [re.sub(r"\(tol [\d.e+-]+,", "(tol T,", s) for s in old])
print(f"{len(new)} lines against {len(old)} lines; as printed {len(strict)} differ; with the printed tol made the same {len(loose)} differ")
for i, a, b in (strict if "--show" in sys.argv else strict[:6]):
    ta = re.search(r"\(tol ([\d.e+-]+),", a)
    tb = re.search(r"\(tol ([\d.e+-]+),", b)
    print(f"  line {i}: tol {ta.group(1)} against {tb.group(1)}" if ta and tb and a != b and re.sub(r"\(tol [\d.e+-]+,", "", a) == re.sub(r"\(tol [\d.e+-]+,", "", b)
          else f"  line {i}: {a}\n       vs {b}")

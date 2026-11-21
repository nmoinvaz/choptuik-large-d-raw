# glue for run903d.sh: the verdict of a ladder rung from its anm_run.log (the first octo-double Newton line is the base polish)
import re, sys
t = open(sys.argv[1], errors="replace").read()
m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (not )?converged", t)
p = re.findall(r"on \d+: \|F\| .* piv ([0-9.e+-]+)\.\.", t)
if not m:
    print("FAILED no octo-double Newton line")
else:
    ok = (not m.group(3)) and float(m.group(2)) <= 1e-60
    print(("OK" if ok else "FAILED") + f" od steps {m.group(1)} max|F| {m.group(2)}" + (" not converged" if m.group(3) else "")
          + f" piv_min {p[-1] if p else '?'}")

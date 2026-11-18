"""#948: what a capped rung had reached, from its anm_run log.

    python caprep948.py RUNG.log          prints one line: the accepted iterations, the last one's |F|, |dz| and lam, and the refused
                                          trials since (lam, max|F|), which is the "last max|F| and lam" the coordinator asked for."""
import re
import sys

its, trials = [], []
for ln in open(sys.argv[1]):
    m = re.match(r"  on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+), .*?, ([\d.]+) s", ln)
    if m:
        its.append(m.groups())
        trials = []
        continue
    m = re.match(r"    on (\d+) trial lam (\S+): max\|F\| (\S+); .*?(refused|accepted), ([\d.]+) s", ln)
    if m:
        trials.append(m.groups())
if its:
    it, F0, F1, d0, d1, lam, dD, t = its[-1]
    s = f"{len(its)} iterations finished (the last, on {it}: max|F| {F0} to {F1}, |dz| {d0} to {d1}, lam {lam}, {t} s)"
else:
    s = "no iteration finished"
if trials:
    s += "; trials since: " + ", ".join(f"lam {float(l):g} max|F| {F} {v}" for _, l, F, v, _ in trials)
print(s)

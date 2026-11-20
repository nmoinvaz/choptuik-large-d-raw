#!/usr/bin/env python3
"""#1048 section 2 (README.md): where a hier_nb.py M = 7 fixed-(A, w) solve stalls, from its verbose=2 log. Per log: each
level-3 iteration's |r_3|; per level nu in (7, 5, 3) the final value of each level-nu solve ("level nu solved"), how many
are above the 1e-6 bar, and hier's noise-floor stops ("level nu (low|top): stop at |g| X (noise floor)") above the bar;
the final |r_3|, |r_5|, |r_7|. Reading: the stall harmonic is the highest nu whose level-nu solves end at a noise-floor
stop above 1e-6 (a "level nu solved" value above the bar right after such a stop).
    python stall1048.py LOG...             one block per log, then a STALL line per log
    python stall1048.py selftest [--mutate=order]   on a synthetic log (the mutation reads the levels bottom-up: must fail)"""
import re
import sys

BAR = 1e-6
NUM = r"([0-9.]+e[+-]\d+)"


def read(text):
    it3 = [float(v) for v in re.findall(r"^level 3 it \d+: \|r_3\| " + NUM, text, re.M)]
    lev = {}
    last_stop = {}
    for line in text.splitlines():
        m = re.match(r"\s*level (\d) \((?:low|top)\): stop at \|g\| " + NUM + r" \(noise floor\)", line)
        if m:
            nu, g = int(m.group(1)), float(m.group(2))
            last_stop[nu] = g
            lev.setdefault(nu, dict(solved=[], floor_stops=[], ends_at_floor_above=0))["floor_stops"].append(g)
            continue
        m = re.match(r"\s*level (\d) solved: \|r_\d\| " + NUM, line)
        if m:
            nu, v = int(m.group(1)), float(m.group(2))
            d = lev.setdefault(nu, dict(solved=[], floor_stops=[], ends_at_floor_above=0))
            d["solved"].append(v)
            if v > BAR and last_stop.get(nu) is not None:
                d["ends_at_floor_above"] += 1
            last_stop[nu] = None
    fin = {int(nu): float(v) for nu, v in re.findall(r"F_(\d)/F_1 = .*?r_\d " + NUM, text)}
    return it3, lev, fin


def stall(lev, mut=""):
    order = (3, 5, 7) if mut == "order" else (7, 5, 3)
    return next((nu for nu in order if lev.get(nu, {}).get("ends_at_floor_above", 0) > 0), None)


def report(path):
    it3, lev, fin = read(open(path).read())
    out = [f"{path.split('/')[-1]}: level-3 iterations |r_3| " + ", ".join(f"{v:.2e}" for v in it3)]
    for nu in (7, 5, 3):
        d = lev.get(nu)
        if not d:
            continue
        s = sorted(d["solved"])
        above = [g for g in d["floor_stops"] if g > BAR]
        out.append(f"  level {nu}: {len(s)} solves, final |r_{nu}| median {s[len(s) // 2]:.2e}, largest {s[-1]:.2e}, "
                   f"{sum(v > BAR for v in s)} above 1e-6 ({d['ends_at_floor_above']} right after a noise-floor stop); "
                   f"noise-floor stops {len(d['floor_stops'])}, {len(above)} above 1e-6"
                   + (f" (largest {max(above):.2e})" if above else "") if s else f"  level {nu}: no solve line")
    out.append("  final " + ", ".join(f"|r_{nu}| {fin[nu]:.1e}" for nu in sorted(fin)))
    out.append(f"  STALL harmonic: {stall(lev)}")
    return "\n".join(out)


def selftest(mut):
    syn = "\n".join(["   level 7 solved: |r_7| 1.0e-10  (3 residuals)", "   level 5 (top): stop at |g| 3.0e-06 (noise floor)",
                     "   level 5 solved: |r_5| 3.0e-06  (9 residuals)", "level 3 it 0: |r_3| 5.0e-01  lam 1",
                     "   level 3 (top): stop at |g| 2.0e-02 (noise floor)", "   level 3 solved: |r_3| 2.0e-02  (40 residuals)"])
    got = stall(read(syn)[1], mut)
    print(f"selftest{' --mutate=' + mut if mut else ''}: stall harmonic {got} (expect 5): {'PASS' if got == 5 else 'FAIL'}")
    return got == 5


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(0 if selftest("order" if "--mutate=order" in sys.argv else "") else 1)
    print("\n".join(report(p) for p in sys.argv[1:]))

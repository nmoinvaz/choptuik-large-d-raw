"""#1012: level 7's and level 9's solve ends beside level 5's. For each level-5 solve of a log (the window of lines up to and including its `level 5 solved` line, the last window being the
lines after the last one), print level 5's end |r_5|, the number, minimum, median and maximum of the level-7 and level-9 solves (`level K solved: |r_K| X`) inside the window, and the
counts of the stop reasons of levels 7 and 9 there. Reads main ec7cfea7+ log format (verbose 2).

    python levels1012.py LABEL:LOG [LABEL:LOG ...]          (stdlib only; exit 1 when a check fails)
Checks: the windows' level-7 and level-9 counts add up to the number of `level K solved` mentions in the whole log (a loose count, independent of the strict per-line pattern);
a log with one such line damaged must trip it."""
import re, statistics, sys

STRICT = {k: re.compile(rf"^\s+level {k} solved: \|r_{k}\| (\S+)\s+\(") for k in (7, 9)}
STOP = re.compile(r"^\s+level (7|9) \((low|top)\): stop at \|r_\d\| \S+: (.*)$")
bad = 0
for arg in sys.argv[1:]:
    label, log = arg.split(":", 1)
    with open(log, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    lines = text.splitlines()
    wins, cur = [], []
    for l in lines:
        cur.append(l)
        m = re.match(r"\s+level 5 solved: \|r_5\| (\S+)", l)
        if m:
            wins.append((m.group(1), cur)); cur = []
    wins.append((None, cur))
    print(f"\n### {label}   ({log}, {len(lines)} lines)\n")
    print("| level-5 solve | end |r_5| | level 7 solves: n, min / median / max | level 9 solves: n, min / median / max | level 7 stops | level 9 stops |")
    print("|---|---|---|---|---|---|")
    tot = {7: 0, 9: 0}
    for i, (end, ls) in enumerate(wins):
        row = {}
        for k in (7, 9):
            v = sorted(float(m.group(1)) for l in ls for m in [STRICT[k].match(l)] if m)
            tot[k] += len(v)
            row[k] = f"{len(v)}, {v[0]:.1e} / {statistics.median(v):.1e} / {v[-1]:.1e}" if v else "0"
        stops = {7: {}, 9: {}}
        for l in ls:
            m = STOP.match(l)
            if m:
                r = re.sub(r"every trial rejected.*", "every trial rejected", m.group(3))
                r = re.sub(r"a fresh Jacobian no longer halves.*", "no longer halves", r)
                stops[int(m.group(1))][r] = stops[int(m.group(1))].get(r, 0) + 1
        fmt = lambda d: "; ".join(f"{n} x {r}" for r, n in sorted(d.items(), key=lambda kv: -kv[1])) or "-"
        name = f"{i + 1}" if end is not None else "after the last (unfinished)"
        if end is None and not any(row[k] != "0" for k in (7, 9)):
            continue
        print(f"| {name} | {end if end is not None else '-'} | {row[7]} | {row[9]} | {fmt(stops[7])} | {fmt(stops[9])} |")
    for k in (7, 9):
        loose = len(re.findall(rf"level {k} solved", text))
        if loose != tot[k]:
            print(f"COUNT CHECK FAILED: level {k}: windows hold {tot[k]} solved lines, the log mentions {loose}"); bad = 1
sys.exit(bad)

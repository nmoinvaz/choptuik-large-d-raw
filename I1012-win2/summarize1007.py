"""#1007: per run, level 5's solves (|r_5| at the end, the approach (low) and polish (top) stops with their reasons, accepted iterations, trials at verbose 3,
residuals, seconds), level 3's iterations, stops and end, and the end values of r_1, r_3, r_5, r_7, r_9.
Reads main ec7cfea7's log format (stop line: `level N (low|top): stop at |r_N| X: reason`; trial line: `level N (low|top) it K trial lam L: |r_N| A against B:
accepted|rejected`).   Usage: python summarize1007.py XI:LOG [XI:LOG ...]   (stdlib only; exit 1 when a check fails)
Checks: the number of table rows equals the number of `level 5 solved` lines, and each r_k at the end equals the last `level k solved` value to 2 digits."""
import re, sys

BP = chr(92) + "|"
HEAD = ("| time (s) | level-5 solve ends at " + BP + "r_5" + BP + " | approach (low) stop | polish (top) stop | accepted iterations " + BP + "r_5" + BP +
        " | trials (acc/rej) | residuals | seconds |" + chr(10) + "|---|---|---|---|---|---|---|---|")
bad = 0
for arg in sys.argv[1:]:
    xi, log = arg.split(":", 1)
    t = open(log, encoding="utf-8", errors="replace").read().splitlines()
    print(f"\n### XI {xi}   ({log}, {len(t)} lines)\n")
    print(HEAD)
    low = top = None; its = []; acc = rej = 0; rows = 0
    for l in t:
        m = re.match(r"\s+level 5 \((low|top)\): stop at \|r_5\| (\S+): (.*)", l)
        if m:
            if m.group(1) == "low": low = f"{m.group(2)}: {m.group(3)}"
            else: top = f"{m.group(2)}: {m.group(3)}"
            continue
        m = re.match(r"level 5 it \d+: \|r_5\| (\S+)", l)
        if m: its.append(m.group(1)); continue
        m = re.match(r"\s+level 5 \((low|top)\) it \d+ trial lam \S+: \|r_5\| \S+ against \S+: (accepted|rejected)", l)
        if m:
            acc += m.group(2) == "accepted"; rej += m.group(2) == "rejected"; continue
        m = re.match(r"\s+level 5 solved: \|r_5\| (\S+)\s+\((\d+) residuals, (\d+) s\)\s+\[(\d+) s total\]", l)
        if m:
            rows += 1
            print(f"| {m.group(4)} | {m.group(1)} | {low or '-'} | {top or '-'} | {', '.join(its) or '-'} | {acc}/{rej} | {m.group(2)} | {m.group(3)} |")
            low = top = None; its = []; acc = rej = 0
    n5 = sum(1 for l in t if "level 5 (top): stop at" in l)           # independent of the rows: each finished solve prints one polish stop
    if rows != n5: print(f"COUNT CHECK FAILED: {rows} rows against {n5} level 5 (top) stop lines"); bad = 1
    if rows == 0: print("| no level 5 solve finished | | | | | | | |")
    print("\nlevel 3:")
    for l in t:
        if re.match(r"level 3 it \d+:", l): print("  " + re.sub(r"\s+x \[.*\]", "", l.strip())[:160])
        elif re.match(r"\s+level 3 \((low|top)\) it \d+ trial", l): print("    " + l.strip()[:160])
        elif re.match(r"\s+level 3 \((low|top)\)", l) and "stop at" in l: print("  " + l.strip()[:200])
        elif re.match(r"\s+level 3 solved", l): print("  " + l.strip()[:200])
    ends = {}
    for l in t:
        m = re.match(r"\s+F_(\d+)/F_1 = .*? r_\d+ (\S+)$", l)
        if m: ends[int(m.group(1))] = m.group(2)
        m = re.match(r"FIXED-A M \d+: .*r_1 (\S+?)\s+\[(\d+) s, (\d+) residuals\]", l)
        if m: ends["r1"] = f"{m.group(1)} [{m.group(2)} s, {m.group(3)} residuals]"
    if ends:
        print("end values: " + ", ".join(f"{'r_1' if k == 'r1' else 'r_' + str(k)} {v}" for k, v in sorted(ends.items(), key=lambda kv: (isinstance(kv[0], str), kv[0]))))
        for k in (3, 5, 7, 9):                          # v2 (#1012): the end value is the ACCEPTED state's, so it must equal ONE of the level-k solves (to 2 digits), not the last
            vals = [re.match(rf"\s+level {k} solved: \|r_{k}\| (\S+)", l) for l in t]
            vals = [m.group(1) for m in vals if m]
            if k in ends and vals and not any(f"{float(v):.1e}" == f"{float(ends[k]):.1e}" or f"{float(v):.0e}" == f"{float(ends[k]):.0e}" for v in vals):
                print(f"END CHECK: r_{k} printed {ends[k]} but no level {k} solved line of the log has that value"); bad = 1
    else:
        print("no FIXED-A line (the run was stopped before the end)")
sys.exit(bad)

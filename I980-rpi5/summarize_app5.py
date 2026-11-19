"""#980: per XI, level 5's solves and level 3's first iterations from the whole verbose=2 logs.  python3 summarize_app5.py XI:LOG [XI:LOG ...]  (stdlib)
Per level-5 solve: |r_5| at its end, the approach ('low') solve's |g| and the polish ('top') solve's |g| where the log prints a stop line (else '-'),
the accepted iterations of level 5 printed in it (|r_5| each), residuals and seconds in it, and the time of the solve's end."""
import re, sys
for arg in sys.argv[1:]:
    xi, log = arg.split(":", 1)
    t = open(log).read().splitlines()
    print(f"\n### XI {xi}   ({log}, {len(t)} lines)\n")
    print("| time (s) | level 5 solve, \\|r_5\\| | approach solve stopped at \\|g\\| | polish solve stopped at \\|g\\| | accepted iterations \\|r_5\\| | residuals | seconds |\n|---|---|---|---|---|---|---|")
    low = top = None; its = []; n = 0
    for l in t:
        m = re.match(r"level 5 it \d+: \|r_5\| (\S+)", l)
        if m: its.append(m.group(1)); continue
        m = re.match(r"\s+level 5 \((low|top)\): stop at \|g\| (\S+)", l)
        if m:
            if m.group(1) == "low": low = m.group(2)
            else: top = m.group(2)
            continue
        m = re.match(r"\s+level 5 solved: \|r_5\| (\S+)\s+\((\d+) residuals, (\d+) s\)\s+\[(\d+) s total\]", l)
        if m:
            n += 1
            print(f"| {m.group(4)} | {m.group(1)} | {low or '-'} | {top or '-'} | {', '.join(its) or '-'} | {m.group(2)} | {m.group(3)} |")
            low = top = None; its = []
    if n == 0: print("| no level 5 solve finished | | | | | | |")
    k = [l for l in t if "K by level" in l]
    print()
    for l in t:
        m = re.match(r"level 3 it (\d+): \|r_3\| (\S+)\s+lam (\S+)\s+x \[.*\]\s+\[(\d+) s, (\d+) residuals\]", l)
        if m: print(f"level 3 it {m.group(1)} (lam {m.group(3)}): |r_3| {m.group(2)} [{m.group(4)} s, {m.group(5)} residuals]")
    for l in t:
        if l.strip().startswith(("level 3 (top)", "level 3 solved", "FIXED-A", "F_3/F_1")):
            print(l.strip()[:200])

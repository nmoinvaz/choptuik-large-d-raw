"""How much of each macm3 run's wall-clock window was the Mac asleep? (I68-macm3, the same script as I125-macm3's with this task's windows.)

Reads `pmset -g log` (macOS), takes every "Entering Sleep state" to the next Wake or DarkWake event as an interval of sleep,
and overlaps those with the run windows below (UTC, from each task's exits.txt or post; the log is in local time, PST here,
UTC - 8 h on these dates). The log starts 2026-11-06 10:55 PST, so earlier runs (T133) cannot be checked.
    python3 pmset_sleep.py
"""
import datetime as dt
import re
import subprocess

RUNS = [  # name, start UTC, end UTC, wall seconds (from this folder's exits.txt)
    ("build modecount_cx", "2026-11-08 06:55:50", "2026-11-08 06:56:36", 46),
    ("planted test", "2026-11-08 06:57:06", "2026-11-08 06:57:07", 1),
    ("circles (job 4)", "2026-11-08 06:57:25", "2026-11-08 06:58:36", 71),
]

log = subprocess.run(["/usr/bin/pmset", "-g", "log"], capture_output=True, text=True).stdout
events = []
for ln in log.splitlines():
    m = re.match(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) [+-]\d{4} (Sleep|Wake|DarkWake)\s+(\S.*)", ln)
    if m and not m.group(3).startswith("Requests"):
        events.append((dt.datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S"), m.group(2), m.group(3)))
sleeps = []
for i, (t, kind, rest) in enumerate(events):
    if kind == "Sleep" and rest.startswith("Entering Sleep state"):
        nxt = next((e[0] for e in events[i + 1:] if e[1] in ("Wake", "DarkWake")), None)
        if nxt:
            sleeps.append((t, nxt, re.search(r"due to '([^']+)", rest).group(1)))


def to_pst(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S") - dt.timedelta(hours=8)


print(f"log from {events[0][0]} to {events[-1][0]} PST; {len(sleeps)} sleeps, "
      f"{sum(1 for s in sleeps if (s[1] - s[0]).total_seconds() > 120)} longer than 2 min")
print("| run | wall s | asleep s | awake s |")
print("|---|---|---|---|")
for name, a, b, wall in RUNS:
    A, B = to_pst(a), to_pst(b)
    asleep = sum(max(0.0, (min(e, B) - max(s, A)).total_seconds()) for s, e, _ in sleeps)
    print(f"| {name} | {wall} | {asleep:.0f} | {wall - asleep:.0f} |")
print()
print("sleeps over 2 min (PST):")
for s, e, why in sleeps:
    if (e - s).total_seconds() > 120:
        print(f"  {s} to {e.time()}, {(e - s).total_seconds():.0f} s, {why}")

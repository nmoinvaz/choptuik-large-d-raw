"""How much of each macm3 run's wall-clock window was the Mac asleep? (I125-macm3, found when two rays took 2506 s instead of 517 s.)

Reads `pmset -g log` (macOS), takes every "Entering Sleep state" to the next Wake or DarkWake event as an interval of sleep,
and overlaps those with the run windows below (UTC, from each task's exits.txt or post; the log is in local time, PST here,
UTC - 8 h on these dates). The log starts 2026-11-06 10:55 PST, so earlier runs (T133) cannot be checked.
    python3 pmset_sleep.py
"""
import datetime as dt
import re
import subprocess

RUNS = [  # name, start UTC, end UTC, wall seconds
    ("T139 pilot", "2026-11-07 04:07:15", "2026-11-07 04:21:35", 852),
    ("T139 chain", "2026-11-07 04:21:54", "2026-11-07 11:36:35", 26081),
    ("T142 control D 79.7657 (cut at 1.5 h)", "2026-11-07 11:37:29", "2026-11-07 13:07:44", 5415),
    ("T142 D 130 --it 6 (stopped)", "2026-11-07 13:07:45", "2026-11-07 13:27:32", 1187),
    ("T142 D 130 --it 1", "2026-11-07 13:27:48", "2026-11-07 13:44:09", 981),
    ("T146 run 1 (D 80)", "2026-11-07 13:44:33", "2026-11-07 14:07:05", 1352),
    ("T146 run 2 (D 100)", "2026-11-07 14:07:25", "2026-11-07 15:06:06", 3521),
    ("T149 5b", "2026-11-07 15:22:57", "2026-11-07 15:48:50", 1553),
    ("T149 7b", "2026-11-07 15:48:50", "2026-11-07 15:56:10", 440),
    ("T149 7a", "2026-11-07 15:56:10", "2026-11-07 16:03:50", 460),
    ("T148 11b", "2026-11-07 16:05:18", "2026-11-07 16:51:28", 2770),
    ("T148 13b", "2026-11-07 16:51:28", "2026-11-07 17:10:49", 1161),
    ("T153 three nodes", "2026-11-07 17:11:11", "2026-11-07 20:46:12", 12901),
    ("I37 ray", "2026-11-08 04:14:35", "2026-11-08 04:22:39", 484),
    ("I38 five processes", "2026-11-08 04:56:38", "2026-11-08 05:33:34", 2174),
    ("I125 rays", "2026-11-08 06:02:15", "2026-11-08 06:44:01", 2506),
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

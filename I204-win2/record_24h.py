#!/usr/bin/env python3
"""I204-win2: the crash and temperature record of the 24 h after the load started (issue #204).

    python -I record_24h.py [START [END]]       defaults 2026-11-09T01:30:41 and 2026-11-10T01:30:00 (UTC)
        Reads sensor_log.txt (one reading every 5 minutes, from sensor_log.py + Core Temp) and crashes.txt / crash_temps.txt.
        Prints: the readings in the window and their gaps; utilization (Windows processor-utility counter, above 100% over the base
        clock), package power, hottest core, mean of 20 cores, free memory, each as mean / min / max; the number of readings at or above
        100 C, 102 C and 104 C (TjMax 105 C) with their times; hours at full load by two definitions (readings with utilization >= 100%,
        and the sum of the loop's 13-copy windows from driver.txt); the crash entries of crashes.txt after the window start.
        A planted check: --selftest builds a log with a gap and a 105 C row and must report both."""
import os, re, sys, datetime as dt

HERE = os.path.dirname(os.path.abspath(__file__))
PAT = re.compile(r"^(\d{4}-\d\d-\d\d) (\d\d:\d\d:\d\d)Z .*?util% (\d+) pkgW ([\d.]+) .*?free_GB ([\d.]+) temp max (\d+).*?core temps C min/mean/max \d+/([\d.]+)/")


def parse(lines):
    rows = []
    for line in lines:
        m = PAT.match(line)
        if m:
            t = dt.datetime.fromisoformat(m.group(1) + "T" + m.group(2))
            rows.append((t, int(m.group(3)), float(m.group(4)), float(m.group(5)), int(m.group(6)), float(m.group(7))))
    return rows


def stat(v): return f"mean {sum(v) / len(v):.1f}, min {min(v)}, max {max(v)}"


def report(rows, start, end, out=print):
    r = [x for x in rows if start <= x[0] <= end]
    out(f"window {start} to {end} UTC: {len(r)} readings, first {r[0][0].time()}, last {r[-1][0].time()}")
    gaps = [(a[0], b[0]) for a, b in zip(r, r[1:]) if (b[0] - a[0]).total_seconds() > 330]
    out(f"gaps above 5.5 min between readings: {[(str(a.time()), str(b.time())) for a, b in gaps] if gaps else 'none'}")
    out(f"utilization %   {stat([x[1] for x in r])}")
    out(f"package power W {stat([x[2] for x in r])}")
    out(f"free memory GB  {stat([x[3] for x in r])}")
    out(f"hottest core C  {stat([x[4] for x in r])}")
    out(f"mean of 20 cores C {stat([x[5] for x in r])}")
    for lim in (100, 102, 104, 105):
        hit = [x for x in r if x[4] >= lim]
        out(f"readings with the hottest core >= {lim} C: {len(hit)}" + (" at " + ", ".join(f"{x[0].strftime('%d %H:%M')} ({x[4]} C, {x[2]} W)" for x in hit[:30]) if hit and lim >= 104 else ""))
    full = [x for x in r if x[1] >= 100]
    out(f"readings with utilization >= 100%: {len(full)} of {len(r)}, about {len(full) * 5 / 60:.1f} h of {len(r) * 5 / 60:.1f} h")
    p = max(r, key=lambda x: x[2])
    out(f"peak package power {p[2]} W at {p[0]} (hottest core then {p[4]} C, utilization {p[1]}%)")
    return r


def selftest():
    t0 = dt.datetime(2026, 11, 9, 1, 30)
    lines = []
    for i in range(10):
        t = t0 + dt.timedelta(minutes=5 * i + (20 if i >= 5 else 0))
        temp = 105 if i == 7 else 80
        lines.append(f"{t.date()} {t.time()}Z  clock MHz min/mean/max 3300/3540/3900 perf% 130 util% {110 if i == 7 else 50} pkgW {150.0 if i == 7 else 60.0} coreW 1 free_GB 40.0 temp max {temp} threads 20 | CoreTemp x core temps C min/mean/max 50/60.5/{temp} [1] core load% [1] VID")
    out = []
    report(parse(lines), t0, t0 + dt.timedelta(hours=2), out=out.append)
    ok = any("gaps above" in x and "none" not in x for x in out) and any(">= 105 C: 1" in x for x in out) and any("utilization >= 100%: 1 of 10" in x for x in out)
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    start = dt.datetime.fromisoformat(sys.argv[1] if len(sys.argv) > 1 else "2026-11-09T01:30:41")
    end = dt.datetime.fromisoformat(sys.argv[2] if len(sys.argv) > 2 else "2026-11-10T01:30:00")
    rows = parse(open(os.path.join(HERE, "sensor_log.txt"), encoding="utf-8", errors="replace"))
    report(rows, start, end)
    print()
    print("crashes.txt entries (all, with their dates):")
    for line in open(os.path.join(HERE, "crashes.txt"), encoding="utf-8", errors="replace"):
        print("  " + line.rstrip()[:170])
    ct = os.path.join(HERE, "crash_temps.txt")
    print("crash_temps.txt:", open(ct).read().strip() if os.path.exists(ct) and os.path.getsize(ct) else "empty or absent (no event since the watchers' restart)")
    print("windows of the 13-copy loop (driver.txt): " + "; ".join(l.strip() for l in open(os.path.join(HERE, "driver.txt")) if "round" in l and "13 copies" in l))

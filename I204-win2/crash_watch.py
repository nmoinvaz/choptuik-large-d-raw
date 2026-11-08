#!/usr/bin/env python3
"""Watches the Windows logs for a crash of ANY process and records it with a CPU clock/load/power reading (issue #177).
Read only: it kills nothing and changes no setting. Polls every 60 s for
  - Application Error (event 1000) and Application Hang (1002),
  - a new Windows Error Reporting report directory (ReportArchive or ReportQueue),
  - WHEA-Logger events, Kernel-Power 41, BugCheck 1001 and unexpected-shutdown 6008 in the System log.
On the first poll with something new it appends a line per item to crashes.txt, the reading to crash_temps.txt (the CPU
temperature is n/a, see sensors.py) and exits 18, so that the session is woken. State (last record ids, known report
directories) is kept in --state; the first run baselines it and backfills the last Application Errors as 'before watcher'.

    python crash_watch.py --state FILE [--interval 60]"""
import argparse, datetime as dt, json, os, subprocess, sys, time
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sensors

NS = "{http://schemas.microsoft.com/win/2004/08/events/event}"
WER = ["C:/ProgramData/Microsoft/Windows/WER/ReportArchive", "C:/ProgramData/Microsoft/Windows/WER/ReportQueue"]
Q = {
    "app1000": ("Application", "*[System[Provider[@Name='Application Error'] and (EventID=1000)]]"),
    "app1002": ("Application", "*[System[Provider[@Name='Application Hang'] and (EventID=1002)]]"),
    "whea": ("System", "*[System[Provider[@Name='Microsoft-Windows-WHEA-Logger']]]"),
    "sys": ("System", "*[System[(EventID=41 or EventID=1001 or EventID=6008) and (Provider[@Name='Microsoft-Windows-Kernel-Power'] "
                      "or Provider[@Name='Microsoft-Windows-WER-SystemErrorReporting'] or Provider[@Name='EventLog'])]]"),
}


def events(log, query, count):
    out = subprocess.run(["wevtutil", "qe", log, "/q:" + query, f"/c:{count}", "/rd:true", "/f:xml"],
                         capture_output=True, text=True, timeout=60).stdout
    res = []
    for e in ET.fromstring("<r>" + out + "</r>"):
        s = e.find(NS + "System")
        res.append(dict(id=int(s.find(NS + "EventRecordID").text), eid=int(s.find(NS + "EventID").text),
                        time=s.find(NS + "TimeCreated").get("SystemTime")[:19].replace("T", " ") + "Z",
                        prov=s.find(NS + "Provider").get("Name"),
                        data=[(d.text or "") for d in e.iter(NS + "Data")]))
    return sorted(res, key=lambda x: x["id"])


def describe(kind, ev):
    d = ev["data"]
    if kind == "app1000" and len(d) >= 9:
        pid = int(d[8], 16) if d[8].lower().startswith("0x") else d[8]
        return (f"{ev['time']}  event 1000  process {d[0]} {d[1]}  module {d[3]}  offset 0x{d[7]}  code {d[6]}  "
                f"pid {pid}  path {d[10] if len(d) > 10 else ''}")
    return f"{ev['time']}  {kind} event {ev['eid']} {ev['prov']}  data {' | '.join(x[:80] for x in d[:6])}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--state", required=True)
    ap.add_argument("--interval", type=float, default=60)
    a = ap.parse_args()
    try:
        st = json.load(open(a.state))
    except (OSError, ValueError):
        st = None
    crashes, temps = os.path.join(HERE, "crashes.txt"), os.path.join(HERE, "crash_temps.txt")
    if st is None:
        st = {"last": {}, "wer": {}}
        with open(crashes, "a") as f:
            f.write("# crashes of any process on win2, from the Application and System logs; temperature n/a (no built-in source)\n")
            for ev in events("Application", Q["app1000"][1], 50):
                f.write("before watcher: " + describe("app1000", ev) + "\n")
        for k, (log, q) in Q.items():
            evs = events(log, q, 1)
            st["last"][k] = evs[-1]["id"] if evs else 0
        st["wer"] = {d: sorted(os.listdir(d)) for d in WER if os.path.isdir(d)}
        json.dump(st, open(a.state, "w"))
    print("crash_watch up, last ids", st["last"], flush=True)
    while True:
        new = []
        for k, (log, q) in Q.items():
            for ev in events(log, q, 50):
                if ev["id"] > st["last"].get(k, 0):
                    new.append((k, ev))
                    st["last"][k] = ev["id"]
        for d in WER:
            if os.path.isdir(d):
                for name in sorted(set(os.listdir(d)) - set(st["wer"].get(d, []))):
                    new.append(("wer-report", dict(eid=0, prov=os.path.basename(d), id=0, data=[name],
                                                   time=dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"))))
                st["wer"][d] = sorted(os.listdir(d))
        if new:
            now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")
            try:
                reading = sensors.fmt(sensors.read())
            except Exception as e:
                reading = f"reading failed: {e!r}"
            lines = [describe(k, ev) for k, ev in new]
            with open(crashes, "a") as f:
                f.write("\n".join(lines) + "\n")
            with open(temps, "a") as f:
                f.write(f"detected {now}, reading taken at {dt.datetime.now(dt.timezone.utc):%H:%M:%SZ}: {reading}\n")
                f.write("".join("    " + l + "\n" for l in lines))
            json.dump(st, open(a.state, "w"))
            print("NEW\n" + "\n".join(lines) + "\n" + reading, flush=True)
            return 18
        json.dump(st, open(a.state, "w"))
        time.sleep(a.interval)


if __name__ == "__main__":
    sys.exit(main())

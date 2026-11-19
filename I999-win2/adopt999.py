"""#999: cap and exit-file duty for runs whose scheduler was replaced (the coordinator dropped XI 0.14 while 0.12 and 0.13 ran).

    python adopt999.py [--cap_s 3600] TAG:PID:START_UTC [TAG:PID:START_UTC ...]      START_UTC = YYYY-MM-DD_HH:MM:SS (an underscore, no space)
    python adopt999.py --selftest [--mutate=nokill]

Polls each PID (the run's launcher process, which ends when the run's main ends) every 10 s; at START + cap it kills the run's whole tree
(taskkill /T /F, hier.py's spawn workers survive a kill of the main process). Writes logs/<TAG>.exit as chain999.py does, except that the exit
code of an adopted process is not available ("exit not captured"); the line says whether the log has a FIXED-A line.
"""
import calendar, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
LOGS = os.path.join(HERE, "logs")


def alive(pid):
    out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True).stdout
    return str(pid) in out.split()


def main():
    a = sys.argv[1:]
    selftest = "--selftest" in a
    cap = float(a[a.index("--cap_s") + 1]) if "--cap_s" in a else 3600.0
    items = [t for t in a if t.count(":") >= 2 and not t.startswith("--")]
    if selftest:
        p = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"], creationflags=0x200)
        items, cap = [f"adopt_selftest:{p.pid}:" + time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())], 3.0
    jobs = []
    for t in items:
        tag, pid, start = t.split(":", 2)
        jobs.append((tag, int(pid), calendar.timegm(time.strptime(start.replace("_", " "), "%Y-%m-%d %H:%M:%S"))))
    print(time.strftime("%H:%M:%S UTC", time.gmtime()), "adopting", jobs, "cap", cap, "s", flush=True)
    res = {}
    while jobs:
        time.sleep(2 if selftest else 10)
        for tag, pid, t0 in list(jobs):
            note = ""
            if alive(pid) and time.time() - t0 > cap:
                if "--mutate=nokill" not in a:
                    subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)
                    time.sleep(1)
                note = f" (killed the process tree at the {cap:g} s cap, taskkill /T /F /PID {pid})"
            elif alive(pid):
                continue
            log = os.path.join(LOGS, tag + ".log")
            fixed = os.path.exists(log) and "FIXED-A M" in open(log, encoding="utf-8", errors="replace").read()
            msg = (f"exit not captured (the run was adopted after its scheduler was replaced){note}; ended "
                   f"{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())} UTC after {time.time() - t0:.0f} s; FIXED-A line in the log: {fixed}")
            if not selftest:
                open(os.path.join(LOGS, tag + ".exit"), "w").write(msg + "\n")
            print(tag, msg, flush=True); res[tag] = (pid, note); jobs.remove((tag, pid, t0))
    if selftest:
        pid, note = next(iter(res.values()))
        ok = "killed" in note and not alive(pid)
        print("selftest", "PASS" if ok else "FAIL", flush=True)
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
        return 0 if ok else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

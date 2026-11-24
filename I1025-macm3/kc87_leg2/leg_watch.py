#!/usr/bin/env python3
"""leg_watch.py: the 3 h per point stop of the k_c 87 leg2 (t5's order, #1025): kills the leap by exact pid when no point has been recorded for CAP seconds.
usage: leg_watch.py --rec RECORDS.jsonl --since LEAP.started --exits EXITS --rootkey "leap87 root pid" --stop STOP.txt --done DONE [--cap 10800] [--poll 30]
       leg_watch.py --selftest [--mutate=cap]
The clock of a point starts at the leap's start (the mtime of --since) or at the last write of RECORDS.jsonl, whichever is later (the leap appends one line per accepted point;
retries of a failed solve belong to the point's time). The kill is the pinned leap_guard.py's own stop_leap(pid): exact pid, only when the command line holds ell_leap.py,
the process tree killed through the shims (macOS: shims_mac/ first on PATH). --selftest plants (last, now, cap) cases and a dummy with and without ell_leap.py in its command line;
--mutate=cap disables the cap and the selftest must then exit 1."""
import os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "in"))
import leap_guard as g

def over(now, last, cap, mutate=None):
    return mutate != "cap" and (now - last) > cap

def selftest(mutate=None):
    bad = []
    for name, now, last, cap, want in (("1 s past the cap", 10801, 0, 10800, True), ("exactly at the cap", 10800, 0, 10800, False), ("a point just recorded", 20000, 19990, 10800, False),
                                       ("a long first point", 40000, 100, 10800, True), ("2.9 h", 10440, 0, 10800, False)):
        got = over(now, last, cap, mutate)
        if got != want: bad.append("%s: stop %s, want %s" % (name, got, want))
    py = sys.executable
    code = "import time; time.sleep(120)"
    p_yes = subprocess.Popen([py, "-c", code, g.KEY], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    p_no = subprocess.Popen([py, "-c", code, "other.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2)
    try:
        r_yes, r_no = g.stop_leap(p_yes.pid), g.stop_leap(p_no.pid)
        time.sleep(1)
        if r_yes != "killed" or g.alive(p_yes.pid): bad.append("the dummy with %s was not killed (%s)" % (g.KEY, r_yes))
        if r_no != "left" or not g.alive(p_no.pid): bad.append("the dummy without %s was not left alone (%s)" % (g.KEY, r_no))
    finally:
        for p in (p_yes, p_no):
            if p.poll() is None: p.kill()
    for b in bad: print("SELFTEST FAIL:", b)
    print("selftest %s%s" % ("FAILS" if bad else "passes", " (mutate=%s)" % mutate if mutate else ""))
    return 1 if bad else 0

def main():
    a = sys.argv[1:]
    mutate = next((x.split("=", 1)[1] for x in a if x.startswith("--mutate=")), None)
    if "--selftest" in a: sys.exit(selftest(mutate))
    opt = {k: a[a.index(k) + 1] for k in ("--rec", "--since", "--exits", "--rootkey", "--stop", "--done", "--cap", "--poll") if k in a}
    cap, poll = float(opt.get("--cap", 10800)), float(opt.get("--poll", 30))
    pid = None
    while pid is None:
        if os.path.exists(opt["--done"]): return
        m = re.findall(re.escape(opt["--rootkey"]) + r" (\d+)", open(opt["--exits"]).read()) if os.path.exists(opt["--exits"]) else []
        if m: pid = int(m[-1])
        else: time.sleep(poll)
    print("watch on leap root pid %d, cap %g s per point" % (pid, cap), flush=True)
    while not os.path.exists(opt["--done"]):
        last = os.path.getmtime(opt["--since"])
        if os.path.exists(opt["--rec"]): last = max(last, os.path.getmtime(opt["--rec"]))
        now = time.time()
        if over(now, last, cap, mutate):
            r = g.stop_leap(pid)
            msg = "STOP: no point for %.0f s (cap %g s); leap root pid %d: %s; %s" % (now - last, cap, pid, r, time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
            open(opt["--stop"], "a").write(msg + "\n"); print(msg, flush=True)
            return
        time.sleep(poll)

if __name__ == "__main__":
    main()

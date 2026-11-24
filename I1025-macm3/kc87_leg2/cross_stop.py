#!/usr/bin/env python3
"""cross_stop.py: part c's early stop (t5, hc 24 Nov): stop the leap once two consecutive scanned roots are below 0 (the crossing of lambda_1 = 0 is then bracketed).
usage: cross_stop.py --exits EXITS --rootkey "leap87c root pid" --stop STOP.txt --done DONE [--poll 60]
       cross_stop.py --selftest [--mutate=cross]
Every poll it asks `chain_next.py crossed` (YES when the two largest scanned roots in roots87.txt are both below 0); on YES it stops the leap by the pinned leap_guard.py's stop_leap(pid) (exact pid, only when the command line holds ell_leap.py,
the tree killed through shims_mac), writes STOP.txt with the two roots and tells t5 by hc. --selftest plants YES and NO answers and a dummy process with and without ell_leap.py in its command line; --mutate=cross ignores YES and the selftest must then exit 1."""
import os, re, shutil, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "in"))
import leap_guard as g
CHAIN = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/chain_next.py")
ROOTS = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda/roots87.txt")

def decide(answer, mutate=None):
    return mutate != "cross" and answer.strip() == "YES"

def selftest(mutate=None):
    bad = []
    for ans, want in (("YES", True), ("NO", False), ("", False), ("YES\n", True)):
        if decide(ans, mutate) != want: bad.append("answer %r: stop %s, want %s" % (ans, decide(ans, mutate), want))
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
    opt = {k: a[a.index(k) + 1] for k in ("--exits", "--rootkey", "--stop", "--done", "--poll") if k in a}
    poll = float(opt.get("--poll", 60))
    pid = None
    while pid is None:
        if os.path.exists(opt["--done"]): return
        m = re.findall(re.escape(opt["--rootkey"]) + r" (\d+)", open(opt["--exits"]).read()) if os.path.exists(opt["--exits"]) else []
        if m: pid = int(m[-1])
        else: time.sleep(poll)
    print("crossing watch on leap root pid %d" % pid, flush=True)
    while not os.path.exists(opt["--done"]):
        ans = subprocess.run([sys.executable, CHAIN, "crossed"], capture_output=True, text=True).stdout
        if decide(ans, mutate):
            rows = [l.split()[:2] for l in open(ROOTS) if l.strip() and not l.startswith("#")]
            last2 = sorted((float(d), float(r)) for d, r in rows)[-2:]
            r = g.stop_leap(pid)
            msg = "STOP: two consecutive scanned roots below 0 (D %r: %.6f, D %r: %.6f), the crossing of lambda_1 = 0 is bracketed; leap root pid %d: %s; %s" % (
                last2[0][0], last2[0][1], last2[1][0], last2[1][1], pid, r, time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
            open(opt["--stop"], "a").write(msg + "\n"); print(msg, flush=True)
            hc = shutil.which("hc")
            if hc: subprocess.run([hc, "send", "nathans-macbook-air-m5-3/t5", "macm3 #1025 kc87_leg2 part c " + msg], capture_output=True)
            return
        time.sleep(poll)

if __name__ == "__main__":
    main()

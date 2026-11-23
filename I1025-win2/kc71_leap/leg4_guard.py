#!/usr/bin/env python3
"""leg4_guard.py: stop rule and point table of leg 4 of the k_c 71 leap (#1025, the coordinator's hc of 2026-11-23).

usage: leg4_guard.py --rec RECORDS.jsonl --n0 N --exits EXITS --log LEAP.log --out POINTS.txt --stop STOP.txt --done DONE
                     [--poll 15] [--mutate=slope|sigma]
       leg4_guard.py --selftest [--mutate=slope|sigma]

Reads the leap's record file (data/l1kc71Lw1025c.jsonl, accepted points only; the first N0 records are leg 3's and
earlier). For every new record it appends one row to POINTS.txt (D, Delta, dDelta/dD against the previous accepted point,
the smallest regular singular value sigma_reg = sv_reg_small[0], |J^+ dF/dn| = tan_norm, this step's h and the next h,
psi-constraint, |F|, steps, seconds), and it STOPS the leap when
  (1) dDelta/dD changes sign (the slope of a new step has the other sign than the previous slope, or is zero), or
  (2) sigma_reg falls below 1e-12.
Stopping = taskkill /T /F of the leap's root pid (read from EXITS, "leap4 root pid N") after the check that its command line
holds ell_leap.py, then STOP.txt with the reason and the numbers. The next h comes from the "fold watch:" line the leap prints
after the point. Heartbeat: POINTS.txt.hb (a time stamp every poll). --selftest plants the cases (and a dummy process with and
without ell_leap.py in its command line) and exits 0 when every case reads as written; --mutate=slope or --mutate=sigma
disables one rule and the selftest must then exit 1."""
import json
import os
import re
import subprocess
import sys
import time

SIGMA_BAR = 1e-12
KEY = "ell_leap.py"


def verdict(prev_slope, slope, sigma, mutate=None):
    why = []
    if mutate != "slope" and (slope == 0.0 or (slope > 0) != (prev_slope > 0)):
        why.append("dDelta/dD turned: %.6g after %.6g" % (slope, prev_slope))
    if mutate != "sigma" and sigma < SIGMA_BAR:
        why.append("sigma_reg %.4g is below %.0e" % (sigma, SIGMA_BAR))
    return why


def cmdline(pid):
    r = subprocess.run(["powershell", "-NoProfile", "-Command",
                        "(Get-CimInstance Win32_Process -Filter 'ProcessId=%d').CommandLine" % pid],
                       capture_output=True, text=True)
    s = r.stdout.strip()
    return s or None


def stop_leap(pid, key=KEY):
    cl = cmdline(pid)
    if cl is None:
        return "gone"
    if key not in cl:
        return "left"
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)
    return "killed"


def alive(pid):
    return cmdline(pid) is not None


def selftest(mutate=None):
    bad = []
    cases = [("increasing, sigma 1.5e-11", 0.0264, 0.0300, 1.5e-11, False),
             ("slope turns negative", 0.0264, -0.0010, 1.5e-11, True),
             ("slope exactly zero", 0.0264, 0.0, 1.5e-11, True),
             ("negative slope turns positive", -0.02, 0.01, 1.5e-11, True),
             ("sigma 9.9e-13", 0.0264, 0.0300, 9.9e-13, True),
             ("sigma 1.0e-12 is not below", 0.0264, 0.0300, 1.0e-12, False),
             ("sigma 1.0001e-12", 0.0264, 0.0300, 1.0001e-12, False)]
    for name, ps, s, sg, want in cases:
        got = bool(verdict(ps, s, sg, mutate))
        if got != want:
            bad.append("%s: stop %s, want %s" % (name, got, want))
    py = sys.executable
    p_yes = subprocess.Popen([py, "-c", "import time; time.sleep(120)", KEY])
    p_no = subprocess.Popen([py, "-c", "import time; time.sleep(120)", "other.py"])
    time.sleep(2)
    try:
        r_yes, r_no = stop_leap(p_yes.pid), stop_leap(p_no.pid)
        time.sleep(1)
        if r_yes != "killed" or alive(p_yes.pid):
            bad.append("the dummy with %s was not killed (%s)" % (KEY, r_yes))
        if r_no != "left" or not alive(p_no.pid):
            bad.append("the dummy without %s was not left alone (%s)" % (KEY, r_no))
    finally:
        for p in (p_yes, p_no):
            if p.poll() is None:
                p.kill()
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s%s" % ("FAILS" if bad else "passes", " (mutate=%s)" % mutate if mutate else ""))
    return 1 if bad else 0


def next_h(logtxt, D, h):
    lines = logtxt.splitlines()
    key = '"D": %r,' % D
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].startswith("{") and key in lines[i]:
            if i + 1 < len(lines) and lines[i + 1].startswith("fold watch:"):
                m = re.search(r"h -> ([0-9.eE+-]+)", lines[i + 1])
                return float(m.group(1)) if m else h
            return h
    return h


def main():
    a = sys.argv[1:]
    mutate = next((x.split("=", 1)[1] for x in a if x.startswith("--mutate=")), None)
    if "--selftest" in a:
        sys.exit(selftest(mutate))
    opt = {}
    for k in ("--rec", "--n0", "--exits", "--log", "--out", "--stop", "--done", "--poll"):
        if k in a:
            opt[k] = a[a.index(k) + 1]
    rec_path, n0 = opt["--rec"], int(opt["--n0"])
    poll = float(opt.get("--poll", 15))
    hb = opt["--out"] + ".hb"
    pid = None
    while pid is None:
        if os.path.exists(opt["--done"]):
            return
        m = re.findall(r"leap4 root pid (\d+)", open(opt["--exits"]).read()) if os.path.exists(opt["--exits"]) else []
        if m:
            pid = int(m[-1])
        else:
            time.sleep(poll)
    hist = [json.loads(x) for x in open(rec_path) if x.strip()]
    assert len(hist) >= n0 >= 2, "the record file has %d records, expected at least %d" % (len(hist), n0)
    prev = hist[n0 - 1]
    prev_slope = (prev["Delta"] - hist[n0 - 2]["Delta"]) / (prev["D"] - hist[n0 - 2]["D"])
    done = n0
    if not os.path.exists(opt["--out"]):
        open(opt["--out"], "w").write("| D | Delta | dDelta/dD | sigma_reg | J+dF/dn | h | next h | constraint | F | steps | s |\n"
                                      "|---|---|---|---|---|---|---|---|---|---|---|\n")
    print("guard on leap root pid %d, %d records before leg 4, last D %g, previous slope %.6g" % (pid, n0, prev["D"], prev_slope),
          flush=True)
    while not os.path.exists(opt["--done"]):
        open(hb, "w").write(time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + "\n")
        lines = [x for x in open(rec_path) if x.strip()]
        while len(lines) > done:
            time.sleep(6)
            rec = json.loads(lines[done])
            slope = (rec["Delta"] - prev["Delta"]) / (rec["D"] - prev["D"])
            sigma, tn = rec["sv_reg_small"][0], rec["tan_norm"]
            nh = next_h(open(opt["--log"]).read(), rec["D"], rec["h"])
            row = "| %.8g | %.12f | %.6f | %.4e | %.4f | %g | %g | %.3e | %.3e | %d | %d |" % (
                rec["D"], rec["Delta"], slope, sigma, tn, rec["h"], nh, rec["constraint"], rec["F"], rec["steps"], rec["seconds"])
            open(opt["--out"], "a").write(row + "\n")
            print("POINT " + row, flush=True)
            why = verdict(prev_slope, slope, sigma, mutate)
            prev, prev_slope, done = rec, slope, done + 1
            if why:
                r = stop_leap(pid)
                msg = "STOP at D %g: %s; leap root pid %d: %s; %s" % (rec["D"], "; ".join(why), pid, r,
                                                                     time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
                open(opt["--stop"], "w").write(msg + "\n" + row + "\n")
                print(msg, flush=True)
                return
        time.sleep(poll)


if __name__ == "__main__":
    main()

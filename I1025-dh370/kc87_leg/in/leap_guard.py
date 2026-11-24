#!/usr/bin/env python3
"""leap_guard.py: stop rule and point table of an ell_leap.py leg (#1025; the coordinator's rule of 2026-11-23 ~12:30 UTC).
Replaces leg4_guard.py, whose rule (2), sigma_reg < 1e-12, cannot fire: sv_reg_small lies above the null cutoff 1e-12 sigma_max.

usage: leap_guard.py --rec RECORDS.jsonl --exits EXITS --rootkey "leap4 root pid" --log LEAP.log --out POINTS.txt --stop STOP.txt --done DONE
                     (--n0 N | --seeds SEED_A.jsonl SEED_B.jsonl) [--poll 15] [--settle 6] [--mutate=slope|cos|nnull]
       leap_guard.py --selftest [--mutate=slope|cos|nnull]

--n0 N: the first N records of RECORDS.jsonl are earlier legs'; the last two give the previous slope, the last one the previous n_null.
--seeds A B: RECORDS.jsonl is the new leg's own file (empty at the start); the previous points are the last records of the two seed record
files (no n_null there, so the n_null rule starts at the second point).
For every new record a row goes to POINTS.txt: D, Delta, dDelta/dD against the previous accepted point, sigma_reg = sv_reg_small[0],
|J^+ dF/dn| = tan_norm, this step's h and the next h (the leap's "fold watch" line), psi-constraint, |F|, steps, seconds, n_null, the
null cutoff 1e-12 sigma_max and the largest cos_t_reg. The leap is STOPPED (taskkill /T /F of the root pid after the check that its
command line holds ell_leap.py, then STOP.txt with the reason) when
  (1) dDelta/dD has the other sign than at the previous step or is zero, or
  (2) the largest cos_t_reg is >= 0.5 (the tangent lies along a weak regular mode), or
  (3) n_null rises (a mode sinks into the null set) with the largest cos_t_reg >= 0.3.
A mode entering the regular set (n_null falls, D 20.75 of leg 3) does not stop. Heartbeat: POINTS.txt.hb. --selftest plants the cases and a
dummy process with and without ell_leap.py in its command line and exits 0 when all read as written; each --mutate disables one rule and
the selftest must then exit 1."""
import json
import os
import re
import subprocess
import sys
import time

COS_BAR = 0.5
COS_NNULL_BAR = 0.3
KEY = "ell_leap.py"


def verdict(prev_slope, slope, prev_nnull, nnull, maxcos, mutate=None):
    why = []
    if mutate != "slope" and (slope == 0.0 or (slope > 0) != (prev_slope > 0)):
        why.append("dDelta/dD turned: %.6g after %.6g" % (slope, prev_slope))
    if mutate != "cos" and maxcos >= COS_BAR:
        why.append("max cos_t_reg %.4g >= %g" % (maxcos, COS_BAR))
    if mutate != "nnull" and prev_nnull is not None and nnull > prev_nnull and maxcos >= COS_NNULL_BAR:
        why.append("n_null rose %d -> %d with max cos_t_reg %.4g >= %g" % (prev_nnull, nnull, maxcos, COS_NNULL_BAR))
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
    # name, prev_slope, slope, prev_nnull, nnull, maxcos, stop?
    cases = [("normal, the D 20.75 look: n_null falls, cos 0.051", 0.0264, 0.0270, 64, 63, 0.051, False),
             ("normal, flat n_null, cos 0.05", 0.0264, 0.0270, 63, 63, 0.05, False),
             ("slope turns negative", 0.0264, -0.0010, 63, 63, 0.05, True),
             ("slope exactly zero", 0.0264, 0.0, 63, 63, 0.05, True),
             ("negative slope turns positive", -0.02, 0.01, 63, 63, 0.05, True),
             ("cos exactly 0.5, n_null flat", 0.0264, 0.0270, 63, 63, 0.5, True),
             ("cos 0.6, n_null flat", 0.0264, 0.0270, 63, 63, 0.6, True),
             ("cos 0.49, n_null flat", 0.0264, 0.0270, 63, 63, 0.49, False),
             ("n_null rises with cos 0.3", 0.0264, 0.0270, 63, 64, 0.3, True),
             ("n_null rises with cos 0.35", 0.0264, 0.0270, 63, 64, 0.35, True),
             ("n_null rises with cos 0.29", 0.0264, 0.0270, 63, 64, 0.29, False),
             ("n_null rises by two with cos 0.4", 0.0264, 0.0270, 63, 65, 0.4, True),
             ("no n_null history (seed), cos 0.2", 0.0264, 0.0270, None, 64, 0.2, False),
             ("no n_null history (seed), cos 0.6", 0.0264, 0.0270, None, 64, 0.6, True)]
    for name, ps, s, pn, nn, c, want in cases:
        got = bool(verdict(ps, s, pn, nn, c, mutate))
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


def last_record(path):
    return json.loads([x for x in open(path) if x.strip()][-1])


def main():
    a = sys.argv[1:]
    mutate = next((x.split("=", 1)[1] for x in a if x.startswith("--mutate=")), None)
    if "--selftest" in a:
        sys.exit(selftest(mutate))
    opt = {}
    for k in ("--rec", "--n0", "--exits", "--rootkey", "--log", "--out", "--stop", "--done", "--poll", "--settle"):
        if k in a:
            opt[k] = a[a.index(k) + 1]
    poll, settle = float(opt.get("--poll", 15)), float(opt.get("--settle", 6))
    hb = opt["--out"] + ".hb"
    pid = None
    while pid is None:
        if os.path.exists(opt["--done"]):
            return
        m = re.findall(re.escape(opt["--rootkey"]) + r" (\d+)", open(opt["--exits"]).read()) if os.path.exists(opt["--exits"]) else []
        if m:
            pid = int(m[-1])
        else:
            time.sleep(poll)
    if "--seeds" in a:
        i = a.index("--seeds")
        ra, rb = last_record(a[i + 1]), last_record(a[i + 2])
        prev2, prev, done = ra, rb, 0
    else:
        n0 = int(opt["--n0"])
        hist = [json.loads(x) for x in open(opt["--rec"]) if x.strip()]
        assert len(hist) >= n0 >= 2, "the record file has %d records, expected at least %d" % (len(hist), n0)
        prev2, prev, done = hist[n0 - 2], hist[n0 - 1], n0
    prev_slope = (prev["Delta"] - prev2["Delta"]) / (prev["D"] - prev2["D"])
    prev_nnull = prev.get("n_null")
    if not os.path.exists(opt["--out"]):
        open(opt["--out"], "w").write("| D | Delta | dDelta/dD | sigma_reg | J+dF/dn | h | next h | constraint | F | steps | s | n_null | cutoff | max cos_t_reg |\n"
                                      "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    print("guard on leap root pid %d, %d records before this leg, last D %g, previous slope %.6g, previous n_null %s" % (
        pid, done, prev["D"], prev_slope, prev_nnull), flush=True)
    while not os.path.exists(opt["--done"]):
        open(hb, "w").write(time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + "\n")
        lines = [x for x in open(opt["--rec"]) if x.strip()] if os.path.exists(opt["--rec"]) else []
        while len(lines) > done:
            time.sleep(settle)
            rec = json.loads(lines[done])
            slope = (rec["Delta"] - prev["Delta"]) / (rec["D"] - prev["D"])
            sigma, tn = rec["sv_reg_small"][0], rec["tan_norm"]
            nnull, maxcos, cutoff = rec["n_null"], max(rec["cos_t_reg"]), 1e-12 * rec["sv_J_max"]
            nh = next_h(open(opt["--log"]).read(), rec["D"], rec["h"])
            row = "| %.8g | %.12f | %.6f | %.4e | %.4f | %g | %g | %.3e | %.3e | %d | %d | %d | %.3e | %.4f |" % (
                rec["D"], rec["Delta"], slope, sigma, tn, rec["h"], nh, rec["constraint"], rec["F"], rec["steps"], rec["seconds"],
                nnull, cutoff, maxcos)
            open(opt["--out"], "a").write(row + "\n")
            print("POINT " + row, flush=True)
            why = verdict(prev_slope, slope, prev_nnull, nnull, maxcos, mutate)
            prev, prev_slope, prev_nnull, done = rec, slope, nnull, done + 1
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

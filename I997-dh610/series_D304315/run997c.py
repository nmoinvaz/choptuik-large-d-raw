#!/usr/bin/env python3
"""run997c.py | --selftest [--mutate]: #997's Delta series at D 3.04315 (M 320, N 8) with the coordinator's pilot stop rule (his comment of 2026-11-22): anm_lowd.py from a worktree at origin/main (ab0ddb8c) with venv-i1058, 10 threads, nice 10;
the command is diffed against his before the launch (cmddiff997.py; a diff stops the launch). Rules: each order's time is reported (exits_997c.txt 'ORDER k' lines); if order 2 is not done within 3 h, or an order's solve does not converge ('converged False' on a z_k line),
the run is stopped by TERM to its exact pid and reported ('PILOT END ... STOP'); 'PILOT END ... order 2 done' marks the pilot's end otherwise; the series file is saved before the target stage, which is stopped by exact pid past 30 min after it appears;
'SERIES END exit rc' marks the process's end. A sampler logs RSS, CPU, MemAvailable and load every 60 s (rss_997c.log). --selftest checks the parsers and decisions on planted log lines; --mutate loosens each bar and must fail."""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = "/home/nathan/Source/choptuik-large-d-raw"
WT = "/home/nathan/Source/choptuik-large-d-997c"
PY = "/home/nathan/Source/venv-i1058/bin/python"
OUT = f"{RAW}/I997-dh610/series_D304315"
STATE = f"{RAW}/I945-win2/leg/states/lowD343_D3.043150_M320.npz"
SERIES = f"{OUT}/series_D3.04315_M320_N8.npz"
LOG = f"{HERE}/exits_997c.txt"
ORDER2_WALL, RULE30 = 3 * 3600, 1800


def say(msg):
    with open(LOG, "a") as f:
        f.write(f"997c {msg} {time.strftime('%F %T', time.gmtime())} UTC\n")


ORD = re.compile(r"^  z_(\d+): \|z\| (\S+), \|rhs\| (\S+), (\d+) products, converged (True|False), (\d+) \+ (\d+) s", re.M)
BASE = re.compile(r"^base .*?\|F\| (\S+), pivots (\S+)\.\.(\S+), (\d+) s", re.M)


def orders(text):
    """[(k, products, converged, seconds)] of the z_k lines"""
    return [(int(m.group(1)), int(m.group(4)), m.group(5) == "True", int(m.group(6)) + int(m.group(7))) for m in ORD.finditer(text)]


def decision(text, wall, order2_wall=ORDER2_WALL):
    """None to go on, or the reason to stop: an order whose solve did not converge, or order 2 not done within order2_wall"""
    o = orders(text)
    for k, p, c, s in o:
        if not c:
            return f"order {k}'s solve did not converge ({p} products)"
    if wall > order2_wall and not any(k == 2 for k, _, _, _ in o):
        return f"order 2 not done within {order2_wall / 3600:.0f} h"
    return None


def selftest(mutate):
    ok = True
    o2 = 9 * 3600 if mutate else ORDER2_WALL
    t1 = "base /x.npz: D 3.04315, M 320, |F| 7.35e-21, pivots 1.8e-11..5.1e+01, 3840 s\n  z_1: |z| 1.0e+04, |rhs| 1.20e+02, 4 products, converged True, 100 + 50 s\n"
    t2 = t1 + "  z_2: |z| 2.0e+05, |rhs| 6.15e+03, 4 products, converged True, 110 + 52 s\n"
    tf = t1 + "  z_2: |z| 2.0e+05, |rhs| 6.15e+03, 40 products, converged False, 110 + 52 s\n"
    cases = [(orders(t2) == [(1, 4, True, 150), (2, 4, True, 162)], True), (decision(t2, 5 * 3600, o2) is None, True), (decision(t1, 2 * 3600, o2) is None, True),
             (decision(t1, 3.5 * 3600, o2) is not None, True), (decision(tf, 100, o2 if not mutate else 0) is not None, True),
             (BASE.search(t1) is not None and BASE.search(t1).group(2) == "1.8e-11", True), (orders("nothing") == [], True)]
    for i, (got, want) in enumerate(cases):
        g = got == want
        ok &= g
        print(f"selftest case {i}: {got!r} (want {want!r}): {'pass' if g else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else ""), "pass" if ok else "FAIL")
    return ok


def main():
    cmd = ["nice", "-n", "10", PY, "-u", "anm_lowd.py", RAW, OUT, "--state", STATE, "--N", "8", "--checks", "", "--target", "3.0431", "--threads", "10", "--save_series", SERIES]
    import shlex
    r = subprocess.run([PY, "-I", f"{HERE}/cmddiff997.py", " ".join(shlex.quote(c) for c in cmd)], capture_output=True, text=True)
    open(f"{HERE}/cmddiff_997c.txt", "w").write(r.stdout + r.stderr)
    say(f"command diff against the coordinator's: {r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[:200]} (exit {r.returncode})")
    if r.returncode != 0:
        say("the command differs from the coordinator's: not launched")
        return 1
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    logf = open(f"{HERE}/anm_lowd.log", "w")
    logf.write("# cmd (cwd hp/): " + " ".join(cmd) + "\n")
    logf.flush()
    t0 = time.time()
    proc = subprocess.Popen(cmd, cwd=f"{WT}/hp", env=env, stdout=logf, stderr=subprocess.STDOUT)
    say(f"anm_lowd.py started, pid {proc.pid}")
    seen, saved, stopped, last, pilot_end = 0, None, None, 0.0, False
    rssf = open(f"{HERE}/rss_997c.log", "a")
    while proc.poll() is None:
        time.sleep(20)
        if time.time() - last >= 60:
            last = time.time()
            ps = subprocess.run(["ps", "-o", "rss=,pcpu=", "-p", str(proc.pid)], capture_output=True, text=True).stdout.split()
            ma = re.search(r"MemAvailable:\s+(\d+)", open("/proc/meminfo").read())
            rssf.write(f"{time.strftime('%F %T', time.gmtime())} UTC pid {proc.pid} rss_kB {ps[0] if ps else None} pcpu {ps[1] if len(ps) > 1 else None} memavail_kB {ma.group(1) if ma else None} load {open('/proc/loadavg').read().split()[0]}\n")
            rssf.flush()
        text = open(f"{HERE}/anm_lowd.log").read()
        b = BASE.search(text)
        if b and seen == 0 and not any(True for _ in ORD.finditer(text)):
            pass
        o = orders(text)
        while seen < len(o):
            k, p, c, s = o[seen]
            say(f"ORDER {k}: {p} products, converged {c}, {s} s")
            seen += 1
            if k == 2 and not pilot_end:
                pilot_end = True
                say(f"PILOT END: order 2 done {int(time.time() - t0)} s after the start (orders so far: " + ", ".join(f"{kk}: {ss} s" for kk, _, _, ss in o) + ")")
        why = decision(text, time.time() - t0)
        if why and stopped is None:
            stopped = why
            say(f"PILOT END: STOP: {why}: TERM to exact pid {proc.pid}")
            proc.terminate()
            break
        if saved is None and os.path.exists(SERIES):
            saved = time.time()
            say("the series file is saved (the target stage follows)")
        if saved and time.time() - saved > RULE30:
            stopped = "target stage past 30 min after the series was saved"
            say(f"{stopped}: TERM to exact pid {proc.pid}")
            proc.terminate()
            break
    try:
        proc.wait(timeout=120)
    except subprocess.TimeoutExpired:
        say(f"still alive after 120 s: KILL to exact pid {proc.pid}")
        proc.kill()
        proc.wait()
    o = orders(open(f"{HERE}/anm_lowd.log").read())
    say(f"SERIES END: exit {proc.returncode}, wall {int(time.time() - t0)} s, orders " + ", ".join(f"{k}: {'ok' if c else 'NOT converged'} {s} s" for k, _, c, s in o) + (f"; stopped: {stopped}" if stopped else ""))
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    sys.exit(main())

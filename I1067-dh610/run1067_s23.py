#!/usr/bin/env python3
"""#1067 stages 2 and 3 (dh610): the fine plan on the M 512 state of stage 1, then its series, as run1014b.py's B2 with the M 512 state.

    run1067_s23.py                 stage 2 (make_planb_1014.py), stage 3 (anm_lowd.py --N 12), the stop rules below
    run1067_s23.py --selftest [--mutate]   the parsers and decisions on planted text (exit 1 on failure; --mutate loosens each bar, the checks must fail)

  plan    make_planb_1014.py STATE DST 1e-45 0.05 1 (B2's settings: tol_step 1e-45, hmax 0.05; MINSTEPS 1, the step count is recorded, B2's bar of 4388 was for the M 384 series). Its own --mutate control
          runs first and must fail on its check (exit 1 with a FAIL line); the real run must print 'pass' (the vector identical to the state's, max|F| on the new plan at most 1e-26, the meta keys kept).
  series  anm_lowd.py RAW OUT --state <the _plan.npz> --N 12 --checks "" --target 3.0474 --threads 10 --save_series series_D3.0475_M512_N12.npz (B2's command, --threads 10 for 6). Stopped by exact pid,
          unconverged, when the base's smallest pivot is below 1e-6, or z_1 needs more than 6 products or does not converge, or the target stage runs more than 30 min after the series file is saved
          (the issue: the series is saved before the target stage), or at 30 h of wall time (a ceiling against a hang, not a result rule).
Every 60 s the main process's RSS, peak RSS, MemAvailable and the load go to rss_1067_series.txt."""
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAWL = "/home/nathan/Source/choptuik-large-d-raw"
WT = "/home/nathan/Source/choptuik-large-d-1067"
PY = "/home/nathan/Source/venv-i1058/bin/python"
LOG = f"{HERE}/exits_1067.txt"
PIVOT_MIN, MAX_PRODUCTS, CAP, RULE30 = 1e-6, 6, 30 * 3600, 1800
PLAN_TOL, PLAN_HMAX, PLAN_MIN = 1e-45, 0.05, 1


def say(msg):
    with open(LOG, "a") as f:
        f.write(f"1067 {msg} {time.strftime('%F %T', time.gmtime())} UTC\n")


def base_pivot(text):
    """the smallest pivot of the `base ...` line of anm_lowd.py, or None"""
    m = re.search(r"^base .*pivots ([0-9.eE+-]+)\.\.([0-9.eE+-]+)", text, re.M)
    return float(m.group(1)) if m else None


def z1_info(text):
    """(products, converged) of the `  z_1:` line, or None"""
    m = re.search(r"^  z_1: .*?, (\d+) products, converged (True|False)", text, re.M)
    return (int(m.group(1)), m.group(2) == "True") if m else None


def plan_steps(text):
    """(steps, passed) of make_planb_1014.py's result line, or None"""
    m = re.search(r"^plan tol_step \S+ hmax \S+: (\d+) steps .*: (pass|FAIL)$", text, re.M)
    return (int(m.group(1)), m.group(2) == "pass") if m else None


def plan_ok(got, minsteps=PLAN_MIN):
    return bool(got) and got[1] and got[0] >= minsteps


def stage3_stop(pivot, z1, pivot_min=PIVOT_MIN, max_products=MAX_PRODUCTS):
    """reason to stop the series (None to go on)"""
    if pivot is not None and pivot < pivot_min:
        return f"base smallest pivot {pivot:.1e} below {pivot_min:.0e}"
    if z1 is not None and (not z1[1] or z1[0] > max_products):
        return f"z_1 needs {z1[0]} products, converged {z1[1]}"
    return None


def selftest(mutate):
    ok = True
    pm, mp = (PIVOT_MIN * 1e-6, MAX_PRODUCTS * 10) if mutate else (PIVOT_MIN, MAX_PRODUCTS)
    cases = [(stage3_stop(2.8e-10, None, pm, mp) is not None, True), (stage3_stop(5.0e-5, None, pm, mp) is None, True),
             (stage3_stop(5e-5, (40, False), pm, mp) is not None, True), (stage3_stop(5e-5, (4, True), pm, mp) is None, True), (stage3_stop(5e-5, (7, True), pm, mp) is not None, True)]
    for i, (got, want) in enumerate(cases):
        g = got == want
        ok &= g
        print(f"selftest case {i}: {got!r} (want {want!r}): {'pass' if g else 'FAIL'}")
    txt = "base /x/M512.npz: D 3.0475, M 512, |F| 1.4e-28, pivots 2.8e-10..5.1e+01, 6876 s\n  z_1: |z| 1.484e+09, |rhs| 1.20e+02, 40 products, converged False, 178 + 964 s\n"
    g = base_pivot(txt) == 2.8e-10 and z1_info(txt) == (40, False) and base_pivot("nothing") is None and z1_info("nothing") is None
    ok &= g
    print("selftest parsers (base pivot 2.8e-10; z_1 40 products False; junk None):", "pass" if g else "FAIL")
    pl = "plan tol_step 1e-45 hmax 0.05: 4460 steps (need >= 1), max|F| 1.4e-27, vector identical True, meta keys kept True: pass\n"
    g = plan_steps(pl) == (4460, True) and plan_steps(pl.replace("pass", "FAIL")) == (4460, False) and plan_steps("nothing") is None
    ok &= g
    print("selftest plan line parsed (4460, True), FAIL -> False, junk -> None:", "pass" if g else "FAIL")
    mn = 1 if mutate else 1000
    g = plan_ok((4460, True), 1) and not plan_ok((4460, False), 1) and not plan_ok(None, 1) and not plan_ok((500, True), mn if not mutate else 1000)
    ok &= g
    print("selftest plan bar (4460 ok; a failed check and no result rejected; 500 < 1000 rejected):", "pass" if g else "FAIL")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def kill(proc, why):
    say(f"{why}: TERM to exact pid {proc.pid}")
    proc.terminate()
    try:
        proc.wait(timeout=120)
    except subprocess.TimeoutExpired:
        say(f"still alive after 120 s: KILL to exact pid {proc.pid}")
        proc.kill()


def stage_plan(state):
    """the plan: (path, steps) or None. The planted --mutate control must fail on its check first."""
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    out = f"{HERE}/states/lowD1067_D3.0475_M512_plan.npz"
    cmd = ["nice", "-n", "10", PY, "-u", f"{HERE}/ref/make_planb_1014.py", state, out, f"{PLAN_TOL:g}", str(PLAN_HMAX), str(PLAN_MIN)]
    t0 = time.time()
    r = subprocess.run(cmd + ["--mutate"], cwd=f"{WT}/hp", env=env, capture_output=True, text=True)
    open(f"{HERE}/plan_mutate.log", "w").write(r.stdout + r.stderr)
    gm = plan_steps(r.stdout)
    good = r.returncode == 1 and gm is not None and gm[1] is False      # a FAIL line from the check itself, not a crash
    say(f"plan control (--mutate must fail on its check): exit {r.returncode}, result {gm}: {'ok' if good else 'CONTROL DID NOT FAIL PROPERLY'}")
    if not good:
        return None
    r = subprocess.run(cmd, cwd=f"{WT}/hp", env=env, capture_output=True, text=True)
    open(f"{HERE}/plan_1e-45.log", "w").write(r.stdout + r.stderr)
    got = plan_steps(r.stdout)
    say(f"plan tol_step {PLAN_TOL:g} hmax {PLAN_HMAX:g}: {got}, exit {r.returncode}, {int(time.time() - t0)} s (both runs)")
    if r.returncode == 0 and plan_ok(got):
        return out, got[0]
    return None


def proc_mem(pid):
    try:
        t = open(f"/proc/{pid}/status").read()
        g = lambda k: (int(re.search(rf"^{k}:\s+(\d+) kB", t, re.M).group(1)) if re.search(rf"^{k}:\s+(\d+) kB", t, re.M) else None)  # noqa: E731
        return g("VmRSS"), g("VmHWM")
    except OSError:
        return None, None


def stage_series(state):
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    ser = f"{HERE}/series_D3.0475_M512_N12.npz"
    t0 = time.time()
    say("series (anm_lowd.py --N 12 on the M 512 plan state, then the target stage; 30-minute rule, 30 h cap) start")
    logf = open(f"{HERE}/series512.log", "w")
    cmd = ["nice", "-n", "10", PY, "-u", "anm_lowd.py", RAWL, f"{HERE}/series512", "--state", state, "--N", "12", "--checks", "", "--target", "3.0474", "--threads", "10", "--save_series", ser]
    logf.write("# cmd (cwd hp/): " + " ".join(cmd) + "\n")
    logf.flush()
    proc = subprocess.Popen(cmd, cwd=f"{WT}/hp", env=env, stdout=logf, stderr=subprocess.STDOUT)
    say(f"anm_lowd.py pid {proc.pid}")
    rssf = open(f"{HERE}/rss_1067_series.txt", "a")
    saved, stopped, last = None, None, 0.0
    while proc.poll() is None:
        time.sleep(20)
        if time.time() - last >= 60:
            last = time.time()
            rss, hwm = proc_mem(proc.pid)
            ma = re.search(r"^MemAvailable:\s+(\d+) kB", open("/proc/meminfo").read(), re.M)
            rssf.write(f"{time.strftime('%F %T', time.gmtime())} UTC pid {proc.pid} rss_kB {rss} hwm_kB {hwm} memavail_kB {ma.group(1) if ma else None} load {open('/proc/loadavg').read().split()[0]}\n")
            rssf.flush()
        text = open(f"{HERE}/series512.log").read()
        why = stage3_stop(base_pivot(text), z1_info(text))
        if why and stopped is None:
            stopped = why
            kill(proc, f"series unconverged ({why})")
            break
        if saved is None and os.path.exists(ser):
            saved = time.time()
            say("series saved")
        if saved and time.time() - saved > RULE30:
            kill(proc, "target stage past 30 min after the series was saved")
            break
        if time.time() - t0 > CAP:
            kill(proc, "30 h cap")
            break
    proc.wait()
    say(f"series stage exit {proc.returncode} wall {int(time.time() - t0)} s")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    st = f"{HERE}/states/lowD1067_D3.0475_M512.npz"
    if not os.path.exists(st):
        say("no stage 1 state: stages 2 and 3 not run")
        sys.exit(1)
    p = stage_plan(st)
    if not p:
        say("plan stage did not pass: series not run")
        sys.exit(1)
    say(f"plan: {p[1]} steps at tol_step {PLAN_TOL:g}, state {os.path.basename(p[0])}")
    stage_series(p[0])
    say("run1067_s23.py done")

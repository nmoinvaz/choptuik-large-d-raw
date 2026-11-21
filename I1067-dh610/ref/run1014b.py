#!/usr/bin/env python3
"""#1014 step B (coordinator approved C then B, hc 2026-11-20 about 05:31 UTC): lift T82-win's M 384 state to the planner's converged plan with lowD_dd.py, then its series.

    run1014b.py                 stage 1 (lowD_dd.py --Ms 384 from T82-win's M 384 state, planner's plan), the stop rule after each Newton call, then stage 2 (anm_lowd.py series)
    run1014b.py --selftest [--mutate]   the parsers and decisions on planted log lines (exit 1 on failure; --mutate loosens each bar, the checks must fail)

Rules, fixed before the run (README "Step B"):
  stage 1  after each Newton call (a new `^  newton` line of stage1b.log) the checkpoint is copied and its max|F| measured by resid1014.py (planted +1e-20 control must read 1.0e-20);
           stop (exact pid) when max|F| <= 1e-26 (the floor class of my M 320, 1.4e-27) and use that checkpoint as the state; after call 3 with max|F| > 1e-26 stop and report (no series).
  plan     (coordinator's hc, 2026-11-20 about 06:50 UTC, after step C's base pivot 1.1e-12 on 1820 steps) the lifted state gets a plan of at least 4388 steps, s.plan(zh, zl, tol_step, 0.05)
           with the first tol_step of 1e-40, 1e-41, ... that gives that count (make_planb_1014.py: vector identical, max|F| <= 1e-26, its --mutate must fail). Then the driver logs the step count
           and waits for the file B2_GO in this folder (I post the count and the cost estimate first, as the coordinator asked) before the series starts.
  stage 2  anm_lowd.py as for M 320, same flags, on the state with the fine plan. Stopped by exact pid, unconverged, when the base's smallest pivot is below 1e-6, or z_1 needs more than 6
           products or does not converge, when the target stage runs more than 30 min after the series file is saved, or at 14 h of wall time (the 10 h of the M 384 command is below the
           7.9-9.4 h estimated for the series file at 4460 steps; it is a ceiling against a hang, not a result rule). Wall times only are quoted (t_jac is the old LU-fill copy, #1040)."""
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAWL = "/home/nathan/Source/choptuik-large-d-raw"
WT = "/home/nathan/Source/choptuik-large-d-1014"
PY = "/home/nathan/Source/choptuik-large-d-935/.venv/bin/python"
START = f"{RAWL}/T82-win/states/lowDhm_x0.000157-0.975_D3.0475_M384.npz"
NODES = "0.000157,0.000313,0.000625,0.00125,0.0025,0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.975"
LOG = f"{HERE}/exits_1014.txt"
FLOOR, MAX_CALLS, PIVOT_MIN, MAX_PRODUCTS, CAP, RULE30 = 1e-26, 3, 1e-6, 6, 50400, 1800
PLAN_MIN, PLAN_HMAX, PLAN_TOLS = 4388, 0.05, (1e-40, 1e-41, 1e-42, 1e-43, 1e-44, 1e-45)


def say(msg):
    with open(LOG, "a") as f:
        f.write(f"1014 {msg} {time.strftime('%F %T', time.gmtime())} UTC\n")


def newton_lines(text):
    return [l for l in text.splitlines() if l.startswith("  newton")]


def base_pivot(text):
    """the smallest pivot of the `base ...` line of anm_lowd.py, or None"""
    m = re.search(r"^base .*pivots ([0-9.eE+-]+)\.\.([0-9.eE+-]+)", text, re.M)
    return float(m.group(1)) if m else None


def z1_info(text):
    """(products, converged) of the `  z_1:` line, or None"""
    m = re.search(r"^  z_1: .*?, (\d+) products, converged (True|False)", text, re.M)
    return (int(m.group(1)), m.group(2) == "True") if m else None


def plan_steps(text):
    """the step count of make_planb_1014.py's result line, or None"""
    m = re.search(r"^plan tol_step \S+ hmax \S+: (\d+) steps .*: (pass|FAIL)$", text, re.M)
    return (int(m.group(1)), m.group(2) == "pass") if m else None


def plan_ok(got, minsteps=PLAN_MIN):
    return bool(got) and got[1] and got[0] >= minsteps


def stage1_decision(call, fmax, floor=FLOOR, max_calls=MAX_CALLS):
    if fmax <= floor:
        return "floor"
    return "stop-not-floor" if call >= max_calls else "continue"


def stage2_stop(pivot, z1, pivot_min=PIVOT_MIN, max_products=MAX_PRODUCTS):
    """reason to stop the series (None to go on)"""
    if pivot is not None and pivot < pivot_min:
        return f"base smallest pivot {pivot:.1e} below {pivot_min:.0e}"
    if z1 is not None and (not z1[1] or z1[0] > max_products):
        return f"z_1 needs {z1[0]} products, converged {z1[1]}"
    return None


def selftest(mutate):
    ok = True
    floor, mc, pm, mp = (FLOOR * 1e3, MAX_CALLS + 5, PIVOT_MIN * 1e-6, MAX_PRODUCTS * 10) if mutate else (FLOOR, MAX_CALLS, PIVOT_MIN, MAX_PRODUCTS)
    cases = [
        (stage1_decision(1, 1.42e-27, floor, mc), "floor"), (stage1_decision(1, 5e-24, floor, mc), "continue"), (stage1_decision(3, 5e-24, floor, mc), "stop-not-floor"),
        (stage1_decision(2, 9.9e-27, floor, mc), "floor"), (stage1_decision(2, 1.1e-26, floor, mc), "continue"),
        (stage2_stop(2.8e-10, None, pm, mp) is not None, True), (stage2_stop(5.0e-5, None, pm, mp) is None, True),
        (stage2_stop(5e-5, (40, False), pm, mp) is not None, True), (stage2_stop(5e-5, (4, True), pm, mp) is None, True), (stage2_stop(5e-5, (7, True), pm, mp) is not None, True),
    ]
    for i, (got, want) in enumerate(cases):
        g = got == want
        ok &= g
        print(f"selftest case {i}: {got!r} (want {want!r}): {'pass' if g else 'FAIL'}")
    txt = "base /x/T82.npz: D 3.0475, M 384, |F| 1.4e-28, pivots 2.8e-10..5.1e+01, 6876 s\n  z_1: |z| 1.484e+09, |rhs| 1.20e+02, 40 products, converged False, 178 + 964 s\n"
    ok &= base_pivot(txt) == 2.8e-10 and z1_info(txt) == (40, False)
    print("selftest parsers (base pivot 2.8e-10; z_1 40 products False):", "pass" if base_pivot(txt) == 2.8e-10 and z1_info(txt) == (40, False) else "FAIL")
    nl = "  newton 0: |F| 2.25e-22 |dz| 1e-17 lam 1 dDelta 1e-30 Delta 2.4 piv 5.0e-05..4.5e+01  t 9423.6s\nother\n  newton 0: |F| 1e-27 ...\n"
    ok &= len(newton_lines(nl)) == 2
    pl = "plan tol_step 1e-40 hmax 0.05: 4460 steps (need >= 4388), max|F| 1.4e-27, vector identical True, meta keys kept True: pass\n"
    good = plan_steps(pl) == (4460, True) and plan_steps(pl.replace("pass", "FAIL")) == (4460, False) and plan_steps("nothing") is None
    ok &= good
    print("selftest plan line parsed (4460, True), FAIL -> False, junk -> None:", "pass" if good else "FAIL")
    mn = 1 if mutate else PLAN_MIN
    good = plan_ok((4460, True), mn) and not plan_ok((4000, True), mn) and not plan_ok((5000, False), mn) and not plan_ok(None, mn)
    ok &= good
    print("selftest plan bar (4460 ok; 4000 steps, a failed check and no result rejected):", "pass" if good else "FAIL")
    print("selftest newton lines counted 2:", "pass" if len(newton_lines(nl)) == 2 else "FAIL")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def resid(state, tag):
    """max|F| of a checkpoint by resid1014.py (2 threads, nice 19), with its planted-1e-20 control; (F, control) or raises"""
    out = f"{HERE}/resid_{tag}.log"
    with open(out, "w") as f:
        subprocess.run(["nice", "-n", "19", PY, "-u", f"{HERE}/resid1014.py", "2", state, "--mutate"], cwd="/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/026ace6b-8e85-4de1-9fd2-85ec04d52786/scratchpad", stdout=f, stderr=subprocess.STDOUT, check=True,
                       env=dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"))
    vals = re.findall(r"(as saved|\+1e-20): max\|F\| ([0-9.eE+-]+)", open(out).read())
    d = {k: float(v) for k, v in vals}
    return d["as saved"], d["+1e-20"]


def kill(proc, why):
    say(f"{why}: killing pid {proc.pid} by exact pid")
    proc.terminate()
    try:
        proc.wait(timeout=60)
    except subprocess.TimeoutExpired:
        proc.kill()


def stage1():
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    t0 = time.time()
    say(f"stage B1 (lowD_dd.py --Ms 384 from T82-win's M 384 state on the planner's plan, --it_max 3, 6 threads) start")
    logf = open(f"{HERE}/stage1b.log", "w")
    proc = subprocess.Popen(["nice", "-n", "10", PY, "-u", "lowD_dd.py", f"{HERE}/m384b.jsonl", "--start", START, "--Ms", "384", "--nodes", NODES, "--kt", "36", "--kcs", "100",
                             "--ks", "250", "--jac", "f64", "--tol", "1e-29", "--it_max", str(MAX_CALLS), "--threads", "6", "--tag", "lowD1014b"], cwd=f"{WT}/hp", env=env, stdout=logf,
                            stderr=subprocess.STDOUT)
    ck = f"{WT}/hp/data/lowD_states/lowD1014b_D3.0475_M384_ckpt.npz"
    final = f"{WT}/hp/data/lowD_states/lowD1014b_D3.0475_M384.npz"
    seen = 0
    chosen = None
    while True:
        time.sleep(20)
        text = open(f"{HERE}/stage1b.log").read()
        n = len(newton_lines(text))
        if n > seen and os.path.exists(ck):
            seen = n
            dst = f"{HERE}/states/lowD1014b_D3.0475_M384_ckpt_after_call{n}.npz"
            shutil.copy2(ck, dst)
            say(f"B1 Newton call {n} landed: {newton_lines(text)[-1].strip()[:150]}; checkpoint copied, measuring max|F|")
            F, ctl = resid(dst, f"b_after_call{n}")
            say(f"B1 call {n}: max|F| of the checkpoint {F:.3e} (planted 1e-20 control reads {ctl:.2e}: {'ok' if abs(ctl - 1e-20) < 1e-22 else 'CONTROL FAILED'})")
            if abs(ctl - 1e-20) >= 1e-22:
                kill(proc, "control failed")
                return None
            d = stage1_decision(n, F)
            if d == "floor":
                kill(proc, f"B1 call {n} at the floor (<= {FLOOR:.0e})")
                chosen = dst
                break
            if d == "stop-not-floor":
                kill(proc, f"B1 call {n} still above {FLOOR:.0e}")
                return None
        if proc.poll() is not None:
            say(f"B1 lowD_dd.py exited {proc.returncode} after {int(time.time() - t0)} s")
            if os.path.exists(final):
                chosen = final
            break
    if chosen is None:
        say("B1 no state chosen: stage B2 not run")
        return None
    out = f"{HERE}/states/lowD1014b_D3.0475_M384.npz"
    shutil.copy2(chosen, out)
    say(f"B1 done, wall {int(time.time() - t0)} s: state {os.path.basename(chosen)} copied to states/lowD1014b_D3.0475_M384.npz")
    return out


def stage_plan(state):
    """the lifted state with a plan of at least PLAN_MIN steps; (path, steps, tol) or None. The planted --mutate control must fail on the first tolerance tried."""
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1")
    out = f"{HERE}/states/lowD1014b_D3.0475_M384_plan.npz"
    first = True
    for tol in PLAN_TOLS:
        cmd = ["nice", "-n", "10", PY, "-u", f"{HERE}/make_planb_1014.py", state, out, f"{tol:g}", str(PLAN_HMAX), str(PLAN_MIN)]
        if first:
            r = subprocess.run(cmd + ["--mutate"], cwd=f"{WT}/hp", env=env, capture_output=True, text=True)
            open(f"{HERE}/plan_b_mutate.log", "w").write(r.stdout + r.stderr)
            gm = plan_steps(r.stdout)
            good = r.returncode == 1 and gm is not None and gm[1] is False      # a FAIL line from the check itself, not a crash
            say(f"B2 plan control (--mutate must fail on its check): exit {r.returncode}, result {gm}: {'ok' if good else 'CONTROL DID NOT FAIL PROPERLY'}")
            if not good:
                return None
            first = False
        r = subprocess.run(cmd, cwd=f"{WT}/hp", env=env, capture_output=True, text=True)
        open(f"{HERE}/plan_b_{tol:g}.log", "w").write(r.stdout + r.stderr)
        got = plan_steps(r.stdout)
        say(f"B2 plan tol_step {tol:g}: {got}")
        if r.returncode == 0 and plan_ok(got):
            return out, got[0], tol
    return None


def wait_go():
    """the series starts only after I have posted the step count and cost estimate (file B2_GO)"""
    say("B2 plan ready; waiting for B2_GO (the step count and cost estimate are posted first)")
    while not os.path.exists(f"{HERE}/B2_GO"):
        time.sleep(30)
    say("B2_GO seen")


def stage2(state):
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    ser = f"{HERE}/series_D3.0475_M384p_N12.npz"
    t0 = time.time()
    say("stage B2 (series N 12 from the lifted M 384, then the target stage; 30-minute rule, 10 h cap) start")
    logf = open(f"{HERE}/stage2b.log", "w")
    proc = subprocess.Popen(["nice", "-n", "10", PY, "-u", "anm_lowd.py", RAWL, f"{HERE}/series384p", "--state", state, "--N", "12", "--checks", "", "--target", "3.0474", "--threads", "6",
                             "--save_series", ser], cwd=f"{WT}/hp", env=env, stdout=logf, stderr=subprocess.STDOUT)
    saved = None
    stopped = None
    while proc.poll() is None:
        time.sleep(20)
        text = open(f"{HERE}/stage2b.log").read()
        why = stage2_stop(base_pivot(text), z1_info(text))
        if why and stopped is None:
            stopped = why
            kill(proc, f"B2 unconverged ({why})")
            break
        if saved is None and os.path.exists(ser):
            saved = time.time()
            say("B2 series saved")
        if saved and time.time() - saved > RULE30:
            kill(proc, "B2 target stage past 30 min after the series was saved")
            break
        if time.time() - t0 > CAP:
            kill(proc, "B2 10 h cap")
            break
    proc.wait()
    say(f"stage B2 exit {proc.returncode} wall {int(time.time() - t0)} s")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    s = stage1()
    p = stage_plan(s) if s else None
    if s and not p:
        say("B2 no plan reached the step count: series not run")
    if p:
        say(f"B2 plan: {p[1]} steps at tol_step {p[2]:g}, state {os.path.basename(p[0])}")
        wait_go()
        stage2(p[0])
    say("run1014b.py done")

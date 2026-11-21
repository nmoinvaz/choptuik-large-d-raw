#!/usr/bin/env python3
"""#1067 stage 1 (dh610): the lift of B2's M 384 state at D 3.0475 to M 512 with lowD_dd.py, as run1014b.py's B1 with --Ms 512.

    run1067_s1.py                 stage 1, the stop rules below, the chosen state copied to states/lowD1067_D3.0475_M512.npz (exit 0), else exit 1
    run1067_s1.py --selftest [--mutate]   the parsers and decisions on planted text (exit 1 on failure; --mutate loosens each bar, the checks must fail)

B1's command (run1014b.py, stage1) changed only in --Ms 512, --start (the M 384 state of raw I1014-dh170/states, blob 74daf429), the output paths (--tag lowD1067, the jsonl and log in this folder)
and --threads 10 (the issue's thread budget; B2 used 6). The first Newton call is the pilot. Rules, fixed before the run (issue #1067, run1014b.py):
  pilot  a first call above 8 h (wall since the start, before its `newton 0` line) or an RSS above 45 GB (taken as 45e9 bytes, any time in stage 1) stops the task by exact pid, with a report.
         Reported after the first call: its wall (since the start and its own), the peak RSS, the start max|F| and |dz|.
  floor  after each Newton call the checkpoint is copied and its max|F| measured (resid1014.py; its planted +1e-20 control must read 1.0e-20 within 1e-22); the state is accepted at the evaluation
         floor when Delta's own Newton correction on that call, |dDelta| of its newton line, is below 1e-25 (the lowD_dd.py run is then stopped by exact pid); lowD_dd.py's own convergence
         (--tol 1e-29) ends it too, its final state being taken; after call 3 (--it_max 3) not accepted: stop and report, no later stage.
Every 60 s the main process's RSS, peak RSS, MemAvailable and the load go to rss_1067.txt."""
import hashlib
import os
import re
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RAWL = "/home/nathan/Source/choptuik-large-d-raw"
WT = "/home/nathan/Source/choptuik-large-d-1067"
PY = "/home/nathan/Source/venv-i1058/bin/python"
START = f"{HERE}/ref/lowD1014b_D3.0475_M384.npz"
START_BLOB = "74daf429300c75c3deea191702e638ef24fd8993"
NODES = "0.000157,0.000313,0.000625,0.00125,0.0025,0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8,0.9,0.95,0.975"
LOG = f"{HERE}/exits_1067.txt"
WALL_FIRST, RSS_MAX, DDELTA_FLOOR, MAX_CALLS = 8 * 3600, 45e9, 1e-25, 3


def say(msg):
    with open(LOG, "a") as f:
        f.write(f"1067 {msg} {time.strftime('%F %T', time.gmtime())} UTC\n")


def newton_lines(text):
    return [l for l in text.splitlines() if l.startswith("  newton")]


def newton_info(line):
    """(call, |F|, |dz|, lam, dDelta, seconds or None) of a `  newton N: |F| a |dz| b lam c dDelta d ...  t Xs` line, or None"""
    m = re.match(r"\s*newton (\d+): \|F\| (\S+) \|dz\| (\S+) lam (\S+) dDelta (\S+)", line)
    if not m:
        return None
    t = re.search(r"\bt ([0-9.]+) ?s", line)
    return int(m.group(1)), float(m.group(2)), float(m.group(3)), float(m.group(4)), float(m.group(5)), float(t.group(1)) if t else None


def start_F(text):
    m = re.search(r"start \|F\| ([0-9.eE+-]+)", text)
    return float(m.group(1)) if m else None


def status_kb(text, key):
    m = re.search(rf"^{key}:\s+(\d+) kB", text, re.M)
    return int(m.group(1)) if m else None


def first_call_stop(wall, rss_bytes, first_done, wall_max=WALL_FIRST, rss_max=RSS_MAX):
    """reason to stop the task (None to go on): the first call above wall_max, or the RSS above rss_max at any time"""
    if rss_bytes is not None and rss_bytes > rss_max:
        return f"RSS {rss_bytes / 1e9:.1f} GB above {rss_max / 1e9:.0f} GB"
    if not first_done and wall > wall_max:
        return f"first Newton call above {wall_max / 3600:.0f} h"
    return None


def call_decision(call, dDelta, floor=DDELTA_FLOOR, max_calls=MAX_CALLS):
    """call is 1-based (calls landed); floor: Delta's own correction below `floor`; after max_calls not accepted: stop"""
    if abs(dDelta) < floor:
        return "floor"
    return "stop-not-floor" if call >= max_calls else "continue"


def selftest(mutate):
    ok = True
    wm, rm, fl, mc = (WALL_FIRST * 2, RSS_MAX * 2, DDELTA_FLOOR * 1e3, MAX_CALLS + 5) if mutate else (WALL_FIRST, RSS_MAX, DDELTA_FLOOR, MAX_CALLS)
    cases = [
        (first_call_stop(8.1 * 3600, 20e9, False, wm, rm) is not None, True), (first_call_stop(7.9 * 3600, 20e9, False, wm, rm) is None, True),
        (first_call_stop(9 * 3600, 20e9, True, wm, rm) is None, True),                      # the wall rule is for the first call only
        (first_call_stop(100, 46e9, True, wm, rm) is not None, True), (first_call_stop(100, 44e9, True, wm, rm) is None, True),
        (call_decision(1, 5e-27, fl, mc), "floor"), (call_decision(1, -5e-27, fl, mc), "floor"), (call_decision(1, 3e-24, fl, mc), "continue"),
        (call_decision(3, 3e-24, fl, mc), "stop-not-floor"), (call_decision(2, 9.9e-26, fl, mc), "floor"), (call_decision(2, 1.1e-25, fl, mc), "continue"),
    ]
    for i, (got, want) in enumerate(cases):
        g = got == want
        ok &= g
        print(f"selftest case {i}: {got!r} (want {want!r}): {'pass' if g else 'FAIL'}")
    line = "  newton 0: |F| 2.25e-22 |dz| 1.0e-17 lam 1 dDelta -1.2e-30 Delta 2.4 piv 5.0e-05..4.5e+01  t 9423.6s"
    info = newton_info(line)
    g = info == (0, 2.25e-22, 1e-17, 1.0, -1.2e-30, 9423.6) and newton_info("other line") is None and len(newton_lines(line + "\nother\n" + line)) == 2
    ok &= g
    print("selftest newton line parsed:", "pass" if g else "FAIL")
    g = start_F("D 3.0475 M 512: L 123, steps 4502, start |F| 7.99e-05") == 7.99e-05 and start_F("nothing") is None
    ok &= g
    print("selftest start |F| parsed:", "pass" if g else "FAIL")
    st = "Name:\tpython3\nVmPeak:\t 2000 kB\nVmHWM:\t 1500 kB\nVmRSS:\t 1200 kB\n"
    g = status_kb(st, "VmRSS") == 1200 and status_kb(st, "VmHWM") == 1500 and status_kb(st, "VmSwap") is None
    ok &= g
    print("selftest /proc status parsed:", "pass" if g else "FAIL")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def resid(state, tag):
    """max|F| of a checkpoint by resid1014.py (2 threads, nice 19) with its planted +1e-20 control; (F, control) or raises"""
    out = f"{HERE}/resid_{tag}.log"
    with open(out, "w") as f:
        subprocess.run(["nice", "-n", "19", PY, "-u", f"{HERE}/ref/resid1014.py", "2", state, "--mutate"], cwd=HERE, stdout=f, stderr=subprocess.STDOUT, check=True,
                       env=dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1"))
    d = {k: float(v) for k, v in re.findall(r"(as saved|\+1e-20): max\|F\| ([0-9.eE+-]+)", open(out).read())}
    return d["as saved"], d["+1e-20"]


def kill(proc, why):
    say(f"{why}: TERM to exact pid {proc.pid}")
    proc.terminate()
    try:
        proc.wait(timeout=120)
    except subprocess.TimeoutExpired:
        say(f"still alive after 120 s: KILL to exact pid {proc.pid}")
        proc.kill()


def proc_mem(pid):
    try:
        t = open(f"/proc/{pid}/status").read()
        return status_kb(t, "VmRSS"), status_kb(t, "VmHWM")
    except OSError:
        return None, None


def memavail_kb():
    m = re.search(r"^MemAvailable:\s+(\d+) kB", open("/proc/meminfo").read(), re.M)
    return int(m.group(1)) if m else None


def stage1():
    if hashlib.sha1(b"blob %d\0" % os.path.getsize(START) + open(START, "rb").read()).hexdigest() != START_BLOB:
        say("the start state's blob differs from " + START_BLOB + ": stop")
        return None
    head = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    if not head.startswith("276aa1cd"):
        say(f"worktree {WT} is at {head}, not 276aa1cd: stop")
        return None
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    t0 = time.time()
    say(f"worktree {WT} at {head}, venv-i1058, start {START} (blob {START_BLOB}), load {open('/proc/loadavg').read().split()[0]}")
    say("stage 1 (lowD_dd.py --Ms 512 from the M 384 state, --it_max 3, 10 threads) start")
    logf = open(f"{HERE}/stage1.log", "w")
    cmd = ["nice", "-n", "10", PY, "-u", "lowD_dd.py", f"{HERE}/m512b.jsonl", "--start", START, "--Ms", "512", "--nodes", NODES, "--kt", "36", "--kcs", "100", "--ks", "250", "--jac", "f64",
           "--tol", "1e-29", "--it_max", str(MAX_CALLS), "--threads", "10", "--tag", "lowD1067"]
    logf.write("# cmd (cwd hp/): " + " ".join(cmd) + "\n")
    logf.flush()
    proc = subprocess.Popen(cmd, cwd=f"{WT}/hp", env=env, stdout=logf, stderr=subprocess.STDOUT)
    say(f"lowD_dd.py pid {proc.pid}")
    ck = f"{WT}/hp/data/lowD_states/lowD1067_D3.0475_M512_ckpt.npz"
    final = f"{WT}/hp/data/lowD_states/lowD1067_D3.0475_M512.npz"
    seen, chosen, peak, last_rss_log, first_done = 0, None, 0, 0.0, False
    rssf = open(f"{HERE}/rss_1067.txt", "a")
    while True:
        time.sleep(20)
        rss, hwm = proc_mem(proc.pid)
        if hwm:
            peak = max(peak, hwm)
        if time.time() - last_rss_log >= 60:
            last_rss_log = time.time()
            rssf.write(f"{time.strftime('%F %T', time.gmtime())} UTC pid {proc.pid} rss_kB {rss} hwm_kB {hwm} memavail_kB {memavail_kb()} load {open('/proc/loadavg').read().split()[0]}\n")
            rssf.flush()
        why = first_call_stop(time.time() - t0, (rss or 0) * 1024, first_done)
        if why:
            kill(proc, f"pilot stop rule: {why} (peak RSS {peak / 1048576:.1f} GiB, wall {int(time.time() - t0)} s)")
            say("task stopped by the pilot stop rule: report, no later stage")
            return None
        text = open(f"{HERE}/stage1.log").read()
        nl = newton_lines(text)
        n = sum(1 for l in nl if newton_info(l) is not None)
        if n > seen and os.path.exists(ck):
            seen = n
            info = newton_info([l for l in nl if newton_info(l) is not None][-1])
            if not first_done:
                first_done = True
                say(f"PILOT: first Newton call landed after {int(time.time() - t0)} s wall since the start (its own t {info[5]} s): start |F| {start_F(text)}, line |F| {info[1]:.2e} |dz| {info[2]:.2e} "
                    f"lam {info[3]:g} dDelta {info[4]:+.2e}; peak RSS {peak / 1048576:.2f} GiB ({peak / 1e6:.1f} GB), RSS now {(rss or 0) / 1048576:.2f} GiB")
            dst = f"{HERE}/states/lowD1067_D3.0475_M512_ckpt_after_call{n}.npz"
            shutil.copy2(ck, dst)
            say(f"Newton call {n} landed: {nl[-1].strip()[:170]}; checkpoint copied, measuring max|F|")
            F, ctl = resid(dst, f"after_call{n}")
            good = abs(ctl - 1e-20) < 1e-22
            say(f"call {n}: max|F| of the checkpoint {F:.3e} (planted 1e-20 control reads {ctl:.2e}: {'ok' if good else 'CONTROL FAILED'})")
            if not good:
                kill(proc, "control failed")
                return None
            d = call_decision(n, info[4])
            if d == "floor":
                kill(proc, f"call {n}: Delta's Newton correction {info[4]:+.2e} below {DDELTA_FLOOR:.0e}, accepted at the floor")
                chosen = dst
                break
            if d == "stop-not-floor":
                kill(proc, f"call {n}: Delta's correction {info[4]:+.2e} still at or above {DDELTA_FLOOR:.0e}")
                say("stage 1 not at the floor after the last call: report, no later stage")
                return None
        if proc.poll() is not None:
            say(f"lowD_dd.py exited {proc.returncode} after {int(time.time() - t0)} s (peak RSS {peak / 1048576:.2f} GiB)")
            if os.path.exists(final) and "converged" in open(f"{HERE}/stage1.log").read().lower() and proc.returncode == 0:
                chosen = final
            break
    if chosen is None:
        say("stage 1: no state chosen")
        return None
    out = f"{HERE}/states/lowD1067_D3.0475_M512.npz"
    shutil.copy2(chosen, out)
    h = hashlib.sha1(b"blob %d\0" % os.path.getsize(out) + open(out, "rb").read()).hexdigest()
    say(f"stage 1 done, wall {int(time.time() - t0)} s, peak RSS {peak / 1048576:.2f} GiB: state {os.path.basename(chosen)} copied to states/lowD1067_D3.0475_M512.npz (blob {h[:8]})")
    return out


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    s = stage1()
    sys.exit(0 if s else 1)

#!/usr/bin/env python3
"""#1070 (coordinator's hc, after the 22:31 UTC #1070 post): the M 96 state and gamma at D 3.15, M 96, on dh170.
Stage 1: lowD_dd.py OUT --start <M 128 state> --Ms 96 with that state's own nodes, kt 36, kcs 100 (its kc), ks 250, --jac f64 --tol 1e-29 --threads 4 --tag lowD1070, nice 10, cap 4 h.
After every Newton call its checkpoint is copied and its max|F| measured (resid1070.py, with its planted +1e-20 control, as #1014 did); decide() below: converged (max|F| <= 1e-27), at the floor (<= 1e-26 and the
last call gained less than a factor 2), or continue, stalled, control failed. Stage 2 (only after converged or floor): hp/lowD_gamma.py OUT <the M 96 state> --threads=4 --polish=2 --xtol=1e-11 --lam0=4.3977, cap 3 h.
    run_m96.py [--selftest [--mutate]]"""
import os
import re
import shutil
import signal
import subprocess
import sys
import time

P = "/home/nathan/Source/choptuik-large-d-raw-1064w/I1070-dh170"
WT = "/home/nathan/Source/choptuik-large-d-1058b"
PY = f"{WT}/.venv/bin/python"
M128 = "/home/nathan/scratch1070/I927-mac/inputs/lowDhm_x0.000625-0.9_D3.1500_M128.npz"
NODES = "0.000625,0.00125,0.0025,0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8,0.9"
CKPT = f"{WT}/hp/data/lowD_states/lowD1070_D3.1500_M96_ckpt.npz"
FINAL = f"{WT}/hp/data/lowD_states/lowD1070_D3.1500_M96.npz"
M96 = f"{P}/states/lowD1070_D3.1500_M96.npz"
CONV, FLOOR, GAIN, VIS = 1e-27, 1e-26, 2.0, 1e-22


def decide(Fs, ctl, conv=CONV, floor=FLOOR, gain=GAIN, vis=VIS):
    """Fs: the measured max|F| of the checkpoints after Newton calls 1..n; ctl: the planted +1e-20 control reading. Returns 'stop-control', 'converged', 'floor', 'stalled' or 'continue'.
    The planted 1e-20 changes max|F| only where max|F| is below about 1e-22 (vis): there the reading must be 1e-20 within 1e-22. Above it the max masks the plant, and the reading
    must be at least the as-saved max|F| (a plant cannot lower it)."""
    F = Fs[-1]
    if F <= vis:
        if not abs(ctl - 1e-20) < 1e-22:
            return "stop-control"
    elif not ctl >= F * (1 - 1e-3):
        return "stop-control"
    if F <= conv:
        return "converged"
    if F <= floor and len(Fs) >= 2 and F > Fs[-2] / gain:
        return "floor"
    if len(Fs) >= 3 and F > floor and F > Fs[-2] / gain:
        return "stalled"
    return "continue"


def selftest(mutate):
    g, v = (1.2, 1e30) if mutate else (GAIN, VIS)
    cases = [(([1e-12, 3e-20, 2e-28], 1e-20), "converged"), (([1e-12, 4e-27], 1e-20), "continue"), (([1e-12, 4e-27, 3e-27], 1e-20), "floor"), (([1e-12, 4e-27, 1.5e-27], 1e-20), "continue"),
             (([1e-12, 1e-20, 6e-21, 5e-21], 1e-20), "stalled"), (([1e-12, 2e-28], 3e-21), "stop-control"), (([1e-12, 1e-22], 1e-20), "continue"),
             (([8.518e-07], 8.518e-07), "continue"), (([8.518e-07], 1e-08), "stop-control"), (([1e-12, 4e-12, 9e-13], 1.2e-12), "continue"), (([1e-9, 5e-23], 5e-23), "stop-control")]
    ok = True
    for (Fs, ctl), want in cases:
        got = decide(Fs, ctl, gain=g, vis=v)
        print(f"selftest: {'pass' if got == want else 'FAIL'}: Fs {Fs} ctl {ctl}: want {want}, got {got}")
        ok &= got == want
    return ok


def say(msg):
    with open(f"{P}/exits_m96.txt", "a") as f:
        f.write(f"== {time.strftime('%F %T', time.gmtime())} UTC {msg}\n")


def measure(ck):
    r = subprocess.run([PY, "-W", "ignore", f"{P}/resid1070.py", "4", ck], cwd=P, capture_output=True, text=True,
                       env=dict(os.environ, HP_DIR=f"{WT}/hp", OPENBLAS_NUM_THREADS="1", PYTHONPATH=f"{WT}/hp"))
    F = ctl = None
    for ln in r.stdout.splitlines():
        m = re.search(r"max\|F\| ([0-9.e+-]+)", ln)
        if m:
            if " +1e-20:" in ln:
                ctl = float(m.group(1))
            else:
                F = float(m.group(1))
    return F, ctl, r.stdout + r.stderr


def session_pids(proc):
    """the pids of every process in the session this script started for proc (timeout puts its child in a group of its own, so a process group is not enough)"""
    proc.poll()  # reaps the leader, which would otherwise stay listed as a zombie
    return [int(x) for x in subprocess.run(["ps", "-o", "pid=", "--sid", str(proc.pid)], capture_output=True, text=True).stdout.split()]


def kill(proc, why):
    pids = session_pids(proc)
    say(f"{why}: TERM to pids {pids}, the session this script started (by exact pid)")
    for pid in pids:
        try:
            os.kill(pid, signal.SIGTERM)
        except ProcessLookupError:
            pass
    t = time.time()
    while session_pids(proc) and time.time() - t < 60:
        time.sleep(1)
    for pid in session_pids(proc):
        say(f"pid {pid} still alive after 60 s: KILL")
        os.kill(pid, signal.SIGKILL)


def sample(proc, tag, peak):
    """one line of the memory log: RSS summed over the session of proc, its peak, and the machine's MemAvailable"""
    r = subprocess.run(["ps", "-o", "rss=,pcpu=", "--sid", str(proc.pid)], capture_output=True, text=True).stdout.split()
    rss = sum(int(x) for x in r[0::2]) // 1024
    cpu = sum(float(x) for x in r[1::2])
    av = int([l for l in open("/proc/meminfo") if l.startswith("MemAvailable")][0].split()[1]) // 1024
    peak[0] = max(peak[0], rss)
    with open(f"{P}/memlog_m96.log", "a") as f:
        f.write(f"{time.strftime('%T', time.gmtime())} {tag} RSS {rss} MiB (peak {peak[0]}) cpu {cpu:.0f}% MemAvailable {av} MiB\n")
    if av < 2048:
        with open(f"{P}/alert_m96.log", "a") as f:
            f.write(f"ALERT {time.strftime('%T', time.gmtime())} MemAvailable {av} MiB (alert only)\n")


def stage1():
    os.makedirs(f"{P}/states", exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    cmd = ["nice", "-n", "10", "/usr/bin/time", "-v", "timeout", "-s", "TERM", "14400", PY, "-u", "lowD_dd.py", f"{P}/m96.jsonl", "--start", M128, "--Ms", "96", "--nodes", NODES, "--kt", "36", "--kcs", "100",
           "--ks", "250", "--jac", "f64", "--tol", "1e-29", "--threads", "4", "--tag", "lowD1070"]
    say("stage 1 start: " + " ".join(cmd[6:]))
    t0 = time.time()
    logf = open(f"{P}/stage1_m96.log", "w")
    proc = subprocess.Popen(cmd, cwd=f"{WT}/hp", env=env, stdout=logf, stderr=subprocess.STDOUT, start_new_session=True)
    seen, Fs, chosen, verdict, peak, tick = 0, [], None, None, [0], 0
    while True:
        time.sleep(20)
        tick += 1
        if tick % 3 == 0:
            sample(proc, "stage 1", peak)
        text = open(f"{P}/stage1_m96.log").read()
        n = len(re.findall(r"^  newton \d+: .* lam ", text, re.M))
        if n > seen and os.path.exists(CKPT):
            seen = n
            dst = f"{P}/states/lowD1070_D3.1500_M96_ckpt_after_call{n}.npz"
            shutil.copy2(CKPT, dst)
            line = [l for l in text.splitlines() if re.match(r"^  newton \d+: .* lam ", l)][-1].strip()
            F, ctl, out = measure(dst)
            say(f"stage 1 Newton call {n} landed: {line[:170]}; checkpoint copied, max|F| {F}, planted +1e-20 reads {ctl}")
            if F is None or ctl is None:
                kill(proc, "measurement failed")
                return None, "measure-failed", Fs
            Fs.append(F)
            verdict = decide(Fs, ctl)
            say(f"stage 1 call {n}: decide -> {verdict}")
            if verdict in ("converged", "floor"):
                chosen = dst
                kill(proc, f"call {n} {verdict} (max|F| {F:.3e})")
                break
            if verdict in ("stalled", "stop-control"):
                kill(proc, f"call {n} {verdict}")
                return None, verdict, Fs
        if proc.poll() is not None:
            say(f"stage 1 lowD_dd.py exited {proc.returncode} after {int(time.time() - t0)} s")
            src = FINAL if os.path.exists(FINAL) else None
            if src:
                F, ctl, out = measure(src)
                say(f"stage 1 final state {os.path.basename(src)}: max|F| {F}, planted +1e-20 reads {ctl}")
                if F is not None and ctl is not None:
                    Fs.append(F)
                    verdict = decide(Fs, ctl)
                    say(f"stage 1 final: decide -> {verdict}")
                    if verdict in ("converged", "floor"):
                        chosen = src
            break
    if chosen:
        shutil.copy2(chosen, M96)
        say(f"stage 1 done, wall {int(time.time() - t0)} s: {os.path.basename(chosen)} copied to states/lowD1070_D3.1500_M96.npz")
    return chosen, verdict, Fs


def stage2():
    out = f"{P}/lowD_gamma_D3.15_M96.jsonl"
    cmd = ["nice", "-n", "10", "/usr/bin/time", "-v", "timeout", "-s", "TERM", "10800", PY, "-u", "hp/lowD_gamma.py", out, M96, "--threads=4", "--polish=2", "--xtol=1e-11", "--lam0=4.3977"]
    say("stage 2 start: " + " ".join(cmd[6:]))
    t0 = time.time()
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    peak, tick = [0], 0
    with open(f"{P}/stage2_gamma_M96.log", "w") as lf:
        proc = subprocess.Popen(cmd, cwd=WT, env=env, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
        while proc.poll() is None:
            time.sleep(20)
            tick += 1
            if tick % 3 == 0:
                sample(proc, "stage 2", peak)
        rc = proc.returncode
    say(f"stage 2 exit {rc}, {int(time.time() - t0)} s wall")
    if os.path.exists(out):
        r = subprocess.run([PY, "-I", f"{P}/accept_1070.py", out], capture_output=True, text=True)
        say("stage 2 acceptance: " + r.stdout.strip())
    else:
        say("stage 2 acceptance: no record written")
    return rc


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    if os.path.exists(f"{P}/stage1_m96.log"):
        say("refuse: stage1_m96.log exists (no overwrite)")
        sys.exit(3)
    chosen, verdict, Fs = stage1()
    if not chosen:
        say(f"STOP: stage 1 did not reach a converged M 96 state (verdict {verdict}, max|F| after the calls {Fs}); stage 2 not started")
        say("done")
        sys.exit(1)
    stage2()
    say("done")

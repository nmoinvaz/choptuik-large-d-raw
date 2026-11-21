#!/usr/bin/env python3
"""#1070 D 3.35 option (c) (coordinator's hc after the 23:39 UTC report): the resolution change gamma(96) - gamma(80) at D 3.35.
    run_d335c.py           the lift: lowD_dd.py --start <D 3.35 M 96 state> --Ms 80 (its own 13 nodes, kt 36, kcs 100, ks 250) --jac f64 --tol 1e-29 --threads 4 --tag lowD1070c, cap 2 h,
                           judged after every Newton call as run_m96.py's stage 1 (decide(), resid1070.py with its planted control); then gamma at M 80:
                           lowD_gamma.py OUT <M 80 state> --threads=4 --polish=2 --xtol=1e-11 --lam0=3.409446474818443, cap 2 h, then accept_1070.py
decide(), measure(), kill(), session_pids() are run_m96.py's; the sampler, the gamma stage and the lift watcher are run_d335.py's, with the names and caps of this task."""
import importlib.util
import os
import re
import shutil
import subprocess
import sys
import time

P = "/home/nathan/Source/choptuik-large-d-raw-1064w/I1070-dh170"
spec = importlib.util.spec_from_file_location("m96", f"{P}/run_m96.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
WT, PY = m.WT, m.PY
IN96 = "/home/nathan/scratch1070/T39-win/hp/data/lowD_states/lowDvh96_D3.3500_M96.npz"
IN96_BLOB = "255be3715930bf22d449bf243ca3a541c143e67d"
NODES = "0.005,0.01,0.02,0.05,0.1,0.16,0.23,0.3,0.4,0.5,0.6,0.7,0.8"
LAM0 = "3.409446474818443"
CKPT = f"{WT}/hp/data/lowD_states/lowD1070c_D3.3500_M80_ckpt.npz"
FINAL = f"{WT}/hp/data/lowD_states/lowD1070c_D3.3500_M80.npz"
M80 = f"{P}/states/lowD1070c_D3.3500_M80.npz"
REC = f"{P}/lowD_gamma_D3.35_M80.jsonl"
EXITS = f"{P}/exits_d335c.txt" if not os.environ.get("DRY") else "/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/026ace6b-8e85-4de1-9fd2-85ec04d52786/scratchpad/dry_exits_d335c.txt"
CAP = 7200


def say(msg):
    with open(EXITS, "a") as f:
        f.write(f"== {time.strftime('%F %T', time.gmtime())} UTC {msg}\n")


m.say = say


def sample(proc, tag, peak):
    """one line of the memory log: RSS summed over the session of proc, its peak, and the machine's MemAvailable"""
    r = subprocess.run(["ps", "-o", "rss=,pcpu=", "--sid", str(proc.pid)], capture_output=True, text=True).stdout.split()
    rss = sum(int(x) for x in r[0::2]) // 1024
    cpu = sum(float(x) for x in r[1::2])
    av = int([ln for ln in open("/proc/meminfo") if ln.startswith("MemAvailable")][0].split()[1]) // 1024
    peak[0] = max(peak[0], rss)
    with open(f"{P}/memlog_d335c.log", "a") as f:
        f.write(f"{time.strftime('%T', time.gmtime())} {tag} RSS {rss} MiB (peak {peak[0]}) cpu {cpu:.0f}% MemAvailable {av} MiB\n")
    if av < 2048:
        with open(f"{P}/alert_d335c.log", "a") as f:
            f.write(f"ALERT {time.strftime('%T', time.gmtime())} MemAvailable {av} MiB (alert only)\n")


def gamma_stage(label, state, out, lam0, log, tag):
    cmd = ["nice", "-n", "10", "/usr/bin/time", "-v", "timeout", "-s", "TERM", str(CAP), PY, "-u", "hp/lowD_gamma.py", out, state, "--threads=4", "--polish=2", "--xtol=1e-11", f"--lam0={lam0}"]
    say(f"{label} start: " + " ".join(cmd[6:]))
    if os.environ.get("DRY"):
        return 0
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    t0, peak, tick = time.time(), [0], 0
    with open(log, "w") as lf:
        proc = subprocess.Popen(cmd, cwd=WT, env=env, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
        while proc.poll() is None:
            time.sleep(20)
            tick += 1
            if tick % 3 == 0:
                sample(proc, tag, peak)
        rc = proc.returncode
    say(f"{label} exit {rc}, {int(time.time() - t0)} s wall")
    if os.path.exists(out):
        r = subprocess.run([PY, "-I", f"{P}/accept_1070.py", out], capture_output=True, text=True)
        say(f"{label} acceptance: " + r.stdout.strip())
    else:
        say(f"{label} acceptance: no record written")
    return rc


def lift():
    os.makedirs(f"{P}/states", exist_ok=True)
    env = dict(os.environ, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    cmd = ["nice", "-n", "10", "/usr/bin/time", "-v", "timeout", "-s", "TERM", str(CAP), PY, "-u", "lowD_dd.py", f"{P}/lift80_d335c.jsonl", "--start", IN96, "--Ms", "80", "--nodes", NODES, "--kt", "36",
           "--kcs", "100", "--ks", "250", "--jac", "f64", "--tol", "1e-29", "--threads", "4", "--tag", "lowD1070c"]
    say("lift start: " + " ".join(cmd[6:]))
    if os.environ.get("DRY"):
        return None, "dry", []
    t0 = time.time()
    logf = open(f"{P}/lift80_d335c.log", "w")
    proc = subprocess.Popen(cmd, cwd=f"{WT}/hp", env=env, stdout=logf, stderr=subprocess.STDOUT, start_new_session=True)
    seen, Fs, chosen, verdict, peak, tick = 0, [], None, None, [0], 0
    pat = r"^  newton \d+: .* lam "
    while True:
        time.sleep(20)
        tick += 1
        if tick % 3 == 0:
            sample(proc, "lift", peak)
        text = open(f"{P}/lift80_d335c.log").read()
        n = len(re.findall(pat, text, re.M))
        if n > seen and os.path.exists(CKPT):
            seen = n
            dst = f"{P}/states/lowD1070c_D3.3500_M80_ckpt_after_call{n}.npz"
            shutil.copy2(CKPT, dst)
            line = [ln for ln in text.splitlines() if re.match(pat, ln)][-1].strip()
            F, ctl, out = m.measure(dst)
            say(f"lift Newton call {n} landed: {line[:170]}; checkpoint copied, max|F| {F}, planted +1e-20 reads {ctl}")
            if F is None or ctl is None:
                m.kill(proc, "measurement failed")
                return None, "measure-failed", Fs
            Fs.append(F)
            verdict = m.decide(Fs, ctl)
            say(f"lift call {n}: decide -> {verdict}")
            if verdict in ("converged", "floor"):
                chosen = dst
                m.kill(proc, f"call {n} {verdict} (max|F| {F:.3e})")
                break
            if verdict in ("stalled", "stop-control"):
                m.kill(proc, f"call {n} {verdict}")
                return None, verdict, Fs
        if proc.poll() is not None:
            say(f"lift lowD_dd.py exited {proc.returncode} after {int(time.time() - t0)} s")
            if os.path.exists(FINAL):
                F, ctl, out = m.measure(FINAL)
                say(f"lift final state {os.path.basename(FINAL)}: max|F| {F}, planted +1e-20 reads {ctl}")
                if F is not None and ctl is not None:
                    Fs.append(F)
                    verdict = m.decide(Fs, ctl)
                    say(f"lift final: decide -> {verdict}")
                    if verdict in ("converged", "floor"):
                        chosen = FINAL
            break
    if chosen:
        shutil.copy2(chosen, M80)
        say(f"lift done, wall {int(time.time() - t0)} s: {os.path.basename(chosen)} copied to states/lowD1070c_D3.3500_M80.npz")
    return chosen, verdict, Fs


if __name__ == "__main__":
    if subprocess.run(["git", "hash-object", "--no-filters", IN96], capture_output=True, text=True).stdout.strip() != IN96_BLOB:
        say("refuse: the input blob is not " + IN96_BLOB)
        sys.exit(2)
    if os.path.exists(f"{P}/lift80_d335c.log") or os.path.exists(REC):
        say("refuse: a log or record exists (no overwrite)")
        sys.exit(3)
    chosen, verdict, Fs = lift()
    if not chosen:
        say(f"STOP: the lift did not reach a converged M 80 state (verdict {verdict}, max|F| after the calls {Fs}); gamma at M 80 not started")
        say("done")
        sys.exit(1)
    gamma_stage("gamma at M 80", M80, REC, LAM0, f"{P}/stageC2_gamma80_d335c.log", "C2")
    say("done")

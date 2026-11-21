#!/usr/bin/env python3
"""#1070 D 3.35 (coordinator's hc after the 23:15 UTC M 96 report): gamma at M 96 on T39-win's lowDvh96_D3.3500_M96.npz and at M 128 on its lift.
    run_d335.py A          gamma at M 96: lowD_gamma.py OUT <M 96 state> --threads=4 --polish=2 --xtol=1e-11 --lam0=3.4094, cap 3 h, then accept_1070.py
    run_d335.py B          the lift: lowD_dd.py --start <M 96 state> --Ms 128 (its own nodes, kt 36, kcs 100, ks 250) --jac f64 --tol 1e-29 --threads 4 --tag lowD1070b, cap 3 h,
                           judged after every Newton call as run_m96.py's stage 1 (decide(), resid1070.py with its planted control); then, once A is done with exactly one
                           sign change, gamma at M 128 with --lam0 = A's lam, cap 3 h, then accept_1070.py
    run_d335.py --selftest [--mutate]
A and B are independent until B's last stage, so they run side by side (4 threads each). decide(), measure(), kill(), session_pids() are run_m96.py's."""
import importlib.util
import json
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
LAM0 = "3.4094"
CKPT = f"{WT}/hp/data/lowD_states/lowD1070b_D3.3500_M128_ckpt.npz"
FINAL = f"{WT}/hp/data/lowD_states/lowD1070b_D3.3500_M128.npz"
M128 = f"{P}/states/lowD1070b_D3.3500_M128.npz"
REC_A = f"{P}/lowD_gamma_D3.35_M96.jsonl"
REC_B = f"{P}/lowD_gamma_D3.35_M128.jsonl"
EXITS = f"{P}/exits_d335.txt" if not os.environ.get("DRY") else "/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/026ace6b-8e85-4de1-9fd2-85ec04d52786/scratchpad/dry_exits_d335.txt"
WHO = ""


def say(msg):
    with open(EXITS, "a") as f:
        f.write(f"== {time.strftime('%F %T', time.gmtime())} UTC {WHO}{msg}\n")


m.say = say


def sample(proc, tag, peak):
    """one line of the memory log: RSS summed over the session of proc, its peak, and the machine's MemAvailable"""
    r = subprocess.run(["ps", "-o", "rss=,pcpu=", "--sid", str(proc.pid)], capture_output=True, text=True).stdout.split()
    rss = sum(int(x) for x in r[0::2]) // 1024
    cpu = sum(float(x) for x in r[1::2])
    av = int([ln for ln in open("/proc/meminfo") if ln.startswith("MemAvailable")][0].split()[1]) // 1024
    peak[0] = max(peak[0], rss)
    with open(f"{P}/memlog_d335.log", "a") as f:
        f.write(f"{time.strftime('%T', time.gmtime())} {WHO}{tag} RSS {rss} MiB (peak {peak[0]}) cpu {cpu:.0f}% MemAvailable {av} MiB\n")
    if av < 2048:
        with open(f"{P}/alert_d335.log", "a") as f:
            f.write(f"ALERT {time.strftime('%T', time.gmtime())} MemAvailable {av} MiB (alert only)\n")


def lam_of(rec, one=1):
    """gamma's lam from a lowD_gamma.py record when it has exactly `one` sign change, else None"""
    return rec.get("lam") if rec.get("n_signchanges") == one and rec.get("lam") is not None else None


def selftest(mutate):
    one = 0 if mutate else 1
    cases = [({"n_signchanges": 1, "lam": 3.4}, 3.4), ({"n_signchanges": 0, "lam": None}, None), ({"n_signchanges": 2, "lam": 3.4}, None), ({"n_signchanges": 1, "lam": None}, None)]
    ok = True
    for rec, want in cases:
        got = lam_of(rec, one=one) if not mutate else (rec.get("lam") if rec.get("n_signchanges", 0) >= 1 else None)
        print(f"selftest: {'pass' if got == want else 'FAIL'}: {rec}: want {want}, got {got}")
        ok &= got == want
    return ok


def gamma_stage(label, state, out, lam0, log, cap, tag):
    cmd = ["nice", "-n", "10", "/usr/bin/time", "-v", "timeout", "-s", "TERM", str(cap), PY, "-u", "hp/lowD_gamma.py", out, state, "--threads=4", "--polish=2", "--xtol=1e-11", f"--lam0={lam0}"]
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
    cmd = ["nice", "-n", "10", "/usr/bin/time", "-v", "timeout", "-s", "TERM", "10800", PY, "-u", "lowD_dd.py", f"{P}/lift128_d335.jsonl", "--start", IN96, "--Ms", "128", "--nodes", NODES, "--kt", "36",
           "--kcs", "100", "--ks", "250", "--jac", "f64", "--tol", "1e-29", "--threads", "4", "--tag", "lowD1070b"]
    say("lift start: " + " ".join(cmd[6:]))
    if os.environ.get("DRY"):
        return None, "dry", []
    t0 = time.time()
    logf = open(f"{P}/lift128_d335.log", "w")
    proc = subprocess.Popen(cmd, cwd=f"{WT}/hp", env=env, stdout=logf, stderr=subprocess.STDOUT, start_new_session=True)
    seen, Fs, chosen, verdict, peak, tick = 0, [], None, None, [0], 0
    pat = r"^  newton \d+: .* lam "
    while True:
        time.sleep(20)
        tick += 1
        if tick % 3 == 0:
            sample(proc, "lift", peak)
        text = open(f"{P}/lift128_d335.log").read()
        n = len(re.findall(pat, text, re.M))
        if n > seen and os.path.exists(CKPT):
            seen = n
            dst = f"{P}/states/lowD1070b_D3.3500_M128_ckpt_after_call{n}.npz"
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
        shutil.copy2(chosen, M128)
        say(f"lift done, wall {int(time.time() - t0)} s: {os.path.basename(chosen)} copied to states/lowD1070b_D3.3500_M128.npz")
    return chosen, verdict, Fs


def wait_for_a():
    while True:
        if os.path.exists(EXITS) and any(re.search(r"UTC A done", ln) for ln in open(EXITS)):
            return
        time.sleep(20)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    which = sys.argv[1] if len(sys.argv) > 1 else ""
    if which not in ("A", "B"):
        sys.exit("usage: run_d335.py A | B | --selftest [--mutate]")
    WHO = which + " "
    if subprocess.run(["git", "hash-object", "--no-filters", IN96], capture_output=True, text=True).stdout.strip() != IN96_BLOB:
        say("refuse: the input blob is not " + IN96_BLOB)
        sys.exit(2)
    if which == "A":
        log = f"{P}/stageA_gamma96_d335.log"
        if os.path.exists(log) or os.path.exists(REC_A):
            say("refuse: a log or record exists (no overwrite)")
            sys.exit(3)
        gamma_stage("gamma at M 96", IN96, REC_A, LAM0, log, 10800, "A")
        say("done")
    else:
        if os.path.exists(f"{P}/lift128_d335.log") or os.path.exists(REC_B):
            say("refuse: a log or record exists (no overwrite)")
            sys.exit(3)
        chosen, verdict, Fs = lift()
        if not chosen:
            say(f"STOP: the lift did not reach a converged M 128 state (verdict {verdict}, max|F| after the calls {Fs}); gamma at M 128 not started")
            say("done")
            sys.exit(1)
        say("waiting for A's done line")
        wait_for_a()
        recs = [json.loads(ln) for ln in open(REC_A)] if os.path.exists(REC_A) else []
        lam = lam_of(recs[-1]) if recs else None
        if lam is None:
            say("STOP: A has no record with exactly one sign change; gamma at M 128 not started")
            say("done")
            sys.exit(1)
        gamma_stage("gamma at M 128", M128, REC_B, repr(lam), f"{P}/stageB2_gamma128_d335.log", 10800, "B2")
        say("done")

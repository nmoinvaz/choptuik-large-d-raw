#!/usr/bin/env python3
"""#1070 D 3.475 (coordinator's hc after the 00:21 UTC D 3.45 report): gamma at M 96 and at M 128 on T39's stored states, no lift.
    run_d3475.py           A: lowD_gamma.py OUT <lowDvh41_D3.4750_M96.npz> --threads=4 --polish=2 --xtol=1e-11 --lam0=3.14208, cap 2 h, then accept_1070.py;
                           B (only if A has exactly one sign change): the same on the M 128 state with --lam0 = A's lam, cap 2 h, then accept_1070.py
lam_of() is run_d335.py's (selftest there); the gamma stage is run_d335c.py's with the names of this task."""
import importlib.util
import json
import os
import subprocess
import sys
import time

P = "/home/nathan/Source/choptuik-large-d-raw-1064w/I1070-dh170"
spec = importlib.util.spec_from_file_location("d335", f"{P}/run_d335.py")
d = importlib.util.module_from_spec(spec)
spec.loader.exec_module(d)
WT, PY = d.WT, d.PY
IND = "/home/nathan/scratch1070/T39-win/hp/data/lowD_states"
INS = {96: (f"{IND}/lowDvh41_D3.4750_M96.npz", "18811cf5502ad4c0dafa5e31de83446e93472df4"), 128: (f"{IND}/lowDvh41_D3.4750_M128.npz", "d1467b1e3c69dd8b3d81c50b6816c9fc9b2c16a4")}
LAM0 = "3.14208"
CAP = 7200
EXITS = f"{P}/exits_d3475.txt" if not os.environ.get("DRY") else "/tmp/claude-1000/-home-nathan-Source-choptuik-large-d/026ace6b-8e85-4de1-9fd2-85ec04d52786/scratchpad/dry_exits_d3475.txt"


def say(msg):
    with open(EXITS, "a") as f:
        f.write(f"== {time.strftime('%F %T', time.gmtime())} UTC {msg}\n")


def sample(proc, tag, peak):
    """one line of the memory log: RSS summed over the session of proc, its peak, and the machine's MemAvailable"""
    r = subprocess.run(["ps", "-o", "rss=,pcpu=", "--sid", str(proc.pid)], capture_output=True, text=True).stdout.split()
    rss = sum(int(x) for x in r[0::2]) // 1024
    cpu = sum(float(x) for x in r[1::2])
    av = int([ln for ln in open("/proc/meminfo") if ln.startswith("MemAvailable")][0].split()[1]) // 1024
    peak[0] = max(peak[0], rss)
    with open(f"{P}/memlog_d3475.log", "a") as f:
        f.write(f"{time.strftime('%T', time.gmtime())} {tag} RSS {rss} MiB (peak {peak[0]}) cpu {cpu:.0f}% MemAvailable {av} MiB\n")
    if av < 2048:
        with open(f"{P}/alert_d3475.log", "a") as f:
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


if __name__ == "__main__":
    for M, (f, blob) in INS.items():
        if subprocess.run(["git", "hash-object", "--no-filters", f], capture_output=True, text=True).stdout.strip() != blob:
            say(f"refuse: the M {M} input blob is not {blob}")
            sys.exit(2)
    rec_a, rec_b = f"{P}/lowD_gamma_D3.475_M96.jsonl", f"{P}/lowD_gamma_D3.475_M128.jsonl"
    log_a, log_b = f"{P}/stageA_gamma96_d3475.log", f"{P}/stageB_gamma128_d3475.log"
    if any(os.path.exists(x) for x in (rec_a, rec_b, log_a, log_b)):
        say("refuse: a log or record exists (no overwrite)")
        sys.exit(3)
    gamma_stage("A gamma at M 96", INS[96][0], rec_a, LAM0, log_a, "A")
    recs = [json.loads(ln) for ln in open(rec_a)] if os.path.exists(rec_a) else []
    lam = d.lam_of(recs[-1]) if recs else None
    if lam is None:
        say("STOP: A has no record with exactly one sign change; B not started")
        say("done")
        sys.exit(1)
    gamma_stage("B gamma at M 128", INS[128][0], rec_b, repr(lam), log_b, "B")
    say("done")

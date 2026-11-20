#!/usr/bin/env python3
"""#1025 (win), the coordinator's order of 2026-11-20: the k_c 63 leap goes only to D 18 (one cross-check of the Mac's k_c 55 there),
under the same 12 h cap, then stops. ell_win1025.sh's P1 subshell is already parsed and starts `ell_leap.py ... 17.5 20 ...` when the D 17.5 start
is done. This guard waits for that process, kills only its tree at its start (nothing is computed in its first minute), and runs the same
command with D_end 18 in its place, appending to logs1025/leap_kc63.log with a header that says so. When the leap ends with exit 0 it runs
lambda at D 18 on the k_c 63 state only when cfg run_lam is set (off since 2026-11-20 ~03:58 UTC, the coordinator's order: the root finder lam_root
fails past D 17, so no lambda is taken at D 18; the leap's state data/sol_l1kc63W1025_D18.0000.npy is kept for later); in that mode if P2's ell_refine
is alive it waits for it first.

usage (detached, BelowNormal): python guard_leap_1025.py [--now]    python guard_leap_1025.py --selftest
--now (2026-11-20, the coordinator's order): do not wait for the script's leap, run the leap to D 18 at once (the script's P1 subshell is stopped by exact pid first).
Exit: 0 done, 1 the replacement leap did not exit 0, 2 the lambda run did not exit 0, 4 STOP_GUARD_1025 file."""
import json
import os
import subprocess
import sys
import tempfile
import time

WT = r"C:\Users\nathan\Source\choptuik-i1025"
PY = r"C:\Users\nathan\Source\venv-choptuik-314\Scripts\python.exe"
FLAGS = 0x00004000 | 0x08000000            # BelowNormal, no window
CAP_S = 43200                              # 12 h, as the script's timeout
LEAP = ["ell_leap.py", "l1kc63W1025", "1", "63", "data/sol_l1kc63Fw1025_D17.0000.npy", "17", "data/sol_l1kc63Fw1025_D17.5000.npy", "17.5",
        "18", "0.125", "--tol", "1e-12", "--fmax", "1e-8", "--cmax", "1e-2", "--fold"]
LAM = ["ell_refine.py", "l1kc63W1025", "63", "l1kc63Fw1025", "63", "1", "18", "1.9", "--kappa", "0.7", "--u0", "0.04", "--Ks", "30",
       "--tol", "1e-12", "--wait", "600"]


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())


def python_procs():
    """[(pid, ppid, cmdline)] of the python processes"""
    ps = ("Get-CimInstance Win32_Process | Where-Object { $_.Name -like 'python*' } | "
          "Select-Object ProcessId,ParentProcessId,CommandLine | ConvertTo-Json -Compress")
    out = subprocess.run(["powershell", "-NoProfile", "-Command", ps], capture_output=True, text=True).stdout.strip()
    if not out:
        return []
    d = json.loads(out)
    d = d if isinstance(d, list) else [d]
    return [(int(x["ProcessId"]), int(x["ParentProcessId"]), x["CommandLine"] or "") for x in d]


def find_tops(words):
    """the matching python processes whose parent does not match (the launcher shim of a tree), excluding this process"""
    me = os.getpid()
    ms = [(p, q, c) for p, q, c in python_procs() if p != me and all(w in c for w in words)]
    ids = {p for p, _, _ in ms}
    return [p for p, q, _ in ms if q not in ids]


def kill_tree(pid):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)


def logline(path, msg):
    with open(path, "a") as f:
        f.write(msg + "\n")


def run_logged(cmd, cwd, env, logfile, cap_s, stopfile):
    """appends the child's output to logfile and `== exit N` after it; returns N (None when STOP, -9 on the cap)"""
    with open(logfile, "a") as lf:
        p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=lf, stderr=subprocess.STDOUT, creationflags=FLAGS)
        t = time.time()
        while p.poll() is None:
            time.sleep(5)
            if os.path.exists(stopfile):
                kill_tree(p.pid)
                p.wait()
                logline(logfile, f"== killed (STOP file) {now()}")
                return None
            if time.time() - t > cap_s:
                kill_tree(p.pid)
                p.wait()
                logline(logfile, f"== killed (cap {cap_s / 3600:.0f} h) {now()}")
                return -9
    logline(logfile, f"== exit {p.returncode} {now()}")
    return p.returncode


def has_lam(jsonl, D):
    if not os.path.exists(jsonl):
        return False
    for line in open(jsonl):
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if abs(r.get("D", -1) - D) < 1e-9 and r.get("lam"):
            return True
    return False


def guard(cfg):
    gl = os.path.join(cfg["logs"], "guard_1025.log")
    th = str(cfg.get("threads", 4))          # 4 BLAS threads (the script used 2): the eigenvalue scans were stopped, the cores are free
    env = dict(os.environ, OPENBLAS_NUM_THREADS=th, OMP_NUM_THREADS=th, MKL_NUM_THREADS=th, PYTHONDONTWRITEBYTECODE="1")
    ll = os.path.join(cfg["logs"], "leap_kc63.log")
    if cfg.get("now"):          # --now: the script's P1 subshell was stopped, so no leap of the script will start; run the leap at once
        logline(gl, f"{now()} UTC guard start (--now): no script leap to wait for, running the leap to D 18 at once")
        logline(ll, f"== {now()} {' '.join(cfg['leap_cmd'][1:])}   (D_end 18 in place of the script's 20 and {th} BLAS threads in place of 2, the coordinator's orders; started before D 17.5's lambda was done, the script's P1 subshell having been stopped so that its own leap never starts)")
    else:
        logline(gl, f"{now()} UTC guard start; waiting for a python process with {cfg['leap_match']}")
        while True:
            if os.path.exists(cfg["stop"]):
                logline(gl, f"{now()} UTC STOP file, guard ends")
                return 4
            tops = find_tops(cfg["leap_match"])
            if tops:
                break
            time.sleep(cfg["poll"])
        for pid in tops:
            kill_tree(pid)
        logline(gl, f"{now()} UTC killed the script's leap, pid(s) {tops}")
        logline(ll, f"== {now()} {' '.join(cfg['leap_cmd'][1:])}   (D_end 18 in place of the script's 20, the coordinator's order; {th} BLAS threads in place of 2, the scans having been stopped; the script's own leap was killed at its start)")
    rc = run_logged(cfg["leap_cmd"], cfg["cwd"], env, ll, CAP_S, cfg["stop"])
    logline(gl, f"{now()} UTC replacement leap ended, exit {rc}")
    if rc != 0:
        return 1 if rc is not None else 4
    if not cfg.get("run_lam", True):
        logline(gl, f"{now()} UTC lambda at D 18 not run (the coordinator's order of 2026-11-20: the root finder fails past D 17); the leap's state is kept")
        return 0
    while not has_lam(cfg["jsonl"], 18.0):
        if find_tops(cfg["lam_match"]):          # P2's ell_refine is alive (it may be computing D 18): wait for it
            time.sleep(cfg["poll"])
            continue
        al = os.path.join(cfg["logs"], "lam_kc63.log")
        logline(al, f"== {now()} {' '.join(cfg['lam_cmd'][1:])}   (lambda at D 18 on the leap's state, run by the guard since the script's P2 had ended)")
        rc = run_logged(cfg["lam_cmd"], cfg["cwd"], env, al, CAP_S, cfg["stop"])
        logline(gl, f"{now()} UTC lambda run ended, exit {rc}")
        return 0 if rc == 0 and has_lam(cfg["jsonl"], 18.0) else 2
    logline(gl, f"{now()} UTC lambda at D 18 present in {cfg['jsonl']}")
    return 0


def selftest():
    bad = 0
    with tempfile.TemporaryDirectory() as td:
        logs = os.path.join(td, "logs")
        os.makedirs(logs)
        jsonl = os.path.join(td, "rec.jsonl")
        stop = os.path.join(td, "STOP")
        # a stand-in for the script's leap: a python whose command line carries the match words, alive for 300 s
        victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)", "ell_leap.py", "l1kcSELFTEST", "20"], creationflags=FLAGS)
        time.sleep(3)
        rep = [sys.executable, "-c", "import os; print('replacement leap, D_end 18, threads', os.environ['OPENBLAS_NUM_THREADS'], os.environ['OMP_NUM_THREADS'], os.environ['MKL_NUM_THREADS'])"]
        lam = [sys.executable, "-c", f"open(r'{jsonl}', 'a').write('{{\"D\": 18.0, \"lam\": 2.0}}\\n'); print('lam run')"]
        cfg = dict(logs=logs, cwd=td, stop=stop, poll=1, jsonl=jsonl, leap_match=["ell_leap.py", "l1kcSELFTEST"], lam_match=["ell_refine.py", "l1kcSELFTEST"],
                   leap_cmd=rep, lam_cmd=lam)
        rc = guard(cfg)
        alive = victim.poll() is None
        t = open(os.path.join(logs, "leap_kc63.log")).read()
        a = open(os.path.join(logs, "lam_kc63.log")).read()
        ok = rc == 0 and not alive and "replacement leap, D_end 18, threads 4 4 4" in t and "== exit 0" in t and "lam run" in a and '"D": 18.0' in open(jsonl).read()
        print(f"  leap killed at its start, replacement run, lambda run: exit {rc}, victim alive {alive} {'ok' if ok else 'WRONG'}")
        bad += not ok
        if alive:
            kill_tree(victim.pid)
        # replacement leap fails: exit 1, no lambda run
        victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)", "ell_leap.py", "l1kcSELFTEST", "20"], creationflags=FLAGS)
        time.sleep(3)
        os.remove(os.path.join(logs, "lam_kc63.log"))
        open(jsonl, "w").close()
        cfg["leap_cmd"] = [sys.executable, "-c", "import sys; sys.exit(3)"]
        rc = guard(cfg)
        ok = rc == 1 and not os.path.exists(os.path.join(logs, "lam_kc63.log"))
        print(f"  replacement leap exits 3: guard exit {rc}, no lambda run {'ok' if ok else 'WRONG'}")
        bad += not ok
        kill_tree(victim.pid)
        # lambda at D 18 already present: no lambda run
        victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)", "ell_leap.py", "l1kcSELFTEST", "20"], creationflags=FLAGS)
        time.sleep(3)
        open(jsonl, "w").write('{"D": 18.0, "lam": 2.0}\n')
        cfg["leap_cmd"] = rep
        rc = guard(cfg)
        ok = rc == 0 and not os.path.exists(os.path.join(logs, "lam_kc63.log"))
        print(f"  lambda at D 18 already recorded: guard exit {rc}, no lambda run {'ok' if ok else 'WRONG'}")
        bad += not ok
        kill_tree(victim.pid)
        # run_lam off: the leap is replaced and run, no lambda run, exit 0
        victim = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(300)", "ell_leap.py", "l1kcSELFTEST", "20"], creationflags=FLAGS)
        time.sleep(3)
        open(jsonl, "w").close()
        cfg["run_lam"] = False
        rc = guard(cfg)
        ok = rc == 0 and not os.path.exists(os.path.join(logs, "lam_kc63.log")) and "lambda at D 18 not run" in open(os.path.join(logs, "guard_1025.log")).read()
        print(f"  run_lam off: guard exit {rc}, no lambda run, the log says so {'ok' if ok else 'WRONG'}")
        bad += not ok
        kill_tree(victim.pid)
        cfg["run_lam"] = True
        # --now: no victim to kill, the replacement leap runs at once
        os.remove(os.path.join(logs, "leap_kc63.log"))
        cfg["now"] = True
        cfg["run_lam"] = False
        rc = guard(cfg)
        lt = open(os.path.join(logs, "leap_kc63.log")).read()
        ok = rc == 0 and "threads 4 4 4" in lt and "started before D 17.5's lambda was done" in lt
        print(f"  --now: leap run at once, no wait: guard exit {rc} {'ok' if ok else 'WRONG'}")
        bad += not ok
        cfg["now"] = False
        # STOP file before any leap: exit 4
        open(stop, "w").write("x")
        cfg["leap_match"] = ["ell_leap.py", "l1kcNOSUCH"]
        rc = guard(cfg)
        ok = rc == 4
        print(f"  STOP file: guard exit {rc} (want 4) {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    matter = os.path.join(WT, "solver", "matter")
    logs = os.path.join(WT, "logs1025")
    cfg = dict(logs=logs, cwd=matter, stop=os.path.join(WT, "STOP_GUARD_1025"), poll=10, run_lam=False, now="--now" in sys.argv, jsonl=os.path.join(matter, "data", "l1kc63Fw1025.jsonl"),
               leap_match=["ell_leap.py", "l1kc63W1025"], lam_match=["ell_refine.py", "l1kc63W1025"],
               leap_cmd=[PY, "-u"] + LEAP, lam_cmd=[PY, "-u"] + LAM)
    sys.exit(guard(cfg))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""I574-win3 driver: one hp/modecount_circle.py process per circle (one thread, below-normal priority, its own empty
cache and folder), the cap on points enforced from outside because the script has none.

    python drive_574.py RE,IM,R [RE,IM,R ...] [--procs=20] [--stagger=15] [--min_free_gb=4] [--cap=150] [--base=DIR]
    python drive_574.py --status [--base=DIR]

--cap=N and --base=DIR (the folder that holds the circles, default this one) are for the control: a small cap must stop
a circle and write cap.json.

A circle's folder is <this folder>/c<RE><IM>i_R<R>/ with circles.jsonl (the script's record), the script's log and
cache, run.log (its output) and, when it is stopped, cap.json. The cap: a process whose evaluation cache holds more
than CAP + 2 determinants (the 2 are the points c +- 2R of the detrending slope, "+2 for beta" in the script's log) is
killed with its children and cap.json is written; the circle is reported as "cap", never as a winding. A process
that exits non-zero is reported as "error" (its run.log holds the Traceback). A circle with a record already in its
circles.jsonl is skipped, so the same command can be run again. Windows only (priority class, taskkill).
"""
import ctypes
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
HP = r"C:\Users\nathan\Source\choptuik-i574\hp"
PY = r"C:\Users\nathan\Source\choptuik-large-d\.venv\Scripts\python.exe"
SEED = "data/seeds/local/up23_D61.0264.npz"
TAG = "D61.0264_M48_kf27"
CAP = 150
BELOW_NORMAL = 0x00004000


BASE = HERE


def folder(re, im, R):
    return os.path.join(BASE, f"c{re:+.4f}{im:+.4f}i_R{R:g}")


def free_gb():
    class MS(ctypes.Structure):
        _fields_ = [("len", ctypes.c_ulong), ("load", ctypes.c_ulong)] + \
                   [(n, ctypes.c_ulonglong) for n in ("tp", "ap", "tpf", "apf", "tv", "av", "aev")]
    m = MS()
    m.len = ctypes.sizeof(m)
    ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m))
    return m.ap / 2**30


def n_evals(d):
    p = os.path.join(d, f"modecount_{TAG}_evals.jsonl")
    try:
        with open(p, "rb") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def record(d):
    p = os.path.join(d, "circles.jsonl")
    if os.path.exists(p):
        lines = [json.loads(x) for x in open(p) if x.strip()]
        return lines[-1] if lines else None
    return None


def status():
    rows = []
    for n in sorted(os.listdir(BASE)):
        d = os.path.join(BASE, n)
        if not (n.startswith("c") and os.path.isdir(d)):
            continue
        r, cap = record(d), os.path.exists(os.path.join(d, "cap.json"))
        if r:
            z = "; ".join(f"{a:.6f}{b:+.6f}i" for a, b in r.get("zeros", []))
            rows.append(f"{n:34s} winding {r['winding']:+.4f} points {r['points']:3d} "
                        f"{'resolved' if r['resolved'] else 'UNRESOLVED'} {z}")
        else:
            rows.append(f"{n:34s} {'CAP' if cap else 'running/none'} evals {n_evals(d)}")
    print("\n".join(rows))


def kill_tree(p):
    subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)


def main():
    global BASE, CAP
    argv = sys.argv[1:]
    opt = {a.split("=")[0]: a.split("=")[1] for a in argv if a.startswith("--") and "=" in a}
    BASE, CAP = os.path.abspath(opt.get("--base", HERE)), int(opt.get("--cap", CAP))
    if "--status" in argv:
        return status()
    specs = [tuple(float(v) for v in a.split(",")) for a in argv if not a.startswith("--")]
    os.makedirs(BASE, exist_ok=True)
    procs, stagger, min_free = int(opt.get("--procs", 20)), float(opt.get("--stagger", 15)), float(opt.get("--min_free_gb", 4))
    todo, running, done = [], {}, {}
    for re, im, R in specs:
        d = folder(re, im, R)
        if record(d):
            done[d] = "done"
        else:
            todo.append((re, im, R, d))
    last_start, last_msg = 0.0, 0.0
    print(time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()), f"{len(todo)} circles to run, {len(done)} already recorded", flush=True)
    while todo or running:
        now = time.time()
        while todo and len(running) < procs and now - last_start >= stagger and free_gb() >= min_free:
            re, im, R, d = todo.pop(0)
            os.makedirs(d, exist_ok=True)
            cmd = [PY, "-u", "modecount_circle.py", SEED, f"{re},{im},{R}", "--M=48", "--kf=27", "--n0=20",
                   "--fmax=1e-15", f"--data={d}", f"--res={os.path.join(d, 'circles.jsonl')}"]
            out = open(os.path.join(d, "run.log"), "a")
            p = subprocess.Popen(cmd, cwd=HP, stdout=out, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL)
            running[d] = (p, out, time.time())
            last_start = time.time()
            print(time.strftime("%H:%MZ", time.gmtime()), "start", os.path.basename(d), "pid", p.pid, f"free {free_gb():.1f} GB", flush=True)
        for d, (p, out, t0) in list(running.items()):
            rc, n = p.poll(), n_evals(d)
            if rc is None and n > CAP + 2:
                kill_tree(p)
                p.wait()
                json.dump(dict(cap=CAP, evals=n, seconds=round(time.time() - t0)), open(os.path.join(d, "cap.json"), "w"))
                done[d] = "cap"
                print(time.strftime("%H:%MZ", time.gmtime()), "CAP", os.path.basename(d), "evals", n, flush=True)
            elif rc is not None:
                done[d] = "done" if rc == 0 else "error"
                r = record(d)
                print(time.strftime("%H:%MZ", time.gmtime()), done[d].upper(), os.path.basename(d), "exit", rc, "evals", n,
                      (f"winding {r['winding']:+.4f} points {r['points']} resolved {r['resolved']}" if r else ""), flush=True)
            else:
                continue
            out.close()
            del running[d]
        if time.time() - last_msg > 300 and running:
            last_msg = time.time()
            print(time.strftime("%H:%MZ", time.gmtime()), f"free {free_gb():.1f} GB;",
                  " ".join(f"{os.path.basename(d)[:14]}:{n_evals(d)}" for d in running), flush=True)
        time.sleep(5)
    print(time.strftime("%Y-%m-%d %H:%M:%SZ", time.gmtime()), "all finished:", {os.path.basename(d): s for d, s in done.items()}, flush=True)
    status()


if __name__ == "__main__":
    main()

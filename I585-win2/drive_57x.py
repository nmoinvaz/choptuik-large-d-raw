#!/usr/bin/env python3
"""Driver of the mode-count circles of #573 and #574 (and their stages 2 and the mirrors): one process, one thread, below-normal priority, per circle, each with its own empty cache, up to MAXP at once.
usage: python drive_57x.py JOBS.json [--maxp 18] [--cap 150]
JOBS.json: a list of {"task": "I573-win2" | "I574-win2", "name": str, "K": int, "re": float, "im": float, "R": float}. For each job, from D:/choptuik-i573/hp with venv-t126's python:
  python modecount_circle.py data/seeds/local/up23_D61.0264.npz RE,IM,R --M=48 --kf=K --n0=20 --fmax=1e-15 --data=<RAW>/<task>/<name> --res=<RAW>/<task>/<name>/res.jsonl
The state modecount_state_D61.0264_M48_kf<K>.npz is read from hp/data (copied there, sha256 in the READMEs). A job whose res.jsonl already has a record is skipped (resume). The cap: modecount_circle.py has no cap, so the driver counts the
lines of the circle's evaluation cache (each is one determinant; the first two are the beta points) and stops the process tree when it holds more than cap + 2, writing {"cap": true} to <name>/cap.json: 'cap' means the circle needed more than 150
points. Every start and end goes to <RAW>/<task>/jobs_status.jsonl with the exit code and the number of evaluations."""
import json, os, subprocess, sys, time

PY = "C:/Users/nathan/Source/venv-t126/Scripts/python.exe"
HP = "D:/choptuik-i573/hp"
RAW = "D:/choptuik-large-d-raw"
BELOW_NORMAL = 0x00004000
NO_WINDOW = 0x08000000


def argval(flag, default):
    return type(default)(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default


def cache_lines(path):
    try:
        with open(path, "rb") as f:
            return sum(1 for _ in f)
    except OSError:
        return 0


def done(job):
    p = os.path.join(RAW, job["task"], job["name"], "res.jsonl")
    return os.path.exists(p) and os.path.getsize(p) > 0


def status(job, **kw):
    with open(os.path.join(RAW, job["task"], "jobs_status.jsonl"), "a") as f:
        f.write(json.dumps(dict(name=job["name"], t=time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()), **kw)) + "\n")


def launch(job):
    d = os.path.join(RAW, job["task"], job["name"])
    os.makedirs(d, exist_ok=True)
    cmd = [PY, "-u", "modecount_circle.py", "data/seeds/local/up23_D61.0264.npz", f"{job['re']},{job['im']},{job['R']}", "--M=48", f"--kf={job['K']}", "--n0=20", "--fmax=1e-15",
           f"--data={d}", f"--res={d}/res.jsonl"]
    env = dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS="1", PYTHONFAULTHANDLER="1")
    out = open(os.path.join(d, "stdout.log"), "a")
    p = subprocess.Popen(cmd, cwd=HP, env=env, stdout=out, stderr=subprocess.STDOUT, creationflags=BELOW_NORMAL | NO_WINDOW)
    status(job, event="start", pid=p.pid, cmd=" ".join(cmd[1:]))
    return p, out, d


def main():
    jobs = json.load(open(sys.argv[1]))
    maxp, cap = argval("--maxp", 18), argval("--cap", 150)
    queue = [j for j in jobs if not done(j)]
    run = []
    print(f"{len(jobs)} jobs, {len(queue)} to run, at most {maxp} at once, cap {cap} points", flush=True)
    while queue or run:
        while queue and len(run) < maxp:
            j = queue.pop(0)
            p, out, d = launch(j)
            run.append((j, p, out, d, time.time()))
        time.sleep(15)
        for item in list(run):
            j, p, out, d, t0 = item
            n = cache_lines(os.path.join(d, "modecount_D61.0264_M48_kf%d_evals.jsonl" % j["K"]))
            rc = p.poll()
            if rc is None and n > cap + 2:
                subprocess.run(["taskkill", "/T", "/F", "/PID", str(p.pid)], capture_output=True)
                p.wait()
                json.dump(dict(cap=True, evaluations=n, points_cap=cap), open(os.path.join(d, "cap.json"), "w"))
                status(j, event="cap", evaluations=n, seconds=round(time.time() - t0))
                out.close(); run.remove(item)
            elif rc is not None:
                status(j, event="end", exit=rc, evaluations=n, seconds=round(time.time() - t0))
                out.close(); run.remove(item)
    print("all jobs ended", flush=True)


if __name__ == "__main__":
    main()

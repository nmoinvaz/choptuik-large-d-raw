#!/usr/bin/env python3
"""Evaluation of det M at kf 27 for #585: ulp moves, repeats and derivative points at the five points of points_585.json (design in predictions_585.json).
usage: python noise_585.py [--workers 16]       writes evals_585.jsonl (one record per evaluation), skipping tasks already in it (resume)
Per point: kind 'ref' (1), 're' j = 1..25 (Re moved j ulp toward +inf), 'im' j = 1..25 (Im likewise), 'rep' r = 0..49 (the reference argument again, each a separate
task spread over the worker processes), 'dre' (Re -+ 1e-3, two tasks). Each record: id, kind, j, re, im, lnabs, arg, pmin, pmax, sec, worker pid.
Run with venv-t126's python (modecount_cx); the worker imports hp/ from D:/choptuik-i573/hp, one thread per process."""
import concurrent.futures as cf, json, math, os, random, sys, time

HP = "D:/choptuik-i573/hp"
HERE = os.path.dirname(os.path.abspath(__file__))
ST = None


def init():
    global ST
    os.environ["OMP_NUM_THREADS"] = "1"
    os.chdir(HP)
    sys.path.insert(0, HP)
    from modecount_common import setup
    ST = setup("data/seeds/local/up23_D61.0264.npz", M=48, threads=1, kf=27, fmax=1e-15, centre_tol=None)


def work(task):
    pid, kind, j, re_, im = task
    t = time.time()
    la, arg, pmin, pmax = ST.det(re_, im)
    return dict(id=pid, kind=kind, j=j, re=re_, im=im, lnabs=la, arg=arg, pmin=pmin, pmax=pmax, sec=round(time.time() - t, 2), worker=os.getpid())


def tasks_for(points):
    out = []
    for p in points:
        x, y = p["re"], p["im"]
        out.append((p["id"], "ref", 0, x, y))
        xr, yr = x, y
        for j in range(1, 26):
            xr = math.nextafter(xr, math.inf)
            out.append((p["id"], "re", j, xr, y))
        for j in range(1, 26):
            yr = math.nextafter(yr, math.inf)
            out.append((p["id"], "im", j, x, yr))
        for r in range(50):
            out.append((p["id"], "rep", r, x, y))
        out.append((p["id"], "dre", -1, x - 1e-3, y))
        out.append((p["id"], "dre", 1, x + 1e-3, y))
    return out


if __name__ == "__main__":
    workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 16
    points = json.load(open(os.path.join(HERE, "points_585.json")))
    out_path = os.path.join(HERE, "evals_585.jsonl")
    done = set()
    if os.path.exists(out_path):
        for l in open(out_path):
            r = json.loads(l)
            done.add((r["id"], r["kind"], r["j"], r["re"], r["im"]) if r["kind"] != "rep" else (r["id"], "rep", r["j"], r["re"], r["im"]))
    todo = [t for t in tasks_for(points) if t not in done]
    random.Random(585).shuffle(todo)
    print(f"{len(todo)} evaluations to run on {workers} workers", flush=True)
    t0 = time.time()
    with cf.ProcessPoolExecutor(max_workers=workers, initializer=init) as ex, open(out_path, "a") as f:
        futs = [ex.submit(work, t) for t in todo]
        for n, fu in enumerate(cf.as_completed(futs), 1):
            f.write(json.dumps(fu.result()) + "\n")
            f.flush()
            if n % 50 == 0:
                print(f"  {n} done, {time.time() - t0:.0f} s", flush=True)
    print(f"all done in {time.time() - t0:.0f} s", flush=True)

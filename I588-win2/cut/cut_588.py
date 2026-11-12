#!/usr/bin/env python3
"""The replica spread of the R 0.06 circle on lambda_phys against the cut kf (#588's recommended task, approved by the coordinator at 16:22 UTC 2026-11-12).
The same circle() call and the same ulp replicas as ../replicas_588.py (n0 20, tol pi/4, every argument moved by 1 to 3 ulp in Re and Im), for one circle per cut: centre
(2.044645, -0.00032), R 0.06, the circle of #573 that holds lambda_phys = 2.0435 at kf 22 and 25. Per cut: 10 shifted replicas (rep 1..10) and 2 controls (rep 0, no move, each evaluated
freshly with its own memo; they must agree bit for bit with each other).
usage: python cut_588.py run [--workers 3] [--kfs 21,23,24,26,28,29]   writes cut_588.jsonl (one record per replica run) and cut_588_evals.jsonl (one per determinant); resumes
       python cut_588.py pilot KF                                   builds the state at KF and evaluates det M once at the circle's centre (not an argument of circle()), prints the time
       python cut_588.py --selftest                                 the task list (6 cuts x 12 runs, controls first, ordered by cut), the controls unmoved, and ../replicas_588.py's synthetic checks
Run with venv-t126's python (modecount_cx); the workers import hp/ from D:/choptuik-i573/hp (main 80b5056), one thread per process, a state per kf made on first use."""
import concurrent.futures as cf, json, math, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import replicas_588 as RP  # noqa: E402

CENTRE, R = [2.044645, -0.00032], 0.06
KFS = [21, 23, 24, 26, 28, 29]
NREP = 10


def circle_of(kf):
    return dict(name=f"k{kf}_phys", task="I588-win2/cut", kf=kf, centre=CENTRE, R=R)


def task_list(kfs):
    """(circle, rep, tag) ordered by cut, the two controls (rep 0, tags a and b) first within a cut, then the ten shifted replicas"""
    out = []
    for kf in kfs:
        c = circle_of(kf)
        out += [(c, 0, "a"), (c, 0, "b")] + [(c, r, str(r)) for r in range(1, NREP + 1)]
    return out


def work(task):
    circle, rep, tag = task
    rec, evals = RP.run_replica(circle, rep, RP.real_det(circle["kf"]))
    for e in evals:
        e["tag"] = tag
    out = dict(circle=circle["name"], rep=rep, tag=tag, kf=circle["kf"], winding=rec["winding"], resolved=rec["resolved"], points=rec["points"], n_evals=len(evals),
               zero=rec["zeros"][0] if rec.get("zeros") else None, est=rec["zeros_est"][0] if rec.get("zeros") else None, worker=os.getpid())
    return out, evals


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        ok = True
        tl = task_list(KFS)
        good = len(tl) == 72 and [t[2] for t in tl[:3]] == ["a", "b", "1"] and all(tl[i][0]["kf"] <= tl[i + 1][0]["kf"] for i in range(len(tl) - 1))
        good &= all(RP.shift_arg(t[0]["name"], t[1], 2.0, 0.1) == (2.0, 0.1) for t in tl if t[1] == 0)
        good &= all(RP.shift_arg(t[0]["name"], t[1], 2.0, 0.1) != (2.0, 0.1) for t in tl if t[1] > 0 and t[2] == str(t[1]) and t[1] in (1, 2, 3))
        print("task list: 72 runs, ordered by cut, controls first and unmoved, replicas moved:", "ok" if good else "FAIL")
        ok &= good
        r = subprocess.run([sys.executable, os.path.join(os.path.dirname(HERE), "replicas_588.py"), "--selftest"], capture_output=True, text=True)
        sys.stdout.write(r.stdout)
        ok &= r.returncode == 0
        sys.exit(0 if ok else 1)
    if sys.argv[1:2] == ["pilot"]:
        kf = int(sys.argv[2])
        t = time.time()
        det = RP.real_det(kf)
        t1 = time.time()
        la, arg = det(CENTRE[0], CENTRE[1])
        print(f"kf {kf}: state made in {t1 - t:.0f} s; det M at the centre {CENTRE}: ln|det| {la:.6f}, arg {arg:.6f}, {time.time() - t1:.1f} s", flush=True)
        sys.exit(0)
    if sys.argv[1:2] == ["run"]:
        workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 3
        kfs = [int(k) for k in sys.argv[sys.argv.index("--kfs") + 1].split(",")] if "--kfs" in sys.argv else KFS
        out_path, ev_path = os.path.join(HERE, "cut_588.jsonl"), os.path.join(HERE, "cut_588_evals.jsonl")
        done = set()
        if os.path.exists(out_path):
            for l in open(out_path):
                x = json.loads(l)
                done.add((x["circle"], x["tag"]))
        order = [t for t in task_list(kfs) if (t[0]["name"], t[2]) not in done]
        print(f"{len(kfs)} cuts, {len(order)} replica runs to do on {workers} workers", flush=True)
        t0 = time.time()
        with cf.ProcessPoolExecutor(max_workers=workers) as ex, open(out_path, "a") as fo, open(ev_path, "a") as fe:
            futs = [ex.submit(work, t) for t in order]
            for n, fu in enumerate(cf.as_completed(futs), 1):
                rec, evals = fu.result()
                fo.write(json.dumps(rec) + "\n")
                fo.flush()
                for e in evals:
                    fe.write(json.dumps(e) + "\n")
                fe.flush()
                print(f"  {n}/{len(order)} {rec['circle']} rep {rec['tag']} done, {rec['n_evals']} determinants, {time.time() - t0:.0f} s", flush=True)
        print(f"all done in {time.time() - t0:.0f} s", flush=True)
        sys.exit(0)
    print(__doc__)

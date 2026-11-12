#!/usr/bin/env python3
"""Ulp replicas of the twelve R 0.06 circles of #573, #574 and #585 (#588): the same circle() call as the real runs (hp/modecount_circle.py, n0 20, tol pi/4), with every argument
lam it asks det M at moved by 1 to 3 ulp in Re and in Im, signs and sizes drawn per (circle, replica, lam). Replica 0 is the control: no move, freshly evaluated, and its zero must equal
the stored one bit for bit. Replicas 1..10 are the shifted ones. Each distinct argument costs one determinant (the base 20 points, the 2 beta points c +- 2R and the bisection points).
usage: python replicas_588.py run [--workers 9]    writes replicas_588.jsonl (one record per replica) and replicas_588_evals.jsonl (one per determinant); resumes
       python replicas_588.py --selftest           the shift function (1 to 3 ulp, deterministic, replica 0 unmoved) and a synthetic circle: the replica spread of a det with known noise
                                                   is recovered within 30 percent, and noise-free replicas of a smooth det give 1e-12
Run with venv-t126's python (modecount_cx); the workers import hp/ from D:/choptuik-i573/hp, one thread per process, a state per kf made on first use."""
import concurrent.futures as cf, glob, json, math, os, random, sys, time

HP = "D:/choptuik-i573/hp"
RAW = "D:/choptuik-large-d-raw"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HP)
N0, TOL = 20, math.pi / 4
NREP = 10
STATES = {}


def circles():
    out = []
    for pat in ("I573-win2/k*_z_*", "I574-win2/k27_z_*", "I585-win2/k27_z_*"):
        for d in sorted(glob.glob(os.path.join(RAW, pat))):
            if os.path.isdir(d):
                r = [json.loads(l) for l in open(os.path.join(d, "res.jsonl"))][-1]
                out.append(dict(name=os.path.basename(d), task=os.path.basename(os.path.dirname(d)), kf=r["kfreeze"], centre=r["center"], R=r["R"], zero=r["zeros"][0], est=r["zeros_est"][0]))
    return out


def shift_arg(circle, rep, x, y):
    """(x, y) moved by 1 to 3 ulp in each of Re and Im, sign and size drawn from (circle, rep, x, y); rep 0 is unmoved"""
    if rep == 0:
        return x, y
    g = random.Random(f"{circle}|{rep}|{x!r}|{y!r}")
    out = []
    for v in (x, y):
        k = g.choice([-3, -2, -1, 1, 2, 3])
        for _ in range(abs(k)):
            v = math.nextafter(v, math.inf if k > 0 else -math.inf)
        out.append(v)
    return out[0], out[1]


def real_det(kf):
    if kf not in STATES:
        os.chdir(HP)
        os.environ["OMP_NUM_THREADS"] = "1"
        from modecount_common import setup
        STATES[kf] = setup("data/seeds/local/up23_D61.0264.npz", M=48, threads=1, kf=kf, fmax=1e-15, centre_tol=None)
    st = STATES[kf]

    def f(x, y):
        la, arg, _, _ = st.det(x, y)
        return la, arg
    return f


def run_replica(circle, rep, det_xy):
    """circle() on the shifted arguments; returns (record, evals)"""
    import modecount_circle as C
    c = complex(*circle["centre"])
    evals, memo = [], {}

    def det(lam):
        key = (float(lam.real), float(lam.imag))
        if key not in memo:
            sx, sy = shift_arg(circle["name"], rep, key[0], key[1])
            t = time.time()
            la, arg = det_xy(sx, sy)
            memo[key] = (la, arg)
            evals.append(dict(circle=circle["name"], rep=rep, re=key[0], im=key[1], sre=sx, sim=sy, lnabs=la, arg=arg, sec=round(time.time() - t, 2)))
        return memo[key]
    rec = C.circle(det, c, circle["R"], TOL, N0)
    return rec, evals


def work(task):
    circle, rep = task
    rec, evals = run_replica(circle, rep, real_det(circle["kf"]))
    out = dict(circle=circle["name"], rep=rep, kf=circle["kf"], winding=rec["winding"], resolved=rec["resolved"], points=rec["points"], n_evals=len(evals),
               zero=rec["zeros"][0] if rec.get("zeros") else None, est=rec["zeros_est"][0] if rec.get("zeros") else None, worker=os.getpid())
    return out, evals


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        import modecount_circle as C
        ok = True
        # the shift function
        base = (2.396619, 0.547672)
        d1 = [shift_arg("t", 1, *base) for _ in range(2)]
        good = d1[0] == d1[1] and shift_arg("t", 0, *base) == base
        ulps = [abs(round((a - b) / math.ulp(b))) for a, b in zip(shift_arg("t", 1, *base), base)]
        good &= all(1 <= u <= 3 for u in ulps)
        print("shift: deterministic, rep 0 unmoved, 1 to 3 ulp moved (got %s):" % ulps, "ok" if good else "FAIL")
        ok &= good
        # a synthetic circle: det = (lam - z) exp(a (lam - c)) with an added noise of sigma that depends on the exact argument bits (a hash), i.e. the evaluation's own ulp noise
        c, z, a = complex(1.902797, 0.916032), complex(1.903548, 0.910715), complex(40.0, 10.0)
        circ = dict(name="synthetic", kf=0, centre=[c.real, c.imag], R=0.06)

        def mk(sigma):
            def det_xy(x, y):
                lam = complex(x, y)
                v = (lam - z) * complex(math.exp((a * (lam - c)).real), 0) * complex(math.cos((a * (lam - c)).imag), math.sin((a * (lam - c)).imag))
                g = random.Random(f"{x!r}|{y!r}")
                return math.log(abs(v)) + g.gauss(0, sigma), math.atan2(v.imag, v.real) + g.gauss(0, sigma)
            return det_xy
        zs = [complex(*run_replica(circ, r, mk(1e-3))[0]["zeros"][0]) for r in range(1, 41)]
        m = sum(zs) / len(zs)
        s = math.sqrt(sum(abs(q - m) ** 2 for q in zs) / (len(zs) - 1))
        pred = 0.06 * math.sqrt(2 * (1e-3) ** 2) / math.sqrt(N0)  # R |eps|rms / sqrt(n): the noise of the first power sum
        good = 0.7 * pred < s < 1.5 * pred
        print(f"synthetic noise sigma 1e-3: replica spread {s:.2e} against R sqrt(2) sigma / sqrt(n0) = {pred:.2e} (the beta points add a little):", "ok" if good else "FAIL")
        ok &= good
        zs0 = [complex(*run_replica(circ, r, mk(0.0))[0]["zeros"][0]) for r in range(1, 6)]
        m0 = sum(zs0) / len(zs0)
        s0 = math.sqrt(sum(abs(q - m0) ** 2 for q in zs0) / (len(zs0) - 1))
        good = s0 < 1e-9
        print(f"noise-free det, shifted replicas: spread {s0:.2e} (must be below 1e-9; the ulp moves change the zero by about the derivative times 1e-16):", "ok" if good else "FAIL")
        ok &= good
        sys.exit(0 if ok else 1)
    if sys.argv[1:2] == ["run"]:
        workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 9
        circs = circles()
        out_path, ev_path = os.path.join(HERE, "replicas_588.jsonl"), os.path.join(HERE, "replicas_588_evals.jsonl")
        done = set()
        if os.path.exists(out_path):
            for l in open(out_path):
                r = json.loads(l)
                done.add((r["circle"], r["rep"]))
        tasks = [(c, r) for r in [0] + list(range(1, NREP + 1)) for c in circs if (c["name"], r) not in done]
        order = [t for t in tasks if t[1] == 0] + random.Random(588).sample([t for t in tasks if t[1] > 0], len([t for t in tasks if t[1] > 0]))
        print(f"{len(circs)} circles, {len(order)} replica runs to do on {workers} workers", flush=True)
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
                print(f"  {n}/{len(order)} {rec['circle']} rep {rec['rep']} done, {rec['n_evals']} determinants, {time.time() - t0:.0f} s", flush=True)
        print(f"all done in {time.time() - t0:.0f} s", flush=True)
        sys.exit(0)
    print(__doc__)

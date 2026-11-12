#!/usr/bin/env python3
"""Exploratory add-on of #585 (predictions_585_addon.json, committed before this run): the ulp noise of det M at the base points of the two kf 27 R 0.06 circles.
Six points: t = i/20, i = 0, 7, 14 of circle A (centre 1.902797+0.916032i) and circle B (centre 2.396619+0.547672i), R 0.06, as circle() computes them. At each: the reference
and 15 Re moves (j ulp, j = 1..15, repeated nextafter toward +inf). Same worker code as noise_585.py (state kf 27, one thread per process).
usage: python circle_noise_585.py run [--workers 2]     writes circle_evals_585.jsonl (resume)
       python circle_noise_585.py analyze                std of ln|det| and arg per point, the pooled sigma_circle, E1, E2 and the control (reference vs the circle's cached value)
       python circle_noise_585.py --selftest             the std/pooling code on synthetic values of known sigma (within 15 percent)
Run with venv-t126's python."""
import concurrent.futures as cf, glob, json, math, os, random, statistics as st, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
CIRCLES = {"A": ("circles/k27_z_re1.9028_im+0.9160", 1.902797, 0.916032), "B": ("k27_z_re2.3966_im+0.5477", 2.396619, 0.547672)}
IDX = (0, 7, 14)
R, N0, NJ = 0.06, 20, 15


def points():
    out = []
    for name, (_, cr, ci) in CIRCLES.items():
        c = complex(cr, ci)
        for i in IDX:
            lam = c + R * complex(math.cos(2 * math.pi * i / N0), math.sin(2 * math.pi * i / N0))
            out.append((f"{name}{i}", float(lam.real), float(lam.imag)))
    return out


def tasks():
    t = []
    for pid, x, y in points():
        t.append((pid, "ref", 0, x, y))
        xr = x
        for j in range(1, NJ + 1):
            xr = math.nextafter(xr, math.inf)
            t.append((pid, "re", j, xr, y))
    return t


def wrap(x):
    return math.remainder(x, 2 * math.pi)


def stds(recs):
    out = {}
    for pid in sorted({r["id"] for r in recs}):
        R_ = [r for r in recs if r["id"] == pid]
        ref = [r for r in R_ if r["kind"] == "ref"][0]
        vals = [ref] + [r for r in R_ if r["kind"] == "re"]
        out[pid] = (st.stdev([v["lnabs"] for v in vals]), st.stdev([wrap(v["arg"] - ref["arg"]) for v in vals]), len(vals))
    return out


def pooled(d, key):
    return math.sqrt(st.mean(v[key] ** 2 for v in d.values()))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        rng = random.Random(3)
        recs = []
        for pid, x, y in points():
            recs.append(dict(id=pid, kind="ref", lnabs=1.0, arg=0.5))
            for j in range(NJ):
                recs.append(dict(id=pid, kind="re", lnabs=1.0 + rng.gauss(0, 5e-4), arg=0.5 + rng.gauss(0, 5e-4)))
        d = stds(recs)
        g = (pooled(d, 0), pooled(d, 1))
        ok = all(abs(x / 5e-4 - 1) < 0.15 for x in g)
        print("known sigma 5e-4, pooled std ln, arg:", " ".join(f"{x:.2e}" for x in g), "ok" if ok else "FAIL")
        sys.exit(0 if ok else 1)
    out_path = os.path.join(HERE, "circle_evals_585.jsonl")
    if sys.argv[1:2] == ["run"]:
        import noise_585 as N
        workers = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 2
        done = set()
        if os.path.exists(out_path):
            for l in open(out_path):
                r = json.loads(l)
                done.add((r["id"], r["kind"], r["j"], r["re"], r["im"]))
        todo = [t for t in tasks() if t not in done]
        print(f"{len(todo)} evaluations on {workers} workers", flush=True)
        t0 = time.time()
        with cf.ProcessPoolExecutor(max_workers=workers, initializer=N.init) as ex, open(out_path, "a") as f:
            for n, fu in enumerate(cf.as_completed([ex.submit(N.work, t) for t in todo]), 1):
                f.write(json.dumps(fu.result()) + "\n")
                f.flush()
                if n % 10 == 0:
                    print(f"  {n} done, {time.time() - t0:.0f} s", flush=True)
        print(f"all done in {time.time() - t0:.0f} s")
        sys.exit(0)
    if sys.argv[1:2] == ["analyze"]:
        recs = [json.loads(l) for l in open(out_path)]
        d = stds(recs)
        # control: each reference equals the circle's own cached value bit for bit
        cached = {}
        for name, (folder, _, _) in CIRCLES.items():
            for l in open(glob.glob(os.path.join(HERE, folder, "modecount_*_evals.jsonl"))[0]):
                r = json.loads(l)
                cached[(r["re"], r["im"])] = (r["lnabs"], r["arg"])
        print("| point | re | im | values | std ln\\|det\\| | std arg | reference equals the circle's cached value |\n|---|---|---|---|---|---|---|")
        allsame = True
        for pid, x, y in points():
            ref = [r for r in recs if r["id"] == pid and r["kind"] == "ref"][0]
            same = cached.get((x, y)) == (ref["lnabs"], ref["arg"])
            allsame &= same
            print(f"| {pid} | {x:.6f} | {y:.6f} | {d[pid][2]} | {d[pid][0]:.2e} | {d[pid][1]:.2e} | {'yes' if same else 'NO'} |")
        s_ln, s_arg = pooled(d, 0), pooled(d, 1)
        print(f"\nsigma_circle (pooled rms): ln|det| {s_ln:.3e}, arg {s_arg:.3e}; control: all six references bit equal to the cached values: {allsame}")
        e1 = 2.7e-4 <= s_ln <= 3.3e-3 and s_ln <= 3.3e-3 / 2
        errs = [json.load(open(p))["err0"] for p in sorted(glob.glob(os.path.join(HERE, "planted_585_[AB]_*.json")))]
        m = st.mean(errs)
        ref_val = 0.045 * s_ln
        e2 = ref_val / 3 <= m <= 3 * ref_val
        print(f"E1 (between 2.7e-4 and 3.3e-3 and at least 2x below the near points): {'holds' if e1 else 'FAILS'}")
        print(f"E2 (mean noise-free error {m:.2e} within a factor 3 of 0.045 x sigma_circle = {ref_val:.2e}): {'holds' if e2 else 'FAILS'}")
        sys.exit(0 if (e1 and e2 and allsame) else 1)
    print(__doc__)

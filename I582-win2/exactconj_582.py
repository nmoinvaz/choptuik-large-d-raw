#!/usr/bin/env python3
"""Exact conjugate symmetry of det M at kf 27: det M(conj lam) = conj det M(lam), tested at the EXACT conjugate argument (same Re bits, Im negated).
sym_582.py compares the circles' cached points instead, which are conjugates only to one ulp in Re (cos(2 pi s) rounds differently), and the evaluation is noise-limited
at about 1e-3 in ln|det| and arg for a one-ulp change of the argument (conj_diag in the README), so that comparison fails its pre-stated 1e-6 bound. This script
takes the NPTS lower points of the #582 and #574 caches with the largest cached asymmetry, evaluates det at their exact conjugates (6 worker processes, one thread
each) and compares with the cached lower value.
usage: python exactconj_582.py [--npts 6]            pass: |d ln|det|| < 1e-9 and |arg sum| < 1e-9 (mod 2 pi) at every point
       python exactconj_582.py --mutate=ulp          control: Re of the conjugate shifted by one ulp, the check must fail (exit 1)
Writes exactconj_582[_ulp].jsonl next to this script. Run from any directory; the worker imports hp/ from D:/choptuik-i573/hp (venv-t126)."""
import concurrent.futures as cf, glob, json, math, os, sys

HP = "D:/choptuik-i573/hp"
RAW = "D:/choptuik-large-d-raw"
HERE = os.path.dirname(os.path.abspath(__file__))
ST = None


def init():
    global ST
    os.chdir(HP)
    sys.path.insert(0, HP)
    from modecount_common import setup
    ST = setup("data/seeds/local/up23_D61.0264.npz", M=48, threads=1, kf=27, fmax=1e-15, centre_tol=None)


def work(pt):
    re_, im = pt
    la, arg, pmin, pmax = ST.det(re_, im)
    return la, arg


def load(f):
    return [json.loads(l) for l in open(glob.glob(f"{RAW}/{f}/modecount_*_evals.jsonl")[0])]


def pick(npts):
    pairs = [(f"I582-win2/k27_re{r:.2f}_im-{i:.2f}", f"I574-win2/k27_re{r:.2f}_im+{i:.2f}") for r, i in [(2.85, 1.25), (3.85, 1.25), (4.35, 1.25)] + [(r, 1.75) for r in (1.85, 2.35, 2.85, 3.35, 3.85, 4.35)]]
    cand = {}
    for lo, up in pairs:
        U = {(round(r["re"], 9), round(r["im"], 9)): r for r in load(up)}
        for r in load(lo):
            u = U.get((round(r["re"], 9), round(-r["im"], 9)))
            if u:
                cand[(r["re"], r["im"])] = (abs(r["lnabs"] - u["lnabs"]), r)
    return [v[1] for v in sorted(cand.values(), key=lambda x: -x[0])[:npts]]


if __name__ == "__main__":
    os.environ["OMP_NUM_THREADS"] = "1"
    npts = int(sys.argv[sys.argv.index("--npts") + 1]) if "--npts" in sys.argv else 6
    mut = "--mutate=ulp" in sys.argv
    pts = pick(npts)
    args = [(r["re"] + (math.ulp(r["re"]) if mut else 0.0), -r["im"]) for r in pts]
    with cf.ProcessPoolExecutor(max_workers=npts, initializer=init) as ex:
        out = list(ex.map(work, args))
    ok = True
    rows = []
    for r, (la, arg) in zip(pts, out):
        d = abs(r["lnabs"] - la)
        a = abs(math.remainder(r["arg"] + arg, 2 * math.pi))
        good = d < 1e-9 and a < 1e-9
        ok &= good
        rows.append(dict(re=r["re"], im=r["im"], lnabs_lower=r["lnabs"], arg_lower=r["arg"], lnabs_conj=la, arg_conj=arg, dln=d, argsum=a, ok=good))
        print(f"({r['re']:.6f}, {r['im']:+.6f}) cached asymmetry-pick: |d ln|det|| {d:.2e}  |arg sum| {a:.2e}  {'ok' if good else 'FAIL'}")
    with open(os.path.join(HERE, "exactconj_582_ulp.jsonl" if mut else "exactconj_582.jsonl"), "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
    print("all points ok" if ok else "FAIL")
    sys.exit(0 if ok else 1)

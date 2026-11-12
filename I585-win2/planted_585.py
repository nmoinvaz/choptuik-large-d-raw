#!/usr/bin/env python3
"""A zero planted on the cached determinants of a kf 27 R 0.06 circle, recovered by circle() of hp/modecount_circle.py with and without noise (#585, criteria P6, P7).
For each of the two circles (A: #574's at 1.902797+0.916032i, B: the new one at 2.396619+0.547672i) and phi = 0, 90, 180, 270 degrees: lam0 = centre + 0.025 e^{i phi};
the planted determinant is det(lam) (lam - lam0), i.e. (ln|det| + ln|lam - lam0|, arg det + arg(lam - lam0)), W = 2, n0 = 20, tol pi/4, the same call as the real runs.
Points the bisections need that the cache lacks are computed with the same state (hp setup, kf 27, threads 1) and kept in extra_<case>.jsonl.
Noise: Gaussian, independent on ln|det| and arg, per distinct lam and realization (seeded by the case, the realization and the argument), sigma from sigma_585.json (pooled near
points, key near_ln and near_arg) unless --sigma_ln/--sigma_arg are given; 200 realizations per case.
usage: python planted_585.py --all [--nreal 200] [--workers 8]   runs the cases whose circle exists, writes planted_585_<A|B>_<phi>.json
       python planted_585.py --summary                            table and verdicts P6, P7 from those files (exit 1 if one fails)
       --tag _x --sigma_ln S --sigma_arg S                         exploratory runs at another sigma, files planted_585_x_<A|B>_<phi>.json (not registered; --summary --tag _x)
       python planted_585.py --selftest                           synthetic det with two zeros: both recovered to 1e-9 for the four phi; the noise wrapper with sigma 0 changes nothing;
                                                                  --mutate=sign (arg sign flipped) must fail it, a cached value moved by 0.5 (the synthetic's 'cache' control) must fail the replay check
Run with venv-t126's python. Error bar kinds: 'own estimate' is the circle's n0/2 against n0 power sums (zeros_est), not a bound; the rms is over noise realizations."""
import concurrent.futures as cf, glob, json, math, os, random, statistics as st, sys, time

HP = "D:/choptuik-i573/hp"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HP)
CIRCLES = {"A": "circles/k27_z_re1.9028_im+0.9160", "B": "k27_z_re2.3966_im+0.5477"}
PHIS = [0, 90, 180, 270]
OFFSET, N0, TOL = 0.025, 20, math.pi / 4
ST = None


def wrap(x):
    return math.remainder(x, 2 * math.pi)


def load_circle(name):
    d = os.path.join(HERE, CIRCLES[name])
    rec = [json.loads(l) for l in open(os.path.join(d, "res.jsonl"))][-1]
    cache = {}
    for l in open(glob.glob(os.path.join(d, "modecount_*_evals.jsonl"))[0]):
        r = json.loads(l)
        cache[(r["re"], r["im"])] = (r["lnabs"], r["arg"])
    return rec, cache


def real_det(key):
    global ST
    if ST is None:
        os.chdir(HP)
        os.environ["OMP_NUM_THREADS"] = "1"
        from modecount_common import setup
        ST = setup("data/seeds/local/up23_D61.0264.npz", M=48, threads=1, kf=27, fmax=1e-15, centre_tol=None)
    la, arg, _, _ = ST.det(key[0], key[1])
    return la, arg


def make_det(cache, fallback, lam0, noise=None, counters=None, extra=None):
    memo = {}

    def det(lam):
        key = (float(lam.real), float(lam.imag))
        if key in memo:
            return memo[key]
        if key not in cache:
            counters["fallback"] += 1
            if counters["fallback"] > counters["cap"]:
                raise RuntimeError("more than 80 uncached points")
            cache[key] = fallback(key)
            if extra is not None:
                extra.write(json.dumps(dict(re=key[0], im=key[1], lnabs=cache[key][0], arg=cache[key][1])) + "\n")
                extra.flush()
        la, arg = cache[key]
        if lam0 is not None:
            f = lam - lam0
            la, arg = la + math.log(abs(f)), wrap(arg + math.atan2(f.imag, f.real))
        if noise is not None:
            n1, n2 = noise(key)
            la, arg = la + n1, wrap(arg + n2)
        memo[key] = (la, arg)
        return memo[key]
    return det


def noise_fn(case, r, s_ln, s_arg):
    def f(key):
        g = random.Random(f"{case}|{r}|{key[0]!r}|{key[1]!r}")
        return g.gauss(0, s_ln), g.gauss(0, s_arg)
    return f


def matched(rec, lam0):
    z = [complex(*p) for p in rec["zeros"]]
    i = min(range(len(z)), key=lambda k: abs(z[k] - lam0))
    return z, i, rec["zeros_est"][i]


def run_case(name, phi, nreal, s_ln, s_arg, fallback=real_det, circle_data=None, mutate=None):
    import modecount_circle as C
    rec0, cache = circle_data or load_circle(name)
    if circle_data is None:  # real determinants computed by earlier runs of this circle's cases (they do not depend on phi or on the noise)
        for fn in glob.glob(os.path.join(HERE, f"extra_{name}_*.jsonl")):
            for l in open(fn):
                r = json.loads(l)
                cache.setdefault((r["re"], r["im"]), (r["lnabs"], r["arg"]))
    c, R = complex(*rec0["center"]), rec0["R"]
    case = f"{name}_{phi}"
    cnt = dict(fallback=0, cap=80 if circle_data is None else 10 ** 6)
    extra = open(os.path.join(HERE, f"extra_{case}.jsonl"), "a") if circle_data is None else None
    # the unplanted replay must reproduce the stored circle
    rep = C.circle(make_det(cache, fallback, None, None, cnt, extra), c, R, TOL, N0)
    replay_diff = max(abs(complex(*a) - complex(*b)) for a, b in zip(rep["zeros"], rec0["zeros"])) if rep["zeros"] and len(rep["zeros"]) == len(rec0["zeros"]) else math.inf
    lam0 = c + OFFSET * complex(math.cos(math.radians(phi)), math.sin(math.radians(phi)))
    sg = -1.0 if mutate == "sign" else 1.0
    base_det = make_det(cache, fallback, lam0, None, cnt, extra)
    det0 = (lambda lam: (lambda v: (v[0], sg * v[1]))(base_det(lam)))
    p0 = C.circle(det0, c, R, TOL, N0)
    out = dict(case=case, circle=name, phi=phi, centre=[c.real, c.imag], R=R, lam0=[lam0.real, lam0.imag], replay_diff=replay_diff, winding0=p0["winding"], resolved0=p0["resolved"],
               fallback_after_noise_free=cnt["fallback"], sigma_ln=s_ln, sigma_arg=s_arg, nreal=nreal)
    if round(p0["winding"]) != 2 or "zeros" not in p0:
        out.update(ok_noise_free=False)
        return out
    z, i, est = matched(p0, lam0)
    other = 1 - i
    out.update(rec0=[z[i].real, z[i].imag], est0=est, err0=abs(z[i] - lam0), within0=abs(z[i] - lam0) <= est,
               other_move=abs(z[other] - complex(*rec0["zeros"][0])), other_est=p0["zeros_est"][other])
    # a noise wrapper of sigma 0 must change nothing
    p_s0 = C.circle(make_det(cache, fallback, lam0, noise_fn(case, -1, 0.0, 0.0), cnt, extra), c, R, TOL, N0)
    out["sigma0_identical"] = p_s0["zeros"] == p0["zeros"]
    errs, moves, bad, capped = [], [], 0, False
    for r in range(nreal):
        try:
            pr = C.circle(make_det(cache, fallback, lam0, noise_fn(case, r, s_ln, s_arg), cnt, extra), c, R, TOL, N0)
        except RuntimeError:
            capped = True
            break
        if round(pr["winding"]) != 2 or "zeros" not in pr or not pr["resolved"]:
            bad += 1
            continue
        zr, ir, _ = matched(pr, lam0)
        errs.append(abs(zr[ir] - lam0))
        moves.append(abs(zr[ir] - z[i]))
    out.update(fallback_total=cnt["fallback"], bad_realizations=bad, n_used=len(errs), capped=capped, realizations_run=r + 1 if nreal else 0)
    if errs:
        rms = math.sqrt(st.mean(e * e for e in errs))
        out.update(rms_err=rms, rms_move=math.sqrt(st.mean(m * m for m in moves)), median_err=st.median(errs), max_err=max(errs), frac_over_est=sum(e > est for e in errs) / len(errs),
                   rms_over_est=rms / est)
    return out


def case_main(args):
    name, phi, nreal, s_ln, s_arg, tag = args
    res = run_case(name, phi, nreal, s_ln, s_arg)
    with open(os.path.join(HERE, f"planted_585{tag}_{name}_{phi}.json"), "w") as f:
        json.dump(res, f, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    return res


def summary(tag=""):
    rows = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(HERE, f"planted_585{tag}_[AB]_*.json")))]
    print("| case | lam0 | replay equals stored | W | recovered lam0, error | own estimate | within (P6) | sigma 0 identical | rms error, noise | rms / estimate | rms move | frac over estimate | extra points | bad realizations |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    p6, p7 = [], []
    for r in rows:
        if "err0" not in r:
            print(f"| {r['case']} | | {r['replay_diff']:.1e} | {r['winding0']:.3f} | FAILED to plant | | | | | | | | | |")
            p6.append(False)
            p7.append(False)
            continue
        p6.append(bool(r["within0"]))
        ok7 = "rms_over_est" in r and 0.3 <= r["rms_over_est"] <= 3
        p7.append(ok7)
        print(f"| {r['case']} | {r['lam0'][0]:.5f}{r['lam0'][1]:+.5f}i | {r['replay_diff']:.1e} | 2 | {r['rec0'][0]:.7f}{r['rec0'][1]:+.7f}i, {r['err0']:.2e} | {r['est0']:.2e} | {'yes' if r['within0'] else 'NO'} | {r['sigma0_identical']} | "
              f"{r.get('rms_err', float('nan')):.2e} | {r.get('rms_over_est', float('nan')):.2f} | {r.get('rms_move', float('nan')):.2e} | {r.get('frac_over_est', float('nan')):.2f} | {r.get('fallback_total', 0)} | {r.get('bad_realizations', 0)} |")
    n = len(rows)
    print(f"\ncases {n}; P6 (within own estimate noise-free, all 8): {'holds' if n == 8 and all(p6) else 'FAILS'} ({sum(p6)} of {n}); "
          f"P7 (rms between 0.3 and 3 times the estimate, at least 6 of 8): {'holds' if n == 8 and sum(p7) >= 6 else 'FAILS'} ({sum(p7)} of {n})")
    return 0 if n == 8 and all(p6) and sum(p7) >= 6 else 1


def selftest():
    import modecount_circle as C
    c = complex(1.902797, 0.916032)
    z1 = c + complex(0.00075, -0.00532)
    a = complex(40.0, 10.0)
    ok = True
    for mutate in (None, "sign", "cache"):
        good = True
        for phi in PHIS:
            lam0 = c + OFFSET * complex(math.cos(math.radians(phi)), math.sin(math.radians(phi)))

            def f(lam):
                v = (lam - z1) * (lam - lam0) * complex(math.exp((a * (lam - c)).real), 0) * complex(math.cos((a * (lam - c)).imag), math.sin((a * (lam - c)).imag))
                return math.log(abs(v)), math.atan2(v.imag, v.real)
            cache = {}
            # the synthetic plays the cached circle: its 'cache' is filled on demand by the same function, a replay of the unplanted det (without the lam0 factor)
            def f0(lam):
                v = (lam - z1) * complex(math.exp((a * (lam - c)).real), 0) * complex(math.cos((a * (lam - c)).imag), math.sin((a * (lam - c)).imag))
                return math.log(abs(v)), math.atan2(v.imag, v.real)
            rec0 = C.circle(f0, c, 0.06, TOL, N0)
            rec0 = dict(center=[c.real, c.imag], R=0.06, zeros=rec0["zeros"], zeros_est=rec0["zeros_est"])
            fb = lambda key: f0(complex(*key))
            if mutate == "cache":
                # a cached value moved by 0.5: the replay of the unplanted circle must stop reproducing the stored one
                cache[(c.real + 0.06, c.imag)] = (f0(complex(c.real + 0.06, c.imag))[0] + 0.5, 0.0)
            res = run_case("S", phi, 3, 1e-3, 1e-3, fallback=fb, circle_data=(rec0, cache), mutate=mutate if mutate == "sign" else None)
            if "err0" not in res:
                good = False
                continue
            zs = sorted([complex(*p) for p in C.circle(f, c, 0.06, TOL, N0)["zeros"]], key=lambda q: (q.real, q.imag))
            tr = sorted([z1, lam0], key=lambda q: (q.real, q.imag))
            err = max(abs(p - q) for p, q in zip(zs, tr))
            good &= err < 1e-9 and res["err0"] < 1e-9 and res["sigma0_identical"] and res["replay_diff"] < 1e-12
        label = {None: "planted synthetic (two zeros, four phi): both recovered to 1e-9, replay equal, sigma 0 identical", "sign": "--mutate=sign (arg flipped): must fail", "cache": "--mutate=cache (cached value moved): must fail"}[mutate]
        verdict = good if mutate is None else not good
        print(f"{label}: {'ok' if verdict else 'FAIL'}")
        ok &= verdict
    return 0 if ok else 1


if __name__ == "__main__":
    def opt(flag, default):
        return type(default)(sys.argv[sys.argv.index(flag) + 1]) if flag in sys.argv else default
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--summary" in sys.argv:
        sys.exit(summary(opt("--tag", "")))
    if "--all" in sys.argv:
        sig = json.load(open(os.path.join(HERE, "sigma_585.json")))
        s_ln, s_arg = opt("--sigma_ln", sig["near_ln"]), opt("--sigma_arg", sig["near_arg"])
        nreal = opt("--nreal", 200)
        tag = opt("--tag", "")
        cases = [(n, p, nreal, s_ln, s_arg, tag) for n in CIRCLES for p in PHIS if os.path.exists(os.path.join(HERE, CIRCLES[n], "res.jsonl")) and not os.path.exists(os.path.join(HERE, f"planted_585{tag}_{n}_{p}.json"))]
        print(f"{len(cases)} cases, sigma_ln {s_ln:.3e} sigma_arg {s_arg:.3e}, {nreal} realizations", flush=True)
        with cf.ProcessPoolExecutor(max_workers=opt("--workers", 8)) as ex:
            for r in ex.map(case_main, cases):
                print(r["case"], "within0" if r.get("within0") else "not within0", "rms/est", r.get("rms_over_est"), "extra", r.get("fallback_total"), flush=True)
        sys.exit(0)
    print(__doc__)

"""#1098 D 4628: the double-double residual (no Newton) of form_s.py jump's guess, per block, for several fit states,
degrees, Moebius a and ks; the guess formed exactly as cmd_jump forms it (scale_s, polyfit in 1/n, unscale_s, a plan at
the target D from s_to_a). A state alone at its own D with its own segs is the baseline.

    python3 jump_guess_resid.py HP_DIR THREADS CASE [CASE ...]
    CASE = D:deg:a:ks:STATE[+STATE...]   (D "own": the single state's D, segs and D_str; ks "own": the state's ks)
"""
import sys
import time

hp_dir, threads = sys.argv[1], int(sys.argv[2])
sys.path.insert(0, hp_dir)
import mpmath as mp  # noqa: E402
import numpy as np  # noqa: E402

import form_s  # noqa: E402
from form_s import blocks_s, groups_s, make_solver, make_solver_s, s_to_a, scale_s, unscale_s  # noqa: E402
from octo_corrector import load_o, o8  # noqa: E402

cache = {}


def state(p):
    if p not in cache:
        cache[p] = load_o(p)
    return cache[p]


def horizon_split(F, M, K):
    v = np.asarray(F[0]) + np.asarray(F[1])
    b = K * 3 * M
    return [float(np.abs(v[b + f * M:b + (f + 1) * M]).max()) for f in range(3)]


plans = {}
for case in sys.argv[3:]:
    Ds, deg, a, ks, paths = case.split(":")
    paths = paths.split("+")
    rows = sorted([(state(p)[1]["D"], state(p)[0], state(p)[1]) for p in paths], key=lambda r: r[0])
    m0 = rows[-1][2]
    M, nodes = int(m0["M"]), list(m0["nodes"])
    K = len(nodes)
    for r in rows:
        if list(r[2]["nodes"]) != nodes:
            print(f"  note: {r[0]:g}'s nodes {r[2]['nodes']} differ from {nodes}", flush=True)
    ks = int(m0["ks"]) if ks == "own" else int(ks)
    a = float(a)
    t0 = time.time()
    if Ds == "own":
        assert len(rows) == 1
        with mp.workdps(60):
            Dt = mp.mpf(m0["D_str"])
        z8 = [np.ascontiguousarray(q) for q in rows[0][1]]
        segs = m0["segs"]
        how = f"the state itself at its D {float(Dt):g}, its segs"
    else:
        with mp.workdps(60):
            Dt = mp.mpf(Ds)
        Dv = np.array([r[0] for r in rows])
        Y = np.array([scale_s(sum(np.asarray(p) for p in r[1][:2]), r[0], M, K) for r in rows])
        t = 1.0 / (Dv - 2.0)
        tt = 1.0 / (float(Dt) - 2.0)
        c = np.polyfit(t, Y, int(deg))
        y = np.array([np.polyval(c[:, j], tt) for j in range(Y.shape[1])])
        zS = unscale_s(y, float(Dt), M, K)
        key = (Ds, deg, tuple(paths))
        if key not in plans:
            zA = s_to_a(zS, float(Dt), M, K, nodes)
            kw = dict(kt=int(m0.get("kt", 36)), kc=int(m0["kc"]), ks=ks, threads=threads, kfreeze=13)
            sa = make_solver(Dt, M, nodes=nodes, **kw)
            plans[key] = [list(map(float, g)) for g in sa.plan(np.ascontiguousarray(zA), np.zeros(len(zA)), 1e-40, 0.05)]
        segs = plans[key]
        z8 = [np.ascontiguousarray(zS)] + [np.zeros(len(zS)) for _ in range(7)]
        how = f"deg {deg} fit to D {', '.join(format(r[0], 'g') for r in rows)}"
    s = make_solver_s(Dt, M, nodes, kt=int(m0.get("kt", 36)), kc=int(m0["kc"]), ks=ks, threads=threads, kfreeze=13,
                      segs=segs, mob=a)
    F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(2)])
    bl = blocks_s(F, M, K)
    hs = horizon_split(F, M, K)
    print(f"D {float(Dt):g}, {how}, a {a:g}, ks {ks}, {sum(len(g) - 1 for g in segs)} steps: dd max |F| per block "
          + " ".join(f"{b:.2e}" for b in bl) + f"; horizon rows p/m/c {hs[0]:.2e} {hs[1]:.2e} {hs[2]:.2e}"
          + f" ({time.time() - t0:.0f} s)", flush=True)

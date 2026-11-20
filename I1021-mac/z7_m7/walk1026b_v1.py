#!/usr/bin/env python3
"""walk1026b.py (walk1026.py with --r1bar, --stepbar, --posbar and --selftest [--mutate=noposbar], #1021 rerun) NAME A W B3 C3 [--xi1 0.2] [--procs 2] [--maxit 25] [--tr 0.02,0.03] [--bar 1e-6] [--out walks] [--logs logs]: the outer (A, w/w_inf) Newton of the M = 5 selection from complete fixed-(A, w) solves, the
route m7_outer.py's 'newton' mode took when hier's own level-1 Newton cannot be used (#1026). Why: started at a zero of the M = 3 problem, hier_nb.py 5's level-1 Newton stops at |r_1| = 121 without a step
(its nested level-3 re-solves fail at the trial points, logs/probe_*), while a fixed-(A, w) solve from the M = 3 harmonics converges at the M = 5 zero and half-way (|r_3| 1e-8). Each point is
`hier_nb.py 5 A w --x=B3,C3[,B5,C5] --fixA --schur --procs P --verbose=1 --xi1=XI` (cwd solver/inner_stokes of the worktree, the harmonics of the best earlier point as the start), a solve counts when |r_3| and |r_5|
< 1e-6. The Jacobian of (Re r_1, Im r_1) in (A, w) is a forward difference over the first three points (steps 2e-3 in A, 1e-3 in w), then Broyden's rule; every step is from the point of smallest |r_1|, cut to
a trust region |dA| <= TR0, |dw| <= TR1 and halved up to four times when the solve fails or |r_1| does not fall. Converged when the full Newton step from the best point is below 3e-6 in A and in w with
|r_1| of that point below 1e-2 (J is about 1e4, so that is a position error below 1e-6); the zero is then that point plus the step. B3, C3 are the level-3 start harmonics (-2 Im F_3, 2 Re F_3 of the M = 3 solve); B5, C5 start from the seed file at w_inf
(hier's default) until a solve gives them. Writes walks/walk_NAME_xiXI.json (every point, the verdict) and logs/fix_NAME_xiXI_N.log per solve."""
import json
import os
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.environ.get("W1026_WT", "/home/nathan/Source/cl-995")
PY = os.environ.get("W1026_PY", sys.executable)
BAR = 1e-6


def solve(A, w, x, xi, procs, tag, logdir):
    arg = [PY, "-u", "hier_nb.py", "5", f"{A:.12f}", f"{w:.12f}", "--x=" + ",".join(f"{v:.10f}" for v in x), "--fixA", "--schur", "--procs", str(procs), "--verbose=1", f"--xi1={xi}"]
    log = os.path.join(logdir, f"{tag}.log")
    with open(log, "w") as fh:
        fh.write("# " + " ".join(arg) + "\n")
        fh.flush()
        subprocess.run(["nice", "-n", "10"] + arg, cwd=os.path.join(WT, "solver", "inner_stokes"), stdout=fh, stderr=subprocess.STDOUT, timeout=3600)
    txt = open(log).read()
    m = re.findall(r"FIXED-A M (\d+): A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", txt)
    f3 = re.findall(r"F_3/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_3 ([0-9.]+e[+-]\d+)", txt)
    f5 = re.findall(r"F_5/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_5 ([0-9.]+e[+-]\d+)", txt)
    if not (m and f3 and f5):
        return dict(A=A, w=w, ok=False, why="no FIXED-A line", log=log)
    Af = float(m[-1][1])
    a3, b3, r3 = float(f3[-1][0]), float(f3[-1][1]), float(f3[-1][2])
    a5, b5, r5 = float(f5[-1][0]), float(f5[-1][1]), float(f5[-1][2])
    return dict(A=A, w=w, r1=[float(m[-1][3]), float(m[-1][4])], r3=r3, r5=r5, x=[a3 * Af, b3 * Af, a5 * Af, b5 * Af], F3=[a3, b3], F5=[a5, b5],
                ok=bool(r3 < BAR and r5 < BAR), why="" if r3 < BAR and r5 < BAR else f"|r_3| {r3:.1e} |r_5| {r5:.1e} not under {BAR:g}", log=log)


def conv_test(step, rb, acc, bars, mut=""):
    """#1021 rerun criteria (coordinator, #1048's closing comment): at one iteration, (1) |r_1| of the best point <= R1BAR,
    (2) the Newton step under STEPBAR in A and in w/w_inf, (3) with POSBAR, the last two accepted walk points within POSBAR in A
    and in w/w_inf (2 accepted points needed); --mutate=noposbar drops (3) (the selftest must then fail)"""
    r1bar, stepbar, posbar = bars
    ok = abs(step[0]) < stepbar and abs(step[1]) < stepbar and (r1bar is None or float(np.hypot(*rb)) <= r1bar)
    if posbar is not None and mut != "noposbar":
        ok = ok and len(acc) >= 2 and abs(acc[-1][0] - acc[-2][0]) <= posbar and abs(acc[-1][1] - acc[-2][1]) <= posbar
    return bool(ok)


def selftest(mut):
    b = (3.8e-2, 1e-5, 1e-5)
    got = [conv_test([2e-6, 1e-6], [0.02, 0.0], [(1.0, 1.0), (1.0 + 4e-6, 1.0)], b, mut),
           conv_test([2e-6, 1e-6], [0.05, 0.0], [(1.0, 1.0), (1.0 + 4e-6, 1.0)], b, mut),
           conv_test([2e-5, 1e-6], [0.02, 0.0], [(1.0, 1.0), (1.0 + 4e-6, 1.0)], b, mut),
           conv_test([2e-6, 1e-6], [0.02, 0.0], [(1.0, 1.0), (1.0 + 4e-5, 1.0)], b, mut),
           conv_test([2e-6, 1e-6], [0.02, 0.0], [(1.0, 1.0)], b, mut)]
    want = [True, False, False, False, False]
    print(f"selftest{' --mutate=' + mut if mut else ''}: {got} (expect {want}): {'PASS' if got == want else 'FAIL'}")
    return got == want


def main(argv):
    global BAR
    name, A0, w0 = argv[0], float(argv[1]), float(argv[2])
    x3 = [float(argv[3]), float(argv[4])]
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
    xi, procs, maxit = opt("--xi1", "0.2"), int(opt("--procs", "2")), int(opt("--maxit", "25"))
    BAR = float(opt("--bar", "1e-6"))      # |r_3|, |r_5| bar of a converged solve; the runs of the readings use the default 1e-6
    tr = [float(v) for v in opt("--tr", "0.02,0.03").split(",")]
    out = opt("--out", os.path.join(HERE, "walks"))
    r1bar = opt("--r1bar", '1e-2'); stepbar = float(opt("--stepbar", "3e-6")); posbar = opt("--posbar", None)
    bars = (None if r1bar is None else float(r1bar), stepbar, None if posbar is None else float(posbar))
    logdir = opt("--logs", os.path.join(HERE, "logs"))
    os.makedirs(out, exist_ok=True)
    pts, n = [], [0]
    path = os.path.join(out, f"walk_{name}_xi{xi}.json")

    def run(A, w, x):
        n[0] += 1
        p = solve(A, w, x, xi, procs, f"fix_{name}_xi{xi}_{n[0]:02d}", logdir)
        p["n"] = n[0]
        pts.append(p)
        r = p.get("r1")
        print(f"point {n[0]}: A {A:.9f} w {w:.9f}  " + (f"r_1 {r[0]:+.4e}{r[1]:+.4e}i |r_1| {np.hypot(*r):.3e} |r_3| {p['r3']:.1e} |r_5| {p['r5']:.1e} {'ok' if p['ok'] else 'NOT CONVERGED'}" if r else p["why"]), flush=True)
        json.dump(dict(name=name, xi1=xi, start=[A0, w0, *x3], points=pts, verdict=verdict[0]), open(path, "w"), indent=1)
        return p

    verdict = [dict(converged=False, why="not finished")]
    p0 = run(A0, w0, x3)
    if not p0["ok"]:
        verdict[0] = dict(converged=False, why="the start solve did not converge: " + p0["why"])
        json.dump(dict(name=name, xi1=xi, start=[A0, w0, *x3], points=pts, verdict=verdict[0]), open(path, "w"), indent=1)
        return 1
    z0 = np.array([A0, w0])
    ps = []
    for dz in ([2e-3, 0.0], [0.0, 1e-3]):
        q = run(A0 + dz[0], w0 + dz[1], p0["x"])
        if not q["ok"]:
            verdict[0] = dict(converged=False, why="a Jacobian-step solve did not converge: " + q["why"])
            json.dump(dict(name=name, xi1=xi, start=[A0, w0, *x3], points=pts, verdict=verdict[0]), open(path, "w"), indent=1)
            return 1
        ps.append(q)
    r0 = np.array(p0["r1"])
    J = np.column_stack([(np.array(ps[0]["r1"]) - r0) / 2e-3, (np.array(ps[1]["r1"]) - r0) / 1e-3])
    best = p0
    acc = [(p0["A"], p0["w"])]                          # accepted walk points, for (3)
    for it in range(maxit):
        zb, rb = np.array([best["A"], best["w"]]), np.array(best["r1"])
        step = -np.linalg.solve(J, rb)
        done = conv_test(step, rb, acc, bars)
        print(f"iteration {it}: best |r_1| {np.hypot(*rb):.3e} at ({zb[0]:.9f}, {zb[1]:.9f}); Newton step ({step[0]:+.3e}, {step[1]:+.3e}); J singular values {np.linalg.svd(J, compute_uv=False)}", flush=True)
        if done:
            verdict[0] = dict(converged=True, A=zb[0] + step[0], w=zb[1] + step[1], solved_A=zb[0], solved_w=zb[1], r1=list(rb), r3=best["r3"], r5=best["r5"], F3=best["F3"], F5=best["F5"],
                              newton_step=list(step), points=len(pts), xi1=xi, bars=list(bars))
            break
        s = min(1.0, tr[0] / max(abs(step[0]), 1e-300), tr[1] / max(abs(step[1]), 1e-300))
        newp = None
        for _ in range(5):
            zn = zb + s * step
            q = run(zn[0], zn[1], best["x"])
            if q["ok"] and np.hypot(*q["r1"]) < np.hypot(*rb):
                newp = q
                break
            s *= 0.5
        if newp is None:
            verdict[0] = dict(converged=False, why="no step reduced |r_1| with a converged solve (five halvings)", best=dict(A=best["A"], w=best["w"], r1=best["r1"]), points=len(pts), xi1=xi)
            break
        dz, dr = np.array([newp["A"] - best["A"], newp["w"] - best["w"]]), np.array(newp["r1"]) - rb
        J = J + np.outer(dr - J @ dz, dz) / (dz @ dz)
        best = newp
        acc.append((newp["A"], newp["w"]))
    else:
        verdict[0] = dict(converged=False, why=f"{maxit} iterations", best=dict(A=best["A"], w=best["w"], r1=best["r1"]), points=len(pts), xi1=xi)
    json.dump(dict(name=name, xi1=xi, start=[A0, w0, *x3], points=pts, verdict=verdict[0]), open(path, "w"), indent=1)
    print("VERDICT", json.dumps(verdict[0]), flush=True)
    return 0 if verdict[0]["converged"] else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(0 if selftest("noposbar" if "--mutate=noposbar" in sys.argv else "") else 1)
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""walk1027.py NAME A W B3 C3 B5 C5 [--xi1 0.15] [--procs 2] [--maxit 25] [--tr 0.01,0.02] [--bar 1e-6] [--seed 1027] [--out walks] [--logs logs]: #1026's walk (walk1026.py) at M = 7 (#1027). Each point is
`INNER_NB_RTOL=1e-13 hier_nb.py 7 A w --x=B3,C3,B5,C5,B7,C7 --xi1=XI --pretune --fixA --schur --predict --floor --procs P --h3=1e-4 --verbose=2` (the M = 7 flags of proof/B_tail_M7.md; the start of
F_7 is zero, the harmonics of the best earlier point otherwise, read from the last `x [...]` of its log). A solve counts when |r_3|, |r_5| and |r_7| are under BAR; when the first attempt's |r_3| is not, up to three repeats
follow from its end state with every harmonic times (1 + 1e-7 u), u uniform in (-1, 1) from random.Random(SEED), one generator per walk in solve order (the protocol of #976, #977, #1002), and the first attempt under
the bar counts. The outer Newton is walk1026's (forward-difference Jacobian steps 2e-3 in A and 1e-3 in w/w_inf, then Broyden, steps from the point of smallest |r_1| cut to the trust region TR, halved up to four
times), converged when the Newton step from the best point is under 3e-4 in A and in w/w_inf (about one solve's noise: |r_1| scatters by about 1 over a Jacobian whose smallest singular value is 3e3). The zero is that
point plus the step. Writes walks/walk_NAME_xiXI.json (every point, the F_nu/F_1 of each, the verdict) and logs/fix_NAME_xiXI_N[_rK].log per attempt."""
import json
import os
import random
import re
import subprocess
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WT = os.environ.get("W1027_WT", "/home/nathan/Source/cl-995")
PY = os.environ.get("W1027_PY", sys.executable)
BAR = 1e-6
M = 7


def attempt(A, w, x, xi, procs, tag, logdir):
    arg = [PY, "-u", "hier_nb.py", str(M), f"{A:.12f}", f"{w:.12f}", "--x=" + ",".join(f"{v:.12g}" for v in x), f"--xi1={xi}", "--pretune", "--fixA", "--schur", "--predict", "--floor", "--procs", str(procs),
           "--h3=1e-4", "--verbose=2"]
    log = os.path.join(logdir, f"{tag}.log")
    env = dict(os.environ, INNER_NB_RTOL="1e-13")
    with open(log, "w") as fh:
        fh.write("# INNER_NB_RTOL=1e-13 " + " ".join(arg) + "\n")
        fh.flush()
        subprocess.run(["nice", "-n", "10"] + arg, cwd=os.path.join(WT, "solver", "inner_stokes"), stdout=fh, stderr=subprocess.STDOUT, timeout=5400, env=env)
    txt = open(log).read()
    m = re.findall(r"FIXED-A M (\d+): A ([0-9.]+)\s+w/w_inf ([0-9.]+).*?r_1 ([+-][0-9.]+e[+-]\d+)([+-][0-9.]+e[+-]\d+)i", txt)
    f = {nu: re.findall(rf"F_{nu}/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_{nu} ([0-9.]+e[+-]\d+)", txt) for nu in (3, 5, 7)}
    xs = re.findall(r"x \[([^\]]+)\]", txt)
    if not (m and all(f.values()) and xs):
        return dict(A=A, w=w, ok=False, why="no FIXED-A line", log=log)
    xl = [float(v) for v in xs[-1].split(",")]
    F = {nu: [float(f[nu][-1][0]), float(f[nu][-1][1])] for nu in f}
    R = {nu: float(f[nu][-1][2]) for nu in f}
    ok = all(R[nu] < BAR for nu in R)
    return dict(A=A, w=w, r1=[float(m[-1][3]), float(m[-1][4])], r3=R[3], r5=R[5], r7=R[7], x=xl[2:8], F3=F[3], F5=F[5], F7=F[7], ok=ok, log=log,
                why="" if ok else f"|r_3| {R[3]:.1e} |r_5| {R[5]:.1e} |r_7| {R[7]:.1e} not under {BAR:g}")


def main(argv):
    global BAR
    name, A0, w0 = argv[0], float(argv[1]), float(argv[2])
    x0 = [float(v) for v in argv[3:7]] + [0.0, 0.0]
    opt = lambda k, d: argv[argv.index(k) + 1] if k in argv else d
    xi, procs, maxit = opt("--xi1", "0.15"), int(opt("--procs", "2")), int(opt("--maxit", "25"))
    tr = [float(v) for v in opt("--tr", "0.01,0.02").split(",")]
    BAR = float(opt("--bar", "1e-6"))
    rng = random.Random(int(opt("--seed", "1027")))
    out, logdir = opt("--out", os.path.join(HERE, "walks")), opt("--logs", os.path.join(HERE, "logs"))
    os.makedirs(out, exist_ok=True)
    pts, n = [], [0]
    path = os.path.join(out, f"walk_{name}_xi{xi}.json")
    verdict = [dict(converged=False, why="not finished")]

    def save():
        json.dump(dict(name=name, xi1=xi, M=M, start=[A0, w0, *x0], bar=BAR, points=pts, verdict=verdict[0]), open(path, "w"), indent=1)

    def run(A, w, x):
        n[0] += 1
        p = attempt(A, w, x, xi, procs, f"fix_{name}_xi{xi}_{n[0]:02d}", logdir)
        k = 0
        while not p["ok"] and p.get("x") and k < 3:
            k += 1
            xp = [v * (1 + 1e-7 * rng.uniform(-1, 1)) for v in p["x"]]
            print(f"   repeat {k} of point {n[0]} from the first attempt's end state, perturbed ({p['why']})", flush=True)
            q = attempt(A, w, xp, xi, procs, f"fix_{name}_xi{xi}_{n[0]:02d}_r{k}", logdir)
            if q.get("x") and (q["ok"] or q["r3"] < p["r3"]):
                p = dict(q, first_attempt=dict(r3=p["r3"], r5=p["r5"], r7=p["r7"]), repeats=k)
            if q["ok"]:
                break
        p["n"] = n[0]
        pts.append(p)
        r = p.get("r1")
        print(f"point {n[0]}: A {A:.9f} w {w:.9f}  " + (f"r_1 {r[0]:+.4e}{r[1]:+.4e}i |r_1| {np.hypot(*r):.3e} |r_3| {p['r3']:.1e} |r_5| {p['r5']:.1e} |r_7| {p['r7']:.1e} {'ok' if p['ok'] else 'NOT CONVERGED'}  F7/F5 {np.hypot(*p['F7']) / np.hypot(*p['F5']):.4f}" if r else p["why"]), flush=True)
        save()
        return p

    p0 = run(A0, w0, x0)
    if not p0["ok"]:
        verdict[0] = dict(converged=False, why="the start solve did not converge: " + p0["why"])
        save()
        return 1
    ps = []
    for dz in ([2e-3, 0.0], [0.0, 1e-3]):
        q = run(A0 + dz[0], w0 + dz[1], p0["x"])
        if not q["ok"]:
            verdict[0] = dict(converged=False, why="a Jacobian-step solve did not converge: " + q["why"])
            save()
            return 1
        ps.append(q)
    r0 = np.array(p0["r1"])
    J = np.column_stack([(np.array(ps[0]["r1"]) - r0) / 2e-3, (np.array(ps[1]["r1"]) - r0) / 1e-3])
    best = p0
    for it in range(maxit):
        zb, rb = np.array([best["A"], best["w"]]), np.array(best["r1"])
        step = -np.linalg.solve(J, rb)
        print(f"iteration {it}: best |r_1| {np.hypot(*rb):.3e} at ({zb[0]:.9f}, {zb[1]:.9f}); Newton step ({step[0]:+.3e}, {step[1]:+.3e}); J singular values {np.linalg.svd(J, compute_uv=False)}", flush=True)
        if abs(step[0]) < 3e-4 and abs(step[1]) < 3e-4:
            verdict[0] = dict(converged=True, A=zb[0] + step[0], w=zb[1] + step[1], solved_A=zb[0], solved_w=zb[1], r1=list(rb), r3=best["r3"], r5=best["r5"], r7=best["r7"], F3=best["F3"], F5=best["F5"], F7=best["F7"],
                              newton_step=list(step), points=len(pts), xi1=xi)
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
            verdict[0] = dict(converged=False, why="no step reduced |r_1| with a converged solve (five halvings)", best=dict(A=best["A"], w=best["w"], r1=best["r1"], F3=best["F3"], F5=best["F5"], F7=best["F7"]), points=len(pts), xi1=xi)
            break
        dz, dr = np.array([newp["A"] - best["A"], newp["w"] - best["w"]]), np.array(newp["r1"]) - rb
        J = J + np.outer(dr - J @ dz, dz) / (dz @ dz)
        best = newp
    else:
        verdict[0] = dict(converged=False, why=f"{maxit} iterations", best=dict(A=best["A"], w=best["w"], r1=best["r1"], F3=best["F3"], F5=best["F5"], F7=best["F7"]), points=len(pts), xi1=xi)
    save()
    print("VERDICT", json.dumps(verdict[0]), flush=True)
    return 0 if verdict[0]["converged"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

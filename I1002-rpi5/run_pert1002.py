"""#1002 on rpi5 (I1000's run_pert989.py with --A, --w and no m7_outer call): perturbed fixed-(A, w) solves from a source log's end state.

    python3 run_pert1002.py --end LOG_END --xi1 0.145 --seeds 1000-1007 --tag rtol14_xi0145_dA [--A 2.719419] [--w 1.000022] [--rel 1e-7] [--par 2] [--cap_h 3]
    python3 run_pert1002.py --selftest [--mutate=r3|seed|std]

Run from solver/inner_stokes of the code worktree, INNER_NB_RTOL=1e-13 in the environment. Each solve k is one zero solve (A, w/w_inf fixed at 2.719219,
1.000022) of #964's S started from the 9-decimal x of the last `level 3 it` line of LOG_END (I989-win2's xi1 0.145 `zero` log) with every harmonic times
1 + REL*u, u = 2 random() - 1 from random.Random(seed_k), seed_k = 980 + k, six draws in the harmonics' order: eight starts, none chained. Up to --par
solves run side by side (two processes each). All eight are kept in the log set; m7_outer.py itself drops those with |r_3| >= 1e-6 (the printed two digits).
Output: logs/hier_nb_M7_rpi5_<tag>_s<seed>[_r3high].log, logs/m7_outer_rpi5_<tag>.txt, logs/scatter_<tag>.txt (stats of the centre's r_1), driver log.
"""
import os, random, re, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_job import parse, crashed, S, BAR, PY, Z_A, Z_W

import numpy as np  # needs the venv python


def perturbed(end, rel, rng):
    return ",".join(f"{float(v) * (1 + rel * (2 * rng.random() - 1)):.10g}" for v in end.split(","))


def stats(r1s, sv_min=None, J=None):
    """r1s: list of (re, im). sigma = sqrt(trace of the sample covariance) (ddof 1; for two solves |d|/sqrt 2, #989's 0.23)"""
    R = np.array(r1s, float)
    n = len(R)
    mean = R.mean(axis=0)
    cov = np.cov(R.T, ddof=1) if n > 1 else np.zeros((2, 2))
    out = dict(n=n, mean=mean, sigma=float(np.sqrt(np.trace(cov))), cov=cov)
    if J is not None:
        Ji = np.linalg.inv(J)
        out["se_prop"] = float(np.sqrt(np.trace(Ji @ cov @ Ji.T) / n))     # propagated through J^-1 with J fixed
        sv = np.linalg.svd(J, compute_uv=False)
        out["se_bound"] = out["sigma"] / (np.sqrt(n) * sv[-1])              # sigma / (sqrt(n) * smallest singular value), #989's formula
        out["sv"] = sv
    return out


def selftest(a):
    mut = [t for t in a if t.startswith("--mutate=")]
    mut = mut[0].split("=")[1] if mut else ""
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + label); ok = ok and cond
    r = random.Random(981 if mut == "seed" else 980)
    u = [round(2 * r.random() - 1, 6) for _ in range(6)]
    chk("seed 980: the six u are -0.145862, 0.957375, -0.651575, -0.576905, -0.426037, -0.176319", u == [-0.145862, 0.957375, -0.651575, -0.576905, -0.426037, -0.176319])
    e = "0.1489782,0.014770826,0.008424259,0.001511207,0.00047421,0.000121682"
    p = perturbed(e, 1e-7, random.Random(980))
    chk("seed 980's start: harmonic 1 is 0.1489782 x (1 - 0.145862e-7) = 0.14897819784", p.split(",")[0] == "0.1489781978")
    chk("every harmonic within 1e-7 relative", all(abs(float(x) / float(y) - 1) <= 1e-7 + 1e-10 for x, y in zip(p.split(","), e.split(","))))
    # two solves of #989 at 0.145 (-0.4254+0.0216i, -0.0975-0.0016i): sigma 0.23, as the issue's recommendation says
    s = stats([(-0.4254, 0.0216), (-0.0975, -0.0016)])
    sg = s["sigma"] * (2 if mut == "std" else 1)
    chk("sigma of #989's two centre solves is 0.232", abs(sg - 0.2324) < 5e-4)
    # a planted J and covariance: the propagated standard error against a hand value
    J = np.diag([1e4, 2e3]); R = [(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)]
    s = stats(R, J=J)
    chk("planted: four points (+-1, 0), (0, +-1): trace of the ddof-1 covariance 4/3, sigma 1.1547", abs(s["sigma"] - np.sqrt(4 / 3)) < 1e-9)
    chk("planted: bound = sigma / (2 * 2e3)", abs(s["se_bound"] - np.sqrt(4 / 3) / (2 * 2e3)) < 1e-12)
    chk("1.0e-06 as printed does not pass", not ((float("1.0e-06") <= BAR) if mut == "r3" else (float("1.0e-06") < BAR)))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def run1(cmd, log, deadline):
    f = open(log, "w")
    p = subprocess.Popen(["nice", "-n", "10"] + cmd, stdout=f, stderr=subprocess.STDOUT, start_new_session=True)
    return p, f


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest(a)
    g = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    xi1, tag, endlog, dA, dw = g("--xi1", "0.145"), g("--tag", "rtol14_xi0145"), g("--end"), g("--dA"), g("--dw")
    A0, W0 = float(g("--A", Z_A)), float(g("--w", Z_W))
    lo, hi = (int(t) for t in g("--seeds", "980-987").split("-"))
    rel, par, cap_h = float(g("--rel", "1e-7")), int(g("--par", 2)), float(g("--cap_h", 3))
    t0 = time.time(); deadline = t0 + cap_h * 3600
    drv = open(f"logs/run1002_{tag}.driver.log", "a")

    def log_driver(s):
        line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
        print(line, flush=True); drv.write(line + "\n"); drv.flush()
    log_driver(f"INNER_NB_RTOL={os.environ.get('INNER_NB_RTOL')} end state from {endlog}, seeds {lo}-{hi}, rel {rel:g}, {par} side by side, cap {cap_h:g} h")
    _, r3e, end = parse(open(endlog).read())
    log_driver(f"end state of {endlog}: |r_3| {r3e:.2e}, x {end}")
    jobs = []
    for sd in range(lo, hi + 1):
        x0 = perturbed(end, rel, random.Random(sd))
        log = f"logs/hier_nb_M7_rpi5_{tag}_s{sd}.log"
        cmd = [PY, "-u", "hier_nb.py", "7", f"{A0:.9g}", f"{W0:.9g}", f"--x={x0}", f"--xi1={xi1}"] + S
        jobs.append((sd, log, cmd, x0))
    if "--dry" in a:
        for sd, log, cmd, x0 in jobs:
            print(" ".join(cmd[1:6]), x0, "->", log)
        return 0
    running, done = [], {}
    while jobs or running:
        while jobs and len(running) < par:
            sd, log, cmd, x0 = jobs.pop(0)
            log_driver(f"seed {sd}: start x {x0}")
            p, f = run1(cmd, log, deadline); running.append((sd, log, p, f))
        time.sleep(3)
        for item in list(running):
            sd, log, p, f = item
            if time.time() > deadline and p.poll() is None:
                os.killpg(p.pid, 9); p.wait(); log_driver(f"seed {sd}: killed at the cap")
            if p.poll() is not None:
                f.close(); running.remove(item)
                txt = open(log).read(); res = parse(txt)
                if crashed(txt) or res is None:
                    log_driver(f"seed {sd}: Traceback or no FIXED-A line (exit {p.returncode})"); done[sd] = (log, None); continue
                r1, r3, e = res
                ok = r3 < BAR
                if not ok:
                    new = log[:-4] + "_r3high.log"; os.rename(log, new); log = new
                done[sd] = (log, (r1, r3))
                log_driver(f"seed {sd}: r_1 {r1.real:+.4f}{r1.imag:+.4f}i  |r_3| {r3:.2e}  {'passes' if ok else 'above the bar'}  [{time.time()-t0:.0f} s]")
    log_driver(f"{sum(1 for v in done.values() if v[1] is not None and v[1][1] < BAR)} of {len(done)} solves under the bar")
    if dA is None:
        return 0
    cen = [done[sd][0] for sd in sorted(done) if done[sd][1] is not None]
    cmd = [PY, "m7_outer.py", "--local"] + cen + ["--", dA, dw]
    log_driver("run: " + " ".join(cmd))
    out = subprocess.run(cmd, capture_output=True, text=True)
    txt = out.stdout + out.stderr + f"(exit {out.returncode})\n"
    open(f"logs/m7_outer_rpi5_{tag}.txt", "w").write(f"# xi1 {xi1}\n$ {' '.join(cmd)}\n" + txt)
    log_driver(f"m7_outer.py --local exit {out.returncode}; output in logs/m7_outer_rpi5_{tag}.txt")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())

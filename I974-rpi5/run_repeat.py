"""#974 run 3: repeats of xi1 0.14's zero solve at rtol 1e-13, then m7_outer.py --local with every passing centre solve.

    python3 run_repeat.py --xi1 0.14 --tag rtol13_xi014 --seed LOG_ZERO --dA LOG --dw LOG [--max 3] [--want 2] [--cap_h 3]
                          [--perturb REL --rngseed N]
    python3 run_repeat.py --selftest [--mutate=r3|count|endstate]

Run from solver/inner_stokes/ of the code worktree, with INNER_NB_RTOL=1e-13 in the environment. Each repeat is one zero solve (A, w/w_inf
fixed at 2.719219, 1.000022) of #964's S, started from the previous solve's own end state (the 9-decimal x of its last `level 3 it` line,
the seed's for the first). The same end state would give the same r_1 (numba solves are deterministic, #964), so the chain moves on. It stops
after --want repeats with |r_3| < 1e-6 or after --max repeats, whichever comes first. A Traceback before a FIXED-A line stops it.
With --perturb REL each repeat instead starts from the SEED's end state with every harmonic multiplied by 1 + REL*u, u uniform in
(-1, 1) from random.Random(N) (the chain gives the same r_1 every time, I974 run 3's first result); the logs are then ..._pert<k>.log.
Logs: logs/hier_nb_M7_rpi5_<tag>_rep<k>.log (renamed _r3high when |r_3| >= 1e-6); driver log logs/run974_<tag>.driver.log.
"""
import os, random, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from run_job import parse, crashed, run, S, BAR, PY, Z_A, Z_W  # I965's run_job.py: the §3.1 parser, stop rules and solve command


def passes(r3, want_mut=""):
    return r3 < BAR


def perturbed(end, rel, rng):
    """the end state's harmonics, each times 1 + rel*u, u uniform in (-1, 1), as a --x string (10 significant digits)"""
    return ",".join(f"{float(v) * (1 + rel * (2 * rng.random() - 1)):.10g}" for v in end.split(","))


def selftest(a):
    mut = [t for t in a if t.startswith("--mutate=")]
    mut = mut[0].split("=")[1] if mut else ""
    ok = True

    def chk(label, cond):
        nonlocal ok
        print(("ok   " if cond else "FAIL ") + label); ok = ok and cond
    t = open("logs/hier_nb_M7_rpi5_rtol13_xi014_zero.log").read()
    r1, r3, end = parse(t)
    if mut == "r3":
        r3 = 1.0 / r3
    chk("Job A zero: |r_3| 7.2e-7, passes the bar", abs(r3 - 7.2e-7) < 1e-9 and passes(r3))
    if mut == "endstate":
        end = ",".join(end.split(",")[:3])
    chk("Job A zero: end state is six 9-decimal harmonics", end is not None and len(end.split(",")) == 6)
    t2 = open("logs/hier_nb_M7_rpi5_rtol13_xi014_zero_repeat_r3high.log").read()
    _, r3b, _ = parse(t2)
    if mut == "count":
        r3b = 1e-7
    chk("Job A zero_repeat_r3high: |r_3| 1.2e-5, does not pass", not passes(r3b))
    chk("1.0e-06 as printed does not pass (m7_outer's rule)", not passes(float("1.0e-06")))
    e = "0.1489782,0.014770826,0.008424259,0.001511207,0.00047421,0.000121682"
    p1, p2 = perturbed(e, 1e-7, random.Random(974)), perturbed(e, 1e-7, random.Random(974))
    if mut == "pert":
        p2 = perturbed(e, 1e-7, random.Random(975))
    chk("perturbed start is reproducible from its rng seed", p1 == p2)
    chk("perturbed start differs from the end state, by at most 1e-7 relative",
        p1 != e and all(abs(float(x) / float(y) - 1) <= 1e-7 + 1e-10 for x, y in zip(p1.split(","), e.split(","))))
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def main():
    a = sys.argv[1:]
    if "--selftest" in a:
        return selftest(a)
    g = lambda k, d=None: a[a.index(k) + 1] if k in a else d
    xi1, tag, seed, dA, dw = g("--xi1"), g("--tag"), g("--seed"), g("--dA"), g("--dw")
    mx, want, cap_h = int(g("--max", 3)), int(g("--want", 2)), float(g("--cap_h", 3))
    rel, rng = float(g("--perturb", 0)), random.Random(int(g("--rngseed", 974)))
    name = "pert" if rel else "rep"
    t0 = time.time(); deadline = t0 + cap_h * 3600
    drv = open(f"logs/run974_{tag}.driver.log", "a")
    drv.write(f"INNER_NB_RTOL={os.environ.get('INNER_NB_RTOL')} seed {seed} max {mx} want {want} cap {cap_h:g} h perturb {rel:g} rngseed {g('--rngseed', 974)}\n")

    def log_driver(s):
        line = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()) + " " + s
        print(line, flush=True); drv.write(line + "\n"); drv.flush()
    _, r3s, end = parse(open(seed).read())
    seed_end = end
    log_driver(f"seed {seed}: |r_3| {r3s:.2e}, end state x {end}")
    logs, npass = [], 0
    for k in range(1, mx + 1):
        log = f"logs/hier_nb_M7_rpi5_{tag}_{name}{k}.log"
        x0 = perturbed(seed_end, rel, rng) if rel else end
        cmd = [PY, "-u", "hier_nb.py", "7", f"{Z_A:.9g}", f"{Z_W:.9g}", f"--x={x0}", f"--xi1={xi1}"] + S
        rc = run(cmd, log, deadline, log_driver)
        txt = open(log).read()
        if rc is None:
            log_driver(f"{name}{k}: stopped by the {cap_h:g} h cap"); logs.append(log); break
        res = parse(txt)
        if crashed(txt) or res is None:
            log_driver(f"{name}{k}: Traceback or no FIXED-A line (exit {rc}): stop"); logs.append(log); break
        r1, r3, e = res
        ok = passes(r3)
        npass += ok
        log_driver(f"{name}{k}: r_1 {r1.real:+.4f}{r1.imag:+.4f}i  |r_3| {r3:.2e}  {'passes' if ok else 'above the bar'}  [{time.time()-t0:.0f} s]")
        if not ok:
            new = log[:-4] + "_r3high.log"; os.rename(log, new); log = new
        logs.append(log)
        if e is None:
            log_driver(f"{name}{k}: no end state in the log: stop"); break
        end = e  # chain (ignored with --perturb): the next repeat starts from this solve's own end state
        if npass >= want:
            break
    log_driver(f"{npass} of {len(logs)} repeats pass the bar")
    cen = [seed] + logs
    cmd = [PY, "m7_outer.py", "--local"] + cen + ["--", dA, dw]
    log_driver("run: " + " ".join(cmd))
    out = subprocess.run(cmd, capture_output=True, text=True)
    txt = out.stdout + out.stderr + f"(exit {out.returncode})\n"
    open(f"logs/m7_outer_rpi5_{tag}_{name}.txt", "w").write(f"# xi1 {xi1}\n$ {' '.join(cmd)}\n" + txt)
    log_driver(f"m7_outer.py --local exit {out.returncode}; output in logs/m7_outer_rpi5_{tag}_{name}.txt")
    print(txt)
    return 0


if __name__ == "__main__":
    sys.exit(main())

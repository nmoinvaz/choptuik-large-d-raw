"""#1021: the repeats of #1027's walk (the protocol of #976, #977, #1002) for one fixed-(A, w) M = 5 solve whose first
attempt is not under the bar (|r_3|, |r_5| < 1e-6): up to three repeats from the best attempt's end state (its
F_3/F_1, F_5/F_1 times A, as walk1026.py reads them), every harmonic times (1 + 1e-7 u), u uniform in (-1, 1) from
random.Random(1027), one generator per solve; the first attempt under the bar counts, else the one of smallest |r_3|.
Each attempt is `hier.py 5 A w --x=B3,C3,B5,C5 --fixA --schur --procs 1 --verbose=1 --xi1=XI` in CODE/solver/inner_stokes
at nice 19, logged to LOG's name with _rK; then m5_read.py's verdict line. Exit 0 when an attempt is under the bar.
    python m5_repeat.py CODE PY LOG"""
import os, random, re, subprocess, sys

code, py, log0 = sys.argv[1:4]
BAR = 1e-6
here = os.path.dirname(os.path.abspath(__file__))


def read(log):
    t = open(log).read()
    m = re.findall(r"FIXED-A M 5: A ([0-9.]+)\s+w/w_inf ([0-9.]+)", t)
    f3 = re.findall(r"F_3/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_3 ([0-9.]+e[+-]\d+)", t)
    f5 = re.findall(r"F_5/F_1 = ([+-][0-9.]+)([+-][0-9.]+)i.*?r_5 ([0-9.]+e[+-]\d+)", t)
    xi = re.search(r"--xi1=([0-9.]+)", t).group(1)
    if not (m and f3 and f5):
        return None
    A, w = m[-1]
    Af = float(A)
    x = [float(f3[-1][0]) * Af, float(f3[-1][1]) * Af, float(f5[-1][0]) * Af, float(f5[-1][1]) * Af]
    return dict(A=A, w=w, xi=xi, x=x, r3=float(f3[-1][2]), r5=float(f5[-1][2]), log=log)


p = read(log0)
if p is None:
    raise SystemExit(f"{log0}: no FIXED-A block")
print(f"first attempt {os.path.basename(log0)}: |r_3| {p['r3']:.2g}, |r_5| {p['r5']:.2g}", flush=True)
rng, best = random.Random(1027), p
for k in range(1, 4):
    if best["r3"] < BAR and best["r5"] < BAR:
        break
    xp = [v * (1 + 1e-7 * rng.uniform(-1, 1)) for v in best["x"]]
    log = log0.replace(".log", f"_r{k}.log")
    arg = [py, "-u", "hier.py", "5", p["A"], p["w"], "--x=" + ",".join(f"{v:.10f}" for v in xp), "--fixA", "--schur",
           "--procs", "1", "--verbose=1", f"--xi1={p['xi']}"]
    with open(log, "w") as fh:
        fh.write("# " + " ".join(arg) + f" (repeat {k} of {os.path.basename(log0)}, perturbed 1e-7)\n")
        fh.flush()
        subprocess.run(["nice", "-n", "19"] + arg, cwd=os.path.join(code, "solver", "inner_stokes"), stdout=fh,
                       stderr=subprocess.STDOUT, timeout=3600)
    q = read(log)
    if q is None:
        print(f"repeat {k}: no FIXED-A block", flush=True)
        continue
    print(f"repeat {k} {os.path.basename(log)}: |r_3| {q['r3']:.2g}, |r_5| {q['r5']:.2g}", flush=True)
    if (q["r3"] < BAR and q["r5"] < BAR) or q["r3"] < best["r3"]:
        best = q
print(f"counted: {os.path.basename(best['log'])}", flush=True)
r = subprocess.run([py, os.path.join(here, "m5_read.py"), best["log"]], capture_output=True, text=True)
print(r.stdout.strip())
sys.exit(r.returncode)

#!/usr/bin/env python3
"""#1025 d19125 (dh610) plant_grid4.py [--mutate=shift|round2]: does dh170's read_lower.py (blob 89309d3c, unedited) read a 0.0025 grid with four-decimal lambda keys?
Planted scans on the real lambda list of this run (1.505 to 1.545 at 0.0025, plus a repeat of 1.525), written as six files scan_D19.125_p<i mod 6>.jsonl like the lane's and read through read_lower.py's command line:
  A two simple roots 0.0092 apart (1.5204 and 1.5296), det nearly linear through each: two robust changes whose det-linear estimates must be within 5e-4 of the roots, no minimum without a change, the repeat agrees;
  B no root, a merged pair's trace: ln|det| with one minimum at 1.525 and no sign change: zero changes, exactly one free minimum at 1.525;
  C one root at 1.51137, off the three-decimal grid: one change, estimate within 5e-4.
Exit 0 only if every case reads as planted. --mutate=shift moves the expected roots by 0.003 (A and C must then fail); --mutate=round2 writes the lambdas rounded to two decimals, a stand-in for a coarse-key reader (the cases must fail). Each mutation must exit 1."""
import os, sys, json, re, subprocess
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__)); IN = f"{HERE}/in"
PY = sys.executable
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
LAMS = [round(1.505 + 0.0025 * i, 4) for i in range(17)] + [1.525]
TOL = 5e-4


def write(d, f):
    os.makedirs(d, exist_ok=True)
    fh = [open(f"{d}/scan_D19.125_p{p}.jsonl", "w") for p in range(6)]
    for i, l in enumerate(LAMS):
        v = f(l)
        lam = round(l, 2) if MUT == "round2" else l
        fh[i % 6].write(json.dumps(dict(D=19.125, kc=63, lam=lam, sign=1.0 if v > 0 else -1.0, ln=float(np.log(abs(v))), noise=[1.0, 1.0], noise_robust=True, f64_sign=1.0, f64_ln=0.0, state="planted", sec=0)) + "\n")
    for h in fh:
        h.close()


def read(d):
    env = dict(os.environ, D18_DIR=IN, PYTHONDONTWRITEBYTECODE="1")
    r = subprocess.run([PY, "-W", "ignore", f"{IN}/read_lower.py", d, "1.505", "1.545"], capture_output=True, text=True, env=env)
    ch = [(float(m.group(3)), m.group(1), m.group(2)) for m in re.finditer(r"robust change \(([\d.]+), ([\d.]+)\), [+-] to [+-], det-linear ([\d.]+)", r.stdout)]
    mn = re.search(r"minima without a sign change: (.*)", r.stdout).group(1)
    free = [float(x) for x in re.findall(r"\(([\d.]+), [\d.]+\)", mn)]
    return r.returncode, [c[0] for c in ch], free, "DISAGREE" not in r.stdout and "agree" in r.stdout, r.stdout


def main():
    s = 0.003 if MUT == "shift" else 0.0
    tag = MUT or "plain"
    a1, a2, c0 = 1.5204 + s, 1.5296 + s, 1.51137 + s
    fA = lambda l: (l - 1.5204) * (l - 1.5296) * 40 * (1 + 0.3 * (l - 1.5))
    fB = lambda l: (l - 1.525) ** 2 + 1e-5
    fC = lambda l: (l - 1.51137) * (1 + 0.5 * (l - 1.5))
    res = []
    for name, f in (("A", fA), ("B", fB), ("C", fC)):
        d = f"{HERE}/plant4_{tag}/{name}"
        write(d, f)
        res.append((name,) + read(d)[:4])
    okA = res[0][1] == 0 and len(res[0][2]) == 2 and abs(res[0][2][0] - a1) < TOL and abs(res[0][2][1] - a2) < TOL and not res[0][3] and res[0][4]
    okB = res[1][1] == 0 and res[1][2] == [] and res[1][3] == [1.525]
    okC = res[2][1] == 0 and len(res[2][2]) == 1 and abs(res[2][2][0] - c0) < TOL and not res[2][3]
    for name, ok, r in zip("ABC", (okA, okB, okC), res):
        print(f"  case {name}: reader exit {r[1]}, changes {[round(x, 5) for x in r[2]]}, free minima {r[3]}, repeat agrees {r[4]}: {'as planted' if ok else 'NOT as planted'}")
    good = okA and okB and okC
    print("plant_grid4" + (f" --mutate={MUT}" if MUT else ""), "PASS" if good else "FAIL")
    return 0 if good else 1


sys.exit(main())

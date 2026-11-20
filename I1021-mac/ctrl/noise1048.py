#!/usr/bin/env python3
"""#1048 section 1 (README.md): the residual noise at the known zero. For M in (5, 7) and xi1 in XIS, 5 fixed-(A, w) solves at
the stored zero from starts with every harmonic times (1 + 1e-7 u), u uniform in (-1, 1), one random.Random(1048) per (M, xi1)
set in start order. The solves are ../z7_m7/walk1026.py's solve (M = 5) and walk1027.py's attempt (M = 7, INNER_NB_RTOL=1e-13),
unchanged. Each solve is appended to noise/points.jsonl as it ends; a solve already there is not run again.
    python noise1048.py run            the solves (env W1026_WT/W1026_PY/W1027_WT/W1027_PY as ../z7_m7/common_z7.sh)
    python noise1048.py table          per set: n converged, sigma_1, mean r_1, median and largest |r_nu|
    python noise1048.py selftest [--mutate=sigma]      sigma_1 on synthetic r_1 (the mutation must fail, exit 1)"""
import json
import math
import os
import random
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "z7_m7"))
XIS = ("0.15", "0.175", "0.2", "0.225", "0.25")
N, BAR = 5, 1e-6
START = {5: (2.718579189229888, 0.9992284031945021,
             [0.1492035749173264, 0.01471905249087869, 0.008405346906375517, 0.0014703451817031647]),
         7: (2.7192361834604184, 1.0000243221375533,
             [0.148979544, 0.014770959, 0.008424396, 0.001511232, 0.000474221, 0.000121685])}
OUT = os.path.join(HERE, "noise", "points.jsonl")
LOGS = os.path.join(HERE, "noise", "logs")


def run():
    import walk1026, walk1027
    os.makedirs(LOGS, exist_ok=True)
    done = set()
    if os.path.exists(OUT):
        done = {json.loads(l)["tag"] for l in open(OUT)}
    for M in (5, 7):
        A, w, x0 = START[M]
        for xi in XIS:
            rng = random.Random(1048)
            for k in range(1, N + 1):
                x = [v * (1 + 1e-7 * rng.uniform(-1, 1)) for v in x0]
                tag = f"M{M}_xi{xi}_s{k}"
                if tag in done:
                    continue
                try:
                    if M == 5:
                        p = walk1026.solve(A, w, x, xi, 1, tag, LOGS)
                    else:
                        p = walk1027.attempt(A, w, x, xi, 1, tag, LOGS)
                except subprocess.TimeoutExpired as e:
                    p = dict(A=A, w=w, ok=False, why=f"timeout {e.timeout} s", log=os.path.join(LOGS, tag + ".log"))
                rec = dict(tag=tag, M=M, xi1=xi, start=k, x_start=x, **{q: p.get(q) for q in ("A", "w", "r1", "r3", "r5", "r7", "ok", "why", "x")})
                rec["log"] = os.path.relpath(p["log"], HERE)
                with open(OUT, "a") as fh:
                    fh.write(json.dumps(rec) + "\n")
                r = p.get("r1")
                print(f"{tag}: " + (f"r_1 {r[0]:+.4e}{r[1]:+.4e}i |r_3| {p['r3']:.1e} |r_5| {p['r5']:.1e}"
                                    + (f" |r_7| {p['r7']:.1e}" if M == 7 else "") + (" ok" if p["ok"] else " not converged")
                                    if r else p["why"]), flush=True)


def sigma(r1s, mut=""):
    """sample standard deviation of complex r_1 over n >= 2 solves (None otherwise)"""
    n = len(r1s)
    if n < 2:
        return None
    m = complex(sum(z.real for z in r1s) / n, sum(z.imag for z in r1s) / n)
    s = sum(abs(z - m) ** 2 for z in r1s)
    return math.sqrt(s / (n if mut == "sigma" else n - 1))


def table(path=OUT):
    recs = [json.loads(l) for l in open(path)]
    rows = []
    for M in (5, 7):
        for xi in XIS:
            rs = [r for r in recs if r["M"] == M and r["xi1"] == xi]
            if not rs:
                continue
            ok = [r for r in rs if r["ok"]]
            r1 = [complex(*r["r1"]) for r in ok]
            sg = sigma(r1)
            mean = complex(sum(z.real for z in r1) / len(r1), sum(z.imag for z in r1) / len(r1)) if r1 else None
            row = dict(M=M, xi1=xi, solves=len(rs), converged=len(ok), sigma1=sg, mean_r1=[mean.real, mean.imag] if mean else None)
            for nu in (3, 5, 7) if M == 7 else (3, 5):
                v = sorted(r[f"r{nu}"] for r in rs if r.get(f"r{nu}") is not None)
                row[f"r{nu}_median"], row[f"r{nu}_max"] = (v[len(v) // 2], v[-1]) if v else (None, None)
            rows.append(row)
    return rows


def selftest(mut):
    got = [sigma([1 + 0j, -1 + 0j], mut), sigma([1j, 1j, 1j], mut), sigma([2 + 0j], mut)]
    want = [math.sqrt(2.0), 0.0, None]
    ok = got[2] is None and abs(got[0] - want[0]) < 1e-15 and got[1] == 0.0
    print(f"selftest{' --mutate=' + mut if mut else ''}: sigma {got} (expect {want}): {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else ""
    if mode == "run":
        run()
    elif mode == "table":
        for row in table():
            print(json.dumps(row))
    elif mode == "selftest":
        sys.exit(0 if selftest("sigma" if "--mutate=sigma" in sys.argv else "") else 1)
    else:
        sys.exit(__doc__)

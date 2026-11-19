#!/usr/bin/env python3
"""#996: the coordinator's acceptance rule for the truncated models' sigma_k: accept sigma_k only where a run at higher digits agrees to 1% of Delta sigma_{M+1} or
better; the agreement is reported per k.
    python agree996.py          (reads the M*.log files of this folder, 15 printed digits)
For each M the pair of runs is (lower digits, higher digits): M 3 and M 5 at 60 against 120 digits, M 7 at 60 against 120 (the 60-digit M 7 run was stopped at k 11
and is known wrong), M 9 at 120 against 180 (K 9 only). Delta sigma_{M+1} = sigma_{M+1}^[M+2] - sigma_{M+1}^[M], both from the highest-digit runs available (M 3 from the
120-digit M 3 and M 5, M 5 from the 120-digit M 5 and M 7, M 7 from the 120-digit M 7 and M 9); it does not exist for M 9 (it needs M 11), and the rule is then not
evaluated, the absolute differences are listed. The ratio |sigma_low - sigma_high| / |Delta sigma_{M+1}| is the thing to read; a k is accepted where it is <= 0.01.
--selftest plants a difference at 1% and at 2% and checks the verdicts."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RES = {}      # fit residual per log and k (the coordinator, 2026-11-19: each model's residual beside its sigma_k, sigma_{M+1} above all)
PAT = re.compile(r"^k (\d+): sigma_(\d+) = \(([^ ]+) ([+-] ?[^ ]+)j\)\s+fit resid ([\d.e+-]+)")


def read(name):
    p = os.path.join(HERE, name)
    RES[name] = {}
    out = {}
    if os.path.exists(p):
        for line in open(p):
            m = PAT.match(line)
            if m:
                out[int(m.group(1))] = complex(float(m.group(3)), float(m.group(4).replace(" ", "")))
                RES.setdefault(name, {})[int(m.group(1))] = float(m.group(5))
    return out


RUNS = {"M3_60": "M3.log", "M3_120": "M3_dps120.log", "M5_60": "M5.log", "M5_120": "M5_dps120.log", "M7_60": "M7.log", "M7_120": "M7_dps120.log",
        "M9_120": "M9_dps120.log", "M9_180": "M9_K9_dps180.log"}
PAIRS = {3: ("M3_60", "M3_120"), 5: ("M5_60", "M5_120"), 7: ("M7_60", "M7_120"), 9: ("M9_120", "M9_180")}
SHIFT = {3: ("M3_120", "M5_120"), 5: ("M5_120", "M7_120"), 7: ("M7_120", "M9_120")}   # Delta sigma_{M+1} = sigma^[M+2] - sigma^[M]


def verdict(r):
    return "accepted" if r <= 0.01 * (1 + 1e-9) else "NOT accepted"


def table(runs=None):
    R = runs or {k: read(v) for k, v in RUNS.items()}
    lines = []
    for M in (3, 5, 7, 9):
        lo, hi = PAIRS[M]
        a, b = R[lo], R[hi]
        sh = None
        if M in SHIFT:
            s_m, s_n = R[SHIFT[M][0]], R[SHIFT[M][1]]
            k = 2 * (M + 1) + 1                         # the k that carries sigma_{M+1}
            if k in s_m and k in s_n:
                sh = abs(s_n[k] - s_m[k])
        lines.append(f"M {M}: {lo} against {hi}, Delta sigma_{M + 1} = " + (f"{sh:.3e}" if sh else "not yet available" if M in SHIFT else "n/a (needs M 11)"))
        for k in sorted(set(a) & set(b)):
            d = abs(a[k] - b[k])
            tag = f"sigma_{(k - 1) // 2}{' (= sigma_M+1)' if (k - 1) // 2 == M + 1 else ''}"
            res = f"  fit resid {RES.get(RUNS[hi], {}).get(k, float('nan')):.1e} ({hi}), {RES.get(RUNS[lo], {}).get(k, float('nan')):.1e} ({lo})"
            ds = "equal in all 15 printed digits (< 1e-15 relative)" if d == 0 else f"|difference| {d:.2e}"
            if sh:
                r = d / sh
                lines.append(f"   k {k:2d} {tag:<22} {ds}  = {r:.2e} of Delta sigma_{M + 1}: {verdict(r)};{res}")
            else:
                lines.append(f"   k {k:2d} {tag:<22} {ds}  (no Delta sigma_{M + 1} yet);{res}")
    return "\n".join(lines)


def selftest():
    sh = {1: complex(0, 0)}
    base = {1: complex(1.0, 0.0), 3: complex(0.5, 0.25), 5: complex(0.1, 0.2), 7: complex(0.01, 0.02), 9: complex(0.001, 0.002), 11: complex(0.0005, 0.0005)}
    shift = 4e-5
    runs = {k: dict(base) for k in RUNS}
    runs["M3_120"] = dict(base)
    runs["M3_120"][9] = base[9] + 0.0       # sigma_4 of M 3
    runs["M5_120"] = dict(base)
    runs["M5_120"][9] = base[9] + shift     # M 5's sigma_4 differs from M 3's by the shift 4e-5 (k = 9 is sigma_4)
    runs["M3_60"] = dict(base)
    runs["M3_60"][3] = base[3] + 0.01 * shift     # 1%: accepted (<= 0.01)
    runs["M3_60"][5] = base[5] + 0.02 * shift     # 2%: not accepted
    t = table(runs)
    ok = "k  3" in t and ("= 1.00e-02 of Delta sigma_4: accepted" in t) and ("= 2.00e-02 of Delta sigma_4: NOT accepted" in t)
    print("selftest:", "pass" if ok else "FAIL")
    if not ok:
        print(t)
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
    print(table())

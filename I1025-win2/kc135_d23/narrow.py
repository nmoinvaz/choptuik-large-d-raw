#!/usr/bin/env python3
"""narrow.py STATE_BASENAME D OUT_ENDS.jsonl LO0 HI0 FILE.jsonl [FILE.jsonl ...] | --selftest [--mutate]   (#1025 kc135_d23: the narrowed bracket for a secant restart)

Reads every record of the files (scan rows and the secant's own evaluation rows) of the state STATE_BASENAME at D with lambda in [LO0, HI0] (the secant's original bracket: rows outside it are ignored), keeps those whose noise test is robust (field noise_robust, else robust),
and prints 'LO HI': HI the smallest robust lambda with hybrid sign -1, LO the largest robust lambda below it with sign +1 (the bracket of the one robust + to - change). Writes the two records
(noise_robust set from robust when absent) to OUT_ENDS.jsonl, the file d18_secant.py run takes as --ends. Exit 0; 2 when no such pair exists.
--selftest: planted rows (a clean change; extra rows inside and outside; a - before a + at a smaller lambda; a non-robust row at the edge) must give the written brackets; --mutate swaps the roles of the signs
(the selftest must then exit 1)."""
import json
import sys

MUT = "--mutate" in sys.argv


def bracket(rows, lo0=-1e9, hi0=1e9):
    ok = [r for r in rows if r.get("noise_robust", r.get("robust")) and lo0 - 1e-12 <= r["lam"] <= hi0 + 1e-12]
    plus, minus = (-1, 1) if MUT else (1, -1)
    neg = sorted(r["lam"] for r in ok if r["sign"] == minus)
    if not neg:
        return None
    hi = neg[0]
    pos = sorted(r["lam"] for r in ok if r["sign"] == plus and r["lam"] < hi)
    if not pos:
        return None
    lo = pos[-1]
    pick = lambda lam: [r for r in ok if abs(r["lam"] - lam) < 1e-12][-1]
    return lo, hi, pick(lo), pick(hi)


def selftest():
    def row(lam, sign, robust=True):
        return dict(lam=lam, sign=sign, noise_robust=robust, D=23.0, kc=135, state="s.npy")
    cases = [
        ("clean", [row(0.04, 1), row(0.045, 1), row(0.05, -1), row(0.055, -1)], (0.045, 0.05)),
        ("narrowed by the secant's own rows", [row(0.04, 1), row(0.045, 1), row(0.05, -1), row(0.0482, 1), row(0.0491, -1)], (0.0482, 0.0491)),
        ("a non-robust + at 0.049 is ignored", [row(0.04, 1), row(0.047, 1), row(0.05, -1), row(0.049, 1, False)], (0.047, 0.05)),
        ("a - below the original bracket is ignored", [row(0.03, -1), row(0.04, 1), row(0.045, 1), row(0.05, -1)], (0.045, 0.05)),
    ]
    bad = []
    for name, rows, want in cases:
        b = bracket(rows, 0.045, 0.05)
        got = None if b is None else (b[0], b[1])
        if got != want:
            bad.append("%s: %r (wanted %r)" % (name, got, want))
    if bracket([row(0.04, 1), row(0.045, 1)]) is not None:
        bad.append("no - row: a bracket was returned")
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    state, D, out, lo0, hi0, files = args[0], float(args[1]), args[2], float(args[3]), float(args[4]), args[5:]
    rows = []
    for f in files:
        for l in open(f):
            if l.strip():
                r = json.loads(l)
                if r.get("kind") == "root" or "sign" not in r or "lam" not in r:
                    continue
                if r.get("state") == state and r.get("D") == D:
                    rows.append(r)
    b = bracket(rows, lo0, hi0)
    if b is None:
        print("no robust + to - pair in %d rows" % len(rows))
        return 2
    lo, hi, rlo, rhi = b
    for r in (rlo, rhi):
        r.setdefault("noise_robust", bool(r.get("robust")))
    open(out, "w").write("".join(json.dumps(r) + "\n" for r in (rlo, rhi)))
    print("%r %r" % (lo, hi))
    return 0


if __name__ == "__main__":
    sys.exit(main())

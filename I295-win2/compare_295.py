#!/usr/bin/env python3
"""I295-win2: does sigma_n at interior orders depend on K at J 1500? (issue #295, step 1)

    python -I compare_295.py [NEW.json [REF.json [CONTROL.json]]]
        defaults: ./sigF_w1.10_K15_J1500_p1280.json, ../I228-win2/sigF_w1.10_K45_J1500_p1280.json (the reference) and
        ../I82-win2/sigF_w1.09_K45_J1500_p1280.json (the control).
        Compares the sigma_str entries n = 1..6 (re and im strings) of NEW with REF, bit for bit, and prints the six pairs of
        strings. The control repeats the comparison of NEW with CONTROL (the other node, 1.09) and must differ at n = 1.
        Exit 0: n = 1..6 all equal and the control differs at n = 1 (sigma does not depend on K at J 1500, step 2 is not run).
        Exit 1: some n <= 6 differs (the first n and its relative size are printed, step 2 runs).
        Exit 2: a file is missing, or the control does not differ at n = 1 (the comparison could not fail).
    python -I compare_295.py --selftest
        a copy of the K 45 file is equal to itself at n = 1..6, one planted digit at n = 4 is found at n = 4 with its relative size,
        the real 1.09 file differs from the 1.10 file at n = 1, and a control that equals the reference makes the run exit 2."""
import copy, json, os, sys

from mpmath import mp, mpf, mpc

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
NS = range(1, 7)
NEW = os.path.join(HERE, "sigF_w1.10_K15_J1500_p1280.json")
REF = os.path.join(RAW, "I228-win2", "sigF_w1.10_K45_J1500_p1280.json")
CTL = os.path.join(RAW, "I82-win2", "sigF_w1.09_K45_J1500_p1280.json")


def z(s): return mpc(mpf(s[0]), mpf(s[1]))


def rel(a, b): return abs(z(a) - z(b)) / abs(z(b))


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def pairs(a, b):
    """[(n, equal, relative size or None)] for n = 1..6 of two loaded files."""
    out = []
    for n in NS:
        x, y = a["sigma_str"][n], b["sigma_str"][n]
        out.append((n, x == y, None if x == y else rel(x, y)))
    return out


def run(new, ref, ctl, out=print):
    for p in (new, ref, ctl):
        if not os.path.exists(p):
            out(f"MISSING {p}")
            return 2
    a, r, c = load(new), load(ref), load(ctl)
    out(f"new {a['wf']} K {a['K']} J {a['J']} prec {a['prec']} procs {a['procs']}; ref {r['wf']} K {r['K']} J {r['J']}; control {c['wf']} K {c['K']} J {c['J']}")
    pr = pairs(a, r)
    for n, eq, d in pr:
        out(f"n={n} {'equal' if eq else 'DIFFERENT, relative ' + mp.nstr(d, 3)}\n   new {a['sigma_str'][n]}\n   ref {r['sigma_str'][n]}")
    pc = pairs(a, c)
    out("control (new against " + f"{c['wf']} K {c['K']}): " + ", ".join(f"n={n} {'equal' if eq else 'differs'}" for n, eq, _ in pc))
    if pc[0][1]:
        out("CONTROL DID NOT FIRE at n = 1, the comparison could not fail")
        return 2
    bad = [x for x in pr if not x[1]]
    if bad:
        n, _, d = bad[0]
        out(f"VERDICT: sigma_n depends on K at J 1500, first difference at n = {n}, relative {mp.nstr(d, 3)} (n = {[x[0] for x in bad]}). Step 2 runs.")
        return 1
    out("VERDICT: sigma_1..sigma_6 equal bit for bit, no dependence on K at J 1500 at these orders. Step 2 is not run.")
    return 0


def selftest():
    import tempfile
    fails = []
    ref = load(REF)
    with tempfile.TemporaryDirectory() as td:
        def dump(name, obj):
            p = os.path.join(td, name)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(obj, f)
            return p
        sink = []
        q = lambda s: sink.append(s)
        same = dump("same.json", ref)
        if any(not eq for _, eq, _ in pairs(ref, load(same))):
            fails.append("a copy differs from itself")
        bad = copy.deepcopy(ref)
        s = bad["sigma_str"][4][0]
        j = len(s) - 3
        bad["sigma_str"][4][0] = s[:j] + ("0" if s[j] != "0" else "1") + s[j + 1:]
        pr = pairs(load(dump("bad.json", bad)), ref)
        found = [n for n, eq, _ in pr if not eq]
        if found != [4] or not (pr[3][2] > 0):
            fails.append(f"planted digit at n = 4 found at {found}")
        if pairs(ref, load(CTL))[0][1]:
            fails.append("the real 1.09 file equals the 1.10 file at n = 1")
        if run(same, REF, same, out=q) != 2 or not any("CONTROL DID NOT FIRE" in x for x in sink):
            fails.append("a control equal to the reference did not make the run exit 2")
        sink.clear()
        if run(same, REF, CTL, out=q) != 0:
            fails.append("a copy against the reference with the real control did not exit 0")
        sink.clear()
        if run(dump("bad2.json", bad), REF, CTL, out=q) != 1:
            fails.append("a planted difference did not make the run exit 1")
    print("selftest: ok" if not fails else "selftest FAILED:\n  " + "\n  ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run(*(args + [NEW, REF, CTL][len(args):])))

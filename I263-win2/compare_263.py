#!/usr/bin/env python3
"""I263-win2: main's count-independent amp_flint_par.py (64914d8, #246) at K 33, J 1000, omega/omega_inf 1.10 (issue #263).

    python -I compare_263.py [DIR]
        DIR defaults to this folder. Reads sigF_w1.10_K33_J1000_main_procs2.json and ..._procs3.json. After dropping the timing keys and
        `procs` (compare_202.load):
        1. the two compared with each other (acceptance 1: bit for bit equal, or the first differing key per section);
        2. each against the three earlier K 33 files: original code with 3 workers (../I202-win2), with 2 workers (../I229-win2, equal to
           ../T153-macm3), and the per-task order of #247 (../I247-win2, 2 and 3 workers equal): equal or the first differing key, and
           the relative difference of sigma_16;
        3. acceptance 2: sigma_16 of each run against the spread of the three earlier values (the largest relative difference between two of
           them, 1.41e-18): within it, or the difference reported;
        4. the wall times (the `seconds` of each JSON) against #202 (3 workers) and #229 (2 workers), and against #247's 3 and 2 workers.
        Exit 0: the two runs are bit for bit equal. Exit 1: they differ. Exit 2: a file is missing.
    python -I compare_263.py --selftest
        a copy is equal and 'within'; a sigma_16 changed by 1e-15 relative is 'outside' the spread and its key is named; two differing runs
        give exit 1 (exit 1 inside if any of these fails)."""
import copy, json, os, sys
from itertools import combinations
from mpmath import mp, mpf, mpc

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I202-win2"))
sys.path.insert(0, os.path.join(RAW, "I236-win2"))
import compare_202 as K
import compare_236 as C

REFS = {"original, 3 workers (#202)": ("I202-win2", "sigF_w1.10_K33_J1000.json"),
        "original, 2 workers (#229)": ("I229-win2", "sigF_w1.10_K33_J1000_procs2.json"),
        "per-task order, 2 workers (#247)": ("I247-win2", "sigF_w1.10_K33_J1000_fixsum_procs2.json")}
WALL = {"#202 original, 3 workers": ("I202-win2", "sigF_w1.10_K33_J1000.json"),
        "#229 original, 2 workers": ("I229-win2", "sigF_w1.10_K33_J1000_procs2.json"),
        "#247 per-task order, 3 workers": ("I247-win2", "sigF_w1.10_K33_J1000_fixsum_procs3.json"),
        "#247 per-task order, 2 workers": ("I247-win2", "sigF_w1.10_K33_J1000_fixsum_procs2.json")}


def z(s): return mpc(mpf(s[0]), mpf(s[1]))


def rel16(a, b): return abs(z(a["sigma_str"][16]) - z(b["sigma_str"][16])) / abs(z(b["sigma_str"][16]))


def show(name, d, out):
    out(f"  {name}: " + ("EQUAL (bit for bit, timing keys and procs dropped)" if not d else "differ"))
    for sec, txt in d.items():
        out(f"      {sec}: {txt}")


def report(runs, refs, out=print):
    """runs: {2: obj, 3: obj} (canonical, procs dropped); refs: {name: obj}. Returns 0 if the two runs are equal."""
    d = C.pair_diff(runs[2], runs[3])
    out("== acceptance 1: the two runs of main's code")
    show("main procs2 vs main procs3", d, out)
    spread = max((rel16(a, b) for a, b in combinations(refs.values(), 2)), default=mpf(0))
    out(f"== acceptance 2: sigma_16 against the spread of the earlier three values ({mp.nstr(spread, 3)} relative)")
    for n in (2, 3):
        out(f"  main procs{n}: sigma_16 {runs[n]['sigma_str'][16]}")
        for name, o in refs.items():
            r = rel16(runs[n], o)
            show(f"vs {name}", C.pair_diff(runs[n], o), out)
            out(f"      sigma_16 relative difference {mp.nstr(r, 3)}  " + ("within" if r <= spread else "OUTSIDE") + " the spread")
    return 0 if not d else 1


def selftest():
    base = K.load(os.path.join(RAW, "I202-win2", "sigF_w1.10_K33_J1000.json"))
    refs = {n: K.load(os.path.join(RAW, *p)) for n, p in REFS.items()}
    q = lambda s: None
    ok = report({2: base, 3: copy.deepcopy(base)}, refs, out=q) == 0
    e = copy.deepcopy(base)
    s = e["sigma_str"][16]
    z16 = z(s) * (1 + mpf("1e-15"))
    e["sigma_str"][16] = [mp.nstr(z16.real, 20), mp.nstr(z16.imag, 20)]
    log = []
    ok &= report({2: e, 3: copy.deepcopy(base)}, refs, out=log.append) == 1 and any("OUTSIDE" in x for x in log) and any("first at sigma_16" in x for x in log)
    log = []
    ok &= report({2: copy.deepcopy(base), 3: copy.deepcopy(base)}, refs, out=log.append) == 0 and any(" within " in x for x in log) \
        and not any("OUTSIDE" in x for x in log if "vs original, 3 workers" in x)
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


def wall(path):
    return json.load(open(path)).get("seconds")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    d = sys.argv[1] if len(sys.argv) > 1 else HERE
    paths = {n: os.path.join(d, f"sigF_w1.10_K33_J1000_main_procs{n}.json") for n in (2, 3)}
    miss = [p for p in paths.values() if not os.path.exists(p)]
    if miss:
        print("MISSING", *miss)
        sys.exit(2)
    runs = {n: K.load(p) for n, p in paths.items()}
    refs = {name: K.load(os.path.join(RAW, *rel)) for name, rel in REFS.items()}
    rc = report(runs, refs)
    print("== acceptance 3: wall times (seconds in the JSON), the load beside each run differed")
    for n in (2, 3):
        print(f"  main procs{n}: {wall(paths[n])} s")
    for name, rel in WALL.items():
        print(f"  {name}: {wall(os.path.join(RAW, *rel))} s")
    sys.exit(rc)

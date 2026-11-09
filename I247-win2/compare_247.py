#!/usr/bin/env python3
"""I247-win2: the fixed-order sum at K 33, J 1000, omega/omega_inf 1.10 with 2 and 3 workers (issue #247).

    python -I compare_247.py [DIR]
        DIR defaults to this folder. Reads sigF_w1.10_K33_J1000_fixsum_procs2.json and ..._procs3.json (made by
        ../I236-win2/amp_flint_par_fixsum.py) and compares, after dropping the timing keys and `procs` (compare_202.load):
        the two with each other, and each with the original-code K 33 files of #202 (../I202-win2, 3 workers), #229
        (../I229-win2, 2 workers) and T153 (../T153-macm3, 2 workers). For each pair: equal, or the first differing entry of
        each section (sigma_str index with the relative difference, sigma_err index, f key, fit_info key and field).
        Exit 0: the two fixed-order runs are bit for bit equal. Exit 1: they differ (the first differing key is printed).
        Exit 2: a file is missing.
    python -I compare_247.py --selftest
        a copy is equal, one planted digit in one sigma string (and one in fit_info) is named at its key, and two files that
        differ give exit 1 (exit 1 inside if any of these fails)."""
import copy, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I202-win2"))
sys.path.insert(0, os.path.join(RAW, "I236-win2"))
import compare_202 as K
import compare_236 as C  # pair_diff(): first differing key per section

REFS = {"I202 (original, 3 workers)": ("I202-win2", "sigF_w1.10_K33_J1000.json"),
        "I229 (original, 2 workers)": ("I229-win2", "sigF_w1.10_K33_J1000_procs2.json"),
        "T153 macm3 (original, 2 workers)": ("T153-macm3", "sigF_w1.10_K33_J1000.json")}


def show(name, d, out):
    out(f"  {name}: " + ("EQUAL (bit for bit, timing keys and procs dropped)" if not d else "differ"))
    for sec, txt in d.items():
        out(f"      {sec}: {txt}")


def report(f2, f3, refs, out=print):
    d = C.pair_diff(f2, f3)
    out("== the two fixed-order runs")
    show("fixsum procs2 vs fixsum procs3", d, out)
    for tag, f in (("procs2", f2), ("procs3", f3)):
        out(f"== fixed-order {tag} against the original-code files")
        for name, o in refs.items():
            show(name, C.pair_diff(f, o), out)
    return 0 if not d else 1


def selftest():
    p = os.path.join(RAW, "I202-win2", "sigF_w1.10_K33_J1000.json")
    base = K.load(p)
    q = lambda s: None
    ok = report(base, copy.deepcopy(base), {}, out=q) == 0
    e = copy.deepcopy(base)
    s = e["sigma_str"][9]
    j = next(i for i in range(6, len(s[1])) if s[1][i].isdigit())
    e["sigma_str"][9] = [s[0], s[1][:j] + ("0" if s[1][j] != "0" else "1") + s[1][j + 1:]]
    log = []
    ok &= report(base, e, {}, out=log.append) == 1 and any("first at sigma_9" in x for x in log)
    e = copy.deepcopy(base)
    k = sorted(e["fit_info"], key=C.kn)[100]
    e["fit_info"][k][1] *= 1.5
    log = []
    ok &= report(base, e, {}, out=log.append) == 1 and any(f"first at {k} in err" in x for x in log)
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    d = sys.argv[1] if len(sys.argv) > 1 else HERE
    paths = [os.path.join(d, f"sigF_w1.10_K33_J1000_fixsum_procs{n}.json") for n in (2, 3)]
    missing = [x for x in paths if not os.path.exists(x)]
    if missing:
        print("MISSING", *missing)
        sys.exit(2)
    refs = {name: K.load(os.path.join(RAW, *rel)) for name, rel in REFS.items() if os.path.exists(os.path.join(RAW, *rel))}
    sys.exit(report(K.load(paths[0]), K.load(paths[1]), refs))

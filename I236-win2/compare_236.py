#!/usr/bin/env python3
"""I236-win2: how does amp_flint_par.py's output depend on --procs? (issue #236)

    python -I compare_236.py [DIR] [--prefix sigF_w1.10_K25_J1000_procs]
        DIR defaults to this folder. Reads <prefix><N>_<r>.json for N = 1..4 and r = r1, r2 (a file that is missing is listed
        and left out). Timing keys and `procs` are dropped (../I140-win2/compare.py's rule). For every pair of runs: equal or
        not, and for a pair that differs the first differing entry of each section, named: sigma_str (index n, relative
        difference), sigma_err (index), f (key "k_nu", ordered by k then nu), fit_info (key and which of Mf, err, resid), and
        any other top-level key. Then the bit-for-bit equal classes, and per pair of counts whether all of its run pairs are equal.
        Exit 0: both runs of every count are equal (equal counts give equal bits). Exit 1: some pair of equal counts differs
        (the main finding of the issue). Exit 2: a file is missing.
    python -I compare_236.py --selftest
        a copy with other timing keys and procs is equal; a planted digit in one sigma string, one f entry and one fit_info
        entry are each found at their key by the pair test; a pair of equal counts that differs makes the verdict exit 1."""
import copy, os, sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "I202-win2"))
import compare_202 as K  # load(): canonical object, timing keys and procs dropped

NS = (1, 2, 3, 4)
RUNS = ("r1", "r2")


def kn(key):
    k, nu = key.split("_")
    return int(k), int(nu)


def first_list_idx(a, b):
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return i
    return None if len(a) == len(b) else min(len(a), len(b))


def pair_diff(a, b):
    """dict section -> description of the first difference, empty when a == b"""
    d = {}
    i = first_list_idx(a["sigma_str"], b["sigma_str"])
    if i is not None:
        from mpmath import mp, mpf, mpc
        mp.dps = 50
        za, zb = (mpc(mpf(x[0]), mpf(x[1])) for x in (a["sigma_str"][i], b["sigma_str"][i]))
        d["sigma_str"] = f"first at sigma_{i}, relative {mp.nstr(abs(za - zb) / abs(zb), 3)}; n of {len([1 for x, y in zip(a['sigma_str'], b['sigma_str']) if x != y])} differ"
    i = first_list_idx(a["sigma_err"], b["sigma_err"])
    if i is not None:
        d["sigma_err"] = f"first at index {i} ({len([1 for x, y in zip(a['sigma_err'], b['sigma_err']) if x != y])} differ)"
    ks = sorted(set(a["f"]) | set(b["f"]), key=kn)
    bad = [k for k in ks if a["f"].get(k) != b["f"].get(k)]
    if bad:
        d["f"] = f"first at {bad[0]} ({len(bad)} of {len(ks)} differ)"
    ks = sorted(set(a["fit_info"]) | set(b["fit_info"]), key=kn)
    bad = [k for k in ks if a["fit_info"].get(k) != b["fit_info"].get(k)]
    if bad:
        pos = [i for i, (x, y) in enumerate(zip(a["fit_info"][bad[0]], b["fit_info"][bad[0]])) if x != y]
        names = ("Mf", "err", "resid")
        d["fit_info"] = f"first at {bad[0]} in {'/'.join(names[i] for i in pos)} ({len(bad)} of {len(ks)} differ)"
    for k in sorted(set(a) | set(b)):
        if k in ("sigma_str", "sigma_err", "f", "fit_info"):
            continue
        if a.get(k) != b.get(k):
            d[k] = "differs"
    return d


def report(runs, out=print):
    """runs: {(N, r): object}. Returns the exit code."""
    labels = sorted(runs)
    diffs = {(x, y): pair_diff(runs[x], runs[y]) for x, y in combinations(labels, 2)}
    out("== pairs of runs (equal = bit for bit after dropping the timing keys and procs)")
    for (x, y), d in diffs.items():
        tag = "EQUAL" if not d else "differ"
        out(f"  procs{x[0]}_{x[1]} vs procs{y[0]}_{y[1]}: {tag}")
        for sec, txt in d.items():
            out(f"      {sec}: {txt}")
    classes = []
    for lab in labels:
        for c in classes:
            if not diffs[(c[0], lab)]:
                c.append(lab)
                break
        else:
            classes.append([lab])
    out("== classes of runs that are bit for bit equal")
    for c in classes:
        out("  " + ", ".join(f"procs{n}_{r}" for n, r in c))
    out("== by pair of counts (all run pairs between the two counts equal / none / mixed)")
    for n, m in combinations(NS, 2):
        res = [not diffs[tuple(sorted(((n, r1), (m, r2))))] for r1 in RUNS for r2 in RUNS
               if (n, r1) in runs and (m, r2) in runs]
        out(f"  procs {n} vs procs {m}: " + ("equal" if res and all(res) else "differ" if res and not any(res) else "mixed" if res else "no data"))
    same = [(x, y) for (x, y) in diffs if x[0] == y[0]]
    bad = [(x, y) for (x, y) in same if diffs[(x, y)]]
    out(f"== equal counts: {len(same) - len(bad)} of {len(same)} pairs equal" +
        ("" if not bad else "; DIFFER: " + ", ".join(f"procs{x[0]} {x[1]}/{y[1]}" for x, y in bad)))
    return 1 if bad else 0


def selftest():
    p = os.path.join(os.path.dirname(HERE), "I202-win2", "sigF_w1.10_K33_J1000.json")
    base = K.load(p)
    quiet = lambda s: None
    ok = True
    a = {(1, "r1"): base, (1, "r2"): copy.deepcopy(base)}
    ok &= report(a, out=quiet) == 0
    e = copy.deepcopy(base)
    s = e["sigma_str"][9]
    j = next(i for i in range(6, len(s[1])) if s[1][i].isdigit())
    e["sigma_str"][9] = [s[0], s[1][:j] + ("0" if s[1][j] != "0" else "1") + s[1][j + 1:]]
    ok &= pair_diff(base, e).get("sigma_str", "").startswith("first at sigma_9") and set(pair_diff(base, e)) == {"sigma_str"}
    e = copy.deepcopy(base)
    k = sorted(e["f"], key=kn)[40]
    e["f"][k][0] *= 1.0000001
    d = pair_diff(base, e)
    ok &= d.get("f", "").startswith(f"first at {k} ") and set(d) == {"f"}
    e = copy.deepcopy(base)
    k = sorted(e["fit_info"], key=kn)[60]
    e["fit_info"][k][2] *= 1.01
    d = pair_diff(base, e)
    ok &= d.get("fit_info", "").startswith(f"first at {k} in resid") and set(d) == {"fit_info"}
    e = copy.deepcopy(base)
    e["sigma_err"][3] *= 1.5
    ok &= pair_diff(base, e).get("sigma_err", "").startswith("first at index 3")
    b = {(1, "r1"): base, (1, "r2"): e, (2, "r1"): base, (2, "r2"): base}
    out = []
    ok &= report(b, out=out.append) == 1 and any("DIFFER: procs1" in x for x in out)
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    argv = sys.argv[1:]
    if "--prefix" in argv:
        i = argv.index("--prefix")
        del argv[i:i + 2]
    args = [x for x in argv if not x.startswith("--")]
    d = args[0] if args else HERE
    prefix = "sigF_w1.10_K25_J1000_procs"
    if "--prefix" in sys.argv:
        prefix = sys.argv[sys.argv.index("--prefix") + 1]
    runs, missing = {}, []
    for n in NS:
        for r in RUNS:
            f = os.path.join(d, f"{prefix}{n}_{r}.json")
            if os.path.exists(f):
                runs[(n, r)] = K.load(f)
            else:
                missing.append(f)
    for m in missing:
        print("MISSING", m)
    rc = report(runs)
    sys.exit(2 if missing else rc)

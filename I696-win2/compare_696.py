#!/usr/bin/env python3
"""#696: Delta with the horizon series summed to ks 300 and 360 against ks 130, at D 245.1366 and D 253.8043 (runs of run_696.sh).
usage: python compare_696.py               reads D245/ and D253/ next to this file and the chain states of the raw repository; prints the report
                                           exit 0 all checks pass, 1 a check fails, 2 runs missing
       python compare_696.py --selftest    synthetic states and logs with planted differences: the differences and ratio are recovered, every
                                           check passes on the clean data, and each one fails when its input is broken once on purpose
Delta of a state = the exact sum of the last entry of each of its parts (zh, zl, z2 .. z7), each a double, in mpmath (never the decimal strings).
Checks, all fixed by the issue: control A (r130) moves Delta by at most 1e-40 from the chain state; control B (p300, r300's base at ks 300) reproduces
r300's Delta to 1e-40; r300's and r360's first octo-double |F| (the `on 0: |F|` line) is at least 1e-30 (below that --ks did nothing); r300 and r360
converge to max|F| <= 1e-60. Error bar: delta_all.csv's err column (a fit extrapolation's), which has no row at D 253.80 (last D 245.6366), so that D is
compared with the last rows' err and the report says so."""
import csv, glob, json, os, re, shutil, sys, tempfile
import numpy as np
from mpmath import mp, mpf, nstr

mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
BAR_CTL, F_FIRST, F_CONV = mpf("1e-40"), 1e-30, 1e-60
DS = {"D245": "I603-win2/chain/anm_pin3_D245.1366.npz", "D253": "I603-win2/chain_nat/anm_pin3_D253.8043.npz"}
CSV = os.path.join(RAW, "..", "choptuik-large-d", "hp", "data", "delta_all.csv")


def delta_of(path):
    z = np.load(path)
    return sum((mpf(float(z[k][-1])) for k in KEYS if k in z.files), mpf(0))


def first_F(log):
    for line in open(log, encoding="utf-8", errors="replace"):
        m = re.match(r"\s+on 0: \|F\| ([0-9.e+-]+)", line)
        if m:
            return float(m.group(1))
    return None


def final_F(log):
    """(max|F|, converged) of the last 'octo-double Newton: n steps, max|F| X, converged|not converged' line"""
    out = None
    for line in open(log, encoding="utf-8", errors="replace"):
        m = re.search(r"octo-double Newton: \d+ steps, max\|F\| ([0-9.e+-]+), (converged|not converged)", line)
        if m:
            out = (float(m.group(1)), m.group(2) == "converged")
    return out


def collect(dd_dir, chain_state):
    """the Delta of the chain state, of each run's base, and each run's first and final |F|; None for what is missing"""
    r = {"chain": delta_of(chain_state)}
    for tag in ("r130", "r300", "r360", "p300"):
        b = glob.glob(os.path.join(dd_dir, tag, "base_pin3_D*.npz"))
        log = os.path.join(dd_dir, tag + ".log")
        r[tag] = delta_of(b[0]) if b else None
        r[tag + "_first"] = first_F(log) if os.path.exists(log) else None
        r[tag + "_final"] = final_F(log) if os.path.exists(log) else None
    return r


def judge(r, err):
    """the numbers and the verdicts of one D; err is delta_all.csv's err used for the comparison"""
    need = ("r130", "r300", "r360", "p300")
    if any(r[t] is None for t in need):
        return None
    d1, d2 = r["r300"] - r["r130"], r["r360"] - r["r300"]
    v = {}
    v["A: r130 moves Delta by at most 1e-40"] = abs(r["r130"] - r["chain"]) <= BAR_CTL
    v["B: p300 reproduces r300 to 1e-40"] = abs(r["p300"] - r["r300"]) <= BAR_CTL
    v["r300 first |F| >= 1e-30"] = r["r300_first"] is not None and r["r300_first"] >= F_FIRST
    v["r360 first |F| >= 1e-30"] = r["r360_first"] is not None and r["r360_first"] >= F_FIRST
    v["r300 converged to 1e-60"] = r["r300_final"] is not None and r["r300_final"][1] and r["r300_final"][0] <= F_CONV
    v["r360 converged to 1e-60"] = r["r360_final"] is not None and r["r360_final"][1] and r["r360_final"][0] <= F_CONV
    return dict(d1=d1, d2=d2, ratio=(d2 / d1) if d1 != 0 else None, d1_over_err=abs(d1) / mpf(err), v=v)


def err_for(D_label, rows):
    """delta_all.csv's err at the D (an exact row), or at the last row when there is none, with a flag"""
    D = {"D245": 245.1366177558899, "D253": 253.8043}[D_label]
    best = min(rows, key=lambda x: abs(float(x["D"]) - D))
    exact = abs(float(best["D"]) - D) < 1e-3
    return best["err"], float(best["D"]), exact


def report(dirs, rows):
    ok, missing = True, False
    for lab, chain_state in DS.items():
        dd = os.path.join(HERE, lab) if dirs is None else dirs[lab][0]
        cs = os.path.join(RAW, chain_state) if dirs is None else dirs[lab][1]
        r = collect(dd, cs)
        err, derr, exact = err_for(lab, rows)
        j = judge(r, err)
        print(f"\n== {lab}: chain state {os.path.relpath(cs, RAW) if dirs is None else cs}")
        for t in ("chain", "r130", "r300", "r360", "p300"):
            print(f"   Delta {t:5s} {nstr(r[t], 40) if r[t] is not None else 'missing'}   first |F| {r.get(t + '_first')}   final {r.get(t + '_final')}")
        if j is None:
            print("   runs missing, no verdicts yet")
            missing = True
            continue
        print(f"   Delta(300) - Delta(130) = {nstr(j['d1'], 8)}")
        print(f"   Delta(360) - Delta(300) = {nstr(j['d2'], 8)}")
        print(f"   ratio (360-300)/(300-130) = {nstr(j['ratio'], 6) if j['ratio'] is not None else 'n/a'}   (the issue's bar is 1e-6)")
        print(f"   |Delta(300) - Delta(130)| / err = {nstr(j['d1_over_err'], 6)}   (err {err} of the delta_all.csv row at D {derr:.4f}"
              f"{'' if exact else ', the last row: there is no row at this D'}; a fit extrapolation's err, not a bound on a difference)")
        for k, good in j["v"].items():
            print(f"   {k}: {'holds' if good else 'FAILS'}")
            ok &= bool(good)
    return 2 if missing else (0 if ok else 1)


def selftest():
    """planted: Delta(300) - Delta(130) = 3e-12, Delta(360) - Delta(300) = 1.5e-17 (ratio 5e-6), controls exact; then each check broken once"""
    tmp = tempfile.mkdtemp(prefix="cmp696_")

    def state(path, total_parts):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        np.savez(path, **{k: np.array([0.0, v]) for k, v in zip(KEYS, total_parts)}, meta="{}")

    def parts(x):
        """a Delta as eight exact doubles (greedy), so the exact sum is x to 1e-60"""
        out, rem = [], mpf(x)
        for _ in range(8):
            p = float(rem)
            out.append(p)
            rem -= mpf(p)
        return out

    base = mpf("1.685761245195318") + mpf("3.0163700305894226e-34")
    plant = {"chain": base, "r130": base, "r300": base + mpf("3e-12"), "r360": base + mpf("3e-12") + mpf("1.5e-17"), "p300": base + mpf("3e-12")}
    logs = {"r130": ("1e-91", "6.8e-92", True), "r300": ("4.0e-14", "2.0e-85", True), "r360": ("4.0e-13", "3.0e-85", True), "p300": ("1e-90", "1e-90", True)}

    def build(root, mutate=None):
        dd = os.path.join(root, "D245")
        cs = os.path.join(root, "chain", "anm_pin3_D245.1366.npz")
        P, L = dict(plant), {k: list(v) for k, v in logs.items()}
        if mutate == "A":
            P["r130"] = P["r130"] + mpf("2e-40")
        if mutate == "B":
            P["p300"] = P["p300"] + mpf("3e-40")
        if mutate == "first":
            L["r300"][0] = "1e-91"
        if mutate == "conv":
            L["r360"][1], L["r360"][2] = "1e-30", False
        state(cs, parts(P["chain"]))
        for t in ("r130", "r300", "r360", "p300"):
            state(os.path.join(dd, t, "base_pin3_D245.1366.npz"), parts(P[t]))
            with open(os.path.join(dd, t + ".log"), "w") as f:
                f.write(f"  on 0: |F| {L[t][0]} converged, Delta 1.6\n      octo-double Newton: 3 steps, max|F| {L[t][1]}, {'converged' if L[t][2] else 'not converged'}; x\n")
        return {"D245": (dd, cs)}

    rows = [{"D": "245.1366177558899", "err": "4.4e-11"}]
    ok = True
    r = collect(*build(os.path.join(tmp, "clean"))["D245"])
    j = judge(r, "4.4e-11")
    got = (abs(j["d1"] - mpf("3e-12")) < mpf("1e-45"), abs(j["d2"] - mpf("1.5e-17")) < mpf("1e-50"), abs(j["ratio"] - mpf("5e-6")) < mpf("1e-12"), all(j["v"].values()))
    print("planted differences recovered (d1 3e-12, d2 1.5e-17, ratio 5e-6) and every check holds on clean data:", "ok" if all(got) else f"FAIL {got}")
    ok &= all(got)
    for mut, name in (("A", "A: r130 moves Delta by at most 1e-40"), ("B", "B: p300 reproduces r300 to 1e-40"), ("first", "r300 first |F| >= 1e-30"), ("conv", "r360 converged to 1e-60")):
        r = collect(*build(os.path.join(tmp, mut), mut)["D245"])
        jm = judge(r, "4.4e-11")
        good = jm is not None and not jm["v"][name] and sum(1 for x in jm["v"].values() if not x) == 1
        print(f"mutation {mut} fails exactly its check ({name}):", "ok" if good else "FAIL")
        ok &= good
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    rows = list(csv.DictReader(open(os.environ.get("DELTA_ALL_CSV", "D:/choptuik-i696/hp/data/delta_all.csv"), encoding="utf-8")))
    sys.exit(report(None, rows))

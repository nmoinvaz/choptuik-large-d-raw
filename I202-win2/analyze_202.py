#!/usr/bin/env python3
"""I202-win2: what differs between win2's K 33 J 1000 file at omega/omega_inf 1.10 and macm3's, and how win2's file stands
against #82's K 45 J 1500 node (issue #202).

    python -I analyze_202.py [RAW]      RAW is the raw-data repository root (default: the parent of this folder)

Part 1: every differing leaf of the two canonical objects (timing keys dropped, as I140-win2/compare.py), by top key; the
        sigma strings that differ with their relative difference; the fit_info triples (Mf, err, resid) that differ, by order.
Part 2: |dsigma_n|/|sigma_n| (n = 1..16, from the 20 stored digits, mpmath 50 digits) of #82's K 45 J 1500 node against
        T155-win2's K 33 file at 1.09 and 1.11 (same machine), T153-macm3's K 33 file at 1.10, and this folder's K 33 file at
        1.10, then n by n whether the 1.10 row is at most the larger of the 1.09 and 1.11 rows.
Control: the three rows of #82's closing table (posted values at n = 7, 9, 16) must be reproduced from the files by this code,
        or the script exits 2 before printing a verdict. Exit 0 when the 1.10 row lies within the 1.09/1.11 rows at every n,
        1 when it does not."""
import json, os, sys
from mpmath import mp, mpf, mpc

mp.dps = 50
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I140-win2"))
import compare as C  # canon(), first_diff(): the timing-key rule of #140


def P(*a): return os.path.join(RAW, *a)


def leaves(a, b, path, out):
    if type(a) != type(b):
        out.append((path, "type")); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                out.append((f"{path}/{k}", "missing")); continue
            leaves(a[k], b[k], f"{path}/{k}", out)
    elif isinstance(a, list):
        if len(a) != len(b):
            out.append((path, f"len {len(a)}/{len(b)}")); return
        for i, (x, y) in enumerate(zip(a, b)):
            leaves(x, y, f"{path}[{i}]", out)
    elif a != b:
        out.append((path, "val"))


def z(s): return mpc(mpf(s[0]), mpf(s[1]))


def rel(a, b, n): return abs(z(a[n]) - z(b[n])) / abs(z(b[n]))


def sig(*p): return json.load(open(P(*p)))["sigma_str"]


def part1():
    w, _, _ = C.canon(P("I202-win2", "sigF_w1.10_K33_J1000.json"))
    m, _, _ = C.canon(P("T153-macm3", "sigF_w1.10_K33_J1000.json"))
    out = []
    leaves(w, m, "", out)
    print(f"== part 1: win2 (this folder) against T153-macm3, K 33 J 1000, omega 1.10; {len(out)} differing leaves")
    for k in sorted(w):
        d = []
        leaves(w[k], m[k], "", d)
        print(f"   {k:10s} {'equal' if not d else f'{len(d)} differ'}")
    print("   sigma_str, index: relative difference (the strings carry 20 digits)")
    for i, (a, b) in enumerate(zip(w["sigma_str"], m["sigma_str"])):
        if a != b:
            print(f"   sigma_{i}: {mp.nstr(rel(w['sigma_str'], m['sigma_str'], i), 3)}  win2 {a}  macm3 {b}")
    print(f"   sigma_str equal for n = {[i for i, (a, b) in enumerate(zip(w['sigma_str'], m['sigma_str'])) if a == b]}")
    print(f"   sigma_err[16] win2 {w['sigma_err'][16]!r} macm3 {m['sigma_err'][16]!r}")
    fw, fm = w["fit_info"], m["fit_info"]
    print(f"   fit_info: {len(fw)} families, same keys {sorted(fw) == sorted(fm)}; (Mf, err, resid) triples")
    bad = {}
    for key in fw:
        k = int(key.split("_")[0])
        diff = [i for i in range(3) if fw[key][i] != fm[key][i]]
        if diff:
            bad.setdefault(k, []).append((key, diff))
    print(f"   Mf equal in all families: {all(fw[k][0] == fm[k][0] for k in fw)}")
    for k in sorted(bad):
        print(f"   order {k}: {len(bad[k])} of {k // 2 + 1} families differ in err or resid")
    print(f"   orders below {min(bad)} equal in every triple: "
          f"{all(fw[k] == fm[k] for k in fw if int(k.split('_')[0]) < min(bad))}")
    fd = [k for k in w["f"] if w["f"][k] != m["f"][k]]
    print(f"   f entries differing ({len(fd)} of {len(w['f'])}): {fd}")
    for k in fd:
        print(f"      {k}: win2 {w['f'][k]}  macm3 {m['f'][k]}")


def part2():
    ns = list(range(1, 17))
    k45 = {x: sig("I82-win2", f"sigF_w{x}_K45_J1500_p1280.json") for x in ("1.09", "1.10", "1.11")}
    t155 = {x: sig("T155-win2", f"sigF_w{x}_K33_J1000.json") for x in ("1.09", "1.11")}
    mac = sig("T153-macm3", "sigF_w1.10_K33_J1000.json")
    new = sig("I202-win2", "sigF_w1.10_K33_J1000.json")
    rows = {
        "1.09 K45 vs T155-win2 K33": [rel(t155["1.09"], k45["1.09"], n) for n in ns],
        "1.11 K45 vs T155-win2 K33": [rel(t155["1.11"], k45["1.11"], n) for n in ns],
        "1.10 K45 vs T153-macm3 K33": [rel(mac, k45["1.10"], n) for n in ns],
        "1.10 K45 vs I202-win2 K33": [rel(new, k45["1.10"], n) for n in ns],
        "I202-win2 vs T153-macm3": [rel(new, mac, n) for n in ns],
    }
    print("\n== part 2: |dsigma_n|/|sigma_n| of the K 45 J 1500 nodes of #82 against the K 33 J 1000 files")
    print(f"{'n':38s}" + " ".join(f"{n:>8d}" for n in ns))
    for k, v in rows.items():
        print(f"{k:38s}" + " ".join(f"{mp.nstr(x, 2):>8s}" for x in v))
    # control: #82's closing table, the values posted there (n = 7, 9, 16)
    posted = {"1.09 K45 vs T155-win2 K33": {7: "6.7e-20", 9: "3.2e-17", 16: "3.5e-16"},
              "1.11 K45 vs T155-win2 K33": {7: "3.6e-19", 9: "3.3e-18", 16: "4.4e-16"},
              "1.10 K45 vs T153-macm3 K33": {7: "1.2e-18", 9: "9.4e-18", 16: "1.2e-15"}}
    ok = True
    for name, d in posted.items():
        for n, s in d.items():
            got = mp.nstr(rows[name][n - 1], 2)
            ok &= got == s
            print(f"   control {name} n {n}: posted {s}, here {got} {'ok' if got == s else 'MISMATCH'}")
    if not ok:
        print("control failed: this code does not reproduce #82's table, no verdict")
        return 2
    a, b, c = rows["1.09 K45 vs T155-win2 K33"], rows["1.11 K45 vs T155-win2 K33"], rows["1.10 K45 vs I202-win2 K33"]
    print("\n   n   1.10 (win2 K33)   larger of 1.09/1.11   ratio   verdict")
    above = []
    for i, n in enumerate(ns):
        mx = max(a[i], b[i])
        ok_n = c[i] <= mx
        r = mp.nstr(c[i] / mx, 3) if mx != 0 else ("0" if c[i] == 0 else "inf")
        if not ok_n:
            above.append(n)
        print(f"   {n:2d}  {mp.nstr(c[i], 2):>14s}  {mp.nstr(mx, 2):>18s}  {r:>7s}   {'within' if ok_n else 'ABOVE'}")
    print(f"   above the larger same-machine row at n = {above}")
    return 0 if not above else 1


if __name__ == "__main__":
    part1()
    sys.exit(part2())

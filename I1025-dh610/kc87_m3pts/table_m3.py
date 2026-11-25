#!/usr/bin/env python3
"""#1025 kc87_m3pts (dh610) table_m3.py [selftest [--mutate]]: the results table of the README from the leg_read.txt of each point (and the k_c 95 row from ../kc95_d2175/leg_read.txt). No number is typed by hand except the
coordinator's chord values CH (the exact linear interpolation / extrapolation of macm3's roots 21.5 0.744479, 21.625 0.696157, 21.75 0.646846, 21.875 0.596477, which the order rounded to its predictions) and macm3's own D 21.75 root.
usage (from this folder): python3 -I table_m3.py > results_table.txt
selftest: a planted leg_read text parses to the planted fields; --mutate swaps the range ends in the parser, which the selftest must catch (exit 1)."""
import re, sys

PAT = re.compile(r"change \(([\d.]+), ([\d.]+)\), (\S+ to \S+), det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]")
PRED = re.compile(r"against the prediction ([\d.]+):")
CH = {"21.5625": 0.5 * (0.744479 + 0.696157), "21.6875": 0.5 * (0.696157 + 0.646846), "21.8125": 0.5 * (0.646846 + 0.596477), "21.9375": 0.596477 + 0.5 * (0.596477 - 0.646846)}


def parse(txt, mutate=False):
    m = PAT.search(txt)
    p = PRED.search(txt)
    if not m or not p:
        return None
    a, b, ori, root, lo, hi = m.groups()
    if mutate:
        lo, hi = hi, lo
    return dict(a=a, b=b, ori=ori, root=float(root), lo=float(lo), hi=float(hi), pred=float(p[1]))


def selftest(mutate):
    r = parse("hybrid signs: x\n   change (0.645, 0.650), - to +, det-linear 0.646846, range [0.646292, 0.646846]\nagainst the prediction 0.6468: change minus prediction +0.000046", mutate)
    ok = r and r["a"] == "0.645" and r["lo"] == 0.646292 and r["hi"] == 0.646846 and r["lo"] < r["hi"]
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    print("| point | bracket | det-linear root | estimator range (spread over interpolation choices, not an enclosure) | prediction | root - prediction | chord or extrapolation, exact | root - chord |")
    print("|---|---|---|---|---|---|---|---|")
    for D, path, label in [("21.5625", "21.5625/leg_read.txt", "k_c 87, D 21.5625 (macm3's state, Linux)"), ("21.6875", "21.6875/leg_read.txt", "k_c 87, D 21.6875 (Linux)"),
                           ("21.75", "21.75/leg_read.txt", "k_c 87, D 21.75 (Linux; macm3's macOS reading 0.646846)"), ("21.8125", "21.8125/leg_read.txt", "k_c 87, D 21.8125 (Linux)"),
                           ("21.9375", "21.9375/leg_read.txt", "k_c 87, D 21.9375 (Linux, extrapolated prediction)"), ("k95", "../kc95_d2175/leg_read.txt", "k_c 95, D 21.75 (regridded, Linux; prediction 0.6498)")]:
        r = parse(open(path).read())
        ch = CH.get(D)
        print(f"| {label} | ({r['a']}, {r['b']}) | {r['root']:.6f} | [{r['lo']:.6f}, {r['hi']:.6f}] | {r['pred']} | {r['root'] - r['pred']:+.6f} | " + (f"{ch:.6f} | {r['root'] - ch:+.6f} |" if ch else "- | - |"))

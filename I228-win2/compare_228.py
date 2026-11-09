#!/usr/bin/env python3
"""I228-win2: #82's K 45, J 1500 node at omega/omega_inf 1.10 rerun on win2's new firmware (issue #228).

    python -I compare_228.py [NEW.json [OLD.json]]
        defaults: ./sigF_w1.10_K45_J1500_p1280.json and ../I82-win2/sigF_w1.10_K45_J1500_p1280.json.
        Part 1: bit for bit comparison after dropping the timing keys (`procs` is kept, both runs used 3). Prints the first
        differing entry and, for a sigma string, the first differing sigma index with both strings and the relative difference;
        the number of sigma strings that differ.
        Part 2: |dsigma_n|/|sigma_n| (n = 1..16, from the 20 stored digits, mpmath 50 digits) of the new file against win2's K 33
        J 1000 file at 1.10 (../I202-win2), next to #82's same-machine rows (1.09 and 1.11, K 45 against T155-win2's K 33) and the
        old 1.10 file against the same K 33 file; per n whether the new row is at most the larger of the 1.09 and 1.11 rows.
        Part 0 (also with `--log [NEW.log [OLD.log]]`): the two logs line by line with the elapsed-time suffix `[...s]` removed: every
        `k <order>:` line (S_1, fit Mf/err/resid, sigma) and every `   k <order> nu <nu>:` line. Prints "identical through order K" for
        the orders both logs have, or the first differing line with both texts.
        Exit 0: bit for bit equal. Exit 1: not equal (the issue then asks for second_zero_nodes.py --k45 and #203's
        second_zero.py real on the new file). Exit 2: a file is missing.
    python -I compare_228.py --selftest
        a copy is equal, one planted digit in one sigma string is found at its index, and the part-2 rows reproduce the values
        posted in #82 for the old file (exit 1 inside if any fails)."""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I140-win2"))
import compare as C
from mpmath import mp, mpf, mpc

mp.dps = 50
NS = list(range(1, 17))


def z(s): return mpc(mpf(s[0]), mpf(s[1]))


def rel(a, b, n): return abs(z(a[n]) - z(b[n])) / abs(z(b[n]))


def part1(new, old, out=print):
    d = C.first_diff(new, old)
    if d is None:
        out("part 1: bit for bit equal (timing keys dropped, procs kept)")
        return 0
    path, va, vb = d
    out(f"part 1: NOT equal. First differing entry: {path}\n   new {va}\n   old {vb}")
    bad = [i for i, (x, y) in enumerate(zip(new["sigma_str"], old["sigma_str"])) if x != y]
    if bad:
        i = bad[0]
        out(f"   first differing sigma string: sigma_{i}, relative {mp.nstr(rel(new['sigma_str'], old['sigma_str'], i), 3)}\n"
            f"      new {new['sigma_str'][i]}\n      old {old['sigma_str'][i]}\n"
            f"   {len(bad)} of {len(new['sigma_str'])} sigma strings differ: {bad}")
    else:
        out("   all sigma strings equal")
    return 1


def log_lines(path):
    import re
    out = []
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip(chr(10))
        if re.match(r"^k \d+:", line) or re.match(r"^   k \d+ nu ", line):
            out.append(re.sub(r"\s*\[\d+s\]$", "", line))
    return out


def part0(new_lines, old_lines, out=print):
    """compare the common prefix of orders; returns 0 if identical"""
    import re
    last = max((int(re.match(r"^k (\d+):", l).group(1)) for l in new_lines if re.match(r"^k \d+:", l)), default=0)

    def upto(lines):
        return [l for l in lines if int(re.match(r"^(?:   )?k (\d+)", l).group(1)) <= last]
    a, b = upto(new_lines), upto(old_lines)
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            out(f"part 0: first differing log line (line {i + 1} of {len(a)}):" + chr(10) + f"   new {x}" + chr(10) + f"   old {y}")
            return 1
    if len(a) != len(b):
        out(f"part 0: the logs have {len(a)} and {len(b)} lines up to order {last}, the first {min(len(a), len(b))} are identical")
        return 1
    out(f"part 0: identical through order {last} ({len(a)} lines: S_1, fit Mf/err/resid, sigma and every nu line, elapsed times removed)")
    return 0


def sig(*p):
    return json.load(open(os.path.join(RAW, *p)))["sigma_str"]


def part2(newS, out=print):
    k45 = {w: sig("I82-win2", f"sigF_w{w}_K45_J1500_p1280.json") for w in ("1.09", "1.10", "1.11")}
    t155 = {w: sig("T155-win2", f"sigF_w{w}_K33_J1000.json") for w in ("1.09", "1.11")}
    k33 = sig("I202-win2", "sigF_w1.10_K33_J1000.json")
    rows = {"1.09 K45 vs T155-win2 K33": [rel(t155["1.09"], k45["1.09"], n) for n in NS],
            "1.11 K45 vs T155-win2 K33": [rel(t155["1.11"], k45["1.11"], n) for n in NS],
            "1.10 old K45 vs I202-win2 K33": [rel(k33, k45["1.10"], n) for n in NS],
            "1.10 NEW K45 vs I202-win2 K33": [rel(k33, newS, n) for n in NS]}
    out("part 2: |dsigma_n|/|sigma_n|")
    out(f"{'n':32s}" + " ".join(f"{n:>8d}" for n in NS))
    for k, v in rows.items():
        out(f"{k:32s}" + " ".join(f"{mp.nstr(x, 2):>8s}" for x in v))
    a, b, c = rows["1.09 K45 vs T155-win2 K33"], rows["1.11 K45 vs T155-win2 K33"], rows["1.10 NEW K45 vs I202-win2 K33"]
    above = [n for i, n in enumerate(NS) if c[i] > max(a[i], b[i])]
    out("   n at which the new 1.10 row is above the larger of the 1.09 and 1.11 rows: " + (str(above) if above else "none"))
    return rows, above


def selftest():
    q = lambda s: None
    old = C.canon(os.path.join(RAW, "I82-win2", "sigF_w1.10_K45_J1500_p1280.json"))[0]
    ok = part1(copy.deepcopy(old), old, out=q) == 0
    e = copy.deepcopy(old)
    s = e["sigma_str"][9]
    j = next(i for i in range(6, len(s[1])) if s[1][i].isdigit())
    e["sigma_str"][9] = [s[0], s[1][:j] + ("0" if s[1][j] != "0" else "1") + s[1][j + 1:]]
    log = []
    ok &= part1(e, old, out=log.append) == 1 and any("sigma_9" in x for x in log)
    rows, above = part2(old["sigma_str"], out=q)
    ok &= [mp.nstr(rows["1.10 old K45 vs I202-win2 K33"][n - 1], 2) for n in (7, 9, 16)] == ["1.2e-18", "9.4e-18", "1.2e-15"] \
        and above == [6, 7, 15, 16]
    lo = log_lines(os.path.join(RAW, "I82-win2", "w1.10.log"))
    ok &= part0(list(lo), lo, out=q) == 0
    bad = list(lo)
    i = next(j for j, l in enumerate(bad) if l.startswith("k 21:"))
    bad[i] = bad[i].replace("S_1^(21) = (", "S_1^(21) = (9", 1)
    log = []
    ok &= part0(bad, lo, out=log.append) == 1 and any("first differing log line" in x for x in log) and any("k 21:" in x for x in log)
    ok &= part0(lo[:40], lo, out=q) == 0
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    n = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sigF_w1.10_K45_J1500_p1280.json")
    o = sys.argv[2] if len(sys.argv) > 2 else os.path.join(RAW, "I82-win2", "sigF_w1.10_K45_J1500_p1280.json")
    if not (os.path.exists(n) and os.path.exists(o)):
        print("MISSING", n if not os.path.exists(n) else o)
        sys.exit(2)
    new, old = C.canon(n)[0], C.canon(o)[0]
    rc = part1(new, old)
    part2(new["sigma_str"])
    ln, lo = os.path.join(HERE, "w1.10.log"), os.path.join(RAW, "I82-win2", "w1.10.log")
    if os.path.exists(ln) and os.path.exists(lo):
        rc |= part0(log_lines(ln), log_lines(lo))
    sys.exit(rc)

#!/usr/bin/env python3
"""#861: the Pi's output logs and JSON against the stored lemmas_M_runs/ files.

    python3 cmp861.py NEW_DIR STORED_DIR

Logs: both files with their timings ([12.3 s], (12 s), 12.3 s) removed, line by line. A line whose text apart from its
numbers differs is a structural difference (N, k, ok, True/False are text or numbers in the line, so they are caught by
the number comparison or the skeleton). A number that differs in its printed digits is listed with its relative
difference. JSON: leaf by leaf, ignoring the timing keys; floats by relative difference, everything else by equality.
Exit 1 when a structural difference, a changed N, k or ok, or a changed boolean is found.
"""
import json, os, re, sys

TIME = re.compile(r"\s*[\[(]\s*\d+(\.\d+)?\s*s\s*[\])]|\b\d+(\.\d+)? s\b")
NUM = re.compile(r"[-+]?\d+\.?\d*(?:[eE][-+]?\d+)?")
PAIRS = [("fpm_table5.log", "fixed_point_M_table_M5.log"), ("fpm_data5.log", "fixed_point_M_data_M5.log"),
         ("sector5.log", "lemma6_sector_M5_rp0.08_1e-6.log"), ("scan5.log", "lemmaS_scan_M5.log")]
JPAIRS = [("fixed_point_M_table_M5.json",) * 2, ("fixed_point_M_data_M5.json",) * 2,
          ("lemma6_sector_M5_rp0.08_1e-6.json",) * 2]
TIMEKEYS = {"sec", "time", "secs", "wall"}
bad = []


def strip(s):
    return TIME.sub("", s).rstrip()


def logcmp(a, b, name):
    la, lb = [strip(x) for x in open(a).read().splitlines()], [strip(x) for x in open(b).read().splitlines()]
    if len(la) != len(lb):
        bad.append(f"{name}: {len(la)} lines against {len(lb)}")
        print(f"== {name}: {len(la)} lines against {len(lb)}")
    ndiff, worst, nnum, flags = 0, (0.0, None), 0, []
    for i, (x, y) in enumerate(zip(la, lb)):
        if x == y:
            continue
        sx, sy = NUM.sub("#", x), NUM.sub("#", y)
        nx, ny = NUM.findall(x), NUM.findall(y)
        if sx != sy or len(nx) != len(ny):
            bad.append(f"{name} line {i + 1}: text differs")
            print(f"  line {i + 1} text differs:\n    new   : {x[:200]}\n    stored: {y[:200]}")
            continue
        ndiff += 1
        for u, v in zip(nx, ny):
            if u != v:
                nnum += 1
                try:
                    r = abs(float(u) - float(v)) / max(abs(float(u)), abs(float(v)), 1e-300)
                except ValueError:
                    r = float("inf")
                if r > worst[0]:
                    worst = (r, f"line {i + 1}: {u} against {v}")
    print(f"== {name} against {os.path.basename(b)}: {len(la)} lines, {ndiff} lines with a differing printed number "
          f"({nnum} numbers), worst relative difference {worst[0]:.1e}" + (f" ({worst[1]})" if worst[1] else ""))


def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, p + f"[{i}]")
    else:
        yield p, x


def key(p):
    return re.sub(r"\[\d+\]", "", p).rsplit("/", 1)[-1]


def jsoncmp(a, b, name):
    A, B = dict(leaves(json.load(open(a)))), dict(leaves(json.load(open(b))))
    if A.keys() != B.keys():
        bad.append(f"{name}: structure differs")
        print(f"== {name}: structure differs ({len(A)} leaves against {len(B)})")
        return
    num, other, nd = {}, [], 0
    for p in A:
        x, y = A[p], B[p]
        if x == y or key(p) in TIMEKEYS:
            continue
        nd += 1
        if isinstance(x, bool) or isinstance(y, bool) or isinstance(x, str) or isinstance(y, str) or key(p) in ("N", "k", "ok", "low_ok"):
            other.append((p, x, y))
            bad.append(f"{name}: {p} {x} against {y}")
        else:
            r = abs(x - y) / max(abs(x), abs(y), 1e-300)
            if key(p) not in num or r > num[key(p)][0]:
                num[key(p)] = (r, x, y)
    print(f"== {name}: {len(A)} leaves, {nd} differ apart from timings: {len(other)} non-numeric (N, k, flags, strings), "
          f"{len(num)} numeric keys")
    for k, (r, x, y) in sorted(num.items(), key=lambda t: -t[1][0])[:8]:
        print(f"   {k:10s} worst relative difference {r:.2e} ({x} against {y})")
    for t in other[:6]:
        print("   differs:", t)


new, old = sys.argv[1], sys.argv[2]
for n, s in PAIRS:
    if os.path.exists(os.path.join(new, n)):
        logcmp(os.path.join(new, n), os.path.join(old, s), n)
    else:
        print(f"== {n}: missing")
        bad.append(f"{n} missing")
for n, s in JPAIRS:
    if os.path.exists(os.path.join(new, n)):
        jsoncmp(os.path.join(new, n), os.path.join(old, s), n)
    else:
        print(f"== {n}: missing")
        bad.append(f"{n} missing")
print("structural or flag differences:", "; ".join(bad) if bad else "none")
sys.exit(1 if bad else 0)

#!/usr/bin/env python3
"""#901: the Pi's runs of run901.sh against the Mac's folders (I427, I866, I869, I870, I877, I878).

    python3 cmp901.py PI_FOLDER RAW_ROOT

Per log (the Pi's <name>.log against the Mac's log of the same run): the lines whose text apart from numbers differs
(structural), the exit statuses (exits.txt against its "must be"), the count of "overlap True" and "overlap False", the
contraction constants (every "contraction constant ... <= x" value, as printed), and the largest relative difference of any
other printed number with its line (these are ball radii, midpoint differences and timings, which move with the machine).
Per JSON start set: every ball string "[m +/- r]" by midpoint (digits agreed, overlap) and radius ratio.
Exit 1 on a structural difference, an exit status other than the required one, a differing overlap count or contraction
constant, or a missing Mac log.
"""
import json, os, re, sys

PI, ROOT = sys.argv[1], sys.argv[2]
NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
TIME = re.compile(r"\s*\[\s*\d+(\.\d+)?\s*s\s*\]|\b\d+(\.\d+)? s\b|\(\d+(\.\d+)? s\)")
BALL = re.compile(r"^\[\s*([-+0-9.eE]*)\s*\+/-\s*([-+0-9.eE]+)\s*\]$")
CONTR = re.compile(r"contraction constant[^<]*<=\s*([0-9.eE+-]+)")
bad = []


def mac_path(name):
    """the Mac's file for the Pi's run <name>"""
    if name.startswith(("planted", "check", "lip", "two_", "start")):
        return f"I427-mac/{name}"
    if name.startswith("cert2_"):
        return f"I869-mac/{name}"
    if name.startswith("cert_M3"):
        return f"I866-mac/{name}"
    if name.startswith("cert_M5_1e-10"):
        return "I866-mac/" + name.replace("_1e-10", "")
    if name.startswith("cert_M5"):
        return f"I870-mac/{name}"
    if name.startswith("kernel"):
        return f"I877-mac/{name}"
    if name.startswith("cli"):
        return f"I878-mac/{name}"
    return None


def read(p):
    return open(p, errors="replace").read() if os.path.exists(p) else None


def rel(a, b):
    m = max(abs(a), abs(b))
    return abs(a - b) / m if m > 0 else 0.0


def clean(t):
    return [TIME.sub("", l).rstrip() for l in t.splitlines()
            if not re.match(r"^(stored set |\s*$)", l) and not l.startswith(("python-flint",))]


# 1. exit statuses
want = {}
for l in open(os.path.join(PI, "exits.txt")):
    m = re.match(r"^(\S+): exit (\d+) \(must be (\d+)\), (\d+) s", l)
    if m:
        want[m[1]] = (int(m[2]), int(m[3]), int(m[4]))
nbad = [n for n, (g, w, _) in want.items() if g != w]
for n in nbad:
    bad.append(f"{n}: exit {want[n][0]}, must be {want[n][1]}")
print(f"runs: {len(want)}; exit status as required: {len(want) - len(nbad)}; checks (0): {sum(1 for g, w, _ in want.values() if w == 0)}, "
      f"mutations (3): {sum(1 for g, w, _ in want.values() if w == 3)}; wall {sum(t for *_, t in want.values())} s\n")

print("| run | Mac log | lines | text differs | overlap True/False (Pi / Mac) | contraction constants (Pi / Mac) | largest relative difference of any other number |")
print("|---|---|---|---|---|---|---|")
for n in sorted(want, key=lambda n: list(want).index(n)):
    pi = read(os.path.join(PI, n + ".log"))
    mp = mac_path(n)
    mac = read(os.path.join(ROOT, mp + ".log")) if mp else None
    if pi is None:
        print(f"| {n} | missing Pi log |"); bad.append(f"{n}: no Pi log"); continue
    if mac is None:
        print(f"| {n} | none ({mp}) | {len(pi.splitlines())} | | | | |"); bad.append(f"{n}: no Mac log"); continue
    a, b = clean(pi), clean(mac)
    txt = [i + 1 for i in range(min(len(a), len(b))) if NUM.sub("#", a[i]) != NUM.sub("#", b[i])]
    if len(a) != len(b):
        txt.append(f"count {len(a)}/{len(b)}")
    ov = (pi.count("overlap True"), pi.count("overlap False")), (mac.count("overlap True"), mac.count("overlap False"))
    ca, cb = CONTR.findall(pi), CONTR.findall(mac)
    worst, where = 0.0, ""
    for i in range(min(len(a), len(b))):
        if i + 1 in txt:
            continue
        for u, v in zip(NUM.findall(a[i]), NUM.findall(b[i])):
            if u != v:
                r = rel(float(u), float(v))
                if r > worst:
                    worst, where = r, f"line {i + 1}: {u} against {v}"
    if txt:
        bad.append(f"{n}: text differs at {txt[:4]}")
    if ov[0] != ov[1]:
        bad.append(f"{n}: overlap counts {ov[0]} against {ov[1]}")
    if ca != cb:
        bad.append(f"{n}: contraction constants {ca} against {cb}")
    print(f"| {n} | {mp}.log | {len(a)} | {len(txt)} | {ov[0][0]}/{ov[0][1]} against {ov[1][0]}/{ov[1][1]} | "
          f"{', '.join(ca) if ca else '-'}{' (equal)' if ca == cb and ca else ' (DIFFER: ' + ', '.join(cb) + ')' if ca != cb else ''} | {worst:.1e} {where} |")

# 2. JSON start sets
print("\n| start set | balls | overlap | midpoints agree to (digits) | max abs mid difference / (r1+r2) | radius ratio Pi/Mac |")
print("|---|---|---|---|---|---|")


def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from leaves(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from leaves(v, p + f"[{i}]")
    else:
        yield p, x


import mpmath
mpmath.mp.dps = 200
for j in ("start_M5.json", "start_M5_sector.json", "start_M5_k40_sector.json", "start_M3_cert.json"):
    pa, pb = os.path.join(PI, j), os.path.join(ROOT, "I427-mac", j)
    if not (os.path.exists(pa) and os.path.exists(pb)):
        print(f"| {j} | missing |"); bad.append(f"{j}: missing"); continue
    A, B = dict(leaves(json.load(open(pa)))), dict(leaves(json.load(open(pb))))
    if A.keys() != B.keys():
        print(f"| {j} | structure differs ({len(A)} against {len(B)} leaves) |"); bad.append(f"{j}: structure"); continue
    nb, nov, mind, maxr, rr, other = 0, 0, 1e9, 0.0, [], 0
    for p in A:
        x, y = A[p], B[p]
        mx, my = (BALL.match(x) if isinstance(x, str) else None), (BALL.match(y) if isinstance(y, str) else None)
        if mx and my:
            a_, b_ = (mpmath.mpf(mx[1]) if mx[1] else mpmath.mpf(0)), (mpmath.mpf(my[1]) if my[1] else mpmath.mpf(0))
            r1, r2 = mpmath.mpf(mx[2]), mpmath.mpf(my[2])
            d = abs(a_ - b_)
            nb += 1
            nov += d <= r1 + r2
            if d > 0 and max(abs(a_), abs(b_)) > 0:
                mind = min(mind, float(-mpmath.log10(d / max(abs(a_), abs(b_)))))
            maxr = max(maxr, float(d / (r1 + r2)))
            if r2 > 0:
                rr.append(float(r1 / r2))
        elif x != y and not p.endswith(("/sec", "/time")):
            other += 1
    if nov != nb:
        bad.append(f"{j}: {nb - nov} balls disjoint")
    if other:
        bad.append(f"{j}: {other} non-ball leaves differ")
    print(f"| {j} | {nb} | {nov} | {mind:.1f} | {maxr:.1e} | {min(rr):.3f} to {max(rr):.3f} |" + (f" ({other} other leaves differ)" if other else ""))

print("\nstructural, exit, overlap-count or contraction-constant differences:", "; ".join(bad) if bad else "none")
sys.exit(1 if bad else 0)

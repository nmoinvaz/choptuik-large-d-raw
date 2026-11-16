"""#908: the wall times by group, the bracketed times of the logs against the Mac's, and the lines that differ apart from numbers.
usage: python -I -X utf8 times908.py WIN_FOLDER RAW_ROOT   (the Mac's logs are found as cmp901.py finds them)"""
import os
import re
import statistics
import sys

W, ROOT = sys.argv[1], sys.argv[2]
sys.argv = [sys.argv[0], W, ROOT]
BR = re.compile(r"\[\s*(\d+(?:\.\d+)?)\s*s\s*\]")


def mac_path(name):
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


def rd(p):
    return open(p, encoding="utf-8", errors="replace").read()


runs = []
for l in open(os.path.join(W, "exits.txt"), encoding="utf-8"):
    m = re.match(r"^(\S+): exit (\d+) \(must be (\d+)\), (\d+) s", l)
    if m:
        runs.append((m[1], int(m[2]), int(m[3]), int(m[4])))
grp = {"#427 (planted, check_m1, lip, two, start)": [], "cert (M3, M5 at h 1e-10, 1e-9, 1e-11)": [], "cert2": [],
       "kernel, cli": []}
for n, g, w, t in runs:
    k = ("cert2" if n.startswith("cert2_") else "cert (M3, M5 at h 1e-10, 1e-9, 1e-11)" if n.startswith("cert_")
         else "kernel, cli" if n.startswith(("kernel", "cli")) else "#427 (planted, check_m1, lip, two, start)")
    grp[k].append((n, g, w, t))
print("| group | runs | exit 0 / exit 3 | wall |")
print("|---|---|---|---|")
for k, v in grp.items():
    print(f"| {k} | {len(v)} | {sum(1 for x in v if x[2] == 0)} / {sum(1 for x in v if x[2] == 3)} | {sum(x[3] for x in v)} s |")
print(f"total {sum(x[3] for x in runs)} s\n")

pairs, other = [], []
for n, *_ in runs:
    mp = mac_path(n)
    a, b = rd(os.path.join(W, n + ".log")), rd(os.path.join(ROOT, mp + ".log"))
    ta, tb = [float(x) for x in BR.findall(a)], [float(x) for x in BR.findall(b)]
    if len(ta) == len(tb):
        pairs += [(n, u, v) for u, v in zip(ta, tb)]
    else:
        other.append((n, len(ta), len(tb)))
    la, lb = a.splitlines(), b.splitlines()
    for i, (x, y) in enumerate(zip(la, lb)):
        if x.rstrip() != y.rstrip() and x.startswith("stored set"):
            other.append((n, "stored set line", x.strip()[:100], y.strip()[:100]))
big = [(n, u, v, u / v) for n, u, v in pairs if v >= 5]
print(f"bracketed times: {len(pairs)} in all, {len(big)} of 5 s or more on the Mac")
if big:
    r = [x[3] for x in big]
    print(f"  Windows / Mac: min {min(r):.2f}, median {statistics.median(r):.2f}, max {max(r):.2f}")
    for n, u, v, q in sorted(big, key=lambda x: -x[1])[:5]:
        print(f"  {n}: {u:g} s against {v:g} s ({q:.2f})")
print("other differences:")
seen = set()
for o in other:
    print("  ", o)

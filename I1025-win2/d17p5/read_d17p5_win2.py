#!/usr/bin/env python3
"""read_d17p5_win2.py: win2's dd determinant signs at D 17.5 (k_c 63) at lambda 1.9072222575778963 (lower) and 1.9472222575778963 (upper), under xfkappa's rule:
a dd sign counts if its 5 exact variants agree and 1e-24 relative noise leaves it unchanged (both seeds); 1e-20 and 1e-16 are information.
The coordinator's reading: minus at the lower and plus at the upper = the root passes its sign check; the same sign at both = no root between them."""
import json
import os
import re

H = os.path.dirname(os.path.abspath(__file__)) + "/"
recs = [json.loads(x) for f in sorted(os.listdir(H)) if f.startswith("ell_ddm_d17p5_win2") and f.endswith(".jsonl") for x in open(H + f) if x.strip()]
summ = open(H + "summary_d17p5.txt").read() if os.path.exists(H + "summary_d17p5.txt") else ""
print("| lambda | dd signs of the 5 variants | agree | dd ln abs det | spread over variants | noise 1e-24 signs (2 seeds) | 1e-20 | 1e-16 | counts | float64 sign | dd M build s | s per LU | wall s |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
sg = {}
for lam in ("1.9072222575778963", "1.9472222575778963"):
    r = [x for x in recs if x["lam"] == float(lam) and not x.get("mutate")]
    if not r:
        print("| %s | no record | | | | | | | | | | | |" % lam)
        continue
    r = r[-1]
    signs = [int(x["sign"]) for x in r["dd"]]
    lns = [x["ln"] for x in r["dd"]]
    ns = {e["eps"]: [int(s) for s in e["signs"]] for e in (r["noise"] or [])}
    n24 = ns.get(1e-24, [])
    counts = r["dd_agree"] and bool(n24) and all(s == signs[0] for s in n24)
    sg[lam] = (signs[0], counts)
    log = open(H + "det_%s.log" % lam).read() if os.path.exists(H + "det_%s.log" % lam) else ""
    m = re.search(r"dd M built in (\d+) s", log)
    lu = re.search(r"([0-9.]+) s per LU", log)
    wl = re.search(r"det_%s: ell_ddm.py det exit \d+ \(want 0\), (\d+) s wall" % re.escape(lam), summ)
    print("| %s | %s | %s | %.10f | %.1e | %s | %s | %s | %s | %+d | %s | %s | %s |" % (
        lam, signs, r["dd_agree"], lns[0], max(lns) - min(lns), n24, ns.get(1e-20), ns.get(1e-16),
        "yes" if counts else "NO", int(r["f64_sign"]), m.group(1) if m else "?", lu.group(1) if lu else "?", wl.group(1) if wl else "?"))
print()
lo, hi = sg.get("1.9072222575778963"), sg.get("1.9472222575778963")
if not lo or not hi:
    print("READING: not available (a point is missing)")
elif not (lo[1] and hi[1]):
    print("READING: a sign does not count (variants split or 1e-24 noise flips it): neither reading applies")
elif lo[0] < 0 < hi[0]:
    print("READING: dd minus at the lower point and plus at the upper: the root passes its sign check")
elif lo[0] == hi[0]:
    print("READING: the same sign (%+d) at both points: no root between them" % lo[0])
else:
    print("READING: plus at the lower and minus at the upper: a change in the opposite direction, not one of the two readings")

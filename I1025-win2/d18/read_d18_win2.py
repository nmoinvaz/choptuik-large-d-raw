#!/usr/bin/env python3
"""read_d18_win2.py: win2's dd determinant signs at D 18 (k_c 63) under xfkappa's rule (d18_dd_criteria.log), read from ell_ddm_d18_win2.jsonl and the det logs.
A dd sign counts if its 5 exact variants agree and 1e-24 relative noise leaves it unchanged (both seeds); the 1e-20 and 1e-16 noise are information.
Prints, per lambda: the 5 variant signs, ln|det|, the spread over variants, the noise signs, the float64 sign, whether the sign counts, and the seconds
(M build, per LU, wall of the invocation, from the logs and summary_d18.txt)."""
import json
import os
import re

H = os.path.dirname(os.path.abspath(__file__)) + "/"
recs = [json.loads(x) for f in sorted(os.listdir(H)) if f.startswith("ell_ddm_d18_win2") and f.endswith(".jsonl") for x in open(H + f) if x.strip()]
summ = open(H + "summary_d18.txt").read() if os.path.exists(H + "summary_d18.txt") else ""
print("| lambda | dd signs of the 5 variants | agree | dd ln abs det | spread over variants | noise 1e-24 signs (2 seeds) | 1e-20 | 1e-16 | counts | float64 sign | dd M build s | s per LU | wall s |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
for lam in ("1.788704083622953", "1.8", "1.752930001950494", "1.824478165295412"):
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
    log = open(H + "det_%s.log" % lam).read() if os.path.exists(H + "det_%s.log" % lam) else ""
    m = re.search(r"dd M built in (\d+) s", log)
    lu = re.search(r"([0-9.]+) s per LU", log)
    wl = re.search(r"det_%s: ell_ddm.py det exit \d+ \(want 0\), (\d+) s wall" % re.escape(lam), summ)
    print("| %s | %s | %s | %.10f | %.1e | %s | %s | %s | %s | %+d | %s | %s | %s |" % (
        lam, signs, r["dd_agree"], lns[0], max(lns) - min(lns), n24, ns.get(1e-20), ns.get(1e-16),
        "yes" if counts else "NO", int(r["f64_sign"]), m.group(1) if m else "?", lu.group(1) if lu else "?", wl.group(1) if wl else "?"))

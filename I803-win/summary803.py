#!/usr/bin/env python3
"""#803: #780's summary at D = 4. The largest phase change at the double count's points (dd0_D4.jsonl, from
i780_compare.py) within 1e-3 rad, and B0, U0 and FULL's windings over the light-cone block in double-double
(counts_dd0.jsonl) equal to I95's double counts of lowDn_D4.0000_M48 (1, 0, 0).
    python -I summary803.py FOLDER I95_COUNTS        exit 0 when every check holds"""
import json
import os
import sys

LIMIT = 1e-3
STATE = "lowDn_D4.0000_M48.npz"


def recs(p):
    return [json.loads(x) for x in open(p) if x.strip()]


def main(folder, i95):
    ok = True
    rs = [r for r in recs(os.path.join(folder, "dd0_D4.jsonl")) if r.get("kind") == "eval" and "dphase" in r]
    if not rs:
        print("no compared points")
        return 1
    w = max(rs, key=lambda r: abs(r["dphase"]))
    good = abs(w["dphase"]) <= LIMIT
    ok &= good
    print(f"D4: {len(rs)} points, largest |dphase| {abs(w['dphase']):.2e} rad at {w['lam']}, largest |d ln|det|| "
          f"{max(abs(r['dln']) for r in rs):.2e}: {'OK' if good else 'BAD'} (D 20.04: 3.4e-4, D 10: 3.9e-6, #780)")
    double = {r["box_name"]: r for r in recs(i95) if r.get("state") == STATE and r.get("mutate") is None and r.get("plant") is None}
    dd0 = {r["box_name"]: r for r in recs(os.path.join(folder, "counts_dd0.jsonl")) if r.get("state", STATE) == STATE}
    for box in ("B0", "U0", "FULL"):
        a, b = double.get(box), dd0.get(box)
        if not (a and b):
            print(f"   {box}: a count is missing")
            ok = False
            continue
        same = round(a["winding_g"]) == round(b["winding_g"]) and abs(b["winding_g"] - round(b["winding_g"])) < 1e-6
        ok &= same
        print(f"   {box:4s} winding: double {a['winding_g']:.13f}, light-cone block in double-double {b['winding_g']:.13f}: "
              f"{'equal' if same else 'DIFFER'}")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))

#!/usr/bin/env python3
"""Per-row table of two lemma6b1_cover_M.py run directories (rows 0..17, M = 5, --tag=_cert), win2's against macm3's.

    python rows_table_vs_macm3.py WIN2_RUNS MACM3_RUNS     markdown table; exit 0 if every disc of both runs is ok
                                                          and the two runs have the same discs per row, else 1
    python rows_table_vs_macm3.py --selftest               a planted failed disc in a copy of win2's rows is reported
                                                          (exit 1 inside); the selftest exits 1 if it is not

Columns: discs, Lohner steps, max Lambda and max box radius of each run, and the ratio win2 / macm3 of the box radii.
The box radius and Lambda are balls' upper bounds from FLINT's radius bookkeeping, so they may differ between builds
(AGENTS.md, #111); the discs' ok flags and counts are what the covering check uses.
"""
import json, os, sys


def load(d):
    rows = {}
    for j in range(18):
        p = os.path.join(d, f"row_{j:02d}.json")
        if os.path.exists(p):
            with open(p) as f:
                rows[j] = json.load(f)
    return rows


def table(a, b, out=print):
    out("| row | \\|u\\| | discs | steps win2 / macm3 | max Lam win2 | max Lam macm3 | max box radius win2 | "
        "max box radius macm3 | radius ratio | wall win2 |")
    out("|---|---|---|---|---|---|---|---|---|---|")
    bad = []
    for j in range(18):
        ra, rb = a.get(j), b.get(j)
        if ra is None or rb is None:
            out(f"| {j} | | | | | | | | | missing: win2 {ra is None}, macm3 {rb is None} |")
            bad.append(f"row {j} missing")
            continue
        da, db = ra["discs"], rb["discs"]
        la, lb = max(d["Lam"] for d in da), max(d["Lam"] for d in db)
        xa, xb = max(d["box_rad"] for d in da), max(d["box_rad"] for d in db)
        oka, okb = all(d["ok"] for d in da) and ra["ok"], all(d["ok"] for d in db) and rb["ok"]
        if not (oka and okb):
            bad.append(f"row {j} not ok (win2 {oka}, macm3 {okb})")
        if len(da) != len(db):
            bad.append(f"row {j} discs {len(da)} against {len(db)}")
        out(f"| {j} | {ra['rho']:.2f} | {len(da)}{'' if len(da) == len(db) else f' / {len(db)}'} | "
            f"{ra['steps']} / {rb['steps']} | {la:.3f} | {lb:.3f} | {xa:.1e} | {xb:.1e} | {xa / xb:.2f} | "
            f"{ra['sec']:.0f} s |")
    return bad


def selftest():
    import copy, tempfile
    a = load(sys.argv[2]) if len(sys.argv) > 2 else None
    if a is None:
        print("selftest needs WIN2_RUNS as the second argument"); return 1
    b = copy.deepcopy(a)
    lines = []
    clean = table(a, b, out=lines.append)
    b[3]["discs"][2]["ok"] = False
    planted = table(a, b, out=lambda s: None)
    ok = clean == [] and any("row 3 not ok" in s for s in planted)
    print("selftest", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    bad = table(load(sys.argv[1]), load(sys.argv[2]))
    print()
    print("verdict:", "every disc of both runs ok, same discs per row" if not bad else "; ".join(bad))
    sys.exit(1 if bad else 0)

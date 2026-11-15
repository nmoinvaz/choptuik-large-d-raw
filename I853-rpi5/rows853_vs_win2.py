#!/usr/bin/env python3
"""Per-row table of the Pi's lemma6b1 M=5 run against win2's stored one (I121-win2/lemma6b1_runs_M5_cert).

    python3 rows853_vs_win2.py PI_RUNS WIN2_RUNS

Per row: discs, Lohner steps, max Lam and max box radius of each run, the relative differences, the worst per-disc
relative difference of Lam and of box_rad, and whether every disc is ok in both. Exit 1 if any disc is not ok or the
disc or step counts differ. Rows with a relative difference above 1e-6 are listed after the table.
"""
import json, os, sys


def load(d):
    out = {}
    for j in range(18):
        with open(os.path.join(d, f"row_{j:02d}.json")) as f:
            out[j] = json.load(f)
    return out


def rel(a, b):
    return abs(a - b) / abs(b) if b else float("inf")


a, b = load(sys.argv[1]), load(sys.argv[2])
print("| row | \\|u\\| | discs | steps | max Lam Pi | max Lam win2 | rel diff | max box radius Pi | max box radius win2 | "
      "ratio Pi / win2 | worst disc rel diff Lam | worst disc ratio box radius | all ok |")
print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
bad, over = [], []
for j in range(18):
    ra, rb = a[j], b[j]
    da, db = ra["discs"], rb["discs"]
    same = len(da) == len(db) and ra["steps"] == rb["steps"]
    if not same:
        bad.append(f"row {j}: discs {len(da)} / {len(db)}, steps {ra['steps']} / {rb['steps']}")
    ok = ra["ok"] and rb["ok"] and all(d["ok"] for d in da) and all(d["ok"] for d in db)
    if not ok:
        bad.append(f"row {j}: not all ok")
    la, lb = max(d["Lam"] for d in da), max(d["Lam"] for d in db)
    xa, xb = max(d["box_rad"] for d in da), max(d["box_rad"] for d in db)
    wl = max((rel(x["Lam"], y["Lam"]) for x, y in zip(da, db)), default=0.0)
    ratios = [x["box_rad"] / y["box_rad"] for x, y in zip(da, db)]
    wr = max(ratios, key=lambda r: abs(r - 1)) if ratios else 1.0
    print(f"| {j} | {ra['rho']:.2f} | {len(da)}{'' if len(da) == len(db) else f' / {len(db)}'} | {ra['steps']}"
          f"{'' if ra['steps'] == rb['steps'] else f' / {rb['steps']}'} | {la:.4f} | {lb:.4f} | {rel(la, lb):.1e} | "
          f"{xa:.2e} | {xb:.2e} | {xa / xb:.3f} | {wl:.1e} | {wr:.3f} | {'yes' if ok else 'NO'} |")
    over.append((j, rel(la, lb), wl, xa / xb, wr))
print()
print("rows whose max Lam differs by more than 1e-6 relative:",
      ", ".join(f"{j} ({l:.1e})" for j, l, *_ in over if l > 1e-6) or "none", f"(worst {max(o[1] for o in over):.1e})")
print("rows with a disc whose Lam differs by more than 1e-6 relative:",
      ", ".join(f"{j} ({w:.1e})" for j, _, w, *_ in over if w > 1e-6) or "none", f"(worst of the others {max(o[2] for o in over if o[2] <= 1e-6):.1e})")
print(f"max box radius ratio Pi / win2 over the rows: {min(o[3] for o in over):.3f} to {max(o[3] for o in over):.3f}; "
      f"rows within 1e-6 of 1: {', '.join(str(o[0]) for o in over if abs(o[3] - 1) <= 1e-6) or 'none'}")
print("problems:", "; ".join(bad) if bad else "none")
sys.exit(1 if bad else 0)

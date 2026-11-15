#!/usr/bin/env python3
"""#873: the Pi's JSON outputs against the stored files of solver/proof/.

    python3 cmp873.py NEW_DIR STORED_PROOF_DIR STORED_RUNS_DIR

Per file pair: leaf by leaf, ignoring the timing keys. A ball string "[m +/- r]" is compared by its midpoint (printed
digits) and its radius (ratio); a float by relative difference; everything else (N, k, ok flags, booleans, other
strings) by equality. Then the covering rows, 12 rows against the stored ones, as a per-row table of discs, Lohner
steps, the largest Lam and box radius. Exit 1 when a non-numeric leaf, a ball midpoint, a count or a flag differs.
"""
import json, os, re, sys

BALL = re.compile(r"^\[\s*([-+0-9.eE]+)\s*\+/-\s*([-+0-9.eE]+)\s*\]$")
TIMEKEYS = {"sec", "time", "secs", "wall", "seconds"}
bad = []


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


def rel(a, b):
    return abs(a - b) / max(abs(a), abs(b), 1e-300)


def jsoncmp(a, b, name):
    A, B = dict(leaves(json.load(open(a)))), dict(leaves(json.load(open(b))))
    if A.keys() != B.keys():
        bad.append(f"{name}: structure differs")
        print(f"== {name}: structure differs ({len(A)} leaves against {len(B)}; only new: {sorted(set(A) - set(B))[:3]}, only stored: {sorted(set(B) - set(A))[:3]})")
        return
    nd, num, mids, rads, other = 0, {}, [], [], []
    for p in A:
        x, y = A[p], B[p]
        if x == y or key(p) in TIMEKEYS:
            continue
        nd += 1
        mx, my = (BALL.match(x) if isinstance(x, str) else None), (BALL.match(y) if isinstance(y, str) else None)
        if mx and my:
            if mx[1] != my[1]:
                mids.append((p, x, y))
                bad.append(f"{name}: ball midpoint {p} {x} against {y}")
            rads.append(float(mx[2]) / float(my[2]))
        elif isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool) and not isinstance(y, bool) \
                and key(p) not in ("N", "k", "steps", "n"):
            r = rel(x, y)
            if key(p) not in num or r > num[key(p)][0]:
                num[key(p)] = (r, x, y)
        else:
            other.append((p, x, y))
            bad.append(f"{name}: {p} {x} against {y}")
    print(f"== {name}: {len(A)} leaves, {nd} differ apart from timings: {len(mids)} ball midpoints, {len(other)} other non-numeric, "
          f"{len(num)} numeric keys, {len(rads)} ball radii" + (f" (ratio {min(rads):.3f} to {max(rads):.3f})" if rads else ""))
    for k, (r, x, y) in sorted(num.items(), key=lambda t: -t[1][0])[:6]:
        print(f"   {k:14s} worst relative difference {r:.2e} ({x} against {y})")
    for t in (mids + other)[:6]:
        print("   differs:", t)


def rows(new, old):
    print("| row | discs | steps | max Lam Pi | max Lam stored | rel diff | max box radius Pi | stored | ratio | all ok |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for j in range(12):
        pa, pb = os.path.join(new, f"row_{j:02d}.json"), os.path.join(old, f"row_{j:02d}.json")
        if not (os.path.exists(pa) and os.path.exists(pb)):
            print(f"| {j} | missing |"); bad.append(f"row {j} missing"); continue
        a, b = json.load(open(pa)), json.load(open(pb))
        da, db = a["discs"], b["discs"]
        same = len(da) == len(db) and a["steps"] == b["steps"]
        ok = a["ok"] and b["ok"] and all(d["ok"] for d in da) and all(d["ok"] for d in db)
        if not same:
            bad.append(f"row {j}: discs {len(da)}/{len(db)}, steps {a['steps']}/{b['steps']}")
        if not ok:
            bad.append(f"row {j}: not all ok")
        la, lb = max(d["Lam"] for d in da), max(d["Lam"] for d in db)
        xa, xb = max(d["box_rad"] for d in da), max(d["box_rad"] for d in db)
        print(f"| {j} | {len(da)}{'' if len(da) == len(db) else f' / {len(db)}'} | {a['steps']}"
              f"{'' if a['steps'] == b['steps'] else f' / {b['steps']}'} | {la:.6f} | {lb:.6f} | {rel(la, lb):.1e} | "
              f"{xa:.2e} | {xb:.2e} | {xa / xb:.3f} | {'yes' if ok else 'NO'} |")
    print()
    print("discs in all rows:", sum(len(json.load(open(os.path.join(new, f'row_{j:02d}.json')))['discs']) for j in range(12)
                                    if os.path.exists(os.path.join(new, f'row_{j:02d}.json'))))


new, proof, runs = sys.argv[1], sys.argv[2], sys.argv[3]
PAIRS = [("lemma6_sector_1e-9.json", "lemma6_sector_1e-9.json"), ("lemma6_path_point.json", "lemma6_path_point.json"),
         ("lemma6_path_box_1e-9.json", "lemma6_path_box_1e-9.json"), ("lemma6_jump_1e-9.json", "lemma6_jump_1e-9.json"),
         ("lemma6_jump_stored_box.json", "lemma6_jump_1e-9.json"), ("lemma6b1_check_1e-9.json", "lemma6b1_check_1e-9.json")]
for n, s in PAIRS:
    if os.path.exists(os.path.join(new, n)):
        jsoncmp(os.path.join(new, n), os.path.join(proof, s), f"{n} against {s}")
    else:
        print(f"== {n}: missing")
if os.path.isdir(os.path.join(new, "lemma6b1_runs_rpi5")):
    print()
    if os.path.exists(os.path.join(new, "lemma6b1_runs_rpi5", "ray.json")):
        jsoncmp(os.path.join(new, "lemma6b1_runs_rpi5", "ray.json"), os.path.join(runs, "ray.json"), "lemma6b1_runs ray.json")
    rows(os.path.join(new, "lemma6b1_runs_rpi5"), runs)
print("structural, midpoint, count or flag differences:", "; ".join(bad) if bad else "none")
sys.exit(1 if bad else 0)

"""#942: count the distinct results of each arm of run942.sh.

    python count942.py FOLDER [ARM ...]        (default arms: p a b c)

A result is a run's Delta (the last entry of each of the four parts, summed exactly) with its final |F|. A second count uses
the bits of the run's saved state (every entry of the four parts). The control run (ctl in arm a) is listed apart."""
import glob
import hashlib
import json
import os
import statistics
import sys
from fractions import Fraction

import numpy as np

# the Mac's two results as printed (#942): the parts of Delta are rounded to 7 digits, so a difference
# below about 1e-23 is not resolved here
MAC = {"mac common": [1.78498451800529434, 9.389859e-17, 3.600e-33], "mac odd (3rd part)": [1.78498451800529434, 9.389859e-17, -5.816e-33]}


def exact(parts):
    return sum(Fraction(x) for x in parts)


def read(path):
    with open(path) as f:
        return json.loads(f.readline())


def state_bits(path):
    if not os.path.exists(path):
        return None
    h = hashlib.sha256()
    with np.load(path, allow_pickle=True) as z:
        for k in sorted(z.files):
            if z[k].dtype.kind == "f":
                h.update(k.encode())
                h.update(np.ascontiguousarray(z[k]).tobytes())
    return h.hexdigest()[:12]


def runtime(log):
    for ln in open(log):
        if ln.startswith("time "):
            return float(ln.split()[1])
    return float("nan")


def load(folder, arm):
    out = []
    for p in sorted(glob.glob(os.path.join(folder, arm, "*.jsonl"))):
        n = os.path.basename(p)[:-6]
        r = read(p)
        r["name"] = n
        r["sbits"] = state_bits(os.path.join(folder, arm, n + ".npz"))
        r["wall"] = runtime(os.path.join(folder, arm, n + ".log"))
        out.append(r)
    return out


def klass(r):
    return (tuple(r["Delta_q"]), r["F"])


def show(title, rs, ref=None):
    print(f"\n== {title}: {len(rs)} runs, {sum(bool(r['conv']) for r in rs)} converged, steps {sorted({r['steps'] for r in rs})}, "
          f"wall {min(r['wall'] for r in rs):.0f}-{statistics.median(r['wall'] for r in rs):.0f}-{max(r['wall'] for r in rs):.0f} s "
          f"(min-median-max)")
    cl = {}
    for r in rs:
        cl.setdefault(klass(r), []).append(r)
    print(f"   distinct (Delta parts, |F|): {len(cl)}; distinct saved-state bits: {len({r['sbits'] for r in rs})}")
    ds = [exact(r["Delta_q"]) for r in rs]
    print(f"   spread of Delta (max - min, exact): {float(max(ds) - min(ds)):.3e}")
    base = exact(max(cl.items(), key=lambda kv: len(kv[1]))[0][0]) if ref is None else ref
    for k, v in sorted(cl.items(), key=lambda kv: -len(kv[1])):
        d = [f"{x:.17g}" for x in k[0]]
        print(f"   x{len(v):<3} |F| {k[1]:.3e}  Delta {d[0]} {k[0][1]:+.6e} {k[0][2]:+.3e} {k[0][3]:+.2e}  "
              f"minus ref {float(exact(k[0]) - base):+.3e}  state bits {sorted({r['sbits'] for r in v})}  {','.join(r['name'] for r in v[:6])}"
              + ("..." if len(v) > 6 else ""))
    return cl


def main():
    folder = sys.argv[1]
    arms = sys.argv[2:] or ["p", "a", "b", "c"]
    allr = {a: load(folder, a) for a in arms}
    ctl = [r for rs in allr.values() for r in rs if r["name"] == "ctl"]
    allr = {a: [r for r in rs if r["name"] != "ctl"] for a, rs in allr.items()}
    clss = {}
    for a in arms:
        if allr[a]:
            clss[a] = show(f"arm {a}", allr[a])
    every = [r for rs in allr.values() for r in rs]
    if every:
        print("\n== across arms (Delta parts, |F|):")
        keys = sorted({klass(r) for r in every}, key=lambda k: -sum(klass(r) == k for r in every))
        ref = exact(keys[0][0])
        for k in keys:
            n = {a: sum(klass(r) == k for r in allr[a]) for a in arms if allr[a]}
            print(f"   {n}  |F| {k[1]:.3e}  Delta minus ref {float(exact(k[0]) - ref):+.3e}  3rd {k[0][2]:+.3e} 4th {k[0][3]:+.2e}")
        print(f"   {len(keys)} distinct of {len(every)} runs; saved-state bits {len({r['sbits'] for r in every})} distinct")
        ma = klass(max(every, key=lambda r: sum(klass(x) == klass(r) for x in every)))
        for nm, parts in MAC.items():
            print(f"   most common here minus {nm}: {float(exact(ma[0]) - exact(parts)):+.3e} (Mac parts printed to 7 digits)")
    for r in ctl:
        ref = klass(max(allr["a"], key=lambda x: sum(klass(y) == klass(x) for y in allr["a"])))
        same = klass(r) == ref
        print(f"\n== control {r['name']}: |F| {r['F']:.3e}, Delta minus arm a's common {float(exact(r['Delta_q']) - exact(ref[0])):+.3e}, "
              f"steps {r['steps']}, state bits {r['sbits']} (arm a's: {sorted({x['sbits'] for x in allr['a']})}); "
              f"{'SAME as arm a (not counted as distinct)' if same else 'DISTINCT from arm a'} by (Delta, |F|)")


if __name__ == "__main__":
    main()

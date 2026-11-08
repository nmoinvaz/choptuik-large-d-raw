#!/usr/bin/env python3
"""Entry-by-entry diff of two lemma6_jump_M.py --save-B files (fields X and B, balls stored as [mid, rad] strings).

    python b_diff.py A.json B.json     prints the first differing entry, the largest |mid_a - mid_b| / max(rad_a, rad_b),
                                        the count of entries whose balls are disjoint, and the radius ratios
    python b_diff.py --selftest         a file against itself differs nowhere; one planted digit is found (exit 1 if not)
"""
import json, sys
from decimal import Decimal, getcontext

getcontext().prec = 200


def balls(obj, path=()):
    """yield (path, mid, rad) for every [mid, rad] pair of strings in obj"""
    if (isinstance(obj, list) and len(obj) == 2 and all(isinstance(s, str) for s in obj)):
        yield path, Decimal(obj[0]), Decimal(obj[1])
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            yield from balls(x, path + (i,))


def diff(a, b, out=print):
    first, worst, disjoint, n, rr = None, (Decimal(0), None), 0, 0, []
    for f in ("X", "B"):
        ea, eb = list(balls(a[f], (f,))), list(balls(b[f], (f,)))
        if [p for p, _, _ in ea] != [p for p, _, _ in eb]:
            out(f"field {f}: layouts differ ({len(ea)} against {len(eb)} balls)")
            return 2
        for (p, ma, ra), (_, mb, rb) in zip(ea, eb):
            n += 1
            if rb > 0:
                rr.append(ra / rb)
            if (ma, ra) != (mb, rb) and first is None:
                first = (p, ma, ra, mb, rb)
            d = abs(ma - mb)
            rel = d / max(ra, rb) if max(ra, rb) > 0 else (Decimal(0) if d == 0 else Decimal("Infinity"))
            if rel > worst[0]:
                worst = (rel, p)
            if d > ra + rb:
                disjoint += 1
    out(f"{n} balls compared (X then B)")
    if first is None:
        out("identical in every entry")
        return 0
    p, ma, ra, mb, rb = first
    out(f"first differing entry {p}: mid {ma:.25e} rad {ra:.6e} | mid {mb:.25e} rad {rb:.6e}")
    out(f"largest |mid_a - mid_b| / max(rad_a, rad_b) = {worst[0]:.3e} at {worst[1]}")
    out(f"disjoint balls: {disjoint}")
    if rr:
        rr.sort()
        out(f"rad_a / rad_b: min {rr[0]:.4f}, median {rr[len(rr) // 2]:.4f}, max {rr[-1]:.4f}")
    return 1


def selftest():
    src = {"X": [[["1.5", "1e-10"], ["2.5", "1e-10"]]], "B": [[[["3.25", "1e-8"], ["4.0", "2e-8"]]]]}
    ok = diff(src, src, out=lambda s: None) == 0
    bad = json.loads(json.dumps(src))
    bad["B"][0][0][1][0] = "4.1"
    lines = []
    ok &= diff(src, bad, out=lines.append) == 1 and any("('B', 0, 0, 1)" in s for s in lines)
    print("selftest", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    with open(sys.argv[1]) as fa, open(sys.argv[2]) as fb:
        rc = diff(json.load(fa), json.load(fb))
    sys.exit(0 if rc in (0, 1) else rc)

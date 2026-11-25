#!/usr/bin/env python3
"""#1076 fu022mp_corner_e (dh610) tile_cells.py PARENT.jsonl OUT.jsonl A,WF | selftest [--mutate=drop|shift]: the four quarters of the box in PARENT.jsonl (one line a0 a1 w0 w1) as the recount's cells
(ok false), with the midpoints (a0 + a1) / 2 and (w0 + w1) / 2 that argcount's own split uses (so the cached keys agree), in the order SW, NW, NE, SE. A,WF is the point without value; the quarter holding it as a vertex
must be exactly one and goes last. Checks, each able to fail: the four areas add to the parent's (1e-12 relative), the quarters' edges lie on three A values and three wf values (shared edges identical), exactly one quarter
has the point as a vertex. Exit 1 when a check fails. selftest: a planted parent; --mutate=drop drops a quarter (area), --mutate=shift moves one quarter's shared edge by 1e-6 (edges): each exits 1."""
import json, sys


def quarters(p):
    a0, a1, w0, w1 = p
    am, wm = (a0 + a1) / 2, (w0 + w1) / 2
    return {"SW": (a0, am, w0, wm), "SE": (am, a1, w0, wm), "NW": (a0, am, wm, w1), "NE": (am, a1, wm, w1)}


def verts(c):
    return {(c[0], c[2]), (c[1], c[2]), (c[1], c[3]), (c[0], c[3])}


def checks(p, ch, pt):
    area = sum((c[1] - c[0]) * (c[3] - c[2]) for c in ch.values())
    pa = (p[1] - p[0]) * (p[3] - p[2])
    As = {x for c in ch.values() for x in c[:2]}
    Ws = {x for c in ch.values() for x in c[2:]}
    holders = [n for n, c in ch.items() if pt in verts(c)]
    return dict(area=(len(ch) == 4 and abs(area - pa) <= 1e-12 * pa), edges=(len(As) == 3 and len(Ws) == 3),
                holder=(len(holders) == 1)), holders


def build(p, pt, mutate=None):
    ch = quarters(p)
    if mutate == "drop":
        del ch["NW"]
    if mutate == "shift":
        c = ch["NE"]
        ch["NE"] = (c[0] + 1e-6, c[1], c[2], c[3])
    return ch, checks(p, ch, pt)


def selftest(mutate):
    p, pt = (3.0, 4.0, 0.0, 0.5), (4.0, 0.0)
    ch, (res, holders) = build(p, pt, mutate)
    ok = all(res.values()) and holders == ["SE"]
    print("selftest" + (f" --mutate={mutate}" if mutate else ""), res, holders, "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        m = [a.split("=")[1] for a in sys.argv if a.startswith("--mutate=")]
        sys.exit(selftest(m[0] if m else None))
    src, out, pt = sys.argv[1], sys.argv[2], tuple(float(x) for x in sys.argv[3].split(","))
    d = [json.loads(l) for l in open(src) if l.strip()]
    assert len(d) == 1, "one parent box"
    p = (d[0]["a0"], d[0]["a1"], d[0]["w0"], d[0]["w1"])
    ch, (res, holders) = build(p, pt)
    print("parent", p, "point", pt, res, "holder", holders)
    if not all(res.values()) or len(holders) != 1:
        sys.exit(1)
    order = [n for n in ("SW", "NW", "NE", "SE") if n != holders[0]] + holders
    with open(out, "w") as fh:
        for n in order:
            c = ch[n]
            fh.write(json.dumps(dict(a0=c[0], a1=c[1], w0=c[2], w1=c[3], ok=False, note=f"{n} quarter of {list(p)}")) + "\n")
    print("wrote", out, order)

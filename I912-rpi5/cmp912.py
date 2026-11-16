#!/usr/bin/env python3
"""#912: the Pi's outputs against the Mac's I865-mac.  python3 -I cmp912.py PI_FOLDER MAC_FOLDER
JSON (s3.json, s5.json): every leaf; equal, differing float (relative difference), differing ball string "[m +/- r]"
(overlap by the exact interval test, radius ratio), or other. Logs: the Pi's log against the Mac's of the same run with the
trailing "exit N" line of the Mac's harness removed (m1box has no Mac log of the same run; m3box_prefix is the Mac's
box.log, the run before the fix)."""
import json, os, re, sys
import mpmath
mpmath.mp.dps = 100
PI, MAC = sys.argv[1], sys.argv[2]
BALL = re.compile(r"^\[\s*([-+0-9.eE]+)\s*\+/-\s*([-+0-9.eE]+)\s*\]$")
def leaves(x, p=""):
    if isinstance(x, dict):
        for k, v in x.items(): yield from leaves(v, p + "/" + k)
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from leaves(v, p + f"[{i}]")
    else:
        yield p, x
bad = []
for f in ("s3.json", "s5.json"):
    a, b = dict(leaves(json.load(open(f"{PI}/{f}")))), dict(leaves(json.load(open(f"{MAC}/{f}"))))
    print(f"## {f}: {len(a)} leaves (Mac {len(b)}), same keys {a.keys() == b.keys()}, byte-identical {open(f'{PI}/{f}','rb').read() == open(f'{MAC}/{f}','rb').read()}")
    if a.keys() != b.keys():
        bad.append(f"{f}: keys"); continue
    eq = sum(1 for k in a if a[k] == b[k])
    fl, bl, ot = [], [], []
    for k in a:
        if a[k] == b[k]: continue
        m1, m2 = (BALL.match(a[k]) if isinstance(a[k], str) else None), (BALL.match(b[k]) if isinstance(b[k], str) else None)
        if m1 and m2:
            x, y, r1, r2 = (mpmath.mpf(m1[1]), mpmath.mpf(m2[1]), mpmath.mpf(m1[2]), mpmath.mpf(m2[2]))
            bl.append((k, abs(x - y) <= r1 + r2, float(r1 / r2) if r2 else float("nan"), a[k], b[k]))
        elif isinstance(a[k], float) and isinstance(b[k], float):
            fl.append((k, abs(a[k] - b[k]) / max(abs(a[k]), abs(b[k]))))
        else:
            ot.append((k, a[k], b[k]))
    print(f"   equal leaves {eq}; differing float leaves {len(fl)}" + (f" (largest relative difference {max(r for _, r in fl):.2e} at {max(fl, key=lambda t: t[1])[0]}; families: {sorted(set(re.sub(r'\[\d+\]', '', k) for k, _ in fl))})" if fl else ""))
    print(f"   differing ball leaves {len(bl)}: " + ("; ".join(f"{k} {'overlap' if o else 'DISJOINT'} radius ratio {r:.3f} ({s} against {t})" for k, o, r, s, t in bl) if bl else "none"))
    print(f"   other differing leaves {len(ot)}: {ot[:6] if ot else 'none'}")
    bad += [f"{f}: disjoint ball {k}" for k, o, *_ in bl if not o] + [f"{f}: other leaf {k}" for k, *_ in ot]
print()
pairs = [("s3", "s3"), ("s5", "s5"), ("s1", "s1"), ("m3box", "m3box"), ("m5box", "m5box"), ("m5box9", "m5box9"), ("m3box_prefix", "box")]
for p, m in pairs:
    A = open(f"{PI}/{p}.log").read().splitlines()
    B = [l for l in open(f"{MAC}/{m}.log").read().splitlines() if not re.match(r"^exit \d+$", l)]
    same = A == B
    print(f"log {p}.log against {m}.log: {len(A)} lines, {'identical' if same else 'DIFFERENT'}")
    if not same: bad.append(f"{p}: log differs")
print("\ndifferences other than float noise of the f64 weights and ball radii:", "; ".join(bad) if bad else "none")

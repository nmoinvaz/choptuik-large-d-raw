"""#1084: value_point / value_v of the value_mp module in MODDIR, with each solve's trace (refreshes, skips and the
predicted shifts) printed to stderr; the row (as the CLI prints it) on stdout. The wrapper only passes trace=[].

    python drive.py MODDIR point A WF F3RE F3IM [--iters=12] [--floor=0|1]
    python drive.py MODDIR pointv A WF --M=5 --v=B3,C3,... [--iters=8] [--floor=0|1]
"""
import json
import sys

moddir = sys.argv[1]
sys.path.insert(0, moddir)
import mpmath as mpm  # noqa: E402
import value_mp as VM  # noqa: E402

assert VM.__file__.startswith(moddir.rstrip("/")), VM.__file__
args = [a for a in sys.argv[2:] if not a.startswith("--")]
opts = dict(a[2:].split("=", 1) for a in sys.argv[2:] if a.startswith("--") and "=" in a)
_solve = VM.solve


def solve(*a, **k):
    tr = []
    out = _solve(*a, trace=tr, **k)
    print(json.dumps(dict(dps=mpm.mp.dps, keep_J=k.get("keep_J"), calls=out[6],
                          trace=[[t[0]] + [None if x is None else mpm.nstr(x, 4) for x in t[1:]] for t in tr])),
          file=sys.stderr, flush=True)
    return out


VM.solve = solve
kw = dict(iters=int(opts.get("iters", 12)))
if "floor" in opts:
    kw["floor"] = opts["floor"] != "0"
if args[0] == "point":
    row = VM.value_point(args[1], args[2], args[3], args[4], **kw)
else:
    row = VM.value_v(args[1], args[2], opts["v"].split(","), int(opts["M"]), **kw)
print(json.dumps(row), flush=True)

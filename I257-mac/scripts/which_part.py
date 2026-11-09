"""#257: for each circle whose alias-rule replay needs new determinants (recheck.jsonl), whether the repeated
verification alone (alias 0, as edge() repeats it) already needs them, or only the alias rule does. No determinants.

    python3 which_part.py CODE_HP_DIR RECHECK.jsonl
"""
import json
import math
import sys

sys.path.insert(0, sys.argv[1])
import modecount_circle as C  # noqa: E402


class Missing(Exception):
    pass


seen = set()
for line in open(sys.argv[2]):
    r = json.loads(line)
    if r.get("verdict") != "needs new determinants":
        continue
    key = (r["cache"], tuple(r["center"]), r["R"])
    if key in seen:
        continue
    seen.add(key)
    v = {}
    for x in open(r["cache"]):
        x = json.loads(x)
        v[(x["re"], x["im"])] = (x["lnabs"], x["arg"])

    def det(lam):
        k = (float(lam.real), float(lam.imag))
        if k not in v:
            raise Missing(k)
        return v[k]
    try:
        rec = C.circle(det, complex(*r["center"]), r["R"], math.pi / 4, r["n0"], None, alias=0.0)
        part = f"repeated verification alone needs none ({rec['points']} points): the alias rule asks for them"
    except Missing as e:
        part = f"the repeated verification alone already needs one, at {e.args[0][0]:.6f} {e.args[0][1]:+.6f}i"
    print(f"{r['tag']} c {r['center']} R {r['R']}: {part}", flush=True)

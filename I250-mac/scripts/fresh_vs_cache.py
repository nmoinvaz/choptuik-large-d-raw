"""Build check of October's control (#250, criteria in ../README.md): det M recomputed fresh at cached points of
October's circle, on October's state, against October's cache.

    python fresh_vs_cache.py HP_DIR STATE.npz CACHE.jsonl OUT.json RE,IM [RE,IM ...] [--mutate=swap]

Passes when |ln|det| fresh - cached| <= 1e-8 and |arg fresh - cached| (wrapped) <= 1e-8 at every point. --mutate=swap
compares each fresh value with the next point's cache entry (the control, which must fail). Exit 0 on pass, 1 on fail.
"""
import json
import math
import sys

hp_dir, path, cache_path, out = sys.argv[1:5]
pts = [tuple(float(v) for v in a.split(",")) for a in sys.argv[5:] if not a.startswith("--")]
mutate = next((a.split("=", 1)[1] for a in sys.argv[5:] if a.startswith("--mutate=")), None)
sys.path.insert(0, hp_dir)
import modecount_common as mc  # noqa: E402

cache = {}
for line in open(cache_path):
    r = json.loads(line)
    cache[(r["re"], r["im"])] = r
st = mc.setup(path, M=None, kf=None, fmax=1e-15)
TOL = 1e-8
rows = []
for i, p in enumerate(pts):
    la, arg, pmin, pmax = st.det(p[0], p[1])
    ref = cache[pts[(i + 1) % len(pts)] if mutate == "swap" else p]
    d_ln, d_arg = abs(la - ref["lnabs"]), abs(math.remainder(arg - ref["arg"], 2 * math.pi))
    rows.append(dict(re=p[0], im=p[1], lnabs=la, arg=arg, cached_lnabs=ref["lnabs"], cached_arg=ref["arg"],
                     d_lnabs=d_ln, d_arg=d_arg))
    print(f"  {p}: fresh {la!r} {arg!r}; cached {ref['lnabs']!r} {ref['arg']!r}; diff {d_ln:.1e} {d_arg:.1e}",
          flush=True)
ok = all(r["d_lnabs"] <= TOL and r["d_arg"] <= TOL for r in rows)
json.dump(dict(state=path, cache=cache_path, mutate=mutate, tol=TOL, rows=rows, passed=ok), open(out, "w"), indent=1)
print(f"{'PASS' if ok else 'FAIL'} (mutate {mutate})", flush=True)
sys.exit(0 if ok else 1)

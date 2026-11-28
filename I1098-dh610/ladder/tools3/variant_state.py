"""A copy of a saved form-S state whose meta asks for another discretization (#1098's budget): steps2 (every Taylor
step halved), seg<i> (only segment i's steps halved), ks+N, kc+N, kt+N, ks=N, or mob<a> (the Moebius horizon with a,
keeping ks unless ks= or ks+ follows: mob16,ks=800). The state's values are kept; a solve from it (release_ls --harm 13,
whose inner held solves re-converge everything but harmonic 13 under the new discretization) gives Delta's change.

    python3 variant_state.py HP_DIR STATE OUT VARIANT[,VARIANT...]
"""
import sys

hp_dir, path, out, vars_ = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4].split(",")
sys.path.insert(0, hp_dir)
from octo_corrector import load_o, save_o  # noqa: E402


def halve(g):
    return [g[0]] + [v for a, b in zip(g[:-1], g[1:]) for v in (0.5 * (a + b), b)]


z8, meta = load_o(path)
m = dict(meta)
for var in vars_:
    if var == "steps2":
        m["segs"] = [halve(g) for g in m["segs"]]
    elif var.startswith("seg"):
        i = int(var[3:])
        m["segs"] = [halve(g) if j == i else g for j, g in enumerate(m["segs"])]
    elif var.startswith("mob"):
        m["hmob"] = float(var[3:])
    elif var.startswith("ks="):
        m["ks"] = int(var[3:])
    elif var != "base":
        name, n = var.split("+")
        m[name] = int(m.get(name, 36 if name == "kt" else 0)) + int(n)
m["variant"] = ",".join(vars_)
save_o(out, z8, m)
print(f"{m['variant']}: kt {m.get('kt', 36)}, kc {m['kc']}, ks {m['ks']}, mob {m.get('hmob', 0)}, "
      f"{sum(len(g) - 1 for g in m['segs'])} Taylor steps; saved {out}", flush=True)

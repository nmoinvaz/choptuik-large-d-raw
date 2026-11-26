"""A copy of a saved form-S state whose meta asks for another discretization (#1098's budget): steps2 (every Taylor
step halved), ks+N, kc+N or kt+N. The state's values are kept; a solve from it (release_ls --harm 13, whose inner
held solves re-converge everything but harmonic 13 under the new discretization) gives Delta's change.

    python3 variant_state.py STATE OUT VARIANT
"""
import sys

sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
from octo_corrector import load_o, save_o  # noqa: E402

path, out, var = sys.argv[1], sys.argv[2], sys.argv[3]
z8, meta = load_o(path)
m = dict(meta)
if var == "steps2":
    m["segs"] = [[g[0]] + [v for a, b in zip(g[:-1], g[1:]) for v in (0.5 * (a + b), b)] for g in meta["segs"]]
elif var != "base":
    name, n = var.split("+")
    m[name] = int(meta.get(name, 36 if name == "kt" else 0)) + int(n)
m["variant"] = var
save_o(out, z8, m)
print(f"{var}: kt {m.get('kt', 36)}, kc {m['kc']}, ks {m['ks']}, {sum(len(g) - 1 for g in m['segs'])} Taylor steps; "
      f"saved {out}", flush=True)

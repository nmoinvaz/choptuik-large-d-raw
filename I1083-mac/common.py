import json, os, sys, time
import numpy as np
WT = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a984952191346adc9/hp"
sys.path.insert(0, WT)
SC = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad"
ST = os.path.join(SC, "states")
OUT = os.path.join(SC, "mh")
STATES = {"low": os.path.join(ST, "D3.044375_M96.npz"), "hi": os.path.join(ST, "D3.15_M96.npz")}


def load_state(key):
    d = np.load(STATES[key])
    return d["zh"].copy(), d["zl"].copy(), json.loads(str(d["meta"]))


def solver(meta, threads=2, nodes=None, match_node=None):
    import tau_map
    s0, L = meta["map"]
    return tau_map.make_solver_mapped(meta["D"], meta["M"], s0, L, nodes=nodes or meta["nodes"], kt=meta.get("kt", 36),
                                      kc=meta.get("kc", 60), ks=meta.get("ks", 100), threads=threads,
                                      match_node=match_node)


def node(z, M, i):
    o = 2 * M + 4 * M * i
    return z[o:o + 4 * M]

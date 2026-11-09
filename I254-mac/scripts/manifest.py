"""The state lists of #254's sweeps, from an inventory of npz metas (scripts/inventory.py), duplicates (same bytes)
dropped and listed. Writes one list per group to I254-mac/lists/<group>.txt (absolute paths) and dups.txt.

    python3 manifest.py INVENTORY.json CODE_ROOT RAW_ROOT
"""
import hashlib
import json
import os
import sys

inv = json.load(open(sys.argv[1]))
code, raw = sys.argv[2], sys.argv[3]
out = os.path.join(raw, "I254-mac", "lists")
os.makedirs(out, exist_ok=True)


def h(p):
    return hashlib.sha1(open(p, "rb").read()).hexdigest()


groups = {
    # mode-count states at M >= 48 on the large-D layout (first node >= 0.1), raw folders
    "modecount": [r for r in inv if r["root"] == "raw" and r["M"] >= 48 and r["x0"] >= 0.1],
    # M >= 48 states with first node 0.01-0.02 (low D, D 4-15)
    "lowD_x002": [r for r in inv if r["M"] >= 48 and 0.01 <= r["x0"] < 0.1],
    # the states gamma_batch.py takes by default (hp/data/states, seeds, seeds/local), and the other seeds
    "gamma_own": [r for r in inv if r["root"] == "code" and r["path"].startswith(("hp/data/states/", "hp/data/seeds/"))],
    # hp/data's own M >= 48 mode-count states
    "modecount_code": [r for r in inv if r["root"] == "code" and r["path"].startswith("hp/data/modecount_state")
                       and r["M"] >= 48],
    # large-D M 32 states in hp/data/large_d (the up70 / T48 continuation)
    "large_d": [r for r in inv if r["root"] == "code" and r["path"].startswith("hp/data/large_d/")],
    # the chains that delta_all.csv cites (T138-win2 chain and chain_o, I19-win2 crawl) and T73's pinned states
    "chains": [r for r in inv if r["root"] == "raw" and r["M"] == 32 and r["path"].startswith(
        ("T138-win2/chain/", "T138-win2/chain_o/", "I19-win2/crawl/", "T73/t73/"))],
    # every low-D state with first node below 0.01 (outside the issue's scope; coverage only)
    "lowD_small": [r for r in inv if r["M"] >= 48 and r["x0"] < 0.01],
}
seen = {}
dups = []
for g, rows in groups.items():
    keep = []
    for r in sorted(rows, key=lambda r: r["path"]):
        p = os.path.join(code if r["root"] == "code" else raw, r["path"])
        k = h(p)
        if k in seen:
            dups.append(f"{p} = {seen[k]}")
            continue
        seen[k] = p
        keep.append(p)
    open(os.path.join(out, g + ".txt"), "w").write("\n".join(keep) + "\n")
    print(g, len(rows), "states,", len(keep), "after duplicates")
open(os.path.join(out, "dups.txt"), "w").write("\n".join(dups) + "\n")

"""Inventory of the npz states (meta only) of the code repository's hp/data and of the raw-data repository: path, root,
D, M, first and last node, K, kc, ks.

    python3 inventory.py CODE_ROOT RAW_ROOT OUT.json
"""
import json
import os
import sys

import numpy as np

out = []
for root_name, root, sub in (("code", sys.argv[1], "hp/data"), ("raw", sys.argv[2], "")):
    for dp, dn, fn in os.walk(os.path.join(root, sub)):
        dn[:] = [d for d in dn if d != ".git"]
        for f in fn:
            if not f.endswith(".npz"):
                continue
            p = os.path.join(dp, f)
            try:
                d = np.load(p)
                if "meta" not in d.files:
                    continue
                m = json.loads(str(d["meta"]))
            except Exception:
                continue
            if not isinstance(m, dict) or "M" not in m or "nodes" not in m:
                continue
            out.append(dict(root=root_name, path=os.path.relpath(p, root), D=m.get("D"), M=m["M"], x0=m["nodes"][0],
                            x1=m["nodes"][-1], K=len(m["nodes"]), kc=m.get("kc"), ks=m.get("ks"), F=m.get("F")))
json.dump(out, open(sys.argv[3], "w"), indent=0)
print(len(out), "states")

#!/usr/bin/env python3
"""planhash1064.py STATE.npz | --selftest [--break]: the sha256 of a state's stored plan (the meta's 'segs', as JSON with sorted nothing and repr floats) and its step count; the plan of a saved base is the plan its run used.
--selftest: equal plans give equal hashes, a plan changed in one node's last bit gives another; --break expects the changed plan to hash equal and must exit 1."""
import hashlib
import json
import sys

import numpy as np


def plan_hash(segs):
    s = json.dumps([[float(x) for x in sg] for sg in segs], separators=(",", ":"))
    return hashlib.sha256(s.encode()).hexdigest(), sum(len(sg) - 1 for sg in segs)


def selftest(brk):
    p = [[0.3, 0.31, 0.4], [0.4, 0.5]]
    q = [[0.3, 0.31, np.nextafter(0.4, 1)], [0.4, 0.5]]
    ok1 = plan_hash(p) == plan_hash([[0.3, 0.31, 0.4], [0.4, 0.5]])
    ok2 = (plan_hash(p)[0] != plan_hash(q)[0]) if not brk else (plan_hash(p)[0] == plan_hash(q)[0])
    print("  equal plans, equal hashes:", "ok" if ok1 else "WRONG")
    print("  one node's last bit changed, another hash:", "ok" if ok2 else "WRONG")
    print("selftest", "PASS" if ok1 and ok2 else "FAIL")
    return 0 if ok1 and ok2 else 1


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    z = np.load(sys.argv[1], allow_pickle=True)
    m = json.loads(str(z["meta"]))
    h, n = plan_hash(m["segs"])
    print(f"{h} {n} steps")

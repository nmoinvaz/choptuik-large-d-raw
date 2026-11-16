#!/usr/bin/env python3
"""#855: compare two .npz states key by key, the arrays bit for bit.

    python3 -I cmp_npz.py A.npz B.npz [A2.npz B2.npz ...]

Prints, per pair, the keys present in only one file, the arrays whose bytes differ (dtype, shape or content) and the
number of arrays identical. The key 'meta' (a JSON string with the run's source path and settings) is compared as text
and its differing fields are listed, since `cmp` fails on those alone. Exits 1 when any array other than 'meta' differs."""
import json
import sys

import numpy as np


def load(path):
    z = np.load(path, allow_pickle=False)
    return {k: z[k] for k in z.files}


def meta_diff(a, b):
    ma, mb = json.loads(str(a)), json.loads(str(b))
    keys = sorted(set(ma) | set(mb))
    return [k for k in keys if ma.get(k) != mb.get(k)]


args = sys.argv[1:]
if len(args) < 2 or len(args) % 2:
    sys.exit(__doc__)
bad = 0
for pa, pb in zip(args[::2], args[1::2]):
    a, b = load(pa), load(pb)
    only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
    same, diff = 0, []
    for k in sorted(set(a) & set(b)):
        if k == "meta":
            continue
        x, y = a[k], b[k]
        if x.dtype == y.dtype and x.shape == y.shape and x.tobytes() == y.tobytes():
            same += 1
        else:
            diff.append(k)
    print(f"{pa}\n{pb}\n  arrays identical {same}, differing {len(diff)} {diff}, only in A {only_a}, only in B {only_b}")
    if "meta" in a and "meta" in b:
        print(f"  meta fields that differ: {meta_diff(a['meta'], b['meta'])}")
    bad += len(diff) + len(only_a) + len(only_b)
sys.exit(1 if bad else 0)

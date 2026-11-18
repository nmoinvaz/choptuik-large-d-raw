#!/usr/bin/env python3
"""#954: word-for-word comparison of saved series.   python3 -I compare954.py A.npz B.npz [C.npz ...]   (each against the first)
Counts the 64-bit words that differ per file pair (and the keys missing); exit 1 when any word differs."""
import sys

import numpy as np

base = np.load(sys.argv[1], allow_pickle=False)
bad = 0
for p in sys.argv[2:]:
    o = np.load(p, allow_pickle=False)
    missing = set(base.files) ^ set(o.files)
    words = sum(int((base[k].view(np.uint64) != o[k].view(np.uint64)).sum()) for k in base.files if k in o.files)
    total = sum(base[k].size for k in base.files)
    print(f"{sys.argv[1]} against {p}: {words} of {total} words differ, {len(missing)} keys missing")
    bad += words + len(missing)
sys.exit(1 if bad else 0)

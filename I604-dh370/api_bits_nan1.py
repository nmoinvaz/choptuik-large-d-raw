#!/usr/bin/env python3
"""I523-mac/api_bits.py with every NaN hashed as one pattern (#600's reading of the sign bit of a NaN, which x86 writes
as 0xFFF8... and arm64 as 0x7FF8...). Same arguments as api_bits.py dump; the compare stays api_bits.py's.

    python3 api_bits_nan1.py dump HPDIR RAWDIR OUT.json [--perturb] [--only=lowd|large]

It imports the api_bits.py beside the I523-mac folder, replaces its digest, and prints the distinct NaN bit patterns it
replaced (count per pattern) so that the replacement is on record."""
import collections
import importlib.util
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("api_bits", os.path.join(HERE, "..", "I523-mac", "api_bits.py"))
ab = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ab)

CANON = np.float64("nan")
assert CANON.tobytes().hex() == "000000000000f87f", "canonical NaN must be 0x7FF8000000000000"
seen = collections.Counter()
orig = ab.digest


def digest(x):
    if isinstance(x, (list, tuple)):
        return [digest(v) for v in x]
    if isinstance(x, float):
        return orig(CANON if x != x else x)
    a = np.ascontiguousarray(np.asarray(x, dtype=np.float64)).copy()
    nan = np.isnan(a)
    if nan.any():
        for pat, c in zip(*np.unique(a[nan].view(np.uint64), return_counts=True)):
            seen[f"{int(pat):016x}"] += int(c)
        a[nan] = CANON
    return orig(a)


ab.digest = digest
if __name__ == "__main__":
    only = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--only=")), "")
    ab.dump(sys.argv[2], sys.argv[3], sys.argv[4], "--perturb" in sys.argv, only)
    print("NaN bit patterns replaced (pattern: count):", dict(seen))

#!/usr/bin/env python3
"""#854's acceptance that the default (keep_projected off) reproduces #839 A_s1's step 0 (both checks must pass, exit 0).

dz0 A.npz B.npz: planted --save_dz0's start and first step (z0..z7, d0..d7, eight parts each) of the code before #854
(4617f876) and after, the option off, compared bit for bit.
step0 A.log B.log: step 0's printed record, the trial lines, their projection lines and the step line, with the seconds
removed, compared as text. A_s1 wrote no JSON, so its printed record is the one there is.
Controls (each must fail): dz0 against the option's own dz0 (its start is the projection, its step has no
displacement); step0 --mutate=digit (one digit of B's step line changed).
usage: python3 cmp_854.py dz0 A.npz B.npz | step0 A.log B.log [--mutate=digit]"""
import re
import sys

import numpy as np


def dz0(a, b):
    A, B = np.load(a), np.load(b)
    keys = [f"{c}{q}" for c in "zd" for q in range(8)]
    bad = [k for k in keys if not (A[k].dtype == B[k].dtype and A[k].shape == B[k].shape
                                   and A[k].tobytes() == B[k].tobytes())]
    print(f"dz0 {a} against {b}: {len(keys) - len(bad)} of {len(keys)} arrays equal bit for bit"
          + (f"; differ: {bad}" if bad else "") + f": {'pass' if not bad else 'FAIL'}")
    return 0 if not bad else 1


SEC = re.compile(r",? [0-9.]+ s$")


def step0_lines(path):
    """step 0's printed record: its trial and projection lines, and its step line, without the seconds"""
    out = []
    for ln in open(path).read().splitlines():
        if ln.startswith("    on 0 trial ") or ln.startswith("      on 0, lam ") or ln.startswith("  on 0:"):
            out.append(SEC.sub("", ln))
    return out


def step0(a, b, mutate=""):
    A, B = step0_lines(a), step0_lines(b)
    if mutate == "digit" and B:
        last = B[-1]
        i = last.index("lam ") + 4         # the accepted lam's first digit
        B[-1] = last[:i] + ("9" if last[i] != "9" else "8") + last[i + 1:]
    same = A == B and len(A) > 0
    first = next((k for k, (x, y) in enumerate(zip(A, B)) if x != y), None)
    print(f"step0 {a} against {b}: {len(A)} and {len(B)} lines" + (f", the first difference at line {first}:\n  {A[first]}\n  "
                                                                  f"{B[first]}" if first is not None else "")
          + f": {'pass' if same else 'FAIL'}")
    return 0 if same else 1


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    mut = next((x.split("=", 1)[1] for x in sys.argv[1:] if x.startswith("--mutate=")), "")
    sys.exit(dz0(*args[1:3]) if args[0] == "dz0" else step0(*args[1:3], mutate=mut))

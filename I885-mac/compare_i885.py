#!/usr/bin/env python3
"""Compare the outputs of run_i885.sh with the stored files of the same name in solver/proof/ (#885).

    python3 compare_i885.py <output directory> <solver/proof>

Every file is compared leaf by leaf. A JSON file is one tree, a log of JSON records is a list of trees, and any other
line is a list of its numbers with the text around them. A new record or line is matched to the stored one that
agrees in every leaf that is not a number and is closest in the numbers. Wall times and the paths of the output
directory are dropped first. For b8m_lc_lip.json the entries are split at 1e-60: below it they are the rounding noise
of a secant slope (see the README)."""
import json
import os
import re
import sys

NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
TIME = re.compile(r"\[\s*[0-9.]+ s\]|\([0-9.]+ s\)|\b[0-9.]+ s\b")


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{p}[{i}]")
    else:
        yield p, o


def tree(line, out):
    """(numbers, everything else) of one record or line"""
    line = line.replace(out.rstrip("/") + "/", "")
    try:
        d = dict(leaves(json.loads(line)))
        num = {k: v for k, v in d.items() if isinstance(v, (int, float)) and not isinstance(v, bool) and
               not k.endswith(("/time", "/sec"))}
        rest = {k: v for k, v in d.items() if k not in num and not k.endswith(("/time", "/sec", "/h8log", "/jump",
                                                                                "/log", "/label"))}
        return num, json.dumps(rest, sort_keys=True)
    except (ValueError, TypeError):
        line = TIME.sub("", line)
        return dict(enumerate(float(x) for x in NUM.findall(line))), NUM.sub("#", line).strip()


def worst(a, b):
    ks = [k for k in a if k in b]
    if len(ks) != len(a) or len(a) != len(b):
        return None
    return max(((abs(a[k] - b[k]) / max(abs(a[k]), 1e-300), k) for k in ks), default=(0.0, ""), key=lambda t: t[0])


def units(path, out):
    txt = open(path).read()
    try:
        json.loads(txt)
        return [tree(txt, out)]
    except ValueError:
        return [tree(ln, out) for ln in txt.splitlines() if ln.strip()]


def main():
    out, proof = sys.argv[1], sys.argv[2]
    print("file | records or lines matched | largest relative difference of a number, and where")
    for name in sorted(os.listdir(out)):
        stored = os.path.join(proof, name)
        if name in ("exits.txt", "compare.txt") or not os.path.isfile(stored):
            continue
        if name == "b8m_lc_lip.json":
            A, B = json.load(open(stored))["M"], json.load(open(os.path.join(out, name)))["M"]
            lo, hi = [k for k in A if A[k] < 1e-60], [k for k in A if A[k] >= 1e-60]
            print(f"{name} | {len(A)} entries, same keys {sorted(A) == sorted(B)} | {len(hi)} entries of 1e-60 or "
                  f"more: {max(abs(B[k] / A[k] - 1) for k in hi):.1e}; {len(lo)} below it: "
                  f"{sum(abs(B[k] / A[k] - 1) > 1e-9 for k in lo)} move by more than 1e-9, by factors "
                  f"{min(B[k] / A[k] for k in lo):.3f} to {max(B[k] / A[k] for k in lo):.3f}")
            continue
        S, N = units(stored, out), units(os.path.join(out, name), out)
        res, miss = [], 0
        for num, rest in N:
            c = [w for w in (worst(sn, num) for sn, sr in S if sr == rest) if w is not None]
            if c:
                res.append(min(c, key=lambda t: t[0]))
            else:
                miss += 1
        w = max(res, key=lambda t: t[0]) if res else (0.0, "")
        print(f"{name} | {len(res)} of {len(N)} (the stored file has {len(S)}) | {w[0]:.1e}"
              + (f" at {str(w[1])[-40:]}" if w[0] > 1e-12 else ""))


if __name__ == "__main__":
    main()

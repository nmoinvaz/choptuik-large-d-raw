#!/usr/bin/env python3
"""Compare two sets of outputs of the B8 chain, file by file (#890).

    python3 compare_i890.py <new directory> <old directory> [--only=a.log,b.json]

For every file of the old directory that the new one has. A JSON file is one tree, a log of JSON records is a list of
trees matched in order, and any other file is compared line by line in order: the text with its numbers masked, then
the numbers. Wall times are dropped. Reported per file: the count of lines or records, the fields that only one side
has, the lines whose text differs, and the largest relative difference of a number with its place.
For b8m_lc_lip.json the entries at or below the new file's floor are counted apart."""
import json
import os
import re
import sys

NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
TIME = re.compile(r"\[\s*[0-9.]+ s\]|\([0-9.]+ s\)|\b[0-9.]+ s\b")
SKIP = ("/time", "/sec")


def leaves(o, p=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{p}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{p}[{i}]")
    else:
        yield p, o


def unit(line):
    """(kind, numbers, the rest) of a record or a line"""
    try:
        d = {k: v for k, v in leaves(json.loads(line)) if not k.endswith(SKIP)}
        num = {k: v for k, v in d.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
        return "json", num, {k: v for k, v in d.items() if k not in num}
    except (ValueError, TypeError):
        line = TIME.sub("", line)
        return "text", dict(enumerate(float(x) for x in NUM.findall(line))), NUM.sub("#", line).strip()


def units(path):
    txt = open(path).read()
    try:
        json.loads(txt)
        return [unit(txt)]
    except ValueError:
        return [unit(ln) for ln in txt.splitlines() if ln.strip()]


def rel(a, b):
    m = max(abs(a), abs(b))
    return abs(a - b) / m if m > 0 else 0.0


def main():
    new, old = sys.argv[1], sys.argv[2]
    only = next((a.split("=", 1)[1].split(",") for a in sys.argv[3:] if a.startswith("--only=")), None)
    print("file | lines or records, new and old | fields or text that differ | largest relative difference of a number")
    for name in sorted(os.listdir(old)):
        pn, po = os.path.join(new, name), os.path.join(old, name)
        if not os.path.isfile(pn) or (only and name not in only):
            continue
        if name == "b8m_lc_lip.json":
            dn, do = json.load(open(pn)), json.load(open(po))
            A, B, fl = do["M"], dn["M"], dn.get("floor", 0.0)
            up = [k for k in B if B[k] > fl]
            hp = max(rel(dn["hprime"][k], do["hprime"][k]) for k in do["hprime"])
            print(f"{name} | {len(B)} and {len(A)} entries | new fields {sorted(set(dn) - set(do))}; "
                  f"{len(B) - len(up)} entries at the floor {fl:g} (old values at most "
                  f"{max([A[k] for k in B if B[k] <= fl] or [0]):.1e}) | {len(up)} entries above it: "
                  f"{max(rel(A[k], B[k]) for k in up):.1e}; hprime {hp:.1e}")
            continue
        N, O = units(pn), units(po)
        worst, where, text, fields = 0.0, "", 0, set()
        for i, ((kn, nn, rn), (ko, no, ro)) in enumerate(zip(N, O)):
            if kn != ko:
                text += 1
                continue
            if kn == "json":
                fields |= {k for k in set(nn) ^ set(no)} | {k for k in set(rn) ^ set(ro)}
                text += sum(1 for k in rn if k in ro and rn[k] != ro[k] and not k.endswith(("/h8log", "/jump")))
            elif rn != ro or len(nn) != len(no):
                text += 1
                continue
            for k in nn:
                if k in no and rel(nn[k], no[k]) > worst:
                    worst, where = rel(nn[k], no[k]), f"record {i + 1} {k}" if kn == "json" else f"line {i + 1}"
        f = (f"{len(fields)} fields on one side only ({', '.join(sorted(fields)[:3])})" if fields else "") + \
            (f"{'; ' if fields else ''}{text} with other text" if text else "")
        print(f"{name} | {len(N)} and {len(O)} | {f or 'none'} | {worst:.1e}" + (f" at {where}" if worst > 1e-12 else ""))


if __name__ == "__main__":
    main()

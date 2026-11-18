#!/usr/bin/env python3
"""#960's default-bits pair: compares the files two anm_run.py runs wrote, bit for bit (array bytes, so non-finite
payloads count), their meta strings, and their jsonl records without the timing fields.

    python3 bits_cmp960.py DIR_A DIR_B          exit 0 when every file and record is identical, else 1
    python3 bits_cmp960.py --selftest           plants a one-ulp change in a copy, which must be reported (exit 1 on failure)
"""
import json
import os
import shutil
import sys
import tempfile

import numpy as np

TIMING = ("t_", "seconds", "wall", "time", "elapsed")


def strip(o):
    if isinstance(o, dict):
        return {k: strip(v) for k, v in o.items() if not any(k.startswith(t) or k == t for t in TIMING)}
    if isinstance(o, list):
        return [strip(v) for v in o]
    return o


def compare(a, b, out=print):
    bad = 0
    fa, fb = sorted(f for f in os.listdir(a) if f.endswith(".npz")), sorted(f for f in os.listdir(b) if f.endswith(".npz"))
    if fa != fb:
        out(f"npz file sets differ: only A {sorted(set(fa) - set(fb))}, only B {sorted(set(fb) - set(fa))}")
        bad += 1
    for f in sorted(set(fa) & set(fb)):
        da, db = np.load(os.path.join(a, f)), np.load(os.path.join(b, f))
        if sorted(da.keys()) != sorted(db.keys()):
            out(f"{f}: keys differ")
            bad += 1
            continue
        nd, nk = [], 0
        for k in sorted(da.keys()):
            x, y = da[k], db[k]
            same = (x.dtype == y.dtype and x.shape == y.shape and x.tobytes() == y.tobytes())
            nk += 1
            if not same:
                nd.append(k)
        if nd:
            bad += 1
            out(f"{f}: DIFFER in {len(nd)} of {nk} arrays: {nd[:8]}")
            for k in nd[:3]:
                x, y = da[k], db[k]
                if x.dtype.kind == "f" and x.shape == y.shape:
                    d = np.abs(x - y)
                    out(f"    {k}: max|diff| {np.nanmax(d):.3e}, differing entries {int(np.sum(x.view(np.uint64) != y.view(np.uint64)))} of {x.size}")
        else:
            out(f"{f}: identical ({nk} arrays)")
    ja, jb = os.path.join(a, "anm_run.jsonl"), os.path.join(b, "anm_run.jsonl")
    if os.path.exists(ja) and os.path.exists(jb):
        ra = [strip(json.loads(x)) for x in open(ja) if x.strip()]
        rb = [strip(json.loads(x)) for x in open(jb) if x.strip()]
        if ra == rb:
            out(f"anm_run.jsonl: {len(ra)} records identical without timing fields")
        else:
            bad += 1
            out(f"anm_run.jsonl: records DIFFER ({len(ra)} against {len(rb)})")
            for i, (p, q) in enumerate(zip(ra, rb)):
                if p != q:
                    ks = [k for k in set(p) | set(q) if p.get(k) != q.get(k)]
                    out(f"    record {i}: keys {sorted(ks)}")
    else:
        bad += 1
        out("anm_run.jsonl missing in one directory")
    return bad


def selftest():
    a = sys.argv[2] if len(sys.argv) > 2 else None
    t = tempfile.mkdtemp()
    A, B = os.path.join(t, "A"), os.path.join(t, "B")
    os.makedirs(A)
    z = np.linspace(1.0, 2.0, 7)
    np.savez(os.path.join(A, "s.npz"), zh=z, meta=np.array("{}"))
    json.dump(dict(a=1.0, t_coef=5.0, attempts=[dict(F=1.0, t_corr=2.0)]), open(os.path.join(A, "anm_run.jsonl"), "w"))
    shutil.copytree(A, B)
    lines = []
    ok = compare(A, B, lines.append) == 0                   # identical copies pass (timing fields may differ)
    r = json.load(open(os.path.join(B, "anm_run.jsonl")))
    r["t_coef"], r["attempts"][0]["t_corr"] = 9.0, 8.0
    json.dump(r, open(os.path.join(B, "anm_run.jsonl"), "w"))
    ok = ok and compare(A, B, lines.append) == 0
    z2 = z.copy()
    z2.view(np.uint64)[3] += 1                              # one ulp
    np.savez(os.path.join(B, "s.npz"), zh=z2, meta=np.array("{}"))
    ok = ok and compare(A, B, lines.append) == 1            # the planted ulp must be reported
    r["attempts"][0]["F"] = 1.0000001
    json.dump(r, open(os.path.join(B, "anm_run.jsonl"), "w"))
    shutil.copy(os.path.join(A, "s.npz"), os.path.join(B, "s.npz"))
    ok = ok and compare(A, B, lines.append) == 1            # a changed record value must be reported
    print("\n".join(lines))
    print("selftest:", "pass" if ok else "FAIL")
    shutil.rmtree(t)
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    sys.exit(1 if compare(sys.argv[1], sys.argv[2]) else 0)

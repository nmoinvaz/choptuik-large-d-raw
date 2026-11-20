"""#1013 recount3, before the run: is step 2's xi1 0.18 cache on the sheet of the sheetfix's xi1 0.17 cache?
    python3 sheet_precheck.py POINTS_0.17 POINTS_0.18 [--quiet]      lists the valued 0.18 points that are off the sheet (exit 1 if any)
    python3 sheet_precheck.py POINTS_0.17 POINTS_0.18 --mutate       control: one valued 0.18 point's F3 shifted by 0.3 must add
                                                                     exactly one point to the off-sheet list (exit 0 when it does)
On one root (sheet) of S3 = 0, F3 does not depend on xi1 (xfchecks' sheet check). So a valued 0.18 point and a valued 0.17 point at
the same (A, w/w_inf) have the same F3. The sheetfix's 0.17 cache is on one sheet (|dF3| < 0.1 between adjacent valued points,
xfchecks, #1013 comment 7034829136); a 0.18 point without a 0.17 twin is compared with its nearest valued 0.17 point. |dF3| > 0.1 is off
the sheet (xfchecks' bound). Valued = argcount's `valued3`: info < 1e-8 or the continuation's fix.ok."""
import json, math, sys

V = lambda r: (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))
key = lambda r: (round(r["A"], 7), round(r["wf"], 8))


def off_sheet(p17, p18, shift_index=None, quiet=False):
    """-> (indices into p18 of the off-sheet valued points, number compared)"""
    ref = {key(r): complex(r["F3re"], r["F3im"]) for r in p17 if V(r) and math.isfinite(r["F3re"])}
    bad, n = [], 0
    for i, r in enumerate(p18):
        if not (V(r) and math.isfinite(r["F3re"])):
            continue
        n += 1
        f = complex(r["F3re"], r["F3im"]) + (0.3 if i == shift_index else 0.0)
        k = key(r)
        if k in ref:
            d, why = abs(f - ref[k]), "same point at 0.17"
        else:
            kk = min(ref, key=lambda q: (q[0] - k[0]) ** 2 + (q[1] - k[1]) ** 2)
            d, why = abs(f - ref[kk]), f"nearest 0.17 valued point {kk}"
        if d > 0.1:
            bad.append(i)
        if not quiet:
            print(f"{'OFF ' if d > 0.1 else 'ok  '} line {i + 1:3d} A {k[0]:.7f} wf {k[1]:.8f} F3 {f.real:+.4f}{f.imag:+.4f}i  {why}: |dF3| {d:.4f}")
    return bad, n


if __name__ == "__main__":
    p17 = [json.loads(l) for l in open(sys.argv[1])]
    p18 = [json.loads(l) for l in open(sys.argv[2])]
    if "--mutate" in sys.argv:
        base, _ = off_sheet(p17, p18, quiet=True)
        i = next(j for j, r in enumerate(p18) if V(r) and math.isfinite(r["F3re"]) and j not in base)
        mut, _ = off_sheet(p17, p18, shift_index=i, quiet=True)
        print(f"control: off-sheet points {len(base)} -> {len(mut)} when line {i + 1}'s F3 is shifted by 0.3 (must rise by one)")
        sys.exit(0 if len(mut) == len(base) + 1 else 1)
    bad, n = off_sheet(p17, p18, quiet="--quiet" in sys.argv)
    print(f"{len(p18)} records at 0.18; {n} valued compared; off the sheet: {len(bad)}")
    sys.exit(1 if bad else 0)

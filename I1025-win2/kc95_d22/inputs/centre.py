#!/usr/bin/env python3
"""centre.py ROOTS87.txt D | --selftest [--mutate]: the scan centre of the k_c 95 regrid lanes (#1025 kc95_d22, kc95_d225; the coordinator's hc of 2026-11-24 ~17:25 UTC):
lambda = (macm3's k_c 87 root at that D + 0.003) rounded to 0.005, scanned +-0.01 by 0.005, plus a repeat of the centre; the prediction is root + 0.003 (bar 0.005).
ROOTS87.txt is macm3's I1025-macm3/kc87_leg_lambda/roots87.txt (rows `D root lo hi source ...`, `#` comments). Prints `PRED CENTRE ROOT` (PRED to 4 decimals, CENTRE to 3), exit 0;
exit 2 when the file has no row for D (the root is not published yet); exit 3 when it has two rows for D that differ.
--selftest: planted rows (21.75 -> root 0.646846 -> prediction 0.6498, centre 0.650; a root on a rounding edge; a missing D exit 2; two different rows exit 3) must read as written;
--mutate adds 0.03 to the offset, which the planted cases must then catch (exit 1)."""
import sys

OFFSET = 0.003 + (0.03 if "--mutate" in sys.argv else 0.0)


def read_root(text, D):
    rows = []
    for l in text.splitlines():
        t = l.split()
        if not t or t[0].startswith("#"):
            continue
        try:
            if abs(float(t[0]) - D) < 1e-9:
                rows.append(float(t[1]))
        except ValueError:
            continue
    if not rows:
        return None
    if max(rows) - min(rows) > 1e-9:
        raise ValueError("two rows for D %g that differ: %s" % (D, rows))
    return rows[-1]


def centre(root):
    pred = root + OFFSET
    return pred, round(round(pred / 0.005) * 0.005, 3)


def selftest():
    bad = []
    txt = "# D root lo hi source\n21.625 0.696157 0.695767 0.696157 macm3 bracket 0.695 0.700\n21.75 0.646846 0.646292 0.646846 macm3 bracket 0.645 0.650\n22.0 0.60 0.6 0.6 x\n22.0 0.6 0.6 0.6 x\n"
    r = read_root(txt, 21.75)
    p, c = centre(r)
    if abs(p - 0.649846) > 1e-9 or c != 0.650:
        bad.append("21.75: pred %r centre %r" % (p, c))
    p, c = centre(0.6418)   # 0.6448 -> 0.645
    if c != 0.645:
        bad.append("0.6418: centre %r" % c)
    p, c = centre(0.6525)   # 0.6555 -> 0.655
    if c != 0.655:
        bad.append("0.6525: centre %r" % c)
    if read_root(txt, 22.5) is not None:
        bad.append("22.5 should be missing")
    if read_root(txt, 22.0) != 0.6:
        bad.append("22.0 duplicate rows that agree")
    try:
        read_root(txt + "22.0 0.61 0.6 0.6 x\n", 22.0)
        bad.append("differing duplicate rows not refused")
    except ValueError:
        pass
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--selftest" in sys.argv:
        return selftest()
    try:
        root = read_root(open(a[0]).read(), float(a[1]))
    except ValueError as e:
        print(e)
        return 3
    if root is None:
        return 2
    p, c = centre(root)
    print("%.4f %.3f %.6f" % (p, c, root))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""#785: v_1's share of the pinned first step's squared norm, (v_1^T dz)^2 / |dz|^2, from uf688.py logs' "pinned step"
line (norm, then V^T dz, the first entry v_1's), and the 0.975 run against #688's log.
    python3 share785.py LOG [LOG ...] [--ref688 LOG688]
    python3 share785.py --selftest
For each log: sigma_1, u_1^T r, the pinned step's norm, v_1^T dz and the share. With --ref688, sigma_1 and u_1^T r of the
first log against #688's to 1e-5 relative (another build, and the logs print 6 digits, one unit of which is up to
2e-6 relative); exit 1 when either differs by more."""
import re
import sys

PIN = re.compile(r"pinned step: max ([0-9.eE+-]+), norm ([0-9.eE+-]+), Delta [0-9.eE+-]+; V\^T dz ((?:[+-][0-9.eE+-]+ ?)+)")
SIG = re.compile(r"\|\|J v_1\|\| ([0-9.eE+-]+)")
UTR = re.compile(r"u_1\^T r = ([0-9.eE+-]+)")


def read(path):
    s = open(path, encoding="utf-8", errors="replace").read()
    p, g, u = PIN.search(s), SIG.search(s), UTR.search(s)
    if not (p and g and u):
        return None
    vt = [float(x) for x in p.group(3).split()]
    norm = float(p.group(2))
    return dict(sigma1=float(g.group(1)), utr=float(u.group(1)), norm=norm, v1=vt[0], share=vt[0] ** 2 / norm ** 2)


def main(argv):
    logs = [a for a in argv if not a.startswith("--") and (argv.index(a) == 0 or argv[argv.index(a) - 1] != "--ref688")]
    ok = True
    print("| log | sigma_1 | u_1^T r | pinned step norm | v_1^T dz | share (v_1^T dz)^2 / norm^2 |\n|---|---|---|---|---|---|")
    recs = []
    for path in logs:
        r = read(path)
        recs.append(r)
        if r is None:
            print(f"| {path} | no pinned step line | | | | |")
            ok = False
            continue
        print(f"| {path.rsplit('/', 1)[-1]} | {r['sigma1']:.6e} | {r['utr']:.6e} | {r['norm']:.4e} | {r['v1']:+.4e} | {r['share']:.4f} |")
    if "--ref688" in argv:
        ref = read(argv[argv.index("--ref688") + 1])
        a = recs[0]
        if ref is None or a is None:
            print("ref688: a log could not be read")
            return 1
        ds, du = abs(a["sigma1"] / ref["sigma1"] - 1), abs(a["utr"] / ref["utr"] - 1)
        good = ds <= 1e-5 and du <= 1e-5
        ok &= good
        print(f"\nagainst #688: sigma_1 {ref['sigma1']:.6e} (relative {ds:.1e}), u_1^T r {ref['utr']:.6e} (relative {du:.1e}): "
              f"{'within 1e-5' if good else 'NOT within 1e-5'}; #688's share {ref['share']:.4f}")
    return 0 if ok else 1


def selftest():
    line = ("  pinned step: max 2.139e-02, norm 1.923e-01, Delta +7.114e-03; V^T dz -1.86e-01 +3.19e-02 +3.73e-02 +5.19e-03; "
            "sigma 4.674e-40")
    m = PIN.search(line)
    vt = [float(x) for x in m.group(3).split()] if m else []
    share = vt[0] ** 2 / float(m.group(2)) ** 2 if m else None
    ok = m is not None and len(vt) == 4 and abs(share - 0.9355) < 1e-3
    print(f"  #688's line: share {share:.4f} (expected 0.9355, #688's 94%) {'ok' if ok else 'WRONG'}")
    print("selftest", "passed" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))

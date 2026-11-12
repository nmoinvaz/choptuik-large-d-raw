#!/usr/bin/env python3
"""#522: the chirp fit's period at the centres of the two halves against the periods fitted to each half alone.
usage: python centres_522.py        (run from I522-win2; reads results_chirp_522_with_half_units.txt, results_halfunit_522.txt and ../I521-win2/results_521.txt)
Chirp: P(D) = P0 + p1 (D - 228) at the centre of the low half (12 unit states D 216.13 to 227.13, centre 221.63) and of the high half (D 228.13 to 237.13, centre 232.63).
The half periods are the quadratic + sinusoid fits: low from results_halfunit_522.txt (23 states, half-unit spacing), high from results_521.txt (D 228 to 237).
Exits 1 if a chirp period at a centre differs from the half's own fitted period by more than 0.05.
--mutate=p1zero: the drift is set to 0 (a constant period P0), which must exit 1."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LO_C, HI_C = (216.1312 + 227.1312) / 2, (228.1312 + 237.1312) / 2
tol = 0.05


def chirp():
    out = {}
    for ln in open(os.path.join(HERE, "results_chirp_522_with_half_units.txt"), encoding="utf-8"):
        m = re.match(r"\s+ln sigma_(\d): P0 = ([\d.]+) at D 228, drift p1 = ([+-][\d.]+)", ln)
        if m:
            out[int(m.group(1))] = (float(m.group(2)), float(m.group(3)))
    return out


def low():
    out = {}
    for ln in open(os.path.join(HERE, "results_halfunit_522.txt"), encoding="utf-8"):
        m = re.match(r"\s+ln sigma_(\d) \(c\) quadratic \+ sinusoid: N \d+, P = ([\d.]+)", ln)
        if m:
            out[int(m.group(1))] = float(m.group(2))
    return out


def high():
    out = {}
    sec = False
    for ln in open(os.path.join(HERE, "..", "I521-win2", "results_521.txt"), encoding="utf-8"):
        if ln.startswith("high"):
            sec = True
        elif ln.startswith("all"):
            sec = False
        m = re.match(r"\s+ln sigma_(\d) \(c\) quadratic \+ sinusoid: N \d+, P = ([\d.]+)", ln)
        if sec and m:
            out[int(m.group(1))] = float(m.group(2))
    return out


if __name__ == "__main__":
    c, lo, hi = chirp(), low(), high()
    assert len(c) == 4 and len(lo) == 4 and len(hi) == 4, (c, lo, hi)
    bad = 0
    print("| series | chirp P at D 221.63 | low half fitted | chirp P at D 232.63 | high half fitted |")
    print("|---|---|---|---|---|")
    for i in (1, 2, 3, 4):
        P0, p1 = c[i]
        if "--mutate=p1zero" in sys.argv:
            p1 = 0.0
        a, b = P0 + p1 * (LO_C - 228), P0 + p1 * (HI_C - 228)
        bad += abs(a - lo[i]) > tol or abs(b - hi[i]) > tol
        print(f"| sigma_{i} | {a:.3f} | {lo[i]:.3f} | {b:.3f} | {hi[i]:.3f} |")
    print("check: pass" if not bad else f"check: FAIL ({bad} series differ by more than {tol})")
    sys.exit(1 if bad else 0)

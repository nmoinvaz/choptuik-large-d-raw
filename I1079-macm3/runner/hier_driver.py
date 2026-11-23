"""#1079 macm3b: run main's hier.py (unchanged) with the same arguments, and print the final x and r at full precision (hier.report prints A and w/w_inf to 9 decimals and F_3/F_1 to 6).
    python -u hier_driver.py M A wf [hier.py's options]
It imports hier from main's worktree, wraps hier.report (printing repr of x and r first, then calling the original), and calls hier.main(). Nothing else is changed.
The guard matters: hier's spawn workers import this file as __main__."""
import sys
HIER_DIR = "/Users/nathan/Source/choptuik-large-d-1079/solver/inner_stokes"
if HIER_DIR not in sys.path:
    sys.path.insert(0, HIER_DIR)
import hier as H

_orig = H.report


def _report(x, r, M, tag):
    print("FULL x (A, w/w_inf, B3, C3, ...) = " + repr([float(t) for t in x]), flush=True)
    print("FULL r = " + repr([float(t) for t in r]), flush=True)
    return _orig(x, r, M, tag)


H.report = _report

if __name__ == "__main__":
    sys.argv = ["hier.py"] + sys.argv[1:]
    H.main()

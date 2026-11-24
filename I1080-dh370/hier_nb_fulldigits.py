"""#1080: hier_nb.py with the solved x printed in full digits (hier.report prints 9; main's hier.main returns nothing).

    cd solver/inner_stokes && python -u hier_nb_fulldigits.py <hier_nb.py's arguments>

The same code path as hier_nb.py (its main(), unchanged); only hier.report is wrapped: after the normal report it prints
'FULLDIGITS x = [A, w, B3, C3, ..., BM, CM]' with repr() of each float64 (and writes them to --fulldigits-out=PATH if given as an environment variable
FULLDIGITS_OUT). Spawned workers import this file as __mp_main__ and need nothing of it (the guard below)."""
import json
import os
import sys

sys.path.insert(0, os.getcwd())
import hier                                                   # noqa: E402
import hier_nb                                                # noqa: E402


def main():
    orig = hier.report

    def report(x, r, M, *a, **k):
        out = orig(x, r, M, *a, **k)
        xs = [float(v) for v in x]
        print("FULLDIGITS x = " + json.dumps(xs), flush=True)
        if os.environ.get("FULLDIGITS_OUT"):
            open(os.environ["FULLDIGITS_OUT"], "w").write(json.dumps(xs) + "\n")
        return out

    hier.report = report
    hier_nb.main()


if __name__ == "__main__":
    main()

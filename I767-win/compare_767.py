#!/usr/bin/env python3
"""#767: the laptop's K 15, J 1500, 1280-bit sigma files at wf 1.09 and 1.11 against win2's K 45 files of #82, sigma_0..7.
    python -I compare_767.py FOLDER REFS     (FOLDER: I767-win; REFS: the folder with K45_w1.09.json, K45_w1.10.json and
                                             K45_w1.11.json, copies of I82-win2/sigF_w<wf>_K45_J1500_p1280.json)
    python -I compare_767.py --selftest
Each pair passes when sigma_str (20 digits, real and imaginary) is equal at n = 0..7; otherwise the first differing n is
named. Control: the 1.09 K 15 file against the 1.10 K 45 file must differ. Exit 0 when both pairs pass and the control
differs."""
import json
import os
import sys

N_MAX = 7


def first_diff(a, b, n_max=N_MAX):
    """the first n <= n_max at which the sigma strings differ, or None"""
    for n in range(n_max + 1):
        if n >= len(a) or n >= len(b) or a[n] != b[n]:
            return n
    return None


def main(folder, refs):
    ok = True
    print("| wf | file | reference | first differing n (0..7) | verdict |\n|---|---|---|---|---|")
    new = {w: json.load(open(os.path.join(folder, f"sigF_w{w}_K15_J1500_p1280.json"))) for w in ("1.09", "1.11")}
    for w, ref in (("1.09", "1.09"), ("1.11", "1.11"), ("1.09", "1.10")):
        r = json.load(open(os.path.join(refs, f"K45_w{ref}.json")))
        n = first_diff(new[w]["sigma_str"], r["sigma_str"])
        control = w != ref
        good = (n is not None) if control else (n is None)
        ok &= good
        print(f"| {w} | K 15, procs {new[w]['procs']} | K 45 at {ref}, procs {r['procs']}{' (control)' if control else ''} | "
              f"{'none' if n is None else n} | {'pass' if good else 'FAIL'} |")
    print("PASS" if ok else "FAIL")
    return 0 if ok else 1


def selftest():
    a = [["1.0", "0.0"], ["0.80574692525712709388", "0.48568936920179601896"]] + [["0.1", "0.2"]] * 6
    b = [x[:] for x in a]
    b[3] = ["0.1", "0.20000000000000000001"]
    cases = [("equal strings", first_diff(a, a), None), ("one digit of sigma_3", first_diff(a, b), 3),
             ("a file short of order 7", first_diff(a, a[:5]), 5)]
    bad = 0
    for label, got, want in cases:
        print(f"  {label}: {got} (expected {want}) {'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], sys.argv[2]))

#!/usr/bin/env python3
"""I202-win2: win2's amplitude node at omega/omega_inf 1.10, K 33, J 1000, against macm3's T153 file (issue #202).

    python compare_202.py [WIN2.json [MACM3.json]]
        defaults: ./sigF_w1.10_K33_J1000.json and ../T153-macm3/sigF_w1.10_K33_J1000.json.
        Compares the two after dropping the timing keys (I140-win2/compare.py's rule) and `procs` (win2 ran 3 processes and
        macm3 2; the result must not depend on it). Exit 0: bit for bit equal. Exit 1: the first differing entry is printed,
        and for the sigma strings the first differing sigma index with both strings.
    python compare_202.py --selftest
        a file against itself is equal, a different `procs` alone is ignored, one planted digit in one sigma string is
        found at its index (exit 1 inside if any of the three fails)."""
import copy, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "I140-win2"))
import compare as C


def load(path):
    obj, _, _ = C.canon(path)
    obj.pop("procs", None)
    return obj


def report(a, b, out=print):
    d = C.first_diff(a, b)
    if d is None:
        out("bit for bit equal (timing keys and procs dropped)")
        return 0
    path, va, vb = d
    out(f"first differing entry: {path}\n  win2   {va}\n  macm3  {vb}")
    if path.startswith("/sigma_str["):
        i = int(path.split("[")[1].split("]")[0])
        out(f"  the first differing sigma string is sigma_{i}: win2 {a['sigma_str'][i]} / macm3 {b['sigma_str'][i]}")
    return 1


def selftest():
    p = os.path.join(os.path.dirname(HERE), "T153-macm3", "sigF_w1.10_K33_J1000.json")
    a = load(p)
    ok = report(a, copy.deepcopy(a), out=lambda s: None) == 0
    import tempfile
    c = json.load(open(p)); c["procs"] = 7; c["seconds"] = 1.0
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(c, fh)
    try:
        ok &= report(a, load(fh.name), out=lambda s: None) == 0
    finally:
        os.remove(fh.name)
    e = copy.deepcopy(a)
    s = e["sigma_str"][9]
    e["sigma_str"][9] = [s[0], s[1][:-3] + ("0" if s[1][-3] != "0" else "1") + s[1][-2:]]
    out = []
    r = report(a, e, out=out.append)
    ok &= r == 1 and any("sigma_9" in x for x in out)
    print("selftest:", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:2] == ["--selftest"]:
        sys.exit(selftest())
    w = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "sigF_w1.10_K33_J1000.json")
    m = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(HERE), "T153-macm3", "sigF_w1.10_K33_J1000.json")
    sys.exit(report(load(w), load(m)))

#!/usr/bin/env python3
"""Bit-for-bit comparison of the I140 repeat runs (issue #140).

    python compare.py [DIR]       DIR defaults to the folder of this file. Prints, per family, the SHA-256 of every JSON
                                  after dropping the timing keys, the groups of identical files, the first differing
                                  entry of any two that differ, the exit table from exits.txt, and the stack found in
                                  the log of any copy without a JSON. Also compares each B with I104-win2's.
                                  Exit 0: the copies of every family are identical and the control differs.
                                  Exit 1: copies differ, or a copy has no JSON (crash).
                                  Exit 2: the rp control's rho_6a JSON hashes like the copies, or macm3's B (known different) equals
                                  the copies' B, so that comparison could not fail.
    python compare.py --selftest  timings alone do not change a hash, one changed digit does (exit 1 inside).

Dropped keys: `sec`, `seconds`, `timing`, `order_times`, and any key ending in `_s`, `time` or `times`. The issue names
`sec`, `timing`, `_s` and `time`; `seconds` and `order_times` are the amplitude JSON's own timing keys and are added.
"""
import hashlib, json, os, sys

DROP = {"sec", "seconds", "timing", "order_times"}


def is_timing(key):
    return key in DROP or key.endswith(("_s", "time", "times"))


def strip(obj, dropped):
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if is_timing(k):
                dropped.add(k)
            else:
                out[k] = strip(v, dropped)
        return out
    if isinstance(obj, list):
        return [strip(x, dropped) for x in obj]
    return obj


def canon(path):
    dropped = set()
    with open(path) as f:
        obj = strip(json.load(f), dropped)
    return obj, hashlib.sha256(json.dumps(obj, sort_keys=True).encode()).hexdigest(), sorted(dropped)


def first_diff(a, b, path=""):
    """the path and the two values of the first entry where a and b differ, or None"""
    if type(a) != type(b):
        return path, repr(a)[:80], repr(b)[:80]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"{path}/{k}", "missing" if k not in a else "present", "missing" if k not in b else "present"
            d = first_diff(a[k], b[k], f"{path}/{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return path, f"length {len(a)}", f"length {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else (path, repr(a)[:80], repr(b)[:80])


def family(title, files, out, control=None, extra=None):
    """files: {label: path}. Returns (copies_identical, control_differs or None, copies_missing)"""
    out(f"\n== {title}")
    objs, hashes, missing = {}, {}, []
    for lab, p in files.items():
        if not os.path.exists(p):
            missing.append(lab)
            out(f"  {lab:14s} NO JSON")
            continue
        o, h, dropped = canon(p)
        objs[lab], hashes[lab] = o, h
        out(f"  {lab:14s} {h}   dropped keys: {', '.join(dropped) or 'none'}")
    labs = [l for l in files if l in hashes and not l.startswith("control")]
    ident = len(set(hashes[l] for l in labs)) <= 1 and bool(labs) and not missing
    if len(labs) > 1:
        groups = {}
        for l in labs:
            groups.setdefault(hashes[l], []).append(l)
        out("  copies: " + ("all identical" if len(groups) == 1 else "DIFFER, groups " + str(list(groups.values()))))
        if len(groups) > 1:
            g = list(groups.values())
            d = first_diff(objs[g[0][0]], objs[g[1][0]])
            out(f"  first differing entry between {g[0][0]} and {g[1][0]}: {d}")
    ctl = None
    if control and control in hashes and labs:
        ctl = hashes[control] != hashes[labs[0]]
        out(f"  control {control} hash {'differs from' if ctl else 'EQUALS'} the copies' hash")
        if ctl:
            out(f"  first entry where the control differs: {first_diff(objs[labs[0]], objs[control])}")
    for lab, p in (extra or {}).items():
        if os.path.exists(p) and labs:
            _, h, _ = canon(p)
            same = [l for l in labs if hashes[l] == h]
            out(f"  {lab}: {'equal to ' + ', '.join(same) if same else 'differs from every copy'} ({h[:16]}...)")
            if not same:
                out(f"    first differing entry against {labs[0]}: {first_diff(objs[labs[0]], canon(p)[0])}")
    return ident, ctl, missing


def macm3_b_equals_copies(d, raw):
    a, b = os.path.join(d, "B_copy1.json"), os.path.join(raw, "I103-macm3", "B_M5_sub1e-18.json")
    return os.path.exists(a) and os.path.exists(b) and canon(a)[1] == canon(b)[1]


def main(d):
    raw = os.path.dirname(os.path.abspath(d))
    lines = []
    out = lambda s: (print(s), lines.append(s))
    i104 = os.path.join(raw, "I104-win2")
    cp = [1, 2, 3]
    r1 = family("lemma 6a(5), rho_6a JSON (--json)", {**{f"l6a_copy{i}": f"{d}/l6a_copy{i}.json" for i in cp},
                "control_rp0.081": f"{d}/l6a_control.json"}, out, control="control_rp0.081",
                extra={"I104-win2 lemma6a": f"{i104}/lemma6a_M5_sub1e-18.json"})
    # B is the backward enclosure from the box alone, so rp does not enter it: the rp control is expected to give the
    # same B (listed below, not a control). B's own control is a B known to differ, macm3's (#110: 748 of 760 radii).
    r2 = family("lemma 6a(5), stored B (--save-B); the rp control's B is expected equal", {**{f"B_copy{i}": f"{d}/B_copy{i}.json"
                for i in cp}, "control_rp0.081": f"{d}/B_control.json"}, out,
                extra={"I104-win2 B": f"{i104}/B_M5_sub1e-18.json",
                       "I103-macm3 B (expected to differ)": f"{os.path.join(raw, 'I103-macm3')}/B_M5_sub1e-18.json"})
    r3 = family("amp_flint_par 1.10 K 15 J 750 640 bits, --procs 1", {f"amp_copy{i}": f"{d}/amp_copy{i}.json"
                                                                       for i in cp}, out)
    out("\n== exits.txt")
    ex = os.path.join(d, "exits.txt")
    out(open(ex).read().rstrip() if os.path.exists(ex) else "  no exits.txt")
    crashed = [l for r in (r1, r2, r3) for l in r[2]]
    for lab in sorted(set(crashed)):
        base = lab.replace("B_copy", "l6a_copy").replace("B_control", "l6a_control")
        log = os.path.join(d, base + ".log")
        if os.path.exists(log):
            t = open(log, errors="replace").read().strip().splitlines()[-25:]
            out(f"\n== tail of {os.path.basename(log)} for {lab} (no JSON)")
            out("\n".join(t))
    code = 0
    if any(not r[0] for r in (r1, r2, r3)) or crashed:
        code = 1
    if code == 0 and r1[1] is False:
        code = 2  # the rho_6a JSON of the control (rp = 0.081) must differ, or the comparison could not fail
    if code == 0 and macm3_b_equals_copies(d, raw):
        code = 2  # macm3's B is known to differ from win2's, so B's comparison must show it
    out(f"\nexit {code}: " + {0: "copies identical in every family, control differs",
                              1: "copies differ or a copy has no JSON", 2: "control hashes like the copies"}[code])
    with open(os.path.join(d, "compare.txt"), "w") as f:
        f.write("\n".join(lines) + "\n")
    return code


def selftest():
    a = {"M": 5, "sec": 1.5, "rho6a": "[0.2 +/- 1e-9]", "order_times": [1, 2], "x": {"f_s": 3, "v": ["1.0", "2.0"]}}
    b = json.loads(json.dumps(a)); b["sec"] = 9.9; b["order_times"] = [7, 8]; b["x"]["f_s"] = 4
    c = json.loads(json.dumps(a)); c["x"]["v"][1] = "2.0000000001"
    h = lambda o: hashlib.sha256(json.dumps(strip(o, set()), sort_keys=True).encode()).hexdigest()
    ok = h(a) == h(b) and h(a) != h(c) and first_diff(strip(a, set()), strip(c, set()))[0] == "/x/v[1]"
    print("selftest", "ok" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--selftest"]:
        sys.exit(selftest())
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))))

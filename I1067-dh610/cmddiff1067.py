#!/usr/bin/env python3
"""cmddiff1067.py ACTUAL_CMD_FILE | --selftest [--break]: the diff of a stage 1 lowD_dd.py command against run1014b.py's B1 command (ref/run1014b.py, dh170's, read with ast: the Popen list that holds 'lowD_dd.py'), the coordinator's rule of 21 Nov
(diff each launch's command, keep the diff). Both are reduced to the tokens after 'lowD_dd.py' and compared as option -> value maps. The options that must differ for #1067 are --Ms (512), --threads (10), --tag (lowD1067), the jsonl path and --start's
value (this folder's), --it_max (resumes) and --resume (added): the others must be equal (--nodes, --kt, --kcs, --ks, --jac, --tol). Prints the unified token diff, then 'cmddiff1067: ONLY THE EXPECTED OPTIONS DIFFER' or 'UNEXPECTED DIFFERENCE: ...';
exit 0 only for the first. --selftest plants a changed --kt, a dropped --jac, a changed --nodes and a changed --tol (each must be unexpected) and the expected command (must pass); --break expects a planted slip to pass and must exit 1."""
import ast
import difflib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECTED = {"--Ms", "--threads", "--tag", "--start", "--it_max", "--resume"}   # plus the jsonl path (the first positional)


def ref_tokens():
    src = open(os.path.join(HERE, "ref", "run1014b.py")).read()
    tree = ast.parse(src)
    consts = {}
    for n in ast.walk(tree):
        if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name) and isinstance(n.value, ast.Constant):
            consts[n.targets[0].id] = n.value.value
    for n in ast.walk(tree):
        if isinstance(n, ast.Call) and n.args and isinstance(n.args[0], ast.List) and any(isinstance(e, ast.Constant) and e.value == "lowD_dd.py" for e in n.args[0].elts):
            out = []
            for e in n.args[0].elts:
                if isinstance(e, ast.Constant):
                    out.append(str(e.value))
                elif isinstance(e, ast.Name):
                    out.append(str(consts.get(e.id, "{" + e.id + "}")))
                elif isinstance(e, ast.JoinedStr):
                    out.append("{path}/" + "".join(v.value for v in e.values if isinstance(v, ast.Constant)).lstrip("/"))
                else:
                    out.append("{" + ast.unparse(e) + "}")
            i = out.index("lowD_dd.py")
            return out[i + 1:]
    raise SystemExit("run1014b.py: no lowD_dd.py Popen list found")


def as_map(t):
    m, i = {"__jsonl__": t[0]}, 1
    while i < len(t):
        if t[i].startswith("--"):
            if i + 1 < len(t) and not t[i + 1].startswith("--"):
                m[t[i]] = t[i + 1]
                i += 2
            else:
                m[t[i]] = True
                i += 1
        else:
            i += 1
    return m


def compare(actual):
    a, r = actual, ref_tokens()
    d = list(difflib.unified_diff(r, a, "run1014b.py B1", "actual", lineterm="", n=0))
    ma, mr = as_map(a), as_map(r)
    bad = sorted(k for k in set(ma) | set(mr) if ma.get(k) != mr.get(k) and k not in EXPECTED and k != "__jsonl__")
    return d, bad


def selftest(brk):
    r = ref_tokens()
    exp = list(r)
    exp[exp.index("--Ms") + 1] = "512"; exp[exp.index("--threads") + 1] = "10"; exp[exp.index("--tag") + 1] = "lowD1067"; exp[exp.index("--start") + 1] = "/x/ref/lowD1014b_D3.0475_M384.npz"
    exp[exp.index("--it_max") + 1] = "1"; exp[0] = "/x/m512b.jsonl"; exp += ["--resume"]
    def mod(f):
        t = list(exp); f(t); return t
    cases = [("the expected command", exp, True),
             ("a changed --kt", mod(lambda t: t.__setitem__(t.index("--kt") + 1, "40")), False),
             ("a dropped --jac f64", mod(lambda t: (t.pop(t.index("--jac")), t.pop(t.index("f64")))), False),
             ("a changed --nodes", mod(lambda t: t.__setitem__(t.index("--nodes") + 1, "0.1,0.2")), False),
             ("a changed --tol", mod(lambda t: t.__setitem__(t.index("--tol") + 1, "1e-20")), False)]
    if brk:
        cases[1] = (cases[1][0], cases[1][1], True)
    bad = 0
    for name, t, want in cases:
        d, b = compare(t)
        ok = (not b) == want
        print(f"  {name}: {'only expected options differ' if not b else 'unexpected: ' + ','.join(b)} (expected {'pass' if want else 'unexpected'}): {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    import shlex
    t = shlex.split(open(sys.argv[1]).read())
    t = t[t.index("lowD_dd.py") + 1:]
    d, bad = compare(t)
    for l in d:
        print(l)
    print("cmddiff1067: ONLY THE EXPECTED OPTIONS DIFFER" if not bad else "cmddiff1067: UNEXPECTED DIFFERENCE: " + ", ".join(bad))
    sys.exit(0 if not bad else 1)

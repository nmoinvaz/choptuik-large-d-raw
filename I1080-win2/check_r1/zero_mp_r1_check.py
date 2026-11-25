"""#1080: zero_mp.py's --r1 pass-through. A fake value_mp records every value_v call (A, wf, v, M, r1, kwargs) made by
newton() on the M > 3 path; the old file (commit 6b807830) and the new one must make byte-identical call lists at the
default r1, and the new one must pass '0.2' through when asked (the old one cannot: exit 1 on that comparison is the
control). Exit 0 iff default calls are identical and the --r1=0.2 calls differ from the default's only in r1."""
import importlib.util, json, sys, types

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec)
    sys.argv = [path]; spec.loader.exec_module(m); return m

def run(path, name, **kw):
    log = []
    fake = types.ModuleType("value_mp")
    def value_v(A, wf, v, M, r1="0.17", **k):
        log.append([repr(A), repr(wf), [str(x) for x in v], M, r1, sorted((a, repr(b)) for a, b in k.items())])
        R = (float(A) - 3.4) * 100 + 1j * (float(wf) - 0.2) * 50
        return dict(re=R.real, im=R.imag, sig=1e-17, valued=True, v=[str(x) for x in v], info=0.0, seconds=0.0,
                    J=([["1"]], [["1"]]) if k.get("want_J") else None)
    fake.value_v = value_v
    sys.modules["value_mp"] = fake
    m = load(path, name)
    m.newton(3.5, 0.21, ["1.0", "0.1", "0.4", "0.01"], m._value_v, 2, 1e-7, 1e-8, 1, None, M=5, **kw)
    return log

d = sys.argv[1]
old = run(d + "/zero_mp_old.py", "zo")
new = run(d + "/zero_mp_new.py", "zn")
new2 = run(d + "/zero_mp_new.py", "zn2", r1="0.2")
ok1 = json.dumps(old) == json.dumps(new)
strip = lambda L: [[*c[:4], *c[5:]] for c in L]
ok2 = json.dumps(strip(new)) == json.dumps(strip(new2)) and all(c[4] == "0.2" for c in new2) and all(c[4] == "0.17" for c in new)
ctl = json.dumps(old) != json.dumps(new2)           # the control: the old file cannot pass r1 = 0.2
print(f"calls {len(old)}; default old == new: {ok1}; --r1=0.2 reaches every call and changes nothing else: {ok2}; "
      f"control (old differs from new at r1 0.2): {ctl}")
sys.exit(0 if ok1 and ok2 and ctl else 1)

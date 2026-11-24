"""#1084 (d): the new value_mp with floor=False against the old module (6b807830) on value_mp_floor_check's planted
residual: value_v rows including calls, at M = 3 and 5 from four starts each, and solve() from a far Jacobian.

    python floor0_vs_old.py WORKTREE_INNER_STOKES OLD_DIR
"""
import importlib.util
import sys

new_dir, old_dir = sys.argv[1], sys.argv[2]
sys.path.insert(0, new_dir)
import mpmath as mp  # noqa: E402
import value_mp_floor_check as CHK  # noqa: E402
import value_mp as NEW  # noqa: E402

spec = importlib.util.spec_from_file_location("value_mp_old", old_dir + "/value_mp.py")
OLD = importlib.util.module_from_spec(spec)
spec.loader.exec_module(OLD)
NEW.IM.residual_demixed = CHK.planted
OLD.IM.residual_demixed = CHK.planted
ok = True
n_cmp = 0
for M in (3, 5):
    for s in range(4):
        mp.mp.dps = 50
        v0 = [mp.nstr(mp.mpf(k + 1) / (3 * (k + 2)) + mp.mpf("3.5") / 1000 + mp.mpf("0.3") / 7000
                      + mp.mpf(10) ** -(5 + s) * (-1) ** (k + s), 40) for k in range(M - 1)]
        a = OLD.value_v("3.5", "0.3", v0, M, iters=12, want_J=True)
        b = NEW.value_v("3.5", "0.3", v0, M, iters=12, want_J=True, floor="--mutate=floor-on" in sys.argv)
        diff = [k for k in set(a) | set(b) if k != "seconds" and a.get(k) != b.get(k)]
        ok &= not diff
        n_cmp += 1
        print(f"M {M} start {s}: calls old {a['calls']} new {b['calls']}; {'identical' if not diff else 'DIFFER ' + str(diff)}")
mp.mp.dps = 34
far = [mp.mpf(k + 1) / (3 * (k + 2)) + mp.mpf("3.5") / 1000 + mp.mpf("0.3") / 7000 + mp.mpf("1e-3") for k in range(2)]
o = OLD.solve("3.5", "0.3", far, "0.17", 34, 40, iters=0)
near = [mp.nstr(t - mp.mpf("1e-3") + mp.mpf("1e-7"), 40) for t in far]
x = OLD.solve("3.5", "0.3", near, "0.17", 42, 50, iters=12, J=(o[3], o[4]))
y = NEW.solve("3.5", "0.3", near, "0.17", 42, 50, iters=12, J=(o[3], o[4]), floor=False, keep_J=False)
L = lambda B: [[B[i, k] for k in range(B.cols)] for i in range(B.rows)]
same = (x[0], x[1], tuple(x[2]), x[6], L(x[3]), L(x[4])) == (y[0], y[1], tuple(y[2]), y[6], L(y[3]), L(y[4]))
ok &= same
print(f"far-Jacobian solve: calls old {x[6]} new {y[6]}; R, r, v, J {'identical' if same else 'DIFFER'}")
print(f"floor=False against the old module: {'PASS' if ok else 'FAIL'} ({n_cmp} value_v rows and one solve)")
sys.exit(0 if ok else 1)

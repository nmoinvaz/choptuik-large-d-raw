"""#935 follow-up (b): the octo-double path of the chains' corrector that calls multidouble's Python helpers
(od_axpy, od_add_dd): PinnedO.residual_o and PinnedO.newton_o (hp/octo_corrector.py) on one stored chain state, written
for a bit-for-bit comparison between two multidouble Python packages under the same kernel (the running venv's hpkernel).
The package is the one `import multidouble` finds first (PYTHONPATH puts another before the venv's).

    python pinnedo_dump.py HP_DIR STATES_ROOT PREFIX
    python pinnedo_dump.py --compare A B CTL

Dump, per variant: held8 (the state's own system, held values in eight parts: od_axpy in residual_o), heldfloat (the
held values as floats: od_add_dd in residual_o), and ctl_qdoffset (the control: PinnedO's J^-1 c through the quad-double
LU, mutate_offset 'qd'). Each writes residual_o(z) and newton_o(z)'s step, F and pivots. Compare, fixed before the first
run: A and B (the two packages) must have every entry of held8 and heldfloat with the same bits, and CTL (ctl_qdoffset of
B) must change the step of B's held8. Every differing entry is listed. Exit 0 only then."""
import sys

import numpy as np

STATE = "I903-win2/ks_chain/leg06_D212.0000_ks230/anm_pin3_D215.0000.npz"
VARIANTS = {"held8": {}, "heldfloat": {"held": "float"}, "ctl_qdoffset": {"mutate_offset": "qd"}}


def bits(a):
    return np.ascontiguousarray(np.asarray(a, dtype=np.float64)).view(np.uint64)


def dump(hp, root, prefix):
    sys.path.insert(0, hp)
    import multidouble
    import hpkernel
    from octo_corrector import truth_system
    print(f"multidouble {multidouble.__file__}\nhpkernel {hpkernel.__file__}", flush=True)
    for name, kw in VARIANTS.items():
        z, meta, (s, sp, sq, so), info = truth_system(root, STATE, threads=5, **kw)
        if len(z) != 8:
            raise SystemExit(f"{STATE}: {len(z)} parts, not eight")
        zo = [np.ascontiguousarray(np.asarray(x)) for x in z]
        out = {}
        F = so.residual_o(list(zo))
        out.update({f"F{k}": np.asarray(F[k]) for k in range(8)})
        d, f0, f1, pmin, pmax = so.newton_o(list(zo))
        out.update({f"dz{k}": np.asarray(d[k]) for k in range(8)})
        out.update(nF0=np.asarray(f0), nF1=np.asarray(f1), pmin=np.float64(pmin), pmax=np.float64(pmax))
        np.savez(f"{prefix}_{name}.npz", **out)
        print(f"{name}: D {meta.get('D_str')!s:.8}, {info['plan']} plan, held {info['held']}, max|F| (pinned, octo) "
              f"{np.max(np.abs(out['F0'])):.3e}, max|dz| {np.max(np.abs(out['dz0'])):.3e}", flush=True)
    return 0


def compare(a, b, ctl):
    ok = True
    for name in ("held8", "heldfloat"):
        A, B = np.load(f"{a}_{name}.npz"), np.load(f"{b}_{name}.npz")
        n = sum(A[k].size for k in A.files)
        diff = {k: np.flatnonzero(bits(A[k]).ravel() != bits(B[k]).ravel()) for k in A.files}
        nd = sum(len(v) for v in diff.values())
        print(f"{name}: {nd} of {n} entries differ, A against B", flush=True)
        for k, idx in diff.items():
            for i in idx[:10]:
                print(f"   {k}[{i}]: A {bits(A[k]).ravel()[i]:016x}  B {bits(B[k]).ravel()[i]:016x}", flush=True)
            if len(idx) > 10:
                print(f"   {k}: {len(idx) - 10} more", flush=True)
        ok &= nd == 0
    B, C = np.load(f"{b}_held8.npz"), np.load(f"{ctl}_ctl_qdoffset.npz")
    dctl = sum(int(np.count_nonzero(bits(B[f"dz{k}"]) != bits(C[f"dz{k}"]))) for k in range(8))
    print(f"control (J^-1 c through the quad-double LU) against B's held8: {dctl} step entries differ", flush=True)
    fired = dctl > 0
    print(f"{'PASS' if ok else 'FAIL'}: A and B {'have' if ok else 'do NOT have'} the same bits; control "
          f"{'fired' if fired else 'DID NOT FIRE'}", flush=True)
    return 0 if ok and fired else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(compare(*a[1:4]) if a[0] == "--compare" else dump(a[0], a[1], a[2]))

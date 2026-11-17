"""#934: the octo-double residual and Newton step on stored chain states, written for a bit-for-bit comparison between
two hpkernel builds. The Python is the same for both (the new worktree's hp); the kernel is the running venv's.

    python state_dump.py HP_DIR STATES_ROOT PREFIX [--control]
    python state_dump.py --compare OLD NEW CTL

Dump: per state, residual_o(z) and newton_o(z) (two tangents, the default), or with --control newton_o(z, mutate=25,
tangents=4), each evaluation's tangents read in reverse. Compare, fixed before the first run: exit 0 only when every
part of every entry of both states' residuals and steps has the same bits in OLD and NEW, and CTL's steps differ from
OLD's."""
import sys

import numpy as np

STATES = {"k160_D231": "I903-dh610/chain_k160/anm_pin3_D231.0000.npz",
          "i841_D259": "I841-dh370/chain/anm_pin3_D259.5166.npz"}


def bits(a):
    return np.ascontiguousarray(np.asarray(a, dtype=np.float64)).view(np.uint64)


def dump(hp, root, prefix, control):
    sys.path.insert(0, hp)
    import hpkernel
    from octo_corrector import truth_system
    print(f"hpkernel {hpkernel.__file__}", flush=True)
    for name, p in STATES.items():
        z, meta, (s, _, _, _), info = truth_system(root, p, threads=5)
        if len(z) != 8:
            raise SystemExit(f"{p}: {len(z)} parts, not eight")
        zo = [np.ascontiguousarray(np.asarray(x)) for x in z]
        out = {}
        if control:
            st = s.newton_o(list(zo), mutate=25, tangents=4)
        else:
            F = s.residual_o(list(zo))
            out.update({f"F{k}": np.asarray(F[k]) for k in range(8)})
            st = s.newton_o(list(zo))
        out.update({f"dz{k}": np.asarray(st[0][k]) for k in range(8)})
        out.update(a1=np.asarray(st[1]), a2=np.asarray(st[2]), f3=np.float64(st[3]), f4=np.float64(st[4]))
        np.savez(f"{prefix}_{name}.npz", **out)
        what = "control step" if control else f"max|F| {np.max(np.abs(out['F0'])):.3e}"
        print(f"{name}: D {meta.get('D_str', meta.get('D'))!s:.16}, {info['plan']} plan, {what}", flush=True)
    return 0


def compare(old, new, ctl):
    ok, fired = True, True
    for name in STATES:
        o, n, c = (np.load(f"{x}_{name}.npz") for x in (old, new, ctl))
        d = {k: int(np.count_nonzero(bits(o[k]) != bits(n[k]))) for k in o.files}
        dres = sum(v for k, v in d.items() if k.startswith("F"))
        dstep = sum(v for k, v in d.items() if not k.startswith("F"))
        dctl = sum(int(np.count_nonzero(bits(o[f"dz{k}"]) != bits(c[f"dz{k}"]))) for k in range(8))
        print(f"{name}: entries that differ, old against new: residual {dres}, step {dstep}; control (tangents "
              f"reversed) {dctl}", flush=True)
        ok &= dres + dstep == 0
        fired &= dctl > 0
    print(f"{'PASS' if ok else 'FAIL'}: residuals and steps {'are' if ok else 'are NOT'} the same bits; control "
          f"{'fired' if fired else 'DID NOT FIRE'}", flush=True)
    return 0 if ok and fired else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    sys.exit(compare(*a[1:4]) if a[0] == "--compare" else dump(a[0], a[1], a[2], "--control" in a))

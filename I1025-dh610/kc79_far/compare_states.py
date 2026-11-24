#!/usr/bin/env python3
"""#1025 kc79_far (dh610) compare_states.py D [DIR] | selftest [--mutate]: the two states of win2's k_c 79 leap (tag g, h 0.03125) and far scout (tag i, h 0.0625) at one D, side by side (coordinator t5, hc 24 Nov: two
continuation paths to one D and k_c, the state reproducibility). Reads (DIR defaults to D<D>) the last row at D of DIR/g/in/l1kc79Lw1025g.jsonl and DIR/i/in/l1kc79Lw1025i.jsonl and the two states beside them; prints Delta, |F|, steps,
psi-constraint (the ordered four), then h and seconds, and, as an extra, the L2 distance of the two state vectors (Delta entry included) when their shapes match. No number is typed by hand.
selftest: planted rows and states with known differences must be read back to those differences (Delta 1e-7, |F| ratio 1.01, steps -2, constraint 3e-6, state distance 5e-9); --mutate reads the constraint column as |F|, which the
planted check must catch: the selftest exits 1 (FIRED)."""
import sys, json, os, tempfile
import numpy as np

FIELDS = [("Delta", "Delta"), ("|F|", "F"), ("steps", "steps"), ("psi-constraint", "constraint"), ("h", "h"), ("seconds", "seconds")]


def row_at(path, D):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    rows = [r for r in rows if r.get("D") == D]
    if not rows:
        raise SystemExit(f"no row at D {D} in {path}")
    return rows[-1]


def read(g, i, zg, zi, mutate=False):
    out = []
    for name, key in FIELDS:
        k = "constraint" if (mutate and key == "F") else key
        a, b = g.get(k), i.get(k)
        out.append((name, a, b, None if a is None or b is None else b - a, None if a in (None, 0) or b is None else b / a))
    d = None
    if zg.shape == zi.shape:
        d = float(np.linalg.norm(zi - zg))
    return out, d


def show(D, g, i, out, d, zg, zi):
    print(f"D {D}: tag g (h {g.get('h')}) against tag i (h {i.get('h')}); kc {g.get('kc')} and {i.get('kc')}")
    print("| quantity | tag g | tag i | i - g | i / g |")
    print("|---|---|---|---|---|")
    for name, a, b, df, ra in out:
        fmt = lambda v: "-" if v is None else (repr(v) if isinstance(v, float) else str(v))
        print(f"| {name} | {fmt(a)} | {fmt(b)} | {fmt(df)} | {fmt(ra)} |")
    print(f"extra, not ordered: L2 distance of the two state vectors (Delta entry included): {d!r} (shapes {zg.shape} and {zi.shape}); Delta entries {zg[-1]!r} and {zi[-1]!r}")


def selftest(mutate):
    rg = dict(D=21.5, kc=79, F=4.5e-10, steps=2650, constraint=5.6e-3, Delta=1.125, h=0.03125, seconds=4500)
    ri = dict(rg, F=4.5e-10 * 1.01, steps=2648, constraint=5.6e-3 + 3e-6, Delta=1.125 + 1e-7, h=0.0625, seconds=9000)
    zg = np.zeros(10); zi = zg.copy(); zi[3] = 5e-9
    out, d = read(rg, ri, zg, zi, mutate)
    want = {"Delta": 1e-7, "steps": -2, "psi-constraint": 3e-6}
    bad = 0
    for name, a, b, df, ra in out:
        if name in want:
            ok = abs(df - want[name]) <= 1e-12 + 1e-9 * abs(want[name])
            bad += not ok
            print(f"  {name}: difference {df!r} (planted {want[name]!r}): {'ok' if ok else 'WRONG'}")
    f = [x for x in out if x[0] == "|F|"][0]
    ok = abs(f[4] - 1.01) < 1e-12
    bad += not ok
    print(f"  |F| ratio {f[4]!r} (planted 1.01): {'ok' if ok else 'WRONG'}")
    ok = d is not None and abs(d - 5e-9) < 1e-18
    bad += not ok
    print(f"  state distance {d!r} (planted 5e-09): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    if mutate and bad:
        print("mutate: control FIRED (exit 1)")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    D = float(sys.argv[1])
    R = next((a for a in sys.argv[2:] if not a.startswith("--")), f"D{sys.argv[1]}")
    rg = row_at(f"{R}/g/in/l1kc79Lw1025g.jsonl", D)
    ri = row_at(f"{R}/i/in/l1kc79Lw1025i.jsonl", D)
    Df = f"{D:.6f}"
    zg = np.load(f"{R}/g/in/sol_l1kc79Lw1025g_D{Df}.npy")
    zi = np.load(f"{R}/i/in/sol_l1kc79Lw1025i_D{Df}.npy")
    out, d = read(rg, ri, zg, zi, "--mutate" in sys.argv)
    show(sys.argv[1], rg, ri, out, d, zg, zi)

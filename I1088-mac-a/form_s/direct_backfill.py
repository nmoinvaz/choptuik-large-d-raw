"""direct_s.jsonl back-filled for the converged form-S solves before form_s.py jump wrote it (#1088): per state, the
quad-double residual of the system it solved (the check), the discretization report (top harmonics; the residual's
change at kc + 20, ks + 200 and halved Taylor steps; bars 1e-25) and the Hamiltonian code check, with the solve's own
residual, gain, commit, machine and time from its logs (the table below). Appends to each raw folder's direct_s.jsonl.

    python3 direct_backfill.py
"""
import json, os, sys, time
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a3b9be47f38a490b5/hp")
import numpy as np
import mpmath as mp
import jump
from form_s import make_solver_s, HeldS, held_field, disc_report, ham_check, direct_line
from octo_corrector import load_o

R = "/Users/nathan/Source/choptuik-large-d-raw-1088a"
# state, folder, system, the solve's max |F| and precision, Delta's gain (None: not formed), held -> full dDelta,
# Track C (value, err) where delta_all.csv has no series row, commit, machine, the solve's end (utc), log
rows = [
    ("I1088-mac-a/form_s/j250_held/jump_s_D250.0000.npz", "I1088-mac-a", "held", None, "od", None, None, None,
     "38bc62c1 (Rust 38943f4f, dev-o1)", "mac", None, "I1088-mac-a/form_s/j250_held/jump.log"),
    ("I1088-dh370/j300_held/jump_s_D300.0000.npz", "I1088-dh370", "held", None, "od", 9.62e8, None, None,
     "38bc62c1 (Rust 38943f4f)", "dh370-fedora", "2026-11-25 04:02:37", "I1088-dh370/j300_held/jump.log"),
    ("I1088-dh610/out/rls300/release_ls_h13_D300.0000.npz", "I1088-dh610", "full", 5.41e-50, "od", 5.32e19,
     -9.747e-12, None, "6e57fdf8 (Rust 38943f4f)", "dh610-fedora", "2026-11-25 06:09:05", "I1088-dh610/out/rls300.log"),
    ("I1088-dh610/j400_held/jump_s_D400.0000.npz", "I1088-dh610", "held", None, "od", 4.11e8, None, None,
     "38bc62c1 (Rust 38943f4f)", "dh610-fedora", None, "I1088-dh610/j400_held/jump.log"),
    ("I1088-dh370/j1000_held_mob/jump_s_D1000.0000.npz", "I1088-dh370", "held", 3.731e-67, "od", None, None,
     ("1.654240854245", 7.8e-10), "6a534b4d (Rust 6244fbff)", "dh370-fedora", "2026-11-25 08:04:25",
     "I1088-dh370/j1000_held_mob/jump.log"),
]
for (st, folder, system, Fs, sprec, gain, h2f, tcg, commit, machine, utc, logp) in rows:
    t0 = time.time()
    path = os.path.join(R, st)
    z8, meta = load_o(path)
    M, nodes = int(meta["M"]), list(meta["nodes"])
    K = len(nodes)
    with mp.workdps(60):
        D = mp.mpf(meta["D_str"])
    mob = float(meta.get("hmob", 0.0) or 0.0)
    kfs = 3 if system == "held" else 13
    kw = dict(kt=int(meta.get("kt", 36)), kc=int(meta["kc"]), threads=2, kfreeze=kfs)
    h8 = held_field(z8, M) if system == "held" else None
    s = make_solver_s(D, M, nodes, ks=int(meta["ks"]), segs=meta["segs"], mob=mob, **kw)
    s = HeldS(s, M, K, h8) if h8 is not None else s
    F = s.residual_s([np.ascontiguousarray(z8[q]) for q in range(4)])
    Fc = float(np.abs(np.asarray(F[0]) + np.asarray(F[1])).max())
    meta = dict(meta, ks=int(meta["ks"]))
    dsc = disc_report(z8, meta, kw, mob, h8, F, gain if gain else float("nan"))
    hc = ham_check(z8, meta, threads=2)
    if Fs is None:
        Fs = meta.get("F")
    sd = jump.series_delta(meta["D_str"]) or jump.series_delta(str(int(round(float(D)))))
    tc = (dict(value=mp.nstr(sd[0], 16), err=sd[1], source="delta_all.csv series") if sd is not None else
          dict(value=tcg[0], err=tcg[1], source="given") if tcg else None)
    rec = direct_line(z8, meta, path, system, Fs, sprec, Fc, "qd", bound=(gain * Fc if gain else None), held_to_full=h2f,
                      disc=dsc, ham={str(b): r for b, r in hc.items()}, tc=tc, commit=commit,
                      extra=dict(machine=machine, solve_utc=utc, backfilled=True, log=logp, gain=gain,
                                 full_dDelta_first_order=meta.get("full_dDelta_first_order")))
    with open(os.path.join(R, folder, "direct_s.jsonl"), "a") as fh:
        fh.write(json.dumps(rec) + "\n")
    print(f"{st}: D {float(D):g} {system}, qd check |F| {Fc:.2e}, disc {dsc['verdict']}, Hamiltonian a rows "
          f"{max(r['a'] for r in hc.values()):.1e} ({time.time() - t0:.0f} s)", flush=True)

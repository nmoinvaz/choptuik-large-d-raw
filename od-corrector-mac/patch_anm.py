p = "/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a74f73ca27245af7e/hp/anm_run.py"
t = open(p).read()


def rep(old, new, count=1):
    global t
    assert t.count(old) == count, (old, t.count(old))
    t = t.replace(old, new)


# usage
rep("""        [--jet_o 0]

--corrector qd""", """        [--jet_o 0] [--corrector od --tol_od 1e-40]

--corrector qd""")
# --jet_o paragraph: the corrector it needs
rep("""summed by Horner's rule in octo-double (od_axpy) and rounded to quad-double, where the quad-double corrector starts, so
it needs --corrector qd and with --reseed also --reseed_q 1; it replaces --jet_q, --pred_q and --fix1, and --probe does""",
"""summed by Horner's rule in octo-double (od_axpy) and rounded to quad-double, where the quad-double corrector starts, so
it needs --corrector qd (or od) and with --reseed also --reseed_q 1; it replaces --jet_q, --pred_q and --fix1, and --probe does""")
# the od paragraph, after --save_pred's
rep("""its re-seed as pred_pin<k>_D<D>.npz, an input for testing the re-seed (13.26).
\"\"\"""", """its re-seed as pred_pin<k>_D<D>.npz, an input for testing the re-seed (13.26).
--corrector od is the corrector in octo-double (hp/octo_corrector.py, notes/OCTO_DOUBLE.md 5): newton_od, newton_qd's
rule on the octo-double kernel (PinnedO: Solver.newton_o, olu_solve and residual_o with the held offset), to --tol_od
on max |F| in at most --qd_it steps, with --reseed 2 inside ElimO (ElimQ's quad-double projection put back in eight
parts). Under --jet_o 1 it starts from the octo-double prediction in all eight parts, its horizon data re-seeded; a
restart from a state saved by it polishes all eight parts. Its states are saved in eight parts (octo_corrector.save_o:
save_q's four, which load_q reads, and four more), and the series of the next base (--jet_o) is taken at all eight.
M = 32 only; --accept_stall_qd does not apply.
\"\"\"""")
# imports
rep("""from raw_out import require_raw  # noqa: E402
""", """from raw_out import require_raw  # noqa: E402
from octo_corrector import ElimO, PinnedO, has_o, load_o, newton_od, o8, o8_of_q, q4_of_o, save_o, with_horizon  # noqa: E402,F401
""")
# o8 helpers now in octo_corrector
rep('''def o8(z):
    """an octo-double vector's eight parts as contiguous float64 arrays"""
    return tuple(np.ascontiguousarray(np.asarray(p, dtype=float)) for p in z)


def o8_of_q(zq):
    """a quad-double vector's four parts promoted to eight (the lower four zero): the same values exactly"""
    zero = np.zeros(len(zq[0]))
    return o8(tuple(zq) + (zero, zero, zero, zero))


def q4_of_o(zo):
    """an octo-double vector rounded to quad-double: its first four parts plus the rest's sum (float64, from the
    smallest up), renormalized by qd_add_dd, as OD::to_qd does; the rounding is about 2^-212 of each entry"""
    zo = o8(zo)
    tail = zo[4] + (zo[5] + (zo[6] + zo[7]))
    return tuple(np.ascontiguousarray(np.asarray(p)) for p in qd_add_dd(zo[0], zo[1], zo[2], zo[3], tail, np.zeros(len(tail))))


''', "")
# options
rep("""               save_pred=0, jet_o=0)
""", """               save_pred=0, jet_o=0)
    opt.update(tol_od=1e-40)            # --corrector od (hp/octo_corrector.py)
""")
rep("""    if opt["jet_o"] and (opt["corrector"] != "qd" or opt["jet_q"]""", """    if opt["jet_o"] and (opt["corrector"] not in ("qd", "od") or opt["jet_q"]""")
rep("""        raise SystemExit("--jet_o 1 needs --corrector qd, and with --reseed also --reseed_q 1; it replaces --jet_q, --pred_q \"""",
    """        raise SystemExit("--jet_o 1 needs --corrector qd or od, and with --reseed also --reseed_q 1; it replaces --jet_q, --pred_q \"""")
rep("""        raise SystemExit(f"--jet_o 1: the octo-double solver is built for M = 32 and N <= 31, not M {M}, N {N}")
""", """        raise SystemExit(f"--jet_o 1: the octo-double solver is built for M = 32 and N <= 31, not M {M}, N {N}")
    if opt["corrector"] == "od" and (M != 32 or (opt["reseed"] and not opt["reseed_q"])):
        raise SystemExit(f"--corrector od: the octo-double solver is built for M = 32 (not {M}), and with --reseed it needs --reseed_q 1")
""")
# correct(): the od block
rep('''    def correct(spx, ph, pl, tol, z4_start=None):
        """T75's corrector (scan_hp.py dnp): deflated Newton, then plain Newton steps from below 1e-12 if they lower |F|;
        returns zh, zl, |F|, steps, accepted (converged, or stalled below accept_stall). z4_start: the quad-double
        corrector's start in four parts (--pred_q), else (ph, pl)"""
''', '''    def correct(spx, ph, pl, tol, z4_start=None, z8_start=None):
        """T75's corrector (scan_hp.py dnp): deflated Newton, then plain Newton steps from below 1e-12 if they lower |F|;
        returns zh, zl, |F|, steps, accepted (converged, or stalled below accept_stall). z4_start: the quad-double
        corrector's start in four parts (--pred_q), else (ph, pl). z8_start: the octo-double corrector's in eight"""
        if opt["corrector"] == "od":
            # --corrector od: the octo-double Newton (hp/octo_corrector.py), with --reseed 2 inside ElimO
            so = PinnedO(spx.s, spx.ch, spx.cl)
            if elim.get("rs") is not None:
                so = ElimO(so, elim["rs"])
            z0 = z8_start if z8_start is not None else o8_of_q(z4_start if z4_start is not None else qparts(ph, pl))
            try:
                z8, hist, conv = newton_od(so, z0, tol=opt["tol_od"], it_max=opt["qd_it"], verbose=True)
            except StartNotProjected as e:
                print(f"      elim projections {e.args[0]}: the start's projection failed, attempt stopped", flush=True)
                Fh, Fl = spx.residual(z0[0], z0[1])
                return np.asarray(z0[0]), np.asarray(z0[1]), float(rnorm(Fh, Fl)), 0, False, 0.0
            if elim.get("rs") is not None:
                print(f"      elim projections {so.counts}", flush=True)
                z8 = so.project(z8)             # the point whose residual converged (unprojected below the switch)
            last_q["z8"], last_q["z4"] = z8, q4_of_o(z8)
            Fh, Fl = spx.residual(z8[0], z8[1])
            Fc = float(rnorm(Fh, Fl))
            fo = float(hist[-1]["F"]) if hist else float("nan")
            print(f"      octo-double Newton: {len(hist)} steps, max|F| {fo:.1e}, {'converged' if conv else 'not converged'}; double-double |F| "
                  f"of its first two parts {Fc:.1e}", flush=True)
            return np.asarray(z8[0]), np.asarray(z8[1]), Fc, len(hist), bool(conv), 0.0
''')
# base polish
rep("""        z4_base = tuple(np.ascontiguousarray(np.asarray(p)) for p in load_q(os.path.join(raw, opt["state"]))[0])
        zh, zl, F0, _, _, _ = correct(sp, zh, zl, opt["tol"], z4_base if opt["corrector"] == "qd" else None)
""", """        z4_base = tuple(np.ascontiguousarray(np.asarray(p)) for p in load_q(os.path.join(raw, opt["state"]))[0])
        if opt["corrector"] == "od":
            # --corrector od: the octo-double polish from all eight stored parts (a four-part state's promoted)
            zh, zl, F0, _, _, _ = correct(sp, zh, zl, opt["tol"], z8_start=load_o(os.path.join(raw, opt["state"]))[0])
        else:
            zh, zl, F0, _, _, _ = correct(sp, zh, zl, opt["tol"], z4_base if opt["corrector"] == "qd" else None)
""")
# the series base under --jet_o
rep("""            zq = last_q["z4"] if "z4" in last_q else load_q(os.path.join(raw, opt["state"]))[0]
            zo = o8_of_q(zq)
""", """            zq = last_q["z4"] if "z4" in last_q else load_q(os.path.join(raw, opt["state"]))[0]
            zo = o8_of_q(zq)
            if "z8" in last_q or ("z4" not in last_q and has_o(os.path.join(raw, opt["state"]))):
                # the base in eight parts: the octo-double corrector's, or a state it stored
                zo = last_q["z8"] if "z8" in last_q else load_o(os.path.join(raw, opt["state"]))[0]
""")
# the prediction in eight parts
rep("""                pred4 = None
""", """                pred4 = None
                pred8 = None                       # --corrector od: the octo-double prediction, the start
""")
rep("""                    pred4 = q4_of_o(horner_o(Zo, a))
""", """                    pred8 = horner_o(Zo, a)
                    pred4 = q4_of_o(pred8)
""")
rep("""                    if pred4 is not None:
                        pred4 = tuple(np.ascontiguousarray(np.asarray(v)) for v in zr)
""", """                    if pred4 is not None:
                        pred4 = tuple(np.ascontiguousarray(np.asarray(v)) for v in zr)
                    if pred8 is not None and rsd["ok"]:
                        pred8 = with_horizon(pred8, zr, rs_n)          # the re-seeded horizon data in eight parts
""")
rep("""                ch, cl, Fc, nsteps, accepted, dcorr = correct(spn, ph, pl, tol, pred4)
""", """                ch, cl, Fc, nsteps, accepted, dcorr = correct(spn, ph, pl, tol, pred4, z8_start=pred8)
""")
# saving
rep("""        if opt["corrector"] == "qd" and "z4" in last_q:
            save_q(os.path.join(out, f"anm_pin{kf}_D{float(D):.4f}.npz"), last_q["z4"], meta_out)
""", """        if opt["corrector"] == "qd" and "z4" in last_q:
            save_q(os.path.join(out, f"anm_pin{kf}_D{float(D):.4f}.npz"), last_q["z4"], meta_out)
        elif opt["corrector"] == "od" and "z8" in last_q:
            save_o(os.path.join(out, f"anm_pin{kf}_D{float(D):.4f}.npz"), last_q["z8"], dict(meta_out, parts=8))
""")
open(p, "w").write(t)
print("patched")

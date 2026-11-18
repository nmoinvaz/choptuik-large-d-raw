#!/usr/bin/env python3
"""#967 item 3 (dh610): #842's recommended task 1. Is a chain attempt's refusal the predictor or the arithmetic?

Run from the worktree's hp/ directory, as anm_run.py with the #842 chain's flags and --state the case's base (see
run_item3_967.sh); this script replaces arclength.run_chain, so anm_run's own base setup (the chain's plan, held fit,
solver, re-seeder) is the chain's. I967_CASE names the case:

  main     base = step 61's end (arc_062, D 259.903269724106), the series arcjet_062, target D = step 62's attempt 4
           (a = 1.3274018656201874e-05, D_start 259.9032732750934967532716882824809), the point the chain refused.
  control  base = step 60's end (arc_061), the series arcjet_061, target D = step 61's accepted attempt (a = 8.4953719399692e-05),
           where arc_062 is a converged solution.

Per case: (A) the fixed-D octo-double Newton (ChainSys.correct, border=False, the chain's flags, --qd_it 60) started from the
base state itself at the target D (its horizon re-seed may not project that start); (B) the series' prediction at the
target by the D-series (sum of w_m (D - D_0)^m, m <= k, from the arcjet file) at orders k = 1, 2, 4, ... 24 and the
chain's arclength composition moved to the target, each: max|F| as is and after the chain's re-seed; (D) the fixed-D
Newton from the full D-series' prediction; then each prediction's miss against the converged solution (A's, else D's);
(C) the chain's own attempt (bordered, --qd_it 20) replayed, its F_pred and its F by iteration against arc.jsonl's,
word for word. The control case's solution is also compared with arc_062, the chain's accepted state. Nothing is
loosened: pass is max|F| <= --tol_od (1e-60). Output: i3_<case>.json beside the chain's output directory.
"""
import json
import os
import sys
import time

HP = os.environ.get("I967_HP", os.getcwd())
sys.path.insert(0, HP)

# the chain's own records: the step, the attempt's index, the base's files, and the attempt's a
CASES = dict(
    main=dict(base="I842-dh610/chain/arc_062_D259.903270.npz", jet="I842-dh610/chain/arcjet_062_D259.903270.npz",
              step=62, attempt=3, ref=None),
    control=dict(base="I842-dh610/chain/arc_061_D259.903243.npz", jet="I842-dh610/chain/arcjet_061_D259.903243.npz",
                 step=61, attempt=0, ref="I842-dh610/chain/arc_062_D259.903270.npz"),
)


def run_case(c):
    import mpmath as mp
    import numpy as np
    import arclength as A
    from octo_corrector import load_o, q4_of_o, with_horizon
    case = os.environ["I967_CASE"]
    cfg = CASES[case]
    opt, raw, out = c["opt"], c["raw"], c["out"]
    opt["qd_it"] = int(os.environ.get("I967_QD_IT", "60"))
    KS = [int(k) for k in os.environ.get("I967_KS", "1,2,4,8,12,16,20,24").split(",")]
    recs = [json.loads(line) for line in open(os.path.join(raw, "I842-dh610/chain/arc.jsonl"))]
    rec = next(r for r in recs if r.get("step") == cfg["step"])
    att = rec["attempts"][cfg["attempt"]]
    crec = att["corrector"]
    t0 = time.time()
    out_json = dict(case=case, step=cfg["step"], attempt=cfg["attempt"], a=att["a"], qd_it=opt["qd_it"], tol_od=opt["tol_od"],
                    threads=opt["threads"], record=dict(D_pred=crec["D_pred"], D_start=crec["D_start"], F_pred=crec["F_pred"],
                                                        its=crec["its"], converged=att["converged"]))

    def say(k, v):
        out_json[k] = v
        print(f"i3 {case} {k}: {json.dumps(v, default=str)} ({time.time() - t0:.0f} s)", flush=True)
        with open(os.path.join(out, f"i3_{case}.json"), "w") as f:
            json.dump(out_json, f, indent=1, default=str)

    z8, meta = load_o(c["state_path"])
    with mp.workdps(A.DPS_SERIES):
        D0 = A.dd_round(mp.mpf(meta["D_str"]))
        sysm = A.ChainSys(c, z8, D0)
        base8 = sysm.base8
        W = sysm.series_from_file(os.path.join(raw, cfg["jet"]), D0, opt["N"])
        Z, H, cond, magn = A.compose(W, int(rec["sign"]))
        a = mp.mpf(att["a"])
        xp, Dp = A.horner(Z, a), D0 + A.horner(H, a)
        tz, tD = A.unit_tangent(Z, H, a)
        Dd = A.dd_round(Dp)
        x0 = A.to_mp_vec(base8)
        say("setup", dict(state=meta["D_str"], D0=mp.nstr(D0, 34), c_D=mp.nstr(c["D"], 34), D_pred=mp.nstr(Dp, 34),
                          D_pred_matches_record=mp.nstr(Dp, 34) == crec["D_pred"], D_start=mp.nstr(Dd, 34),
                          D_start_matches_record=mp.nstr(Dd, 34) == crec["D_start"], dD=float(Dd - D0), tD=float(tD),
                          cond_max=float(max(cond))))
        e = sysm.at(Dd)

        def F_of(x):
            return A.omax(e["po"].residual_o(A.to_parts(x)))

        def reseeded_F(x):
            pred8 = A.to_parts(x)
            zr, rsd = e["rs"].reseed(q4_of_o(pred8))
            return A.omax(e["po"].residual_o(with_horizon(pred8, zr, e["rs"]))) if rsd["ok"] else None

        def rel(u, v):
            d = A.vadd(u, v, -1)
            i = max(range(len(d)), key=lambda j: abs(d[j]))
            return dict(rel_max=float(A.vmax(d) / A.vmax(v)), at=i, of=len(d), delta_rel=float(abs(d[-1]) / abs(v[-1])))
        say("F_state_at_target_unreseeded", F_of(x0))

        # (A) the fixed-D Newton from the state itself (--qd_it solves), refused where the re-seed cannot project the start
        ta = time.time()
        xn, Dn, conv, ra = sysm.correct(x0, Dd, tz, tD, border=False)
        say("A_newton_from_state", dict(converged=bool(conv), its=ra["its"], F=ra["F"], F_start_reseeded=ra["F_pred"],
                                        why=ra.get("why"), seconds=round(time.time() - ta, 1), reseed=ra.get("reseed")))

        # (B) the D-series' prediction at the target by order k (sum of w_m (D - D_0)^m, m <= k): the re-seeded start's max|F|
        h = Dd - D0
        Pk = {k: A.horner(W[:k + 1], h) for k in KS}
        pb = {}
        for k in KS:
            pb[k] = dict(F_unreseeded=F_of(Pk[k]), F_reseeded=reseeded_F(Pk[k]))
            say(f"B_order_{k}", pb[k])
        P2 = Pk[opt["N"]]
        P1 = A.vadd(xp, tz, (Dd - Dp) / tD)
        say("B_arclength", dict(F_unreseeded=F_of(P1), F_reseeded=reseeded_F(P1), vs_Dseries=rel(P1, P2)))

        # (D) the fixed-D Newton from the full D-series' prediction, --qd_it (60) solves
        td = time.time()
        xd, Dd2, convd, rd = sysm.correct(P2, Dd, tz, tD, border=False)
        say("D_newton_from_prediction", dict(converged=bool(convd), its=rd["its"], F=rd["F"], F_start_reseeded=rd["F_pred"],
                                             why=rd.get("why"), seconds=round(time.time() - td, 1)))
        xs = xn if conv else (xd if convd else None)
        if xs is not None:
            say("miss", dict(solution_from="state" if conv else "prediction", state=rel(x0, xs),
                             **{f"order_{k}": rel(Pk[k], xs) for k in KS}, arclength=rel(P1, xs)))
            if conv and convd:
                say("A_vs_D_solution", rel(xn, xd))
            if cfg["ref"]:
                zr_, mr = load_o(os.path.join(raw, cfg["ref"]))
                say("solution_vs_accepted", rel(xs, A.to_mp_vec(zr_)))

        # (C) the chain's own attempt replayed (bordered, the chain's --qd_it 20)
        opt["qd_it"] = 20
        tc = time.time()
        xc, Dc, convc, rc = sysm.correct(xp, Dp, tz, tD, border=True)
        itsr = [(h_["F"], h_["lam"]) for h_ in crec["its"]]
        itsn = [(h_["F"], h_["lam"]) for h_ in rc["its"]]
        say("C_chain_attempt", dict(converged=bool(convc), F_pred=rc["F_pred"], F_pred_record=crec["F_pred"],
                                    F_pred_same=rc["F_pred"] == crec["F_pred"], its=rc["its"], its_same=itsr == itsn,
                                    converged_record=att["converged"], seconds=round(time.time() - tc, 1), seconds_record=crec["seconds"]))
    say("done", dict(seconds=round(time.time() - t0, 1)))
    return 0


def main():
    import arclength
    arclength.run_chain = run_case
    import anm_run
    sys.argv = ["anm_run.py"] + sys.argv[1:]
    anm_run.main()


if __name__ == "__main__":
    main()

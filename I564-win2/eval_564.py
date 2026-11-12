#!/usr/bin/env python3
"""#564: evaluation of the antiphase model's registered predictions (predictions_564.json, committed at raw 950e85a6 and posted on #564 before any state of #558 was read) against #558's twelve states D 203.63 to 198.13.
usage: python eval_564.py [--selftest]       (run from I564-win2 after #558's chain; reads predictions_564.json, ../I558-win2/eq_D*.log, ../I557-win2/joint_557.py and what it needs)
Reported: for M0 (the issue's model, a constant in T) and M1 (T with a linear term), the rms of ln sigma_a and ln sigma_b over the twelve states, predicted minus measured, and its split into the sum (S) and the difference (T)
errors; beside them the separate cubic fits (the p2 chirp with a cubic trend fitted to the same 63 states, one per series). Acceptance of #564: the rms of ln sigma_1 and ln sigma_2 at most 0.014; both models are judged.
The file predictions_564.json is checked against the committed one (git show 950e85a6) before it is used.
--selftest: a prediction shifted by +0.02 is flagged against the 0.014 limit and an exact one is not."""
import json, math, os, subprocess, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
for p in ("I558-win2", "I557-win2", "I535-win2", "I533-win2", "I525-win2", "I522-win2", "I521-win2", "I505-win2"):
    sys.path.insert(0, os.path.join(HERE, "..", p))
import joint_557 as j  # noqa: E402
import period_558 as p8  # noqa: E402
import period_p2_533 as m  # noqa: E402
LIMIT = 0.014
COMMIT = "950e85a6"


def rms(e):
    return float(math.sqrt(np.mean(np.asarray(e) ** 2)))


def selftest():
    y = np.linspace(-90, -80, 12)
    ok = rms(y + 0.02 - y) > LIMIT and rms(y - y) <= LIMIT
    print("selftest: ok" if ok else "selftest FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    path = os.path.join(HERE, "predictions_564.json")
    committed = subprocess.run(["git", "-C", "D:/choptuik-large-d-raw-push", "show", f"{COMMIT}:I564-win2/predictions_564.json"], capture_output=True)
    same = committed.returncode == 0 and json.load(open(path)) == json.loads(committed.stdout)
    print(f"predictions_564.json equals the version committed at {COMMIT}: {'yes' if same else 'NO'}")
    pred = json.load(open(path))
    new = p8.collect_new()
    Dn = np.array(sorted(new, reverse=True))
    Yn = np.array([np.mean(new[d], axis=0) for d in Dn])
    assert np.allclose(Dn, np.array(pred["D_new"]), atol=1e-3), (Dn, pred["D_new"])
    print(f"{len(Dn)} measured states D {Dn[0]:.4f} to {Dn[-1]:.4f}")
    Do, Yo = j.all_states()
    F = m.Fitter(Do, 3)
    res = {}
    print("\n| model | series | prediction rms | max abs error | mean error (predicted minus measured) | meets 0.014 |\n|---|---|---|---|---|---|")
    for mname in ("M0", "M1"):
        for pair, (ia, ib) in (("12", (0, 1)), ("34", (2, 3))):
            P = pred["models"][mname][pair]
            for k, (idx, key) in enumerate(((ia, "pred_a"), (ib, "pred_b"))):
                e = np.array(P[key]) - Yn[:, idx]
                res[(mname, idx + 1)] = rms(e)
                print(f"| {mname} | sigma_{idx + 1} | {rms(e):.4f} | {np.max(np.abs(e)):.4f} | {np.mean(e):+.4f} | {'yes' if rms(e) <= LIMIT else 'no'} |")
    for i in (1, 2, 3, 4):
        best, f0 = F.fit_free(Yo[:, i - 1])
        e = m.predict(Dn, Do, Yo[:, i - 1], 3, best["theta"]) - Yn[:, i - 1]
        res[("sep", i)] = rms(e)
        print(f"| separate cubic p2 chirp | sigma_{i} | {rms(e):.4f} | {np.max(np.abs(e)):.4f} | {np.mean(e):+.4f} | {'yes' if rms(e) <= LIMIT else 'no'} |")
    print("\nsplit of the M1 error into the sum and the difference (half of each enters a series: e_a = (eS - eT) / 2, e_b = (eS + eT) / 2)")
    print("| pair | rms of the sum error eS | rms of the difference error eT | eS / 2 | eT / 2 |\n|---|---|---|---|---|")
    for pair, (ia, ib) in (("12", (0, 1)), ("34", (2, 3))):
        P = pred["models"]["M1"][pair]
        eS = (np.array(P["pred_a"]) + np.array(P["pred_b"])) - (Yn[:, ia] + Yn[:, ib])
        eT = (np.array(P["pred_b"]) - np.array(P["pred_a"])) - (Yn[:, ib] - Yn[:, ia])
        print(f"| sigma_{ia + 1}, sigma_{ib + 1} | {rms(eS):.4f} | {rms(eT):.4f} | {rms(eS) / 2:.4f} | {rms(eT) / 2:.4f} |")
    print("\nper-state errors of M1 (predicted minus measured) for sigma_1 and sigma_2")
    P = pred["models"]["M1"]["12"]
    print("| D | measured ln sigma_1 | error | measured ln sigma_2 | error |\n|---|---|---|---|---|")
    for k, d in enumerate(Dn):
        print(f"| {d:.4f} | {Yn[k, 0]:.3f} | {P['pred_a'][k] - Yn[k, 0]:+.4f} | {Yn[k, 1]:.3f} | {P['pred_b'][k] - Yn[k, 1]:+.4f} |")
    for mname in ("M0", "M1"):
        ok = res[(mname, 1)] <= LIMIT and res[(mname, 2)] <= LIMIT
        print(f"\nacceptance of #564 for {mname} (sigma_1 {res[(mname, 1)]:.4f}, sigma_2 {res[(mname, 2)]:.4f}, limit {LIMIT}): {'pass' if ok else 'FAIL'}")
    print(f"separate cubic fits: sigma_1 {res[('sep', 1)]:.4f}, sigma_2 {res[('sep', 2)]:.4f}")

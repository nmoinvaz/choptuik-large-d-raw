#!/usr/bin/env python3
"""prec_verdict.py DIR | --selftest [--mutate]   (#1025 prec_kc111_d21125; the verdict rule written in the README before the first run)

Reads DIR/prec_k<KC>_lam<LAM>.jsonl (one record per lambda, from d18_hybsign_prec.py) and prints, per lambda, the hybrid sign and ln|det|, the sign under noise 1e-15 / 1e-12 / 1e-10 (2 seeds), the all-double-double sign and ln|det|, the float64 sign
and the script's reading (robust / state-limited / rounding-limited), then the control and the verdict.
CONTROL c4 (against dh170's own hybrid rows at D 21.125, pinned in inputs/): at lambda 0.860, 0.865, 0.870 and 0.875 (k_c 111; rows of dh170's raw I1025-dh170/kc111_d21125_low, merged_all, blob 10da3d2b, the same state blob edbb419e) and 0.880 and 0.885 (k_c 103) the hybrid sign here equals dh170's and |ln here - ln there| <= 1e-3. A sign that differs = the control FAILS, no verdict;
an ln that differs by more than 1e-3 with the sign equal is printed as a platform difference of the hybrid ln (information, not a failure).
VERDICT (registered): the points beside the roots are k_c 111 0.865, 0.870 and k_c 103 0.880, 0.885.
  'real'      : every point beside the roots that exists reads robust AND the hybrid signs change between 0.865 and 0.870 (k_c 111, when both exist) and between 0.880 and 0.885 (k_c 103, when both exist);
  'numerical' : at least one point beside the roots reads state-limited or rounding-limited (the roots are then not resolved at the 0.005 grid);
  'undecided' : otherwise (a point missing, or robust without the sign change); the outer k_c 111 points 0.860 and 0.875 are printed and counted only as information.
--selftest: planted record sets (all robust with the changes; one state-limited beside a root; one rounding-limited; robust without a change; a control sign failure) must classify as written; --mutate makes 'numerical' impossible (the verdict says 'real' whenever the signs change),
which the planted state-limited case must catch (exit 1)."""
import glob
import json
import os
import sys

MUT = "--mutate" in sys.argv
BESIDE = {111: (0.865, 0.870), 103: (0.880, 0.885)}
CTRL = {111: (0.860, 0.865, 0.870, 0.875), 103: (0.880, 0.885)}   # k_c 111: 0.860 and 0.865 from dh170's kc111_d21125_low (the coordinator, 25 Nov ~15:15 UTC), 0.870 and 0.875 from his kc111_d21125


def reading(r):
    out = []
    if any(float(a) >= 1e-12 and any(s != r["sign"] for s in ss) for a, ss in r["noise"].items()):
        out.append("state-limited")
    if r.get("alldd_sign") is not None and r["alldd_sign"] != r["sign"]:
        out.append("rounding-limited")
    return ",".join(out) or "robust"


def verdict(recs, ref):
    """recs: {(kc, lam): record}; ref: {(kc, lam): (sign, ln)} dh170's rows. Returns (control_ok, verdict, lines)"""
    lines = []
    ok = True
    for (kc, lam), r in sorted(recs.items()):
        lines.append("k_c %d lambda %.3f: hybrid %+d ln %.6f | noise %s | all-dd %s ln %s | float64 %+d | reading %s | %s s" % (
            kc, lam, r["sign"], r["ln"], {a: [int(s) for s in ss] for a, ss in r["noise"].items()},
            ("%+d" % r["alldd_sign"]) if r.get("alldd_sign") is not None else "n/a", ("%.6f" % r["alldd_ln"]) if r.get("alldd_ln") is not None else "n/a", r["f64_sign"], reading(r), r.get("sec")))
    for kc in CTRL:
        for lam in CTRL[kc]:
            r = recs.get((kc, lam)); b = ref.get((kc, lam))
            if r is None or b is None:
                continue
            if int(r["sign"]) != int(b[0]):
                ok = False
                lines.append("CONTROL c4 FAILS at k_c %d lambda %.3f: hybrid sign %+d here, %+d in dh170's row" % (kc, lam, r["sign"], b[0]))
            elif abs(r["ln"] - b[1]) > 1e-3:
                lines.append("c4 information at k_c %d lambda %.3f: the sign agrees, the hybrid ln differs by %.3e (%.6f here, %.6f in dh170's row)" % (kc, lam, r["ln"] - b[1], r["ln"], b[1]))
            else:
                lines.append("c4 at k_c %d lambda %.3f: sign and ln agree with dh170's row (diff %.1e)" % (kc, lam, r["ln"] - b[1]))
    if not ok:
        return False, "control failed: no verdict", lines
    beside = [(kc, lam) for kc in BESIDE for lam in BESIDE[kc] if (kc, lam) in recs]
    bad = [(kc, lam) for kc, lam in beside if reading(recs[(kc, lam)]) != "robust"]
    changes = []
    for kc in BESIDE:
        a, b = BESIDE[kc]
        if (kc, a) in recs and (kc, b) in recs:
            changes.append((kc, int(recs[(kc, a)]["sign"]) != int(recs[(kc, b)]["sign"])))
    if bad and not MUT:
        v = "numerical (not robust beside a root: %s)" % ", ".join("k_c %d lambda %.3f %s" % (kc, lam, reading(recs[(kc, lam)])) for kc, lam in bad)
    elif beside and len(beside) == 4 and all(c for _, c in changes) and len(changes) == 2:
        v = "real (all four points beside the roots robust, the hybrid signs change between 0.865 and 0.870 at k_c 111 and between 0.880 and 0.885 at k_c 103)"
    else:
        v = "undecided (beside-root points present: %d of 4; sign changes: %s)" % (len(beside), changes)
    return True, v, lines


def load(d):
    recs = {}
    for f in glob.glob(os.path.join(d, "prec_k*_lam*.jsonl")):
        for l in open(f):
            if l.strip():
                r = json.loads(l)
                recs[(int(r["kc"]), round(float(r["lam"]), 3))] = r
    return recs


def load_ref(d):
    ref = {}
    for kc, f in ((111, "inputs/kc111/dh170_low_merged_all_D21.125.jsonl"), (103, "inputs/kc103/dh170_merged_D21.125.jsonl")):
        p = os.path.join(d, f)
        if os.path.exists(p):
            for l in open(p):
                if l.strip():
                    r = json.loads(l)
                    ref[(kc, round(float(r["lam"]), 3))] = (int(r["sign"]), float(r["ln"]))
    return ref


def selftest():
    def rec(kc, lam, sign, noise_flip=False, dd_flip=False, ln=-3000.0):
        n = {"1e-15": [sign, sign], "1e-12": [sign, sign], "1e-10": [sign, -sign if noise_flip else sign]}
        return dict(kc=kc, lam=lam, sign=sign, ln=ln, noise=n, f64_sign=sign, alldd_sign=-sign if dd_flip else sign, alldd_ln=ln, sec=1)
    ref = {(111, 0.870): (1, -3000.0), (111, 0.875): (1, -3000.0), (103, 0.880): (1, -3000.0), (103, 0.885): (-1, -3000.0)}
    def mk(**kw):
        d = {(111, 0.865): rec(111, 0.865, -1), (111, 0.870): rec(111, 0.870, 1), (111, 0.875): rec(111, 0.875, 1), (103, 0.880): rec(103, 0.880, 1), (103, 0.885): rec(103, 0.885, -1)}
        d.update(kw)
        return d
    bad = []
    cases = [
        ("all robust with the changes", mk(), "real"),
        ("state-limited beside the k_c 111 root", mk(**{"x": None}) if False else {**mk(), (111, 0.865): rec(111, 0.865, -1, noise_flip=True)}, "numerical"),
        ("rounding-limited beside the k_c 103 root", {**mk(), (103, 0.885): rec(103, 0.885, -1, dd_flip=True)}, "numerical"),
        ("robust, no change at k_c 111", {**mk(), (111, 0.865): rec(111, 0.865, 1)}, "undecided"),
        ("control sign failure", {**mk(), (103, 0.880): rec(103, 0.880, -1)}, "control failed"),
        ("one point missing", {k: v for k, v in mk().items() if k != (103, 0.885)}, "undecided"),
    ]
    for name, recs, want in cases:
        okc, v, _ = verdict(recs, ref)
        if not v.startswith(want):
            bad.append("%s: %r (wanted %s)" % (name, v, want))
    for b in bad:
        print("SELFTEST FAIL:", b)
    print("selftest %s" % ("FAILS" if bad else "passes"))
    return 1 if bad else 0


def main():
    if "--selftest" in sys.argv:
        return selftest()
    d = [a for a in sys.argv[1:] if not a.startswith("--")][0]
    recs = load(d)
    okc, v, lines = verdict(recs, load_ref(d))
    print("\n".join(lines))
    print("points: %d" % len(recs))
    print("VERDICT: %s" % v)
    return 0


if __name__ == "__main__":
    sys.exit(main())

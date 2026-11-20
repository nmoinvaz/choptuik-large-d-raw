#!/usr/bin/env python3
"""#1025 (win): the coordinator's checks of an ell_refine.py record of lambda (2026-11-20).
    python check_1025.py REC.jsonl D [--ref V] [--rule pct|edge]    report the record at D in REC.jsonl; exit 0 when its rule passes, else 1
    python check_1025.py --selftest                                  planted records, and each rule's failure case
ell_refine.py's lam_root takes grid = guess * (1 + w * [-1, 0, 1]) for w in (0.02, 0.06, 0.15, 0.35), the first w with a sign change of det M between
neighbouring grid points, then brentq inside that interval [grid[i], grid[i+1]] (the record keeps lam_guess, lam, n_signchanges, n_eval, not w).
w is derived here as the first of those whose grid holds lam, and the interval is the one that holds lam (assumes no other root in a smaller grid).
Both rules need n_signchanges == 1. Rule pct (D 16.5, whose guess is the same-D k_c 55 lambda): |lam - guess| / guess <= 2%.
Rule edge (D 17.5, whose guess is the previous D's lambda): the root is not at its interval's edge, i.e. its distance to each edge is at least 0.05 grid steps
(0.05 is this script's choice; the distances are printed so any other bar can be read off)."""
import json
import sys

WS = (0.02, 0.06, 0.15, 0.35)
EDGE_BAR = 0.05
PCT_BAR = 0.02


def analyse(r, ref=None):
    g, lam = r["lam_guess"], r["lam"]
    out = dict(D=r["D"], kc=r["kc"], guess=g, lam=lam, n_signchanges=r["n_signchanges"], n_eval=r.get("n_eval"),
               rel_to_guess=(lam - g) / g)
    w = next((w for w in WS if g * (1 - w) <= lam <= g * (1 + w)), None)
    out["w"] = w
    if w is not None:
        grid = [g * (1 + w * s) for s in (-1.0, 0.0, 1.0)]
        i = 0 if lam < g else 1
        lo, hi = grid[i], grid[i + 1]
        step = g * w
        out.update(grid=grid, interval=(lo, hi), step=step, d_lo=(lam - lo) / step, d_hi=(hi - lam) / step)
    if ref is not None:
        out.update(ref=ref, d_ref=lam - ref, d_ref_rel=(lam - ref) / ref)
    out["one_change"] = out["n_signchanges"] == 1
    out["pct_ok"] = abs(out["rel_to_guess"]) <= PCT_BAR
    out["edge_ok"] = w is not None and min(out["d_lo"], out["d_hi"]) >= EDGE_BAR
    return out


def report(a, rule):
    print(f"D {a['D']}  k_c {a['kc']}: lam {a['lam']:.9f}, guess {a['guess']:.9f} ({100 * a['rel_to_guess']:+.3f}% from it), n_eval {a['n_eval']}")
    print(f"  n_signchanges {a['n_signchanges']} -> {'OK (1)' if a['one_change'] else 'SUSPECT (must be 1)'}")
    if a["w"] is None:
        print("  bracket: lam lies outside every grid guess*(1 +- w), w in (0.02, 0.06, 0.15, 0.35): cannot be derived -> SUSPECT")
    else:
        lo, hi = a["interval"]
        print(f"  bracket: w {a['w']}, grid {a['grid'][0]:.6f}, {a['grid'][1]:.6f}, {a['grid'][2]:.6f} (step {a['step']:.6f}); root in [{lo:.6f}, {hi:.6f}]: "
              f"{a['d_lo']:.3f} grid steps from the lower edge, {a['d_hi']:.3f} from the upper")
    if "ref" in a:
        print(f"  Mac's k_c 55 value {a['ref']:.7f}: lam - ref {a['d_ref']:+.3e} ({100 * a['d_ref_rel']:+.3f}%)")
    print(f"  2% test (|lam - guess| <= 2%): {'pass' if a['pct_ok'] else 'fail'};  edge test (>= {EDGE_BAR} steps from both edges): {'pass' if a['edge_ok'] else 'fail'}")
    ok = a["one_change"] and (a["pct_ok"] if rule == "pct" else a["edge_ok"])
    print(f"  rule {rule}: {'PASS' if ok else 'SUSPECT, not to be used'}")
    return ok


def selftest():
    bad = 0

    def rec(g, lam, n=1):
        return dict(D=1.0, kc=63, lam_guess=g, lam=lam, n_signchanges=n, n_eval=10)
    cases = [   # name, record, ref, rule, expected pass, expected w, d_lo, d_hi
        ("planted: guess 2.0, root 1.95 (2.5% away, w 0.06), edge rule", rec(2.0, 1.95), None, "edge", True, 0.06, 0.5833, 0.4167),
        ("planted: guess 2.0, root 1.99 (0.5% away, w 0.02), pct rule", rec(2.0, 1.99), None, "pct", True, 0.02, 0.75, 0.25),
        ("control: two sign changes", rec(2.0, 1.99, 2), None, "pct", False, 0.02, 0.75, 0.25),
        ("control: root at the bracket's edge (1.8800001, w 0.06)", rec(2.0, 1.8800001), None, "edge", False, 0.06, None, None),
        ("control: 2.5% from the guess under the pct rule", rec(2.0, 1.95), None, "pct", False, 0.06, None, None),
        ("planted: root above the guess (2.03, w 0.02)", rec(2.0, 2.03), None, "edge", True, 0.02, 0.75, 0.25),
    ]
    for name, r, ref, rule, want, w, dlo, dhi in cases:
        a = analyse(r, ref)
        ok = (a["one_change"] and (a["pct_ok"] if rule == "pct" else a["edge_ok"])) == want and a["w"] == w
        if dlo is not None:
            ok = ok and abs(a["d_lo"] - dlo) < 1e-3 and abs(a["d_hi"] - dhi) < 1e-3
        print(f"  {name}: pass {want} expected, w {a['w']}, {'ok' if ok else 'WRONG'}")
        bad += not ok
    a = analyse(rec(2.0, 1.95), 1.9522)
    ok = abs(a["d_ref"] + 0.0022) < 1e-12 and abs(a["d_ref_rel"] + 0.0022 / 1.9522) < 1e-12
    print(f"  distance to a reference value: {a['d_ref']:+.4f} {'ok' if ok else 'WRONG'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("path"); ap.add_argument("D", type=float)
    ap.add_argument("--ref", type=float, default=None); ap.add_argument("--rule", choices=("pct", "edge"), default="edge")
    a = ap.parse_args()
    recs = [json.loads(l) for l in open(a.path) if l.strip()]
    r = next((x for x in recs if abs(x["D"] - a.D) < 1e-9 and x.get("lam")), None)
    if r is None:
        sys.exit(f"no record with lam at D {a.D} in {a.path}")
    sys.exit(0 if report(analyse(r, a.ref), a.rule) else 1)


if __name__ == "__main__":
    main()

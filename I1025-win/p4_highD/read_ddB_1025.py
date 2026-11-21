#!/usr/bin/env python3
"""#1025 winb follow-on: the dd sign check of a hybrid root (the coordinator's amendment of 2026-11-21 06:30 UTC and his Amendment 3 of 07:33 UTC).
usage: read_ddB_1025.py LO.jsonl HI.jsonl ROOT [HYBRID.jsonl]    (the det records of ell_ddm.py det at ROOT - 0.02 and ROOT + 0.02; HYBRID.jsonl defaults to
the follow-on's own ell_p4_hybrid_1025_w_highD.jsonl; the hybrid record is the one at the det records' D)
A dd sign COUNTS at a lambda if its 5 exact variants agree and relative noise 1e-24 on the dd propagator entries leaves it unchanged (both seeds), as in
raw I1025-mac/dd_signtest_D17.5_criteria.log and d18_dd_criteria.log; the noise at 1e-20 and 1e-16 is information.
Reading, Amendment 3 (the coordinator's, ruled at 07:33 UTC before any dd result existed; v1, read_ddB_1025_v1.py, had minus-lower/plus-upper only):
the root passes if the two counting dd signs are opposite, in either orientation, and each equals the hybrid's sign at the hybrid evaluation nearest
that point. The same sign at both: no root between them. A sign that does not count at either point: neither reading applies, and that is reported.
Opposite counting signs that differ from the hybrid's at the nearest evaluation are reported as the dd disagreeing with the hybrid (no pass).
The orientation (minus below and plus above, or plus below and minus above) is printed as information."""
import json, sys
OUTJS = "C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD/ell_p4_hybrid_1025_w_highD.jsonl"
def rec(fn, D=None):
    r = [json.loads(l) for l in open(fn) if l.strip()]
    r = [x for x in r if D is None or abs(x["D"] - D) < 1e-9]
    return r[-1] if r else None
lo, hi, root = rec(sys.argv[1]), rec(sys.argv[2]), float(sys.argv[3])
hyb = rec(sys.argv[4] if len(sys.argv) > 4 else OUTJS, (lo or hi)["D"])
if hyb is None:
    sys.exit(f"no hybrid record at D {(lo or hi)['D']} in {sys.argv[4] if len(sys.argv) > 4 else OUTJS}")
ev = {float(k): v["sign"] for k, v in hyb["evals"].items()}
def sign(r):
    if r is None:
        return None, False, "no record"
    s = {x["sign"] for x in r["dd"]}
    agree = len(s) == 1
    n24 = [e for e in (r.get("noise") or []) if abs(e["eps"] - 1e-24) < 1e-30]
    n24ok = bool(n24) and all(x == r["dd"][0]["sign"] for x in n24[0]["signs"])
    info = {f"{e['eps']:g}": e["signs"] for e in (r.get("noise") or [])}
    return (r["dd"][0]["sign"] if agree else None), (agree and n24ok), f"5 variants {[x['sign'] for x in r['dd']]} agree {agree}, noise {info}, ln|det| {r['dd'][0]['ln']:.10f}, float64 sign {r.get('f64_sign')}"
def nearest(x):
    k = min(ev, key=lambda k: abs(k - x))
    return k, ev[k]
(sl, cl, tl), (sh, ch, th) = sign(lo), sign(hi)
xl, xh = root - 0.02, root + 0.02
(kl, hl), (kh, hh) = nearest(xl), nearest(xh)
mism = [n for n, r, x in (("lower", lo, xl), ("upper", hi, xh)) if r is not None and abs(r["lam"] - x) > 1e-9]
print(f"root {root!r}: lower point {xl!r} (record lam {lo and lo['lam']!r}): dd sign {sl}, counts {cl}; {tl}")
print(f"           upper point {xh!r} (record lam {hi and hi['lam']!r}): dd sign {sh}, counts {ch}; {th}")
print(f"hybrid sign at the evaluation nearest the lower point: {hl} at {kl!r} ({kl - xl:+.3e} away); nearest the upper point: {hh} at {kh!r} ({kh - xh:+.3e} away)")
ori = lambda a, b: {(-1.0, 1.0): "minus below, plus above (the usual one)", (1.0, -1.0): "plus below, minus above"}.get((a, b), "same sign")
if mism:
    out = "NEITHER READING APPLIES: the record lambda differs from root -/+ 0.02 at the " + " and ".join(mism) + " point"
elif not (cl and ch):
    out = "NEITHER READING APPLIES: a dd sign does not count at " + ("the lower" if not cl else "") + (" and " if not (cl or ch) else "") + ("the upper" if not ch else "") + " point"
elif sl == sh:
    out = f"NO ROOT BETWEEN THEM: the same sign ({sl:+.0f}) at both points"
elif sl == hl and sh == hh:
    out = f"ROOT PASSES: the counting dd signs are opposite and equal the hybrid's nearest signs; orientation {ori(sl, sh)}"
else:
    out = f"DD DISAGREES WITH THE HYBRID: opposite dd signs ({sl:+.0f}, {sh:+.0f}) but the hybrid's nearest signs are ({hl:+.0f}, {hh:+.0f}); no pass"
print("DDREAD:", out)

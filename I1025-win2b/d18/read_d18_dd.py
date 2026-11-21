#!/usr/bin/env python3
"""#1025 D 18 upper root: the dd sign check, read as winb's Amendment 3 (raw I1025-win/p4_highD/read_ddB_1025.py v2, which hard-codes the offset 0.02; here it is a parameter, 0.005).
usage: read_d18_dd.py LO.jsonl HI.jsonl ROOT HYBRID.jsonl [OFF]   |   read_d18_dd.py selftest
A dd sign COUNTS if its 5 exact variants agree and 1e-24 relative noise on the dd propagator entries (both seeds) leaves it unchanged (1e-20 and 1e-16 are information).
The root passes if the two counting dd signs are opposite, in either orientation, and each equals the hybrid sign at the hybrid evaluation nearest that point.
The same sign at both: no root between them. A sign that does not count: neither reading applies.
Opposite counting signs that differ from the hybrid's nearest ones: the dd disagrees with the hybrid (no pass)."""
import json, sys


def rec(fn, D=None):
    r = [json.loads(l) for l in open(fn) if l.strip()]
    r = [x for x in r if D is None or abs(x["D"] - D) < 1e-9]
    return r[-1] if r else None


def sign(r):
    if r is None:
        return None, False, "no record"
    agree = len({x["sign"] for x in r["dd"]}) == 1
    n24 = [e for e in (r.get("noise") or []) if abs(e["eps"] - 1e-24) < 1e-30]
    n24ok = bool(n24) and all(x == r["dd"][0]["sign"] for x in n24[0]["signs"])
    info = {f"{e['eps']:g}": e["signs"] for e in (r.get("noise") or [])}
    return ((r["dd"][0]["sign"] if agree else None), (agree and n24ok),
            f"5 variants {[x['sign'] for x in r['dd']]} agree {agree}, noise {info}, ln|det| {r['dd'][0]['ln']:.10f}, float64 sign {r.get('f64_sign')}")


def read(lo, hi, root, hyb, off=0.005, verbose=True):
    ev = {float(k): v["sign"] for k, v in hyb["evals"].items()}
    (sl, cl, tl), (sh, ch, th) = sign(lo), sign(hi)
    xl, xh = root - off, root + off

    def nearest(x):
        k = min(ev, key=lambda k: abs(k - x))
        return k, ev[k]
    (kl, hl), (kh, hh) = nearest(xl), nearest(xh)
    mism = [n for n, r, x in (("lower", lo, xl), ("upper", hi, xh)) if r is not None and abs(r["lam"] - x) > 1e-9]
    if verbose:
        print(f"root {root!r}: lower point {xl!r} (record lam {lo and lo['lam']!r}): dd sign {sl}, counts {cl}; {tl}")
        print(f"           upper point {xh!r} (record lam {hi and hi['lam']!r}): dd sign {sh}, counts {ch}; {th}")
        print(f"hybrid sign at the evaluation nearest the lower point: {hl} at {kl!r} ({kl - xl:+.3e} away); "
              f"nearest the upper point: {hh} at {kh!r} ({kh - xh:+.3e} away)")
    ori = {(-1.0, 1.0): "minus below, plus above (the usual one)", (1.0, -1.0): "plus below, minus above"}
    if mism:
        return "NEITHER READING APPLIES: the record lambda differs from root -/+ offset at the " + " and ".join(mism) + " point"
    if not (cl and ch):
        return "NEITHER READING APPLIES: a dd sign does not count at " + " and ".join(n for n, c in (("the lower", cl), ("the upper", ch)) if not c) + " point"
    if sl == sh:
        return f"NO ROOT BETWEEN THEM: the same sign ({sl:+.0f}) at both points"
    if sl == hl and sh == hh:
        return f"ROOT PASSES: the counting dd signs are opposite and equal the hybrid's nearest signs; orientation {ori.get((sl, sh), 'same sign')}"
    return f"DD DISAGREES WITH THE HYBRID: opposite dd signs ({sl:+.0f}, {sh:+.0f}) but the hybrid's nearest signs are ({hl:+.0f}, {hh:+.0f}); no pass"


if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    ROOT = 1.8063

    def hyb(flip=False):
        s = -1.0 if flip else 1.0
        return dict(D=18.0, evals={"1.7885": dict(sign=s), "1.825": dict(sign=-s), "1.8615": dict(sign=-s),
                                   "1.80629999": dict(sign=s), "1.80630001": dict(sign=-s)})

    def det(lam, sign, agree=True, n24=None):
        n24 = [sign, sign] if n24 is None else n24
        sg = [sign] * 5 if agree else [sign, sign, -sign, sign, sign]
        return dict(D=18.0, kc=63, lam=lam, dd=[dict(sign=x, ln=-1925.0, sec=1.0) for x in sg],
                    noise=[dict(eps=1e-24, signs=n24), dict(eps=1e-20, signs=[sign, sign]), dict(eps=1e-16, signs=[sign, sign])], f64_sign=1.0)
    L, H = ROOT - 0.005, ROOT + 0.005
    cases = [("upper-root orientation, hybrid +,-; dd +,-", det(L, 1.0), det(H, -1.0), hyb(), "ROOT PASSES"),
             ("usual orientation, hybrid -,+; dd -,+", det(L, -1.0), det(H, 1.0), hyb(True), "ROOT PASSES"),
             ("dd +,+", det(L, 1.0), det(H, 1.0), hyb(), "NO ROOT"),
             ("dd -,-", det(L, -1.0), det(H, -1.0), hyb(), "NO ROOT"),
             ("dd -,+ against hybrid +,-", det(L, -1.0), det(H, 1.0), hyb(), "DD DISAGREES"),
             ("a variant disagrees at the lower", det(L, 1.0, agree=False), det(H, -1.0), hyb(), "NEITHER"),
             ("1e-24 noise flips the upper", det(L, 1.0), det(H, -1.0, n24=[-1.0, 1.0]), hyb(), "NEITHER"),
             ("record lambda is root -/+ 0.02, not 0.005", det(ROOT - 0.02, 1.0), det(H, -1.0), hyb(), "NEITHER")]
    bad = 0
    for name, lo, hi, h, want in cases:
        got = read(lo, hi, ROOT, h, verbose=False)
        ok = got.startswith(want)
        bad += not ok
        print(f"selftest {name}: {got[:58]} (want {want}) {'ok' if ok else 'WRONG'}")
    print("selftest", "passes" if bad == 0 else f"FAILS ({bad} wrong)")
    sys.exit(1 if bad else 0)
lo, hi, root = rec(sys.argv[1]), rec(sys.argv[2]), float(sys.argv[3])
off = float(sys.argv[5]) if len(sys.argv) > 5 else 0.005
hyb = rec(sys.argv[4], (lo or hi)["D"])
msg = read(lo, hi, root, hyb, off)
print("DDREAD:", msg)
sys.exit(0 if msg.startswith("ROOT PASSES") else 1)

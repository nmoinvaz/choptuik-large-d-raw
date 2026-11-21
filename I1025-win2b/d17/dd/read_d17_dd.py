#!/usr/bin/env python3
"""#1025 D 17 k_c 71: the reading of the two dd det points (README.md, fixed before the run). A dd sign counts if its 5 variants agree and 1e-24 relative noise (both seeds)
leaves it unchanged (the 1e-20 and 1e-16 noise are information). Minus at the lower point and plus at the upper: the root passes, k_c error lam71(17) - 2.0399399392 = +8.637e-5.
The same counted sign at both: no root between them. A point whose sign does not count: no reading. usage: read_d17_dd.py LO.jsonl HI.jsonl | read_d17_dd.py selftest"""
import json, sys
HYB, REF63 = 2.0400263140919073, 2.0399399392


def counts(r):
    n24 = [e for e in r["noise"] if abs(e["eps"] - 1e-24) < 1e-30]
    return bool(r["dd_agree"]) and len(n24) == 1 and all(s == r["dd"][0]["sign"] for s in n24[0]["signs"])


def reading(lo, hi):
    cl, ch = counts(lo), counts(hi)
    sl, sh = lo["dd"][0]["sign"], hi["dd"][0]["sign"]
    if not (cl and ch):
        return "NO READING: " + ", ".join(n for n, c in (("lower", cl), ("upper", ch)) if not c) + " sign does not count"
    if sl < 0 and sh > 0:
        return f"ROOT PASSES: minus at the lower point, plus at the upper; the k_c error at D 17 is {HYB - REF63:+.3e}"
    if sl == sh:
        return f"NO ROOT between them: the same counted sign ({sl:+.0f}) at both"
    return f"OPPOSITE signs in the other order (plus below, minus above): not the root's pattern ({sl:+.0f} at the lower, {sh:+.0f} at the upper)"


def rec(lam, sign, agree=True, n24=None, lvl=None):
    n24 = [sign, sign] if n24 is None else n24
    return dict(D=17.0, kc=71, lam=lam, dd_agree=agree, dd=[dict(sign=sign, ln=-2200.0, sec=1.0)] * 5, f64_sign=sign, f64_ln=-2200.0,
                noise=[dict(eps=1e-24, signs=n24), dict(eps=1e-20, signs=[sign, sign]), dict(eps=1e-16, signs=[sign, sign])], noise_robust=True)


if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    cases = [("minus then plus", rec(2.02, -1.0), rec(2.06, 1.0), "ROOT PASSES"), ("plus at both", rec(2.02, 1.0), rec(2.06, 1.0), "NO ROOT"),
             ("minus at both", rec(2.02, -1.0), rec(2.06, -1.0), "NO ROOT"), ("plus then minus", rec(2.02, 1.0), rec(2.06, -1.0), "OPPOSITE"),
             ("variants disagree at the lower", rec(2.02, -1.0, agree=False), rec(2.06, 1.0), "NO READING"),
             ("1e-24 noise flips the upper", rec(2.02, -1.0), rec(2.06, 1.0, n24=[1.0, -1.0]), "NO READING"),
             ("no 1e-24 entry at the lower", dict(rec(2.02, -1.0), noise=[dict(eps=1e-20, signs=[-1.0, -1.0])]), rec(2.06, 1.0), "NO READING")]
    bad = 0
    for name, lo, hi, want in cases:
        got = reading(lo, hi); ok = got.startswith(want); bad += not ok
        print(f"selftest {name}: {got[:60]} (want {want}) {'ok' if ok else 'WRONG'}")
    print("selftest", "passes" if bad == 0 else f"FAILS ({bad} wrong)"); sys.exit(1 if bad else 0)
rows = []
for f in sys.argv[1:3]:
    rows.append([json.loads(l) for l in open(f) if l.strip()][-1])
for r in rows:
    print(f"lambda {r['lam']!r}: dd signs of the 5 variants {[x['sign'] for x in r['dd']]}, agree {r['dd_agree']}, ln|det| {r['dd'][0]['ln']:.10f}, noise signs "
          + ", ".join(f"{e['eps']:.0e} {e['signs']}" for e in r["noise"]) + f", float64 sign {r['f64_sign']:+.0f}, counts {counts(r)}")
msg = reading(*rows); print(msg); sys.exit(0 if msg.startswith("ROOT PASSES") else 1)

#!/usr/bin/env python3
"""#1025 kc71_d1925 (dh610) compare_dh170.py OURS.jsonl THEIRS.jsonl | selftest [--mutate]: the cross-machine check of the points both machines evaluated (dh170's lane 2, D 19.25, lambda
1.42 to 1.45, 4 threads, raw 7143608c, copied as in/ref_dh170_lane2_scan_D19.25_p0.jsonl) against this scan (1 thread each). Per shared lambda (keys round(lam, 4)): hybrid sign equal, noise_robust equal,
float64 sign equal where both have it, relative difference of the hybrid ln|det| (bar 1e-9, the coordinator's; information). Exit 0 if every shared point is within the bar with equal signs, 1 otherwise;
2 if no lambda is shared. A repeated lambda in OURS is compared once per row against the first row of THEIRS.
selftest: identical rows pass; a ln shift of 1e-8 relative, a sign flip, a noise_robust flip and a float64 sign flip must each fail; no shared lambda exits 2. --mutate widens the bar to 1e-6, which the
1e-8 shift case must then fail to catch (the selftest exits 1)."""
import sys, json

BAR = 1e-9


def load(f):
    return [json.loads(l) for l in open(f) if l.strip()]


def compare(ours, theirs, bar=BAR):
    th = {}
    for r in theirs:
        th.setdefault(round(r["lam"], 4), r)
    out, ok, n = [], True, 0
    for r in ours:
        k = round(r["lam"], 4)
        if k not in th:
            continue
        t = th[k]
        n += 1
        d = abs(r["ln"] - t["ln"]) / abs(t["ln"])
        good = r["sign"] == t["sign"] and bool(r["noise_robust"]) == bool(t["noise_robust"]) and r.get("f64_sign") == t.get("f64_sign") and d <= bar
        ok &= good
        out.append(f"  lam {k}: sign {r['sign']:+.0f} vs {t['sign']:+.0f}, noise_robust {r['noise_robust']} vs {t['noise_robust']}, float64 sign {r.get('f64_sign'):+.0f} vs {t.get('f64_sign'):+.0f}, "
                   f"ln|det| {r['ln']:.12f} vs {t['ln']:.12f}, relative difference {d:.3e} (bar {bar:g}): {'ok' if good else 'DIFFERENT'}")
    return (2 if n == 0 else (0 if ok else 1)), out


def selftest(mutate):
    bar = 1e-6 if mutate else BAR
    base = [dict(lam=1.42, sign=1.0, ln=-2186.7628971332033, noise_robust=True, f64_sign=1.0), dict(lam=1.43, sign=1.0, ln=-2187.2342474896022, noise_robust=True, f64_sign=1.0)]
    cp = lambda **kw: [dict(r, **kw) if i == 0 else dict(r) for i, r in enumerate(base)]
    cases = [("identical", base, 0), ("ln shift 1e-8 relative", cp(ln=base[0]["ln"] * (1 + 1e-8)), 1), ("sign flip", cp(sign=-1.0), 1),
             ("noise_robust flip", cp(noise_robust=False), 1), ("float64 sign flip", cp(f64_sign=-1.0), 1),
             ("no shared lambda", [dict(r, lam=r["lam"] + 0.5) for r in base], 2)]
    bad = 0
    for name, ours, want in cases:
        got, _ = compare(ours, base, bar)
        ok = got == want
        bad += not ok
        print(f"  {name}: exit {got} (expected {want}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        sys.exit(selftest("--mutate" in sys.argv))
    rc, out = compare(load(sys.argv[1]), load(sys.argv[2]))
    print("\n".join(out) or "  (no shared lambda)")
    print({0: "PASS: every shared point agrees (sign, noise, float64 sign, ln|det| within the bar)", 1: "DIFFERENT: see the lines above", 2: "no shared lambda"}[rc])
    sys.exit(rc)

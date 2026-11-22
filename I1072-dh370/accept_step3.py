"""#1072 step 3 acceptance (the issue's: each run ends with exactly one sign change in its bracket and |F| below 1e-27; the difference between M' 128 and M' 96 is
reported as a resolution change, not a bound; no outside target at D 3.0444). usage: accept_step3.py RECORDS.jsonl | accept_step3.py selftest [--mutate=sign|F|none_gamma]
Exit 0 only when every record passes (and at least one exists); --mutate (a control) makes the selftest fail: sign (two sign changes), F (|F| x 1e3), none_gamma (no root found)."""
import json, sys
F_BAR = 1e-27
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
args = [a for a in sys.argv[1:] if not a.startswith("--")]


def mutate(r):
    r = dict(r)
    if MUT == "sign": r["n_signchanges"] = 2
    if MUT == "F": r["F"] *= 1e3
    if MUT == "none_gamma": r["gamma"] = None
    return r


def check(recs, out=print):
    recs = [mutate(r) for r in recs]
    ok = bool(recs)
    for r in sorted(recs, key=lambda r: -r["M"]):
        good = r.get("gamma") is not None and r["n_signchanges"] == 1 and r["F"] < F_BAR
        out(f"D {r['D']} M' {r['M']} map {r.get('map')}: gamma {r.get('gamma')!r}, lambda {r.get('lam')!r}, sign changes {r['n_signchanges']}, |F| {r['F']:.2e} (bar {F_BAR:.0e}), {r['n_det']} determinants, {r['seconds']} s: {'PASS' if good else 'FAIL'}")
        ok &= good
    d = {r["M"]: r.get("gamma") for r in recs}
    if d.get(128) is not None and d.get(96) is not None:
        out(f"gamma(M' 128) - gamma(M' 96) = {d[128] - d[96]:+.3e} (a resolution change, not a bound; no outside target at this D)")
    return ok


def selftest():
    base = dict(D=3.044375, M=128, F=1e-29, n_signchanges=1, n_det=9, seconds=1.0, map=[1.96, 0.4], gamma=0.19, lam=5.2)
    cases = [("planted good", [base, dict(base, M=96)], True), ("two sign changes", [dict(base, n_signchanges=2)], False),
             ("|F| 1e-26", [dict(base, F=1e-26)], False), ("no root", [dict(base, gamma=None)], False), ("no records", [], False)]
    ok = True
    for name, recs, want in cases:
        got = check(recs, out=lambda s: None)
        print(f"planted: {name}: verdict {got}, expected {want}: {'PASS' if got == want else 'FAIL'}")
        ok &= got == want
    print("selftest:", "PASS" if ok else "FAIL")
    return ok


if args and args[0] == "selftest":
    sys.exit(0 if selftest() else 1)
recs = [json.loads(l) for l in open(args[0]) if l.strip()]
ok = check(recs)
print("ACCEPTANCE:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)

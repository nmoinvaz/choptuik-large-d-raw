"""#1072 step 2 acceptance, as the issue fixes it: for every lowD_gamma.py record of a mapped state at D 3.15, exactly one sign change in the
bracket and |F| below 1e-27; and at M' 128, gamma within 1.05e-6 of the uniform gamma(128) (the uniform M error at D 3.15). Reported beside it,
not a pass rule: gamma(M' 128) - gamma(M' 96) per map against the uniform 1.05e-6, and Ecker et al.'s 0.22739 within about 1e-5.
usage: accept_gamma.py RECORDS.jsonl --ref UNIFORM_M128.jsonl [--ref96 UNIFORM_M96.jsonl]  |  accept_gamma.py selftest [--mutate=shift|sign|F]
The uniform gamma(128) record: raw I1070-macm3/lowD_gamma_D3.15_M128_r2.jsonl (blob b9da6a94), gamma 0.22738724224291604; the M 96 one:
raw I1070-dh170/lowD_gamma_D3.15_M96.jsonl, gamma 0.22738618769170593. Exit 0 only when every acceptance line passes (1 otherwise).
--mutate (a control, each must make the selftest or the check fail): shift (every gamma + 2e-6), sign (two sign changes), F (|F| x 1e3)."""
import json, sys

BAR = 1.05e-6
F_BAR = 1e-27
ECKER, ECKER_SPREAD = 0.22739, 1e-5
args = [a for a in sys.argv[1:] if not a.startswith("--")]
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)


def opt(name):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else None


def load(f):
    return [json.loads(l) for l in open(f) if l.strip()]


def mutate(r):
    r = dict(r)
    if MUT == "shift":
        r["gamma"] += 2e-6
    if MUT == "sign":
        r["n_signchanges"] = 2
    if MUT == "F":
        r["F"] *= 1e3
    return r


def name(r):
    m = r.get("map")
    return "L %g (s0 %.4f)" % (m[1], m[0]) if m else "uniform"


def check(recs, g128, g96=None, out=print):
    ok = True
    recs = [mutate(r) for r in recs if r.get("map") and r.get("gamma") is not None]
    for r in sorted(recs, key=lambda r: (-r["map"][1], r["M"])):
        good = r["n_signchanges"] == 1 and r["F"] < F_BAR
        line = f"{name(r)} M' {r['M']}: gamma {r['gamma']:.10f}, sign changes {r['n_signchanges']}, |F| {r['F']:.2e} (bar {F_BAR:.0e})"
        if r["M"] == 128:
            dev = r["gamma"] - g128
            good &= abs(dev) <= BAR
            line += f", gamma - uniform gamma(128) {dev:+.2e} (bar {BAR:.2e})"
        ok &= good
        out(f"{line}: {'PASS' if good else 'FAIL'}")
    for L in sorted({r["map"][1] for r in recs}, reverse=True):
        d = {r["M"]: r["gamma"] for r in recs if r["map"][1] == L}
        if 128 in d and 96 in d:
            out(f"beside: L {L:g} gamma(M' 128) - gamma(M' 96) {d[128] - d[96]:+.2e}, against the uniform {g128 - g96:+.2e}" if g96 else
                f"beside: L {L:g} gamma(M' 128) - gamma(M' 96) {d[128] - d[96]:+.2e}")
    for r in recs:
        out(f"beside: {name(r)} M' {r['M']}: |gamma - Ecker et al.'s {ECKER}| {abs(r['gamma'] - ECKER):.1e} (their spread about {ECKER_SPREAD:.0e})")
    if not recs:
        out("no mapped record: nothing accepted"); ok = False
    return ok


def selftest():
    g = 0.22738724224291604
    base = dict(D=3.15, F=1e-28, n_signchanges=1)
    good = [dict(base, M=128, gamma=g + 4e-7, map=[1.83, 0.7]), dict(base, M=96, gamma=g + 1e-7, map=[1.83, 0.7])]
    cases = [("planted good records", good, True),
             ("gamma 2e-6 off the uniform at M' 128", [dict(good[0], gamma=g + 2e-6)], False),
             ("two sign changes", [dict(good[0], n_signchanges=2)], False),
             ("|F| 1e-26", [dict(good[0], F=1e-26)], False),
             ("a bar-edge deviation of 1.04e-6", [dict(good[0], gamma=g + 1.04e-6)], True),
             ("no mapped record", [dict(base, M=128, gamma=g, map=None)], False)]
    ok = True
    for name_, recs, want in cases:
        got = check(recs, g, g - 1.05e-6, out=lambda s: None)
        print(f"planted: {name_}: verdict {got}, expected {want}: {'PASS' if got == want else 'FAIL'}")
        ok &= got == want
    print("selftest:", "PASS" if ok else "FAIL")
    return ok


if args and args[0] == "selftest":
    sys.exit(0 if selftest() else 1)
ref = load(opt("--ref"))[-1]
g128 = ref["gamma"]
g96 = load(opt("--ref96"))[-1]["gamma"] if opt("--ref96") else None
print(f"uniform gamma(128) {g128!r} (F {ref['F']:.1e}, {ref['n_signchanges']} sign change, {ref['n_det']} determinants)" + (f"; uniform gamma(96) {g96!r}" if g96 else ""))
ok = check(load(args[0]), g128, g96)
print("ACCEPTANCE:", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)

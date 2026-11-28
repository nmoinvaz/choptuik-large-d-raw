#!/usr/bin/env python3
"""#1109 stage 1e on macm3: the nonlinear elimination's log (ne.out) as the order's table: per outer step |U_w^T F|, Delta, dDelta from R0,
|F|, steps, seconds; the trial fractions of each outer step; the reading (a) or (b).
Usage: python3 ne_summary.py [NE.out]      (default ne.out beside this script; dDelta from the printed 12-digit Delta of outer 0)
       python3 ne_summary.py --selftest    (planted logs: (a) falls 2x per step to <= 1e-12, (b) a stop line, neither: must be read so)"""
import os, re, sys

OUTER = re.compile(r"^outer (\d+): \|F\| (\S+), weak pair s/s_max (.*?), \|U_w\^T F\| (\S+), Delta (\S+); Gauss-Newton \|dz\| (\S+) dDelta (\S+) \((\d+) s for J and SVD\)")
FRAC = re.compile(r"^\s+fraction (\S+): chord \|F\| (.*?) -> (\S+), \|U_w\^T F\| (\S+), Delta (\S+), steps (\d+)")
TOOK = re.compile(r"^\s+took fraction (\S+): \|F\| (\S+), Delta (\S+); saved (\S+)")
SYS = re.compile(r"steps (\d+) \(record (\d+)\): the record system")
STOP = re.compile(r"^\s+stop: ")


def parse(text):
    outs, steps0, stop = [], None, False
    for line in text.splitlines():
        m = SYS.search(line)
        if m and steps0 is None:
            steps0 = int(m.group(1))
        m = OUTER.match(line)
        if m:
            outs.append(dict(k=int(m.group(1)), F=float(m.group(2)), uwf=float(m.group(4)), Delta=float(m.group(5)), gn_dDelta=float(m.group(7)),
                             sec=int(m.group(8)), fracs=[], took=None))
            continue
        m = FRAC.match(line)
        if m and outs:
            chord = [float(x) for x in m.group(2).split()]
            outs[-1]["fracs"].append(dict(f=m.group(1), chord=chord, Fend=float(m.group(3)), uwf=float(m.group(4)), Delta=float(m.group(5)), steps=int(m.group(6))))
            continue
        m = TOOK.match(line)
        if m and outs:
            outs[-1]["took"] = dict(f=m.group(1), F=float(m.group(2)), Delta=float(m.group(3)), saved=m.group(4))
            continue
        if STOP.match(line):
            stop = True
    return outs, steps0, stop


def reading(outs, stop):
    uw = [o["uwf"] for o in outs]
    falls = all(a / b >= 2 for a, b in zip(uw, uw[1:]))
    if not stop and falls and uw[-1] <= 1e-12:
        return "(a)"
    if stop:
        return "(b)"
    return "neither (no stop line and not (a))"


def report(text, out=print):
    outs, steps0, stop = parse(text)
    D0 = outs[0]["Delta"]
    out("| outer | |U_w^T F| | Delta | dDelta from R0 | |F| | steps | J and SVD s | Gauss-Newton dDelta | fraction taken |")
    out("|---|---|---|---|---|---|---|---|---|")
    for o in outs:
        prev = outs[o["k"] - 1] if o["k"] else None
        took = prev["took"] if prev else None
        steps = next((fr["steps"] for fr in prev["fracs"] if fr["f"] == took["f"]), "?") if prev else steps0
        out(f"| {o['k']} | {o['uwf']:.4e} | {o['Delta']:.12f} | {o['Delta'] - D0:+.6e} | {o['F']:.4e} | {steps} | {o['sec']} | {o['gn_dDelta']:+.4e} | "
            f"{(took['f'] if took else '-')} |")
    out("\nTrial fractions (chord |F| first to last; |U_w^T F| and Delta after the chord steps):")
    for o in outs:
        for fr in o["fracs"]:
            out(f"- outer {o['k']} fraction {fr['f']}: chord {fr['chord'][0]:.2e} .. min {min(fr['chord']):.2e} .. {fr['chord'][-1]:.2e} -> {fr['Fend']:.4e}; "
                f"|U_w^T F| {fr['uwf']:.4e}; dDelta {fr['Delta'] - D0:+.6e}; steps {fr['steps']}")
    r = reading(outs, stop)
    ratios = [a["uwf"] / b["uwf"] for a, b in zip(outs, outs[1:])]
    out(f"\n|U_w^T F| ratios outer k / outer k+1: {', '.join(f'{x:.3f}' for x in ratios)}; stop line: {stop}; reading: {r}")
    return r


def planted(uws, stop):
    s = "D 23.0 k_c 127: |F| 3.1959136189e-10 (record 3.1949266444e-10), steps 4179 (record 4179): the record system\n"
    d = 1.174322502744
    for k, u in enumerate(uws):
        s += (f"outer {k}: |F| 3.1959e-10, weak pair s/s_max 4.253e-11, |U_w^T F| {u:.4e}, Delta {d - 0.001 * k:.12f}; Gauss-Newton |dz| 2.779e-02 "
              f"dDelta -1.9581e-02 (498 s for J and SVD)\n")
        if k < len(uws) - 1:
            s += f"   fraction 1.0: chord |F| 1e-5 1e-9 -> 3.2e-10, |U_w^T F| {u / 3:.4e}, Delta {d - 0.001 * (k + 1):.12f}, steps 4200\n"
            s += f"   took fraction 1.0: |F| 3.2e-10, Delta {d - 0.001 * (k + 1):.12f}; saved sol_ne{k + 1}_D23.0000.npy (its own step map)\n"
    if stop:
        s += "   stop: the last outer step cut |U_w^T F| by less than 2x (1.045e-10 -> 1.042e-10)\n"
    return s


def selftest():
    cases = [([1e-10, 4e-11, 1e-11, 8e-13], False, "(a)"), ([1.0453e-10, 1.0420e-10], True, "(b)"), ([1e-10, 4e-11, 3e-12], False, "neither (no stop line and not (a))"),
             ([1e-10, 6e-11, 1e-13], False, "neither (no stop line and not (a))")]
    ok = True
    for uws, stop, want in cases:
        got = report(planted(uws, stop), out=lambda s: None)
        print(f"planted {uws} stop {stop}: expected {want}, read {got}")
        ok &= got == want
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    report(open(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "ne.out")).read())

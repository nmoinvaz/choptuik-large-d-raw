#!/usr/bin/env python3
"""#949 (reopened 2026-11-20): the post rows of ks_chain3b's states, from track949.csv, pairfold949.csv and the near_null JSONs (run track949.py and pairfold949.py first).

    row949.py [N]      markdown rows of the last N (default 2) ks_chain3b states (chain 4): D, sigma_Delta, Delta share, slope, baseline, excess, sigma_2 and its slope,
                       sigma_pair with slope, the pair's D*(4)/(5) with the window shifts, the rule, the pinned step's Delta component; then the run of
                       consecutive states with excess > 0.10 at the end (the trigger needs 3) and 'TRIGGER FIRED' when it is >= 3
    row949.py --selftest [--mutate]   the run counter on planted excess series (exit 1 on failure; --mutate counts with >= instead of > and a boundary case must fail)
sigma_2 and the pinned Delta component are picked as relay_dh370_949.py's picks() does (Delta mode = largest Delta share; sigma_2 = smallest sigma of the vectors that are
neither the Delta mode nor the pair)."""
import csv
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TRIGGER = 0.10


def run_len(ex, strict=True):
    n = 0
    for x in reversed(ex):
        if x is not None and (x > TRIGGER if strict else x >= TRIGGER):
            n += 1
        else:
            break
    return n


def picks(rec):
    v = rec["vectors"]
    d = max(range(len(v)), key=lambda i: v[i]["delta"])
    pair = [i for i in range(len(v)) if i != d and {("p1", 3), ("m_h", 3)} <= {(b, k) for b, k, _ in v[i]["top"]}]
    rest = sorted((i for i in range(len(v)) if i != d and i not in pair), key=lambda i: v[i]["sigma"])
    return d, rest[0]


def selftest(mutate):
    strict = not mutate
    ok = True
    for ex, want in (([0.08, 0.1035], 1), ([0.1035, 0.11, 0.12], 3), ([0.12, 0.09, 0.11], 1), ([0.1, 0.11], 1), ([0.2, None], 0)):
        got = run_len(ex, strict)
        good = got == want
        ok &= good
        print(f"selftest: run of excess > 0.10 at the end of {ex} = {got} (want {want}): {'pass' if good else 'FAIL'}")
    print("selftest" + (" --mutate" if mutate else "") + ":", "pass" if ok else "FAIL")
    return ok


def main():
    n = int(next((a for a in sys.argv[1:] if a.isdigit()), 2))
    tr = [r for r in csv.DictReader(open(os.path.join(HERE, "track949.csv"))) if r["chain"] == "4" and r["classified"] == "1"]
    pf = {round(float(r["D"]), 4): r for r in csv.DictReader(open(os.path.join(HERE, "pairfold949.csv")))}
    tr.sort(key=lambda r: float(r["D"]))
    print("| D | σ_Δ | Δ share | σ_Δ slope | baseline | excess | σ_2 (σ_2/σ_Δ) | σ_2 slope | σ_pair, slope | pair D*(4)/(5), shifts | rule | pinned Δ |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    prev2 = None
    for i, r in enumerate(tr):
        D = float(r["D"])
        name = f"c3b_ks{r['ks']}_D{D:.4f}"
        p = os.path.join(HERE, name + ".json")
        rec = json.load(open(p)) if os.path.exists(p) else None
        s2 = pin = None
        if rec:
            d, k2 = picks(rec)
            s2, pin = rec["vectors"][k2]["sigma"], rec["step_pinned"]["delta"]
        prev_s2 = prev2
        prev2 = (D, s2)
        if i < len(tr) - n:
            continue
        s2slope = "" if not (s2 and prev_s2 and prev_s2[1]) else f"{-math.log(s2 / prev_s2[1]) / (D - prev_s2[0]):.3f}"
        q = pf.get(round(D, 4))
        sd = float(r["sigma_delta"])
        pr = "" if not q else (f"{q['Dstar_last4'] or 'none'} ({q['shift4'] or '-'}) / {q['Dstar_last5'] or 'none'} ({q['shift5'] or '-'})")
        print(f"| {D:.4f} | {sd:.4e} | {float(r['delta_share']):.3f} | {float(r['interval_slope']):.4f} | {float(r['trigger_baseline']):.4f} | {float(r['trigger_excess']):+.4f} | "
              f"{'' if s2 is None else format(s2, '.4e')} ({'' if s2 is None else format(s2 / sd, '.3f')}) | {s2slope} | {float(r['sigma_pair']):.3e}, {r['pair_interval_slope']} | {pr} | "
              f"{'met' if q and q['rule_met'] == '1' else 'not met'} | {'' if pin is None else format(pin, '+.3e')} |")
    ex = [float(r["trigger_excess"]) if r["trigger_excess"] else None for r in tr]
    k = run_len(ex)
    print(f"excess run above {TRIGGER} at the end: {k} of 3" + ("  *** TRIGGER FIRED ***" if k >= 3 else ""))


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest("--mutate" in sys.argv) else 1)
    main()

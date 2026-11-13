#!/usr/bin/env python3
"""#643: rt_sigma.py's bounds and x's content on the K = 7 roots, their K = 0 controls and the N_t = 48 state at D 50, classified by #423's rules (README.md).
usage: python table_643.py          (from this folder; reads logs/<label>_<smooth|rough>.log and table_423.py's parser)
Labels: K7_a, K7_b (horizon rows, K = 7), K0_a, K0_b (the same starts without rows), NT48 (the N_t = 48 state). Per run: best bound of 3 starts, spread, worst residual, mu, E, C0, C4, class (#423's definitions).
Verdict per state: (H) = edge + seen only by rough + horizon-like; (C) = centre in omega_4 + seen by smooth + not horizon-like; neither otherwise. The D trend of #423's rule cannot be formed from one D and is carried over
from #423's 32x121 K = 0 series (D 40 to 50: -0.57 decades per 10 in D, not horizon-like); so (H) cannot come out here. Reproduction control: K0_a rough within a factor 3 of #163's 1.2e-34, K7_a rough
within a factor 3 of #163's 4.9e-34."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import table_423 as t  # noqa: E402

LABELS = ("K7_a", "K0_a", "K7_b", "K0_b", "NT48")
CARRIED_TREND = "not horizon-like"


def load(label, kind):
    p = os.path.join(HERE, "logs", f"{label}_{kind}.log")
    if not os.path.exists(p):
        return None
    r = t.parse(open(p, encoding="utf-8", errors="replace").read())
    if r["head"] is None or not r["starts"]:
        return None
    return r["head"], t.summarize(r)


def main():
    runs = {(lab, k): load(lab, k) for lab in LABELS for k in ("rough", "smooth")}
    print("| state | K | grid | kind | bound (best of 3) | starts' spread | worst residual | products | mu | E (edge) | C0 (centre) | C4 (w4 centre) | class |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for lab in LABELS:
        for k in ("rough", "smooth"):
            r = runs[(lab, k)]
            if r is None:
                print(f"| {lab} | | | {k} | not yet | | | | | | | | |")
                continue
            h, s = r
            f = lambda key, fmt: fmt % s[key] if key in s and s[key] is not None else "n/a"
            print(f"| {h['state']} | {h['K']} | {h['Nt']}x{h['N']} | {k} | {s['bound']:.3e} | {s['spread']:.1f} | {s['res']:.1e} | {s['prods']} | {f('mu', '%.2f')} | {f('E', '%.2f')} | {f('C0', '%.2f')} | {f('C4', '%.2f')} | {s.get('cls', 'n/a')} |")
    print("\nPer state (smooth against rough, class, verdict by #423's rules with the carried D trend):")
    for lab in LABELS:
        ro, sm = runs[(lab, "rough")], runs[(lab, "smooth")]
        if ro is None or sm is None:
            continue
        ratio = sm[1]["bound"] / ro[1]["bound"]
        seen = ratio <= 100
        cls = ro[1].get("cls")
        if cls == "edge" and not seen and CARRIED_TREND == "horizon-like":
            v = "(H)"
        elif cls == "centre in w4" and seen and CARRIED_TREND == "not horizon-like":
            v = "(C)"
        else:
            v = "neither"
        print(f"  {lab}: rough {ro[1]['bound']:.3e}, smooth {sm[1]['bound']:.3e}, smooth/rough {ratio:.2e} ({'seen' if seen else 'not seen'} by smooth); x {cls} (rough start; smooth start: {sm[1].get('cls')}); trend (carried) {CARRIED_TREND} -> {v}")
    print("\nThe rows against their same-start controls (rough bound, K = 7 / K = 0):")
    for s_ in ("a", "b"):
        a, b = runs[(f"K7_{s_}", "rough")], runs[(f"K0_{s_}", "rough")]
        if a and b:
            print(f"  start {s_}: {a[1]['bound']:.3e} / {b[1]['bound']:.3e} = {a[1]['bound'] / b[1]['bound']:.2f}; class {a[1].get('cls')} (mu {a[1].get('mu'):.2f}) against {b[1].get('cls')} (mu {b[1].get('mu'):.2f})")
    print("\nReproduction of #163 (same code, another machine):")
    for lab, ref in (("K0_a", 1.2e-34), ("K7_a", 4.9e-34)):
        r = runs[(lab, "rough")]
        if r:
            q = r[1]["bound"] / ref
            print(f"  {lab} rough {r[1]['bound']:.3e} against {ref:.1e}: factor {q:.2f} -> {'within 3' if 1 / 3 <= q <= 3 else 'OUTSIDE 3'}")
    ref23 = 1.404e-34
    nt = runs[("NT48", "rough")]
    if nt:
        print(f"\nN_t = 48 (48x121) rough {nt[1]['bound']:.3e} against #423's 32x121 K = 0 at D 50.007 ({ref23:.3e}): factor {nt[1]['bound'] / ref23:.2f}")


if __name__ == "__main__":
    main()

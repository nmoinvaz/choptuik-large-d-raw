#!/usr/bin/env python3
"""#681: 12 rough starts per state, the median as the bound, R(D) = median(K = 7) / median(K = 0), the window of 3 with bootstrap intervals, and the verdict of the rules fixed in README.md.
usage: python table_681.py [--selftest]          (from this folder; reads logs/{K7,K0}_{D40,D50,D55}_rough.log and the earlier 3-start logs of ../I671-win/logs and ../I643-win/logs)
Bound of a run = the median of its 12 rough bounds (geometric mean of the 6th and 7th smallest); best, Q1 (3rd and 4th), Q3 (9th and 10th) and max are context. FOLLOWS if R(40.02)/R(50.007) and
R(54.996)/R(50.007) are both inside [1/3, 3] and so are their bootstrap 95% intervals (10000 resamples of each state's 12 bounds with replacement, random.Random(681)); DOES NOT FOLLOW if a point ratio is
outside and its interval entirely outside; UNDECIDED otherwise. --selftest: planted samples with a known ratio, including one that must come out DOES NOT FOLLOW and one UNDECIDED."""
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import table_423 as t  # noqa: E402

DS = (("D40", 40.020065), ("D50", 50.007491), ("D55", 54.996085))
WINDOW = 3.0
NBOOT = 10000


def gmean(a, b):
    return math.exp(0.5 * (math.log(a) + math.log(b)))


def median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else gmean(s[n // 2 - 1], s[n // 2])


def quart(v, which):
    s = sorted(v)
    n = len(s)
    if n < 12:
        return None
    return gmean(s[2], s[3]) if which == 1 else gmean(s[8], s[9])


def inside(x):
    return 1 / WINDOW <= x <= WINDOW


def verdict(k7, k0, seed=681, nboot=NBOOT):
    """k7, k0: dict D-key -> list of 12 bounds. Returns (point ratios, intervals, verdict)."""
    def ratios(a, b):
        r = {d: median(a[d]) / median(b[d]) for d in a}
        return {d: r[d] / r["D50"] for d in ("D40", "D55")}
    pt = ratios(k7, k0)
    rng = random.Random(seed)
    samples = {"D40": [], "D55": []}
    for _ in range(nboot):
        a = {d: [rng.choice(k7[d]) for _ in k7[d]] for d in k7}
        b = {d: [rng.choice(k0[d]) for _ in k0[d]] for d in k0}
        r = ratios(a, b)
        for d in samples:
            samples[d].append(r[d])
    ci = {}
    for d in samples:
        s = sorted(samples[d])
        ci[d] = (s[int(0.025 * nboot)], s[int(0.975 * nboot) - 1])
    if all(inside(pt[d]) and inside(ci[d][0]) and inside(ci[d][1]) for d in pt):
        v = "FOLLOWS"
    elif any((not inside(pt[d])) and (ci[d][1] < 1 / WINDOW or ci[d][0] > WINDOW) for d in pt):
        v = "DOES NOT FOLLOW"
    else:
        v = "UNDECIDED"
    return pt, ci, v


def selftest():
    rng = random.Random(7)

    def sample(med, sigma, n=12):
        return [med * math.exp(rng.gauss(0, sigma)) for _ in range(n)]
    cases = []
    # K = 7 and K = 0 with the same R at all D: follows
    k0 = {d: sample(1e-34, 0.3) for d, _ in DS}
    k7 = {d: sample(4e-34, 0.3) for d, _ in DS}
    cases.append(("same R everywhere, narrow starts", k7, k0, "FOLLOWS"))
    # R at D 40 ten times smaller, narrow starts: does not follow
    k7b = {"D40": sample(0.4e-34, 0.15), "D50": sample(4e-34, 0.15), "D55": sample(4e-34, 0.15)}
    k0b = {d: sample(1e-34, 0.15) for d, _ in DS}
    cases.append(("R(40) a factor 10 low, narrow starts", k7b, k0b, "DOES NOT FOLLOW"))
    # R at D 40 four times smaller but starts spread by a factor of ~20: undecided
    k7c = {"D40": sample(1e-34, 1.2), "D50": sample(4e-34, 1.2), "D55": sample(4e-34, 1.2)}
    k0c = {d: sample(1e-34, 1.2) for d, _ in DS}
    cases.append(("R(40) a factor 4 low, wide starts", k7c, k0c, "UNDECIDED"))
    bad = 0
    for name, a, b, want in cases:
        pt, ci, v = verdict(a, b, nboot=2000)
        print(f"  planted '{name}': ratios {pt['D40']:.2f}, {pt['D55']:.2f}; intervals {ci['D40'][0]:.2f} to {ci['D40'][1]:.2f}, {ci['D55'][0]:.2f} to {ci['D55'][1]:.2f} -> {v} (expected {want}) {'ok' if v == want else 'WRONG'}")
        bad += v != want
    print("selftest", "FAILED" if bad else "passed")
    return bad


def load(path):
    if not os.path.exists(path):
        return None
    r = t.parse(open(path, encoding="utf-8", errors="replace").read())
    return r


def cls_of(c):
    fl = c["fields"]
    F = max(f["max"] for f in fl.values())
    E = max(max(f["P"], f["M"]) for f in fl.values()) / F
    C0 = max(f["C"] for f in fl.values()) / F
    C4 = fl["w4"]["C"] / F
    return "edge" if E >= 0.5 and E >= 3 * C0 else ("centre in w4" if C4 >= 0.5 and C4 >= 3 * E else "mixed")


def main():
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    runs = {}
    for k in ("K7", "K0"):
        for d, D in DS:
            r = load(os.path.join(HERE, "logs", f"{k}_{d}_rough.log"))
            if r and r["starts"]:
                runs[(k, d)] = r
    print("| D | K | n starts | best | Q1 | **median (the bound)** | Q3 | max | max/min | starts at the 250 cap | worst residual | classes of the starts (edge / centre in w4 / mixed) | best start's class |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    B = {}
    for d, D in DS:
        for k in ("K7", "K0"):
            r = runs.get((k, d))
            if not r:
                print(f"| {D} | {k} | 0 | not yet | | | | | | | | | |")
                continue
            v = [s["bound"] for _, s in sorted(r["starts"].items())]
            B[(k, d)] = v
            n = len(v)
            q1, q3 = quart(v, 1), quart(v, 3)
            cap = sum(1 for s in r["starts"].values() if s["prods"] >= 250)
            res = max(s["res"] for s in r["starts"].values())
            cc = {"edge": 0, "centre in w4": 0, "mixed": 0}
            for c in r["content"].values():
                cc[cls_of(c)] += 1
            best = min(r["starts"], key=lambda i: r["starts"][i]["bound"])
            bc = cls_of(r["content"][best]) if best in r["content"] else "n/a"
            f = lambda x: "n/a" if x is None else f"{x:.2e}"
            note = "" if n == 12 else f" (only {n})"
            print(f"| {D} | {k} | {n}{note} | {min(v):.2e} | {f(q1)} | **{median(v):.3e}** | {f(q3)} | {max(v):.2e} | {max(v) / min(v):.1f} | {cap} of {n} | {res:.1e} | {cc['edge']} / {cc['centre in w4']} / {cc['mixed']} (of {len(r['content'])}) | {bc} |")
    print("\nAll bounds, sorted (per run):")
    for d, D in DS:
        for k in ("K7", "K0"):
            if (k, d) in B:
                print(f"  {k} D {D}: " + ", ".join(f"{x:.2e}" for x in sorted(B[(k, d)])))
    full = all(len(B.get((k, d), [])) == 12 for k in ("K7", "K0") for d, _ in DS)
    print("\nR(D) = median(K = 7) / median(K = 0), and from the best:")
    R, Rb = {}, {}
    for d, D in DS:
        if ("K7", d) in B and ("K0", d) in B:
            R[d] = median(B[("K7", d)]) / median(B[("K0", d)])
            Rb[d] = min(B[("K7", d)]) / min(B[("K0", d)])
            print(f"  D {D}: median {median(B[('K7', d)]):.3e} / {median(B[('K0', d)]):.3e} = {R[d]:.2f}; best {min(B[('K7', d)]):.3e} / {min(B[('K0', d)]):.3e} = {Rb[d]:.2f}")
    if full:
        k7 = {d: B[("K7", d)] for d, _ in DS}
        k0 = {d: B[("K0", d)] for d, _ in DS}
        pt, ci, v = verdict(k7, k0)
        print("\nThe window of 3 on R(D)/R(50.007491), with the bootstrap 95% intervals:")
        for d, D in (("D40", 40.020065), ("D55", 54.996085)):
            print(f"  R({D}) / R(50.007491) = {pt[d]:.2f}, interval {ci[d][0]:.2f} to {ci[d][1]:.2f}: point {'inside' if inside(pt[d]) else 'OUTSIDE'}, interval {'inside' if inside(ci[d][0]) and inside(ci[d][1]) else ('entirely outside' if ci[d][1] < 1 / WINDOW or ci[d][0] > WINDOW else 'straddles an edge')}")
        print(f"  VERDICT (rule of README.md): the K = 7 bounds {v} the K = 0 trend within a factor {WINDOW:g}")
        print("  (best-of-12 ratios, context: " + ", ".join(f"R_best({D}) / R_best(50.007491) = {Rb[d] / Rb['D50']:.2f}" for d, D in (("D40", 40.020065), ("D55", 54.996085))) + ")")
    else:
        print("\nverdict not formed: fewer than 12 starts in some run")
    # reproduction of the earlier 3-start runs
    print("\nControl (a): the first three starts against the earlier 3-start runs (same draws, same state; within a factor 1.25):")
    earlier = {("K7", "D40"): "../I671-win/logs/K7_D40_rough.log", ("K0", "D40"): "../I671-win/logs/K0_D40_rough.log", ("K7", "D50"): "../I643-win/logs/K7_a_rough.log",
               ("K0", "D50"): "../I643-win/logs/K0_a_rough.log", ("K7", "D55"): "../I671-win/logs/K7_D55_rough.log", ("K0", "D55"): "../I671-win/logs/K0_D55_rough.log"}
    for d, D in DS:
        for k in ("K7", "K0"):
            e = load(os.path.join(HERE, earlier[(k, d)]))
            if e is None or (k, d) not in runs:
                continue
            old = [e["starts"][i]["bound"] for i in sorted(e["starts"])][:3]
            new = [runs[(k, d)]["starts"][i]["bound"] for i in sorted(runs[(k, d)]["starts"])][:3]
            if len(new) < 3:
                print(f"  {k} D {D}: only {len(new)} starts so far")
                continue
            q = [n / o for n, o in zip(new, old)]
            ok = all(1 / 1.25 <= x <= 1.25 for x in q)
            print(f"  {k} D {D}: new {', '.join(f'{x:.3e}' for x in new)} / earlier {', '.join(f'{x:.3e}' for x in old)} = {', '.join(f'{x:.3f}' for x in q)} -> {'reproduces' if ok else 'DIFFERS'}; best of the first three {min(new):.3e} against the earlier best-of-3 {min(old):.3e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""#745: the table of acceptances 1 to 3 for start a's twelve rough bounds at D 40.02 at 1000 products.
usage: python table_745.py [LOG]           (default logs/main_1000.log; reads #681's logs in ../I681-win/logs and imports table_681 / table_423 from ../I681-win, unchanged)
       python table_745.py --control      recomputes from #681's own logs R = 0.98, and the full rule's 0.17, interval 0.06 to 0.91, UNDECIDED (exit 1 if not)
       python table_745.py --selftest     planted changes of the inputs, each of which must move the answer it is meant to move
Acceptance 1: starts 0 to 2 print #720's bounds (the printed four digits equal). Acceptance 2: starts 3 to 11 within a factor 1.5 of #681's bound for the same start, with the products used and how many
of the starts reach the 1000 cap. Acceptance 3: R_a = median(the twelve bounds) / median(#681's K = 0 twelve at D 40.02), with the one-state bootstrap of #681's rule (10000 resamples of each sample's
twelve with replacement, random.Random(681), the 2.5 and 97.5 percentiles as in table_681.verdict), against 0.98; as context the full rule of #681 (table_681.verdict) with this run's twelve in place of
#681's K = 7 sample at D 40.02."""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
I681 = os.path.join(HERE, "..", "I681-win")
sys.path.insert(0, I681)
import table_681 as t  # noqa: E402

ISSUE = {0: "1.257e-34", 1: "9.921e-34", 2: "7.797e-34"}
FACTOR = 1.5
CAP = 1000
SEED = 681
NBOOT = 10000
R_681 = 0.98


def ref_runs():
    """#681's six runs: (K, d) -> {start: dict(bound, prods, ...)}"""
    out = {}
    for k in ("K7", "K0"):
        for d, _ in t.DS:
            r = t.load(os.path.join(I681, "logs", f"{k}_{d}_rough.log"))
            out[(k, d)] = r["starts"]
    return out


def bounds_of(starts):
    return [starts[i]["bound"] for i in sorted(starts)]


def boot_one_state(k7, k0, seed=SEED, nboot=NBOOT):
    """point ratio of the medians and the 95% interval, one state; the resampling of table_681.verdict for one D."""
    rng = random.Random(seed)
    rs = []
    for _ in range(nboot):
        a = [rng.choice(k7) for _ in k7]
        b = [rng.choice(k0) for _ in k0]
        rs.append(t.median(a) / t.median(b))
    rs.sort()
    return t.median(k7) / t.median(k0), rs[int(0.025 * nboot)], rs[int(0.975 * nboot) - 1]


def acc1(new):
    return [(i, f"{new[i]['bound']:.3e}", ISSUE[i], f"{new[i]['bound']:.3e}" == ISSUE[i]) for i in sorted(ISSUE) if i in new]


def acc2(new, ref):
    rows = []
    for i in sorted(new):
        if i in ISSUE or i not in ref:
            continue
        q = new[i]["bound"] / ref[i]["bound"]
        rows.append((i, new[i]["bound"], ref[i]["bound"], q, 1 / FACTOR <= q <= FACTOR, new[i]["prods"], ref[i]["prods"]))
    return rows


def accept3(new, runs):
    k7 = {d: bounds_of(runs[("K7", d)]) for d, _ in t.DS}
    k0 = {d: bounds_of(runs[("K0", d)]) for d, _ in t.DS}
    k7["D40"] = bounds_of(new)
    pt1, lo1, hi1 = boot_one_state(k7["D40"], k0["D40"])
    pt, ci, v = t.verdict(k7, k0, seed=SEED)
    return dict(med=t.median(k7["D40"]), med0=t.median(k0["D40"]), R=pt1, lo=lo1, hi=hi1, pt=pt, ci=ci, verdict=v)


def control():
    runs = ref_runs()
    a = accept3(runs[("K7", "D40")], runs)
    got = (f"{a['R']:.2f}", f"{a['pt']['D40']:.2f}", f"{a['ci']['D40'][0]:.2f}", f"{a['ci']['D40'][1]:.2f}", a["verdict"])
    want = ("0.98", "0.17", "0.06", "0.91", "UNDECIDED")
    print(f"control from #681's logs: K = 7 median {a['med']:.3e}, K = 0 median {a['med0']:.3e}, R = {got[0]} (want {want[0]}), R(40)/R(50) = {got[1]} ({want[1]}), interval {got[2]} to {got[3]} ({want[2]} to {want[3]}), verdict {got[4]} ({want[4]})")
    print(f"  one-state interval of R(40.02) itself: {a['lo']:.2f} to {a['hi']:.2f}")
    ok = got == want
    print("control", "passed" if ok else "FAILED")
    return 0 if ok else 1


def report(path):
    runs = ref_runs()
    r = t.load(path)
    if r is None or not r["starts"]:
        print("no starts printed yet")
        return 2
    new = r["starts"]
    n = len(new)
    print(f"{path}: {n} of 12 starts printed\n")
    print("Acceptance 1 (starts 0 to 2 against #720's printed bounds):")
    for i, b, w, ok in acc1(new):
        print(f"  start {i}: {b} vs {w}: {'equal' if ok else 'MISS'}")
    print("\nAcceptance 2 (starts 3 to 11 against #681's, factor 1.5):\n")
    print("| start | bound at 1000 | #681 bound | ratio | within 1.5 | products used | #681 products | reaches 1000 |\n|---|---|---|---|---|---|---|---|")
    ref = runs[("K7", "D40")]
    rows = acc2(new, ref)
    for i, b, rb, q, ok, p, rp in rows:
        print(f"| {i} | {b:.3e} | {rb:.3e} | {q:.3f} | {'yes' if ok else '**no**'} | {p} | {rp} | {'**yes**' if p >= CAP else 'no'} |")
    print(f"\n  within 1.5: {sum(1 for x in rows if x[4])} of {len(rows)}; the first three: " + ", ".join(f"start {i} {new[i]['prods']} products" for i in sorted(ISSUE) if i in new))
    print(f"  starts reaching the {CAP} cap: {sum(1 for s in new.values() if s['prods'] >= CAP)} of {n} (products used: " + ", ".join(str(new[i]["prods"]) for i in sorted(new)) + ")")
    if n < 12:
        print("\nAcceptance 3 not formed: fewer than 12 starts")
        return 0
    a = accept3(new, runs)
    print(f"\nAcceptance 3: R_a = median {a['med']:.3e} / #681's K = 0 median {a['med0']:.3e} = {a['R']:.2f}, one-state bootstrap 95% interval {a['lo']:.2f} to {a['hi']:.2f} (seed {SEED}, {NBOOT} resamples), against #681's {R_681}")
    print(f"  full rule of #681 with this run's twelve at D 40.02: R(40.02) / R(50.007) = {a['pt']['D40']:.2f}, interval {a['ci']['D40'][0]:.2f} to {a['ci']['D40'][1]:.2f}; R(54.996) / R(50.007) = {a['pt']['D55']:.2f}, interval {a['ci']['D55'][0]:.2f} to {a['ci']['D55'][1]:.2f}; verdict {a['verdict']} (#681: UNDECIDED, 0.17 and 0.06 to 0.91)")
    print("  sorted bounds: " + ", ".join(f"{x:.2e}" for x in sorted(bounds_of(new))))
    return 0


def selftest():
    runs = ref_runs()
    ref = runs[("K7", "D40")]
    bad = 0

    def chk(name, cond):
        nonlocal bad
        print(f"  {name}: {'ok' if cond else 'WRONG'}")
        bad += not cond
    same = {i: dict(s) for i, s in ref.items()}
    chk("the reference's first three printed bounds equal the issue's", all(x[3] for x in acc1(same)) and len(acc1(same)) == 3)
    chk("identical bounds: all nine within 1.5", all(x[4] for x in acc2(same, ref)) and len(acc2(same, ref)) == 9)
    m = {i: dict(s) for i, s in ref.items()}
    m[5]["bound"] *= 1.6
    m[6]["bound"] /= 1.4
    chk("start 5 at 1.6 times fails, start 6 at 1/1.4 passes", [x[0] for x in acc2(m, ref) if not x[4]] == [5])
    m[1]["bound"] *= 1.01
    chk("start 1 changed by 1% misses acceptance 1", [x[0] for x in acc1(m) if not x[3]] == [1])
    m = {i: dict(s) for i, s in ref.items()}
    m[2]["prods"], m[9]["prods"] = 1000, 1000
    chk("two starts at the cap are counted", sum(1 for s in m.values() if s["prods"] >= CAP) == 2)
    x3 = {i: dict(s, bound=3 * s["bound"]) for i, s in ref.items()}
    a = accept3(x3, runs)
    chk(f"K = 7 bounds times 3: R_a moves from 0.98 to {a['R']:.2f} (want 2.93, 3 x 2.403e-34/2.463e-34) and the full rule's R(40)/R(50) to {a['pt']['D40']:.2f} (want 0.50)", f"{a['R']:.2f}" == "2.93" and f"{a['pt']['D40']:.2f}" == "0.50")
    ctl = control()
    chk("the control passes", ctl == 0)
    print("selftest", "FAILED" if bad else "passed")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--control" in sys.argv:
        sys.exit(control())
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    sys.exit(report(args[0] if args else os.path.join(HERE, "logs", "main_1000.log")))

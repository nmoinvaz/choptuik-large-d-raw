"""#966: the strict plant protocol at a series order N (README, fixed 2026-11-21 16:45:57 UTC), for both estimators:
the divided-out Dlog (subdom.sub_dlog) and the mapped Dlog (confmap.mapped). The geometry and amplitudes are those of
subdom.py / confmap.py (s1 = P1 - 262.3756, s2 2.8, A1 and the start ratio from AMP.json, noise 1e-12); the plant
has orders 1..N. Pade degrees M 3..M_max with M_max = floor((N - 1)/3) - 1 (9 at N 31) for the plain Dlog, the
divided-out and the mapped estimators alike; --mmax M overrides it (the check that the old degrees repeat N 31).
j*: the first j (|A2|/|A1| = ratio / 2^j) at which the plain Dlog fails the bars (|mu - 0.5| <= 0.05, |s - 2.8| <=
0.014) on the square-root-pair plant. At j*, j* + 1, j* + 2: each estimator must meet the bars for the square-root
pair and the pole pair, and --mutate=move (the point at 3.3, judged against 2.8) must fail at each.
    python scanN.py CODE AMP.json N [--mmax M]     exit 0 when one estimator passes all six, 2 otherwise"""
import json
import sys

code, ampf, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
sys.path.insert(0, code)
import mpmath as mp  # noqa: E402
import singularity_type as st  # noqa: E402
import subdom as sd  # noqa: E402
import confmap as cm  # noqa: E402

mmax = int(sys.argv[sys.argv.index("--mmax") + 1]) if "--mmax" in sys.argv else (N - 1) // 3 - 1
Ms = range(3, mmax + 1)
sd.N = N
st.MS = Ms
mp.mp.dps = 60
a = json.load(open(ampf))
A1, r0 = complex(*a["A1"]), a["ratio"]
sign = 1.0 if a["A2"] >= 0 else -1.0
judge = lambda e: e is not None and abs(e[1] - 0.5) <= 0.05 and abs(e[0] - sd.S2) <= 0.005 * sd.S2
print(f"N {N}, Pade degrees M 3..{mmax}", flush=True)
jstar = None
for j in range(0, 41):
    e = st.dlog_fit(sd.plant(A1, sign * abs(A1) * r0 / 2 ** j, sd.S1, sd.S2, 0.5))
    print(f"j {j:2d}, |A2|/|A1| {r0 / 2 ** j:.4e}: plain Dlog: {sd.fmt(e)} -> {'meets' if judge(e) else 'FAILS'} the bars",
          flush=True)
    if not judge(e):
        jstar = j
        break
if jstar is None:
    print(f"N {N}: the plain Dlog meets the bars at every j up to 40; no plant reproduces its failure on the data")
    sys.exit(2)
ok = {"divided-out": True, "mapped": True}
for j in (jstar, jstar + 1, jstar + 2):
    A2 = sign * abs(A1) * r0 / 2 ** j
    for name, mu1 in (("square-root pair", 0.5), ("pole pair", -1.0)):
        c, cmv = sd.plant(A1, A2, sd.S1, sd.S2, mu1), sd.plant(A1, A2, sd.S1, sd.S2 + 0.5, mu1)
        for est in ("divided-out", "mapped"):
            if est == "divided-out":
                e, em = sd.sub_dlog(st, c, sd.S1, Ms), sd.sub_dlog(st, cmv, sd.S1, Ms)
            else:
                e, em = cm.mapped(st, c, sd.S1, sd.S2)[0], cm.mapped(st, cmv, sd.S1, sd.S2)[0]
            good, moved = judge(e), judge(em)
            ok[est] &= good and not moved
            print(f"j {j:2d}, {name}, {est}: {sd.fmt(e) if est == 'divided-out' else cm.fmt(e)} -> {'PASS' if good else 'FAIL'}; "
                  f"move: {'fails (as required)' if not moved else 'PASSES (control did not fire)'}", flush=True)
for est, v in ok.items():
    print(f"N {N}, {est}: {'PASSES all six' if v else 'fails'}")
print(f"N {N} (j* = {jstar}, M 3..{mmax}): {'PASS: ' + ', '.join(k for k, v in ok.items() if v) if any(ok.values()) else 'FAIL: neither estimator passes all six'}")
sys.exit(0 if any(ok.values()) else 2)

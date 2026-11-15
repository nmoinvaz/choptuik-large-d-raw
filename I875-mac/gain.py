"""I875-mac check: the first step's gain on an m_h, a_h move from the re-converged root at D 240.1244.

Reads a `step_spread.py --steps` JSON. gain = e_1 / e_0, with e_0 = move / max|z_h| and e_1 = max|z_1 - u_1| /
max|z_h| (u_1 the unperturbed path's first iterate). Passes when the gain is below 1 at the smallest rel and above 1 at
the largest, and gain / rel at the largest rel is within 10% of 7.5556e92 (#852's excess, #840's quadratic part).

Run: python3 gain.py STEPS.json, or python3 gain.py --selftest (a planted quadratic gain passes; one with #852's linear
gain 9.306e3 on top fails at the smallest rel). Its control is #852's I852-mac/steps_D240.json, which must FAIL.
Exits 1 when a check fails.
"""
import json
import sys

Q = 7.5556e92


def check(js):
    zh = js["zh"]
    runs = sorted((r for r in js["runs"] if r["run"] != "unperturbed"), key=lambda r: -r["rel"])
    g = {}
    print(f"gain: {js['state']}, max|z_h| {zh:.10g}")
    for r in runs:
        e0, e1 = r["move"] / zh, r["hist"][0]["e_pair"]
        g[r["rel"]] = e1 / e0
        print(f"  {r['run']}: e_0 {e0:.4e}, e_1 {e1:.4e}, gain {e1 / e0:.4e}, gain / rel {e1 / e0 / r['rel']:.4e}")
    hi, lo = max(g), min(g)
    q = g[hi] / hi
    checks = [("small", g[lo] < 1, f"gain at rel {lo:.0e} {g[lo]:.4e} (< 1)"),
              ("large", g[hi] > 1, f"gain at rel {hi:.0e} {g[hi]:.4e} (> 1)"),
              ("quadratic", abs(q / Q - 1) <= 0.1, f"gain / rel at {hi:.0e} {q:.4e} against {Q:.4e}: {q / Q - 1:+.3e} "
               "(|.| <= 0.1)")]
    for name, ok, what in checks:
        print(f"  check {name}: {what}: {'pass' if ok else 'FAIL'}")
    return all(c[1] for c in checks)


def planted(lin):
    # e_1 = lin rel + Q rel^2 + a floor of 1e-99, e_0 = rel (max|z_h| 1)
    runs = [dict(run="unperturbed", rel=0.0, move=0.0, hist=[])]
    for rel in (1e-90, 1e-93, 1e-96):
        runs.append(dict(run=f"planted rel {rel:g}", rel=rel, move=rel,
                         hist=[dict(k=1, e_pair=lin * rel + Q * rel * rel + 1e-99)]))
    return dict(state="planted", zh=1.0, runs=runs)


if sys.argv[1] == "--selftest":
    res = []
    for lin, want in [(0.0, True), (9.306e3, False)]:
        print(f"planted linear gain {lin:g} (want {'pass' if want else 'FAIL'})")
        res.append(check(planted(lin)) == want)
    ok = all(res)
    print(f"gain selftest: {'PASS' if ok else 'FAIL'}")
else:
    ok = check(json.load(open(sys.argv[1])))
    print(f"gain: {'PASS' if ok else 'FAIL'}")
sys.exit(0 if ok else 1)

#!/usr/bin/env python3
"""#774: Delta of each re-polished state against its stored value, the control, and Delta_full - Delta_held.
usage: python3 cmp_774.py [--selftest] [--mutate X]      (any Python 3 with numpy; python-flint for the cross-check)
Delta of a state = the exact sum of the last entry of every part present (fractions.Fraction, exact), printed to 40
digits. Checks, each exits 1 when it fails:
  reading   the stored states give #742's 40-digit Delta (D 113 from I739-win/B, 117, 120) and X2c's 60 digits, the
            held states give T138's logged 12 digits, and #739's arb reading (I739-win/cmp_739.py) agrees to 1e-100
  control   C_X2c's polished Delta equals X2c's stored one to 1e-50 (--mutate X adds X to the control's Delta, and
            1e-48 must fail), and its Newton lines equal #727's logs/X2c.log
  converged each E job's corrector says converged with final max|F| at most 1e-60
--selftest: planted eight-part states (a Delta read back exactly, a planted shift, the bars' verdicts)."""
import os
import re
import sys
from decimal import ROUND_HALF_EVEN, Decimal, getcontext
from fractions import Fraction

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
KEYS = ("zh", "zl", "z2", "z3", "z4", "z5", "z6", "z7")
getcontext().prec = 120

STORED = {"E_113": "I742-win/P/base_pin13_D113.0000.npz", "E_117": "I742-win/L/anm_pin13_D117.0000.npz",
          "E_120": "I742-win/M/anm_pin13_D120.0000.npz", "E_cont3": "I682-win/cont3/anm_pin13_D99.8750.npz",
          "E_X2c": "I727-win/X2c/base_pin13_D99.8750.npz"}
D_OF = {"E_113": 113, "E_117": 117, "E_120": 120, "E_cont3": 99.875, "E_X2c": 99.875}
B113 = "I739-win/B/anm_pin13_D113.0000.npz"
HELD = lambda D: f"T138-win2/chain/anm_pin3_D{D}.0000.npz"
# #742's table (README, table_742_out.md) and #727's X2c (README): the reading check's strings
T742 = {113: "1.733640141567942734406710993193602081591", 117: "1.730635685860038849267059677903292989227",
        120: "1.728511242950407984923956924965683176416"}
X2C60 = "1.745150028164499252944352893640343550633457431631616393443"
T138 = {113: "1.733640141568", 117: "1.730635685860", 120: "1.728511242950"}       # chain.log, 12 decimals
SHIFT742 = {113: 4.3655e-13, 117: 4.9456e-13, 120: 5.3226e-13}                      # #742's Delta_full - Delta_held
BAR_D99 = 1e-25


def delta(path):
    d = np.load(path if os.path.isabs(path) else os.path.join(RAW, path), allow_pickle=True)
    s = Fraction(0)
    for k in KEYS:
        if k in d.files:
            s += Fraction(float(d[k][-1]))
    return s


def digits(x, dec=39):
    """x rounded to dec decimals (40 significant digits by default, as #742's strings are)"""
    q = Decimal(x.numerator) / Decimal(x.denominator)
    return str(q.quantize(Decimal(1).scaleb(-dec), rounding=ROUND_HALF_EVEN))


def bar_verdict(D, shift):
    bar = BAR_D99 if D == 99.875 else 1e-3 * SHIFT742[D]
    return bar, ("FLAG (above the bar)" if abs(shift) > bar else "below the bar")


def base_of(job):
    folder = os.path.join(HERE, job)
    fs = [f for f in os.listdir(folder) if f.startswith("base_pin")] if os.path.isdir(folder) else []
    return os.path.join(folder, fs[0]) if len(fs) == 1 else None


STEP = re.compile(r"^\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+),")
FIN = re.compile(r"^\s+on (\d+): \|F\| (\S+) converged")
OD = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| (\S+), (\S+)")


def parse_log(job):
    p = os.path.join(HERE, "logs", f"{job}.log")
    if not os.path.exists(p):
        return None
    r = dict(steps=[], final=None, od=None, kernel=None)
    for ln in open(p, encoding="utf-8", errors="replace"):
        if ln.startswith("# build"):
            r["kernel"] = ln.split("hpkernel", 1)[1].strip()
        m = STEP.match(ln)
        if m:
            r["steps"].append(dict(F0=float(m.group(2)), F1=float(m.group(3)), dz0=float(m.group(4)), lam=m.group(6),
                                   dD=float(m.group(7))))
        m = FIN.match(ln)
        if m:
            r["final"] = float(m.group(2))
        m = OD.search(ln)
        if m and r["od"] is None:
            r["od"] = dict(n=int(m.group(1)), F=float(m.group(2).rstrip(",")), says=m.group(3))
    return r


def newton_lines(path):
    """the base polish's Newton lines (up to the line 'base <state>: ...') with the seconds stripped"""
    out = []
    for ln in open(path, encoding="utf-8", errors="replace"):
        if ln.startswith("base ") and "D " in ln:
            break
        if re.match(r"^\s+on \d+:", ln):
            out.append(re.sub(r",\s*[0-9.]+ s$", "", ln.rstrip()))
    return out


def reading_check():
    bad = 0
    for D, path in ((113, B113), (117, STORED["E_117"]), (120, STORED["E_120"])):
        got = digits(delta(path))
        ok = got == T742[D]
        print(f"  reading {path}: {got} {'= #742' if ok else '!= #742 ' + T742[D]}")
        bad += not ok
    got = digits(delta(STORED["E_X2c"]), 57)
    ok = got == X2C60
    print(f"  reading {STORED['E_X2c']} (57 decimals): {got} {'= #727' if ok else '!= #727 ' + X2C60}")
    bad += not ok
    for D in (113, 117, 120):
        got = digits(delta(HELD(D)), 12)
        ok = got == T138[D]
        print(f"  reading {HELD(D)} (12 decimals): {got} {'= chain.log' if ok else '!= chain.log ' + T138[D]}")
        bad += not ok
    try:
        sys.path.insert(0, os.path.join(RAW, "I739-win"))
        import cmp_739 as c
        c.flint.ctx.prec = 600
        worst = 0.0
        for p in [B113, HELD(117)] + list(STORED.values()):
            a = c.delta(os.path.join(RAW, p))
            b = delta(p)
            dd = abs(float((a - c.arb(b.numerator) / c.arb(b.denominator)).mid()))
            worst = max(worst, dd)
        ok = worst <= 1e-100
        print(f"  cross-check with #739's arb reading on {2 + len(STORED)} states: largest difference {worst:.1e} "
              f"{'ok' if ok else 'MISMATCH'}")
        bad += not ok
    except ImportError as e:
        print(f"  cross-check with #739's arb reading not run ({e})")
    return bad


def selftest():
    import tempfile
    bad = 0
    with tempfile.TemporaryDirectory() as tmp:
        x = Fraction(314159265358979323846264338327950288419716939937510582097494459230781640628620899, 10 ** 80) / 2
        parts, r = [], x
        for _ in range(8):
            p = float(r)
            parts.append(p)
            r -= Fraction(p)
        z = {k: np.array([0.0, parts[i]]) for i, k in enumerate(KEYS)}
        np.savez(os.path.join(tmp, "a.npz"), **z)
        got = delta(os.path.join(tmp, "a.npz"))
        e = abs(float(got - x))
        ok = e < 1e-125
        print(f"  planted eight-part Delta read back: error {e:.1e} {'ok' if ok else 'WRONG'}")
        bad += not ok
        z["z7"] = z["z7"] + np.array([0.0, 1.234e-20 * 2.0 ** -300])
        z["z6"] = z["z6"] + np.array([0.0, 1.234e-20])
        np.savez(os.path.join(tmp, "b.npz"), **z)
        s = float(delta(os.path.join(tmp, "b.npz")) - got)
        ok = abs(s / 1.234e-20 - 1) < 1e-12
        print(f"  planted shift 1.234e-20: reads {s:.4e} {'ok' if ok else 'WRONG'}")
        bad += not ok
    for D, s, want in ((117, 5.0e-16, True), (117, 4.0e-16, False), (99.875, 2e-25, True), (99.875, -5e-26, False)):
        got = bar_verdict(D, s)[1].startswith("FLAG")
        print(f"  bar at D {D} for shift {s:+.1e}: {'flag' if got else 'below'} (expected {'flag' if want else 'below'}) "
              f"{'ok' if got == want else 'WRONG'}")
        bad += got != want
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    if "--selftest" in sys.argv:
        sys.exit(1 if selftest() else 0)
    mutate = float(sys.argv[sys.argv.index("--mutate") + 1]) if "--mutate" in sys.argv else 0.0
    bad = 0
    print("## Reading check\n")
    bad += reading_check()

    print("\n## Control: C_X2c (build R, #727's X2c job from its start) against X2c's stored root\n")
    cb = base_of("C_X2c")
    if cb is None:
        print("  C_X2c has no polished state yet")
        bad += 1
    else:
        dc = delta(cb) + Fraction(mutate)
        ds = delta(STORED["E_X2c"])
        diff = float(dc - ds)
        ok = abs(diff) <= 1e-50
        print(f"  Delta(C_X2c){' + ' + str(mutate) + ' (mutated)' if mutate else ''} - Delta(X2c stored) = {diff:+.4e}; "
              f"bar 1e-50: {'met' if ok else 'NOT MET'}")
        bad += not ok
        a, b = np.load(cb), np.load(os.path.join(RAW, STORED["E_X2c"]))
        same = all(np.array_equal(a[k], b[k]) for k in KEYS)
        print(f"  all eight parts bit for bit equal to the stored X2c: {same}")
        mine, ref = newton_lines(os.path.join(HERE, "logs", "C_X2c.log")), newton_lines(os.path.join(RAW, "I727-win/logs/X2c.log"))
        eq = mine == ref[: len(mine)] and len(mine) > 0
        print(f"  Newton lines against #727's X2c.log: {len(mine)} lines, {'all equal' if eq else 'DIFFERENT'}")
        bad += not eq
        if not eq:
            for x, y in zip(mine, ref):
                if x != y:
                    print(f"    ours: {x}\n    #727: {y}")

    print("\n## E_117 against #752's run on the same build (I752-mac/logs/AB_main.log, its base polish)\n")
    if os.path.exists(os.path.join(HERE, "logs", "E_117.log")):
        mine, ref = newton_lines(os.path.join(HERE, "logs", "E_117.log")), newton_lines(os.path.join(RAW, "I752-mac/logs/AB_main.log"))
        eq = len(mine) > 0 and mine == ref
        print(f"  {len(mine)} lines against {len(ref)}: {'all equal' if eq else 'DIFFERENT'}")
        bad += not eq
    else:
        print("  E_117 not run yet")

    print("\n## Shifts on the exact projector (build E) from the stored states\n")
    print("| state | D | start max\\|F\\| on E | Newton steps | final max\\|F\\| | converged (at most 1e-60) | Delta on E (40 digits) | "
          "stored Delta (40 digits) | shift = E - stored | kind | bar | verdict |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    dE = {}
    for job, sp in STORED.items():
        D = D_OF[job]
        lg = parse_log(job)
        b = base_of(job)
        if lg is None or b is None:
            print(f"| {job} | {D:g} | not run or no polished state | | | | | | | | | |")
            continue
        conv = lg["od"] is not None and lg["od"]["says"].startswith("converged") and lg["final"] is not None and lg["final"] <= 1e-60
        bad += not conv
        de, ds = delta(b), delta(sp)
        dE[job] = de
        s = float(de - ds)
        kind = ("measured: exact - rounded, both converged roots on their own plan (stored on win's pre-#523 build)"
                if job != "E_cont3" else
                "exact - stored quad-double state; its od polish on the rounded build takes no Newton step (#727 pilot2)")
        bar, verdict = bar_verdict(D, s)
        st = lg["steps"]
        print(f"| {job} | {D:g} | {st[0]['F0']:.2e} | {len(st)} | {lg['final']:.2e} | {'yes' if conv else 'NO'} | {digits(de)} | "
              f"{digits(ds)} | {s:+.4e} | {kind} | {bar:.2e} | {verdict} |")
    if "E_cont3" in dE and "E_X2c" in dE:
        print(f"\nE_cont3 - E_X2c (one plan, both on E): {float(dE['E_cont3'] - dE['E_X2c']):+.4e}; "
              f"stored cont3 - stored X2c: {float(delta(STORED['E_cont3']) - delta(STORED['E_X2c'])):+.4e}")

    print("\n## Delta_full - Delta_held at D 113, 117, 120\n")
    print("| D | #742 (stored full - stored held) | rounded, held polished (stored full - H_R) | exact (E - H_E) | "
          "exact - #742 | held: H_E - H_R (projector) | held: H_R - stored (its own convergence) |")
    print("|---|---|---|---|---|---|---|")
    for D in (113, 117, 120):
        full_s = delta(B113 if D == 113 else STORED[f"E_{D}"])
        held_s = delta(HELD(D))
        t = full_s - held_s
        hr, he = base_of(f"H_R{D}"), base_of(f"H_E{D}")
        r = f"{float(delta(STORED[f'E_{D}']) - delta(hr)):+.6e}" if hr else "not run"
        if he and f"E_{D}" in dE:
            ex = dE[f"E_{D}"] - delta(he)
            e, em = f"{float(ex):+.6e}", f"{float(ex - t):+.3e}"
        else:
            e = em = "not run"
        hp_ = f"{float(delta(he) - delta(hr)):+.4e}" if hr and he else "not run"
        hc = f"{float(delta(hr) - held_s):+.4e}" if hr else "not run"
        print(f"| {D} | {float(t):+.6e} | {r} | {e} | {em} | {hp_} | {hc} |")
    for D in (113, 117, 120):
        t = float(delta(B113 if D == 113 else STORED[f"E_{D}"]) - delta(HELD(D)))
        ok = abs(t / SHIFT742[D] - 1) < 2e-5
        print(f"  #742's value at D {D} reproduced from the stored states: {t:+.4e} (#742 {SHIFT742[D]:+.4e}) {'ok' if ok else 'MISMATCH'}")
        bad += not ok
    print("\nall checks", "passed" if not bad else f"FAILED ({bad})")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()

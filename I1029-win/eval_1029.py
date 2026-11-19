#!/usr/bin/env python3
"""#1029 (win): evaluator and checks for the amplitude series of the low-omega excited zeros.
The harmonics are summed by solver/eeg_profile/tuned_profile.py's own load_f and harmonics (the head of that file, up to its
`paths = ...` line, is executed unchanged, so no code of it is copied here).

    python -I -X utf8 eval_1029.py --checks      the evaluator's two checks fixed in the issue (logs/checks.log):
        (1) tuned_profile.py --plant exits 0 and --plant --mutate=drift exits 1 (subprocess, same interpreter);
        (2) the stored K 45 file solver/inner_amp/scan45J1250/sigF_w1.0000_K45_J1250_p1280.json at A 2.72, through harmonics:
            |F_3/F_1 - (0.05482 + 0.00543i)| <= 1e-4.
    python -I -X utf8 eval_1029.py --selftest    planted series: the convergence rules and the three readings, each branch, and a mutated bar
    python -I -X utf8 eval_1029.py               the tables and readings for the four sigF_w<wf>_K25_J<J>.json of this folder (exit 0 always)

Fixed before the runs (the issue's words; the choices of mine where it leaves one are marked):
 - Per zero and J: F_nu (nu = 1 .. 13) at A of the zero; |F_nu/F_1| and |F_(nu+2)/F_nu| for nu = 1 .. 11 (F_13 is evaluated only for the last ratio);
   last term of each sum relative to F_nu.
 - CONVERGED at the zero when, at both J: last/F_nu <= 1e-2 for nu = 3, 5, 7 (nu = 1 is the single term A sin theta), and the two J agree in
   |F_nu/F_1| to 1e-3 (mine: absolute difference, nu = 3, 5, 7; the relative difference is printed too).
 - Reading, where converged, from |F_7/F_5|: >= 0.3 NON-DECAY CONFIRMED, <= 0.2 CONTRADICTED, between UNDECIDED (the difference to hier is reported).
   Mine: the class is that at the larger J (1000), and it is UNDECIDED unless the J 750 value gives the same class.
 - Not converged: INCONCLUSIVE, with the last-term sizes.
"""
import json
import os
import re
import subprocess
import sys

import mpmath as mp
import numpy as np

WT = r"C:\Users\nathan\Source\choptuik-i1029"
HERE = os.path.dirname(os.path.abspath(__file__))
TP = os.path.join(WT, "solver", "eeg_profile", "tuned_profile.py")
K45 = os.path.join(WT, "solver", "inner_amp", "scan45J1250", "sigF_w1.0000_K45_J1250_p1280.json")
REF_F3F1 = 0.05482 + 0.00543j
TOL_K45 = 1e-4
LAST_BAR, AGREE_BAR, HI, LO = 1e-2, 1e-3, 0.3, 0.2
# the two zeros (A, wf = omega/omega_inf) and hier's M = 7 values from the issue (#1027): |F3/F1|, |F5/F1|, |F7/F1| and I1027's |F7/F5|
ZEROS = [dict(name="z2233", A=2.233308, wf="0.065740", hier=(0.330, 0.194, 0.131), h75=0.676),
         dict(name="z2573", A=2.573290, wf="0.100532", hier=(0.332, 0.184, 0.117), h75=0.634)]
JS = (750, 1000)


def load_tp():
    src = open(TP).read()
    cut = src.index("paths = args.json or DEFAULT")
    ns = {"__file__": TP, "__name__": "tuned_profile_head"}
    save = sys.argv
    sys.argv = ["tuned_profile.py"]
    try:
        exec(compile(src[:cut], TP, "exec"), ns)
    finally:
        sys.argv = save
    return ns


def series(ns, f, K, A):
    """per nu = 1 .. 13: |F_nu/F_1|, last-term fraction; ratios |F_(nu+2)/F_nu| for nu = 1 .. 11"""
    F, last, nterms = ns["harmonics"](f, K, A, 13)
    a1 = abs(F[1])
    rel = {nu: abs(F[nu]) / a1 for nu in F}
    ratio = {nu: abs(F[nu + 2]) / abs(F[nu]) for nu in range(1, 12, 2)}
    return dict(F=F, rel=rel, ratio=ratio, last=last, nterms=nterms)


def klass(r):
    return "CONFIRMED" if r >= HI else ("CONTRADICTED" if r <= LO else "UNDECIDED")


def judge(sa, sb):
    """sa, sb: series() at J 750 and J 1000 of one zero. Returns the convergence verdict and the reading."""
    c1 = all(s["last"][nu] <= LAST_BAR for s in (sa, sb) for nu in (3, 5, 7))
    ag = {nu: abs(sa["rel"][nu] - sb["rel"][nu]) for nu in (3, 5, 7)}
    c2 = all(v <= AGREE_BAR for v in ag.values())
    out = dict(c1=c1, c2=c2, agree=ag, conv=c1 and c2)
    ra, rb = sa["rel"][7] / sa["rel"][5], sb["rel"][7] / sb["rel"][5]
    out["r75"] = (ra, rb)
    if not out["conv"]:
        out["reading"] = "INCONCLUSIVE (the series does not converge at this point)"
    elif klass(ra) == klass(rb):
        out["reading"] = {"CONFIRMED": "NON-DECAY CONFIRMED", "CONTRADICTED": "CONTRADICTED", "UNDECIDED": "UNDECIDED"}[klass(rb)]
    else:
        out["reading"] = f"UNDECIDED (J 750 reads {klass(ra)}, J 1000 reads {klass(rb)})"
    return out


def planted_f(A, K, r, eps, bump=None):
    """f[(k, nu)] summing at A to F_nu = F_(nu-2) r (F_1 = -iA/2), term j of nu's sum eps^j relative to the first, last term eps^((K-nu)/2) of the
    first. bump = (nu, rel) scales F_nu by (1 + rel)."""
    f = {}
    Fn = -0.5j * A
    for nu in range(3, 14, 2):
        Fn = Fn * r
        tgt = Fn * ((1 + bump[1]) if bump and bump[0] == nu else 1)
        js = range(0, (K - nu) // 2 + 1)
        norm = sum(eps ** j for j in js)
        for j in js:
            f[(nu + 2 * j, nu)] = tgt * eps ** j / norm / A ** (nu + 2 * j)
    return f


def selftest():
    global HI
    ns = load_tp()
    A, K, bad = 2.5, 25, 0
    cases = [("|r| 0.6 (non-decay), eps 0.3, J agree", 0.6 * np.exp(0.3j), 0.3, None, None, "NON-DECAY CONFIRMED"),
             ("|r| 0.055 (decay), eps 0.3", 0.055 * np.exp(0.1j), 0.3, None, None, "CONTRADICTED"),
             ("|r| 0.25 (between), eps 0.3", 0.25 * np.exp(0.1j), 0.3, None, None, "UNDECIDED"),
             ("|r| 0.6, eps 0.9 (last terms large)", 0.6, 0.9, None, None, "INCONCLUSIVE"),
             ("|r| 0.6, the J differ in |F_5/F_1| by 3e-3", 0.6, 0.3, None, (5, 0.02), "INCONCLUSIVE"),
             ("|F7/F5| 0.30005 at J 1000, 0.29993 at J 750 (classes differ, the J agree)", 0.30005, 0.3, (7, -4e-4), None, "UNDECIDED"),
             ]
    for nm, r, eps, bumpa, bumpb, want in cases:
        fa = planted_f(A, K, r, eps, bumpa)
        fb = planted_f(A, K, r, eps, bumpb)
        j = judge(series(ns, fa, K, A), series(ns, fb, K, A))
        ok = j["reading"].startswith(want)
        print(f"  {nm}: {j['reading']} (|F7/F5| {j['r75'][0]:.4f}, {j['r75'][1]:.4f}; conv {j['conv']}) {'ok' if ok else 'WRONG'}")
        bad += not ok
    for r, want in ((HI, "CONFIRMED"), (LO, "CONTRADICTED"), (HI - 1e-9, "UNDECIDED"), (LO + 1e-9, "UNDECIDED")):
        ok = klass(r) == want
        print(f"  klass({r!r}) = {klass(r)} (want {want}; the bars are inclusive): {'ok' if ok else 'WRONG'}")
        bad += not ok
    # the last-term fraction the series reports is the planted eps^((K-nu)/2) (first term normalised): nu = 7, K = 25, eps 0.3
    s = series(ns, planted_f(A, K, 0.6, 0.3), K, A)
    exp7 = 0.3 ** ((K - 7) // 2) / sum(0.3 ** j for j in range(0, (K - 7) // 2 + 1))
    ok = abs(s["last"][7] / exp7 - 1) < 1e-9
    print(f"  last term of nu = 7: {s['last'][7]:.3e} against planted {exp7:.3e}: {'ok' if ok else 'WRONG'}")
    bad += not ok
    # mutated bar: with HI lowered below 0.2 the 'between' plant must flip
    old, HI = HI, 0.2
    try:
        j = judge(series(ns, planted_f(A, K, 0.25, 0.3), K, A), series(ns, planted_f(A, K, 0.25, 0.3), K, A))
    finally:
        HI = old
    ok = j["reading"].startswith("NON-DECAY CONFIRMED")
    print(f"  mutated bar (confirm at 0.2): the 'between' plant reads {j['reading']}: {'flips, as it must' if ok else 'DID NOT FLIP'}")
    bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def checks():
    bad = 0
    py = sys.executable
    for args, want in ((["--plant"], 0), (["--plant", "--mutate=drift"], 1)):
        r = subprocess.run([py, "-I", "-X", "utf8", TP] + args, capture_output=True, text=True, cwd=os.path.dirname(TP))
        tail = " | ".join(r.stdout.strip().splitlines()[-2:])
        ok = r.returncode == want
        print(f"tuned_profile.py {' '.join(args)}: exit {r.returncode} (want {want}) {'ok' if ok else 'WRONG'}\n    {tail}")
        bad += not ok
    ns = load_tp()
    K, J, f = ns["load_f"](K45)
    F, last, nterms = ns["harmonics"](f, K, 2.72, 13)
    q = F[3] / F[1]
    dif = abs(q - REF_F3F1)
    ok = dif <= TOL_K45
    print(f"K 45 J {J} file at A 2.72: F_3/F_1 = {q.real:.6f} {q.imag:+.6f}i, reference 0.05482 + 0.00543i, |difference| {dif:.2e} (bar {TOL_K45:g}): {'ok' if ok else 'WRONG'}")
    print(f"   |F_3/F_1| {abs(q):.5f}, |F_5/F_3| {abs(F[5] / F[3]):.5f}, |F_7/F_5| {abs(F[7] / F[5]):.5f} (known zero: 0.055-0.057 per pair), last terms nu 3, 5, 7: "
          f"{last[3]:.1e} {last[5]:.1e} {last[7]:.1e}")
    bad += not ok
    # the check must be able to fail: a perturbed reference
    ok2 = abs(q - REF_F3F1 * 1.01) > TOL_K45
    print(f"control: against a reference 1% higher the check fails ({abs(q - REF_F3F1 * 1.01):.2e} > {TOL_K45:g}): {'ok' if ok2 else 'WRONG'}")
    bad += not ok2
    print("checks", "FAILED" if bad else "passed")
    return bad


def fm(x, nd=4):
    """float formatting for normal sizes, mpmath's for numbers beyond a double"""
    if isinstance(x, (float, int)) or (hasattr(x, "imag") is False and abs(x) < 1e12):
        return f"{float(x):.{nd}f}" if abs(x) < 1e6 else f"{float(x):.2e}"
    return mp.nstr(x, 3)


def load_run(ns, wf, J):
    """K, f (complex; entries whose double overflowed, stored as Infinity, are rebuilt as mpc from the run log's 10 digits), and how many were rebuilt"""
    base = os.path.join(HERE, f"sigF_w{wf}_K25_J{J}.json")
    K, Jf, f = ns["load_f"](base)
    log = open(os.path.join(HERE, "logs", f"w{wf}_J{J}.log"), encoding="utf-8", errors="replace").read()
    pat = re.compile(r"k (\d+) nu (\d+): .* f \(([-+0-9.e]+) ([+-]) ([-+0-9.e]+)j\)")
    fixed = 0
    for m in pat.finditer(log):
        k, nu = int(m.group(1)), int(m.group(2))
        z = f.get((k, nu))
        if z is not None and not (np.isfinite(z.real) and np.isfinite(z.imag)):
            f[(k, nu)] = mp.mpc(mp.mpf(m.group(3)), (-1 if m.group(4) == "-" else 1) * mp.mpf(m.group(5)))
            fixed += 1
    f = {k: (z if isinstance(z, mp.mpc) else mp.mpc(z.real, z.imag)) for k, z in f.items()}      # every sum in mpmath: a double product of f and A^k overflows past 1e308
    return K, Jf, f, fixed


def main():
    ns = load_tp()
    mp.mp.dps = 30
    allj = {}
    for z in ZEROS:
        S = {}
        for J in JS:
            p = os.path.join(HERE, f"sigF_w{z['wf']}_K25_J{J}.json")
            if not os.path.isfile(p):
                print(f"{z['name']} J {J}: {os.path.basename(p)} missing")
                continue
            K, Jf, f, fixed = load_run(ns, z["wf"], J)
            d = json.load(open(p))
            S[J] = series(ns, f, K, z["A"])
            print(f"\n{z['name']} (A {z['A']}, wf {z['wf']}), J {Jf}, K {K}, prec {d.get('prec')}, procs {d.get('procs')}, seconds {d.get('seconds')}; "
                  f"{fixed} of {len(f)} f entries beyond a double were rebuilt from the run log's 10 digits")
            print("| nu | \|F_nu/F_1\| | \|F_(nu+2)/F_nu\| | terms | last term / F_nu |\n|---|---|---|---|---|")
            for nu in range(1, 12, 2):
                print(f"| {nu} | {fm(S[J]['rel'][nu])} | {fm(S[J]['ratio'][nu])} | {S[J]['nterms'][nu]} | {fm(S[J]['last'][nu], 2) if nu > 1 else 0} |")
        if len(S) == 2:
            j = judge(S[750], S[1000])
            h = z["hier"]
            print(f"\n{z['name']}: |F_nu/F_1| at nu 3, 5, 7: J 750 {fm(S[750]['rel'][3])} {fm(S[750]['rel'][5])} {fm(S[750]['rel'][7])}; J 1000 "
                  f"{fm(S[1000]['rel'][3])} {fm(S[1000]['rel'][5])} {fm(S[1000]['rel'][7])}; hier (#1027) {h[0]:.3f} {h[1]:.3f} {h[2]:.3f}")
            print(f"  |F_7/F_5|: J 750 {fm(j['r75'][0])}, J 1000 {fm(j['r75'][1])}, hier {z['h75']:.3f}")
            print("  J agreement in |F_nu/F_1| (absolute): " + ", ".join(f"nu {nu}: {fm(j['agree'][nu])}" for nu in (3, 5, 7)))
            print(f"  last term <= {LAST_BAR:g} of F_nu at nu 3, 5, 7 at both J: {j['c1']}; J agree to {AGREE_BAR:g}: {j['c2']}  ->  converged: {j['conv']}")
            print(f"  READING {z['name']}: {j['reading']}")
            allj[z["name"]] = j["reading"]
    if allj:
        print("\nreadings: " + "; ".join(f"{k}: {v}" for k, v in allj.items()))

if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--checks" in sys.argv:
        sys.exit(checks())
    main()

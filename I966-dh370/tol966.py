#!/usr/bin/env python3
"""#966 tol_od test (coordinator's hc 2026-11-19): per accepted step of ks_chain3b's legs from LEG0 on, the corrector's final max|F|
('octo-double Newton: N steps, max|F| X' line), the smallest pivot of its last iteration, the Delta error estimate |F| / sigma_Delta
with sigma_Delta = that pivot and with 1.6e-17 (the coordinator's), the octo-double steps and the corrector seconds (the a-line's).
Pass for a step: both estimates <= 1e-18.
From the coordinator's correction (hc 2026-11-19 ~13:30 UTC): the smallest pivot is not sigma_Delta; near_null's sigma_Delta (dh170) is the
denominator that counts. --sigma D=S[,D=S...] adds a column |F| / sigma_Delta(near_null) for the states at those D (4 decimals), 'n/a' otherwise.
usage: python3 -I tol966.py CHAIN_OUT LEG0_PREFIX [--sigma 251.2845=2.822e-18]     python3 -I tol966.py --selftest [--mutate]"""
import glob, re, sys

SIG = 1.6e-17


def steps(text):
    out, fin, piv = [], None, None
    L = text.splitlines()
    for i, l in enumerate(L):
        m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)", l)
        if m:
            fin = (int(m.group(1)), float(m.group(2)), m.group(3))
        m = re.search(r"piv ([0-9.e+-]+)\.\.", l)
        if m and re.match(r"\s+on \d+: \|F\|", l):
            piv = float(m.group(1))
        m = re.match(r"\s+a [0-9.]+ -> D ([0-9.]+):.* (\d+) s$", l)
        if m:
            acc = any("Delta of the saved state" in x for x in L[i + 1:i + 3])
            if fin and acc:
                n, F, c = fin
                out.append(dict(D=m.group(1), od=n, F=F, conv=c, piv=piv, e1=F / piv if piv else None, e2=F / SIG, s=int(m.group(2))))
            fin, piv = None, None
    return out


def selftest(mutate):
    txt = """  on 0: |F| 5.29e-36 -> 1.32e-34, |dz| 3.5e-23 -> 3.1e-44, lam 1, dDelta -3.5e-23, piv 2.4e-17..2.0e+47, 1840.27 s
      octo-double Newton: 1 steps, max|F| 1.3e-34, converged; double-double |F| of its first two parts 2.8e+25
    a 0.600 -> D 251.3055: predicted |F| 2.7e+26, od 1 steps -> 2.8e+25 (tol 4.5e-20), Delta 1.68, moved 1.9e-34, 1840 s
      Delta of the saved state, its eight parts summed exactly: 1.68
"""
    if mutate:
        txt = txt.replace("1.3e-34, converged", "1.3e-34, converged").replace("2.4e-17..", "2.4e-14..")
    s = steps(txt)[0]
    bad = []
    if s["od"] != 1 or abs(s["F"] - 1.3e-34) > 1e-40 or s["conv"] != "converged" or s["s"] != 1840:
        bad.append("fields")
    if abs(s["e1"] - 1.3e-34 / 2.4e-17) > 1e-21:
        bad.append(f"e1 {s['e1']:.3e}")
    if abs(s["e2"] - 1.3e-34 / 1.6e-17) > 1e-21:
        bad.append("e2")
    print("selftest", "FAIL " + ", ".join(bad) if bad else "PASS")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest("--mutate" in sys.argv)
    out, leg0 = sys.argv[1], sys.argv[2]
    sig = {}
    if "--sigma" in sys.argv:
        for kv in sys.argv[sys.argv.index("--sigma") + 1].split(","):
            k, v = kv.split("=")
            sig[f"{float(k):.4f}"] = float(v)
    print("| leg | D | od steps | final max\\|F\\| | smallest pivot | \\|F\\|/pivot | \\|F\\|/1.6e-17 | sigma_Delta (near_null) | \\|F\\|/sigma_Delta | corrector s | pivot-based <= 1e-18 | near_null <= 1e-18 |\n|---|---|---|---|---|---|---|---|---|---|---|---|")
    for log in sorted(glob.glob(out + "/leg*/anm_run.log")):
        leg = log.split("/")[-2]
        if leg[:5] < leg0[:5]:
            continue
        for r in steps(open(log, errors="replace").read()):
            ok = r["e1"] is not None and max(r["e1"], r["e2"]) <= 1e-18
            sg = sig.get(f"{float(r['D']):.4f}")
            en = r["F"] / sg if sg else None
            print(f"| {leg[:5]} | {r['D']} | {r['od']} | {r['F']:.2e} ({r['conv']}) | {r['piv']:.2e} | {r['e1']:.2e} | {r['e2']:.2e} | "
                  f"{'%.3e' % sg if sg else 'n/a'} | {'%.2e' % en if sg else 'n/a'} | {r['s']} | {'yes' if ok else 'NO'} | {('yes' if en <= 1e-18 else 'NO') if sg else 'n/a'} |")

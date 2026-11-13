#!/usr/bin/env python3
"""#696: the keep_plan 0 ladder of run_696_k.sh, per D: Delta(K) - Delta(130k) at each rung, steps, final |F|, first |F|, elim projections, and the comparison with #491's
prediction (notes/FACTORED_HORIZON.md: Delta moves by about 3e-12 at D 245.14 and 1e-7 at D 253.80 from ks 130 to 300 if its amplification reading holds).
usage: python ladder_696.py [D245|D253]   reads D<..>/r<K>k.log and D<..>/r<K>k/base_pin3_D*.npz next to this file; exit 0 when every rung that ran converged, 1 when one did not, 2 none ran
       python ladder_696.py --selftest      synthetic rungs with planted Delta moves and logs: the moves, the steps and the convergence verdicts are recovered, and each broken
                                            input (a rung log not converged, a rung with a base but no converged line, the control r130k moved by 1e-40) is flagged
Delta of a state = the exact sum of the last entry of each of its parts (zh, zl, z2 .. z7), each a double, in mpmath (compare_696.delta_of).
Error-bar kinds: Delta values are exact sums of saved doubles of a converged octo-double state (max|F| in the log), no statistical error; the #491 numbers are a prediction, not a bound."""
import glob, importlib.util, os, re, shutil, sys, tempfile
import numpy as np
from mpmath import mp, mpf, nstr

mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("compare_696", os.path.join(HERE, "compare_696.py"))
cmp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cmp)
RUNGS = [130, 135, 145, 160, 200, 250, 300]
PRED = {"D245": mpf("3e-12"), "D253": mpf("1e-7")}   # #491, ks 130 -> 300
CHAIN = cmp.DS


def tag(k):
    return f"r{k}k"


def rung(dd, k):
    log = os.path.join(dd, tag(k) + ".log")
    base = glob.glob(os.path.join(dd, tag(k), "base_pin3_D*.npz"))
    if not os.path.exists(log):
        return None
    txt = open(log, encoding="utf-8", errors="replace").read()
    nm = re.findall(r"octo-double Newton: (\d+) steps, max\|F\| ([0-9.e+-]+), (converged|not converged)", txt)
    first = re.search(r"^\s+on 0: \|F\| ([0-9.e+-]+)", txt, re.M)
    elim = re.findall(r"elim projections (\{[^}]*\})", txt)
    return dict(delta=cmp.delta_of(base[0]) if base else None, steps=int(nm[-1][0]) if nm else None, final=float(nm[-1][1]) if nm else None,
                converged=bool(nm) and nm[-1][2] == "converged", first=float(first.group(1)) if first else None, elim=elim[-1] if elim else None)


def analyze(dd):
    out = {k: rung(dd, k) for k in RUNGS}
    ran = [k for k in RUNGS if out[k] is not None]
    return out, ran


def table(label, dd, out, ran, chain_delta=None):
    d130k = out[130]["delta"] if out[130] and out[130]["delta"] is not None else None
    print(f"\n== {label}")
    if chain_delta is not None and d130k is not None:
        print(f"   control r130k: Delta(130, new plan) - Delta(130, stored plan) = {nstr(d130k - chain_delta, 8)}  (stored plan = the chain state)")
    print("   ks    steps  first|F|   final|F|   converged  Delta(K) - Delta(130k)     elim projections")
    prev = None
    for k in ran:
        r = out[k]
        dd_ = (r["delta"] - d130k) if (r["delta"] is not None and d130k is not None) else None
        step = (r["delta"] - prev) if (r["delta"] is not None and prev is not None) else None
        print(f"   {k:<5d} {str(r['steps']):<6s} {('%.2e' % r['first']) if r['first'] else '-':<10s} {('%.1e' % r['final']) if r['final'] else '-':<10s} {'yes' if r['converged'] else 'NO':<10s} "
              f"{nstr(dd_, 8) if dd_ is not None else '-':<26s} {r['elim'] or ''}")
        if r["converged"] and r["delta"] is not None:
            prev = r["delta"]
    last = [k for k in ran if out[k]["converged"]]
    if last and last[-1] == 300 and d130k is not None:
        move = out[300]["delta"] - d130k
        p = PRED[label]
        print(f"   Delta(300) - Delta(130k) = {nstr(move, 8)}; #491 predicts about {nstr(p, 2)}; ratio {nstr(move / p, 4)}")
    elif last:
        print(f"   last converged rung: ks {last[-1]}; first rung that did not converge: " + (str([k for k in ran if not out[k]['converged']][0]) if any(not out[k]['converged'] for k in ran) else "none yet"))


def verdict(out, ran):
    return 2 if not ran else (0 if all(out[k]["converged"] for k in ran) else 1)


def selftest():
    tmp = tempfile.mkdtemp(prefix="lad696_")
    KEYS = cmp.KEYS

    def parts(x):
        o, rem = [], mpf(x)
        for _ in range(8):
            p = float(rem)
            o.append(p)
            rem -= mpf(p)
        return o

    def mk(dd, k, delta, steps=5, final="1e-85", conv=True, first="3.0e-36", write_base=True):
        os.makedirs(os.path.join(dd, tag(k)), exist_ok=True)
        if write_base:
            np.savez(os.path.join(dd, tag(k), "base_pin3_D245.1366.npz"), **{kk: np.array([0.0, v]) for kk, v in zip(KEYS, parts(delta))}, meta="{}")
        with open(os.path.join(dd, tag(k) + ".log"), "w") as f:
            f.write(f"  on 0: |F| {first} -> 1e-37, lam 1\n      elim projections {{'ladder': 3, 'failed': 0}}\n      octo-double Newton: {steps} steps, max|F| {final}, {'converged' if conv else 'not converged'}; x\n")

    base = mpf("1.685761245195318")
    plan = {130: base, 135: base + mpf("1e-14"), 145: base + mpf("1e-13"), 160: base + mpf("1e-12"), 200: base + mpf("2e-12"), 250: base + mpf("3e-12"), 300: base + mpf("3.1e-12")}
    ok = True
    d = os.path.join(tmp, "D245")
    for k in RUNGS:
        mk(d, k, plan[k], steps=3 + k // 100)
    out, ran = analyze(d)
    got = abs((out[300]["delta"] - out[130]["delta"]) - mpf("3.1e-12")) < mpf("1e-40") and abs((out[160]["delta"] - out[130]["delta"]) - mpf("1e-12")) < mpf("1e-40") and out[300]["steps"] == 6 and verdict(out, ran) == 0
    print("planted Delta moves (160: 1e-12, 300: 3.1e-12), steps and an all-converged verdict recovered:", "ok" if got else "FAIL")
    ok &= got
    d2 = os.path.join(tmp, "M1")
    for k in RUNGS:
        mk(d2, k, plan[k], conv=(k != 200), final="2e-20" if k == 200 else "1e-85")
    out2, ran2 = analyze(d2)
    got = verdict(out2, ran2) == 1 and not out2[200]["converged"] and out2[160]["converged"]
    print("a rung that did not converge (ks 200) is flagged, exit 1:", "ok" if got else "FAIL")
    ok &= got
    d3 = os.path.join(tmp, "M2")
    for k in (130, 135):
        mk(d3, k, plan[k])
    out3, ran3 = analyze(d3)
    got = ran3 == [130, 135] and verdict(out3, ran3) == 0 and out3[145] is None
    print("rungs not run are not counted as failures (ran [130, 135]):", "ok" if got else "FAIL")
    ok &= got
    d4 = os.path.join(tmp, "M3")
    mk(d4, 130, plan[130], write_base=False)
    out4, ran4 = analyze(d4)
    got = out4[130]["delta"] is None and out4[130]["converged"]
    print("a log that converged but saved no base has Delta None (no value invented):", "ok" if got else "FAIL")
    ok &= got
    chain = base + mpf("1e-40")   # the control moved by 1e-40 against the stored plan: must show as a nonzero move
    mv = out[130]["delta"] - chain
    got = abs(mv + mpf("1e-40")) < mpf("1e-50")
    print("the control's move against the stored plan is reported (planted -1e-40):", "ok" if got else "FAIL")
    ok &= got
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    which = [a for a in sys.argv[1:] if a in CHAIN] or list(CHAIN)
    code = 2
    for lab in which:
        out, ran = analyze(os.path.join(HERE, lab))
        chain_delta = cmp.delta_of(os.path.join(cmp.RAW, CHAIN[lab]))
        table(lab, lab, out, ran, chain_delta)
        code = min(code, verdict(out, ran)) if code != 2 else verdict(out, ran)
    sys.exit(code)

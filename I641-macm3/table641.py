#!/usr/bin/env python3
"""#641: the base polish and the first step of anm_run.py --kfreeze K (K = 9, 7; control K = 3 at D 80) at D 80, 100, 150, 200.
Per run: whether the octo-double base polish converged (steps, max|F|), Delta_base - Delta_state (exact sums of the saved base's parts and of the
stored state's, mp 80 digits), a_max, and the first step's outcome (predicted |F|, accepted or not, Delta of the saved state at D + 1).
Usage: python3 table641.py [RAW worktree]"""
import glob, json, os, re, sys
import mpmath as mp
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-b640/hp")
from hpkernel.driver import load_q
mp.mp.dps = 80
here = os.path.dirname(os.path.abspath(__file__))
RAW = sys.argv[1] if len(sys.argv) > 1 else os.path.join(here, "..")
def delta(path):
    z, m = load_q(path)
    return sum((mp.mpf(float(p[-1])) for p in z), mp.mpf(0))
def state(D):
    return os.path.join(RAW, "T138-win2", "chain_o" if D == 200 else "chain", f"anm_pin3_D{D}.0000.npz")
fits = {80: "4.2e-14 (d10)", 100: "1.2e-12 (d10)", 150: "1.1e-11 (d6)", 200: "2.8e-11 (d6)"}
print("| D | K | base polish | octo-double Newton steps, max abs F | Δ_base − Δ_state | a_max | first step (a = 1) | fits err (delta_all.csv) |")
print("|---|---|---|---|---|---|---|---|")
for D in (80, 100, 150, 200):
    d0 = delta(state(D))
    for K in (3, 9, 7):
        d = os.path.join(here, f"K{K}_D{D}")
        lg = os.path.join(here, f"K{K}_D{D}.log")
        if not os.path.exists(lg):
            continue
        t = open(lg).read()
        m = re.search(r"octo-double Newton: (\d+) steps, max\|F\| (\S+?),? (not converged|converged|NOT converged|stalled[^\n]*)", t)
        base = glob.glob(os.path.join(d, f"base_pin{K}_D{D}.0000.npz"))
        pol = f"{m.group(3)}" if m else "(not finished)"
        stopped = os.path.exists(os.path.join(here, "stops.txt")) and f"K{K}_D{D} stopped" in open(os.path.join(here, "stops.txt")).read()
        if stopped and not m:
            on = re.findall(r"on (\d+): \|F\| (\S+) -> (\S+),", t)
            pol = f"not converging: |F| {on[0][1]} -> {on[-1][2]} after {len(on)} steps, stopped (stops.txt)"; stp = f"{len(on)}, {on[-1][2]}"
        na = re.search(r"base polish not adopted \(max\|F\| (\S+) -> (\S+)\)", t)
        if na: pol = f"not converged, not adopted (|F| {na.group(1)} -> {na.group(2)})"
        stp = f"{m.group(1)}, {m.group(2)}" if m else "-"
        dd = f"{float(delta(base[0]) - d0):+.3e}" if base else "-"
        js = os.path.join(d, "anm_run.jsonl")
        am = "-"; first = "stopped (polish not adopted; stops.txt)" if na else ("stopped (polish not converging; stops.txt)" if stopped and not m else "-")
        if os.path.exists(js) and os.path.getsize(js) and not na:
            r = json.loads(open(js).readline())
            am = f"{r['a_max']:.2f}"
            first = "accepted" if r["converged"] else "NOT accepted"
            q = re.search(r"a 1\.000 -> D [\d.]+: predicted \|F\| (\S+), od (\d+) steps -> (\S+) \(tol (\S+), ([^,)]*)", t)
            allm = re.findall(r"octo-double Newton: (\d+) steps, max\|F\| (\S+?), (converged|not converged)", t)
            if len(allm) > 1: first += f"; octo-double Newton of the step: {allm[1][0]} steps, max|F| {allm[1][1]}, {allm[1][2]}"
            if q: first += f" (double-double |F| of its first two parts: predicted {q.group(1)}, final {q.group(3)}; {q.group(5)})"
        print(f"| {D} | {K}{' (control)' if K == 3 else ''} | {pol} | {stp} | {dd} | {am} | {first} | {fits[D]} |")

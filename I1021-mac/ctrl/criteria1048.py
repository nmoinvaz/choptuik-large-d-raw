#!/usr/bin/env python3
"""#1048 section 3 (README.md): the proposed criteria per radius from the noise table, and the stored control walks judged again
under them. Per (M, xi1): walk bar 3 sigma_1(M, xi1) on |r_1| at the walk's best point (section 1's sigma_1, from the Mac's
noise/table.jsonl); step bars unchanged (walk1026 3e-6, walk1027 3e-4); position: the zero within 1e-5 in A and in w/w_inf
of the stored zero; M = 7 also |F7/F5| at the first solve within 5% of 0.0574. Replay of a walk from its log's iteration lines:
the first iteration meeting the step and walk bars is where it would have stopped (each test uses only points already solved),
its zero = best point + Newton step (as printed, 9 and 4 digits); none met: FAIL when the walk stopped by itself (no step
lowered |r_1|, the iteration cap or a failed solve: the same history follows under any bar), "needs a rerun" when the old
bar stopped it at a point the new bar does not accept.
    python criteria1048.py [TABLE]          TABLE default noise/table.jsonl
    python criteria1048.py selftest [--mutate=nopos]   synthetic walks (the mutation drops the position bar: must fail)"""
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
Z7 = os.path.join(HERE, "..", "z7_m7")
DH = os.path.join(HERE, "dh610_478ecf4b")
STORED = {5: (2.718579189, 0.999228404), 7: (2.71924, 1.000025)}
STEP = {5: 3e-6, 7: 3e-4}
POS, RATIO, RATIO_TOL = 1e-5, 0.0574, 0.05
WALKS = [("Mac", 5, "0.15", f"{Z7}/xi015/logs/walk_control5_xi0.15.log", f"{Z7}/xi015/walks/walk_control5_xi0.15.json"),
         ("Mac", 5, "0.2", f"{Z7}/logs/walk_control5_xi0.2.log", f"{Z7}/walks/walk_control5_xi0.2.json"),
         ("Mac", 7, "0.15", f"{Z7}/xi015/logs/walk_control_xi0.15.log", f"{Z7}/xi015/walks/walk_control_xi0.15.json"),
         ("Mac", 7, "0.2", f"{Z7}/logs/walk_control_xi0.2.log", f"{Z7}/walks/walk_control_xi0.2.json"),
         ("dh610", 5, "0.15", f"{DH}/I1021-dh610_z16_m7_xi015_logs_walk_control5_xi0.15.log", f"{DH}/I1021-dh610_z16_m7_xi015_walks_walk_control5_xi0.15.json"),
         ("dh610", 5, "0.2", f"{DH}/I1026-dh610_logs_walk_control_xi0.2.log", f"{DH}/I1026-dh610_walks_walk_control_xi0.2.json"),
         ("dh610", 5, "0.25", f"{DH}/I1026-dh610_logs_walk_control_xi0.25.log", f"{DH}/I1026-dh610_walks_walk_control_xi0.25.json"),
         ("dh610", 7, "0.2", f"{DH}/I1021-dh610_z16_m7_logs_walk_control_xi0.2.log", f"{DH}/I1021-dh610_z16_m7_walks_walk_control_xi0.2.json"),
         ("dh610", 7, "0.25", f"{DH}/I1021-dh610_z16_m7_logs_walk_control_xi0.25.log", f"{DH}/I1021-dh610_z16_m7_walks_walk_control_xi0.25.json")]
IT = re.compile(r"^iteration (\d+): best \|r_1\| ([0-9.]+e[+-]\d+) at \(([0-9.]+), ([0-9.]+)\); Newton step \(([+-][0-9.]+e[+-]\d+), ([+-][0-9.]+e[+-]\d+)\)", re.M)


def judge(M, its, verdict, first, bar, mut=""):
    """(PASS|FAIL|needs a rerun|no criterion, text); its: [(k, r1, A, w, dA, dw)], first: the walk's first point"""
    if bar is None:
        return "no criterion", "fewer than 2 converged noise solves at this M and radius"
    if not its:
        return "FAIL", "no iteration: " + str(verdict.get("why"))
    for k, r1, A, w, dA, dw in its:
        if abs(dA) < STEP[M] and abs(dw) < STEP[M] and r1 <= bar:
            zA, zw = A + dA, w + dw
            dz = (zA - STORED[M][0], zw - STORED[M][1])
            ok = mut == "nopos" or (abs(dz[0]) <= POS and abs(dz[1]) <= POS)
            txt = f"stops at iteration {k} (|r_1| {r1:.3g} <= bar {bar:.3g}), zero ({zA:.9f}, {zw:.9f}), {dz[0]:+.2e}, {dz[1]:+.2e} from the stored zero"
            if M == 7:
                ra = math.hypot(*first["F7"]) / math.hypot(*first["F5"]) if first and first.get("F7") else None
                rok = ra is not None and abs(ra - RATIO) <= RATIO_TOL * RATIO
                ok = ok and rok
                txt += f"; |F7/F5| at the first solve {ra:.4f}" if ra is not None else "; no |F7/F5|"
            return ("PASS" if ok else "FAIL"), txt
    last = its[-1]
    if verdict.get("converged"):
        return "needs a rerun", f"the old bar stopped it at iteration {last[0]} (|r_1| {last[1]:.3g}), above the bar {bar:.3g}"
    return "FAIL", f"no iteration meets the bars (best |r_1| {min(i[1] for i in its):.3g}, bar {bar:.3g}); stopped by itself: {verdict.get('why')}"


def bars(table):
    return {(r["M"], r["xi1"]): (3 * r["sigma1"] if r["sigma1"] is not None else None, r) for r in table}


def main(path):
    tb = bars([json.loads(l) for l in open(path)])
    print("per radius and M: converged noise solves of 5, sigma_1, walk bar 3 sigma_1, |mean r_1|")
    for (M, xi), (bar, r) in sorted(tb.items(), key=lambda t: (t[0][0], float(t[0][1]))):
        m = math.hypot(*r["mean_r1"]) if r["mean_r1"] else None
        print(f"  M {M} xi1 {xi}: {r['converged']} of {r['solves']}, sigma_1 " + (f"{r['sigma1']:.3g}, bar {bar:.3g}" if bar else "none, no bar")
              + (f", |mean r_1| {m:.3g}" if m is not None else ""))
    res = {}
    for who, M, xi, log, js in WALKS:
        if not os.path.exists(js):
            print(f"{who} M {M} xi1 {xi}: no walk")
            continue
        w = json.load(open(js))
        its = [(int(k), float(r), float(A), float(ww), float(a), float(b)) for k, r, A, ww, a, b in IT.findall(open(log).read())]
        lab, txt = judge(M, its, w["verdict"], w["points"][0] if w.get("points") else None, tb.get((M, xi), (None,))[0])
        res[(who, M, xi)] = lab
        print(f"{who} M {M} xi1 {xi}: {lab}: {txt}")
    print("both controls passing under the proposed criteria, by machine and radius:")
    for who in ("Mac", "dh610"):
        for xi in ("0.15", "0.175", "0.2", "0.225", "0.25"):
            a, b = res.get((who, 5, xi), "no walk"), res.get((who, 7, xi), "no walk")
            print(f"  {who} xi1 {xi}: M = 5 {a}, M = 7 {b}: {'YES' if a == b == 'PASS' else 'no'}")
    return 0


def selftest(mut):
    good5 = [(0, 120.0, 2.7264, 1.0156, -4e-3, -1.5e-2), (1, 0.03, 2.7185812, 0.9992290, -2e-6, -5e-7)]
    off5 = [(0, 0.03, 2.7186, 0.99923, 1e-6, 1e-6)]                          # 2e-5 from the stored zero
    got = [judge(5, good5, dict(converged=False), None, 0.09, mut)[0], judge(5, good5, dict(converged=True), None, 0.01, mut)[0],
           judge(5, good5, dict(converged=False, why="five halvings"), None, 0.01, mut)[0], judge(5, off5, dict(converged=True), None, 0.09, mut)[0],
           judge(5, [], dict(converged=False, why="start"), None, 0.09, mut)[0], judge(5, good5, dict(converged=True), None, None, mut)[0]]
    want = ["PASS", "needs a rerun", "FAIL", "FAIL", "FAIL", "no criterion"]
    ok = got == want
    print(f"selftest{' --mutate=' + mut if mut else ''}: {got} (expect {want}): {'PASS' if ok else 'FAIL'}")
    return ok


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(0 if selftest("nopos" if "--mutate=nopos" in sys.argv else "") else 1)
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "noise", "table.jsonl")))

#!/usr/bin/env python3
"""persist1020.py --counts F1 F2 ... [--counts G1 ...] [--box A0,A1,wf0,wf1 ...] [--exclude A,wf ...] [--selftest] [--mutate=sign|shift]: persist1013.py's rule (xfchecks, #1013; same sign, |dA| <= 0.2,
|dwf| <= 0.25, the nearest M = 3 zero serves one M = 1 zero; a missing partner is an M = 1 artefact when the window is resolved and undecided when the counted region or unresolved cells cut it)
for several counted regions. Each --counts group is one chain (a count and its recount rungs): its zeros join the pool and the unresolved cells of its last file stay unresolved. Each --box is a counted
rectangle (default: #1013's A 1.9-3.9, wf 0.2-1.1 and #1020's A 1.9-3.0, wf 0.03-0.2); a window is inside the counted region when the boxes' union covers it. --exclude A,wf drops the M = 3 zero located
there (to read the verdicts without a partner that failed #1020's relocation). The M = 1 zeros and the pairing are persist1013.py's. Controls (--selftest, exit 1 on a failed control): persist1013's three, and
a window straddling the hole of the two boxes' union is not inside while one in the union is."""
import json
import sys

from persist1013_orig import CORE, DA, DW, M1, pair
import persist1013_orig as P13

BOXES = [(1.9, 3.9, 0.2, 1.1), (1.9, 3.0, 0.03, 0.2)]


def covered(win, boxes):
    """True when the rectangle win = (A0, A1, wf0, wf1) lies in the union of the boxes (elementary cells of the edge grid)"""
    xs = sorted({win[0], win[1]} | {v for b in boxes for v in b[:2] if win[0] < v < win[1]})
    ys = sorted({win[2], win[3]} | {v for b in boxes for v in b[2:] if win[2] < v < win[3]})
    for x0, x1 in zip(xs, xs[1:]):
        for y0, y1 in zip(ys, ys[1:]):
            cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
            if not any(b[0] <= cx <= b[1] and b[2] <= cy <= b[3] for b in boxes):
                return False
    return True


def selftest():
    ok = P13.selftest()
    inside = covered((2.2, 2.6, 0.05, 0.5), BOXES)
    hole = covered((2.9, 3.3, 0.05, 0.3), BOXES)
    past = covered((1.8, 2.3, 0.1, 0.3), BOXES)
    good = inside and not hole and not past
    print(f"selftest (union): a window in the union is inside {inside}, one over the hole at A > 3.0, wf < 0.2 is not {not hole}, one past A 1.9 is not {not past}: {'PASS' if good else 'FAIL'}")
    return ok and good


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest() else 1
    chains, i = [], 0
    while i < len(argv):
        if argv[i] == "--counts":
            j = i + 1
            while j < len(argv) and not argv[j].startswith("--"):
                j += 1
            chains.append(argv[i + 1:j])
            i = j
        else:
            i += 1
    boxes = [tuple(float(v) for v in argv[i + 1].split(",")) for i, a in enumerate(argv) if a == "--box"] or BOXES
    excl = [tuple(float(v) for v in argv[i + 1].split(",")) for i, a in enumerate(argv) if a == "--exclude"]
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    m3, unres, leaf_sum, dropped = [], [], 0, []
    for ch in chains:
        for p in ch:
            d = json.load(open(p))
            leaf_sum += d.get("leaf_sum") or 0
            for z in d["zeros"]:
                loc = z.get("located")
                a, w = (loc["A"], loc["wf"]) if loc else ((z["cell"][0] + z["cell"][1]) / 2, (z["cell"][2] + z["cell"][3]) / 2)
                if any(abs(a - e[0]) < 1e-5 and abs(w - e[1]) < 1e-5 for e in excl):
                    dropped.append((z["W"], a, w))
                    continue
                m3.append((z["W"] * (-1 if mut == "sign" else 1), a + (0.3 if mut == "shift" else 0), w, bool(loc)))
        unres += json.load(open(ch[-1]))["unresolved"]
    print(f"M = 3 zeros from {sum(map(len, chains))} count file(s) in {len(chains)} chain(s): {len(m3)}, sum of signs {sum(z[0] for z in m3)}, leaf sum {leaf_sum}, unresolved cells after each chain's last file {len(unres)}"
          + (f"; excluded {len(dropped)}" if dropped else ""))
    for z in m3:
        print(f"   M = 3 zero of sign {z[0]:+d} at A {z[1]:.6f}, wf {z[2]:.6f}{'' if z[3] else ' (cell centre, not located)'}")
    for z in dropped:
        print(f"   excluded M = 3 zero of sign {z[0]:+d} at A {z[1]:.6f}, wf {z[2]:.6f}")
    pr = pair(M1, [z[:3] for z in m3])
    served = set(pr.values())
    print("M = 1 zeros inside the counted region (boxes " + "; ".join("A %.2f-%.2f, wf %.2f-%.2f" % b for b in boxes) + ") (windows |dA| <= %.2f, |dwf| <= %.2f):" % (DA, DW))
    for k, (s, a, w) in enumerate(M1):
        if not any(b[0] <= a <= b[1] and b[2] <= w <= b[3] for b in boxes):
            continue
        win = (a - DA, a + DA, w - DW, w + DW)
        inside = covered(win, boxes)
        cut = [u for u in unres if u[0] < win[1] and u[1] > win[0] and u[2] < win[3] and u[3] > win[2]]
        tag = "CORE" if a in CORE else "    "
        if k in pr:
            z = m3[pr[k]]
            verdict = f"PERSISTS: M = 3 zero {z[0]:+d} at ({z[1]:.6f}, {z[2]:.6f}), shift ({z[1] - a:+.4f}, {z[2] - w:+.4f})"
        else:
            why = []
            if not inside:
                why.append("window extends past the counted region")
            if cut:
                why.append(f"{len(cut)} unresolved cell(s) in the window")
            verdict = "NO PARTNER, " + ("undecided: " + "; ".join(why) if why else "window resolved: an M = 1 truncation artefact")
        print(f"   {tag} sign {s:+d} A {a:.6f}, wf {w:.6f}: {verdict}")
    for j, z in enumerate(m3):
        if j not in served:
            print(f"   M = 3 zero without partner: sign {z[0]:+d} at ({z[1]:.6f}, {z[2]:.6f})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

#!/usr/bin/env python3
"""persist1013.py [--counts m3/count_A.json ...] [--box A0,A1,wf0,wf1] [--selftest] [--mutate=sign|shift]: the persistence reading fixed before the runs (xfchecks, #1013): an M = 1 zero persists
when an M = 3 zero of the same sign lies within the known zero's shift, |dA| <= 0.2 and |dwf| <= 0.25 (the known zero shifts by +0.184 and +0.239); each M = 3 zero serves one M = 1 zero, the nearest
(by max(|dA|/0.2, |dwf|/0.25)); an M = 1 zero with no partner is an M = 1 truncation artefact when its window is resolved at M = 3, and undecided when unresolved cells or the edge of the counted box
cut its window; an M = 3 zero with no partner is reported too.
The M = 1 zeros are xfchecks' 25 below A 3.98 (#995 comment 7004433173, raw I995-mac 3b74d753), A, wf, sign. M = 3 zeros are read from the count files' `zeros` (located A, wf, sign W; the cell's centre when
not located); the unresolved cells are the last count's `unresolved`. Controls (--selftest): the known M = 1 zero (2.542148, 0.776994, +1) with the M = 3 zero (2.726476, 1.015603, +1) persists; the same
with the sign flipped, or with A shifted by 0.3, does not. Exit 1 on a failed control."""
import json
import sys

M1 = [(-1, 2.139401, 0.278745), (+1, 2.399986, 0.283107), (-1, 2.498222, 0.409349), (+1, 2.542148, 0.776994), (-1, 2.642772, 0.280029), (+1, 2.877304, 0.300451),
      (-1, 3.018699, 0.556954), (+1, 3.094042, 0.688487), (-1, 3.104757, 0.352660), (+1, 3.216677, 0.588357), (+1, 3.307235, 0.367124), (-1, 3.407728, 0.614987),
      (-1, 3.495560, 0.366224), (+1, 3.589749, 0.639405), (-1, 3.659774, 0.265120), (+1, 3.674531, 0.360326), (-1, 3.764805, 0.662816), (+1, 3.932913, 0.684881),
      (-1, 4.094586, 0.705259), (+1, 4.250416, 0.724027), (-1, 4.401009, 0.741479), (+1, 4.546874, 0.757870), (-1, 4.631715, 0.983982), (-1, 4.688425, 0.773346),
      (+1, 4.754081, 1.003258)]
CORE = (2.139401, 2.399986, 2.498222, 2.642772)    # the four stable M = 1 zeros at A 2.14-2.64, wf 0.28-0.41 (the issue's candidates)
DA, DW = 0.2, 0.25


def pair(m1, m3):
    """greedy nearest pairing, same sign and inside the window; returns {index of M = 1: index of M = 3}"""
    cand = []
    for i, (s1, a1, w1) in enumerate(m1):
        for j, (s3, a3, w3) in enumerate(m3):
            if s1 == s3 and abs(a3 - a1) <= DA and abs(w3 - w1) <= DW:
                cand.append((max(abs(a3 - a1) / DA, abs(w3 - w1) / DW), i, j))
    out, used = {}, set()
    for d, i, j in sorted(cand):
        if i not in out and j not in used:
            out[i] = j
            used.add(j)
    return out


def selftest():
    k = (+1, 2.542148, 0.776994)
    base = pair([k], [(+1, 2.726476, 1.015603)])
    flip = pair([k], [(-1, 2.726476, 1.015603)])
    far = pair([k], [(+1, 2.726476 + 0.3, 1.015603)])
    ok = base == {0: 0} and flip == {} and far == {}
    print(f"selftest: known pair persists {base == {0: 0}}, sign flipped does not persist {flip == {}}, shifted by 0.3 does not persist {far == {}}: {'PASS' if ok else 'FAIL'}")
    return ok


def main(argv):
    if "--selftest" in argv:
        return 0 if selftest() else 1
    counts = []  # every file after --counts up to the next flag, in order
    for i, a in enumerate(argv):
        if a == "--counts":
            counts += [v for v in argv[i + 1:i + 1 + next((j for j, b in enumerate(argv[i + 1:]) if b.startswith("--")), len(argv))]]
    box = tuple(float(v) for v in argv[argv.index("--box") + 1].split(",")) if "--box" in argv else (1.9, 3.9, 0.2, 1.1)
    mut = next((a.split("=")[1] for a in argv if a.startswith("--mutate=")), "")
    m3, unres, leaf_sum = [], [], 0
    for p in counts:
        d = json.load(open(p))
        leaf_sum += d.get("leaf_sum") or 0
        for z in d["zeros"]:
            loc = z.get("located")
            a, w = (loc["A"], loc["wf"]) if loc else ((z["cell"][0] + z["cell"][1]) / 2, (z["cell"][2] + z["cell"][3]) / 2)
            m3.append((z["W"] * (-1 if mut == "sign" else 1), a + (0.3 if mut == "shift" else 0), w, bool(loc)))
        last = d["unresolved"]
    unres = last if counts else []
    print(f"M = 3 zeros from {len(counts)} count file(s): {len(m3)}, sum of signs {sum(z[0] for z in m3)}, leaf sum {leaf_sum}, unresolved cells after the last file {len(unres)}")
    for z in m3:
        print(f"   M = 3 zero of sign {z[0]:+d} at A {z[1]:.6f}, wf {z[2]:.6f}{'' if z[3] else ' (cell centre, not located)'}")
    pr = pair(M1, [z[:3] for z in m3])
    served = set(pr.values())
    print("M = 1 zeros inside the counted box A %.1f-%.1f, wf %.1f-%.1f (windows |dA| <= %.2f, |dwf| <= %.2f):" % (box + (DA, DW)))
    for i, (s, a, w) in enumerate(M1):
        if not (box[0] <= a <= box[1] and box[2] <= w <= box[3]):
            continue
        win = (a - DA, a + DA, w - DW, w + DW)
        inside = win[0] >= box[0] and win[1] <= box[1] and win[2] >= box[2] and win[3] <= box[3]
        cut = [u for u in unres if u[0] < win[1] and u[1] > win[0] and u[2] < win[3] and u[3] > win[2]]
        tag = "CORE" if a in CORE else "    "
        if i in pr:
            z = m3[pr[i]]
            verdict = f"PERSISTS: M = 3 zero {z[0]:+d} at ({z[1]:.6f}, {z[2]:.6f}), shift ({z[1] - a:+.4f}, {z[2] - w:+.4f})"
        else:
            why = []
            if not inside:
                why.append("window extends past the counted box")
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

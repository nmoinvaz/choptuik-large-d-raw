"""#1101 R1: the root scan of R1's state (k_c 127, D 23.0, kappa 0.5) read as the order's bars 2-5 (issue #1101, comment 7212257601).
Reads R1/scan/scan_D23.0_p*.jsonl and R1's record; prints markdown: the points, the bracketing pair, the det-linear root(R1) from it (the zero of the straight line through
f = sign * exp(ln|det| - ref), ref the larger ln|det| of the pair; the reader's definition), delta_1 = root(R1) - root(B) with root(B) = 0.045967998 (state B's root from its (0.045, 0.050)
pair), Delta_R1 beside Delta_R0 (and Delta_R2 if given), and, if delta_2 is given, bar 4's r = delta_1/(delta_2 - delta_1) and the order p of (0.7^p - 0.5^p)/(0.5^p - 0.35^p) = r.
The bracketing pair is (0.045, 0.050) if it brackets, else the one robust sign change among the neighbouring points (several: all listed, none chosen).
usage: results_R1.py [--delta2=X] [--dR2=X] [--root2=X]   |   results_R1.py selftest [--mutate=r|pair]   (exit 0 only if every planted case reads as written)
--root2 = root(R2) (delta_2 = root2 - root(B)); mutations (each must make the selftest exit 1): r (r = delta_1/delta_2), pair (the last bracket instead of the (0.045, 0.050) one)"""
import glob, json, math, os, sys
from scipy.optimize import brentq
O = "/home/nathan/Source/choptuik-large-d-raw-wt613/I1101-dh370"
R = O + "/R1"
ROOT_B = 0.045967998
DELTA_R0 = 1.1743225027439044                                   # win2's R0 re-solve (record blob d1a3a641), = state B's record
KAP = (0.7, 0.5, 0.35)
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), "")
OPT = dict(a[2:].split("=", 1) for a in sys.argv[1:] if a.startswith("--") and "=" in a)


def lin(r1, r2):
    ref = max(r1["ln"], r2["ln"])
    f1 = r1["sign"] * math.exp(r1["ln"] - ref); f2 = r2["sign"] * math.exp(r2["ln"] - ref)
    return r1["lam"] + (r2["lam"] - r1["lam"]) * f1 / (f1 - f2)


def brackets(W):
    return [(a, b) for a, b in zip(W, W[1:]) if a["sign"] != b["sign"]]


def pick(W):
    """the (0.045, 0.050) pair if it brackets and both are robust; else the robust brackets (the last of them under the pair mutation)"""
    br = [(a, b) for a, b in brackets(W) if a.get("robust") and b.get("robust")]
    pref = [(a, b) for a, b in br if abs(a["lam"] - 0.045) < 1e-9 and abs(b["lam"] - 0.050) < 1e-9]
    if MUT == "pair":
        return br[-1:] or []
    return pref or br


def order_p(r):
    g = lambda p: (KAP[0] ** p - KAP[1] ** p) / (KAP[1] ** p - KAP[2] ** p) - r
    try:
        return brentq(g, 0.5, 12.0)
    except ValueError:
        return None


def ratio(d1, d2):
    return d1 / d2 if MUT == "r" else d1 / (d2 - d1)


def load():
    rows = {}
    for f in sorted(glob.glob(R + "/scan/scan_D23.0_p*.jsonl")):
        for l in open(f):
            if l.strip():
                w = json.loads(l); rows[round(w["lam"], 6)] = w
    return [rows[k] for k in sorted(rows)]


def main():
    W = load()
    print("| lambda | hybrid sign | noise-robust | robust (dln <= 0.1) | dln | float64 sign | ln\\|det\\| | seconds |")
    print("|---|---|---|---|---|---|---|---|")
    for w in W:
        print(f"| {w['lam']:.3f} | {w['sign']:+.0f} | {w['noise_robust']} | {w.get('robust')} | {w['dln']:.2e} | {w['f64_sign']:+.0f} | {w['ln']:.10f} | {w['sec']} |")
    print(f"\n- points {len(W)}; all noise-robust and robust: {all(w['noise_robust'] and w.get('robust') for w in W)}; signs: " + " ".join(f"{w['lam']:.3f}{'+' if w['sign'] > 0 else '-'}" for w in W))
    allbr = brackets(W); br = pick(W)
    print(f"- hybrid sign changes: {[(a['lam'], b['lam']) for a, b in allbr] or 'none'}; robust ones: {[(a['lam'], b['lam']) for a, b in br] or 'none'}")
    rec = [json.loads(l) for l in open(R + "/l1kc127k050dh370.jsonl") if l.strip()][-1]
    print(f"- R1 record: |F| {rec['F']:.6e}, steps {rec['steps']}, Delta {rec['Delta']!r}, psi-constraint {rec['constraint']:.6e}, kappa {rec['kappa']}, {rec['seconds']} s")
    print(f"- **Delta_R1 {rec['Delta']!r}; Delta_R0 {DELTA_R0!r}; Delta_R1 - Delta_R0 = {rec['Delta'] - DELTA_R0:+.4e}**" + (f"; Delta_R2 {float(OPT['dR2'])!r}; Delta_R1 - Delta_R2 = {rec['Delta'] - float(OPT['dR2']):+.4e}" if "dR2" in OPT else "; Delta_R2 not given"))
    if "dR2" in OPT:
        d2 = float(OPT["dR2"])
        if abs(rec["Delta"] - d2) >= 2e-6:
            r = (DELTA_R0 - rec["Delta"]) / (rec["Delta"] - d2)
            print(f"- bar 2: |Delta_R1 - Delta_R2| >= 2e-6: r for Delta = (D0.7 - D0.5)/(D0.5 - D0.35) = {r:.3f} (kappa^4 predicts 3.74), order p {order_p(r)}")
        else:
            print("- bar 2: |Delta_R1 - Delta_R2| < 2e-6: r for Delta is not formed")
    if len(br) != 1:
        print(f"- **no single robust bracketing pair ({len(br)}): root(R1) is not read; {'several brackets are listed above' if br else 'no robust sign change in the scanned lambda'}**")
        return None
    a, b = br[0]; root = lin(a, b); d1 = root - ROOT_B
    print(f"- bracketing pair ({a['lam']:.3f}, {b['lam']:.3f}){' = the (0.045, 0.050) pair' if abs(a['lam'] - 0.045) < 1e-9 else ''}: **root(R1) det-linear {root:.9f}; delta_1 = root(R1) - root(B) = {d1:+.6f}** (root(B) {ROOT_B})")
    print(f"- bar 5 reading (if |delta_2| <= 1e-3, |delta_1| <= 1e-3 is expected): |delta_1| <= 1e-3: {abs(d1) <= 1e-3}; |delta_1| >= 3e-3: {abs(d1) >= 3e-3}")
    d2 = float(OPT["delta2"]) if "delta2" in OPT else (float(OPT["root2"]) - ROOT_B if "root2" in OPT else None)
    if d2 is None:
        print("- delta_2 not given: r is not formed (the order reports delta_1 at once)")
    elif abs(d2) >= 3e-3:
        r = ratio(d1, d2); p = order_p(r)
        print(f"- bar 4 (|delta_2| = {abs(d2):.6f} >= 3e-3): **r = delta_1/(delta_2 - delta_1) = {r:.3f}** (kappa^4 predicts 3.74; [3.0, 4.6] confirms: {3.0 <= r <= 4.6}); measured order p = {p if p is None else round(p, 3)}")
    else:
        print(f"- bar 5 (|delta_2| = {abs(d2):.6f} <= 3e-3): |delta_1| = {abs(d1):.6f}; |delta_1| <= 1e-3 holds: {abs(d1) <= 1e-3}" + ("" if abs(d2) <= 1e-3 else "; |delta_2| is between 1e-3 and 3e-3: neither bar applies, reported as measured"))
    return root


def selftest():
    global MUT
    def rows(f, grid=(0.045, 0.050, 0.060, 0.070)):
        return [dict(lam=l, sign=1.0 if f(l) > 0 else -1.0, ln=math.log(abs(f(l))), robust=True, noise_robust=True) for l in grid]
    ok = []
    a = 0.061                                                    # case 1: one planted root in (0.060, 0.070), det nearly linear through it
    W = rows(lambda l: (a - l) * (1 + 0.5 * (l - 0.06)))
    br = pick(W); ok.append(len(br) == 1 and (br[0][0]["lam"], br[0][1]["lam"]) == (0.060, 0.070) and abs(lin(*br[0]) - a) < 5e-4)
    W = rows(lambda l: (0.0462 - l) * (0.0615 - l) * (1 + 0.3 * (l - 0.05)))   # case 2: two roots; the (0.045, 0.050) pair is preferred
    br = pick(W); ok.append(len(br) == 1 and (br[0][0]["lam"], br[0][1]["lam"]) == (0.045, 0.050) and abs(lin(*br[0]) - 0.0462) < 1e-3)
    W = rows(lambda l: (0.0615 - l)); W[2]["robust"] = False     # case 3: the change touches a non-robust point: no robust bracket
    ok.append(pick(W) == [])
    c = 0.1                                                      # case 4: planted kappa^4 deltas give r = 3.74 and p = 4
    d1, d2 = c * (KAP[0] ** 4 - KAP[1] ** 4), c * (KAP[0] ** 4 - KAP[2] ** 4)
    r = ratio(d1, d2); p = order_p(r); ok.append(abs(r - 3.7389) < 5e-3 and p is not None and abs(p - 4.0) < 1e-6)
    d1, d2 = c * (KAP[0] ** 3 - KAP[1] ** 3), c * (KAP[0] ** 3 - KAP[2] ** 3)   # case 5: planted cubic deltas read back p = 3
    p3 = order_p(ratio(d1, d2)); ok.append(p3 is not None and abs(p3 - 3.0) < 1e-6)
    print(f"planted: root {a} -> {lin(*pick(rows(lambda l: (a - l) * (1 + 0.5 * (l - 0.06))))[0]):.6f}; r (kappa^4) {r:.4f}, p {p}; p (cubic) {p3}; cases {ok}")
    return all(ok)


if len(sys.argv) > 1 and sys.argv[1] == "selftest":
    good = selftest(); print("selftest", "passes" if good else "FAILS"); sys.exit(0 if good else 1)
main()

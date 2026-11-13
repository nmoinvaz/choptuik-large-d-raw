#!/usr/bin/env python3
"""The tables of the ff08351 rerun of #613 from the eq_*.json files of this folder (Curtis-Reid + Ruiz, the result),
beside e929849's files (../eq_*.json), #580's raw-max floor (../../I580-dh370/) and the F = 0 controls (../eq_*_F0.json).
Run from this folder."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
E929 = os.path.join(HERE, "..")
R580 = os.path.join(HERE, "..", "..", "I580-dh370")
LAYS = ["070", "080", "092", "0975"]
FS = ["1e-14", "1e-12", "1e-10"]
M = "Curtis-Reid + Ruiz"


def load(lay, F, d=HERE):
    return json.load(open(os.path.join(d, f"eq_{lay}_F{F}.json")))


def sig(d):
    return [v["sigma"] for v in d["methods"][M]["vectors"]]


runs = [(l, F) for l in LAYS for F in FS] + [("080", "5e-13"), ("080", "2e-12")]
print("1. per run: planted max |sigma(J S)/sigma(J) - 1| (bound 1e-3), entries below full weight in J and J S, entries full in one only, "
      "largest weight difference (pass: planted ok, 0 full in one only, difference below 1e-6)")
allpass = True
for lay, F in runs:
    d = load(lay, F)
    c = d["cr_sets"]
    ok = d["plant"]["ok"] and c["differ"] == 0 and c["max_dW"] < 1e-6 and c["below_J"] == c["below_JS"]
    allpass &= ok
    print(f"  0.{lay[1:]:<3} F={F:<6} planted {d['plant']['methods'][M]['rel']:.2e}  below {c['below_J']}/{c['below_JS']}  "
          f"full-in-one-only {c['differ']}  dW {c['max_dW']:.1e}  {'pass' if ok else 'FAIL'}")
print("  all 14 pass" if allpass else "  NOT all pass")
print()
print("2. #580's stability criterion: sigma_1..4 over F = 1e-14, 1e-12, 1e-10, max/min (pass below 2), and sigma_1 against F = 0")
for lay in LAYS:
    S = [sig(load(lay, F)) for F in FS]
    spread = [max(s[i] for s in S) / min(s[i] for s in S) for i in range(4)]
    s0 = sig(load(lay, "0", E929))
    print(f"  0.{lay[1:]:<3} spread", " ".join(f"{x:.4g}" for x in spread), "  pass" if max(spread) < 2 else "  FAIL",
          "  F=1e-12 / F=0:", " ".join(f"{b / a:.3g}" for a, b in zip(s0, S[1])))
print()
print("3. sigma_1 at each F: ff08351 | e929849 | #580's raw-max floor (F = 0 for reference)")
for lay in LAYS:
    s0 = sig(load(lay, "0", E929))[0]
    row = []
    for F in FS:
        a, b, c = sig(load(lay, F))[0], sig(load(lay, F, E929))[0], sig(load(lay, F, R580))[0]
        row.append(f"F={F}: {a:.4e} | {b:.4e} | {c:.4e}")
    print(f"  0.{lay[1:]:<3} F=0: {s0:.4e}   " + "   ".join(row))
a, b = sig(load("080", "5e-13"))[0], sig(load("080", "2e-12"))[0]
print(f"  0.80  extra: F=5e-13: {a:.4e}   F=2e-12: {b:.4e}")
print()
print("4. sigma_1..4 of the new floor (F = 1e-12) against e929849's and the raw-max floor's at the same F")
for lay in LAYS:
    n, e, r = sig(load(lay, "1e-12")), sig(load(lay, "1e-12", E929)), sig(load(lay, "1e-12", R580))
    print(f"  0.{lay[1:]:<3} / e929849:", " ".join(f"{x / y:.4g}" for x, y in zip(n, e)), "  / raw-max:", " ".join(f"{x / y:.4g}" for x, y in zip(n, r)))
print()
print("5. weakest equilibrated sigma (sigma_1) at F = 1e-12 and its ratio to the 0.70 layout (the 0.975 choice)")
base = sig(load("070", "1e-12"))[0]
print("  ", "  ".join(f"0.{l[1:]}: {sig(load(l, '1e-12'))[0]:.3e} (x{sig(load(l, '1e-12'))[0] / base:.3g})" for l in LAYS))

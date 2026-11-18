"""#977: read every zero with zero_digits977.py (--json), write logs/zeros977.json and the pairwise table logs/pairs977.md.

    python analyze977.py      (from this folder, RUN_PY's interpreter)
"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.dirname(HERE)
ZS = [  # name, m7_outer output file
    ("Z13e #975 rtol 1e-13, end-state repeats", f"{R}/I975-win2/logs/m7_outer_win2_rtol13_xi015.txt"),
    ("Z13p run 2: rtol 1e-13, perturbed seed 976", f"{HERE}/logs/m7_outer_win2_rtol13_s976_xi015.txt"),
    ("Z14a #976 rtol 1e-14, seed 976", f"{R}/I976-win2/logs/m7_outer_win2_rtol14_xi015.txt"),
    ("Z14b run 1 alone: rtol 1e-14, seed 977", f"{HERE}/logs/m7_outer_win2_rtol14_s977_xi015.txt"),
    ("Z14c #976 + run 1 centres (3 distinct), run 1 offsets", f"{HERE}/logs/m7_outer_win2_rtol14_comb_dedup.txt"),
    ("Z14c' same centres, #976 offsets", f"{HERE}/logs/m7_outer_win2_rtol14_comb_dedup_off976.txt"),
    ("Z14c+dup same with the duplicate solve counted twice", f"{HERE}/logs/m7_outer_win2_rtol14_comb_with_duplicate.txt"),
]
zs, allok = [], True
for name, f in ZS:
    p = subprocess.run([sys.executable, "-I", os.path.join(HERE, "zero_digits977.py"), f, "--json"], capture_output=True, text=True)
    d = json.loads(p.stdout)
    allok = allok and d["matches_m7_outer_print"] and p.returncode == 0
    zs.append({"name": name, "A": d["A"], "w": d["w"], "est": d["estimate"], "n_centre": d["n_centre_good"], "noise": d["centre_noise"]})
zs.append({"name": "rpi5 #965 rtol 1e-13 (printed values only)", "A": 2.719236, "w": 1.000028, "est": 5.8e-6, "n_centre": 2, "noise": 0.021})
json.dump(zs, open(os.path.join(HERE, "logs", "zeros977.json"), "w"), indent=1)
with open(os.path.join(HERE, "logs", "pairs977.md"), "w", encoding="utf-8", newline="\n") as f:
    f.write("| zero | A | w/w_inf | estimate | centre solves | centre noise |\n|---|---|---|---|---|---|\n")
    for z in zs:
        f.write(f"| {z['name']} | {z['A']:.9f} | {z['w']:.9f} | {z['est']:.2e} | {z['n_centre']} | {z['noise']:.3f} |\n")
    f.write("\n")
sys.path.insert(0, HERE)
import pairs977, io, contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    pairs977.show(pairs977.pairs(zs))
open(os.path.join(HERE, "logs", "pairs977.md"), "a", encoding="utf-8", newline="\n").write(buf.getvalue())
print(open(os.path.join(HERE, "logs", "pairs977.md"), encoding="utf-8").read())
print("every zero matches m7_outer's print:", allok)
sys.exit(0 if allok else 1)

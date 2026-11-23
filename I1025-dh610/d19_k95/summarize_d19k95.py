#!/usr/bin/env python3
"""#1025 d19_k95 (dh610) summarize_d19k95.py [--mutate]: prints the result tables and the scorecard of the README from the files of this folder. No number is typed by hand.
Reads: in/l1kc87dh170d19.jsonl (dh170's k_c 87 record), l1kc95dh610d19.jsonl (this regrid's record), in/ref_winb_kc95_d19_regrid_summary.txt and in/ref_winb_kc87_d19_regrid_summary.txt (winb's),
regrid/steps.txt (wall, check exits), regrid/regrid_samples.csv (RSS), in_blobs_regrid.txt. The bars are the ones registered in the README before the run.
--mutate shifts the record's Delta by 1e-6 and scales its norm F by 1.4 before the scorecard: the Delta line must then flip to WRONG and the norm F line to right; the control fires (exit 1) when the verdicts differ
from the clean ones, and exits 3 when they do not. A clean run exits 0 whatever the verdicts."""
import json, re, sys, hashlib, subprocess

mutate = "--mutate" in sys.argv
R = lambda f: json.loads([l for l in open(f) if l.strip()][-1])
a, b = R("in/l1kc87dh170d19.jsonl"), R("l1kc95dh610d19.jsonl")
b_clean = b
if mutate:
    b = dict(b, Delta=b["Delta"] + 1e-6, F=b["F"] * 1.4)

def winb(f):
    t = open(f).read()
    m = re.search(r"wall (\d+) s.*?record: \|F\| (\S+), F_start (\S+), steps (\d+), constraint (\S+), Delta ([0-9.]+);", t, re.S)
    return dict(wall=int(m[1]), F=float(m[2]), F_start=float(m[3]), steps=int(m[4]), constraint=float(m[5]), Delta=float(m[6]))
w95, w87 = winb("in/ref_winb_kc95_d19_regrid_summary.txt"), winb("in/ref_winb_kc87_d19_regrid_summary.txt")

st = open("regrid/steps.txt").read()
wall = int(re.findall(r"regrid exit 0, wall (\d+) s", st)[-1])
end = re.findall(r"^(\S+ \S+) UTC regrid exit 0", st, re.M)[-1]
start = re.findall(r"^(\S+ \S+) UTC regrid starts", st, re.M)[-1]
ex = re.findall(r"kc95 syscheck exit (\d) \(0 wanted\); controls --mutate=F exit (\d), --mutate=steps exit (\d) \(1 wanted each\); kc87_syscheck on the k_c 95 result exit (\d) \(1 wanted\)", st)[-1]
ex = tuple(int(x) for x in ex)
rss = max(int(l.split(",")[1].split()[0]) for l in open("regrid/regrid_samples.csv") if l.strip() and not l.startswith("#"))

print(f"regrid {start} to {end} UTC, exit 0, wall {wall} s (the record's seconds {b['seconds']}); kc95 check exit {ex[0]}, controls --mutate=F {ex[1]}, --mutate=steps {ex[2]}, kc87 check on the result {ex[3]}; peak RSS (60 s samples) {rss / 1048576:.2f} GiB")
print()
print("| record | norm F | F_start | steps | constraint | Delta | seconds |")
print("|---|---|---|---|---|---|---|")
print(f"| dh170 k_c 87 (the source) | {a['F']:.12e} | {a['F_start']:.6e} | {a['steps']} | {a['constraint']:.6e} | {a['Delta']!r} | {a['seconds']} |")
print(f"| this regrid, k_c 95 | {b['F']:.12e} | {b['F_start']:.6e} | {b['steps']} | {b['constraint']:.6e} | {b['Delta']!r} | {b['seconds']} |")
print(f"| winb k_c 87 (Windows) | {w87['F']:.12e} | {w87['F_start']:.6e} | {w87['steps']} | {w87['constraint']:.6e} | {w87['Delta']!r} | {w87['wall']} |")
print(f"| winb k_c 95 (Windows) | {w95['F']:.12e} | {w95['F_start']:.6e} | {w95['steps']} | {w95['constraint']:.6e} | {w95['Delta']!r} | {w95['wall']} |")
print()
d_mine, d_winb = b["Delta"] - a["Delta"], w95["Delta"] - w87["Delta"]
print(f"Delta(k_c 95) - Delta(k_c 87): here {d_mine:+.4e} (dh170's k_c 87 source), winb {d_winb:+.4e}; Delta(k_c 95) here minus winb's k_c 95 {b['Delta'] - w95['Delta']:+.4e}")
print(f"steps ratio k_c 95 / k_c 87: here {b['steps'] / a['steps'] - 1:+.4%}, winb {w95['steps'] / w87['steps'] - 1:+.4%}; constraint here / winb's k_c 95: {b['constraint'] / w95['constraint'] - 1:+.4%}; F_start here / winb's {b['F_start'] / w95['F_start'] - 1:+.4%}")
print()
ok = lambda c: "right" if c else "WRONG"
rows = [("regrid exit 0 (93%)", True, "exit 0"),
        ("wall 3000 to 4500 s (65%)", 3000 <= wall <= 4500, f"{wall} s"),
        ("kc95 check accepts, controls 1 1 (90%)", ex[:3] == (0, 1, 1), f"exits {ex[0]} {ex[1]} {ex[2]}"),
        ("kc87 check refuses the result (97%)", ex[3] == 1, f"exit {ex[3]}"),
        ("steps 3575 +- 40 (65%)", abs(b["steps"] - 3575) <= 40, f"{b['steps']}"),
        ("Delta(95) - Delta(87) = -5.13e-7 +- 1.5e-7 (60%)", abs(d_mine + 5.13e-7) <= 1.5e-7, f"{d_mine:+.4e}"),
        ("norm F 3e-10 to 5e-10 (80%)", 3e-10 <= b["F"] <= 5e-10, f"{b['F']:.4e}"),
        ("constraint within 10% of winb's 1.39786e-4 (60%)", abs(b["constraint"] / 1.39786e-4 - 1) <= 0.10, f"{b['constraint']:.5e} ({b['constraint'] / 1.39786e-4 - 1:+.3%})"),
        ("lane ends 19:20 to 19:55 UTC", "19:20" <= end.split()[1][:5] <= "19:55", f"{end}")]
print("| prediction | result | verdict |")
print("|---|---|---|")
for n, c, r in rows:
    print(f"| {n} | {r} | {ok(c)} |")
if mutate:
    clean = (abs(b_clean["Delta"] - a["Delta"] + 5.13e-7) <= 1.5e-7, 3e-10 <= b_clean["F"] <= 5e-10)
    sys.exit(1 if (rows[5][1], rows[6][1]) != clean else 3)

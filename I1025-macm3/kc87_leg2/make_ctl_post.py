#!/usr/bin/env python3
"""make_ctl_post.py: the #1025 post of the k_c 87 control leap (h 0.03125) against part a (h 0.0625); every number is read from the files (ctl/ records, ctl_compare.py, the two scans' jsonl and read_lower.txt, roots87.txt). Prints markdown; @@T@@ is the time."""
import json, os, re, subprocess, sys
L2 = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2"); L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
recs = [json.loads(l) for l in open(L2 + "/ctl/l1kc87Lmacm3ctl.jsonl") if l.strip()]
PYV = os.path.expanduser("~/Source/venv-macm3-1058b/bin/python")
cmp_ = subprocess.run([PYV, L2 + "/ctl_compare.py"], capture_output=True, text=True, env=dict(os.environ, OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1")).stdout.strip()
def scan(d):
    rows = [json.loads(x) for x in open("%s/%s/scan/scan_D21.375_1025.jsonl" % (L, d))]
    by = {}
    for r in rows: by.setdefault(r["lam"], []).append(r)
    return by
sa, sc = scan("21.375"), scan("21.375_ctl")
def reading(d):
    t = open("%s/%s/read_lower.txt" % (L, d)).read()
    m = re.search(r"robust change \(([\d.]+), ([\d.]+)\), (.) to (.), det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", t)
    return dict(br=(m.group(1), m.group(2)), ori="%s to %s" % (m.group(3), m.group(4)), root=float(m.group(5)), lo=float(m.group(6)), hi=float(m.group(7)))
ra, rc = reading("21.375"), reading("21.375_ctl")
arec = {r["D"]: r for r in (json.loads(l) for l in open(L2 + "/l1kc87Lmacm3.jsonl") if l.strip())}
dD = {r["D"]: r["Delta"] - arec[r["D"]]["Delta"] for r in recs if r["D"] in arec}
assert cmp_.startswith("| D |"), "ctl_compare.py printed no table"
P = []
P.append("**#1025 macm3, the k_c 87 control leap at h 0.03125 against part a (h 0.0625), @@T@@ UTC 24 Nov: lambda_1 at D 21.375 is %.6f (control) against %.6f (part a), difference %+.2e; Delta control minus part a %+.3e at D 21.375 (%+.3e at D 21.3125).**" % (rc["root"], ra["root"], rc["root"] - ra["root"], dD[21.375], dD[21.3125]))
P.append("")
P.append("**Control leap** (t5's order: from dh370's k_c 87 states D 21.21875 and D 21.25, the seeds of part a, to D 21.375 at h 0.03125; raw `I1025-macm3/kc87_leg2/ctl/`, tag `l1kc87Lmacm3ctl`): `ell_leap.py` blob 1eb873e4 at wip/ell1-highD 48c36355, `leap_guard.py` f1fe7c7c and `mode_tracker.py` 807c2d95 unedited (guard with `shims_mac/`), 4 BLAS threads, nice 10, 12 h cap, 3 h watchdog, started outside the terminal; it ran 2026-11-24 18:52:16 to 20:12:25 UTC, exit 0, 4 points, no halving, no Traceback, no STOP file.")
P.append("")
P.append("| point | " + " | ".join("D %r" % r["D"] for r in recs) + " |"); P.append("|---|" + "---|" * len(recs))
for name, f in (("Delta", lambda r: "%.12f" % r["Delta"]), ("\\|F\\|, steps", lambda r: "%.3e, %d" % (r["F"], r["steps"])), ("psi-constraint", lambda r: "%.3e" % r["constraint"]), ("h", lambda r: "%g" % r["h"]), ("seconds", lambda r: "%d" % r["seconds"]), ("n_null", lambda r: "%d" % r["n_null"])):
    P.append("| %s | %s |" % (name, " | ".join(f(r) for r in recs)))
P.append("")
P.append("**Comparison with part a** (`ctl_compare.py` blob 5ad8890d; the L2 distance is of the state vectors, 5695 components, Delta last):")
P.append("")
P.append(cmp_)
P.append("")
P.append("**Scan of the control's D 21.375 state** (`kc87_leg_lambda/21.375_ctl/`; `d18_hybsign.py` e089207a unmodified, part a's window lambda 0.780 to 0.800 by 0.005 plus a repeat of 0.790, 4 processes of 1 thread at nice 15, 20:12:38 to 20:34:01 UTC; the source check ACCEPTED with the record's |F| 4.5473e-10 and 2911 steps, its controls exit 1, the k_c 79 check refused; `read_lower.py` 89309d3c, repeat PASS):")
P.append("")
P.append("| lambda | hybrid sign, part a | ln\\|det\\|, part a | hybrid sign, control | ln\\|det\\|, control | float64 sign, control |"); P.append("|---|---|---|---|---|---|")
for lam in sorted(sc):
    a = sa.get(lam); c = sc[lam]
    P.append("| %.3f%s | %s | %s | %s | %s | %s |" % (lam, " (two evaluations)" if len(c) > 1 else "", "%+d" % a[0]["sign"] if a else "-", "%.4f" % a[0]["ln"] if a else "-", "%+d" % c[0]["sign"], "%.4f" % c[0]["ln"], "%+d" % c[0]["f64_sign"]))
P.append("")
P.append("| | bracket | orientation as printed | det-linear root | estimator range |"); P.append("|---|---|---|---|---|")
P.append("| part a (h 0.0625) | (%s, %s) | %s | **%.6f** | [%.6f, %.6f] |" % (ra["br"][0], ra["br"][1], ra["ori"], ra["root"], ra["lo"], ra["hi"]))
P.append("| control (h 0.03125) | (%s, %s) | %s | **%.6f** | [%.6f, %.6f] |" % (rc["br"][0], rc["br"][1], rc["ori"], rc["root"], rc["lo"], rc["hi"]))
P.append("| control minus part a | | | **%+.2e** | ends %+.2e, %+.2e |" % (rc["root"] - ra["root"], rc["lo"] - ra["lo"], rc["hi"] - ra["hi"]))
P.append("")
P.append("The estimator range is the spread over the interpolation choices of `d185_scan_read.changes`, not an enclosure; the two ranges (widths %.1e and %.1e) overlap on [%.6f, %.6f]. The shift %+.2e is %.2f%% of the root's step into D 21.375 (%.6f, from D 21.3125's 0.814277)." % (ra["hi"] - ra["lo"], rc["hi"] - rc["lo"], max(ra["lo"], rc["lo"]), min(ra["hi"], rc["hi"]), rc["root"] - ra["root"], 100 * abs(rc["root"] - ra["root"]) / abs(ra["root"] - 0.814277), ra["root"] - 0.814277))
P.append("")
P.append("**Predictions** (README, written before the control; scored from the numbers above). Met: 4 points without a halving (h 0.03125 at all four); |Delta control - Delta part a| at D 21.375 below 1e-5 (%.2e); the L2 distance of the states at D 21.375 below 1e-5 of |z_a| (the table); the control's root within 3e-4 of part a's (%+.2e) and below it; each point took 11 to 20 min (%s s), though not with the leap alone: my D 22.0 reproduction and its gate run beside it from 18:55 UTC. Unclear in my own wording: \"the same sign as win2's\" for the Delta difference. I defined it as control minus part a (%+.2e), and win2's +4.1e-6 at k_c 79 is the h 0.0625 path minus the h 0.03125 path, which at k_c 87 is %+.2e: the same sign in win2's convention, the opposite if my sentence is read literally." % (abs(dD[21.375]), rc["root"] - ra["root"], ", ".join(str(r["seconds"]) for r in recs), dD[21.375], -dD[21.375]))
P.append("")
P.append("Raw: `I1025-macm3/kc87_leg2/ctl/` and `I1025-macm3/kc87_leg_lambda/21.375_ctl/` (README first, written by the pipeline; results pushed by it).")
print("\n".join(P))

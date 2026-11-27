#!/usr/bin/env python3
"""score_regrid_x.py [--write] [--plant] : scores the regrid of kc143_d23125x against the items of README.md (registered before the regrid), every number from the files: exits_kc143.txt, regrid/{regrid.log, regrid_samples.csv,
VERDICT.txt}, in/l1kc143macm3d23125x.jsonl, and the reference state kc143_d23125/in/l1kc143macm3d23125.jsonl. Prints the status entry; --write appends it to README.md.
--plant replaces the measured values by planted ones (wall 7000 s, peak RSS 9.8 GiB, Delta +5e-6 from the reference, lam_gauge +1e-7, steps 4708, constraint 7e-4, |F| 3e-10, accepted) and exits 1 unless the planted outcomes read as
written (every item HIT except the three on Delta and lam_gauge): a control that can fail. Tail sums are labeled arithmetic only, not a result."""
import csv, json, re, subprocess, sys
D = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125x/"
RF = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125/"
plant = "--plant" in sys.argv
ex = open(D + "exits_kc143.txt").read()
t_start = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125x: regrid starts", ex).group(1)
t_end, rexit, wall_ex = (lambda m: (m.group(1), int(m.group(2)), int(m.group(3))))(re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125x: regrid exit (\d+), wall (\d+) s", ex))
m = re.search(r"kc143 syscheck exit (\d+) \(0 wanted\); controls --mutate=F exit (\d+), --mutate=steps exit (\d+) \(1 wanted each\); kc135_syscheck on the k_c 143 result exit (\d+) \(1 wanted\)", ex)
sc_exit, cF, cS, c135 = [int(x) for x in m.groups()]
t_acc = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125x: kc143 syscheck", ex).group(1)
log = open(D + "regrid/regrid.log").read()
cw = int(re.search(r"capped_run: exit (\d+) wall (\d+) s cap_hit (\w+)", log).group(2)); cexit = int(re.search(r"capped_run: exit (\d+) wall", log).group(1)); caph = re.search(r"cap_hit (\w+)", log).group(1)
tb = len(re.findall(r"Traceback", log)); nw = len(re.findall(r"RuntimeWarning", log)); nerr = len(re.findall(r"(?:ValueError|MemoryError|IndexError|OverflowError|array.*limit)", log))
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()][-1]
rec = rd(D + "in/l1kc143macm3d23125x.jsonl"); ref = rd(RF + "in/l1kc143macm3d23125.jsonl"); src = rd(D + "in/l1kc127Lmacm3.jsonl")
verdict = open(D + "regrid/VERDICT.txt").read().split()[0]
rows = [r for r in csv.DictReader(open(D + "regrid/regrid_samples.csv")) if r["rss_kB"]]
peak = max(int(r["rss_kB"]) for r in rows) / 1048576; lowav = min(float(r["avail_GiB"]) for r in rows); pcpu = sum(float(r["pcpu"]) for r in rows) / len(rows)
wall = cw; Dl, lg, F, steps, cons = rec["Delta"], rec["lam_gauge"], rec["F"], rec["steps"], rec["constraint"]; acc = (rexit == 0 and sc_exit == 0 and cF == 1 and cS == 1 and c135 == 1 and verdict == "ACCEPTED")
if plant: wall, peak, Dl, lg, steps, cons, F, acc, tb, nerr, cexit, caph, lowav = 7000, 9.8, ref["Delta"] + 5e-6, ref["lam_gauge"] + 1e-7, 4708, 7e-4, 3e-10, True, 0, 0, 0, "False", 9.0
dD = Dl - ref["Delta"]; dG = lg - ref["lam_gauge"]
L = []
def item(name, pct, hit, val): L.append((name, pct, hit, val))
item("accepted by the k_c 143 check (exit 0, controls 1 1, the k_c 135 check refuses the result)", 88, acc, "syscheck exit %d, controls %d %d, kc135 check on the result exit %d, VERDICT %s (%s UTC)" % (sc_exit, cF, cS, c135, verdict, t_acc))
item("no exception, no array limit", 88, tb == 0 and nerr == 0 and cexit == 0 and caph == "False", "capped_run exit %d, cap_hit %s, %d tracebacks, %d error lines, %d numpy RuntimeWarnings (the k_c 135 to 143 regrid: 30)" % (cexit, caph, tb, nerr, nw))
item("|F| below 5e-10", 90, F < 5e-10, "%.4e (the reference %.4e)" % (F, ref["F"]))
item("steps 4708 +- 5", 60, abs(steps - 4708) <= 5, "%d (%+d)" % (steps, steps - 4708))
item("steps within 30 of 4708", 80, abs(steps - 4708) <= 30, "%d" % steps)
item("psi-constraint in (5.9e-4, 8.0e-4)", 60, 5.9e-4 < cons < 8.0e-4, "%.4e (the reference %.4e, ratio %.4f)" % (cons, ref["constraint"], cons / ref["constraint"]))
item("psi-constraint below 1e-2", 99, cons < 1e-2, "%.4e" % cons)
item("Delta within 1e-6 of 1.178015433613 (t5's bar: the same state)", 60, abs(dD) <= 1e-6, "%.12f, difference %+.3e" % (Dl, dD))
item("Delta within 4e-7 of 1.178015433613", 35, abs(dD) <= 4e-7, "difference %+.3e" % dD)
item("lam_gauge within 5e-8 of 0.985365101148", 50, abs(dG) <= 5e-8, "%.12f, difference %+.3e (k_c 135 -> 143 in kc143_d23125: +1.769e-07)" % (lg, dG))
item("wall in (5600, 8200) s", 60, 5600 < wall < 8200, "%d s (capped_run; the exit line %d s; %s to %s UTC)" % (wall, wall_ex, t_start, t_end))
item("wall above 5856 s (the k_c 135 to 143 regrid)", 70, wall > 5856, "%d s" % wall)
item("peak RSS in (9.0, 10.4) GiB", 65, 9.0 < peak < 10.4, "%.3f GiB (60 s samples, %d of them)" % (peak, len(rows)))
item("peak RSS below 11 GiB", 90, peak < 11.0, "%.3f GiB" % peak)
item("no memory alert (available below 2 GiB)", 92, lowav >= 2.0, "lowest available %.1f GiB" % lowav)
H = [i for i in L if i[2]]; M = [i for i in L if not i[2]]
if plant:
    want_miss = {"Delta within 1e-6 of 1.178015433613 (t5's bar: the same state)", "Delta within 4e-7 of 1.178015433613", "lam_gauge within 5e-8 of 0.985365101148"}
    ok = {i[0] for i in M} == want_miss
    print("planted control: HIT %d, MISS %d; the misses are the three Delta and lam_gauge items: %s" % (len(H), len(M), ok)); sys.exit(0 if ok else 1)
fmt = lambda i: "%s (%d%%): %s" % (i[0], i[1], i[3])
out = ["**the regrid, scored** (exits_kc143.txt, regrid/, in/*.jsonl, from the files by command: `score_regrid_x.py`, whose control `--plant` replaces the measured values by planted ones and must read three MISS): ACCEPTED %s UTC, regrid %s to %s UTC, exit %d, capped_run wall %d s. Record: |F| %.4e, F_start %.3e, steps %d (source k_c 127 %d), psi-constraint %.4e (source %.4e), Delta %.12f (source %.12f; the reference %.12f), lam_gauge %.12f (the reference %.12f). Peak RSS %.3f GiB, lowest available %.1f GiB, mean CPU %.1f%% of one core over %d samples."
       % (t_acc, t_start, t_end, rexit, cw, rec["F"], rec["F_start"], rec["steps"], src["steps"], rec["constraint"], src["constraint"], rec["Delta"], src["Delta"], ref["Delta"], rec["lam_gauge"], ref["lam_gauge"], peak, lowav, pcpu, len(rows))]
out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + "; ".join("MISS " + fmt(i) for i in M) + ". (%d items: %d HIT, %d MISS.)" % (len(L), len(H), len(M)))
out.append("**Against the reference state (t5's order; arithmetic only, not a result beyond his bar):** Delta difference %+.3e (his bar 1e-6: %s; %.2f times R0's 4.2e-7), lam_gauge difference %+.3e, |F| %.4e against %.4e, steps %d against %d (%+d), psi-constraint %.4e against %.4e (ratio %.4f), ell_refine seconds %s against %s, wall %d s against 5856 s (the k_c 135 to 143 regrid), peak RSS %.3f against 9.392 GiB." % (
    dD, "a DIFFERENT STATE" if abs(dD) > 1e-6 else "the same state", abs(dD) / 4.2e-7, dG, F, ref["F"], steps, ref["steps"], steps - ref["steps"], cons, ref["constraint"], cons / ref["constraint"], rec.get("seconds"), ref.get("seconds"), wall, peak))
txt = "\n".join(out); print(txt)
if "--write" in sys.argv:
    stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
    open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " "))); print("written")

#!/usr/bin/env python3
"""score_regrid_r1.py [--write] [--plant] : scores the kappa 0.5 regrid of I1101-macm3 (R1) against the items of README.md (the registration, written before the regrid) and t5's bars (|F| <= 5e-10, steps 5851 +- 2%),
every number from the files: exits_r1.txt, regrid/{regrid.log, regrid_samples.csv, VERDICT.txt, bars.txt}, in/l1kc127k050m3.jsonl and the source record in/l1kc127wind23.jsonl (winb's kappa 0.7 state). Prints the status entry; --write appends it to README.md.
--plant replaces the measured values by planted ones (wall 9000 s, peak RSS 9.0 GiB, Delta shift 2e-5 from the source, steps 5851, |F| 3e-10, constraint 1e-3, accepted) and exits 1 unless exactly the three items on wall, RSS and Delta read MISS: a control that can fail.
Tail sums are labeled arithmetic only, not a result."""
import csv, json, re, subprocess, sys
D = "/Users/nathan/Source/choptuik-large-d-raw-903/I1101-macm3/"
plant = "--plant" in sys.argv
ex = open(D + "exits_r1.txt").read()
U = r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC I1101 R1: "
t_start = re.search(U + "regrid starts", ex).group(1)
t_end, rexit, wall_ex = (lambda m: (m.group(1), int(m.group(2)), int(m.group(3))))(re.search(U + r"regrid exit (\d+), wall (\d+) s", ex))
m = re.search(U + r"kc127 syscheck exit (\d+) \(0 wanted\); controls --mutate=F exit (\d+), --mutate=steps exit (\d+) \(1 wanted each\); kc135_syscheck on the result exit (\d+), kc143_syscheck on the result exit (\d+) \(1 wanted each\)", ex)
t_acc = m.group(1); sc_exit, cF, cS, c135, c143 = [int(x) for x in m.groups()[1:]]
log = open(D + "regrid/regrid.log").read()
cw = int(re.search(r"capped_run: exit (\d+) wall (\d+) s cap_hit (\w+)", log).group(2)); cexit = int(re.search(r"capped_run: exit (\d+) wall", log).group(1)); caph = re.search(r"cap_hit (\w+)", log).group(1)
tb = len(re.findall(r"Traceback", log)); nw = len(re.findall(r"RuntimeWarning", log)); nerr = len(re.findall(r"(?:ValueError|MemoryError|IndexError|OverflowError|array.*limit)", log))
rd = lambda p: [json.loads(l) for l in open(p) if l.strip()][-1]
rec = rd(D + "in/l1kc127k050m3.jsonl"); src = rd(D + "in/l1kc127wind23.jsonl")
verdict = open(D + "regrid/VERDICT.txt").read().split()[0]
rows = [r for r in csv.DictReader(open(D + "regrid/regrid_samples.csv")) if r["rss_kB"]]
peak = max(int(r["rss_kB"]) for r in rows) / 1048576; lowav = min(float(r["avail_GiB"]) for r in rows); pcpu = sum(float(r["pcpu"]) for r in rows) / len(rows)
wall = cw; Dl, F, steps, cons = rec["Delta"], rec["F"], rec["steps"], rec["constraint"]; acc = (rexit == 0 and sc_exit == 0 and cF == 1 and cS == 1 and c135 == 1 and c143 == 1 and verdict == "ACCEPTED")
if plant: wall, peak, Dl, steps, cons, F, acc, tb, nerr, cexit, caph, lowav = 9000, 9.0, src["Delta"] + 2e-5, 5851, 1e-3, 3e-10, True, 0, 0, 0, "False", 9.0
dD = Dl - src["Delta"]
L = []
def item(name, pct, hit, val): L.append((name, pct, hit, val))
item("accepted by the k_c 127 check (exit 0, controls 1 1, the k_c 135 and k_c 143 checks refuse the result)", 92, acc, "syscheck exit %d, controls %d %d, kc135 and kc143 checks on the result exit %d %d, VERDICT %s (%s UTC)" % (sc_exit, cF, cS, c135, c143, verdict, t_acc))
item("no exception, no array limit", 90, tb == 0 and nerr == 0 and cexit == 0 and caph == "False", "capped_run exit %d, cap_hit %s, %d tracebacks, %d error lines, %d numpy RuntimeWarnings" % (cexit, caph, tb, nerr, nw))
item("|F| <= 5e-10 (t5's bar)", 92, F <= 5e-10, "%.4e (the source %.4e)" % (F, src["F"]))
item("steps in 5851 +- 2%, 5734 to 5968 (t5's bar)", 60, 5851 * 0.98 <= steps <= 5851 * 1.02, "%d (%+.2f%% from 5851; the source %d at kappa 0.7)" % (steps, 100.0 * (steps / 5851.0 - 1), src["steps"]))
item("steps within 5% of 5851", 85, abs(steps / 5851.0 - 1) <= 0.05, "%d" % steps)
item("psi-constraint below 1e-2", 99, cons < 1e-2, "%.4e (the source %.4e)" % (cons, src["constraint"]))
item("|Delta - 1.174322923416| below 1e-5", 85, abs(dD) < 1e-5, "Delta %.12f, difference %+.3e" % (Dl, dD))
item("wall in (2700, 4800) s", 60, 2700 < wall < 4800, "%d s (capped_run; the exit line %d s; %s to %s UTC)" % (wall, wall_ex, t_start, t_end))
item("peak RSS in (5.5, 7.5) GiB", 60, 5.5 < peak < 7.5, "%.3f GiB (60 s samples, %d of them)" % (peak, len(rows)))
item("no memory alert (available below 2 GiB)", 92, lowav >= 2.0, "lowest available %.1f GiB" % lowav)
H = [i for i in L if i[2]]; M = [i for i in L if not i[2]]
if plant:
    want_miss = {"wall in (2700, 4800) s", "peak RSS in (5.5, 7.5) GiB", "|Delta - 1.174322923416| below 1e-5"}
    ok = {i[0] for i in M} == want_miss
    print("planted control: HIT %d, MISS %d; the misses are the wall, RSS and Delta items: %s" % (len(H), len(M), ok)); sys.exit(0 if ok else 1)
fmt = lambda i: "%s (%d%%): %s" % (i[0], i[1], i[3])
out = ["**the R1 regrid, scored** (exits_r1.txt, regrid/, in/*.jsonl, from the files by command: `score_regrid_r1.py`, whose control `--plant` replaces the measured values by planted ones and must read three MISS): %s %s UTC, regrid %s to %s UTC, exit %d, capped_run wall %d s. Record at kappa 0.5: |F| %.4e, F_start %.3e, steps %d (winb's kappa 0.7 source %d), psi-constraint %.4e (source %.4e), Delta %.12f (source %.12f), lam_gauge %.12f (source %.12f). Peak RSS %.3f GiB, lowest available %.1f GiB, mean CPU %.1f%% of one core over %d samples."
       % (verdict, t_acc, t_start, t_end, rexit, cw, rec["F"], rec["F_start"], rec["steps"], src["steps"], rec["constraint"], src["constraint"], rec["Delta"], src["Delta"], rec["lam_gauge"], src["lam_gauge"], peak, lowav, pcpu, len(rows))]
out.append("Scoring, HIT = the registered event occurred: " + "; ".join("HIT " + fmt(i) for i in H) + ". " + ("; ".join("MISS " + fmt(i) for i in M) + ". " if M else "") + "(%d items: %d HIT, %d MISS.)" % (len(L), len(H), len(M)))
out.append("**Against the source (arithmetic only, not a result):** Delta shift %+.3e, lam_gauge shift %+.3e, steps ratio %.4f (kappa ratio 0.7/0.5 = 1.4000), psi-constraint ratio %.4f, ell_refine seconds %s against %s." % (dD, rec["lam_gauge"] - src["lam_gauge"], steps / float(src["steps"]), cons / src["constraint"], rec.get("seconds"), src.get("seconds")))
txt = "\n".join(out); print(txt)
if "--write" in sys.argv:
    stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
    open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " "))); print("written")

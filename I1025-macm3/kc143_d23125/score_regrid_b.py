#!/usr/bin/env python3
"""score_regrid_b.py [--write] [--mutate=wall|shift] : scores the regrid of kc143_d23125 against the items of BOTH registration entries of README.md
(the first, 2026-11-27 01:50 UTC, and the second, 05:42 UTC), every number from the files: exits_kc143.txt, regrid/{regrid_summary.txt, regrid.log, regrid_samples.csv, syscheck*.txt, VERDICT.txt},
in/l1kc143macm3d23125.jsonl, in/l1kc135macm3d23125.jsonl. Each item is scored as registered, so an item in both entries is scored twice.
Prints the Status entry; --write appends it to README.md. Controls: --mutate=wall (wall minus 1000 s: both wall items must flip to HIT), --mutate=shift (shift plus 4.0e-6: the first entry's shift item must flip to HIT).
Tail sums are labeled arithmetic only, not a result. Read-only except for --write."""
import csv, json, re, subprocess, sys
D = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d23125/"
mut = [a for a in sys.argv if a.startswith("--mutate=")]
mut = mut[0].split("=")[1] if mut else ""
ex = open(D + "exits_kc143.txt").read()
m = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: regrid starts", ex); t_start = m.group(1)
m = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: regrid exit (\d+), wall (\d+) s", ex); t_end, rexit, wall_ex = m.group(1), int(m.group(2)), int(m.group(3))
m = re.search(r"kc143 syscheck exit (\d+) \(0 wanted\); controls --mutate=F exit (\d+), --mutate=steps exit (\d+) \(1 wanted each\); kc135_syscheck on the k_c 143 result exit (\d+) \(1 wanted\)", ex)
sc_exit, cF, cS, c135 = [int(x) for x in m.groups()]
t_acc = re.search(r"== \d{4}-\d\d-\d\d (\d\d:\d\d:\d\d) UTC kc143_d23125: kc143 syscheck", ex).group(1)
log = open(D + "regrid/regrid.log").read()
cw = int(re.search(r"capped_run: exit (\d+) wall (\d+) s cap_hit (\w+)", log).group(2)); cexit = int(re.search(r"capped_run: exit (\d+) wall", log).group(1)); caph = re.search(r"cap_hit (\w+)", log).group(1)
tb = len(re.findall(r"Traceback", log)); nw = len(re.findall(r"RuntimeWarning", log)); nerr = len(re.findall(r"(?:ValueError|MemoryError|IndexError|OverflowError|array.*limit)", log))
rec = [json.loads(l) for l in open(D + "in/l1kc143macm3d23125.jsonl") if l.strip()][-1]
src = [json.loads(l) for l in open(D + "in/l1kc135macm3d23125.jsonl") if l.strip()][-1]
shift = rec["Delta"] - src["Delta"]; sr = rec["steps"] / src["steps"]; cr = rec["constraint"] / src["constraint"]
wall = cw
if mut == "wall": wall -= 1000
if mut == "shift": shift += 4.0e-6
rows = [r for r in csv.DictReader(open(D + "regrid/regrid_samples.csv")) if r["rss_kB"]]
peak = max(int(r["rss_kB"]) for r in rows) / 1048576; lowav = min(float(r["avail_GiB"]) for r in rows); pcpu = sum(float(r["pcpu"]) for r in rows) / len(rows)
# the same rung at D 23.0625 (lane A), for the comparison (arithmetic only)
A = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/kc143_d230625/"
wallA = int(re.search(r"regrid exit 0, wall (\d+) s", open(A + "exits_kc143.txt").read()).group(1))
peakA = max(int(r["rss_kB"]) for r in csv.DictReader(open(A + "regrid/regrid_samples.csv")) if r["rss_kB"]) / 1048576
recA = [json.loads(l) for l in open(A + "in/l1kc143macm3d230625.jsonl") if l.strip()][-1]; shiftA = recA["Delta"] - recA["Delta_src"]
verdict = open(D + "regrid/VERDICT.txt").read().split()[0]
F = rec["F"]
L = []
def item(entry, name, pct, hit, val): L.append((entry, name, pct, hit, val))
acc = (rexit == 0 and sc_exit == 0 and cF == 1 and cS == 1 and c135 == 1 and verdict == "ACCEPTED")
item("1+2", "accepted by the k_c 143 check (exit 0, controls 1 1, the k_c 135 check refuses)", 90, acc, "syscheck exit %d, controls %d %d, kc135 check on the result exit %d, VERDICT %s (%s UTC)" % (sc_exit, cF, cS, c135, verdict, t_acc))
item("1", "no exception, no array limit", 88, tb == 0 and nerr == 0 and cexit == 0 and caph == "False", "capped_run exit %d, cap_hit %s, %d tracebacks, %d error lines, %d numpy RuntimeWarnings (lane A: 16; the k_c 135 logs 14 and 17)" % (cexit, caph, tb, nerr, nw))
item("2", "no exception, no array limit", 90, tb == 0 and nerr == 0 and cexit == 0 and caph == "False", "same")
item("1", "Delta shift in (-6.0e-6, -0.6e-6)", 70, -6.0e-6 < shift < -0.6e-6, "%+.4e (%s the lower end by %.3e)" % (shift, "below" if shift < -6.0e-6 else "inside", abs(shift + 6.0e-6)))
item("2", "Delta shift in (-9.0e-6, -3.5e-6)", 70, -9.0e-6 < shift < -3.5e-6, "%+.4e (central -6.04e-6)" % shift)
item("1", "Delta shift negative", 88, shift < 0, "%+.4e" % shift)
item("2", "Delta shift negative", 90, shift < 0, "%+.4e" % shift)
item("1", "steps ratio in (1.052, 1.066)", 70, 1.052 < sr < 1.066, "%d/%d = %.4f" % (rec["steps"], src["steps"], sr))
item("2", "steps ratio in (1.050, 1.068)", 70, 1.050 < sr < 1.068, "%.4f" % sr)
item("1", "steps within 30 of 4707", 50, abs(rec["steps"] - 4707) <= 30, "%d (%+d)" % (rec["steps"], rec["steps"] - 4707))
item("2", "steps within 30 of 4709", 50, abs(rec["steps"] - 4709) <= 30, "%d (%+d)" % (rec["steps"], rec["steps"] - 4709))
item("1", "psi-constraint in (6.6e-4, 8.5e-4)", 65, 6.6e-4 < rec["constraint"] < 8.5e-4, "%.4e (ratio %.4f)" % (rec["constraint"], cr))
item("2", "psi-constraint in (6.0e-4, 7.9e-4)", 65, 6.0e-4 < rec["constraint"] < 7.9e-4, "%.4e (ratio %.4f)" % (rec["constraint"], cr))
item("1+2", "psi-constraint below 1e-2", 99, rec["constraint"] < 1e-2, "%.4e" % rec["constraint"])
item("1+2", "|F| below 5e-10", 90, F < 5e-10, "%.4e (source %.4e)" % (F, src["F"]))
item("1", "wall 3900 to 5600 s", 60, 3900 <= wall <= 5600, "%d s (capped_run; the exit line %d s; %s to %s UTC)" % (wall, wall_ex, t_start, t_end))
item("2", "wall 4000 to 5000 s", 60, 4000 <= wall <= 5000, "%d s" % wall)
item("1", "peak RSS in (6.5, 9.0) GiB", 65, 6.5 < peak < 9.0, "%.3f GiB (60 s samples, %d of them)" % (peak, len(rows)))
item("2", "peak RSS in (7.2, 9.0) GiB", 65, 7.2 < peak < 9.0, "%.3f GiB" % peak)
item("1", "peak RSS below 11 GiB", 92, peak < 11.0, "%.3f GiB" % peak)
item("2", "peak RSS below 10 GiB", 92, peak < 10.0, "%.3f GiB" % peak)
item("1+2", "no memory alert (available below 2 GiB) with the chain held", 90, lowav >= 2.0, "lowest available %.1f GiB" % lowav)
out = []
out.append("**the regrid, scored** (exits_kc143.txt, regrid/, in/*.jsonl, from the files by command: `score_regrid_b.py`, controls `--mutate=wall` (wall minus 1000 s: both wall items must flip to HIT) and `--mutate=shift` (shift plus 4e-6: the first entry's shift item must flip to HIT)): ACCEPTED %s UTC, regrid %s to %s UTC, exit %d, capped_run wall %d s (the lane's hc line says 5867 s: its figure runs to the hc call, checks and push included). Record: |F| %.4e (source %.4e), F_start %.3e, steps %d (source %d, ratio %.4f), psi-constraint %.4e (source %.4e, ratio %.4f), Delta %.12f (source %.12f), shift %+.4e. Peak RSS %.3f GiB, lowest available memory %.1f GiB, mean CPU %.1f%% of one core over the %d samples."
           % (t_acc, t_start, t_end, rexit, cw, F, src["F"], rec.get("F_start", float("nan")), rec["steps"], src["steps"], sr, rec["constraint"], src["constraint"], cr, rec["Delta"], src["Delta"], shift, peak, lowav, pcpu, len(rows)))
H = [i for i in L if i[3]]; M = [i for i in L if not i[3]]
fmt = lambda i: "%s%s [entry %s]: %s" % (i[1], " (%d%%)" % i[2], i[0], i[4])
out.append("Scoring, HIT = the registered event occurred (entry 1 = the first registration, entry 2 = the second; an item in both is scored twice, shown as 1+2 when the same text): " + "; ".join("HIT " + fmt(i) for i in H) + ". " + "; ".join("MISS " + fmt(i) for i in M) + ". (%d items: %d HIT, %d MISS.)" % (len(L), len(H), len(M)))
R = "/Users/nathan/Source/choptuik-large-d-raw-903/I1025-macm3/"
def rg(folder, exits):
    w = int(re.search(r"regrid exit 0, wall (\d+) s", open(R + folder + "/" + exits).read()).group(1))
    p = max(int(r["rss_kB"]) for r in csv.DictReader(open(R + folder + "/regrid/regrid_samples.csv")) if r["rss_kB"]) / 1048576
    return w, p
w135a, p135a = rg("kc135_d230625", "exits_kc135.txt"); w135b, p135b = rg("kc135_d23125", "exits_kc135.txt")
sh135b = [json.loads(l) for l in open(R + "kc135_d23125/in/l1kc135macm3d23125.jsonl") if l.strip()][-1]; sh135b = sh135b["Delta"] - sh135b["Delta_src"]
out.append("**The misses.** The wall, %d s, is above both registered ranges (3900 to 5600 and 4000 to 5000 s). Arithmetic only, not a result: the same rung at D 23.0625 took %d s, so this regrid took %.3f times as long; the k_c 135 regrids took %d s at D 23.0625 and %d s at D 23.125 (ratio %.3f), so k_c 143 over k_c 135 is %.3f at D 23.125 against %.3f at D 23.0625; both k_c 143 regrids ran one core at about 100%% CPU (mean %.1f%%). The peak RSS, %.3f GiB, is above the upper end 9.0 of both ranges (lane A: %.3f GiB; k_c 135 regrids %.3f GiB at D 23.0625 and %.3f at D 23.125, so k_c 143 over k_c 135 is %.4f at D 23.125 against %.4f at D 23.0625). The Delta shift %+.4e lies %.3e below the first entry's lower end -6.0e-6 and inside the second entry's range, which was set from lane A's shift (%+.4e); the shift is %.3f times the k_c 135 shift at D 23.125 (%+.4e). Not explained."
           % (cw, wallA, cw / wallA, w135a, w135b, w135b / w135a, cw / w135b, wallA / w135a, pcpu, peak, peakA, p135a, p135b, peak / p135b, peakA / p135a, shift, abs(shift + 6.0e-6), shiftA, shift / sh135b, sh135b))
txt = "\n".join(out)
print(txt)
if "--write" in sys.argv and not mut:
    stamp = subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M UTC"]).decode().strip()
    open(D + "README.md", "a").write("- %s: %s\n" % (stamp, txt.replace("\n", " ")))
    print("written")

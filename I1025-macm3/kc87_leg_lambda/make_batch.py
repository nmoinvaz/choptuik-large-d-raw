#!/usr/bin/env python3
"""make_batch.py D1,D2,D3 [--part=b] [--leg=L1,L2,...] [--pred="D1=text;D2=text;D3=text"] [--note="..."] > post.md
One #1025 comment for several scanned points (t5, 24 Nov: one comment per 3 scanned points with all tables): a summary table of the roots and residuals, the leg rows of all points accepted since the last post (one table),
then each point's full section from make_post.py (headline, source, scan, reader and repeat, reading tables, residuals, local slope and track, time and memory, predictions). @@T@@ in the first line is replaced by the caller. Read-only."""
import os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
Ds = [float(x) for x in args[0].split(",")]
def part_of(D):   # the leg part that holds the point: a to D 21.5, b to D 21.96875 (part b stopped there), b2 to D 22.5, c after
    return "a" if D <= 21.5 + 1e-9 else "b" if D <= 21.96875 + 1e-9 else "b2" if D <= 22.5 + 1e-9 else "c"
part = opt.get("--part", "auto")
preds = dict(x.split("=", 1) for x in opt.get("--pred", "").split(";") if "=" in x)
def run(extra):
    return subprocess.run([sys.executable, HERE + "/make_post.py"] + extra, capture_output=True, text=True, check=True).stdout
roots = {}
for l in open(HERE + "/roots87.txt"):
    f = l.split()
    if len(f) >= 2 and not l.startswith("#"): roots[float(f[0])] = float(f[1])
secs = []; rows = []
for D in Ds:
    t = run([repr(D), "--part=" + (part_of(D) if part == "auto" else part), "--skip-leg", "--pred=" + preds.get(repr(D), "(not scored)")])
    h = t.split("\n\n")[0]
    m = re.search(r"det-linear ([\d.-]+) \(estimator range \[([\d.-]+), ([\d.-]+)\]\); (.*?) predicted ([\d.-]+): ([+-][\d.]+); the -0\.33 rule beside it, ([\d.-]+): ([+-][\d.]+)(, outside its 0.005 window)?; local slope ([\d.-]+)", h)
    br = re.search(r"between ([\d.-]+) and ([\d.-]+) \(([^)]*)\)", h)
    rows.append((D, m, br))
    secs.append("### D %r\n\n%s" % (D, t.replace(" (@@T@@ UTC 24 Nov)", "")))
head = "**#1025 macm3, lambda_1 on my own k_c 87 leg, D %s (@@T@@ UTC 24 Nov): %d scanned points in one comment (t5's order).**" % (", ".join(repr(d) for d in Ds), len(Ds))
print(head)
print("\n| D | bracket | det-linear root | primary rule: prediction, residual | -0.33 rule: prediction, residual | local slope |\n|---|---|---|---|---|---|")
for D, m, br in rows:
    print("| %r | (%s, %s) | **%s** | %s, %s | %s, %s%s | %s |" % (D, br.group(1), br.group(2), m.group(1), m.group(5), m.group(6), m.group(7), m.group(8), " (outside 0.005)" if m.group(9) else "", m.group(10)))
if opt.get("--leg"):
    legs = [float(x) for x in opt["--leg"].split(",") if x]
    for pt in dict.fromkeys(part_of(d) if part == "auto" else part for d in legs):   # one leg table per part, in order
        sub = [d for d in legs if (part_of(d) if part == "auto" else part) == pt]
        print()
        print(run(["%r" % Ds[0], "--part=" + pt, "--leg=" + ",".join(repr(d) for d in sub), "--only-leg", "--pred=x"]))
if "--note" in opt: print("\n" + opt["--note"])
print("\nEach point below carries its own tables.\n")
print("\n\n".join(secs))

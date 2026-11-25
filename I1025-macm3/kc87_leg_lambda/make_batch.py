#!/usr/bin/env python3
"""make_batch.py D1,D2,D3 [--part=b] [--leg=L1,L2,...] [--pred="D1=text;D2=text;D3=text"] [--note="..."] > post.md
One #1025 comment for several scanned points (t5, 24 Nov: one comment per 3 scanned points with all tables): a summary table of the roots and residuals, the leg rows of all points accepted since the last post (one table),
then each point's full section from make_post.py (headline, source, scan, reader and repeat, reading tables, residuals, local slope and track, time and memory, predictions). @@T@@ in the first line is replaced by the caller. Read-only."""
import json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
opt = {a.split("=", 1)[0]: a.split("=", 1)[1] for a in sys.argv[1:] if a.startswith("--") and "=" in a}
Ds = [float(x) for x in args[0].split(",")]
def part_of(D):   # the leg part that holds the point: the one whose pushed_points.txt lists it (a: kc87_leg2/, b, b2, c, c2: their folders)
    L2_ = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2")
    for pt, fol in (("c2", "/c2"), ("c", "/c"), ("b2", "/b2"), ("b", "/b"), ("a", "")):
        f = L2_ + fol + "/pushed_points.txt"
        if os.path.exists(f) and any(abs(float(x) - D) < 1e-9 for x in open(f).read().split()): return pt
    raise SystemExit("D %r is in no part's pushed_points.txt" % D)
part = opt.get("--part", "auto")
preds = dict(x.split("=", 1) for x in opt.get("--pred", "").split(";") if "=" in x)
prevs = dict(x.split("=", 1) for x in opt.get("--prev", "").split(";") if "=" in x)       # --prev="D=PD,PR,LO,HI,CD;...": the registered rule base of a point started by hand (make_post.py --prev)
rescans = dict(x.split("=", 1) for x in opt.get("--rescan", "").split(";") if "=" in x)    # --rescan="D=FOLDER": a rescan of that point's state, appended under its section
import json
def rescan_block(D, folder):
    L = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
    rows = [json.loads(x) for x in open("%s/%s/scan/scan_D%s_1025.jsonl" % (L, folder, D))]
    rd = open("%s/%s/read_lower.txt" % (L, folder)).read()
    mm = re.search(r"robust change \(([\d.-]+), ([\d.-]+)\), ([-+] to [-+]), det-linear ([\d.-]+), range \[([\d.-]+), ([\d.-]+)\]", rd)
    by = {}
    for r in rows: by.setdefault(round(r["lam"], 4), []).append(r)
    lines = ["**Rescan of D %s** (`kc87_leg_lambda/%s/`, same state and record, t5's order): lambda %s, hybrid signs as printed, one robust change between the positions below (read_lower prints three decimals; positions from the jsonl).\n" % (D, folder, ", ".join("%g" % x for x in sorted(by))),
             "| lambda | hybrid sign | ln\\|det\\| | float64 sign |", "|---|---|---|---|"]
    for lam in sorted(by):
        r = by[lam][0]
        lines.append("| %g%s | %+d | %.4f | %+d |" % (lam, " (two evaluations)" if len(by[lam]) > 1 else "", r["sign"], r["ln"], r["f64_sign"]))
    ks = sorted(by); ch = [(a, b) for a, b in zip(ks, ks[1:]) if by[a][0]["sign"] != by[b][0]["sign"]]
    lines.append("\nPosition of the change: between %s (%s); det-linear **%s**, estimator range [%s, %s] (a spread over interpolation choices, not an enclosure); repeat %s; %d of %d noise-robust." % (
        " and ".join("%g" % x for x in ch[0]), mm.group(3), mm.group(4), mm.group(5), mm.group(6), "PASS" if "-> PASS" in rd else "FAIL", sum(r["noise_robust"] for r in rows), len(rows)))
    return "\n".join(lines)
def run(extra):
    return subprocess.run([sys.executable, HERE + "/make_post.py"] + extra, capture_output=True, text=True, check=True).stdout
roots = {}
for l in open(HERE + "/roots87.txt"):
    f = l.split()
    if len(f) >= 2 and not l.startswith("#"): roots[float(f[0])] = float(f[1])
secs = []; rows = []
for D in Ds:
    t = run([repr(D), "--part=" + (part_of(D) if part == "auto" else part), "--skip-leg", "--pred=" + preds.get(repr(D), "(not scored)")] + (["--prev=" + prevs[repr(D)]] if repr(D) in prevs else []))
    if repr(D) in rescans: t = t + "\n\n" + rescan_block(D, rescans[repr(D)])
    h = t.split("\n\n")[0]
    m = re.search(r"det-linear ([\d.-]+) \(estimator range \[([\d.-]+), ([\d.-]+)\]\); (.*?) predicted ([\d.-]+): ([+-][\d.]+); the -0\.33 rule beside it, ([\d.-]+): ([+-][\d.]+)(, outside its 0.005 window)?; local slope ([\d.-]+)", h)
    br = re.search(r"between ([\d.-]+) and ([\d.-]+) \(([^)]*)\)", h)
    rows.append((D, m, br))
    secs.append("### D %r\n\n%s" % (D, t.replace(" (@@T@@ UTC 24 Nov)", "")))
head = "**#1025 macm3, lambda_1 on my own k_c 87 leg, D %s (@@T@@ UTC 24 Nov): %d scanned points in one comment (t5's order).**" % (", ".join(repr(d) for d in Ds), len(Ds))
print(head)
print("\n| D | bracket | det-linear root | primary rule: prediction, residual | -0.33 rule: prediction, residual | local slope | psi-constraint |\n|---|---|---|---|---|---|---|")
for D, m, br in rows:
    pt_ = part_of(D) if part == "auto" else part
    cr_ = [json.loads(x) for x in open(os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2/%s%s.jsonl" % ("" if pt_ == "a" else pt_ + "/", {"a": "l1kc87Lmacm3", "b": "l1kc87Lmacm3b", "b2": "l1kc87Lmacm3b2", "c": "l1kc87Lmacm3c", "c2": "l1kc87Lmacm3c2"}[pt_]))) if x.strip()]
    con_ = [r for r in cr_ if r["D"] == D][-1]["constraint"]
    print("| %r | (%s, %s) | **%s** | %s, %s | %s, %s%s | %s | %.2e%s |" % (D, br.group(1), br.group(2), m.group(1), m.group(5), m.group(6), m.group(7), m.group(8), " (outside 0.005)" if m.group(9) else "", m.group(10), con_, "" if con_ <= 1e-2 else " **reduced quality**"))
if opt.get("--leg"):
    legs = [float(x) for x in opt["--leg"].split(",") if x]
    for pt in dict.fromkeys(part_of(d) if part == "auto" else part for d in legs):   # one leg table per part, in order
        sub = [d for d in legs if (part_of(d) if part == "auto" else part) == pt]
        print()
        print(run(["%r" % Ds[0], "--part=" + pt, "--leg=" + ",".join(repr(d) for d in sub), "--only-leg", "--pred=x"]))
if "--note" in opt: print("\n" + opt["--note"])
print("\nEach point below carries its own tables.\n")
print("\n\n".join(secs))
if "--delta-rows" in sys.argv:
    print("\n\n### Weak modes of the leg's rows (t5: delta_reg and sigma of the remaining weak modes in every row; n_null changes shown; psi-constraint above 1e-2 flagged reduced quality)\n")
    for pt_, tag_ in (("b2", "l1kc87Lmacm3b2"), ("c", "l1kc87Lmacm3c"), ("c2", "l1kc87Lmacm3c2")):
        f_ = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2/%s/%s.jsonl" % (pt_, tag_))
        if os.path.exists(f_):
            print("**Part %s** (`kc87_leg2/%s/`):\n" % (pt_, pt_))
            print(subprocess.run([sys.executable, os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg2/delta_rows.py"), f_], capture_output=True, text=True, check=True).stdout)
if "--wide" in sys.argv:
    print("\n\n### The wide scans, side by side\n")
    print(subprocess.run([sys.executable, HERE + "/make_wide.py"], capture_output=True, text=True, check=True).stdout)

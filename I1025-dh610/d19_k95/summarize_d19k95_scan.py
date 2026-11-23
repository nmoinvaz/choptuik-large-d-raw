#!/usr/bin/env python3
"""#1025 d19_k95 (dh610) summarize_d19k95_scan.py [READING.txt] | selftest [--mutate]: prints the result tables, the coordinator's rule and the scorecard of the scan section of the README
from the files of this folder. No number is typed by hand beyond the registered bars. Reads: scan/scan_D19.0_p*.jsonl (rows, in append order per process), read_lower_scan.txt (read_lower.py on
each window and repeat_check.py; or the file given), exits_d19k95_scan.txt (checks, start, end), scan/scan_p*.raw (/usr/bin/time -v), scan/sampler.log.
The rule (coordinator t5, written before the run): the lower root of window 1 (1.395 to 1.435) moves less than 0.002 from dh170's k_c 87 root 1.414576 = converges; more than 0.004, or absent in
the window = discretization; between = no ruling. lambda_1 (window 2, 1.535 to 1.545) within 0.005 of 1.539.
selftest: planted estimates through the same verdict code (1.4146 converges, 1.4170 no ruling, 1.4200 discretization, no root = discretization, 2 roots = no ruling to report; lambda_1 1.5392 within, 1.5450
not); --mutate raises the converge bar to 0.02, and the selftest must then exit 1."""
import sys, re, json, glob, os

REF_LOW, CONV, DISC, REF_L1, BAR_L1 = 1.414576, 0.002, 0.004, 1.539, 0.005
START = "20:10:48"


def verdict(roots, conv=CONV):
    if not roots:
        return "ABSENT in the window: discretization"
    if len(roots) > 1:
        return "more than one root in the window: no ruling (reported)"
    d = abs(roots[0] - REF_LOW)
    return "converges" if d < conv else "discretization" if d > DISC else "no ruling"


def l1_ok(roots):
    return len(roots) == 1 and abs(roots[0] - REF_L1) <= BAR_L1


def selftest(mutate):
    conv = 0.02 if mutate else CONV
    cases = [([1.4146], "converges"), ([1.4170], "no ruling"), ([1.4200], "discretization"), ([], "ABSENT in the window: discretization"),
             ([1.4146, 1.4200], "more than one root in the window: no ruling (reported)")]
    bad = 0
    for r, want in cases:
        got = verdict(r, conv)
        ok = got == want
        bad += not ok
        print(f"  roots {r}: {got} (expected {want}): {'ok' if ok else 'WRONG'}")
    for r, want in [([1.5392], True), ([1.5450], False), ([], False)]:
        ok = l1_ok(r) == want
        bad += not ok
        print(f"  lambda_1 roots {r}: {l1_ok(r)} (expected {want}): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


def parse(txt):
    secs = re.split(r"^=== ", txt, flags=re.M)[1:]
    out = []
    for s in secs:
        title = s.splitlines()[0]
        ch = [(float(m[1]), float(m[2]), m[3], float(m[4]), float(m[5]), float(m[6]))
              for m in re.finditer(r"robust change \(([\d.]+), ([\d.]+)\), (\S+ to \S+), det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", s)]
        signs = re.search(r"hybrid signs: (.*)", s)
        out.append(dict(title=title, ch=ch, signs=signs[1].split() if signs else [], f64=re.search(r"float64 sign differs from the hybrid sign at: (.*)", s),
                        npts=re.search(r"points (\d+) in", s), rep=re.search(r"repeat check .*?: (.*)", s)))
    return out


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    reading = next((a for a in sys.argv[1:] if not a.startswith("--")), "read_lower_scan.txt")
    rows = []
    for p in range(6):
        for i, l in enumerate(open(f"scan/scan_D19.0_p{p}.jsonl")):
            if l.strip():
                r = json.loads(l); r["p"] = p; r["order"] = i; rows.append(r)
    rows.sort(key=lambda r: (r["lam"], r["p"]))
    sg = lambda v: "+" if v > 0 else "-"
    print("| lambda | process | round | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['lam']:.3f} | p{r['p']} | {r['order'] + 1} | {sg(r['sign'])} | {''.join(sg(n) for n in r['noise'])} ({r['noise_robust']}) | {sg(r['f64_sign'])} | {r['ln']!r} | {r['sec']} |")
    t = [r["sec"] for r in rows]
    print(f"\nevaluations {len(rows)} of 12; seconds per point min {min(t)}, median {sorted(t)[len(t) // 2]}, max {max(t)}; not noise-robust: {[r['lam'] for r in rows if not r['noise_robust']] or 'none'}")
    w1 = [r for r in rows if r["lam"] < 1.5]
    f64 = [(r["lam"], sg(r["sign"]), sg(r["f64_sign"])) for r in w1 if r["sign"] != r["f64_sign"]]
    rep = [r for r in rows if abs(r["lam"] - 1.415) < 1e-9]
    rep_ok = len(rep) == 2 and all(rep[0][k] == rep[1][k] for k in ("sign", "noise", "f64_sign", "ln", "f64_ln"))
    print(f"float64 sign differs from the hybrid in window 1 at {len(f64)} of {len(w1)} evaluations: {f64 or 'none'}; the repeat of 1.415 (p{rep[0]['p']} round {rep[0]['order'] + 1}, p{rep[1]['p']} round {rep[1]['order'] + 1}): ln|det| {rep[0]['ln']!r} and {rep[1]['ln']!r}, bit-identical in sign, noise, float64 and ln|det|: {rep_ok}")
    ex = open("exits_d19k95_scan.txt").read()
    chk = re.findall(r"kc95_syscheck exit (\d) \(0 wanted\); controls --mutate=F exit (\d), --mutate=steps exit (\d) \(1 wanted each\); kc87_syscheck exit (\d) \(1 wanted\)", ex)[-1]
    chk = tuple(int(x) for x in chk)
    nrec = len(re.findall(r"^D 19\.0 k_c 95: .*: the record system$", "".join(open(f).read() for f in glob.glob("scan/scan_p?.raw")), re.M))
    ends = re.findall(r"^(\S+ \S+) UTC scan p(\d) \((\S+)\) exit (\d)", ex, re.M) or re.findall(r"^(\S+ \S+) UTC process (\d) exit (\d)", ex, re.M)
    done = re.findall(r"^== (\S+) (\S+) UTC d19_k95 scan: scan done", ex, re.M)
    rss = [int((re.search(r"Maximum resident set size \(kbytes\): (\d+)", open(f).read()) or [0, 0])[1]) for f in sorted(glob.glob("scan/scan_p?.raw"))]
    print(f"\nsource check on the pinned copies: kc95 exit {chk[0]}, controls {chk[1]} {chk[2]}, kc87 check {chk[3]}; processes that printed the record system: {nrec} of 6; peak RSS per process (time -v) {[round(x / 1048576, 2) for x in rss]} GiB; process exits: {len(re.findall(r'process \d exit 0', ex)) + len(re.findall(r'scan p\d .*exit 0', ex))} of 6 with exit 0; scan done line: {done[-1][1] if done else 'not yet'}")
    r1_end = None
    first = {}
    for r in rows:
        if r["order"] == 0:
            first[r["p"]] = r["sec"]
    if len(first) == 6:
        h, m, s = (int(x) for x in START.split(":"))
        r1_end = h * 3600 + m * 60 + s + max(first.values())
        print(f"round 1 ended (start {START} UTC + the latest first-point seconds {max(first.values())}) at {r1_end // 3600:02d}:{r1_end % 3600 // 60:02d} UTC")
    secs = parse(open(reading).read())
    res = {}
    for s in secs:
        if "repeat_check" in s["title"]:
            print(f"\n{s['title']}: {s['rep'][1] if s['rep'] else 'n/a'}")
            continue
        which = "window 1 (1.395 to 1.435)" if "1.395" in s["title"] else "window 2 (1.535 to 1.545)"
        roots = [c[3] for c in s["ch"]]
        res[which[:8]] = (roots, s)
        print(f"\n{which}: hybrid signs {' '.join(s['signs'])}; robust changes {len(s['ch'])}: {[(c[0], c[1], c[2], c[3], (c[4], c[5])) for c in s['ch']]}")
    rw1, s1 = res.get("window 1", ([], None))
    rw2, s2 = res.get("window 2", ([], None))
    full = len(s1["signs"]) == 9 if s1 else False
    print(f"\nthe coordinator's rule, window 1 {'(all 9 points)' if full else '(PARTIAL: ' + str(len(s1['signs'])) + ' points)'}: {verdict(rw1)}" + (f"; the estimate {rw1[0]:.6f} moves {rw1[0] - REF_LOW:+.6f} from dh170's k_c 87 root {REF_LOW} (bars 0.002 and 0.004)" if len(rw1) == 1 else ""))
    print(f"lambda_1, window 2 {'(both points)' if s2 and len(s2['signs']) == 2 else '(PARTIAL)'}: roots {rw2}; within 0.005 of {REF_L1}: {l1_ok(rw2)}" + (f" ({rw2[0] - REF_L1:+.6f})" if len(rw2) == 1 else ""))
    ok = lambda c: "right" if c else "WRONG"
    e1 = (s1["signs"][0][-1], s1["signs"][-1][-1]) if s1 and s1["signs"] else ("?", "?")
    e2 = (s2["signs"][0][-1], s2["signs"][-1][-1]) if s2 and s2["signs"] else ("?", "?")
    one1 = len(rw1) == 1
    d1 = abs(rw1[0] - REF_LOW) if one1 else None
    br1 = tuple(s1["ch"][0][:2]) if one1 else None
    print("\n| prediction (registered before the run) | result | verdict |")
    print("|---|---|---|")
    rows_s = [("pinned copies accepted, controls 1 1, kc87 refuses (96%)", f"exits {chk}", chk == (0, 1, 1, 1)),
              ("all six print the record system (92%)", f"{nrec} of 6", nrec == 6),
              ("every point noise-robust (70%)", f"{sum(r['noise_robust'] for r in rows)} of {len(rows)}", all(r["noise_robust"] for r in rows)),
              ("repeat of 1.415 bit-identical (90%)", f"{rep_ok}", rep_ok),
              ("window 1: exactly one robust change (85%)", f"{len(rw1)}", one1),
              ("window 1: edge signs unequal (88%)", f"{e1[0]} at 1.395, {e1[1]} at 1.435", e1[0] != e1[1]),
              ("window 1: estimate within 0.002 of 1.414576 (75%)", f"{'%.6f' % rw1[0] if one1 else 'none'}", one1 and d1 < 0.002),
              ("window 1: bracket (1.410, 1.415) (50%) or (1.415, 1.420) (40%)", f"{br1}", br1 in ((1.41, 1.415), (1.415, 1.42))),
              ("window 2: one change, signs unequal (85%)", f"{len(rw2)} change, {e2[0]} at 1.535, {e2[1]} at 1.545", len(rw2) == 1 and e2[0] != e2[1]),
              ("window 2: estimate within 0.005 of 1.539 (75%)", f"{rw2}", l1_ok(rw2)),
              ("float64 sign differs from the hybrid at more than half of window 1 (30%; right = it happened)", f"{len(f64)} of {len(w1)} evaluations", len(f64) > len(w1) / 2),
              ("seconds per point 2300 to 3200 s (65%)", f"{min(t)} to {max(t)}", all(2300 <= x <= 3200 for x in t)),
              ("round 1 ends by 21:10 UTC (70%)", f"{r1_end // 3600:02d}:{r1_end % 3600 // 60:02d}" if r1_end else "n/a", bool(r1_end) and r1_end <= 21 * 3600 + 600),
              ("lane ends 21:30 to 22:10 UTC (60%)", done[-1][1] if done else "not yet", bool(done) and "21:30" <= done[-1][1][:5] <= "22:10"),
              ("peak RSS per process below 3.6 GiB (85%)", f"max {max(rss) / 1048576:.2f} GiB" if any(rss) else "n/a", bool(any(rss)) and max(rss) < 3.6 * 1048576)]
    for n, r, c in rows_s:
        print(f"| {n} | {r} | {ok(c)} |")
    if "--mutate" in sys.argv:
        clean = verdict(rw1)
        mut = verdict([x + 0.003 for x in rw1] if rw1 else [REF_LOW])
        print(f"mutate: the window-1 verdict '{clean}' against '{mut}' with the estimate moved by +0.003 (or planted at the reference when absent)")
        print("mutate: control " + ("FIRED (exit 1)" if mut != clean else "did NOT fire (exit 3)"))
        sys.exit(1 if mut != clean else 3)

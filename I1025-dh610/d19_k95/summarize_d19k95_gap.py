#!/usr/bin/env python3
"""#1025 d19_k95 gap (dh610) summarize_d19k95_gap.py [READING.txt] [--mutate] | selftest [--mutate]: prints the result tables, the coordinator's rule and the scorecard of gap/README.md from the files of this
folder (run from d19_k95/). No number is typed by hand beyond the registered bars. Reads: gap/scan/scan_D19.0_p*.jsonl (the five new rows), gap/scan/scan_ref_p*.jsonl (the edge rows 1.435 and 1.535 copied from
../scan by the lane), gap/read_lower_gap.txt (read_lower.py on 1.435 to 1.535, or the file given), exits_d19k95_gap.txt, gap/scan/scan_p*.raw (/usr/bin/time -v), gap/scan/sampler.log.
The rule (coordinator t5, written before the run): no sign change in 1.445 to 1.525 and equal edge signs with 1.435 and 1.535 (all -) closes the pair caveat; anything else leaves it open, reported by position.
selftest: planted sign lists through the same verdict code (all - closed; a + in the middle open with two changes; a + at 1.445 open; a + at 1.525 open); --mutate makes the verdict ignore the sign list and
read the reader's change count only, so the planted + cases must then pass as closed: the selftest exits 1.
--mutate on the real files flips the sign of the middle new point (1.485) in the verdict; the control fires (exit 1) when the verdict changes, and exits 3 when it does not."""
import sys, re, json, glob, datetime

LAMS = [1.435, 1.445, 1.465, 1.485, 1.505, 1.525, 1.535]
START = None


def verdict(signs, changes=None, ignore_signs=False):
    """signs: hybrid signs (+1/-1) at the seven points in order; changes: the reader's robust-change count."""
    flips = [i for i in range(len(signs) - 1) if signs[i] != signs[i + 1]]
    if ignore_signs:
        flips = list(range(changes or 0))
    if not flips:
        return "closed: no sign change, all seven points " + ("-" if signs[0] < 0 else "+")
    return "OPEN: sign change(s) between " + ", ".join(f"{LAMS[i]:.3f} and {LAMS[i + 1]:.3f}" for i in flips if i < len(LAMS) - 1)


def selftest(mutate):
    cases = [([-1] * 7, "closed"), ([-1, -1, -1, 1, -1, -1, -1], "OPEN"), ([-1, 1, -1, -1, -1, -1, -1], "OPEN"), ([-1, -1, -1, -1, -1, 1, -1], "OPEN")]
    bad = 0
    for s, want in cases:
        got = verdict(s, 0, ignore_signs=mutate)
        ok = got.startswith(want)
        bad += not ok
        print(f"  signs {s}: {got} (expected {want}...): {'ok' if ok else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    reading = next((a for a in sys.argv[1:] if not a.startswith("--")), "gap/read_lower_gap.txt")
    new, ref = [], []
    for p in range(5):
        for l in open(f"gap/scan/scan_D19.0_p{p}.jsonl"):
            if l.strip():
                r = json.loads(l); r["p"] = p; new.append(r)
    for f in sorted(glob.glob("gap/scan/scan_ref_p*.jsonl")):
        ref += [json.loads(l) for l in open(f) if l.strip()]
    rows = sorted([dict(r, src="new") for r in new] + [dict(r, src="ref (../scan)", p="-") for r in ref], key=lambda r: r["lam"])
    sg = lambda v: "+" if v > 0 else "-"
    print("| lambda | source | process | hybrid sign | noise signs (robust) | float64 sign | ln of abs det | seconds |")
    print("|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['lam']:.3f} | {r['src']} | {'p%s' % r['p'] if r['p'] != '-' else '-'} | {sg(r['sign'])} | {''.join(sg(n) for n in r['noise'])} ({r['noise_robust']}) | {sg(r['f64_sign'])} | {r['ln']!r} | {r['sec']} |")
    t = [r["sec"] for r in new]
    print(f"\nnew evaluations {len(new)} of 5; seconds per new point min {min(t)}, median {sorted(t)[len(t) // 2]}, max {max(t)}; not noise-robust: {[r['lam'] for r in rows if not r['noise_robust']] or 'none'}")
    f64 = [(r["lam"], sg(r["sign"]), sg(r["f64_sign"])) for r in new if r["sign"] != r["f64_sign"]]
    print(f"float64 sign differs from the hybrid at {len(f64)} of {len(new)} new points: {f64 or 'none'}")
    ln = [r["ln"] for r in rows]
    falls = all(ln[i + 1] < ln[i] for i in range(len(ln) - 1))
    steps = [round(ln[i + 1] - ln[i], 5) for i in range(len(ln) - 1)]
    print(f"ln|det| along the seven points: {[round(x, 5) for x in ln]}; steps {steps}; strictly falling: {falls}")
    ex = open("exits_d19k95_gap.txt").read()
    chk = tuple(int(x) for x in re.findall(r"kc95_syscheck exit (\d) \(0 wanted\); controls --mutate=F exit (\d), --mutate=steps exit (\d) \(1 wanted each\); kc87_syscheck exit (\d) \(1 wanted\)", ex)[-1])
    nrec = len(re.findall(r"^D 19\.0 k_c 95: .*: the record system$", "".join(open(f).read() for f in glob.glob("gap/scan/scan_p?.raw")), re.M))
    done = re.findall(r"^== (\S+) (\S+) UTC d19_k95 gap: scan done", ex, re.M)
    rss = [int((re.search(r"Maximum resident set size \(kbytes\): (\d+)", open(f).read()) or [0, 0])[1]) for f in sorted(glob.glob("gap/scan/scan_p?.raw"))]
    nexit = len(re.findall(r"scan p\d \(\S+\) exit 0", ex))
    print(f"\nsource check on the pinned copies: kc95 exit {chk[0]}, controls {chk[1]} {chk[2]}, kc87 check {chk[3]}; processes that printed the record system: {nrec} of 5; peak RSS per process (time -v) {[round(x / 1048576, 2) for x in rss]} GiB; process exits 0: {nexit} of 5; scan done line: {done[-1][1] if done else 'not yet'}")
    txt = open(reading).read()
    nch = re.search(r"robust changes: (\d+)", txt)
    nch = int(nch[1]) if nch else -1
    lines = re.findall(r"robust change \(([\d.]+), ([\d.]+)\), (\S+ to \S+), det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]", txt)
    pm = re.search(r"points \d+ in", txt)
    print(f"read_lower.py on 1.435 to 1.535: {pm[0] if pm else 'no points line'}; robust changes {nch}: {lines or 'none'}")
    signs = [1 if r["sign"] > 0 else -1 for r in rows]
    sg_mut = list(signs)
    if "--mutate" in sys.argv:
        sg_mut[3] = -sg_mut[3]
    v = verdict(signs, nch)
    print(f"\nthe coordinator's rule: {v}" + ("" if nch == len([i for i in range(6) if signs[i] != signs[i + 1]]) else f"; WARNING: the reader's change count {nch} differs from the sign flips"))
    ok = lambda c: "right" if c else "WRONG"
    r_ok = [r for r in new if abs(r["lam"] - 1.525) < 1e-9]
    ln525 = r_ok[0]["ln"] if r_ok else None
    print("\n| prediction (registered before the run) | result | verdict |")
    print("|---|---|---|")
    rows_s = [("pinned copies accepted, controls 1 1, kc87 refuses (96%)", f"exits {chk}", chk == (0, 1, 1, 1)),
              ("all five print the record system (93%)", f"{nrec} of 5", nrec == 5),
              ("every point noise-robust (85%)", f"{sum(r['noise_robust'] for r in rows)} of {len(rows)}", all(r["noise_robust"] for r in rows)),
              ("no robust change and all seven hybrid signs - (88%)", f"{nch} changes, signs {''.join(sg(r['sign']) for r in rows)}", nch == 0 and all(s < 0 for s in signs)),
              ("ln|det| strictly falls along the seven points (80%)", f"{falls}", falls),
              ("ln|det| at 1.525 within 0.3 of -3248.05 (60%)", f"{ln525!r}", ln525 is not None and abs(ln525 + 3248.05) <= 0.3),
              ("float64 sign agrees with the hybrid at all five (85%)", f"{len(new) - len(f64)} of {len(new)}", not f64),
              ("seconds per point 3500 to 6000 s (65%)", f"{min(t)} to {max(t)}", all(3500 <= x <= 6000 for x in t)),
              ("lane ends by 01:30 UTC (70%)", " ".join(done[-1]) if done else "not yet", bool(done) and datetime.datetime.fromisoformat(" ".join(done[-1])) <= datetime.datetime(2026, 11, 24, 1, 30)),
              ("peak RSS per process below 3.6 GiB (85%)", f"max {max(rss) / 1048576:.2f} GiB" if any(rss) else "n/a", bool(any(rss)) and max(rss) < 3.6 * 1048576)]
    for n, c_, c in rows_s:
        print(f"| {n} | {c_} | {ok(c)} |")
    if "--mutate" in sys.argv:
        vm = verdict(sg_mut, nch)
        print(f"\nmutate: the verdict '{v}' against '{vm}' with the sign of 1.485 flipped")
        print("mutate: control " + ("FIRED (exit 1)" if vm != v else "did NOT fire (exit 3)"))
        sys.exit(1 if vm != v else 3)

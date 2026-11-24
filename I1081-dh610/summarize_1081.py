#!/usr/bin/env python3
"""#1081 dh610 summarize_1081.py [--mutate] | selftest [--mutate]: prints the margin tables, the order's criterion, the acceptance checks and the scorecard of README.md from the files of this folder
(run from this folder, or set I1081_ROOT). No number is typed by hand beyond the registered bars. Reads cfg_<a,b,c>/{point.json, box_<U,s1..s6>.json, krawczyk_<run>.log, controls_U.log, logs/<job>.time,
logs/<job>_stdout.log}, steps.txt, exits_1081.txt and ../I1079-dh610/steps.txt (the #1079 rerun's unperturbed margins at the second zero).
The order's criterion (coordinator t5): a configuration is robust when all six perturbed runs pass (K(X) in int X: True) and the smallest of the 24 relative margins is above +0.2.
selftest: planted margin sets through the same verdict code (all pass, smallest 0.5: robust; one run False: not; smallest 0.15: not; smallest exactly 0.2: not; smallest 0.2001: robust) and planted Krawczyk lines
through the parser; --mutate lowers the bar to -1, so the 0.15 case must then pass as robust: the selftest exits 1.
--mutate on the real files: each configuration's verdict is recomputed after a planted change (a robust configuration gets one margin of -1, a non-robust one gets six passing runs with margins 0.9); the control
fires (exit 1, "control FIRED") when all three verdicts change, and exits 3 when not."""
import sys, os, re, json, glob, hashlib, datetime, statistics

BAR = 0.2
ROOT = os.environ.get("I1081_ROOT", ".")
CFG = {"a": dict(h="1e-12", w="1e-12", prec=256), "b": dict(h="1e-12", w="1e-12", prec=384), "c": dict(h="1e-13", w="1e-13", prec=256)}
RUNS = ["U"] + [f"s{k}" for k in range(1, 7)]
KRE = re.compile(r"K\(X\) in int X: (True|False); relative margins ([+-][\d.]+(?:, [+-][\d.]+)*)")


def parse_kraw(text):
    m = KRE.search(text)
    if not m:
        return None
    return m[1] == "True", [float(x) for x in m[2].split(", ")]


def verdict(runs, bar=BAR):
    """runs: the six perturbed runs as (ok, margins). Robust: all pass and the smallest margin of all of them is above bar."""
    npass = sum(1 for ok, _ in runs if ok)
    smallest = min(min(mg) for _, mg in runs)
    return npass == len(runs) and smallest > bar, npass, smallest


def selftest(mutate):
    bar = -1.0 if mutate else BAR
    good = lambda m: (True, [m, 0.9, 0.98, 0.99])
    cases = [("all pass, smallest 0.5", [good(0.5)] * 6, True),
             ("one run False", [good(0.5)] * 5 + [(False, [0.25, -0.25, 0.98, 0.99])], False),
             ("all pass, smallest 0.15", [good(0.5)] * 5 + [good(0.15)], False),
             ("all pass, smallest exactly 0.2", [good(0.5)] * 5 + [good(0.2)], False),
             ("all pass, smallest 0.2001", [good(0.5)] * 5 + [good(0.2001)], True)]
    bad = 0
    for n, runs, want in cases:
        got = verdict(runs, bar)[0]
        bad += got != want
        print(f"  {n}: robust {got} (expected {want}): {'ok' if got == want else 'WRONG'}")
    lines = [("Krawczyk M = 3: K(X) in int X: True; relative margins +0.711, +0.528, +0.981, +0.992", (True, [0.711, 0.528, 0.981, 0.992])),
             ("Krawczyk M = 3: K(X) in int X: False; relative margins +0.251, -0.247, +0.980, +0.992", (False, [0.251, -0.247, 0.980, 0.992])),
             ("nothing here", None)]
    for t, want in lines:
        got = parse_kraw(t)
        bad += got != want
        print(f"  parse {t[:60]!r}: {got} ({'ok' if got == want else 'WRONG'})")
    planted = ("chain exc2 2026-11-23 17:47:30 margins M3x2E2_h1e-12_w1e-12 exit 0 (0 wanted): Krawczyk M = 3: K(X) in int X: True; relative margins +0.711, +0.528, +0.981, +0.992\n"
               "xload exc2 2026-11-23 18:06:05 cross-load margins M3x2E2_h1e-12_w1e-12 exit 0 (0 wanted): Krawczyk M = 3: K(X) in int X: True; relative margins +0.943, +0.945, +0.988, +0.995\n")
    want = (True, [0.711, 0.528, 0.981, 0.992])
    got = ref79(planted, loose=mutate)
    bad += got != want
    print(f"  ref79 on a chain line followed by a cross-load line: {got} (expected {want}): {'ok' if got == want else 'WRONG'}")
    print("selftest" + (" --mutate" if mutate else ""), "FAIL" if bad else "PASS")
    return 1 if bad else 0


def ref79(text, loose=False):
    """the #1079 rerun's unperturbed margins at the second zero: the line of the chain stage (not the later cross-load line). loose=True is the control's mutation: the last line of any stage."""
    pat = (r"margins M3x2E2_h1e-12_w1e-12 exit 0 \(0 wanted\)" if loose else r"^chain exc2 \S+ \S+ margins M3x2E2_h1e-12_w1e-12 exit 0 \(0 wanted\)") + \
        r": Krawczyk M = 3: K\(X\) in int X: (True|False); relative margins ([+-][\d.]+(?:, [+-][\d.]+)*)"
    m = re.findall(pat, text, re.M)
    return (m[-1][0] == "True", [float(x) for x in m[-1][1].split(", ")]) if m else None


def rd(path):
    return open(os.path.join(ROOT, path)).read()


def jl(path):
    return json.load(open(os.path.join(ROOT, path)))


def wall(path):
    m = re.search(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\): ([\d:.]+)", rd(path))
    t = [float(x) for x in m[1].split(":")]
    return sum(v * 60 ** i for i, v in enumerate(reversed(t)))


def rss(path):
    return int(re.search(r"Maximum resident set size \(kbytes\): (\d+)", rd(path))[1]) / 1048576


def sets_hash(d):
    return hashlib.sha256(json.dumps(d["sets"], sort_keys=True).encode()).hexdigest()[:16]


if __name__ == "__main__":
    if sys.argv[1:2] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    sg = lambda x: f"{x:+.3f}"
    res, checks, jobs, times, rsses = {}, [], {}, {}, {}
    print("| config | run | exit | K(X) in int X | relative margins | smallest | box seconds (file) | perturbed calls | sets differ from U |")
    print("|---|---|---|---|---|---|---|---|---|")
    for c, cf in CFG.items():
        pt = jl(f"cfg_{c}/point.json")
        boxes = {r: jl(f"cfg_{c}/box_{r}.json") for r in RUNS}
        res[c] = {}
        for r in RUNS:
            t = rd(f"cfg_{c}/krawczyk_{r}.log")
            k = parse_kraw(t)
            rc = re.search(r"^exit (\d+)", rd(f"cfg_{c}/krawczyk_{r}.exit"), re.M)[1]
            res[c][r] = k
            pc = re.search(r"perturbed calls: qr_pivot (\d+)", rd(f"cfg_{c}/logs/{r}_stdout.log"))
            pc = int(pc[1]) if pc else None
            diff = "-" if r == "U" else str(sets_hash(boxes[r]) != sets_hash(boxes["U"]))
            print(f"| {c} | {r} | {rc} | {k[0]} | {', '.join(sg(x) for x in k[1])} | {sg(min(k[1]))} | {boxes[r]['sec']:.0f} | {pc if pc is not None else 'none'} | {diff} |")
            checks.append(("record prec/h/w/orders", c, r, boxes[r]["prec"] == cf["prec"] and boxes[r]["h"] == cf["h"] and boxes[r]["w"] == [cf["w"]] and boxes[r].get("orders") == [28, 16]))
            checks.append(("perturbation acted" if r != "U" else "unperturbed run has no perturbation", c, r, (pc is not None and pc > 0) if r != "U" else pc is None))
            if r != "U":
                checks.append(("perturbed box differs from U", c, r, diff == "True"))
        checks.append(("point record prec/orders", c, "point", pt["prec"] == cf["prec"] and pt.get("orders") == [28, 16]))
        if c == "b":
            for r in RUNS:
                checks.append(("b's box differs from a's at the same run (the 384-bit run is not a copy)", c, r, sets_hash(boxes[r]) != sets_hash(jl(f"cfg_a/box_{r}.json"))))
    print()
    pa, pc_ = jl("cfg_a/point.json"), jl("cfg_c/point.json")
    same = all(pa[k] == pc_[k] for k in ("p", "g", "steps"))
    checks.append(("point files of a and c equal in p, g, steps", "a,c", "point", same))
    print("| config | perturbed runs passing | smallest margin of the six perturbed runs | robust (all six pass, smallest > +0.2) | unperturbed run passes | unperturbed margins |")
    print("|---|---|---|---|---|---|")
    vd = {}
    for c in CFG:
        six = [res[c][f"s{k}"] for k in range(1, 7)]
        vd[c] = verdict(six)
        u = res[c]["U"]
        print(f"| {c} (h = w = {CFG[c]['h']}, PREC {CFG[c]['prec']}) | {vd[c][1]} of 6 | {sg(vd[c][2])} | {vd[c][0]} | {u[0]} | {', '.join(sg(x) for x in u[1])} |")
    print()
    ctl = {}
    for c in CFG:
        t = rd(f"cfg_{c}/controls_U.log")
        ctl[c] = ("CONTROLS ALL AS EXPECTED" in t, int(re.search(r"^exit (\d+)", rd(f"cfg_{c}/controls_U.exit"), re.M)[1]))
        checks.append(("certify_M.py controls on U exit 0, all as expected", c, "U", ctl[c] == (True, 0)))
    ex = rd("steps.txt")
    for c in CFG:
        for r in ["point"] + RUNS:
            m = re.findall(rf"^\S+ \S+ end {c} {r} exit (\d+), (\d+) s", ex, re.M)
            jobs[(c, r)] = int(m[-1][0]) if m else None
            times[(c, r)] = wall(f"cfg_{c}/logs/{r}.time")
            rsses[(c, r)] = rss(f"cfg_{c}/logs/{r}.time")
    allexit0 = all(v == 0 for v in jobs.values()) and len(jobs) == 24
    bad = [x for x in checks if not x[3]]
    print(f"acceptance checks: {len(checks) - len(bad)} of {len(checks)} hold; failing: {[x[:3] for x in bad] or 'none'}; every job exit 0: {allexit0} ({len(jobs)} jobs)")
    for c in CFG:
        a = [times[(c, r)] for r in ["point"] + RUNS]
        print(f"config {c}: seconds (wall, /usr/bin/time -v) point {times[(c, 'point')]:.0f}, box U {times[(c, 'U')]:.0f}, perturbed {min(times[(c, f's{k}')] for k in range(1, 7)):.0f} to {max(times[(c, f's{k}')] for k in range(1, 7)):.0f}; peak RSS {min(rsses[(c, r)] for r in ['point'] + RUNS):.2f} to {max(rsses[(c, r)] for r in ['point'] + RUNS):.2f} GiB")
    ln = [l for l in rd("exits_1081.txt").splitlines()]
    st = next((l for l in ln if "pool starts" in l), None)
    en = next((l for l in ln if "pool ended" in l), None)
    stt = datetime.datetime.fromisoformat(re.search(r"== (\S+ \S+) UTC", st)[1]) if st else None
    ent = datetime.datetime.fromisoformat(re.search(r"== (\S+ \S+) UTC", en)[1]) if en else None
    mins = (ent - stt).total_seconds() / 60 if stt and ent else None
    print(f"pool: {stt or 'n/a'} to {ent or 'n/a'}" + (f" ({mins:.0f} min)" if mins else ""))
    k79 = ref79(open(os.path.join(ROOT, "..", "I1079-dh610", "steps.txt")).read())
    print(f"#1079 rerun, second zero, unperturbed (c40fbc77): {k79}; this run's (a, U): {res['a']['U']}; equal to the printed digits: {k79 == res['a']['U']}")
    ok = lambda c: "right" if c else "WRONG"
    fails_a = 6 - vd["a"][1]
    t256 = [times[(c, r)] for c in "ac" for r in ["point"] + RUNS]
    ratio = statistics.median([times[("b", r)] for r in RUNS]) / statistics.median([times[("a", r)] for r in RUNS])
    ratios = [times[("b", r)] / times[("a", r)] for r in ["point"] + RUNS]
    print(f"time ratios b over a per job kind: {[round(x, 2) for x in ratios]}; PREC 256 seconds {min(t256):.0f} to {max(t256):.0f}; peak RSS over all jobs {max(rsses.values()):.2f} GiB")
    pert = [x for x in checks if x[0] == "perturbation acted"]
    diff = [x for x in checks if x[0] == "perturbed box differs from U"]
    print("\n| prediction (registered before the run; right = the stated event happened) | result | verdict |")
    print("|---|---|---|")
    rows = [("every job exit 0 and the acceptance holds (88%)", f"exit0 {allexit0}, failing checks {len(bad)}", allexit0 and not bad),
            ("the perturbation acted in all 18 perturbed runs (96%)", f"{sum(x[3] for x in pert)} of {len(pert)}", all(x[3] for x in pert) and len(pert) == 18),
            ("the 18 perturbed box files all differ from their U (96%)", f"{sum(x[3] for x in diff)} of {len(diff)}", all(x[3] for x in diff) and len(diff) == 18),
            ("unperturbed box passes at a (90%)", str(res["a"]["U"][0]), res["a"]["U"][0]),
            ("unperturbed box passes at b (85%)", str(res["b"]["U"][0]), res["b"]["U"][0]),
            ("unperturbed box passes at c (90%)", str(res["c"]["U"][0]), res["c"]["U"][0]),
            ("(a, U) margins equal the #1079 rerun's to the printed digits (85%)", str(k79 == res["a"]["U"]), k79 == res["a"]["U"]),
            ("(a) at least four of six perturbed runs fail (75%)", f"{fails_a} of 6 fail", fails_a >= 4),
            ("(a) all six perturbed runs fail (25%)", f"{fails_a} of 6 fail", fails_a == 6),
            ("(a) all six perturbed runs pass (5%)", f"{vd['a'][1]} of 6 pass", vd["a"][1] == 6),
            ("(a) not robust (97%)", f"robust {vd['a'][0]}", not vd["a"][0]),
            ("(b) robust (25%)", f"{vd['b'][1]} of 6 pass, smallest {sg(vd['b'][2])}", vd["b"][0]),
            ("(c) robust (70%)", f"{vd['c'][1]} of 6 pass, smallest {sg(vd['c'][2])}", vd["c"][0]),
            ("at least one of b and c robust (75%)", f"b {vd['b'][0]}, c {vd['c'][0]}", vd["b"][0] or vd["c"][0]),
            ("both b and c robust (20%)", f"b {vd['b'][0]}, c {vd['c'][0]}", vd["b"][0] and vd["c"][0]),
            ("PREC 256 jobs each 300 to 650 s (70%)", f"{min(t256):.0f} to {max(t256):.0f}", all(300 <= x <= 650 for x in t256)),
            ("PREC 384 jobs 1.3 to 2.5 times the PREC 256 (a) jobs of the same kind (70%)", f"{min(ratios):.2f} to {max(ratios):.2f}", all(1.3 <= x <= 2.5 for x in ratios)),
            ("the pool ends within 75 min of its start (70%)", f"{mins:.0f} min" if mins else "n/a", mins is not None and mins <= 75),
            ("peak RSS per job below 3 GiB (80%)", f"max {max(rsses.values()):.2f} GiB", max(rsses.values()) < 3)]
    for n, r_, c_ in rows:
        print(f"| {n} | {r_} | {ok(c_)} |")
    if "--mutate" in sys.argv:
        changed = []
        for c in CFG:
            six = [res[c][f"s{k}"] for k in range(1, 7)]
            if vd[c][0]:
                six = six[:5] + [(True, [-1.0, 0.9, 0.98, 0.99])]
            else:
                six = [(True, [0.9, 0.9, 0.98, 0.99])] * 6
            changed.append(verdict(six)[0] != vd[c][0])
        print(f"\nmutate: verdicts changed by the planted change, per configuration (a, b, c): {changed}")
        print("mutate: control " + ("FIRED (exit 1)" if all(changed) else "did NOT fire (exit 3)"))
        sys.exit(1 if all(changed) else 3)

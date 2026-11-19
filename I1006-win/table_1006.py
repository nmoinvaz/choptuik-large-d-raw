#!/usr/bin/env python3
"""#1006 (win): tables and the reading by the issue's acceptance, from logs/T1_{a,b,c24}.log and x/T1_{a,b,c24}.json. From I985-win/table_985.py.

usage: python table_1006.py [--selftest] [--logs DIR] [--x DIR]      (any python 3 with the standard library; from this folder)

Rules (README.md, fixed before the first run). d = the number of singular values within 1e-4 of the top (rt_xcount), gap = s_(d+1)/s_d, clean at 1e-3 or below, share = the smaller of a run's two chord shares in span(p_1..p_d).
 - (H4) AT k = 1/2 AND 3/2 HOLDS if all three runs give d = 4, a clean gap and share >= 0.99.
 - REOPENED if any run gives d = 3 or d >= 5.   DOES NOT HOLD for anything else (d of 1 or 2, d = 4 with a gap above 1e-3 or a share below 0.99).   INCOMPLETE if a run lacks its N bounds or its count.
Informational: the first n start lines of each log against the stored rough log of the same state, in every character and on max|x|, bound and products only."""
import json
import math
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = r"C:\Users\nathan\Source\choptuik-large-d-raw"
RUNS = [("T1_a", "a", 12, RAW + r"\I943-win\logs\K0_D40_rough.log"), ("T1_b", "b", 12, RAW + r"\I701-win\logs\K0b_D40_rough.log"), ("T1_c24", "c", 24, RAW + r"\I951-win\logs\K0c_D40_rough.log")]
CAP = 250
CLEAN, SHARE, CUT = 1e-3, 0.99, 1e-4
START = re.compile(r"^\s+start (\d+): max\|x\| (\S+), bound on the smallest gain (\S+), max\|J x - v\| (\S+), (\d+) products")
XLINE = re.compile(r"^\s+start (\d+), x / max\|x\|:")
HEAD = re.compile(r"max\|F\| (\S+)\s*$")
MU = re.compile(r"^\s+start 0, x / max\|x\|: mu (\S+);")
BEST = re.compile(r"best bound on the smallest gain \(max norm\) (\S+);")


def median(v):
    s = sorted(v)
    n = len(s)
    return s[n // 2] if n % 2 else math.sqrt(s[n // 2 - 1] * s[n // 2])


def parse(path):
    r = dict(maxF=None, bounds=[], prods=[], res=[], mu0=None, best=None, slines=[], xlines=[], exists=os.path.exists(path))
    if not r["exists"]:
        return r
    for ln in open(path, encoding="utf-8", errors="replace"):
        ln = ln.rstrip("\r\n")
        m = START.match(ln)
        if m:
            r["bounds"].append(float(m.group(3)))
            r["prods"].append(int(m.group(5)))
            r["res"].append(m.group(4))
            r["slines"].append(ln)
        elif XLINE.match(ln):
            r["xlines"].append(ln)
            if MU.match(ln):
                r["mu0"] = MU.match(ln).group(1)
        elif r["maxF"] is None and HEAD.search(ln):
            r["maxF"] = HEAD.search(ln).group(1)
        elif BEST.search(ln):
            r["best"] = float(BEST.search(ln).group(1))
    return r


def compare(path, ref, n):
    """(characters equal, fields equal, x lines equal, text) over the first n start lines of path against ref"""
    a, b = parse(path), parse(ref)
    if not a["exists"] or not b["exists"] or len(a["slines"]) < n or len(b["slines"]) < n:
        return None, None, None, "log missing or shorter than n"
    f = lambda ln: tuple(START.match(ln).group(i) for i in (1, 2, 3, 5))
    ne = sum(1 for p, q in zip(a["slines"][:n], b["slines"][:n]) if p == q)
    nf = sum(1 for p, q in zip(a["slines"][:n], b["slines"][:n]) if f(p) == f(q))
    nx = sum(1 for p, q in zip(a["xlines"][:n], b["xlines"][:n]) if p == q) if len(a["xlines"]) >= n and len(b["xlines"]) >= n else 0
    return ne, nf, nx, f"{ne} of {n} start lines equal in every character, {nf} of {n} on max|x|, bound and products, {nx} of {n} x / max|x| lines equal"


def judge(d, gap, share):
    """(ok, why) for one run"""
    if d is None:
        return None, "no count"
    clean = gap is not None and gap <= CLEAN
    ok = d == 4 and clean and share is not None and share >= SHARE
    why = f"d = {d}, gap {'-' if gap is None else format(gap, '.2e')} ({'clean' if clean else 'not clean'}), smaller chord share {'-' if share is None else format(share, '.6f')} ({'>=' if share is not None and share >= SHARE else '<'} 0.99)"
    return ok, why


def reading(runs):
    """runs = [(d, gap, share) or None, ...]. Returns (word, why)."""
    if any(r is None or r[0] is None for r in runs):
        return "INCOMPLETE", "a run lacks its bounds or its count"
    if any(r[0] == 3 or r[0] >= 5 for r in runs):
        return "REOPENED", "d = " + ", ".join(str(r[0]) for r in runs) + " (a, b, c with 24 starts)"
    if all(judge(*r)[0] for r in runs):
        return "HOLDS", "all three give d = 4, a clean gap and chord shares at least 0.99"
    return "DOES NOT HOLD", "; ".join(f"{n}: {judge(*r)[1]}" for n, r in zip("abc", runs) if not judge(*r)[0])


def loadj(xdir, name):
    p = os.path.join(xdir, f"{name}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def fmt(v, f="{:.3e}"):
    return "-" if v is None else f.format(v)


def report(logs, xdir):
    R = {lab: parse(os.path.join(logs, f"{lab}.log")) for lab, _, _, _ in RUNS}
    J = {lab: loadj(xdir, lab) for lab, _, _, _ in RUNS}
    print("| run | sample | starts | printed max abs F | bounds printed | m (median of the bounds) | best bound | products per start (min, median, max) | starts at the 250 cap | worst max abs J x - v | start 0 mu share of x |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for lab, st, n, _ in RUNS:
        r = R[lab]
        m = median(r["bounds"][:n]) if len(r["bounds"]) >= n else None
        pr = sorted(r["prods"][:n])
        pstr = f"{pr[0]}, {median([float(x) for x in pr]):.0f}, {pr[-1]}" if pr else "-"
        cap = f"{sum(1 for x in r['prods'][:n] if x >= CAP)} of {len(r['prods'][:n])}"
        worst = f"{max(float(x) for x in r['res'][:n]):.1e}" if r["res"] else "-"
        print(f"| {lab} | {st} | {n} | {r['maxF'] or '-'} | {len(r['bounds'])} | {fmt(m, '{:.4e}')} | {fmt(r['best'], '{:.4e}')} | {pstr} | {cap} | {worst} | {r['mu0'] or '-'} |")
    print("\nSingular values of the x block relative to s_1 (the cutoff is 1e-4):\n")
    print("| run | d | gap s_(d+1)/s_d | s_2 | s_3 | s_4 | s_5 | s_6 | s_7 | s_8 | s_4 / (1e-4 s_1) | s_5 / (1e-4 s_1) | chord shares in span(p_1..p_d) |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for lab, st, n, _ in RUNS:
        j = J[lab]
        if j is None:
            print(f"| {lab} | - | - | - | - | - | - | - | - | - | - | - | - |")
            continue
        s = j["s_over_s1"]
        sh = "; ".join(f"{k} {v:.6f}" for k, v in (j.get("chords") or {}).items()) or "-"
        row = " | ".join(f"{s[i]:.2e}" if i < len(s) else "-" for i in range(1, 8))
        print(f"| {lab} | {j['d']} | {fmt(j['gap'], '{:.2e}')} | {row} | {s[3] / CUT:.3f} | {s[4] / CUT:.2e} | {sh} |")
    print("\nThe bounds of each run, start 0 to 23:\n")
    print("| start | " + " | ".join(lab for lab, _, _, _ in RUNS) + " |\n|---|" + "---|" * len(RUNS))
    for i in range(24):
        print(f"| {i} | " + " | ".join(f"{R[lab]['bounds'][i]:.3e}" if i < len(R[lab]["bounds"]) else "-" for lab, _, _, _ in RUNS) + " |")
    print("\nInformational, against the stored rough logs of the same state:\n")
    for lab, st, n, ref in RUNS:
        print(f"- {lab} against {os.path.relpath(ref, RAW)}: {compare(os.path.join(logs, lab + '.log'), ref, n)[3]}.")
    rs = []
    for lab, st, n, _ in RUNS:
        j = J[lab]
        full = len(R[lab]["bounds"]) >= n
        sh = min((j.get("chords") or {"x": None}).values()) if j and j.get("chords") else None
        rs.append((j["d"], j["gap"], sh) if j and full else None)
    word, why = reading(rs)
    print(f"\nReading by the pre-set acceptance: **(H4) at k = 1/2 and 3/2 {word}** ({why}).")
    return word


def selftest(bad=0):
    def chk(name, got, want):
        nonlocal bad
        good = got == want
        print(f"  {name}: {got} (want {want}) {'ok' if good else 'WRONG'}")
        bad += not good

    G = (4, 1.9e-4, 1.0)
    for name, rs, want in (("all three d 4 clean", [G, G, G], "HOLDS"), ("gap at the bar", [G, (4, 1e-3, 1.0), G], "HOLDS"), ("share at the bar", [G, G, (4, 1.9e-4, 0.99)], "HOLDS"),
                           ("gap just above the bar", [G, (4, 1.1e-3, 1.0), G], "DOES NOT HOLD"), ("share just under", [G, G, (4, 1.9e-4, 0.989)], "DOES NOT HOLD"),
                           ("no gap value", [G, G, (4, None, 1.0)], "DOES NOT HOLD"), ("no share", [G, G, (4, 1.9e-4, None)], "DOES NOT HOLD"),
                           ("d 3 at one", [G, (3, 1e-4, 1.0), G], "REOPENED"), ("d 5 at one", [G, G, (5, 1e-4, 1.0)], "REOPENED"), ("d 7 at one", [(7, 1e-4, 1.0), G, G], "REOPENED"),
                           ("d 2 at one", [G, G, (2, 1e-4, 1.0)], "DOES NOT HOLD"), ("d 1 at one", [(1, 1e-4, 1.0), G, G], "DOES NOT HOLD"),
                           ("d 3 and a failed share", [(3, 1e-4, 0.5), G, G], "REOPENED"), ("incomplete", [G, None, G], "INCOMPLETE"), ("no d", [G, (None, None, None), G], "INCOMPLETE")):
        chk(name, reading(rs)[0], want)
    for nm, a, b, fn, args, want in (("gap bar 1e-3 -> 1e-2 (gap 5e-3)", "gap is not None and gap <= CLEAN", "gap is not None and gap <= 1e-2", "judge", (4, 5e-3, 1.0), (False, True)),
                                     ("share bar 0.99 -> 0.9 (share 0.95)", "share >= SHARE", "share >= 0.9", "judge", (4, 1.9e-4, 0.95), (False, True)),
                                     ("d == 4 -> d >= 4 (d 5 passes judge)", "ok = d == 4 and", "ok = d >= 4 and", "judge", (5, 1.9e-4, 1.0), (False, True)),
                                     ("reopen d >= 5 -> d >= 6 (d 5)", "r[0] == 3 or r[0] >= 5", "r[0] == 3 or r[0] >= 6", "reading", [G, G, (5, 1e-4, 1.0)], ("REOPENED", "DOES NOT HOLD")),
                                     ("reopen d == 3 dropped (d 3)", "r[0] == 3 or r[0] >= 5", "r[0] >= 5", "reading", [G, (3, 1e-4, 1.0), G], ("REOPENED", "DOES NOT HOLD"))):
        mut = open(__file__).read().replace(a, b)
        assert mut != open(__file__).read(), nm
        ns = {"__file__": __file__}
        exec(compile(mut.split("def loadj")[0], "mut", "exec"), ns)
        o, m = (judge(*args)[0], ns["judge"](*args)[0]) if fn == "judge" else (reading(args)[0], ns["reading"](args)[0])
        chk(f"mutated {nm}", (o, m), want)
    with tempfile.TemporaryDirectory() as td:
        ref, a = os.path.join(td, "ref.log"), os.path.join(td, "a.log")
        starts = [f"  start {i}: max|x| {1 + i:.3e}, bound on the smallest gain {1 / (1 + i):.3e}, max|J x - v| 1.0e-17, 67 products" for i in range(48)]
        xs = [f"  start {i}, x / max|x|: mu +1.00e+00; w1 max 4.0e-02" for i in range(48)]
        open(ref, "w").write("H.npz: D 40 32x121 K 0, max|F| 1.0e-30\n  rhs\n" + "\n".join(starts) + "\n" + "\n".join(xs) + "\n  best bound on the smallest gain (max norm) 1e-36; x\n")

        def mk(s, x, tail="  saved x of 24 starts to X.npz\n"):
            open(a, "w", newline="").write("H.npz: D 40 32x121 K 0, max|F| 1.0e-30\r\n  rhs\r\n" + "\r\n".join(s) + "\r\n" + "\r\n".join(x) + "\r\n  best bound on the smallest gain (max norm) 5e-36; y\r\n" + tail)
        mk(starts[:24], xs[:24])
        chk("compare 24 equal (CRLF, other best line, a saved line)", compare(a, ref, 24)[:3], (24, 24, 24))
        s2 = list(starts[:24])
        s2[7] = s2[7].replace("1.0e-17", "2.0e-17")
        mk(s2, xs[:24])
        chk("compare, a residual differs only: every character 23, fields 24", compare(a, ref, 24)[:3], (23, 24, 24))
        s2[9] = s2[9].replace("67 products", "73 products")
        mk(s2, xs[:24])
        chk("compare, a product count differs too: 22 and 23", compare(a, ref, 24)[:2], (22, 23))
        x2 = list(xs[:24])
        x2[20] = x2[20].replace("+1.00e+00", "-1.00e+00")
        mk(starts[:24], x2)
        chk("compare, one x line changed", compare(a, ref, 24)[2], 23)
        mk(starts[:23], xs[:23])
        chk("compare, 23 starts for n = 24", compare(a, ref, 24)[:3], (None, None, None))
        chk("compare, log missing", compare(os.path.join(td, "none.log"), ref, 12)[:3], (None, None, None))
    for lab, st, n, ref in RUNS:
        if os.path.exists(ref):
            chk(f"{lab}'s stored reference against itself on {n} starts", compare(ref, ref, n)[:3], (n, n, n))
    chk("median: geometric mean of the two middle ones for 12", abs(median([float(i) for i in range(1, 13)]) - math.sqrt(42)) < 1e-12, True)
    print("selftest", "FAILED" if bad else "passed")
    return bad


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    logs = sys.argv[sys.argv.index("--logs") + 1] if "--logs" in sys.argv else os.path.join(HERE, "logs")
    xdir = sys.argv[sys.argv.index("--x") + 1] if "--x" in sys.argv else os.path.join(HERE, "x")
    report(logs, xdir)

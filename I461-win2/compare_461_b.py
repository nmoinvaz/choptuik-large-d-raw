#!/usr/bin/env python3
"""I461-win2 part B: the crawl from D 215.03125 with the fixed re-seed (issue #461). Reads the run's log and anm_run.jsonl.

    python -I compare_461_b.py [LOG [JSONL]]        defaults ./crawlB.log and ./crawlB/anm_run.jsonl
        Per attempt (a segment of the log from its "a <a>: re-seeded (...)" line to its closing "a <a> -> D <D>: ..." line):
        the re-seed status ("ok", or FAILED with its rung text), the corrector's start residual (first "on 0" line), the number
        of octo-double Newton steps and its last line ("converged" or not), the elim projection counts, the last line-search
        factor (lam) and whether anm_run.jsonl accepted it.
        Reading rule of the issue: every re-seed line reads "ok" (else the first that does not, with its rung); a step accepted
        past D 215.03125 is reported with its Delta against the degree-5 polynomial through the last six Delta of the crawl
        (delta_all.csv rows 214.7 to 215.03125, Delta_q0..q3 summed in mpmath) and the difference in absolute value; if every
        step is refused, the lines above are the result.
        Exit 0: every re-seed ok and at least one step accepted past D 215.03125. Exit 1: some re-seed not ok, or no step
        accepted (the lines are the result, not an error). Exit 2: a file is missing.
    python -I compare_461_b.py --selftest
        the crawl's own log (every re-seed FAILED) is read as such and its attempts counted; a copy with FAILED turned to ok reads
        ok; an exact polynomial is extrapolated to the digit and a planted change of one Delta is found."""
import csv
import json
import os
import re
import sys

from mpmath import mp, mpf

mp.dps = 60
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
CSV = os.path.join(os.path.dirname(RAW), "choptuik-large-d", "hp", "data", "delta_all.csv")
START = os.path.join(RAW, "I19-win2", "crawl.log")
LAST_D = mpf("215.03125")
SIX = ["214.7", "214.8", "214.9", "215.0", "215.025", "215.03125"]
ATT = re.compile(r"^    a (\S+): re-seeded \((ok|FAILED[^)]*)\), \S+ s(?:; (rung .*))?$")
END = re.compile(r"^    a (\S+) -> D (\S+): predicted")


def segments(lines):
    """[(a, status, rung text, [lines of the attempt])] from the log lines"""
    out, cur = [], None
    for ln in lines:
        m = ATT.match(ln)
        if m:
            cur = [m.group(1), m.group(2), m.group(3) or "", [ln]]
            out.append(cur)
        elif cur is not None:
            cur[3].append(ln)
    return [tuple(c) for c in out]


def describe(a, status, rung, seg):
    on = [ln for ln in seg if re.match(r"^  on \d+:", ln)]
    m0 = re.search(r"\|F\| (\S+)", on[0]) if on else None
    first = m0.group(1) if m0 else "?"
    lams = [m.group(1) for m in (re.search(r"lam (\S+),", ln) for ln in on) if m]
    lam = lams[-1] if lams else "-"
    nt = next((ln.strip() for ln in seg if "octo-double Newton:" in ln), "no octo-double Newton line")
    pr = next((ln.strip() for ln in seg if "elim projections" in ln), "no projection line")
    end = next((END.match(ln) for ln in seg if END.match(ln)), None)
    return (f"a {a} (-> D {end.group(2) if end else '?'}): re-seed {status}{' ' + rung if rung else ''}; start |F| {first}, {len(on)} corrector iterations, "
            f"last lam {lam}\n    {nt}\n    {pr}")


def sum_q(row): return sum(mpf(row[k]) for k in ("Delta_q0", "Delta_q1", "Delta_q2", "Delta_q3"))


def chain_six(path):
    with open(path, encoding="utf-8") as f:
        rows = {r["D"]: r for r in csv.DictReader(f)}
    return [(mpf(d), sum_q(rows[d])) for d in SIX]


def extrapolate(pts, D):
    """the polynomial of degree len(pts) - 1 through pts, evaluated at D (Lagrange form)"""
    s = mpf(0)
    for i, (xi, yi) in enumerate(pts):
        w = mpf(1)
        for j, (xj, _) in enumerate(pts):
            if j != i:
                w *= (D - xj) / (xi - xj)
        s += w * yi
    return s


def run(log, jsonl, csv_path=CSV, out=print):
    for p in (log, jsonl, csv_path):
        if not os.path.exists(p):
            out(f"MISSING {p}")
            return 2
    lines = [ln.rstrip("\n") for ln in open(log, encoding="utf-8")]
    segs = segments(lines)
    recs = [json.loads(ln) for ln in open(jsonl, encoding="utf-8") if ln.strip()]
    acc = [(a["D_str"], a["Delta"], a["a"]) for r in recs for a in r["attempts"] if a["accepted"]]
    out(f"{len(segs)} attempts in the log, {len(acc)} accepted steps in anm_run.jsonl")
    allok = bool(segs) and all(s[1] == "ok" for s in segs)
    for a, status, rung, seg in segs:
        out(describe(a, status, rung, seg))
    bad = next((s for s in segs if s[1] != "ok"), None)
    out("re-seed lines: all ok" if allok else (f"re-seed lines: first not ok, a {bad[0]}: {bad[1]} {bad[2]}" if bad else "no attempt in the log"))
    pts = chain_six(csv_path)
    past = [(mpf(D), d, a) for D, d, a in acc if mpf(D) > LAST_D + mpf("1e-9")]
    for D, d, a in past:
        e = extrapolate(pts, D)
        out(f"accepted past D 215.03125: D {mp.nstr(D, 12)} (a {a}), Delta {d!r}, degree-5 extrapolation of the last six {mp.nstr(e, 18)}, |difference| {mp.nstr(abs(mpf(d) - e), 3)}")
    stop = [ln for ln in lines if ln.startswith("stopped:")]
    out("the run ended by its own line: " + stop[0] if stop else "no stop line in the log")
    ok = allok and bool(past)
    out("RE-SEEDS OK AND A STEP PAST D 215.03125 ACCEPTED" if ok else "NOT (all re-seeds ok and a step accepted past D 215.03125): the lines above are the result")
    return 0 if ok else 1


def selftest():
    import tempfile
    fails = []
    lines = [ln.rstrip("\n") for ln in open(START, encoding="utf-8")]
    segs = segments(lines)
    n_att = sum(1 for ln in lines if ATT.match(ln))
    if len(segs) != n_att or n_att < 8 or any(s[1] == "ok" for s in segs) or not all(s[1].startswith("FAILED") for s in segs):
        fails.append(f"the crawl's own log: {len(segs)} segments, {n_att} attempt lines, statuses {sorted(set(s[1] for s in segs))}")
    ok_lines = [ln.replace("(FAILED, prediction kept)", "(ok)") for ln in lines]
    if any(s[1] != "ok" for s in segments(ok_lines)):
        fails.append("a copy with FAILED turned to ok did not read ok")
    pts = [(mpf(x), mpf(3) + 2 * mpf(x) - mpf(x) ** 3 / 7 + mpf(x) ** 5 / 1000) for x in ("1", "2", "3", "4", "5", "6")]
    xx = mpf("6.5")
    exact = mpf(3) + 2 * xx - xx ** 3 / 7 + xx ** 5 / 1000
    if abs(extrapolate(pts, xx) - exact) > mpf("1e-50"):
        fails.append("a degree-5 polynomial was not extrapolated exactly")
    bad = list(pts); bad[2] = (bad[2][0], bad[2][1] + mpf("1e-9"))
    if abs(extrapolate(bad, xx) - exact) < mpf("1e-12"):
        fails.append("a planted change of one Delta was not found")
    with tempfile.TemporaryDirectory() as td:
        lg = os.path.join(td, "l.log"); open(lg, "w", encoding="utf-8").write("\n".join(ok_lines) + "\n")
        sink = []
        rc = run(lg, os.path.join(RAW, "I19-win2", "crawl", "anm_run.jsonl"), out=sink.append)
        if rc != 1 or not any("accepted past" not in s for s in sink):
            fails.append(f"the crawl's data with ok re-seeds but no step past 215.03125 should exit 1: rc {rc}")
    print("selftest: ok" if not fails else "selftest FAILED:\n  " + "\n  ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(run(*(args + [os.path.join(HERE, "crawlB.log"), os.path.join(HERE, "crawlB", "anm_run.jsonl")][len(args):])))

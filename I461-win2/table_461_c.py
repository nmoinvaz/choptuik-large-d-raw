#!/usr/bin/env python3
"""I461-win2 parts B2 and B3: the accepted steps of the crawls as a table, and events for the watcher (issue #461).

    python -I table_461_c.py table [--from K] LOG JSONL [LOG JSONL ...]
        markdown table of the accepted steps (the K-th on, default all) of one or more runs in order: D, step size a, the corrector's start
        residual, Newton steps, final max|F|, whether it converged with lam 1 at every step, Delta (the four parts of the step's saved state,
        summed exactly in mpmath as hp/export_delta_all.py does; the log's line if the state is missing) and Delta minus the degree-5 polynomial through the six Delta before it (the crawl's delta_all.csv rows 214.7 to 215.03125,
        Delta_q0..q3 summed, then the accepted steps of the runs in order).
    python -I table_461_c.py events [--quiet] STATE LOG JSONL
        (--quiet: only the flagged accepted steps and the first re-seed that is not ok, the rest are counted) prints what is new since the last call (STATE is a small json file the call keeps): every accepted step with the flags FIRST ACCEPTED
        STEP and NOT CONVERGED AT LAM 1, every re-seed line that does not read ok (status, rung, residual), the stop line. Exit 0 always.
    python -I table_461_c.py --selftest
        the original crawl's own log and anm_run.jsonl are read the same way and each accepted step's Delta is compared with its row of
        delta_all.csv (it must agree to 1e-30), a planted change of one digit is found, an exact polynomial is extrapolated to the digit,
        and a copy of crawlB.log (part B, every step refused) yields no accepted step."""
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
SIX = ["214.7", "214.8", "214.9", "215.0", "215.025", "215.03125"]
ATT = re.compile(r"^    a (\S+): re-seeded \((ok|FAILED[^)]*)\), \S+ s(?:; (rung .*))?$")
END = re.compile(r"^    a (\S+) -> D (\S+): predicted")
ON = re.compile(r"^  on (\d+): \|F\| (\S+)")
CONV = re.compile(r"^  on \d+: \|F\| \S+ converged, Delta (\S+) (\S+)$")
NEWT = re.compile(r"octo-double Newton: (\d+) steps, max\|F\| (\S+), (converged|not converged)")


def segments(lines):
    """one dict per attempt of the log, in order"""
    out, cur, series = [], None, ""
    for ln in lines:
        if ln.startswith("step "):
            series = ln
        m = ATT.match(ln)
        if m:
            cur = dict(a=m.group(1), status=m.group(2), rung=m.group(3) or "", on=[], conv=None, newton=None, end=None, proj="", series=series, lines=[ln])
            out.append(cur)
            continue
        if cur is None:
            continue
        cur["lines"].append(ln)
        if ON.match(ln):
            cur["on"].append(ln)
        c = CONV.match(ln)
        if c:
            cur["conv"] = c.groups()
        n = NEWT.search(ln)
        if n:
            cur["newton"] = (int(n.group(1)), n.group(2), n.group(3) == "converged")
        if "elim projections" in ln:
            cur["proj"] = ln.strip().replace("elim projections ", "")
        e = END.match(ln)
        if e:
            cur["end"] = e.group(2)
    return out


def info(seg):
    """start residual, lam list, whether all lam are 1, final max|F|, Newton steps, converged, Delta (mpf or None)"""
    first = ON.match(seg["on"][0]).group(2) if seg["on"] else "?"
    m1 = re.search(r"\|F\| \S+ -> (\S+?),", seg["on"][0]) if seg["on"] else None
    after1 = m1.group(1) if m1 else "?"
    lams = [float(m.group(1)) for m in (re.search(r"lam (\S+),", ln) for ln in seg["on"]) if m]
    n = seg["newton"]
    delta = mpf(seg["conv"][0]) + mpf(seg["conv"][1]) if seg["conv"] else None
    pv = re.search(r"pivots (\S+?)\.\.(\S+?),", seg.get("series", ""))
    pivots = f"{pv.group(1)}..{pv.group(2)}" if pv else "?"
    lamtxt = " ".join(m.group(1) for m in (re.search(r"lam (\S+),", ln) for ln in seg["on"]) if m)
    return dict(start=first, after1=after1, pivots=pivots, lamtxt=lamtxt, lams=lams, lam1=bool(lams) and all(x == 1 for x in lams), steps=n[0] if n else None, final=n[1] if n else "?",
                conv=bool(n and n[2]), delta=delta)


def load(log, jsonl):
    """(segments, flat jsonl attempts with their record) for a run"""
    lines = [ln.rstrip("\n") for ln in open(log, encoding="utf-8")]
    recs = [json.loads(ln) for ln in open(jsonl, encoding="utf-8") if ln.strip()] if os.path.exists(jsonl) else []
    flat = [(r, a) for r in recs for a in r["attempts"]]
    segs = segments(lines)
    stop = next((ln for ln in lines if ln.startswith("stopped:")), None)
    return segs, flat, stop, lines


def accepted(log, jsonl):
    """[dict(D, a, start, steps, final, conv, lam1, delta, seg)] for the accepted steps; raises if the log and jsonl disagree"""
    segs, flat, _, _ = load(log, jsonl)
    out = []
    for i, (r, a) in enumerate(flat):
        if i >= len(segs) or abs(float(segs[i]["a"]) - a["a"]) > 0.05 * a["a"]:
            raise ValueError(f"attempt {i} of {jsonl} (a {a['a']}) does not match the log's attempt (a {segs[i]['a'] if i < len(segs) else '-'})")
        if a["accepted"]:
            inf = info(segs[i])
            if inf["steps"] is None:
                # the log lines of this attempt are lost (crawlB4.log was replaced under its run at 17:12:27 UTC); use what anm_run.jsonl keeps
                inf.update(steps=a["steps"], lamtxt="(log lines lost)", final="?", conv=bool(r.get("converged", False)), lam1=True)
            sd = state_delta(os.path.dirname(os.path.abspath(jsonl)), a["D"])
            out.append(dict(D=mpf(a["D_str"]), a=a["a"], seg=segs[i], **{**inf, "delta_log": inf["delta"], "delta": sd if sd is not None else inf["delta"],
                                                                          "from_state": sd is not None}))
    return out


def total(parts):
    """the exact sum of the parts (f64 values or their repr strings; empty parts are 0), in mpmath, as hp/export_delta_all.py does"""
    return sum((mpf(float(p)) for p in parts if p != ""), mpf(0))


def sum_q(row): return total([row[k] for k in ("Delta_q0", "Delta_q1", "Delta_q2", "Delta_q3")])


def state_delta(folder, D):
    """the exact Delta of the saved state of the folder whose meta D is D (the last entry of zh, zl, z2, z3 summed), or None"""
    import glob
    import numpy as np
    for p in glob.glob(os.path.join(folder, "anm_pin3_D*.npz")):
        z = np.load(p)
        if abs(json.loads(str(z["meta"]))["D"] - float(D)) < 1e-9:
            return total([z[k][-1] for k in ("zh", "zl", "z2", "z3") if k in z.files])
    return None


def chain_six(path=CSV):
    with open(path, encoding="utf-8") as f:
        rows = {r["D"]: r for r in csv.DictReader(f)}
    return [(mpf(d), sum_q(rows[d])) for d in SIX]


def extrapolate(pts, D):
    s = mpf(0)
    for i, (xi, yi) in enumerate(pts):
        w = mpf(1)
        for j, (xj, _) in enumerate(pts):
            if j != i:
                w *= (D - xj) / (xi - xj)
        s += w * yi
    return s


def table(runs, frm=1, out=print, csv_path=CSV):
    pts = chain_six(csv_path)
    rows = []
    for log, jsonl in runs:
        for s in accepted(log, jsonl):
            d = s["delta"] if s["delta"] is not None else None
            e = extrapolate(pts[-6:], s["D"])
            rows.append((s, d, e))
            if d is not None:
                pts.append((s["D"], d))
    out("| step | D | a | smallest..largest pivot of the base | start residual | max\\|F\\| after the first Newton step | Newton steps | lam per iteration | final residual "
        "| converged, lam 1 | Delta | Delta minus degree-5 extrapolation |")
    out("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k, (s, d, e) in enumerate(rows, 1):
        if k < frm:
            continue
        ok = "yes" if s["conv"] and s["lam1"] else ("NO, converged" if s["conv"] else "NO, not converged")
        dd = mp.nstr(d, 18) if d is not None else "-"
        df = mp.nstr(d - e, 3) if d is not None else "-"
        out(f"| {k} | {mp.nstr(s['D'], 12)} | {s['a']:g} | {s['pivots']} | {s['start']} | {s['after1']} | {s['steps']} | {s['lamtxt']} | {s['final']} | {ok} | {dd} | {df} |")
    return len(rows)


# the runs whose accepted steps come before a run's own in the Delta sequence of its extrapolations (crawlB3 starts from crawlB2's step)
PRIOR = {"crawlB3": [("crawlB2.log", "crawlB2/anm_run.jsonl")],
         "crawlB4": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl")],
         "crawlB5": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl")]}
NEWTON_FLAG = 25      # the coordinator's order of 15:49 UTC: report at once the first step that needs more than this many Newton steps
SERIES = re.compile(r"^step (\d+): D (\S+), pivots (\S+?)\.\.(\S+?), \|z_1\| \S+, \|z_N\| (\S+), ratios 2-5 (.*), a_max (\S+),")


def events(state_path, log, jsonl, out=print, csv_path=CSV, quiet=False):
    st = dict(acc=0, reseed=0, stop=False, ended=False, notok=0, ref=0)
    if os.path.exists(state_path):
        st.update(json.load(open(state_path, encoding="utf-8")))
    segs, flat, stop, lines = load(log, jsonl)
    nref = 0
    for i, (r, a) in enumerate(flat):
        if a["accepted"]:
            continue
        nref += 1
        if nref > st["ref"] and i < len(segs):
            n = segs[i]["newton"]
            tail = " | ".join(re.sub(r"^on (\d+): \|F\| (\S+) -> (\S+), \|dz\| \S+ -> \S+, lam (\S+),.*$", r"on \1 |F| \2->\3 lam \4", ln.strip()).replace(": no trial step accepted, stopping", " no trial step")
                              for ln in segs[i]["on"][-4:])
            out(f"REFUSED attempt a {a['a']:g} to D {a['D_str'][:12]} (a halving follows): {n[0] if n else '?'} Newton steps, max|F| {n[1] if n else '?'}, not converged; "
                f"last iterations: {tail}")
    st["ref"] = nref
    for j in range(st["reseed"], len(segs)):
        s = segs[j]
        if s["status"] != "ok":
            st["notok"] += 1
            if not quiet or st["notok"] == 1:
                out(f"RE-SEED NOT OK ({st['notok']}. so far), attempt a {s['a']} (the run goes on): {s['status']} {s['rung']}")
    st["reseed"] = len(segs)
    acc = accepted(log, jsonl)
    pts = chain_six(csv_path)
    for pl, pj in PRIOR.get(os.path.basename(os.path.dirname(os.path.abspath(jsonl))), []):
        for s in accepted(os.path.join(os.path.dirname(os.path.abspath(jsonl)), "..", pl), os.path.join(os.path.dirname(os.path.abspath(jsonl)), "..", pj)):
            if s["delta"] is not None:
                pts.append((s["D"], s["delta"]))
    for k, s in enumerate(acc):
        e = extrapolate(pts[-6:], s["D"])
        if s["delta"] is not None:
            pts.append((s["D"], s["delta"]))
        if k < st["acc"]:
            continue
        flags = []
        if k == 0:
            flags.append("FIRST ACCEPTED STEP OF THIS RUN")
        if s["steps"] is not None and s["steps"] > NEWTON_FLAG:
            flags.append(f"MORE THAN {NEWTON_FLAG} NEWTON STEPS ({s['steps']})")
        if not s["conv"]:
            flags.append("ACCEPTED WITH A CORRECTOR THAT DID NOT CONVERGE")
        elif not s["lam1"] and not quiet:
            flags.append("NOT CONVERGED AT LAM 1")
        diff = mp.nstr(s["delta"] - e, 3) if s["delta"] is not None else "-"
        if quiet and not flags:
            continue
        out(f"ACCEPTED step {k + 1}: D {mp.nstr(s['D'], 12)}, a {s['a']:g}, start {s['start']}, {s['steps']} Newton steps, final {s['final']}, "
            f"Delta {mp.nstr(s['delta'], 18) if s['delta'] is not None else '-'}, minus extrapolation {diff}" + ("  <<< " + "; ".join(flags) if flags else ""))
    st["acc"] = len(acc)
    ser = [m for m in (SERIES.match(ln) for ln in lines) if m]
    for m in ser[st.get("ser", 0):]:
        zN, amax = float(m.group(5)), float(m.group(7))
        if zN >= 1e-27 or amax <= 3:
            out(f"SERIES RULE BROKEN at the base of step {m.group(1)} (D {m.group(2)}): |z_N| {m.group(5)} (must be below 1e-27), a_max {m.group(7)} (must be above 3), "
                f"pivots {m.group(3)}..{m.group(4)}, ratios 2-5 {m.group(6)}: stop and report")
        elif amax < 3.15 and not st.get("amax_warned"):
            out(f"SERIES WATCH: a_max {m.group(7)} at the base of step {m.group(1)} (D {m.group(2)}), the rule stops the run at 3")
            st["amax_warned"] = True
    st["ser"] = len(ser)
    if stop and not st["stop"]:
        out("STOP: " + stop)
        st["stop"] = True
    if any(ln == "done" for ln in lines) and not st["ended"]:
        out("RUN PRINTED done")
        st["ended"] = True
    json.dump(st, open(state_path, "w", encoding="utf-8"))
    return 0


def selftest():
    import tempfile
    fails = []
    pts = [(mpf(x), mpf(3) + 2 * mpf(x) - mpf(x) ** 3 / 7 + mpf(x) ** 5 / 1000) for x in ("1", "2", "3", "4", "5", "6")]
    xx = mpf("6.5")
    if abs(extrapolate(pts, xx) - (mpf(3) + 2 * xx - xx ** 3 / 7 + xx ** 5 / 1000)) > mpf("1e-50"):
        fails.append("a degree-5 polynomial was not extrapolated exactly")
    log = os.path.join(RAW, "I19-win2", "crawl.log")
    jsonl = os.path.join(RAW, "I19-win2", "crawl", "anm_run.jsonl")
    with open(CSV, encoding="utf-8") as f:
        rows = {round(float(r["D"]), 6): r for r in csv.DictReader(f) if r["source"].startswith("I19-win2/crawl/")}
    acc = accepted(log, jsonl)
    bad = [(mp.nstr(s["D"], 10)) for s in acc if round(float(s["D"]), 6) in rows and s["delta"] is not None
           and abs(s["delta"] - sum_q(rows[round(float(s["D"]), 6)])) > mpf("1e-40")]
    hit = sum(1 for s in acc if round(float(s["D"]), 6) in rows)
    nst = sum(1 for s in acc if s["from_state"])
    badl = [(mp.nstr(s["D"], 10)) for s in acc if round(float(s["D"]), 6) in rows and s["delta_log"] is not None
            and abs(s["delta_log"] - sum_q(rows[round(float(s["D"]), 6)])) > mpf("2e-17")]
    if hit < 5 or bad or badl or nst < hit:
        fails.append(f"the crawl's accepted steps against delta_all.csv: {hit} matched rows, {nst} read from their state, state Delta disagreeing at {bad}, log Delta (limit 2e-17) at {badl}")
    # a planted change of one digit in a Delta line must be found
    lines = [ln.rstrip("\n") for ln in open(log, encoding="utf-8")]
    k = next(i for i, ln in enumerate(lines) if CONV.match(ln))
    g = CONV.match(lines[k]).groups()
    lines[k] = lines[k].replace(g[0], g[0][:-3] + ("7" if g[0][-3] != "7" else "8") + g[0][-2:])
    with tempfile.TemporaryDirectory() as td:
        lg = os.path.join(td, "l.log")
        open(lg, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        acc2 = accepted(lg, jsonl)
        bad2 = [s for s in acc2 if round(float(s["D"]), 6) in rows and s["delta_log"] is not None
                and abs(s["delta_log"] - sum_q(rows[round(float(s["D"]), 6)])) > mpf("2e-17")]
        if not bad2:
            fails.append("a planted change of one digit in a Delta line was not found")
        sink = []
        events(os.path.join(td, "st.json"), log, jsonl, out=sink.append)
        if not any(x.startswith("ACCEPTED step 1") and "FIRST ACCEPTED STEP" in x for x in sink) or not any(x.startswith("RE-SEED NOT OK") for x in sink):
            fails.append("events on the crawl's log did not report a first accepted step and the failed re-seeds")
        if not any(x.startswith("REFUSED attempt") and "Newton steps" in x and "\n" not in x for x in sink):
            fails.append("events on the crawl's log did not report a refused attempt with its Newton lines")
        sink2 = []
        events(os.path.join(td, "st.json"), log, jsonl, out=sink2.append)
        if any(x.startswith("ACCEPTED") or x.startswith("RE-SEED") for x in sink2):
            fails.append("a second call reported the same events again")
        # part B: no step accepted, all four re-seeds ok
        logb, jsb = os.path.join(HERE, "crawlB.log"), os.path.join(HERE, "crawlB", "anm_run.jsonl")
        if os.path.exists(logb) and accepted(logb, jsb):
            fails.append("part B's log, in which every step was refused, gave an accepted step")
    print("selftest: ok" if not fails else "selftest FAILED:\n  " + "\n  ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if a and a[0] == "table":
        frm = 1
        rest = a[1:]
        if rest and rest[0] == "--from":
            frm, rest = int(rest[1]), rest[2:]
        sys.exit(0 if table(list(zip(rest[0::2], rest[1::2])), frm) >= 0 else 1)
    if a and a[0] == "events":
        q = "--quiet" in a
        r = [x for x in a[1:] if x != "--quiet"]
        if len(r) == 3:
            sys.exit(events(r[0], r[1], r[2], quiet=q))
    print(__doc__)
    sys.exit(2)

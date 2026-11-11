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
        h = HOR.match(ln)
        if h:
            cur["hor"] = h.group(1).split("->")[-1].strip()
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
    sm = SERIES.match(seg.get("series", ""))
    zN, ratios, amax = (sm.group(5), sm.group(6), sm.group(7)) if sm else ("?", "?", "?")
    dzs = [(m.group(1), m.group(2)) for m in (re.search(r"\|dz\| (\S+) -> (\S+?),", ln) for ln in seg["on"]) if m]
    dz0 = dzs[0][0] if dzs else "?"
    dzc = next((x for x, y in dzs if float(y) < 0.1 * float(x)), "-")  # |dz| entering the first iteration that shrinks it by more than 10
    return dict(start=first, after1=after1, pivots=pivots, zN=zN, ratios=ratios, amax=amax, dz0=dz0, dzc=dzc, lamtxt=lamtxt, lams=lams, lam1=bool(lams) and all(x == 1 for x in lams), steps=n[0] if n else None, final=n[1] if n else "?",
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
                                                                          "from_state": sd is not None, "idx": i}))
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
    out("| step | D | a | smallest..largest pivot of the base | \\|z_N\\| of the base | ratios 2-5 of the base | a_max | start residual | first \\|dz\\| | \\|dz\\| where the collapse starts "
        "| max\\|F\\| after the first Newton step | Newton steps | lam 0.5 iterations | lam per iteration | final residual | converged, lam 1 | Delta | Delta minus degree-5 extrapolation |")
    out("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for k, (s, d, e) in enumerate(rows, 1):
        if k < frm:
            continue
        ok = "yes" if s["conv"] and s["lam1"] else ("NO, converged" if s["conv"] else "NO, not converged")
        dd = mp.nstr(d, 18) if d is not None else "-"
        df = mp.nstr(d - e, 3) if d is not None else "-"
        out(f"| {k} | {mp.nstr(s['D'], 12)} | {s['a']:g} | {s['pivots']} | {s['zN']} | {s['ratios']} | {s['amax']} | {s['start']} | {s['dz0']} | {s['dzc']} | {s['after1']} | "
            f"{s['steps']} | {sum(1 for x in s['lams'] if x == 0.5)} | {s['lamtxt']} | {s['final']} | {ok} | {dd} | {df} |")
    return len(rows)


# the runs whose accepted steps come before a run's own in the Delta sequence of its extrapolations (crawlB3 starts from crawlB2's step)
PRIOR = {"crawlB3": [("crawlB2.log", "crawlB2/anm_run.jsonl")],
         "crawlB4": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl")],
         "crawlB5": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl")],
         "crawlC": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl"),
                    ("crawlB5.log", "crawlB5/anm_run.jsonl")],
         "crawlD": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl"),
                    ("crawlB5.log", "crawlB5/anm_run.jsonl"), ("crawlC.log", "crawlC/anm_run.jsonl")],
         "crawlE": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl"),
                    ("crawlB5.log", "crawlB5/anm_run.jsonl"), ("crawlC.log", "crawlC/anm_run.jsonl"), ("crawlD.log", "crawlD/anm_run.jsonl")],
         "crawlF": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl"),
                    ("crawlB5.log", "crawlB5/anm_run.jsonl"), ("crawlC.log", "crawlC/anm_run.jsonl"), ("crawlD.log", "crawlD/anm_run.jsonl"),
                    ("crawlE.log", "crawlE/anm_run.jsonl")],
         "crawlG": [("crawlB2.log", "crawlB2/anm_run.jsonl")],
         "crawlH": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlG.log", "crawlG/anm_run.jsonl")],
         "crawlI": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlG.log", "crawlG/anm_run.jsonl"), ("crawlH.log", "crawlH/anm_run.jsonl")],
         "crawlJ": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlG.log", "crawlG/anm_run.jsonl"), ("crawlI.log", "crawlI/anm_run.jsonl")],
         "crawlK": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlG.log", "crawlG/anm_run.jsonl"), ("crawlI.log", "crawlI/anm_run.jsonl"), ("crawlJ.log", "crawlJ/anm_run.jsonl")],
         "crawlD2": [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl"),
                     ("crawlB5.log", "crawlB5/anm_run.jsonl"), ("crawlC.log", "crawlC/anm_run.jsonl"), ("crawlD.log", "crawlD/anm_run.jsonl")]}
NEWTON_FLAG = 25      # the coordinator's order of 21:02 UTC (crawlF, a 0.35): report at once a step that needs more than this many Newton steps (and a lam below LAM_FLAG)
LAM_FLAG = 0.25
STALL_LINE = "lam at or below 0.04 twice in a row, stopping (stalled)"


def step_rule_problems(recs, hmax=0.5, grow=1.25):
    """the coordinator's step rule of crawlI (--a_grow 1.25 --a_hold 1): the first attempt of each step is the step kept after a halved step, 1.25 times the previous step after a
    step accepted at its first attempt, never above h_max and a_max; problems are returned as text (the first step of the run is not checked)"""
    out, prev = [], None
    for r in recs:
        att = r["attempts"]
        first = att[0]["a"]
        if prev is not None:
            a_prev, idx = prev
            want = min(a_prev * grow if idx == 0 else a_prev, hmax, r.get("a_max", hmax))
            if abs(first - want) > 1e-6 * max(want, 1e-9):
                out.append(f"step {r['step']} (D {r['D0']:.5f}): first attempt a {first:g}, the rule gives {want:g} (previous step {a_prev:g}, accepted at attempt {idx})")
        acc = next((i for i, x in enumerate(att) if x["accepted"]), None)
        if acc is not None:
            prev = (att[acc]["a"], acc)
    return out


def stall_problems(segs):
    """a stalled attempt (two Newton steps in a row at lam <= 0.04) must end with STALL_LINE within 3 iterations of its start"""
    out = []
    for s in segs:
        lams = [float(m.group(1)) for m in (re.search(r"lam (\S+),", ln) for ln in s["on"]) if m]
        j = next((i for i in range(len(lams) - 1) if lams[i] <= 0.04 and lams[i + 1] <= 0.04), None)
        has = any(STALL_LINE in ln for ln in s["lines"])
        if j is not None and not has and s["end"] is not None:
            out.append(f"attempt a {s['a']}: lam at or below 0.04 twice in a row from iteration {j} and no '{STALL_LINE}' line")
        if has:
            n_on = len(s["on"])
            if n_on > 4:
                out.append(f"attempt a {s['a']}: the stall line comes after {n_on} Newton iterations (more than 3 after its start)")
    return out


if os.environ.get("EVENTS_PROFILE") == "G":   # crawlG's reading rule of 21:31 UTC: report at once more than 6 Newton steps, any lam below 1, any refusal, series |z_N| above 1e-27 or fourth ratio below 100
    NEWTON_FLAG, LAM_FLAG = 6, 1.0
Z_N_MAX, A_MAX_MIN, A_MAX_WARN = 1e-24, 2.0, 2.5   # the coordinator's series rule of 19:52 UTC: stop above/below the first two, warn once under the third
HOR = re.compile(r"^\s*horizon data refined in octo-double, rung max\|R\| (.*)$")   # the log indents this line by 6 spaces
SERIES = re.compile(r"^step (\d+): D (\S+), pivots (\S+?)\.\.(\S+?), \|z_1\| \S+, \|z_N\| (\S+), ratios 2-5 (.*), a_max (\S+),")


def events(state_path, log, jsonl, out=print, csv_path=CSV, quiet=False):
    st = dict(acc=0, reseed=0, stop=False, ended=False, notok=0, ref=0)
    if os.path.exists(state_path):
        st.update(json.load(open(state_path, encoding="utf-8")))
    segs, flat, stop, lines = load(log, jsonl)
    if os.environ.get("EVENTS_PROFILE") in ("I", "J", "K"):
        recs_i = [json.loads(ln) for ln in open(jsonl, encoding="utf-8") if ln.strip()] if os.path.exists(jsonl) else []
        seen = set(st.get("rule_seen", []))
        for p in step_rule_problems(recs_i, hmax=1.0 if os.environ.get("EVENTS_PROFILE") == "J" else 0.5) + stall_problems(segs):
            if p not in seen:
                out("CRAWLI RULE NOT FOLLOWED (stop and tell the coordinator): " + p)
                seen.add(p)
        st["rule_seen"] = sorted(seen)
    nref = 0
    for i, (r, a) in enumerate(flat):
        if a["accepted"]:
            continue
        nref += 1
        if nref > st["ref"] and i < len(segs):
            n = segs[i]["newton"]
            tail = " | ".join(re.sub(r"^on (\d+): \|F\| (\S+) -> (\S+), \|dz\| \S+ -> \S+, lam (\S+),.*$", r"on \1 |F| \2->\3 lam \4", ln.strip()).replace(": no trial step accepted, stopping", " no trial step")
                              for ln in segs[i]["on"][-4:])
            xr = dict(D=mpf(a["D_str"]), a=a["a"], seg=segs[i], **info(segs[i]))
            out(step_line(xr, refused=True))
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
        if os.environ.get("EVENTS_PROFILE") in ("I", "J", "K"):
            try:
                if float(s["final"]) >= 1e-60:
                    flags.append(f"FINAL RESIDUAL {s['final']} IS NOT BELOW 1e-60 (--tol_od 1e-60)")
            except ValueError:
                pass
        if s["lams"] and min(s["lams"]) < LAM_FLAG:
            flags.append(f"A LAM BELOW {LAM_FLAG:g} ({min(s['lams']):g})")
        if not s["conv"]:
            flags.append("ACCEPTED WITH A CORRECTOR THAT DID NOT CONVERGE")
        elif not s["lam1"] and not quiet:
            flags.append("NOT CONVERGED AT LAM 1")
        diff = mp.nstr(s["delta"] - e, 3) if s["delta"] is not None else "-"
        # the coordinator's verdicts of 2026-11-11 01:06 UTC: a BAD step or base is sent at once, a WATCH one is left to the hourly table
        sm_ = SERIES.match(s["seg"].get("series", ""))
        d0_ = sm_.group(2) if sm_ else "?"
        vline, worst = verdict_line("step", f"{k + 1} D {d0_} -> {mp.nstr(s['D'], 9)} (a {s['a']:g})", step_verdicts(s, (s["delta"] - e) if s["delta"] is not None else None))
        bline, bworst = verdict_line("base", f"D {d0_}", base_verdicts(s))
        if worst == "BAD" or bworst == "BAD":
            out(step_line(s))      # the coordinator's step line of 01:11 UTC, a ✗ in it is sent at once
        if quiet and not flags:
            continue
        out(f"ACCEPTED step {k + 1}: D {mp.nstr(s['D'], 12)}, a {s['a']:g}, start {s['start']}, {s['steps']} Newton steps, final {s['final']}, "
            f"Delta {mp.nstr(s['delta'], 18) if s['delta'] is not None else '-'}, minus extrapolation {diff}" + ("  <<< " + "; ".join(flags) if flags else ""))
    st["acc"] = len(acc)
    ser = [m for m in (SERIES.match(ln) for ln in lines) if m]
    for m in ser[st.get("ser", 0):]:
        zN, amax = float(m.group(5)), float(m.group(7))
        r4 = float(m.group(6).split()[-1])
        if os.environ.get("EVENTS_PROFILE") == "G" and (zN > 1e-27 or r4 < 100):
            out(f"SERIES REPORT at the base of step {m.group(1)} (D {m.group(2)}): |z_N| {m.group(5)}{' (above 1e-27)' if zN > 1e-27 else ''}, "
                f"ratios 2-5 {m.group(6)}{' (fourth below 100)' if r4 < 100 else ''}, a_max {m.group(7)}, pivots {m.group(3)}..{m.group(4)}")
        if zN > Z_N_MAX or amax < A_MAX_MIN:
            out(f"SERIES RULE BROKEN at the base of step {m.group(1)} (D {m.group(2)}): |z_N| {m.group(5)} (must be below {Z_N_MAX:g}), a_max {m.group(7)} (must be above {A_MAX_MIN:g}), "
                f"pivots {m.group(3)}..{m.group(4)}, ratios 2-5 {m.group(6)}: stop and report")
        elif amax < A_MAX_WARN and not st.get("amax_warned"):
            out(f"SERIES WARNING: a_max {m.group(7)} at the base of step {m.group(1)} (D {m.group(2)}) is under {A_MAX_WARN:g} (the run stops at {A_MAX_MIN:g}); the coordinator lowers h_max")
            st["amax_warned"] = True
    st["ser"] = len(ser)
    hor = [m for m in (HOR.match(ln) for ln in lines) if m]
    for m in hor[st.get("hor", 0):]:
        last = m.group(1).split("->")[-1].strip()
        try:
            bad = float(last) >= 1e-50
        except ValueError:
            bad = True
        if bad:
            out(f"HORIZON REFINEMENT BOUND BROKEN: rung max|R| {m.group(1)} (the last number must be below 1e-50)")
    st["hor"] = len(hor)
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
        # the crawlI step rule must be able to fail: a kept step, a 1.25 growth, a wrong first attempt, and a stall line missing
        mk = lambda step, D0, atts, amax=9.0: dict(step=step, D0=D0, a_max=amax, attempts=[dict(a=x, accepted=ok) for x, ok in atts])
        good = [mk(0, 1.0, [(0.5, False), (0.25, True)]), mk(1, 1.25, [(0.25, True)]), mk(2, 1.5, [(0.3125, True)]), mk(3, 1.8, [(0.390625, True)])]
        if step_rule_problems(good):
            fails.append("the crawlI step rule flags a correct sequence: " + "; ".join(step_rule_problems(good)))
        bad = [mk(0, 1.0, [(0.5, False), (0.25, True)]), mk(1, 1.25, [(0.5, True)])]
        if not step_rule_problems(bad):
            fails.append("the crawlI step rule did not flag a first attempt of 0.5 after a halved step of 0.25")
        bad2 = [mk(0, 1.0, [(0.2, True)]), mk(1, 1.2, [(0.2, True)])]
        if not step_rule_problems(bad2):
            fails.append("the crawlI step rule did not flag a first attempt that did not grow 1.25 times after a first-attempt step")
        seg = dict(a="0.5", on=["  on 0: |F| 1e-30 -> 2e-30, |dz| 1e-27 -> 1e-27, lam 0.03, x", "  on 1: |F| 2e-30 -> 2e-30, |dz| 1e-27 -> 1e-27, lam 0.02, x"], lines=["a", "b"], end="D")
        if not stall_problems([seg]):
            fails.append("a stalled attempt without the stall line was not flagged")
        seg["lines"] = ["a", STALL_LINE]
        if stall_problems([seg]):
            fails.append("a stalled attempt with the stall line was flagged")
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


RANK = {"OK": 0, "WATCH": 1, "BAD": 2}


def _band(x, ok, bad, big_is_bad=True):
    """OK/WATCH/BAD of x by the coordinator's bounds (OK below `ok` and BAD above `bad`; the reverse when big_is_bad is False)"""
    if big_is_bad:
        return "OK" if x < ok else ("WATCH" if x <= bad else "BAD")
    return "OK" if x > ok else ("WATCH" if x >= bad else "BAD")


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def step_verdicts(s, ediff=None):
    """[(quantity, OK/WATCH/BAD, text)] of an accepted step by the coordinator's bounds of 2026-11-11 01:06 UTC (the first |dz| and the start max|F| are the attempt's)"""
    out = []
    n = s["steps"]
    if n is None or not s["conv"]:
        out.append(("Newton steps", "BAD", "not converged"))
    else:
        out.append(("Newton steps", "OK" if n <= 4 else ("WATCH" if n <= 8 else "BAD"), f"{n} Newton"))
    lams = s["lams"]
    stall = any(STALL_LINE in ln for ln in s["seg"]["lines"])
    lmin = min(lams) if lams else 1.0
    v = "BAD" if (lmin < 0.25 or stall) else ("OK" if lmin == 1 else "WATCH")
    out.append(("lam", v, "lam 1" if v == "OK" else f"lam down to {lmin:g}" + (" and the stall line" if stall else "")))
    f = _f(s["final"])
    out.append(("final max|F|", "BAD" if f is None or f > 1e-40 else ("OK" if f < 1e-60 else "WATCH"), f"final {s['final']}"))
    st = _f(s["start"])
    out.append(("start max|F|", "BAD" if st is None else _band(st, 1e-33, 1e-25), f"start {s['start']}"))
    dz = _f(s["dz0"])
    out.append(("first |dz|", "BAD" if dz is None else _band(dz, 1e-29, 1e-26), f"first |dz| {s['dz0']}"))
    hor = _f(s["seg"].get("hor"))
    out.append(("horizon rung", "BAD" if hor is None or s["seg"]["status"] != "ok" else _band(hor, 1e-50, 1e-40), f"horizon {s['seg'].get('hor', '?')}"))
    if ediff is not None:
        out.append(("Delta minus extrapolation", _band(abs(ediff), 1e-12, 1e-10), f"Delta-extrap {mp.nstr(ediff, 2)}"))
    return out


def base_verdicts(s):
    """[(quantity, verdict, text)] of the series line of the step's base"""
    sm = SERIES.match(s["seg"].get("series", ""))
    if not sm:
        return [("series", "BAD", "no series line")]
    zN, amax, r4 = float(sm.group(5)), float(sm.group(7)), float(sm.group(6).split()[-1])
    return [("|z_N|", _band(zN, 1e-27, 1e-24), f"|z_N| {sm.group(5)}"), ("a_max", _band(amax, 2.5, 2.0, big_is_bad=False), f"a_max {sm.group(7)}"),
            ("fourth ratio", "OK" if r4 > 150 else "WATCH", f"fourth ratio {sm.group(6).split()[-1]}")]   # the coordinator, 01:33 UTC: a fourth ratio under 150 is ~ at most, never ✗


def verdict_line(kind, label, vs, extra=""):
    worst = max((v for _, v, _ in vs), key=lambda v: RANK[v])
    names = [q for q, v, _ in vs if v == worst] if worst != "OK" else []
    return f"{worst} {kind} {label}: " + ", ".join(t for _, _, t in vs) + (f"  [{worst}: {', '.join(names)}]" if names else "") + extra, worst


def verdicts(runs, frm=1, out=print, csv_path=CSV):
    """the verdict lines (per step, then per base) of the accepted steps of the runs, leading the hourly table"""
    pts = chain_six(csv_path)
    rows = []
    for log, jsonl in runs:
        for s in accepted(log, jsonl):
            e = extrapolate(pts[-6:], s["D"])
            ediff = (s["delta"] - e) if s["delta"] is not None else None
            if s["delta"] is not None:
                pts.append((s["D"], s["delta"]))
            rows.append((s, ediff))
    for k, (s, ediff) in enumerate(rows, 1):
        if k < frm:
            continue
        sm = SERIES.match(s["seg"].get("series", ""))
        d0 = sm.group(2) if sm else "?"
        out(verdict_line("step", f"{k} D {d0} -> {mp.nstr(s['D'], 9)} (a {s['a']:g})", step_verdicts(s, ediff))[0])
        out(verdict_line("base", f"D {d0}", base_verdicts(s), f", smallest pivot {s['pivots'].split('..')[0]} (not judged)")[0])
    return len(rows)


MARK = {"OK": "✓", "WATCH": "~", "BAD": "✗"}
MACHINE = "win2"


def step_line(s, refused=False):
    """the coordinator's step line of 2026-11-11 01:11 UTC: machine, D base -> D target, six marks (Newton steps, step length = the smallest lam, final residual, start residual,
    first move = first |dz|, series) and the numbers in the same order; a refused attempt has the Newton-steps mark BAD"""
    vs = {q: v for q, v, _ in step_verdicts(s)}
    if refused:
        vs["Newton steps"] = "BAD"
    bs = base_verdicts(s)
    ser = max((v for _, v, _ in bs), key=lambda v: RANK[v])
    marks = [MARK[vs[q]] for q in ("Newton steps", "lam", "final max|F|", "start max|F|", "first |dz|")] + [MARK[ser]]
    sm = SERIES.match(s["seg"].get("series", ""))
    d0 = f"{float(sm.group(2)):.2f}" if sm else "?"
    dt = f"{float(s['D']):.2f}"
    lmin = min(s["lams"]) if s["lams"] else 1.0
    two = lambda v: f"{float(v):.1e}" if _f(v) is not None else str(v)   # two significant digits, as in the coordinator's example
    vals = [str(s["steps"]), f"{lmin:g}", two(s["final"]), two(s["start"]), two(s["dz0"]), {"OK": "ok", "WATCH": "watch", "BAD": "bad"}[ser]]
    return f"{MACHINE}  D {d0} -> {dt}   {' '.join(marks)}   ({', '.join(vals)})"


def delta_line(D, delta, digits=11):
    """Delta with only the trusted digits, cut (not rounded) after `digits` decimals: 11 digits and "±2 in the last digit" for an error bar of 2.1e-11 (the coordinator's
    correction of 01:14 UTC; the bar is the spread over the held fit's degree, d6 minus d10, 2e-11 as the working value past D 221 until it is measured)"""
    t = mp.nstr(delta, 30)
    return f"Delta(D {mp.nstr(D, 11)}) = {t[:t.index('.') + 1 + digits]} (±2 in the last digit)"


def steps(runs, out=print):
    """the step lines of every attempt in order (a refused attempt is one line), a Delta line after each accepted step"""
    n = 0
    for log, jsonl in runs:
        segs, flat, _, _ = load(log, jsonl)
        acc = {x["idx"]: x for x in accepted(log, jsonl)}
        for i, (r, a) in enumerate(flat):
            if i >= len(segs):
                break
            seg = segs[i]
            if a["accepted"]:
                x = acc[i]
                out(step_line(x))
                if x["delta"] is not None:
                    out(delta_line(x["D"], x["delta"]))
            else:
                x = dict(D=mpf(a["D_str"]), a=a["a"], seg=seg, **info(seg))
                out(step_line(x, refused=True))
            n += 1
        for seg in segs[len(flat):]:     # attempts of a run that ended before its step record was written (crawlH): a finished, not converged one is a refused line
            if seg["end"] and seg["newton"] and not seg["newton"][2]:
                sm = SERIES.match(seg.get("series", ""))
                x = dict(D=mpf(seg["end"]), a=float(seg["a"]), seg=seg, **info(seg))
                out(step_line(x, refused=True))
                n += 1
    return n


def fseq(runs, out=print):
    """per attempt, the max|F| after each Newton step (the coordinator's 03:43 UTC request: a stall near 1e-51 followed by a jump, or a slow linear fall)"""
    n = 0
    two = lambda v: f"{float(v):.1e}"
    for log, jsonl in runs:
        segs, flat, _, _ = load(log, jsonl)
        for i, seg in enumerate(segs):
            if not seg["on"]:
                continue
            vals = []
            for k, ln in enumerate(seg["on"]):
                m = re.search(r"\|F\| (\S+) -> (\S+?),", ln)
                m2 = re.search(r"\|F\| (\S+) converged", ln)
                m3 = re.search(r"\|F\| (\S+),", ln)
                if m:
                    if k == 0:
                        vals.append(two(m.group(1)))
                    vals.append(two(m.group(2)))
                elif m2:
                    if not vals:
                        vals.append(two(m2.group(1)))
                elif m3 and k == 0:
                    vals.append(two(m3.group(1)))
            sm = SERIES.match(seg.get("series", ""))
            d0 = f"{float(sm.group(2)):.2f}" if sm else "?"
            dt = f"{float(seg['end']):.2f}" if seg["end"] else "(running)"
            out(f"D {d0} -> {dt} (a {float(seg['a']):.3f}): " + " → ".join(vals))
            n += 1
    return n


def guard(log, jsonl):
    """the stop conditions of the coordinator's 03:43 UTC order, as text: a_max under 2.0 or |z_N| above 1e-24 in any base's series line, and an attempt of a 0.25 or below that
    needed more than 12 Newton steps or was refused"""
    segs, flat, stop, lines = load(log, jsonl)
    out = []
    for ln in lines:
        m = SERIES.match(ln)
        if m and (float(m.group(7)) < 2.0 or float(m.group(5)) > 1e-24):
            out.append(f"series of the base D {m.group(2)}: |z_N| {m.group(5)}, a_max {m.group(7)}, ratios 2-5 {m.group(6)}")
    for seg in segs:
        n = seg["newton"]
        if n and float(seg["a"]) <= 0.25 + 1e-9 and (n[0] > 12 or not n[2]):
            out.append(f"attempt a {seg['a']} to D {seg['end']}: {n[0]} Newton steps, {'converged' if n[2] else 'refused'}, max|F| {n[1]}")
    return out


FIRST_CHAIN = [("crawlB2.log", "crawlB2/anm_run.jsonl"), ("crawlB3.log", "crawlB3/anm_run.jsonl"), ("crawlB4.log", "crawlB4/anm_run.jsonl"),
               ("crawlB5.log", "crawlB5/anm_run.jsonl"), ("crawlC.log", "crawlC/anm_run.jsonl"), ("crawlD.log", "crawlD/anm_run.jsonl"),
               ("crawlE.log", "crawlE/anm_run.jsonl"), ("crawlF.log", "crawlF/anm_run.jsonl")]


def cmp_chains(log, jsonl, out=print, base=HERE):
    """Delta of each accepted step of a second chain beside the first chain's Delta at the same D (within 1e-9), and the difference"""
    first = {}
    for l, j in FIRST_CHAIN:
        if os.path.exists(os.path.join(base, l)):
            for s in accepted(os.path.join(base, l), os.path.join(base, j)):
                if s["delta"] is not None:
                    first[round(float(s["D"]), 6)] = s["delta"]
    # the coordinator, 01:55 UTC: information without a verdict (the first chain's states past D 225 carry the old rounding)
    out("| D | Delta of this chain | Delta of the first chain | difference |")
    out("|---|---|---|---|")
    n = 0
    for s in accepted(log, jsonl):
        k = round(float(s["D"]), 6)
        if k in first and s["delta"] is not None:
            n += 1
            diff = s["delta"] - first[k]
            out(f"| {mp.nstr(s['D'], 12)} | {mp.nstr(s['delta'], 20)} | {mp.nstr(first[k], 20)} | {mp.nstr(diff, 3)} |")
    out(f"{n} steps of this chain have a state of the first chain at the same D")
    return n


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")   # the step lines carry ✓ ~ ✗, and python -I ignores PYTHONIOENCODING
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    if a and a[0] == "fseq":
        sys.exit(0 if fseq(list(zip(a[1::2], a[2::2]))) >= 0 else 1)
    if a and a[0] == "guard" and len(a) == 3:
        reasons = guard(a[1], a[2])
        for r in reasons:
            print("STOP: " + r)
        sys.exit(3 if reasons else 0)
    if a and a[0] == "steps":
        sys.exit(0 if steps(list(zip(a[1::2], a[2::2]))) >= 0 else 1)
    if a and a[0] == "verdict":
        frm = 1
        rest = a[1:]
        if rest and rest[0] == "--from":
            frm, rest = int(rest[1]), rest[2:]
        sys.exit(0 if verdicts(list(zip(rest[0::2], rest[1::2])), frm) >= 0 else 1)
    if a and a[0] == "cmp" and len(a) == 3:
        sys.exit(0 if cmp_chains(a[1], a[2]) >= 0 else 1)
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

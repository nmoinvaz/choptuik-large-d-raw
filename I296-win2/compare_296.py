#!/usr/bin/env python3
"""I296-win2: the rest of the I19-win2 crawl, D 214.6 to 215.03125, reproduced on win2's new firmware (issue #296).

    python -I compare_296.py [--csv delta_all.csv]
        Reads ./crawl.log, ./crawl/ (anm_run.jsonl, anm_pin3_D*.npz, pred_pin3_D*.npz) and the crawl's ../I19-win2/crawl.log,
        ../I19-win2/crawl/.
        Part A, logs line by line, elapsed times removed (the new log's closing `done` line dropped): every line of the crawl's log
        (it was stopped by the coordinator at 03:25 UTC in the middle of an attempt, with no stop line) must be equal and present;
        prints "identical" or the first differing line with both texts, or that the new log ends before the crawl's last line.
        The lines the new log has beyond the crawl's last line are counted and its last line shown, with whether it ended by its own
        "stopped:" line (new information, not compared).
        Part B, the seven accepted steps (D 214.6, 214.7, 214.8, 214.9, 215.0, 215.025, 215.03125): the new anm_run.jsonl's accepted
        attempts have these D, their Delta equals delta_all.csv Delta_q0 as a double, and the i-th "converged, Delta X Y" line of the
        new log has X equal to it and Y equal to Delta_q1 in its 5 printed digits.
        Part C, the first seven records of anm_run.jsonl against the crawl's, timing keys dropped (first differing path named).
        Part D, every anm_pin3_D*.npz and pred_pin3_D*.npz of the crawl's folder that the new folder also has, array by array, bit for
        bit (informational), and the files the new folder lacks.
        Verdict "ACCEPTED" when A, B and C hold. Exit 0: accepted. Exit 1: not accepted. Exit 2: a file is missing.
    python -I compare_296.py --selftest
        the crawl's own files pass; a planted digit late in the log, a log cut before the crawl's last line, a planted correction in the csv,
        a changed Delta in record 3 of the jsonl and a planted bit in a saved state are each found (exit 1 inside if any fails)."""
import csv, glob, json, os, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(RAW, "I287-win2"))
import compare_287 as C  # noqa: E402

OLD_LOG = os.path.join(RAW, "I19-win2", "crawl.log")
OLD_DIR = os.path.join(RAW, "I19-win2", "crawl")
STEPS = ["214.6", "214.7", "214.8", "214.9", "215.0", "215.025", "215.03125"]
NSTEP = len(STEPS)


def csv_rows(path):
    with open(path, encoding="utf-8") as f:
        rows = {r["D"]: (float(r["Delta_q0"]), float(r["Delta_q1"])) for r in csv.DictReader(f)}
    return [rows[d] for d in STEPS]


def recs(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(ln) for ln in f if ln.strip()]


def accepted(rs):
    return [(a["D"], a["Delta"]) for r in rs for a in r["attempts"] if a["accepted"]]


def part_a(nl, ol, out):
    if nl and nl[-1] == "done":
        nl = nl[:-1]
    n = len(ol)
    for i in range(min(n, len(nl))):
        if nl[i] != ol[i]:
            out(f"part A: first differing line {i + 1} of the crawl's {n}\n  new: {nl[i]}\n  old: {ol[i]}")
            return False
    if len(nl) < n:
        out(f"part A: first {len(nl)} lines identical, but the new log ends before the crawl's last line ({n})")
        return False
    out(f"part A: identical for all {n} lines of the crawl's log (elapsed times removed); the new log has {len(nl) - n} further lines")
    if len(nl) > n:
        out(f"   new last line: {nl[-1][:200]}")
    out("   the new run ended by its own stop line" if any(s.startswith("stopped:") for s in nl[n:]) else "   no stop line in the new log")
    return True


def part_b(nl, rs, rows, out):
    if nl and nl[-1] == "done":
        nl = nl[:-1]
    ok = True
    acc = accepted(rs)
    ds = [float(d) for d in STEPS]
    if [d for d, _ in acc[:NSTEP]] != ds or len(acc) < NSTEP:
        out(f"part B: accepted steps {[d for d, _ in acc]} are not the crawl's {ds}")
        return False
    conv = [C.CONV.search(ln) for ln in nl]
    conv = [m for m in conv if m]
    if len(conv) < NSTEP:
        out(f"part B: only {len(conv)} 'converged, Delta X Y' lines in the new log")
        return False
    for i, (d, (q0, q1)) in enumerate(zip(STEPS, rows)):
        x, y = conv[i].group(1), conv[i].group(2)
        bad = []
        if acc[i][1] != q0 or float(x) != q0:
            bad.append(f"Delta {acc[i][1]!r} / {x} against {q0!r}")
        if f"{q1:+.4e}" != y:
            bad.append(f"correction {y} against {q1:+.4e}")
        out(f"part B: D {d}: Delta {x} correction {y} " + ("equal to delta_all.csv" if not bad else "DIFFERENT: " + "; ".join(bad)))
        ok = ok and not bad
    return ok


def part_c(rs, old, out):
    ok = True
    if len(rs) < NSTEP:
        out(f"part C: the new jsonl has {len(rs)} records, fewer than the crawl's {len(old)}")
        return False
    for i in range(len(old)):
        d = C.diff_path(rs[i], old[i])
        if d:
            out(f"part C: record {i} differs at {d}")
            ok = False
    if ok:
        out(f"part C: the first {len(old)} records of anm_run.jsonl equal the crawl's (timing keys dropped)")
    return ok


def part_d(new_dir, old_dir, out):
    olds = sorted(glob.glob(os.path.join(old_dir, "*_pin3_D*.npz")))
    same = diff = 0
    lacking = []
    for p in olds:
        q = os.path.join(new_dir, os.path.basename(p))
        if not os.path.exists(q):
            lacking.append(os.path.basename(p)); continue
        sink = []
        ok = C.part_c(q, p, sink.append)
        same += ok; diff += (not ok)
        if not ok:
            out(f"   {os.path.basename(p)}: {sink[0]}")
    out(f"part D: {same} saved state/prediction files bit for bit equal, {diff} differ (informational)" + (f", the new folder lacks {lacking}" if lacking else ""))
    return diff == 0 and not lacking


def run(new_log, new_dir, old_log=OLD_LOG, old_dir=OLD_DIR, csv_path=C.CSV, out=print):
    need = [new_log, os.path.join(new_dir, "anm_run.jsonl"), old_log, os.path.join(old_dir, "anm_run.jsonl"), csv_path]
    for p in need:
        if not os.path.exists(p):
            out(f"MISSING {p}")
            return 2
    nl, ol = C.lines(new_log), C.lines(old_log)
    rs, old = recs(os.path.join(new_dir, "anm_run.jsonl")), recs(os.path.join(old_dir, "anm_run.jsonl"))
    a = part_a(nl, ol, out)
    b = part_b(nl, rs, csv_rows(csv_path), out)
    c = part_c(rs, old, out)
    part_d(new_dir, old_dir, out)
    ok = a and b and c
    out("ACCEPTED" if ok else "NOT ACCEPTED")
    return 0 if ok else 1


def selftest():
    fails = []
    sink = []
    q = sink.append
    rc = run(OLD_LOG, OLD_DIR, out=q)
    if rc != 0 or any(("differ" in s.lower() and "bit for bit equal" not in s) or "NOT" in s for s in sink):
        fails.append(f"the crawl's own files rc {rc}: {sink}")
    ol = C.lines(OLD_LOG)
    raw = open(OLD_LOG, encoding="utf-8").read().split("\n")
    with tempfile.TemporaryDirectory() as td:
        nd = os.path.join(td, "crawl"); shutil.copytree(OLD_DIR, nd)
        j = max(i for i, s in enumerate(raw) if "on 0:" in s and "4.35e-22" in s)
        bad = list(raw); bad[j] = bad[j].replace("4.35e-22", "4.36e-22")
        p = os.path.join(td, "bad.log"); open(p, "w", encoding="utf-8").write("\n".join(bad))
        sink.clear()
        if part_a(C.lines(p), ol, q) or f"line {j + 1} " not in sink[0]:
            fails.append(f"a planted digit late in the log was not found at line {j + 1}: {sink}")
        cut = os.path.join(td, "cut.log"); open(cut, "w", encoding="utf-8").write("\n".join(raw[:len(raw) - 6]))
        sink.clear()
        if part_a(C.lines(cut), ol, q):
            fails.append("a log cut before the crawl's last line was accepted")
        more = os.path.join(td, "more.log"); open(more, "w", encoding="utf-8").write("\n".join(raw) + "\nstopped: no convergence after three halvings\ndone\n")
        sink.clear()
        if not part_a(C.lines(more), ol, q) or not any("own stop line" in s for s in sink):
            fails.append(f"a log with the crawl's lines plus a stop line was not accepted with its stop line shown: {sink}")
        rows = csv_rows(C.CSV)
        wrong = list(rows); wrong[3] = (rows[3][0], rows[3][1] * 1.01)
        sink.clear()
        if part_b(ol, recs(os.path.join(OLD_DIR, "anm_run.jsonl")), wrong, q):
            fails.append("a planted correction in the csv was accepted")
        rs = recs(os.path.join(OLD_DIR, "anm_run.jsonl")); old = recs(os.path.join(OLD_DIR, "anm_run.jsonl"))
        rs[3]["attempts"][0]["Delta"] += 1e-15
        sink.clear()
        if part_c(rs, old, q) or "record 3" not in sink[0]:
            fails.append(f"a changed Delta in record 3 was not found: {sink}")
        import numpy as np
        fz = os.path.join(nd, "anm_pin3_D215.0000.npz")
        z = dict(np.load(fz)); z["zh"] = z["zh"].copy(); z["zh"][7] = np.nextafter(z["zh"][7], 1e9); np.savez(fz, **z)
        sink.clear()
        if part_d(nd, OLD_DIR, q) or not any("anm_pin3_D215.0000.npz" in s for s in sink):
            fails.append(f"a planted bit in the D 215.0 state was not found: {sink}")
    print("selftest: ok" if not fails else "selftest FAILED:\n  " + "\n  ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    csv_path = sys.argv[sys.argv.index("--csv") + 1] if "--csv" in sys.argv else C.CSV
    sys.exit(run(os.path.join(HERE, "crawl.log"), os.path.join(HERE, "crawl"), csv_path=csv_path))

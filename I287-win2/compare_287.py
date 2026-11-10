#!/usr/bin/env python3
"""I287-win2: the first step of the I19-win2 crawl past D 214.5, reproduced on win2's new firmware (issue #287).

    python -I compare_287.py [--csv delta_all.csv]
        Reads ./crawl1.log, ./crawl1/anm_run.jsonl, ./crawl1/anm_pin3_D214.6000.npz and the crawl's
        ../I19-win2/crawl.log, ../I19-win2/crawl/anm_run.jsonl, ../I19-win2/crawl/anm_pin3_D214.6000.npz.
        Part A, logs line by line, elapsed times removed, the new log against the crawl's lines before its "step 1:" line: prints
        "identical" or the first differing line with both texts, and the number of lines compared.
        Part B, the accepted step: the new log's "converged, Delta X Y" line gives Delta and the correction, which must equal
        delta_all.csv row 214.6 (Delta_q0 exactly as a double, Delta_q1 to its 5 printed digits), and the new step-0 record of
        anm_run.jsonl against the crawl's, timing keys dropped (first differing path named).
        Part C, the saved state anm_pin3_D214.6000.npz and the saved prediction pred_pin3_D214.6000.npz against the crawl's, array by array, bit for bit (informational).
        Verdict line "ACCEPTED" when B holds (the acceptance of #287), "NOT ACCEPTED" otherwise. Exit 0: accepted. Exit 1: not
        accepted. Exit 2: a file is missing.
    python -I compare_287.py --selftest
        A copy of the crawl's own files passes all parts, and a planted digit in a log line, a planted correction in the
        csv row, a planted value in the jsonl record and a planted bit in the state are each found (exit 1 inside if any fails)."""
import csv, json, os, re, sys, tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.dirname(HERE)
OLD_LOG = os.path.join(RAW, "I19-win2", "crawl.log")
OLD_JSONL = os.path.join(RAW, "I19-win2", "crawl", "anm_run.jsonl")
OLD_NPZ = os.path.join(RAW, "I19-win2", "crawl", "anm_pin3_D214.6000.npz")
CSV = os.path.join(os.path.dirname(RAW), "choptuik-large-d", "hp", "data", "delta_all.csv")
TIMING = {"t_coef", "t_corr", "seconds"}
ELAPSED = re.compile(r",\s*\d+(?:\.\d+)?\s+s(?=;|$)")
CONV = re.compile(r"converged, Delta (\S+) (\S+)\s*$")


def lines(path):
    with open(path, encoding="utf-8") as f:
        return [ELAPSED.sub("", ln.rstrip("\n")) for ln in f]


def first_step(ls):
    for i, ln in enumerate(ls):
        if ln.startswith("step 1:"):
            return ls[:i]
    return ls


def part_a(new, old, out=print):
    new, old = first_step(new), first_step(old)
    n = min(len(new), len(old))
    for i in range(n):
        if new[i] != old[i]:
            out(f"part A: first differing line {i + 1} of {n} compared\n  new: {new[i]}\n  old: {old[i]}")
            return False
    if len(new) != len(old):
        out(f"part A: first {n} lines identical, but the new log has {len(new)} lines and the crawl's first step {len(old)}")
        return False
    out(f"part A: identical ({n} lines, elapsed times removed)")
    return True


def csv_row(path, d="214.6"):
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["D"] == d:
                return float(row["Delta_q0"]), float(row["Delta_q1"])
    raise KeyError(d)


def diff_path(a, b, p=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k in TIMING:
                continue
            if k not in a or k not in b:
                return f"{p}/{k} missing in {'new' if k not in a else 'old'}"
            d = diff_path(a[k], b[k], f"{p}/{k}")
            if d:
                return d
        return None
    if isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            return f"{p} length {len(a)} against {len(b)}"
        for i, (x, y) in enumerate(zip(a, b)):
            d = diff_path(x, y, f"{p}[{i}]")
            if d:
                return d
        return None
    return None if a == b else f"{p}: new {a!r} old {b!r}"


def part_b(new_ls, new_rec, old_rec, csv_path, out=print):
    ok = True
    m = None
    for ln in first_step(new_ls):
        m = CONV.search(ln) or m
    if m is None:
        out("part B: no 'converged, Delta X Y' line in the new log")
        return False
    x, y = m.group(1), m.group(2)
    q0, q1 = csv_row(csv_path)
    if float(x) != q0:
        out(f"part B: Delta {x} differs from delta_all.csv {q0!r}"); ok = False
    if f"{q1:.4e}" != y:
        out(f"part B: correction {y} differs from delta_all.csv {q1:.4e}"); ok = False
    if ok:
        out(f"part B: Delta {x} and correction {y} equal delta_all.csv row 214.6 ({q0!r}, {q1:.4e})")
    d = diff_path(new_rec, old_rec)
    out("part B: step-0 record of anm_run.jsonl equal to the crawl's (timing keys dropped)" if d is None
        else f"part B: step-0 record differs at {d}")
    return ok


def part_c(new_path, old_path, out=print):
    a, b = np.load(new_path), np.load(old_path)
    bad = []
    for k in b.files:
        if k == "meta":
            continue
        if k not in a.files or a[k].shape != b[k].shape or not np.array_equal(a[k], b[k], equal_nan=True):
            diff = float(np.max(np.abs(a[k] - b[k]))) if k in a.files and a[k].shape == b[k].shape else float("nan")
            bad.append((k, diff))
    out("part C: state arrays bit for bit equal to the crawl's" if not bad
        else "part C: state arrays differ (informational): " + ", ".join(f"{k} max|d| {d:.3g}" for k, d in bad))
    return not bad


def run(new_log, new_jsonl, new_npz, old_log=OLD_LOG, old_jsonl=OLD_JSONL, old_npz=OLD_NPZ, csv_path=CSV, out=print):
    for p in (new_log, new_jsonl, new_npz, old_log, old_jsonl, old_npz, csv_path):
        if not os.path.exists(p):
            out(f"MISSING {p}")
            return 2
    nl = lines(new_log)
    if nl and nl[-1] == "done":  # the run's own closing line, which the crawl's first step (it went on) does not have
        nl = nl[:-1]
    rec = lambda p: json.loads(open(p, encoding="utf-8").readline())
    a = part_a(nl, lines(old_log), out)
    b = part_b(nl, rec(new_jsonl), rec(old_jsonl), csv_path, out)
    part_c(new_npz, old_npz, out)
    new_pred, old_pred = (os.path.join(os.path.dirname(p), "pred_pin3_D214.6000.npz") for p in (new_npz, old_npz))
    if os.path.exists(new_pred) and os.path.exists(old_pred):
        out("saved prediction (pred_pin3_D214.6000.npz):")
        part_c(new_pred, old_pred, out)
    out("ACCEPTED" if b else "NOT ACCEPTED")
    return 0 if b else 1


def selftest():
    fails = []
    sink = []
    q = lambda *a: sink.append(" ".join(map(str, a)))
    rc = run(OLD_LOG, OLD_JSONL, OLD_NPZ, out=q)
    if rc != 0 or any("differ" in s or "NOT" in s for s in sink):
        fails.append(f"copy of the crawl's own files rc {rc}: {sink}")
    with tempfile.TemporaryDirectory() as td:
        ls = open(OLD_LOG, encoding="utf-8").read().split("\n")
        i = next(k for k, s in enumerate(ls) if "1.25e-26" in s and "15.76 s" in s)
        bad = list(ls); bad[i] = bad[i].replace("1.25e-26", "1.26e-26")
        p = os.path.join(td, "l.log"); open(p, "w", encoding="utf-8").write("\n".join(bad))
        sink.clear()
        if part_a(lines(p), lines(OLD_LOG), q) or f"line {i + 1}" not in sink[0]:
            fails.append(f"planted log digit not found at line {i + 1}: {sink}")
        slow = list(ls); slow[i] = slow[i].replace("15.76 s", "99.99 s")
        p2 = os.path.join(td, "t.log"); open(p2, "w", encoding="utf-8").write("\n".join(slow))
        sink.clear()
        if not part_a(lines(p2), lines(OLD_LOG), q):
            fails.append("a changed elapsed time was reported as a difference")
        one = [ln for ln in first_step(ls)]
        for tail, want in (("done", True), ("an extra line", False)):
            p3 = os.path.join(td, "d.log"); open(p3, "w", encoding="utf-8").write("\n".join(one + [tail]) + "\n")
            sink.clear()
            run(p3, OLD_JSONL, OLD_NPZ, out=q)
            if any(s.startswith("part A: identical") for s in sink) != want:
                fails.append(f"a log ending in {tail!r}: part A identical should be {want}: {sink[:1]}")
        c = os.path.join(td, "c.csv")
        with open(c, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f); w.writerow(["D", "Delta_q0", "Delta_q1"]); w.writerow(["214.6", "1.6916473410327395", "-9.4e-17"])
        sink.clear()
        if part_b(lines(OLD_LOG), json.loads(open(OLD_JSONL, encoding="utf-8").readline()),
                  json.loads(open(OLD_JSONL, encoding="utf-8").readline()), c, q):
            fails.append("a planted correction in the csv row was accepted")
        r = json.loads(open(OLD_JSONL, encoding="utf-8").readline()); r2 = json.loads(json.dumps(r))
        r2["attempts"][0]["Delta"] += 1e-15
        if diff_path(r2, r) is None or "Delta" not in diff_path(r2, r):
            fails.append("a planted Delta in the jsonl record was not found")
        r3 = json.loads(json.dumps(r)); r3["t_coef"] = 0.0
        if diff_path(r3, r) is not None:
            fails.append("a changed timing key was reported as a difference")
        z = dict(np.load(OLD_NPZ)); z["zh"] = z["zh"].copy(); z["zh"][5] = np.nextafter(z["zh"][5], 1e9)
        n = os.path.join(td, "s.npz"); np.savez(n, **z)
        sink.clear()
        if part_c(n, OLD_NPZ, q) or "zh" not in sink[0]:
            fails.append(f"a planted last-bit change in zh was not found: {sink}")
    print("selftest: ok" if not fails else "selftest FAILED:\n  " + "\n  ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    csv_path = sys.argv[sys.argv.index("--csv") + 1] if "--csv" in sys.argv else CSV
    sys.exit(run(os.path.join(HERE, "crawl1.log"), os.path.join(HERE, "crawl1", "anm_run.jsonl"),
                 os.path.join(HERE, "crawl1", "anm_pin3_D214.6000.npz"), csv_path=csv_path))

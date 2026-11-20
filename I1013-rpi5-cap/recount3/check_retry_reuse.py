"""#1013 recount3: does a --retry run reuse its cached points?   python3 check_retry_reuse.py POINTS LOG N0 SHA256 [--selftest]
(adapted from check_cache_reuse.py, which allows no repeated key; --retry recomputes the cached points without value by design.)
POINTS = m3/points_M3_r0.18.jsonl, LOG = logs/m3_recount3_r0.18.log, N0 and SHA256 = the cache's line count and hash when the run
started (logs/exits.txt, "recount start ..."). A cached point is `retried` when its record is not argcount's `valued3` (info < 1e-8 or
fix.ok false), the points --retry skips on loading. Checks (exit 0 only if all hold):
1. the first N0 lines of POINTS still hash to SHA256 (the cache was only appended to);
2. a key (A, wf) occurs twice only if its first record is a retried one (nothing valued was solved again), and never three times;
3. no `point` line of LOG names a cached point that is not retried (the log prints a line for each point it computes).
Prints the counts of cached, retried, new records and new log lines, and how many retried points the log has reached.
--selftest: runs the checks on four altered copies (a valued cached key repeated, an altered first line, a log line naming a valued
cached point, a retried key three times); each must fail, and the base (a retried point recomputed) must pass."""
import hashlib, json, re, sys, tempfile


def valued3(r):
    return (isinstance(r.get("info"), float) and r["info"] < 1e-8) or bool((r.get("fix") or {}).get("ok"))


def run(pts, log, n0, sha):
    L = open(pts).read().splitlines(True)
    recs = [json.loads(x) for x in L]
    key = lambda r: (round(r["A"], 12), round(r["wf"], 12))
    cached = {key(r) for r in recs[:n0]}
    retried = {key(r) for r in recs[:n0] if not valued3(r)}
    counts = {}
    for r in recs:
        counts[key(r)] = counts.get(key(r), 0) + 1
    bad_dup = [k for k, c in counts.items() if (c > 1 and k not in retried) or c > 2]
    logk = [(round(float(m.group(1)), 12), round(float(m.group(2)), 12)) for m in
            (re.match(r"  point A (\S+) wf (\S+):", l) for l in open(log)) if m]
    redo = [k for k in logk if k in cached and k not in retried]
    ok = [hashlib.sha256("".join(L[:n0]).encode()).hexdigest() == sha, not bad_dup, not redo]
    print(f"cached points {n0} ({len(cached)} distinct, {len(retried)} retried); records now {len(recs)} ({len(recs) - n0} new); "
          f"log point lines {len(logk)}, retried points reached {len(retried & set(logk))}")
    print(f"1 cache lines unchanged: {ok[0]}; 2 keys repeated beyond a retried one: {len(bad_dup)}; "
          f"3 log lines naming a valued cached point: {len(redo)}")
    return all(ok)


if "--selftest" in sys.argv:
    d = tempfile.mkdtemp(); p, lg = f"{d}/p.jsonl", f"{d}/l.log"
    rec = lambda a, ok=True: json.dumps(dict(A=a, wf=1.0, re=1.0, im=0.0, info=0.0 if ok else float("nan"))) + "\n"
    open(p, "w").write(rec(1.0) + rec(2.0) + rec(3.0, False)); sha = hashlib.sha256(open(p).read().encode()).hexdigest()
    open(p, "a").write(rec(3.0) + rec(4.0))                   # the retried point 3 again, and a new point 4
    open(lg, "w").write("  point A 3.0000000 wf 1.00000000: R 1, |r3| 0, 5 CPU s\n  point A 4.0000000 wf 1.00000000: R 1, |r3| 0, 5 CPU s\n")
    good = run(p, lg, 3, sha); print("base passes:", good)
    q, ql = open(p).read(), open(lg).read()
    bad = []
    open(p, "w").write(q + rec(2.0)); bad.append(run(p, lg, 3, sha)); open(p, "w").write(q)                  # a valued key again
    open(p, "w").write(q.replace("1.0,", "1.5,", 1)); bad.append(run(p, lg, 3, sha)); open(p, "w").write(q)  # a cached line altered
    open(lg, "a").write("  point A 2.0000000 wf 1.00000000: R 1, |r3| 0, 5 CPU s\n"); bad.append(run(p, lg, 3, sha)); open(lg, "w").write(ql)
    open(p, "w").write(q + rec(3.0)); bad.append(run(p, lg, 3, sha)); open(p, "w").write(q)                  # a retried key three times
    print("controls failing as required:", [not b for b in bad], flush=True)
    sys.exit(0 if good and not any(bad) else 1)
sys.exit(0 if run(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]) else 1)

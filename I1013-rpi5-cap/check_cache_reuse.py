"""#1013 rerun: does step 1 reuse its cached points?   python3 check_cache_reuse.py POINTS LOG N0 SHA256 [--selftest]
POINTS = m3/points_M3_r0.17.jsonl, LOG = logs/m3_upper_r0.17_rerun.log, N0 and SHA256 = the cache's line count and hash when the rerun
started (logs/exits.txt, "rerun of step 1 start ...").  Checks (exit 0 only if all hold):
1. the first N0 lines of POINTS still hash to SHA256 (the cache was only appended to);
2. no key (A, wf) occurs twice in POINTS (nothing cached was solved again);
3. no `point` line of LOG names a key of the first N0 lines (the log prints a line for each point it computes).
Prints the count of cached points, of new records and of new log lines. --selftest: runs the checks on three altered copies
(a duplicated cached line, an altered first line, a log line naming a cached point); each must fail."""
import hashlib, json, re, sys, os, tempfile

def run(pts, log, n0, sha):
    L = open(pts).read().splitlines(True)
    head = "".join(L[:n0])
    recs = [json.loads(x) for x in L]
    key = lambda r: (round(r["A"], 12), round(r["wf"], 12))
    cached = {key(r) for r in recs[:n0]}
    keys = [key(r) for r in recs]
    dup = len(keys) - len(set(keys))
    logk = [(round(float(m.group(1)), 12), round(float(m.group(2)), 12)) for m in
            (re.match(r"  point A (\S+) wf (\S+):", l) for l in open(log)) if m]
    redo = [k for k in logk if k in cached]
    ok = [hashlib.sha256(head.encode()).hexdigest() == sha, dup == 0, not redo]
    print(f"cached points {n0} ({len(cached)} distinct); records now {len(recs)} ({len(recs) - n0} new); log point lines {len(logk)}")
    print(f"1 cache lines unchanged: {ok[0]}; 2 duplicate keys: {dup}; 3 log lines naming a cached point: {len(redo)}")
    return all(ok)

if "--selftest" in sys.argv:
    d = tempfile.mkdtemp(); p, lg = f"{d}/p.jsonl", f"{d}/l.log"
    rec = lambda a: json.dumps(dict(A=a, wf=1.0, re=1.0, im=0.0, info=0.0)) + "\n"
    open(p, "w").write(rec(1.0) + rec(2.0) + rec(3.0)); sha = hashlib.sha256(open(p).read().encode()).hexdigest()
    open(p, "a").write(rec(4.0)); open(lg, "w").write("  point A 4.0000000 wf 1.00000000: R 1, |r3| 0, 5 CPU s\n")
    good = run(p, lg, 3, sha); print("base passes:", good)
    bad = []
    q = open(p).read()
    open(p, "w").write(q + rec(2.0)); bad.append(run(p, lg, 3, sha)); open(p, "w").write(q)
    open(p, "w").write(q.replace("1.0,", "1.5,", 1)); bad.append(run(p, lg, 3, sha)); open(p, "w").write(q)
    open(lg, "a").write("  point A 2.0000000 wf 1.00000000: R 1, |r3| 0, 5 CPU s\n"); bad.append(run(p, lg, 3, sha))
    print("controls failing as required:", [not b for b in bad], flush=True)
    sys.exit(0 if good and not any(bad) else 1)
sys.exit(0 if run(sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4]) else 1)

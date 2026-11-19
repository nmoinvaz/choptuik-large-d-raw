"""#1008 macm3b stop rule (coordinator, 2026-11-19): run until t_D changes sign, then one more accepted step, then stop.
Usage: stop_watch_1008.py MODE
Reads OUT/arc.jsonl every 30 s. The step whose record carries a 'turn' (D'(s) = 0 inside its accepted [0, a], anm_run's own
detection, hp/arclength.py turn_in) holds the sign change of t_D; the next accepted step (converged) is the one past it.
When that record exists, SIGTERM the anm_run by the exact pid in the log's first line (capped_run: child pid N), SIGKILL
60 s later if it is still there; logs to exits_1008.txt. Ends when anm_run is gone or the rule has fired."""
import json, os, re, signal, subprocess, sys, time, datetime
mode = sys.argv[1]
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1008-macm3")
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def log(msg):
    with open(f"{O}/exits_1008.txt", "a") as f: f.write(f"1008m {msg} {now()}\n")
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
first = open(f"{O}/{mode}.log").readline()
pid = int(re.search(r"child pid (\d+)", first).group(1))
log(f"stop_watch_1008.py watches {mode}, anm_run pid {pid}: stops one accepted step after the step that holds the first turn")
fired = False
while alive(pid):
    try:
        recs = [json.loads(l) for l in open(f"{O}/{mode}/arc.jsonl")]
    except Exception:
        recs = []
    steps = [r for r in recs if "attempts" in r]
    k = next((i for i, r in enumerate(steps) if r.get("turn")), None)
    if k is not None and len(steps) > k + 1 and steps[k + 1].get("converged"):
        log(f"stop rule met: step {steps[k]['step']} holds the turn (D* {steps[k]['turn'][0]['D'][:22]}), step {steps[k + 1]['step']} accepted past it; SIGTERM anm_run pid {pid}")
        os.kill(pid, signal.SIGTERM)
        fired = True
        for _ in range(12):
            time.sleep(5)
            if not alive(pid): break
        if alive(pid):
            log(f"anm_run pid {pid} still alive 60 s after SIGTERM, SIGKILL")
            os.kill(pid, signal.SIGKILL)
        break
    time.sleep(30)
log(f"stop_watch_1008.py ends ({'rule fired' if fired else 'anm_run no longer running'})")

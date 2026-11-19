"""macm3b #903: wake when attempt 3 of step 53 (chain_k135b local step 4) ends. Accepted: the record is written and the saved state
exists; refused: the next attempt's re-seed line has not yet been logged or has just been. Also wakes when anm_run exits."""
import json, os, re, subprocess, time, datetime
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I903-macm3")
LOG = f"{O}/chain_k135b.log"
n0 = sum(1 for _ in open(f"{O}/chain_k135b/anm_run.jsonl"))
def alive(): return subprocess.run(["pgrep", "-f", "anm_run.py.*chain_k135b"], capture_output=True).returncode == 0
def ends():
    L = open(LOG).read().splitlines()
    i4 = next(i for i, l in enumerate(L) if l.startswith("step 4: D "))
    return [l for l in L[i4 + 1:] if re.match(r"\s+a [0-9.]+ -> D ", l)]
e0 = len(ends())
why = None
t0 = time.time()
while time.time() - t0 < 12 * 3600:
    time.sleep(15)
    if not alive(): why = "anm_run is not running"; break
    if "Traceback" in open(LOG).read(): why = "a Traceback in the log"; break
    e = ends()
    if len(e) > e0:
        time.sleep(20)
        nr = sum(1 for _ in open(f"{O}/chain_k135b/anm_run.jsonl"))
        why = ("attempt ended and the step was recorded (accepted): " if nr > n0 else "attempt ended, no record (refused): ") + e[-1].strip()[:200]
        break
print(f"wake at {datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC: {why}")

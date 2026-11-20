"""macm3b #1008 AB run watcher: wake when anm_run (argv[1]) exits, shows a Traceback, an attempt ends, a new arc record appears,
CORMAX correction lines are in the log (argv[3]), the corrections' seconds pass SECMAX (argv[4]), or after argv[2] minutes."""
import os, re, subprocess, sys, time, datetime
mode, mins, cormax, secmax = sys.argv[1], float(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4])
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1008-macm3")
COR = re.compile(r"\s+on (\d+): \|F\| (\S+) -> (\S+), \|dz\| (\S+) -> (\S+), lam (\S+), dDelta (\S+), piv \S+, ([0-9.]+) s$")
def alive(): return subprocess.run(["pgrep", "-f", f"anm_run.py.*I1008-macm3/{mode}"], capture_output=True).returncode == 0
def log(): return open(f"{O}/{mode}.log").read().splitlines()
def ncor_sec():
    n, s = 0, 0.0
    for l in log():
        m = COR.match(l)
        if m: n += 1; s += float(m.group(8))
    return n, s
def nend(): return sum(1 for l in log() if re.match(r"\s+(a [0-9.]+ -> D |corrector: \d+ steps.*(NOT converged|converged))", l))
def nrec():
    try: return sum(1 for _ in open(f"{O}/{mode}/arc.jsonl"))
    except Exception: return 0
e0, n0, t0 = nend(), nrec(), time.time(); why = f"{mins:g} minutes passed"
while time.time() - t0 < mins * 60:
    time.sleep(30)
    if not alive(): why = "anm_run is not running"; break
    if "Traceback" in "\n".join(log()): why = "a Traceback in the log"; break
    if nend() > e0: why = "an attempt ended (accepted or refused)"; break
    if nrec() > max(n0, 1): why = f"new arc record ({nrec()} now)"; break
    n, s = ncor_sec()
    if n >= cormax: why = f"{n} correction lines in the log ({s:.0f} s)"; break
    if s > secmax: why = f"corrections' seconds {s:.0f} > {secmax:g} ({n} correction lines)"; break
n, s = ncor_sec()
print(f"wake at {datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')} UTC: {why}; {n} correction lines, {s:.0f} s")

"""#1008 macm3b AB2 stop rule (coordinator, 2026-11-20): stop AB2 at once if corrections 0 and 1 both accept lam <= 1/16 (the crawl).
Usage: stop_ab2.py MODE. Reads MODE.log every 10 s; the correction lines are '  on K: |F| .. -> .., |dz| .. -> .., lam L, ...'.
When corrections 0 and 1 are both in the log and both lam <= 0.0625, SIGTERM the anm_run pid of the log's first line
(capped_run: child pid N), SIGKILL 60 s later if it is still there; logs to exits_1008.txt. Ends when anm_run is gone, when
a correction 0 or 1 with lam > 0.0625 is seen (the rule cannot fire), or after the rule fired."""
import os, re, signal, sys, time, datetime
mode = sys.argv[1]
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1008-macm3")
COR = re.compile(r"\s+on (\d+): \|F\| \S+ -> \S+, \|dz\| \S+ -> \S+, lam (\S+),")
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def log(msg):
    with open(f"{O}/exits_1008.txt", "a") as f: f.write(f"1008m {msg} {now()}\n")
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
while not (os.path.exists(f"{O}/{mode}.log") and open(f"{O}/{mode}.log").readline().strip()):
    time.sleep(2)
pid = int(re.search(r"child pid (\d+)", open(f"{O}/{mode}.log").readline()).group(1))
log(f"stop_ab2.py watches {mode}, anm_run pid {pid}: SIGTERM at once if corrections 0 and 1 both accept lam <= 1/16")
lam = {}
fired = False
while alive(pid):
    LL = open(f"{O}/{mode}.log").read().splitlines()
    ia = next((i for i, l in enumerate(LL) if l.strip().startswith("attempt at D")), None)   # the base polish's own 'on 0:' lines come before it
    for l in (LL[ia:] if ia is not None else []):
        m = COR.match(l)
        if m and int(m.group(1)) in (0, 1): lam[int(m.group(1))] = float(m.group(2))
    if any(v > 0.0625 for v in lam.values()):
        log(f"stop_ab2.py: correction {[k for k, v in lam.items() if v > 0.0625][0]} accepted lam > 1/16 (lam {lam}), the rule cannot fire; ends")
        sys.exit(0)
    if len(lam) == 2:
        log(f"stop rule met: corrections 0 and 1 accept lam {lam[0]:g} and {lam[1]:g} (both <= 1/16); SIGTERM anm_run pid {pid}")
        os.kill(pid, signal.SIGTERM)
        fired = True
        for _ in range(12):
            time.sleep(5)
            if not alive(pid): break
        if alive(pid):
            log(f"anm_run pid {pid} still alive 60 s after SIGTERM, SIGKILL")
            os.kill(pid, signal.SIGKILL)
        break
    time.sleep(10)
log(f"stop_ab2.py ends ({'rule fired' if fired else 'anm_run no longer running'})")

"""#1008 macm3b series check: waits for chk_old.log's 'series at D 259.565880482281: pivots' line (the arcjet is saved just before it), then SIGTERMs
the anm_run of the log's first line (capped_run: child pid N) by that exact pid (SIGKILL 60 s later if it is still there), logs to exits_1008.txt,
and runs compare_arcjet.py on run3/arcjet_000_D259.565880.npz and chk_old/arcjet_000_D259.565880.npz (output chk_old_compare.txt).
Usage: chk_series_watch.py [MODE=chk_old]"""
import os, re, signal, subprocess, sys, time, datetime
mode = sys.argv[1] if len(sys.argv) > 1 else "chk_old"
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1008-macm3")
PY = os.path.expanduser("~/Source/venv-macm3-main/bin/python3")
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def log(msg):
    with open(f"{O}/exits_1008.txt", "a") as f: f.write(f"1008m {msg} {now()}\n")
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
while not (os.path.exists(f"{O}/{mode}.log") and open(f"{O}/{mode}.log").readline().strip()):
    time.sleep(2)
pid = int(re.search(r"child pid (\d+)", open(f"{O}/{mode}.log").readline()).group(1))
log(f"chk_series_watch.py watches {mode}, anm_run pid {pid}: stops it once its series is saved, then compares it with run3/arcjet_000")
SER = re.compile(r"\s+series at D 259\.565880482281: pivots")
done = False
while alive(pid):
    if any(SER.match(l) for l in open(f"{O}/{mode}.log").read().splitlines()):
        time.sleep(3)
        log(f"{mode}: series line seen; SIGTERM anm_run pid {pid}")
        os.kill(pid, signal.SIGTERM)
        for _ in range(12):
            time.sleep(5)
            if not alive(pid): break
        if alive(pid):
            log(f"anm_run pid {pid} still alive 60 s after SIGTERM, SIGKILL")
            os.kill(pid, signal.SIGKILL)
        done = True
        break
    time.sleep(10)
a, b = f"{O}/run3/arcjet_000_D259.565880.npz", f"{O}/{mode}/arcjet_000_D259.565880.npz"
if os.path.exists(b):
    r = subprocess.run([PY, f"{O}/compare_arcjet.py", a, b, f"{O}/{mode}_compare.txt"], capture_output=True, text=True)
    first = next((l for l in r.stdout.splitlines() if l.startswith("EQUAL") or l.startswith("NOT EQUAL") or l.startswith("STRUCTURE")), "?")
    log(f"{mode}: compare_arcjet.py rc {r.returncode}: {first[:200]}")
else:
    log(f"{mode}: no arcjet saved ({'series line seen' if done else 'anm_run ended first'}); nothing to compare")
log(f"chk_series_watch.py ends")

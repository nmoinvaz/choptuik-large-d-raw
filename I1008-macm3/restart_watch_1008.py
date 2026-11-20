"""#1008 macm3b restart watcher (the coordinator's order, 2026-11-20 about 20:15 UTC): at run2's next step boundary, stop run2 and restart it from
its last accepted arc state on venv-macm3-1058b (hp at main 8179068d), with the same flags. Usage: restart_watch_1008.py MODE NEWMODE [--dry]
Arms only when OUT/I1058-macm3/at_8179068d/exits_1058.txt shows the four stored-reference checks as wanted (the checks come before the restart).
Reads OUT/MODE/arc.jsonl every 5 s. When an accepted step (converged) beyond the ones present at arming has its state file written, and no
record holds a turn, it SIGTERMs the anm_run of MODE.log's first line by its exact pid (SIGKILL after 60 s), then runs run_restart.sh NEWMODE in the
foreground (so this task lives as long as the restarted run): state = that step's arc_<n>_D*.npz, --a0 = the first-attempt length run2 itself would
have used next (a x grow after a first-attempt acceptance, a after a step that needed a halving; hold), --steps = 20 minus the accepted steps of MODE,
cap = what is left of MODE's 36 h cap. --dry prints those values for the latest accepted step and stops nothing."""
import glob, json, os, re, signal, subprocess, sys, time, datetime
mode, newmode = sys.argv[1], sys.argv[2]
dry = "--dry" in sys.argv
O = os.environ.get("R1008_O") or os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1008-macm3")
LAUNCH = os.environ.get("R1008_LAUNCH") or os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1008-macm3/run_restart.sh")
CHK = os.environ.get("R1008_CHK") or os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1058-macm3/at_8179068d/exits_1058.txt")
GROW = 1.25; STEPS_TOTAL = 20
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def log(msg):
    with open(f"{O}/exits_1008.txt", "a") as f: f.write(f"1008m {msg} {now()}\n")
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
def accepted():
    try: recs = [json.loads(l) for l in open(f"{O}/{mode}/arc.jsonl")]
    except Exception: return []
    return [r for r in recs if "attempts" in r and r.get("converged")]
def a_next(r): return r["a"] * GROW if len(r["attempts"]) == 1 else r["a"]   # arclength.py 415 and 468
def state_of(r):
    fs = sorted(glob.glob(f"{O}/{mode}/arc_{r['step'] + 1:03d}_D*.npz"))
    return fs[-1] if fs and abs(float(re.search(r"_D([0-9.]+)\.npz", fs[-1]).group(1)) - float(r["D_str"])) < 1e-6 else None
def plan(r, nacc):
    st = state_of(r)
    t0 = datetime.datetime.strptime(re.search(r"(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) UTC", [l for l in open(f"{O}/exits_1008.txt") if l.startswith(f"1008m {mode} start")][-1]).group(1), "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.UTC)
    cap = int(re.search(r"cap (\d+) s", [l for l in open(f"{O}/exits_1008.txt") if l.startswith(f"1008m {mode} start")][-1]).group(1))
    left = int(cap - (datetime.datetime.now(datetime.UTC) - t0).total_seconds())
    return st, repr(a_next(r)), STEPS_TOTAL - nacc, left
if dry:
    acc = accepted(); r = acc[-1]
    st, a0, steps, cap = plan(r, len(acc))
    print(f"dry: latest accepted step {r['step']} (a {r['a']!r}, {len(r['attempts'])} attempt(s), D {r['D_str'][:22]}); state {st}; --a0 {a0}; --steps {steps}; cap left {cap} s; "
          f"turn in any record: {any(x.get('turn') for x in acc)}")
    sys.exit(0)
chk = open(CHK).read().splitlines() if os.path.exists(CHK) else []
asw = [l for l in chk if re.search(r"check \S+ exit \d+ \(wanted \d+: as wanted\)", l)]
bad = [l for l in chk if "NOT AS WANTED" in l]
if len(asw) != 4 or bad:
    print(f"not armed: {len(asw)} checks as wanted, {len(bad)} not as wanted in {CHK}"); sys.exit(3)
pid = int(re.search(r"child pid (\d+)", open(f"{O}/{mode}.log").readline()).group(1))
n0 = len(accepted())
log(f"restart_watch_1008.py watches {mode}, anm_run pid {pid}, {n0} accepted steps: at the next accepted step stops it and starts {newmode} from that step's state on venv-macm3-1058b (the four checks at 8179068d are as wanted)")
while alive(pid):
    acc = accepted()
    if len(acc) > n0:
        r = acc[-1]
        if state_of(r):
            time.sleep(3)   # the state file is written before the record's line; 3 s for the series start, nothing is saved after
            if any(x.get("turn") for x in accepted()):
                log(f"restart_watch_1008.py: a turn is recorded in {mode} (step {r['step']}); not restarting, {mode} goes on; ends"); sys.exit(4)
            st, a0, steps, cap = plan(r, len(acc))
            log(f"{mode} step {r['step']} accepted (a {r['a']!r}, {len(r['attempts'])} attempt(s), D {r['D_str'][:22]}); SIGTERM anm_run pid {pid} for the restart as {newmode}: state {os.path.relpath(st, os.path.dirname(O))}, a0 {a0}, steps {steps}, cap {cap} s")
            os.kill(pid, signal.SIGTERM)
            for _ in range(12):
                time.sleep(5)
                if not alive(pid): break
            if alive(pid):
                log(f"anm_run pid {pid} still alive 60 s after SIGTERM, SIGKILL"); os.kill(pid, signal.SIGKILL); time.sleep(2)
            time.sleep(3)   # run_ab.sh's own 'exit' line
            rc = subprocess.run(["bash", LAUNCH, newmode, str(steps), str(cap), os.path.relpath(st, os.path.dirname(O)), a0]).returncode
            log(f"restart_watch_1008.py ends: {newmode} launcher exit {rc}")
            sys.exit(rc)
    time.sleep(5)
log(f"restart_watch_1008.py ends: anm_run {pid} is gone without a restart")
sys.exit(5)

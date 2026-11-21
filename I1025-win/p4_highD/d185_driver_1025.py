#!/usr/bin/env python3
"""#1025 winb, the root at D 18.5 (the coordinator's order of 2026-11-21 10:3x UTC): the hybrid root by raw I1025-mac/p4_hybrid.py (blob a402559b) on xfkappa's leap
state, then, if every hybrid check passes, ell_ddm.py det at root -/+ 0.02 (two processes in parallel, --noise 1e-24,1e-20,1e-16), then read_ddB_1025.py (Amendment 3).
Each child has a 6 h cap (21600 s) and is killed at the cap by its exact pid (taskkill /PID <pid> /T /F on the pid this driver started, never by name).
A sampler thread logs every 60 s the cpu seconds, working set, private bytes and their peaks of every process below a running child, the laptop's free
memory and cpu load, into rows/d185_samples.csv. A thin driver: it runs xfkappa's scripts unchanged.
usage: d185_driver_1025.py [--selftest]"""
import csv, datetime, json, os, subprocess, sys, threading, time

OUT = "C:/Users/nathan/Source/p4hi_1025/I1025-win/p4_highD"
HERE = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
WT_H = "C:/Users/nathan/Source/choptuik-i1025-lowd"     # 505d8399: the hybrid rows' worktree
WT_D = "C:/Users/nathan/Source/choptuik-i1025d"         # 48c36355: ell_ddm.py, as for row B
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
RAW = "C:/Users/nathan/Source/p4hi_1025/raw"
P4 = RAW + "/I1025-mac/p4_hybrid.py"
STATE = RAW + "/I1025-mac/d18/sol_l1kc63Wm1025_D18.500000.npy"
STUB = OUT + "/stub_d185_l1kc63Wm1025_D18.5_leapline.jsonl"
JS = OUT + "/ell_p4_hybrid_1025_w_highD_d185.jsonl"
LOG = OUT + "/d185_w.log"
SAMPLES = OUT + "/rows/d185_samples.csv"
D, KC, CAP = "18.5", "63", 21600
INTERVAL = int(os.environ.get("D185_SAMPLE_S", "60"))
PINS = [(P4, "a402559b5d37661b49da50f07f877af21fd29b3a"), (RAW + "/I1025-mac/signtest.py", "179ea09681b0a75f7cefdff98984b48051b3f085"),
        (STATE, "33c1a58b82229d55661cbd5e79d2c1fce0c0717c"), (RAW + "/I1025-mac/d18/l1kc63Wm1025.jsonl", "08f4dbf367edba55814e5cf989ccd32a9a5dbe67")]
_active = {}        # stage name -> launcher pid, read by the sampler


def say(m):
    line = f"== {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


PS = r"""
$rows = @()
foreach ($lp in @(%s)) {
  foreach ($q in (Get-CimInstance Win32_Process -Filter "ParentProcessId=$lp")) {
    $p = Get-Process -Id $q.ProcessId -ErrorAction SilentlyContinue
    if ($p) { $rows += ('{0},{1},{2:N1},{3:N3},{4:N3},{5:N3},{6:N3},{7}' -f $lp, $p.Id, $p.CPU, ($p.WorkingSet64/1GB), ($p.PeakWorkingSet64/1GB), ($p.PrivateMemorySize64/1GB), ($p.PeakPagedMemorySize64/1GB), $p.Threads.Count) }
  }
}
$os = Get-CimInstance Win32_OperatingSystem
$cpu = (Get-CimInstance Win32_PerfFormattedData_PerfOS_Processor -Filter "Name='_Total'").PercentProcessorTime
$m = Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory
$rows | ForEach-Object { 'P,' + $_ }
('S,{0:N2},{1},{2:N2}' -f ($os.FreePhysicalMemory/1MB), $cpu, ($m.CommittedBytes/1GB))
"""


def sample_once():
    if not _active:
        return
    stages = {v: k for k, v in _active.items()}
    r = subprocess.run(["powershell", "-NoProfile", "-Command", PS % ",".join(str(v) for v in _active.values())], capture_output=True, text=True)
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%H:%M:%S")
    new = not os.path.exists(SAMPLES)
    with open(SAMPLES, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["utc", "stage", "launcher_pid", "python_pid", "cpu_s", "ws_gb", "ws_peak_gb", "private_gb", "private_peak_gb", "threads", "free_phys_gb", "laptop_cpu_pct", "commit_gb"])
        sysrow = next((l.split(",") for l in r.stdout.splitlines() if l.startswith("S,")), ["S", "", "", ""])
        for l in r.stdout.splitlines():
            if l.startswith("P,"):
                _, lp, pid, cpu, ws, wsp, pv, pvp, th = l.split(",")
                w.writerow([now, stages.get(int(lp), "?"), lp, pid, cpu, ws, wsp, pv, pvp, th, sysrow[1], sysrow[2], sysrow[3]])


def sampler(stop):
    while not stop.is_set():
        try:
            sample_once()
        except Exception as e:                  # a sampling failure must never stop the run
            say(f"sampler: {e!r}")
        stop.wait(INTERVAL)


def run_group(cmds, logs, names, cap, cwd, env):
    """start all, poll, kill any still running at the cap by exact pid; returns the exit codes (a string when killed at the cap)"""
    procs, t0 = [], time.time()
    for c, lg, nm in zip(cmds, logs, names):
        f = open(lg, "w")
        p = subprocess.Popen(c, cwd=cwd, env=env, stdout=f, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL)
        procs.append((p, f, nm)); _active[nm] = p.pid
        say(f"started {nm} pid {p.pid}: {' '.join(c)} > {lg}")
    rcs = [None] * len(procs)
    while any(r is None for r in rcs):
        for i, (p, f, nm) in enumerate(procs):
            if rcs[i] is None:
                rc = p.poll()
                if rc is not None:
                    rcs[i] = rc
                    say(f"{nm} pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
                elif time.time() - t0 > cap:
                    r = subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"], capture_output=True, text=True)
                    say(f"CAP {cap} s: killed {nm} pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
                    p.wait(); rcs[i] = "killed at the cap"
        if any(r is None for r in rcs):
            time.sleep(10)
    for nm in names:
        _active.pop(nm, None)
    return rcs


if "--selftest" in sys.argv:
    LOG, SAMPLES, INTERVAL = HERE + "/d185_driver_selftest.log", HERE + "/d185_driver_selftest_samples.csv", 5
    for f in (LOG, SAMPLES):
        open(f, "w").close(); os.remove(f) if f == SAMPLES else None
    stop = threading.Event()
    th = threading.Thread(target=sampler, args=(stop,), daemon=True); th.start()
    quick = [PY, "-c", "import time, numpy; a = numpy.ones((3000, 3000)); print('quick', flush=True); time.sleep(25)"]
    slow = [PY, "-c", "import time; print('slow', flush=True); time.sleep(600)"]
    rcs = run_group([quick, slow], [HERE + "/d185_selftest_a.log", HERE + "/d185_selftest_b.log"], ["quick", "slow"], 40, HERE, dict(os.environ))
    stop.set(); th.join(5)
    rows = list(csv.DictReader(open(SAMPLES)))
    left = subprocess.run(["powershell", "-NoProfile", "-Command", "(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match 'time.sleep\\(600\\)' } | Measure-Object).Count"], capture_output=True, text=True).stdout.strip()
    ok = rcs[0] == 0 and rcs[1] == "killed at the cap" and left == "0" and len(rows) >= 2 and any(r["stage"] == "quick" and float(r["ws_peak_gb"]) > 0.05 for r in rows)
    say(f"selftest: exit codes {rcs}; {len(rows)} sample rows; slow-child processes alive afterwards {left}; {'ok' if ok else 'WRONG'}")
    sys.exit(0 if ok else 1)

say("d185_driver_1025.py: the D 18.5 root; checking pins")
for fn, want in PINS:
    got = subprocess.run(["git", "hash-object", "--no-filters", fn], capture_output=True, text=True).stdout.strip()
    if got != want:
        say(f"REFUSE: {fn} is blob {got}, not {want}")
        sys.exit(2)
if os.path.exists(JS):
    say(f"REFUSE: {JS} exists (use a fresh name)")
    sys.exit(2)
head = subprocess.run(["git", "-C", WT_H, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
headd = subprocess.run(["git", "-C", WT_D, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
if head != "505d839940456a3d04321d75cf66cc3b5bc831c4" or headd != "48c36355d1ba64de4e3112ed968fd6c034384551":
    say(f"REFUSE: worktrees at {head} and {headd}")
    sys.exit(2)
os.makedirs(OUT + "/rows", exist_ok=True)
stop = threading.Event()
threading.Thread(target=sampler, args=(stop,), daemon=True).start()
base = dict(os.environ, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4", RAYON_NUM_THREADS="4", PYTHONDONTWRITEBYTECODE="1")
say(f"pins ok; hybrid: p4_hybrid.py {STUB} {STATE} {D}, 4 threads, BelowNormal, cap {CAP} s; guess 1.6771")
t0 = time.time()
rc = run_group([[PY, "-u", P4, STUB, STATE, D]], [OUT + "/rows/D18.5.log"], ["hybrid"], CAP, WT_H + "/solver/matter",
               dict(base, P4_WT_MATTER=WT_H + "/solver/matter", P4_OUT=JS))[0]
say(f"hybrid ended: {rc} after {time.time() - t0:.0f} s")
if rc != 0 or not os.path.exists(JS):
    say("hybrid gave no record: no verdict, no dd check")
    stop.set(); sys.exit(1)
rec = [json.loads(l) for l in open(JS) if l.strip()][-1]
for l in open(OUT + "/rows/D18.5.log", errors="replace"):
    if l.startswith("D ") or l.startswith("  lam"):
        open(LOG, "a").write(l)
if rec.get("lam") is None:
    say("hybrid found no root: no verdict, no dd check")
    stop.set(); sys.exit(1)
r = subprocess.run([PY, HERE + "/verdict_d185_1025.py", JS, D, "--between", "1.67,1.68", "--out", OUT + "/rows/verdict_D18.5.json"], capture_output=True, text=True)
open(OUT + "/rows/verdict_D18.5.log", "w").write(r.stdout + r.stderr)
for l in r.stdout.splitlines():
    say(l)
if r.returncode != 0:
    say("a hybrid check failed: the dd check is not run; the coordinator decides")
    stop.set(); sys.exit(1)
root = rec["lam"]
lo, hi = root - 0.02, root + 0.02
say(f"dd check: root {root!r}; dd points {lo!r} and {hi!r}; state blob 33c1a58b82229d55661cbd5e79d2c1fce0c0717c; cap {CAP} s each")
lojs, hijs = OUT + "/rows/ell_ddm_D18.5_lo.jsonl", OUT + "/rows/ell_ddm_D18.5_hi.jsonl"
cmds = [[PY, "-u", "ell_ddm.py", "det", STATE, D, KC, repr(x), "--noise", "1e-24,1e-20,1e-16", "--out", fn] for x, fn in ((lo, lojs), (hi, hijs))]
rcs = run_group(cmds, [OUT + "/rows/dd185_lo.log", OUT + "/rows/dd185_hi.log"], ["dd_lo", "dd_hi"], CAP, WT_D + "/solver/matter", base)
say(f"both dd processes ended: {rcs}")
r = subprocess.run([PY, HERE + "/read_ddB_1025.py", lojs, hijs, repr(root), JS], capture_output=True, text=True)
open(OUT + "/rows/dd185_reading.log", "w").write(r.stdout + r.stderr)
for l in r.stdout.splitlines():
    say(l)
stop.set()
say("d185_driver_1025.py done")

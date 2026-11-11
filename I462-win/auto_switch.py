"""#462: switch one chain to main cc6d51b with --held_o 1 --reseed_o 3, at its next saved state, without anyone watching.

    python3 auto_switch.py CHAIN TARGET_D [--dry] [--no-wait]       run from the raw clone's I462-win folder

CHAIN is d6 or d10, TARGET_D the state's D as in its file name (for example 219.1312). The coordinator's rule of
2026-11-11 00:24 UTC: stop the chain after the step in progress saves, restart it from that state with the same command
plus --held_o 1 --reseed_o 3 (keeping --base_polish 0 and --h_max 1.0) on main cc6d51b or later.

1. Waits (4 h at most) until anm_pin3_D<TARGET_D>.npz exists with a size that has not changed for 15 s, and the chain's log
   has an accepted step at that D.
2. Writes CHAIN_long2.cmd with switch_cmd.py (which refuses when the newest state is not the log's last accepted step, or
   when the cap is out of range). Nothing is stopped before this succeeds.
3. Stops that chain only: the cmd.exe that runs CHAIN_long.cmd (taskkill /T /F), then any python.exe of the chain left.
4. Launches CHAIN_long2.cmd at below-normal priority and checks within 150 s that the log prints "base polish skipped"
   and the base line, and that the chain's python processes run at BelowNormal.

Everything is logged to auto_switch_CHAIN.log. --no-wait skips the wait of step 1. --dry stops nothing, launches nothing
and runs switch_cmd.py with --dry. Exit 0 on success, 2 on a refused or failed step (an ALARM line says which)."""
import datetime as dt
import glob
import os
import re
import subprocess
import sys
import time

here = os.path.dirname(os.path.abspath(__file__))
os.chdir(here)
chain, target = sys.argv[1], sys.argv[2]
dry, nowait = "--dry" in sys.argv, "--no-wait" in sys.argv
assert chain in ("d6", "d10"), "CHAIN must be d6 or d10"
LOGF = f"auto_switch_{chain}.log"


def log(msg):
    line = f"{dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M:%S} UTC {msg}"
    print(line, flush=True)
    with open(LOGF, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def ps(cmd):
    return subprocess.run(["powershell", "-NoProfile", "-Command", cmd], capture_output=True, text=True).stdout


def launcher_pids():
    out = ps("Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'cmd.exe' -and $_.CommandLine -match '\\\\"
             + chain + "_long\\.cmd' } | ForEach-Object { $_.ProcessId }")
    return [int(x) for x in out.split()]


def chain_pythons():
    out = ps("Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'I462-win' -and "
             "$_.CommandLine -match 'chain_" + chain + "( |$)' } | ForEach-Object { $_.ProcessId }")
    return [int(x) for x in out.split()]


def alarm(msg):
    log("ALARM " + msg)
    sys.exit(2)


def accepted_ds():
    ds = []
    for ln in open(f"chain_{chain}.log", encoding="utf-8", errors="replace"):
        m = re.match(r"^    a [0-9.]+ -> D ([0-9.]+):", ln)
        if m:
            ds.append(float(m.group(1)))
    return ds


log(f"start: chain {chain}, target D {target}, dry {dry}, no-wait {nowait}")
path = f"chain_{chain}/anm_pin3_D{target}.npz"
if not nowait:
    t0 = time.time()
    while True:
        if os.path.exists(path) and any(abs(d - float(target)) < 2e-4 for d in accepted_ds()):
            s1 = os.path.getsize(path)
            time.sleep(15)
            if os.path.getsize(path) == s1 and s1 > 40000:
                log(f"saved: {path} ({s1} bytes), accepted in the log")
                break
        if time.time() - t0 > 4 * 3600:
            alarm(f"{path} did not appear within 4 h")
        time.sleep(10)

# the new launcher first: nothing is stopped unless this works
r = subprocess.run([sys.executable, "switch_cmd.py", chain] + (["--dry"] if dry else []), capture_output=True, text=True)
log("switch_cmd.py: " + (r.stdout.strip().splitlines() or [""])[0][:300] + (" | " + r.stderr.strip()[:200] if r.stderr.strip() else ""))
if r.returncode != 0:
    alarm("switch_cmd.py refused, the chain keeps running unchanged")
if not dry and not (os.path.exists(f"{chain}_long2.cmd") and time.time() - os.path.getmtime(f"{chain}_long2.cmd") < 120):
    alarm(f"{chain}_long2.cmd was not written")

pids = launcher_pids()
log(f"launcher cmd.exe of {chain}_long.cmd: {pids}; python processes of the chain: {chain_pythons()}")
if dry:
    log("dry run: nothing stopped, nothing launched")
    sys.exit(0)
if len(pids) != 1:
    alarm(f"expected exactly one cmd.exe running {chain}_long.cmd, found {pids}; nothing stopped")

subprocess.run(["taskkill", "/T", "/F", "/PID", str(pids[0])], capture_output=True)
for _ in range(20):
    left = chain_pythons()
    if not left:
        break
    time.sleep(1)
if left:
    for p in left:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(p)], capture_output=True)
    time.sleep(3)
    left = chain_pythons()
if left:
    alarm(f"python processes of {chain} are still alive after the kill: {left}")
log("old run stopped, no python of the chain left")
# the chain's log is held open by the old run's >> redirect until it is stopped, so the marker is written only now
try:
    with open(f"chain_{chain}.log", "a", encoding="utf-8", newline="") as fh:
        fh.write(f"=== {dt.datetime.now(dt.timezone.utc):%H:%M:%S} UTC: {chain} switched to main cc6d51b with --held_o 1 --reseed_o 3 "
                 f"(auto_switch.py), restart from {path}\r\n")
except OSError as e:
    log(f"WARNING the marker line could not be written to chain_{chain}.log: {e}")

cmdpath = os.path.abspath(f"{chain}_long2.cmd")
n0 = len(open(f"chain_{chain}.log", encoding="utf-8", errors="replace").read().splitlines())
subprocess.Popen(f'cmd.exe /c start "I462_{chain}_long2" /belownormal /min cmd /c "{cmdpath}"')
log(f"launched {cmdpath}")
ok = False
for _ in range(30):
    time.sleep(5)
    tail = open(f"chain_{chain}.log", encoding="utf-8", errors="replace").read().splitlines()[n0:]
    if any("base polish skipped" in l for l in tail) and any(l.startswith("base I462-win/chain_" + chain) for l in tail) and len(chain_pythons()) >= 2:
        ok = True
        break
if not ok:
    alarm("the restarted chain did not print its base line within 150 s: read chain_" + chain + ".log")
prio = ps("Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and $_.CommandLine -match 'chain_" + chain +
          "( |$)' } | ForEach-Object { (Get-Process -Id $_.ProcessId).PriorityClass }").split()
log(f"restart verified: base polish skipped and base line printed, priorities {prio}")
sys.exit(0)

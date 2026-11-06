# kills the T132 probe tree if its python processes together pass 10 GB working set, every 20 s until t132.exit
import os, subprocess, sys, time
here = os.path.dirname(os.path.abspath(__file__))
def rss():
    out = subprocess.run(["powershell", "-NoProfile", "-Command",
        "Get-CimInstance Win32_Process | ? { $_.CommandLine -match 'lowD_plan_probe' } | % { '{0} {1}' -f $_.ProcessId, $_.WorkingSetSize }"],
        capture_output=True, text=True).stdout.split("\n")
    pids = [l.split() for l in out if l.strip()]
    return sum(int(w) for _, w in pids) / 2**30, [p for p, _ in pids]
peak = 0.0
while not os.path.exists(os.path.join(here, "t132.exit")):
    g, pids = rss()
    peak = max(peak, g)
    open(os.path.join(here, "guard.peak"), "w").write(f"peak {peak:.2f} GB, now {g:.2f} GB, {time.strftime('%H:%M:%S')}\n")
    if g > 10:
        for p in pids: subprocess.run(["taskkill", "/F", "/T", "/PID", p], capture_output=True)
        open(os.path.join(here, "guard.killed"), "w").write(f"killed at {g:.2f} GB\n")
        break
    time.sleep(20)

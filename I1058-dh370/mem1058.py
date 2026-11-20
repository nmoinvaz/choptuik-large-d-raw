#!/usr/bin/env python3
"""#1058 on dh370: alert-only memory sampler beside ks_chain3b. usage: python3 -I mem1058.py LOG ALERTS EXITS [--poll 5]
Every poll one line: available, used, swap, the build unit's cgroup (current, peak), the largest rustc/cargo/maturin RSS, the chain's anm_run RSS, load.
When MemAvailable falls under 4096 MB (within 4 GB of MemTotal) an ALERT line goes to ALERTS and hc to the coordinator, at most every 10 min.
It never stops or signals anything. It ends when EXITS has a 'checks done' line or a 'build exit' line with a non-zero code."""
import os, subprocess, sys, time, re
log, alerts, exits = sys.argv[1:4]
poll = float(sys.argv[sys.argv.index("--poll") + 1]) if "--poll" in sys.argv else 5.0
UNIT = "i1058b"
THRESH = int(os.environ.get("MEM1058_THRESH", "4096"))   # a selftest lowers or raises it; NOHC=1 skips the hc message
def meminfo():
    d = {}
    for l in open("/proc/meminfo"):
        k, v = l.split(":"); d[k] = int(v.split()[0]) // 1024
    return d
def cg_path():
    r = subprocess.run(["systemctl", "--user", "show", "-p", "ControlGroup", "--value", UNIT], capture_output=True, text=True).stdout.strip()
    return "/sys/fs/cgroup" + r if r else None
def rd(p):
    try: return int(open(p).read().split()[0]) // (1024 * 1024)
    except Exception: return -1
def rss_by_name():
    big, chain = (0, ""), 0
    for pid in filter(str.isdigit, os.listdir("/proc")):
        try:
            cmd = open(f"/proc/{pid}/cmdline", "rb").read().replace(b"\0", b" ").decode(errors="replace")
            st = open(f"/proc/{pid}/status").read()
            rss = int(re.search(r"VmRSS:\s+(\d+)", st).group(1)) // 1024
        except Exception:
            continue
        exe = cmd.split(" ")[0].rsplit("/", 1)[-1]
        if exe in ("rustc", "cargo", "maturin", "cc", "ld", "lld") and rss > big[0]: big = (rss, exe)
        if "anm_run.py" in cmd and "python" in exe: chain = max(chain, rss)
    return big, chain
last_hc = 0.0
mn_av, mx_cg = 10**9, 0
while True:
    m = meminfo(); cg = cg_path()
    cur, pk = (rd(cg + "/memory.current"), rd(cg + "/memory.peak")) if cg else (-1, -1)
    (rs, nm), ch = rss_by_name()
    av = m["MemAvailable"]; used = m["MemTotal"] - av; sw = m["SwapTotal"] - m["SwapFree"]
    mn_av, mx_cg = min(mn_av, av), max(mx_cg, pk)
    with open(log, "a") as f:
        f.write(f"{time.strftime('%F %T', time.gmtime())} UTC avail {av} used {used} swap {sw} | build cg {cur} peak {pk} | biggest {nm} {rs} | chain python {ch} | load {os.getloadavg()[0]:.2f} | min avail {mn_av} max cg peak {mx_cg} (MB)\n")
    if av < THRESH:
        msg = f"{time.strftime('%F %T', time.gmtime())} UTC ALERT: MemAvailable {av} MB < {THRESH} MB (within 4 GB of MemTotal {m['MemTotal']} MB), build cgroup {cur} MB, biggest {nm} {rs} MB, chain python {ch} MB, swap {sw} MB"
        open(alerts, "a").write(msg + "\n")
        if not os.environ.get("NOHC") and time.time() - last_hc >= 600:
            last_hc = time.time()
            subprocess.run(["hc", "send", "nathans-macbook-air-m5-3/t5", "dh370 #1058 alert: " + msg.split("UTC ", 1)[1] + " (watcher only logs, nothing stopped)"], capture_output=True, timeout=60)
    try: ex = open(exits).read()
    except Exception: ex = ""
    if "checks done" in ex or re.search(r"build exit [1-9]", ex): break
    time.sleep(poll)

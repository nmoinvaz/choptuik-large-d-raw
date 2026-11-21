#!/usr/bin/env python3
"""#1070 macm3b: resource log of the lowD_gamma.py process, alert-only (Nathan's rule: no watcher kills or stops anything).
Usage: watch_1070.py MODE [SECONDS_BETWEEN]. Reads the child pid from run_MODE.log's first line (capped_run: child pid N); every
poll appends 'time, rss GB, %cpu, free memory %, free disk GiB, load' to res_MODE.log. hc to the coordinator once per crossing
when free disk < 3 GiB or free memory < 8%. On the process's end writes res_summary_MODE.txt (peak rss, mean and max %cpu over the
polls, min free memory %, min free disk)."""
import datetime, os, re, shutil, subprocess, sys, time
mode = sys.argv[1]; dt = float(sys.argv[2]) if len(sys.argv) > 2 else 60
O = os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1070-macm3")
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
def freemem():
    r = subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout
    m = re.search(r"free percentage: (\d+)%", r); return int(m.group(1)) if m else -1
def alert(msg):
    subprocess.run(["hc", "send", "nathans-macbook-air-m5-3/t5", f"macm3b watcher #1070: {msg}"], capture_output=True)
while not (os.path.exists(f"{O}/run_{mode}.log") and open(f"{O}/run_{mode}.log").readline().strip()): time.sleep(2)
pid = int(re.search(r"child pid (\d+)", open(f"{O}/run_{mode}.log").readline()).group(1))
rows = []; low_d = low_m = False
with open(f"{O}/res_{mode}.log", "a") as lg:
    lg.write(f"# {now()} watch_1070.py {mode}: pid {pid}, poll {dt:.0f} s; columns: time, rss_GB, cpu_pct, free_mem_pct, free_disk_GiB, load1\n")
    while alive(pid):
        r = subprocess.run(["ps", "-o", "rss=,%cpu=", "-p", str(pid)], capture_output=True, text=True).stdout.split()
        if len(r) == 2:
            rss = int(r[0]) / 1048576; cpu = float(r[1]); fm = freemem(); fd = shutil.disk_usage("/System/Volumes/Data").free / 2**30
            rows.append((rss, cpu, fm, fd)); lg.write(f"{now()} {rss:.2f} {cpu:.1f} {fm} {fd:.1f} {os.getloadavg()[0]:.2f}\n"); lg.flush()
            if fd < 3 and not low_d: low_d = True; alert(f"free disk {fd:.1f} GiB < 3 GiB")
            if 0 <= fm < 8 and not low_m: low_m = True; alert(f"free memory {fm}% < 8%")
        time.sleep(dt)
    if rows:
        with open(f"{O}/res_summary_{mode}.txt", "w") as f:
            f.write(f"{mode} pid {pid}, {len(rows)} polls of {dt:.0f} s, ended {now()}\npeak rss {max(r[0] for r in rows):.2f} GB\n"
                    f"cpu %: mean {sum(r[1] for r in rows)/len(rows):.0f}, max {max(r[1] for r in rows):.0f} (ps %cpu of the process, 100 = one core)\n"
                    f"min free memory {min(r[2] for r in rows)}%, min free disk {min(r[3] for r in rows):.1f} GiB\n")

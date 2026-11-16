import os, sys, time, subprocess, signal, datetime
root = int(sys.argv[1]); out = sys.argv[2]
SWAP_MAX_MB = 15000; DISK_MIN_GB = 5.0
def tree(r):
    rows = subprocess.run(["ps", "-axo", "pid=,ppid=,rss=,comm="], capture_output=True, text=True).stdout.splitlines()
    ch = {}; info = {}
    for l in rows:
        p = l.split(None, 3)
        if len(p) < 4: continue
        pid, ppid, rss = int(p[0]), int(p[1]), int(p[2])
        info[pid] = (rss, os.path.basename(p[3])); ch.setdefault(ppid, []).append(pid)
    seen = []; st = [r]
    while st:
        x = st.pop()
        if x in info: seen.append(x)
        st.extend(ch.get(x, []))
    return seen, info
def swap_mb():
    s = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True).stdout
    return float(s.split("used =")[1].split("M")[0])
f = open(out, "a"); f.write("utc,tree_rss_MB,procs,biggest_proc,biggest_rss_MB,swap_used_MB,disk_free_GB,load1\n"); f.flush()
peak = 0.0
while True:
    pids, info = tree(root)
    if not pids: break
    tot = sum(info[p][0] for p in pids) / 1024
    big = max(pids, key=lambda p: info[p][0])
    sw = swap_mb(); sv = os.statvfs(os.path.expanduser("~")); free = sv.f_bavail * sv.f_frsize / 1e9
    ld = os.getloadavg()[0]
    peak = max(peak, tot)
    f.write(f"{datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')},{tot:.0f},{len(pids)},{info[big][1]},{info[big][0]/1024:.0f},{sw:.0f},{free:.1f},{ld:.2f}\n"); f.flush()
    if sw > SWAP_MAX_MB or free < DISK_MIN_GB:
        f.write(f"ABORT swap {sw:.0f} MB or disk {free:.1f} GB at {datetime.datetime.now(datetime.timezone.utc).strftime('%H:%M:%S')}: killing the build tree\n"); f.flush()
        for p in sorted(pids, reverse=True):
            try: os.kill(p, signal.SIGTERM)
            except ProcessLookupError: pass
        break
    time.sleep(5)
f.write(f"END peak tree rss {peak:.0f} MB\n"); f.close()

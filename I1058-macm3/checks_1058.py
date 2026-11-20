"""#1058 macm3b: the four stored-reference checks of hp at main 7ca74dd5, one after the other, beside #1008's run2. Alert-only sampler:
it appends the running check's process tree to mem_checks.log every 30 s and runs `hc send` at under 3 GiB free disk or under 8% free memory, and signals no process.
Usage: checks_1058.py. Each check's output is checks/<name>.log, its exit and wall time go to exits_1058.txt."""
import os, re, sys, time, subprocess, datetime
O = os.path.dirname(os.path.abspath(__file__))
R = os.path.expanduser("~/Source/choptuik-large-d-raw-903")
W = os.path.expanduser("~/Source/choptuik-large-d-1058/hp")
V = os.path.expanduser("~/Source/venv-macm3-1058")
RUN2 = 98367
CHECKS = [("ref", ["ref", f"--compare={R}/T81/ref_main.json", "--Ms=48,64,80"], 0),
          ("scaled", ["scaled", f"--compare={R}/T81/scaled_main.json"], 0),
          ("jets", ["jets", f"--compare={R}/anm-mac/jets_inputs/jets_inputs.json"], 0),
          ("jets_mutate_kappa", ["jets", f"--compare={R}/anm-mac/jets_inputs/jets_inputs.json", "--mutate=kappa"], 1)]
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def log(msg):
    with open(f"{O}/exits_1058.txt", "a") as f: f.write(f"1058m {msg} {now()}\n")
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
def rows():
    out = []
    for l in subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,rss=,comm="], capture_output=True, text=True).stdout.splitlines():
        f = l.split(None, 4)
        if len(f) == 5 and "<defunct>" not in f[4]: out.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]), f[4]))
    return out
def group(pg):
    rs = rows(); kids = {x[0] for x in rs if x[2] == pg}; ch = True
    while ch:
        ch = False
        for pid, pp, g, rss, cm in rs:
            if pp in kids and pid not in kids: kids.add(pid); ch = True
    return [x for x in rs if x[0] in kids]
def free_pct():
    m = re.search(r"free percentage: (\d+)%", subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout)
    return int(m.group(1)) if m else -1
def disk_gib():
    s = os.statvfs("/System/Volumes/Data"); return s.f_bavail * s.f_frsize / 2**30
def alert(txt):
    r = subprocess.run(["hc", "send", "nathans-macbook-air-m5-3/t5", f"macm3b #1058 ALERT (alert only, nothing stopped): {txt}"], capture_output=True, text=True)
    log(f"ALERT sent (hc exit {r.returncode}): {txt}")
env = dict(os.environ, VIRTUAL_ENV=V, PATH=f"{V}/bin:" + os.environ["PATH"], PIP_NO_CACHE_DIR="1")
os.makedirs(f"{O}/checks", exist_ok=True)
last = {}
with open(f"{O}/mem_checks.log", "a") as ml:
    ml.write("time_utc check tree_rss_MB biggest_proc free_pct disk_free_GiB run2_alive\n")
    for name, args, want in CHECKS:
        t0 = time.time()
        lf = open(f"{O}/checks/{name}.log", "w")
        cmd = ["caffeinate", "-is", "nice", "-n", "19", f"{V}/bin/python3", "highm_check.py"] + args
        p = subprocess.Popen(cmd, cwd=W, env=env, stdout=lf, stderr=subprocess.STDOUT, start_new_session=True)
        log(f"check {name} started: cd hp && python3 highm_check.py {' '.join(a.replace(R, '$RAW') for a in args)} (nice 19, default 2 threads), pgid {p.pid}")
        peak = 0
        while p.poll() is None:
            g = group(p.pid); tot = sum(x[3] for x in g) / 1024; big = max(g, key=lambda x: x[3]) if g else None
            fp, dk = free_pct(), disk_gib(); peak = max(peak, tot)
            ml.write(f"{now()} {name} {tot:.0f} {big[4].split('/')[-1] if big else '-'} {fp} {dk:.2f} {int(alive(RUN2))}\n"); ml.flush()
            for key, bad, txt in (("disk", dk < 3.0, f"data volume {dk:.2f} GiB free"), ("mem", 0 <= fp < 8, f"system free memory {fp}%")):
                if bad and time.time() - last.get(key, 0) > 1800:
                    alert(txt + f" during check {name}; its tree {tot / 1024:.1f} GiB, run2 alive {alive(RUN2)}"); last[key] = time.time()
            time.sleep(30)
        rc = p.wait(); lf.close()
        ok = (rc == want)
        log(f"check {name} exit {rc} (wanted {want}: {'as wanted' if ok else 'NOT AS WANTED'}), wall {time.time() - t0:.0f} s, peak tree {peak / 1024:.2f} GiB")
log("checks_1058.py ends")

"""#1058 macm3b: alert-only watcher for the hp build (the coordinator's rule: no watcher stops a process for memory or disk).
Usage: watch_1058.py PGID. Appends to mem.log every 30 s, runs `hc send` when the data volume has under 3 GiB free or the system's free memory is under 8%
(once per episode, again after 30 min if it lasts), and when the build's process group is gone writes build_info.txt and an exits_1058.txt line.
It sends no signal to any process."""
import os, re, sys, time, glob, hashlib, subprocess, datetime
O = os.path.dirname(os.path.abspath(__file__))
V = os.path.expanduser("~/Source/venv-macm3-1058")
PG = int(sys.argv[1])
TEST = bool(os.environ.get("W1058_TEST"))   # the alert check: thresholds nothing meets, no hc call
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def log(msg):
    with open(f"{O}/exits_1058.txt", "a") as f: f.write(f"1058m {msg} {now()}\n")
def ps_rows():
    rows = []
    for l in subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,rss=,comm="], capture_output=True, text=True).stdout.splitlines():
        f = l.split(None, 4)
        if len(f) == 5: rows.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]), f[4]))
    return rows
def group(rows):
    kids = {x[0] for x in rows if x[2] == PG}; ch = True
    while ch:
        ch = False
        for pid, pp, pg, rs, cm in rows:
            if pp in kids and pid not in kids: kids.add(pid); ch = True
    return [x for x in rows if x[0] in kids and "<defunct>" not in x[4]]   # a zombie is gone
def free_pct():
    m = re.search(r"free percentage: (\d+)%", subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout)
    return int(m.group(1)) if m else -1
def disk_gib():
    s = os.statvfs("/System/Volumes/Data"); return s.f_bavail * s.f_frsize / 2**30
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
def alert(txt):
    if TEST: log(f"ALERT (test, hc not called): {txt}"); return
    r = subprocess.run(["hc", "send", "nathans-macbook-air-m5-3/t5", f"macm3b #1058 ALERT (alert only, nothing stopped): {txt}"], capture_output=True, text=True)
    log(f"ALERT sent (hc exit {r.returncode}): {txt}")
log(f"watch_1058.py attached to the build's process group {PG}; alert only (replaces build_1058.py's guard, which never fired and stopped nothing)")
last = {}
with open(f"{O}/mem.log", "a") as ml:
    while True:
        g = group(ps_rows())
        if not g: break
        tot = sum(x[3] for x in g) / 1024; big = max(g, key=lambda x: x[3]); fp = free_pct(); dk = disk_gib()
        ml.write(f"{now()} {tot:.0f} {big[3] / 1024:.0f} {big[4]} {fp} {dk:.2f} {int(alive(98367))}\n"); ml.flush()
        for key, bad, txt in (("disk", dk < (1e6 if TEST else 3.0), f"data volume {dk:.2f} GiB free"), ("mem", 0 <= fp < (101 if TEST else 8), f"system free memory {fp}%")):
            if bad and time.time() - last.get(key, 0) > 1800:
                alert(txt + f"; build tree {tot / 1024:.1f} GiB, run2 alive {alive(98367)}"); last[key] = time.time()
        time.sleep(30)
txt = open(f"{O}/build.log", errors="replace").read()
m = re.search(r"(\d+)\s+maximum resident set size", txt)
rl = re.search(r"([0-9.]+)\s+real\s+([0-9.]+)\s+user\s+([0-9.]+)\s+sys", txt)
ok = re.search(r"^hpkernel (\S+) multidouble (\S+)\s*$", txt, re.M)
t = [l for l in open(f"{O}/mem.log").read().splitlines()[1:] if l.strip()]
info = [f"build.sh wall {float(rl.group(1)):.0f} s ({float(rl.group(1)) / 60:.1f} min), user {rl.group(2)} s, sys {rl.group(3)} s (time -l)" if rl else "time -l real: not found",
        f"build.sh exit: the driver was replaced mid-build, so the status is read from build.log: the import line {'is present: hpkernel ' + ok.group(1) + ' multidouble ' + ok.group(2) if ok else 'is MISSING'}",
        f"time -l maximum resident set size of the largest process: {int(m.group(1)) / 2**30:.2f} GiB" if m else "time -l maximum resident set size: not found",
        f"sampled peak of the build's process tree (30 s samples, {len(t)} samples in mem.log): {max(int(l.split()[3]) for l in t) / 1024:.2f} GiB; lowest free memory {min(int(l.split()[-3]) for l in t)}%, lowest disk free {min(float(l.split()[-2]) for l in t):.2f} GiB"]
env = dict(os.environ, VIRTUAL_ENV=V, PATH=f"{V}/bin:" + os.environ["PATH"])
for cmd in ([f"{V}/bin/python3", "-c", "import hpkernel, multidouble, sys; print('hpkernel', hpkernel.isa(), 'multidouble', multidouble.isa(), 'python', sys.version.split()[0]); print(hpkernel.__file__)"], ["rustc", "--version"], [f"{V}/bin/maturin", "--version"], [f"{V}/bin/python3", "-m", "pip", "list", "--format=freeze"]):
    q = subprocess.run(cmd, env=env, capture_output=True, text=True)
    info.append(f"$ {' '.join(cmd[-2:] if cmd[1] == '-c' else cmd)} -> exit {q.returncode}\n" + (q.stdout + q.stderr).strip())
for f in glob.glob(f"{V}/lib/python3*/site-packages/multidouble-*.dist-info/direct_url.json"):
    info.append(f"{os.path.basename(os.path.dirname(f))}/direct_url.json: {open(f).read().strip()}")
for f in glob.glob(f"{V}/lib/python3*/site-packages/hpkernel/_hpkernel*.so"):
    info.append(f"{os.path.basename(f)} sha1 {hashlib.sha1(open(f, 'rb').read()).hexdigest()[:12]}")
open(f"{O}/build_info.txt", "w").write("\n".join(info) + "\n")
log("build process group gone; build_info.txt written: " + info[0] + "; " + info[1])

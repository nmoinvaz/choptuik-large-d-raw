"""#1058 macm3b: hp/build.sh at main 7ca74dd5 beside #1008's run2, with a memory and disk guard that kills only the build's own process group.
Usage: build_1058.py. Writes build.log, mem.log, build_info.txt and appends to exits_1058.txt in this folder."""
import os, re, sys, time, glob, signal, hashlib, subprocess, datetime
O = os.environ.get("B1058_OUT") or os.path.dirname(os.path.abspath(__file__))
TEST = bool(os.environ.get("B1058_TEST"))   # the guard check: a sleep for a build and a disk threshold nothing meets
W = os.path.expanduser("~/Source/choptuik-large-d-1058/hp")
V = os.path.expanduser("~/Source/venv-macm3-1058")
RUN2 = 98367
def now(): return datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
def log(msg):
    with open(f"{O}/exits_1058.txt", "a") as f: f.write(f"1058m {msg} {now()}\n")
env = dict(os.environ, VIRTUAL_ENV=V, PATH=f"{V}/bin:" + os.environ["PATH"], CARGO_PROFILE_RELEASE_LTO="false", CARGO_PROFILE_RELEASE_CODEGEN_UNITS="16", CARGO_BUILD_JOBS="2", PIP_NO_CACHE_DIR="1")
env.pop("PYTHONHOME", None)
r = subprocess.run([f"{V}/bin/python3", "-m", "pip", "uninstall", "-y", "multidouble"], env=env, capture_output=True, text=True)
open(f"{O}/pip_uninstall.log", "w").write(r.stdout + r.stderr)
log(f"pip uninstall -y multidouble exit {r.returncode} ({(r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else 'no output'})")
t0 = time.time()
bl = open(f"{O}/build.log", "w")
p = subprocess.Popen(["sleep", "300"] if TEST else ["caffeinate", "-is", "nice", "-n", "19", "/usr/bin/time", "-l", "bash", "build.sh"], cwd=W, env=env, stdout=bl, stderr=subprocess.STDOUT, start_new_session=True)
log(f"build started: hp/build.sh at 7ca74dd5 in {W}, CARGO_PROFILE_RELEASE_LTO=false CODEGEN_UNITS=16 CARGO_BUILD_JOBS=2, nice 19, pgid {p.pid}")
def tree(root):
    out = subprocess.run(["ps", "-axo", "pid=,ppid=,pgid=,rss=,comm="], capture_output=True, text=True).stdout.splitlines()
    rows = []
    for l in out:
        f = l.split(None, 4)
        if len(f) == 5: rows.append((int(f[0]), int(f[1]), int(f[2]), int(f[3]), f[4]))
    kids = {root}; ch = True
    while ch:
        ch = False
        for pid, pp, pg, rs, cm in rows:
            if pp in kids and pid not in kids: kids.add(pid); ch = True
    sel = [x for x in rows if x[0] in kids or x[2] == root]
    return sum(x[3] for x in sel) / 1024, max(sel, key=lambda x: x[3]) if sel else None
def free_pct():
    m = re.search(r"free percentage: (\d+)%", subprocess.run(["memory_pressure"], capture_output=True, text=True).stdout)
    return int(m.group(1)) if m else -1
def disk_gib():
    s = os.statvfs("/System/Volumes/Data"); return s.f_bavail * s.f_frsize / 2**30
def alive(pid):
    try: os.kill(pid, 0); return True
    except OSError: return False
peak = 0.0; peak_t = None; low = 0; killed = None
with open(f"{O}/mem.log", "w") as ml:
    ml.write("time_utc tree_rss_MB biggest_rss_MB biggest_proc free_pct disk_free_GiB run2_alive\n")
    while p.poll() is None:
        tot, big = tree(p.pid); fp = free_pct(); dk = disk_gib()
        if tot > peak: peak, peak_t = tot, now()
        ml.write(f"{now()} {tot:.0f} {(big[3] / 1024 if big else 0):.0f} {big[4] if big else '-'} {fp} {dk:.2f} {int(alive(RUN2))}\n"); ml.flush()
        low = low + 1 if 0 <= fp < 8 else 0
        if dk < (1e6 if TEST else 3.0) or low >= 2:
            killed = f"disk free {dk:.2f} GiB, free memory {fp}%"
            log(f"GUARD: {killed}; SIGTERM to the build's process group {p.pid}")
            os.killpg(p.pid, signal.SIGTERM)
            for _ in range(12):
                time.sleep(5)
                if p.poll() is not None: break
            if p.poll() is None: os.killpg(p.pid, signal.SIGKILL)
            break
        time.sleep(30)
rc = p.wait(); wall = time.time() - t0; bl.close()
txt = open(f"{O}/build.log", errors="replace").read()
m = re.search(r"(\d+)\s+maximum resident set size", txt)
info = [f"build.sh exit {rc}, wall {wall:.0f} s ({wall / 60:.1f} min)" + (f", GUARD stop: {killed}" if killed else "")]
info.append(f"time -l maximum resident set size of the largest process: {int(m.group(1)) / 2**30:.2f} GiB" if m else "time -l maximum resident set size: not found")
info.append(f"sampled peak of the build's process tree (30 s samples): {peak / 1024:.2f} GiB at {peak_t}")
for cmd in ([f"{V}/bin/python3", "-c", "import hpkernel, multidouble, sys; print('hpkernel', hpkernel.isa(), 'multidouble', multidouble.isa(), 'python', sys.version.split()[0]); print(hpkernel.__file__)"], ["rustc", "--version"], [f"{V}/bin/maturin", "--version"], [f"{V}/bin/python3", "-m", "pip", "list", "--format=freeze"]):
    q = subprocess.run(cmd, env=env, capture_output=True, text=True)
    info.append(f"$ {' '.join(cmd[-2:] if cmd[1] == '-c' else cmd)} -> exit {q.returncode}\n" + (q.stdout + q.stderr).strip())
for f in glob.glob(f"{V}/lib/python3*/site-packages/multidouble-*.dist-info/direct_url.json"):
    info.append(f"{os.path.basename(os.path.dirname(f))}/direct_url.json: {open(f).read().strip()}")
for f in glob.glob(f"{V}/lib/python3*/site-packages/hpkernel/_hpkernel*.so"):
    info.append(f"{os.path.basename(f)} sha1 {hashlib.sha1(open(f, 'rb').read()).hexdigest()[:12]}")
open(f"{O}/build_info.txt", "w").write("\n".join(info) + "\n")
log(f"build ended: exit {rc}, wall {wall:.0f} s, peak tree {peak / 1024:.2f} GiB" + (f", GUARD stop: {killed}" if killed else ""))
sys.exit(rc)

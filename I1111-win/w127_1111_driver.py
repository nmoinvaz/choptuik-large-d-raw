#!/usr/bin/env python3
"""#1111 winb (t5's order, hc 2026-11-28 10:58 UTC; #1111 body and comment 7231937181): which band of the difference between R2's state and a chord state
on R2's 8351-step map moves det M, at k_c 127, D 23.0, lambda 0.122, with the Rust block 12. Three steps, one driver, nothing runs in my terminal (started by WMI):
  1. jac      python i1101_weakdir.py jac R2REC R2STATE 23.0 I1111-local/jac_r2.npz --pin=25ba3a91,9111bfca              OPENBLAS_NUM_THREADS=4, cap 14400 s
  2. svd      python i1101_weakdir.py svd jac_r2.npz svd_r2.npz                                                          4 threads, cap 7200 s
  3. detparts python i1101_weakdir.py detparts svd_r2.npz R2REC R2STATE CHORD035 23.0 0.122 --b12=rust --b12_threads=4   OPENBLAS_NUM_THREADS=1, RAYON_NUM_THREADS=4,
              D18_DIR the worktree's solver/matter, PYTHONPATH my ellrs (i1102_1025/site), cap 28800 s
Code: worktree choptuik-i1111 = wip/i1101-weakdir at 0ee1d95d (detached), from solver/matter; venv-md510; BelowNormal, no window, killed by the exact pid at a cap.
Order of the driver (any failure stops it with an hc to t5, later steps not run, exit 2):
  0. pins: the worktree HEAD, the solver files (i1101_weakdir.py 472e820d, d18_secant.py 9706e506, ell_b12rs.py a1fff74f, ell_fastm.py 3431e32e, ell_ddm.py 64c4337f, dss_ell.py, ell_dd.py,
     ddnp.py, ell_fastdd.py), my ellrs build, the four raw inputs by blob (R2 state 25ba3a91, R2 record 9111bfca, chord035 state 205b6a90, its map.json 3bed6d4d), the chord map has the record's step
     count (8351); selftests: d18_secant.py selftest 0 and its three controls 1 1 1, ell_b12rs.py selftest 0 and --mutate=nolam, --mutate=harm 1 1;
  1. jac: exit 0 (the tool exits 3 if the system is not the record system or a pin differs), its log says "the record system", 8351 steps, a square J;
  2. svd: exit 0; then the tool's own `planted` check exit 0 and its --mutate=basis control exit 1; then `coords` of the chord state in R2's bands (extra, seconds);
  3. detparts: exit 0 and the five cases A, A + P_null, A + P_weak, A + P_strong, B with sign, ln|det|, dln, robust; the three parts' norms squared add up to |z_B - z_A|^2 (1e-9, from my own V^T on the stored SVD; the tool's three-digit prints agree to 6e-3);
     the table (detparts_table.txt) names the part whose sign equals B's and whose ln|det| is within 0.1 of B's, if any (my reading rule, written before the run; t5 rules).
Caps: cap_seconds.txt in this folder (lines like jac=14400, svd=7200, detparts=28800) overrides a cap at every poll, only on t5's word. hc to t5 at the end of each step and at half a cap.
The npz files stay in I1111-local (outside the raw clones). A sampler (60 s), an alert-only memory watcher and a keep-awake helper run beside it; nothing kills on memory.
usage: w127_1111_driver.py [--dry] [--out=DIR] [--loc=DIR]    (--dry: step 0 only, prints the three commands, starts nothing; K1111_FAKE=ok|jacfail|badparts replaces the three steps by stand-ins, for the tests)"""
import datetime, json, os, re, subprocess, sys, time

import numpy as np

S = os.path.dirname(os.path.abspath(__file__)).replace("\\", "/")
_o = {a[2:].split("=", 1)[0]: a[2:].split("=", 1)[1] for a in sys.argv if a.startswith("--") and "=" in a}
OUT = _o.get("out", S + "/I1111-win").replace("\\", "/")
LOC = _o.get("loc", "C:/Users/nathan/Source/I1111-local").replace("\\", "/")
IN = S + "/inputs"
WT = "C:/Users/nathan/Source/choptuik-i1111"
WTM = WT + "/solver/matter"
SITE = "C:/Users/nathan/Source/i1102_1025/site"          # ellrs (my #1102 build, cp314, avx512), on PYTHONPATH
PY = "C:/Users/nathan/Source/venv-md510/Scripts/python.exe"
HC = "C:/Users/nathan/AppData/Local/Programs/herdr-core/hc.exe"
COORD = "nathans-macbook-air-m5-3/t5"
DRY = "--dry" in sys.argv
FAKE = os.environ.get("K1111_FAKE", "")
QUIET = DRY or bool(FAKE)
D, LAM = "23.0", "0.122"
REC, STATE, CHORD, CMAP = IN + "/r2_record.jsonl", IN + "/r2_state.npy", IN + "/chord035_state.npy", IN + "/chord035_state.map.json"
JAC, SVD = LOC + "/jac_r2.npz", LOC + "/svd_r2.npz"
CAPS = {"jac": 14400, "svd": 7200, "detparts": 28800}
NOTIFY = {"jac": 7200, "svd": 3600, "detparts": 14400}
SFX = ".dry" if DRY else (".fake" if FAKE else "")
LOG = OUT + "/driver_w.log" + SFX
PINS = [(WTM + "/i1101_weakdir.py", "472e820df216e1d7f4ada8eb2f8312fb4e2178a7", True), (WTM + "/d18_secant.py", "9706e506111357e5e6a3f1bccd60154ac3d17cbc", True),
        (WTM + "/ell_b12rs.py", "a1fff74ff07c20bdee50d210c8b8fb1753fcf5ef", True), (WTM + "/ell_fastm.py", "3431e32e39541b4869b1179939e1a0af65ead666", True),
        (WTM + "/ell_ddm.py", "64c4337f490771c98e6deccfd0371a45ea4599f2", True), (WTM + "/dss_ell.py", "5d28c19e17efa6b0103cb81d650891706605532d", True),
        (WTM + "/ell_dd.py", "7e58fcbc2288eca8f8f1ebfc36f7250a328b0c4e", True), (WTM + "/ddnp.py", "9b1fb195d0fa95d5dd7abd1083ac9b36fef04869", True),
        (WTM + "/ell_fastdd.py", "237ebfdd984b280416a53d8c328131db69c23b4e", True),
        (SITE + "/ellrs/ellrs.cp314-win_amd64.pyd", "ddd5a08281f4aa325bd8564f08f9f2c3cebba33d", False), (SITE + "/ellrs/__init__.py", "76c7cfbc8fdfe90adb0debb60ac2d4754974cb1d", False),
        (STATE, "25ba3a91", False), (REC, "9111bfca", False), (CHORD, "205b6a90", False), (CMAP, "3bed6d4d", False)]


def now():
    return datetime.datetime.now(datetime.timezone.utc)


def say(m):
    line = f"== {now():%Y-%m-%d %H:%M:%S} {m}"
    print(line, flush=True)
    open(LOG, "a").write(line + "\n")


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def hc(m):
    msg = f"winb ({now():%H:%M} UTC), #1111 k_c 127 D 23.0 lambda {LAM} (R2 against chord035 on R2's map): {m}"
    if QUIET:
        say("hc (not sent in a dry or fake run): " + msg)
    else:
        sh([HC, "send", COORD, msg])


def stop(m):
    say("STOP: " + m)
    hc("stopped: " + m)
    sys.exit(2)


os.makedirs(OUT + "/rows", exist_ok=True)
os.makedirs(LOC, exist_ok=True)
say(f"w127_1111_driver.py{' (dry run)' if DRY else ''}{' (FAKE=' + FAKE + ')' if FAKE else ''}: which band of the R2 to chord035 difference moves det M, k_c 127, D {D}, lambda {LAM}; checking pins")

# ---- step 0: pins, selftests
env_base = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
if not FAKE:
    head = sh(["git", "-C", WT, "rev-parse", "HEAD"]).stdout.strip()
    if not head.startswith("0ee1d95d"):
        stop(f"the worktree is at {head[:8]}, not 0ee1d95d")
    for p, b, filt in PINS:
        g = sh(["git", "hash-object"] + ([] if filt else ["--no-filters"]) + [p]).stdout.strip()
        if not g.startswith(b):
            stop(f"{p} is blob {g[:8]}, not {b[:8]}")
    say(f"pins ok: worktree 0ee1d95d, i1101_weakdir.py 472e820d, d18_secant.py 9706e506, ell_b12rs.py a1fff74f, ell_fastm.py 3431e32e, ell_ddm.py 64c4337f, the other solver files, my ellrs build, "
        f"R2 state 25ba3a91, R2 record 9111bfca, chord035 state 205b6a90, its map.json 3bed6d4d")
    rec = json.loads(open(REC).read())
    cm = json.load(open(CMAP))
    if cm["steps"] != rec["steps"] or sum(cm["steps_map"].values()) != rec["steps"] or cm["kc"] != rec["kc"] or float(cm["D"]) != float(D):
        stop(f"the chord state's map is not R2's: map steps {cm['steps']} (sum {sum(cm['steps_map'].values())}), record steps {rec['steps']}, kc {cm['kc']} against {rec['kc']}")
    say(f"the chord035 map has R2's step count: {cm['steps']} steps (record {rec['steps']}), k_c {cm['kc']}, D {cm['D']}; its |F| {cm['F']:.4e} (R2's record {rec['F']:.4e})")
    senv = dict(env_base, PYTHONPATH=SITE, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1")
    ex, ex2 = [], []
    for mut in ("", "--mutate=half", "--mutate=norobust", "--mutate=nosigncheck"):
        r = sh([PY, "-u", WTM + "/d18_secant.py", "selftest"] + ([mut] if mut else []), cwd=WTM, env=senv)
        ex.append(r.returncode)
        open(OUT + "/selftest_d18_secant.txt" + SFX, "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC d18_secant.py selftest {mut}\n" + r.stdout + r.stderr + f"exit {r.returncode} ({0 if not mut else 1} wanted)\n")
    for mut in ("", "--mutate=nolam", "--mutate=harm"):
        r = sh([PY, "-u", WTM + "/ell_b12rs.py", "selftest"] + ([mut] if mut else []), cwd=WTM, env=senv)
        ex2.append(r.returncode)
        open(OUT + "/selftest_ell_b12rs.txt" + SFX, "a").write(f"== {now():%Y-%m-%d %H:%M:%S} UTC ell_b12rs.py selftest {mut}\n" + r.stdout + r.stderr + f"exit {r.returncode} ({0 if not mut else 1} wanted)\n")
    if ex != [0, 1, 1, 1] or ex2 != [0, 1, 1]:
        stop(f"selftests: d18_secant.py (and half, norobust, nosigncheck) exits {ex}, wanted [0, 1, 1, 1]; ell_b12rs.py (and nolam, harm) exits {ex2}, wanted [0, 1, 1]")
    say(f"d18_secant.py selftest exit 0 and its controls half, norobust, nosigncheck exit 1, 1, 1; ell_b12rs.py selftest exit 0 and its controls nolam, harm exit 1, 1, as wanted (ellrs from {SITE})")

jenv = dict(env_base, OPENBLAS_NUM_THREADS="4", OMP_NUM_THREADS="4", MKL_NUM_THREADS="4", VECLIB_MAXIMUM_THREADS="4")
denv = dict(env_base, OPENBLAS_NUM_THREADS="1", OMP_NUM_THREADS="1", MKL_NUM_THREADS="1", VECLIB_MAXIMUM_THREADS="1", RAYON_NUM_THREADS="4", D18_DIR=WTM, PYTHONPATH=SITE)
W = WTM + "/i1101_weakdir.py"
CMDS = {"jac": [PY, "-u", W, "jac", REC, STATE, D, JAC, "--pin=25ba3a91,9111bfca"],
        "svd": [PY, "-u", W, "svd", JAC, SVD],
        "detparts": [PY, "-u", W, "detparts", SVD, REC, STATE, CHORD, D, LAM, "--b12=rust", "--b12_threads=4"]}
XCMDS = {"planted": [PY, "-u", W, "planted", SVD], "planted_basis": [PY, "-u", W, "planted", SVD, "--mutate=basis"], "coords": [PY, "-u", W, "coords", SVD, STATE, "chord035=" + CHORD]}


def fake(step):
    """stand-ins for the tests: print what the tool prints (or fails), write the files the next step needs"""
    dz = float(np.linalg.norm(np.load(CHORD) - np.load(STATE)))
    if step == "jac":
        if FAKE == "jacfail":
            return "print('pin differs: state 00000000'); import sys; sys.exit(3)"
        return ("import json; print('D 23.0 k_c 127: |F| 3.1242e-10 (record 3.1242e-10), steps 8351 (record 8351): the record system'); open(r'%s','wb').write(b'x'); "
                "print(json.dumps(dict(out='jac_r2.npz', F=3.1e-10, J_shape=[8300, 8300], seconds=12.5, steps=8351)))" % JAC)
    if step == "svd":
        return ("import numpy as np; s = np.concatenate([np.logspace(0, -4, 8000), np.logspace(-6, -9, 200), np.logspace(-12, -14, 100)]); "
                "np.savez(r'%s', s=s, U=np.zeros(1), Vt=np.zeros(1)); print('svd (8300, 8300): 1.0 s, s_max 1.000000e+00, s_min 1.000e-14')" % SVD)
    if step == "planted":
        return "print('planted PASS'); import sys; sys.exit(0)"
    if step == "planted_basis":
        return "print('planted FAIL (mutate=basis)'); import sys; sys.exit(1)"
    if step == "coords":
        return "print('fractions null 0.231 weak 0.97 strong 6e-5')"
    f = [0.231, 0.97286, 0.0]
    f[2] = float(np.sqrt(1 - f[0] ** 2 - f[1] ** 2))
    if FAKE == "badparts":
        f[1] = 0.5
    p = [x * dz for x in f]
    ln = [-1590.0, -1590.5, -1593.2, -1590.0, -1593.1]
    sg = [1, 1, -1, 1, -1]
    nm = ["A", "A + P_null", "A + P_weak", "A + P_strong", "B"]
    code = "print('record system fake'); "
    for n, v in zip(("null", "weak", "strong"), p):
        code += "print('  part %s: |P dz| %.3e'); " % (n, v)
    for i in range(5):
        code += "print('  %s: hybrid sign %+d ln|det| %.10f dln 1.00e-05 robust True; |F| 3.1e-10 (1.0 s)'); " % (nm[i], sg[i], ln[i])
    return code


def cap_for(step, cap):
    try:
        for ln in open(OUT + "/cap_seconds.txt"):
            m = re.match(r"\s*(\w+)\s*=\s*(\d+)", ln)
            if m and m.group(1) == step:
                return int(m.group(2))
    except OSError:
        pass
    return cap


def run_capped(step, cmd, logf, cap, env, notify_at=None):
    """start BelowNormal without a window, poll every 15 s, kill by the exact pid at the cap; returns (exit code or 'killed at the cap', seconds)"""
    if FAKE:
        cmd = [PY, "-c", fake(step)]
    p = subprocess.Popen(cmd, cwd=WTM if not FAKE else OUT, env=env, stdout=open(logf, "w"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    say(f"{step}: started pid {p.pid}: {' '.join(cmd)[:420]} > {logf}")
    t0, notified = time.time(), False
    while True:
        rc = p.poll()
        if rc is not None:
            say(f"{step}: pid {p.pid} ended with exit {rc} after {time.time() - t0:.0f} s")
            return rc, time.time() - t0
        if notify_at and not notified and time.time() - t0 > notify_at:
            notified = True
            say(f"{step}: still running at {notify_at} s (pid {p.pid}); cap {cap} s; hc to t5")
            hc(f"the {step} (pid {p.pid}) is still running after {notify_at} s; its cap is {cap} s (cap_seconds.txt overrides it).")
        c2 = cap_for(step, cap)
        if c2 != cap:
            say(f"{step}: cap changed from {cap} s to {c2} s (cap_seconds.txt)")
            cap = c2
        if time.time() - t0 > cap:
            r = sh(["taskkill", "/PID", str(p.pid), "/T", "/F"])
            say(f"{step}: CAP {cap} s: killed pid {p.pid} (and its children) by exact pid: {r.stdout.strip()} {r.stderr.strip()}")
            p.wait()
            return "killed at the cap", time.time() - t0
        time.sleep(15 if not FAKE else 0.2)


def tail(f, n=3):
    try:
        return " | ".join(l.strip() for l in open(f, errors="replace").read().strip().splitlines()[-n:])[:900]
    except OSError:
        return "(no log)"


if DRY:
    for k, c in list(CMDS.items()) + list(XCMDS.items()):
        say(f"DRY: would run {k}: " + " ".join(c) + f" (cwd {WTM}; caps {CAPS})")
    say("DRY: nothing started")
    sys.exit(0)
if not FAKE and (os.path.exists(JAC) or os.path.exists(SVD)):
    stop(f"{JAC} or {SVD} exists already")

if not FAKE:
    samp = subprocess.Popen(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", S + "/sample_driver_1111.ps1", "-Drv", str(os.getpid()), "-Out", OUT + "/rows/driver_samples.csv", "-Interval", "60"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, creationflags=0x00004000 | 0x08000000)
    wat = subprocess.Popen([PY, "-u", S + "/k127_watch_alert_1111.py", str(os.getpid()), "driver"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                           creationflags=0x00004000 | 0x08000000)
    kaw = subprocess.Popen([PY, "-u", S + "/keepawake_1111.py", str(os.getpid()), "driver", str(sum(CAPS.values()) + 3600)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL,
                           creationflags=0x00004000 | 0x08000000)
    say(f"alert-only memory watcher pid {wat.pid} (kills nothing), sampler pid {samp.pid}, keep-awake helper pid {kaw.pid} (SetThreadExecutionState until this driver, pid {os.getpid()}, ends; power plan untouched)")
t00 = time.time()
res = {}

# ---- step 1: jac
rc, sec = run_capped("jac", CMDS["jac"], OUT + "/jac_r2.log", CAPS["jac"], jenv, NOTIFY["jac"])
txt = open(OUT + "/jac_r2.log", errors="replace").read()
if rc != 0:
    stop(f"jac ended with exit {rc} after {sec:.0f} s (the tool exits 3 if the system is not the record system or a pin differs): {tail(OUT + '/jac_r2.log')}")
last = [l for l in txt.splitlines() if l.startswith("{")]
js = json.loads(last[-1]) if last else {}
if ": the record system" not in txt or js.get("steps") != 8351 or len(js.get("J_shape", [])) != 2 or js["J_shape"][0] != js["J_shape"][1]:
    stop(f"jac exit 0 but its log is not the record system with 8351 steps and a square J: {tail(OUT + '/jac_r2.log')}")
res["jac"] = (sec, js)
say(f"jac accepted: exit 0, {sec:.0f} s, J {js['J_shape']}, |F| {js['F']:.4e}, steps {js['steps']}; the tool's own line (seconds {js['seconds']}); the record system")
hc(f"jac done (exit 0, {sec:.0f} s, J {js['J_shape'][0]} x {js['J_shape'][1]}, |F| {js['F']:.4e}, steps {js['steps']}, the record system); svd starts now.")

# ---- step 2: svd, planted, coords
rc, sec = run_capped("svd", CMDS["svd"], OUT + "/svd_r2.log", CAPS["svd"], jenv, NOTIFY["svd"])
txt = open(OUT + "/svd_r2.log", errors="replace").read()
m = re.search(r"svd \((\d+), (\d+)\): ([\d.]+) s, s_max ([\d.e+-]+), s_min ([\d.e+-]+)", txt)
if rc != 0 or not m:
    stop(f"svd ended with exit {rc} after {sec:.0f} s: {tail(OUT + '/svd_r2.log')}")
xr = {}
for k in ("planted", "planted_basis", "coords"):
    cmd = XCMDS[k]
    if FAKE:
        cmd = [PY, "-c", fake(k)]
    r = sh(cmd, cwd=WTM if not FAKE else OUT, env=jenv)
    open(OUT + f"/{k}_r2.log", "w").write(r.stdout + r.stderr + f"exit {r.returncode}\n")
    xr[k] = r.returncode
    say(f"{k}: exit {r.returncode}")
if xr["planted"] != 0 or xr["planted_basis"] != 1 or xr["coords"] != 0:
    stop(f"the svd checks: planted exit {xr['planted']} (0 wanted), planted --mutate=basis exit {xr['planted_basis']} (1 wanted), coords exit {xr['coords']} (0 wanted)")
s = np.load(SVD)["s"]
r_ = s / s[0]
nn, nw, ns = int((r_ < 1e-11).sum()), int(((r_ >= 1e-11) & (r_ < 1e-5)).sum()), int((r_ >= 1e-5).sum())
res["svd"] = (sec, (nn, nw, ns))
bands = f"null {nn}, weak {nw}, strong {ns} of {len(s)} (s/s_max cuts 1e-11 and 1e-5; weakest non-null {r_[r_ >= 1e-11][-1]:.3e})"
say(f"svd accepted: exit 0, {sec:.0f} s, s_max {m.group(4)}, s_min {m.group(5)}; planted exit 0 and its --mutate=basis control exit 1; bands {bands}")
hc(f"svd done (exit 0, {sec:.0f} s; {bands}; the tool's planted check passes and its --mutate=basis control fails as wanted); detparts starts now.")

# ---- step 3: detparts
rc, sec = run_capped("detparts", CMDS["detparts"], OUT + "/detparts_r2.log", CAPS["detparts"], denv, NOTIFY["detparts"])
txt = open(OUT + "/detparts_r2.log", errors="replace").read()
parts = {n: float(v) for n, v in re.findall(r"^\s*part (null|weak|strong): \|P dz\| ([\d.e+-]+)", txt, re.M)}
cases = {}
for mm in re.finditer(r"^\s*(A|A \+ P_null|A \+ P_weak|A \+ P_strong|B): hybrid sign ([+-]\d) ln\|det\| ([\w.+-]+) dln ([\w.+-]+) robust (True|False); \|F\| ([\w.+-]+) \(([\d.]+) s\)", txt, re.M):
    cases[mm.group(1)] = dict(sign=int(mm.group(2)), ln=float(mm.group(3)), dln=float(mm.group(4)), robust=mm.group(5) == "True", F=float(mm.group(6)), sec=float(mm.group(7)))
if rc != 0 or len(parts) != 3 or len(cases) != 5:
    stop(f"detparts ended with exit {rc} after {sec:.0f} s with {len(parts)} part lines and {len(cases)} case lines (3 and 5 wanted): {tail(OUT + '/detparts_r2.log')}")
dzv = np.load(CHORD) - np.load(STATE)
dz = float(np.linalg.norm(dzv))
sd = np.load(SVD)
Vt = sd["Vt"]
if Vt.ndim == 2 and Vt.shape[0] == Vt.shape[1] == len(dzv):          # my own band norms from the stored SVD, to 1e-12, against the tool's three-digit prints
    c = Vt @ dzv
    r_ = sd["s"] / sd["s"][0]
    mine = {"null": float(np.linalg.norm(c[r_ < 1e-11])), "weak": float(np.linalg.norm(c[(r_ >= 1e-11) & (r_ < 1e-5)])), "strong": float(np.linalg.norm(c[r_ >= 1e-5]))}
    relsum = abs(np.sqrt(sum(v * v for v in mine.values())) - dz) / dz
    bad = [k for k in parts if abs(parts[k] - mine[k]) > 6e-3 * max(mine[k], 1e-300)]
    if relsum > 1e-9 or bad:
        stop(f"the band norms: mine {mine}, the tool's {parts}; sqrt(sum of squares) against |dz| {dz:.6e}: relative {relsum:.2e}; differing parts {bad}")
    say(f"band norms checked against my own V^T (dz): null {mine['null']:.6e}, weak {mine['weak']:.6e}, strong {mine['strong']:.6e}; sqrt(sum of squares) = |dz| {dz:.6e} to {relsum:.1e}; the tool's three-digit prints agree to 6e-3")
else:
    rel = abs(np.sqrt(sum(v * v for v in parts.values())) - dz) / dz
    if rel > 2e-3:
        stop(f"the three parts' norms do not add up to |z_B - z_A| {dz:.6e}: sqrt(sum of squares) {np.sqrt(sum(v * v for v in parts.values())):.6e}, relative {rel:.2e}")
A, B = cases["A"], cases["B"]
rows = []
carriers = []
for nm in ("A", "A + P_null", "A + P_weak", "A + P_strong", "B"):
    c = cases[nm]
    d = c["ln"] - A["ln"]
    rows.append(f"{nm:14s} sign {c['sign']:+d}  ln|det| {c['ln']:.10f}  dln {c['dln']:.2e}  robust {c['robust']}  |F| {c['F']:.4e}  {c['sec']:.0f} s  ln - ln(A) {d:+.6f}")
    if nm.startswith("A + P") and c["sign"] == B["sign"] and abs(c["ln"] - B["ln"]) <= 0.1:
        carriers.append(nm)
rd = {k: v / dz for k, v in parts.items()}
tab = "\n".join(rows)
verdict = ("carried by " + " and ".join(carriers)) if carriers else "no single part reproduces B (sign and ln|det| within 0.1)"
open(OUT + "/detparts_table.txt", "w").write(tab + f"\n|z_B - z_A| {dz:.6e}; parts |P dz|: null {parts['null']:.4e} ({rd['null']:.4f}), weak {parts['weak']:.4e} ({rd['weak']:.6f}), strong {parts['strong']:.4e} ({rd['strong']:.3e}); "
                                              f"B - A in ln|det| {B['ln'] - A['ln']:+.6f}; reading rule (mine, t5 rules): {verdict}\n")
res["detparts"] = sec
say(f"detparts accepted: exit 0, {sec:.0f} s; |dz| {dz:.4e}, parts null {rd['null']:.4f}, weak {rd['weak']:.6f}, strong {rd['strong']:.3e} of it")
for ln in rows:
    say(ln)
say("reading rule: " + verdict)
total = time.time() - t00
summ = f"jac {res['jac'][0]:.0f} s, svd {res['svd'][0]:.0f} s, detparts {sec:.0f} s, total {total:.0f} s"
open(OUT + "/summary_1111.txt", "w").write(summ + "\n" + tab + "\n")
hc(f"detparts done (exit 0, {sec:.0f} s; {summ}). |z_B - z_A| {dz:.4e}: null {rd['null']:.3f}, weak {rd['weak']:.5f}, strong {rd['strong']:.1e} of it. Table: " + " | ".join(rows) + f". Reading rule (mine; you rule): {verdict}. Raw I1111-win after my next push.")
time.sleep(70 if not FAKE else 0)          # the sampler's last line
say("w127_1111_driver.py done")
sys.exit(0)

#!/usr/bin/env python3
"""#1025 (win) preparation job: a NEW venv (Python 3.14), the repo's requirements.txt, then multidouble 5.1.0 (8c4360ac) built with MSVC's link.exe first on PATH.
Timestamps in UTC to the log. Existing venvs are not touched. Run from an environment where vcvars64.bat has been called (build_md510_1025.cmd)."""
import datetime, json, os, shutil, subprocess, sys, time, glob
HERE = os.path.dirname(os.path.abspath(__file__))
VENV = r"C:\Users\nathan\Source\venv-md510"
BASE = r"C:\Users\nathan\AppData\Local\Programs\Python\Python314\python.exe"
REQ = r"C:\Users\nathan\Source\choptuik-large-d\requirements.txt"
SPEC = "multidouble @ git+https://github.com/nmoinvaz/multidouble@8c4360ac0be804d081faeea524e5c1c6e2fffaaa#subdirectory=python"
LOG = os.path.join(HERE, "build_md510_1025.log")

def say(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC  {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def run(cmd, **kw):
    say("$ " + " ".join(cmd))
    t = time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, **kw)
    with open(LOG, "a") as f:
        f.write(p.stdout)
    say(f"exit {p.returncode} after {time.time() - t:.1f} s")
    return p, time.time() - t

say("start; base " + BASE)
if os.path.exists(VENV):
    say(f"{VENV} exists, stopping (a NEW venv is required)"); sys.exit(3)
lk = shutil.which("link")
say(f"first link on PATH: {lk}")
if not lk or "MSVC" not in lk.upper():
    say("the first link.exe on PATH is not MSVC's, stopping"); sys.exit(4)
for t in ("rustc", "cargo", "git"):
    say(f"{t}: {shutil.which(t)}")
p, _ = run(["rustc", "--version"]); p, _ = run(["cargo", "--version"])
t0 = time.time()
p, _ = run([BASE, "-m", "venv", VENV])
if p.returncode:
    sys.exit(5)
py = os.path.join(VENV, "Scripts", "python.exe")
p, _ = run([py, "--version"])
p, t_req = run([py, "-m", "pip", "install", "--no-cache-dir", "-r", REQ])
if p.returncode:
    sys.exit(6)
say(f"requirements installed in {t_req:.0f} s")
p, t_md = run([py, "-m", "pip", "install", "--no-cache-dir", "-v", SPEC])
say(f"multidouble pip install exit {p.returncode}, build time {t_md:.0f} s ({t_md / 60:.1f} min)")
if p.returncode:
    sys.exit(7)
for d in glob.glob(os.path.join(VENV, "Lib", "site-packages", "multidouble-*.dist-info")):
    du = os.path.join(d, "direct_url.json")
    say(f"{os.path.basename(d)} direct_url.json: {open(du).read().strip() if os.path.exists(du) else 'missing'}")
p, _ = run([py, "-I", "-c", "import multidouble; print(multidouble.__file__, hasattr(multidouble, 'dd_logdet'), hasattr(multidouble, 'qd_logdet'))"], cwd=os.environ.get("USERPROFILE", HERE))
say(f"total {time.time() - t0:.0f} s")

#!/usr/bin/env python3
"""#1058 winb, second start: hp build at main 8179068d in the NEW venv-i1058, then the four stored-reference checks.
The first start (driver_hp_1058.py, log hp1058_build.log) made the venv, installed requirements.txt and ran pip uninstall -y multidouble, then hp/build.sh failed after 0.4 s
before compiling anything: the driver's `bash build.sh` found WSL's C:\\Windows\\System32\\bash.exe (no distribution installed) ahead of Git's bash. This start reuses that
venv (it holds only the requirements, no multidouble, no hpkernel; checked below), repeats the uninstall, and runs `/usr/bin/bash build.sh`. Timestamps in UTC to hp1058b_build.log."""
import datetime, glob, json, os, shutil, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
WT = r"C:\Users\nathan\Source\choptuik-i1058-hp"
WANT = "8179068da460fe6be81312602e4c9987d17d73a3"
VENV = r"C:\Users\nathan\Source\venv-i1058"
BASH = r"C:\Program Files\Git\usr\bin\bash.exe"
RAW = "C:/Users/nathan/Source/hp1058_winb/raw"
LOG = os.path.join(HERE, "hp1058b_build.log")
CHK = os.path.join(HERE, "checks")

def say(msg):
    line = f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC  {msg}"
    print(line, flush=True)
    with open(LOG, "a") as f:
        f.write(line + "\n")

def run(cmd, logfile=None, **kw):
    say("$ " + " ".join(cmd))
    t = time.time()
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, errors="replace", **kw)
    with open(logfile or LOG, "a", encoding="utf-8") as f:
        f.write(p.stdout)
    say(f"exit {p.returncode} after {time.time() - t:.1f} s" + (f" (output in {os.path.basename(logfile)})" if logfile else ""))
    return p, time.time() - t

def stop(code, why):
    say(f"STOP: {why}")
    say("hp1058b driver done")
    sys.exit(code)

say(f"start (second); worktree {WT}, venv {VENV}")
head = subprocess.run(["git", "-C", WT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
say(f"worktree HEAD {head}")
if head != WANT:
    stop(2, "worktree is not at 8179068d")
py = os.path.join(VENV, "Scripts", "python.exe")
sp = os.path.join(VENV, "Lib", "site-packages")
if not os.path.exists(py):
    stop(3, f"{VENV} is missing")
bad = glob.glob(os.path.join(sp, "multidouble*")) + glob.glob(os.path.join(sp, "hpkernel*"))
say(f"venv reused; multidouble/hpkernel entries in site-packages: {bad}")
if bad:
    stop(3, "the venv already holds multidouble or hpkernel")
lk = shutil.which("link")
say(f"first link on PATH (windows): {lk}")
if not lk or "MSVC" not in lk.upper():
    stop(4, "the first link.exe on PATH is not MSVC's")
p, _ = run([BASH, "-c", "type -a link | head -3; type -a bash | head -3; command -v rustc cargo git nice; rustc --version; cargo --version"])
first = [l for l in p.stdout.splitlines() if l.strip()][0] if p.stdout.strip() else ""
if "MSVC" not in first.upper():
    stop(5, f"in bash the first link is not MSVC's: {first}")
for k in ("CARGO_PROFILE_RELEASE_LTO", "CARGO_PROFILE_RELEASE_CODEGEN_UNITS", "PIP_NO_CACHE_DIR", "CARGO_BUILD_JOBS"):
    say(f"env {k}={os.environ.get(k)}")

t0 = time.time()
env = dict(os.environ, PIP_NO_CACHE_DIR="1")
p, _ = run([py, "-m", "pip", "uninstall", "-y", "multidouble"], env=env)
say("multidouble uninstall exit " + str(p.returncode) + " (a warning that it is not installed is fine)")
p, _ = run([py, "-m", "pip", "list", "--format=freeze"])

benv = dict(os.environ, PIP_NO_CACHE_DIR="1", VIRTUAL_ENV=VENV.replace("\\", "/"), PYTHONDONTWRITEBYTECODE="1")
benv["PATH"] = os.path.join(VENV, "Scripts") + os.pathsep + benv["PATH"]
say("build start (hp/build.sh): " + " ".join(f"{k}={benv.get(k)}" for k in ("CARGO_PROFILE_RELEASE_LTO", "CARGO_PROFILE_RELEASE_CODEGEN_UNITS")))
blog = os.path.join(HERE, "hp1058b_build_output.log")
p, t_build = run([BASH, "-c", "cd /c/Users/nathan/Source/choptuik-i1058-hp/hp && /usr/bin/bash build.sh"], logfile=blog, env=benv)
say(f"hp/build.sh exit {p.returncode}, build time {t_build:.0f} s ({t_build / 60:.1f} min)")
if p.returncode:
    stop(8, "hp/build.sh failed")
for d in glob.glob(os.path.join(sp, "multidouble-*.dist-info")):
    du = os.path.join(d, "direct_url.json")
    say(f"{os.path.basename(d)} direct_url.json: {open(du).read().strip() if os.path.exists(du) else 'missing'}")
p, _ = run([py, "-I", "-c", "import hpkernel, multidouble; print('hpkernel', hpkernel.isa(), 'multidouble', multidouble.isa(), multidouble.__file__)"], cwd=os.environ.get("USERPROFILE", HERE))
p, _ = run([py, "-m", "pip", "list", "--format=freeze"])

os.makedirs(CHK, exist_ok=True)
checks = [
    ("ref", ["highm_check.py", "ref", f"--compare={RAW}/T81/ref_main.json", "--Ms=48,64,80"], 0),
    ("scaled", ["highm_check.py", "scaled", f"--compare={RAW}/T81/scaled_main.json"], 0),
    ("jets", ["highm_check.py", "jets", f"--compare={RAW}/anm-mac/jets_inputs/jets_inputs.json"], 0),
    ("jets_mutate_kappa", ["highm_check.py", "jets", f"--compare={RAW}/anm-mac/jets_inputs/jets_inputs.json", "--mutate=kappa"], 1),
]
cenv = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
results = {}
for name, args, want in checks:
    cl = os.path.join(CHK, f"check_{name}.log")
    say(f"check {name}: python {' '.join(args)}")
    p, t = run([py, "-u"] + args, logfile=cl, cwd=os.path.join(WT, "hp"), env=cenv)
    ok = (p.returncode == 0) if want == 0 else (p.returncode != 0)
    results[name] = {"exit": p.returncode, "expected": "0" if want == 0 else "nonzero", "ok": ok, "sec": round(t, 1)}
    say(f"check {name}: exit {p.returncode} ({'as expected' if ok else 'NOT as expected'}), {t:.0f} s")
with open(os.path.join(HERE, "checks_1058.json"), "w") as f:
    json.dump({"build_s": round(t_build, 1), "checks": results}, f, indent=1)
allok = all(r["ok"] for r in results.values())
say("checks: " + ("all four as expected" if allok else "NOT all as expected") + " " + json.dumps(results))
say("hp1058b driver done")
sys.exit(0 if allok else 9)

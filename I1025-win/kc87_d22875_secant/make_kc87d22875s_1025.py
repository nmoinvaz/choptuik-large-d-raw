#!/usr/bin/env python3
"""make_kc87d22875s_1025.py: writes the k_c 87 D 22.875 secant lane's scripts from the k_c 95 D 22.875 secant ones (staging kc95d22875s_1025, raw I1025-win/kc95_d22875_secant at 75a10de70) by asserted
text replacements: kc87d22875s_secant_driver_1025.py (the state, record, bracket and acceptance check changed: the state is macm3's k_c 87 leg state at D 22.875, accepted by kc87_syscheck_1025.py with its
--mutate=F and --mutate=steps exit 1, and refused by the k_c 95 and k_c 103 checks), kc87d22875s_watch_alert_1025.py, keepawake_1025.py, session_check_1025.ps1, sample_driver_secant_1025.ps1,
go_kc87d22875s_1025.cmd, publish_kc87d22875s_1025.sh. The diff of the driver against the k_c 95 one is written to diff_secant_driver_vs_kc95.txt."""
import difflib, os, shutil

S = "C:/Users/nathan/Source/kc87d22875s_1025"
OLD = "C:/Users/nathan/Source/kc95d22875s_1025"


def rd(p):
    return open(p, "rb").read().decode("utf-8")


def wr(p, t):
    open(p, "wb").write(t.encode("utf-8"))


def rep(t, pairs):
    for a, b in pairs:
        assert t.count(a) == 1, a[:140]
        t = t.replace(a, b)
    return t


os.makedirs(S + "/inputs", exist_ok=True)
os.makedirs(S + "/I1025-win/kc87_d22875_secant/rows", exist_ok=True)
for f in ("kc87_syscheck_1025.py", "kc95_syscheck_1025.py", "kc103_syscheck_1025.py"):
    assert os.path.exists(S + "/inputs/" + f), f
for f in ("sol_l1kc87Lmacm3c_D22.875000.npy", "l1kc87Lmacm3c.jsonl"):
    assert os.path.exists(S + "/I1025-win/kc87_d22875_secant/in/" + f), f

# 1. the driver
t = rd(OLD + "/kc95d22875s_secant_driver_1025.py")
i = t.index('"""')
j = t.index('"""', i + 3) + 3
doc = '''"""#1025 winb, the secant refinement of the k_c 87 root at D 22.875 (t5's order, hc of 2026-11-26 ~08:59 UTC, after the k_c 95 D 22.875 ruling): xfkappa's d18_secant.py (branch wip/ell1-speed at 6010e37b,
committed blob a3d90cd5, my copy of the k_c 103 and k_c 95 lanes; the branch tip 92b9bf53 has another d18_secant.py blob, eb1396ad, that adds a scan command) on macm3's k_c 87 leg state
sol_l1kc87Lmacm3c_D22.875000.npy (raw I1025-macm3/kc87_leg_lambda/22.875/in, blob b1e4f8ca) and its record l1kc87Lmacm3c.jsonl (blob 338bd7f1, six rows, the D 22.875 row last; copies in in/),
between LO HI (arguments: the scan's bracket (0.12, 0.13)):
  RAYON_NUM_THREADS=1 d18_secant.py run STUB STATE 22.875 LO HI secant.jsonl --tol=1e-5 --maxev=10 --pin=STATEBLOB,STUBBLOB     one process, BelowNormal, 1 thread (OMP/OPENBLAS/MKL 1 too)
Order of the driver (any failure stops it with an hc to t5, nothing started, exit 2):
  1. pins: d18_secant.py, ell_fastm.py, ell_ddm.py, dss_ell.py, ell_dd.py, ddnp.py in the worktree choptuik-i1025secant (HEAD 6010e37b); the three checks (kc87 6df5d960, kc95 d487e628, kc103 3ab58d16); the state and the record;
  2. d18_secant.py selftest exit 0 and its three controls --mutate=half, norobust, nosigncheck exit 1 each; the selftests of the three checks exit 0;
  3. the ACCEPTANCE of the state: kc87_syscheck_1025.py accepts the record and state (exit 0), its --mutate=F and --mutate=steps exit 1 each, and the k_c 95 and k_c 103 checks refuse them (exit 1 each);
  4. the run, killed by the exact pid (taskkill /PID /T /F) if it passes 28800 s (8 h; t5: stop and report on any step over 8 h), one hc to t5 at 14400 s if it is still running.
The tool's exits: 0 tol reached, 4 maxev or a non-robust interior point (the bracket is valid), 2 refused (ends not robust or with equal signs: t5's "signs at 0.12 and 0.13 that do not differ"), 3 pin differs or
not the record system. Its own records (one per evaluation, then a root record) are appended to secant.jsonl; the log is secant.log. A sampler (60 s), an alert-only memory watcher and a keep-awake helper run
beside it, as in my other drivers; nothing kills on memory.
usage: kc87d22875s_secant_driver_1025.py LO HI [--dry]     (--dry: pins, selftests, acceptance checks, prints the command, starts nothing)"""'''
t = t[:i] + doc + t[j:]
t = rep(t, [
    ('OUT = S + "/I1025-win/kc95_d22875_secant"', 'OUT = S + "/I1025-win/kc87_d22875_secant"'),
    ('STATE, STUB = OUT + "/in/sol_l1kc95win2d22875_D22.8750.npy", OUT + "/in/l1kc95win2d22875.jsonl"', 'STATE, STUB = OUT + "/in/sol_l1kc87Lmacm3c_D22.875000.npy", OUT + "/in/l1kc87Lmacm3c.jsonl"'),
    ('B_STATE, B_STUB = "a14f0d50edb575e85387851a61cb2324c1983317", "5381f89d5fe4f81a113295cdde8eb6358de937e8"', 'B_STATE, B_STUB = "b1e4f8cad92d4384f3c2e2dffe15cd2b801251dd", "338bd7f1afa55d6afd80f03051402b855e198a3f"'),
    ('#1025 k_c 95 D {D} secant refinement', '#1025 k_c 87 D {D} secant refinement'),
    ('the secant refinement of the k_c 95 root at D {D}, bracket', 'the secant refinement of the k_c 87 root at D {D}, bracket'),
    ('S + "/kc95d22875s_watch_alert_1025.py"', 'S + "/kc87d22875s_watch_alert_1025.py"'),
    ('usage: kc95d22875s_secant_driver_1025.py LO HI [--dry]"', 'usage: kc87d22875s_secant_driver_1025.py LO HI [--dry]"'),
    ('say(f"kc95d22875s_secant_driver_1025.py: ', 'say(f"kc87d22875s_secant_driver_1025.py: '),
    ('say("kc95d22875s_secant_driver_1025.py done")', 'say("kc87d22875s_secant_driver_1025.py done")'),
    ('selftests: kc95_syscheck exit 0, kc87_syscheck exit 0, kc103_syscheck exit 0 (0 wanted each)', 'selftests: kc87_syscheck exit 0, kc95_syscheck exit 0, kc103_syscheck exit 0 (0 wanted each)'),
])
a = t.index("t0 = time.time()\nsrc = {}")
b = t.index('cmd = [PY, "-u", WTM + "/d18_secant.py", "run"')
accept = '''t0 = time.time()
src = {}
for name, cmdl in (("source_kc87_syscheck.txt", [PY, IN + "/kc87_syscheck_1025.py", STUB, STATE, D, WTM]), ("source_kc87_syscheck_mutate_F.txt", [PY, IN + "/kc87_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=F"]),
                   ("source_kc87_syscheck_mutate_steps.txt", [PY, IN + "/kc87_syscheck_1025.py", STUB, STATE, D, WTM, "--mutate=steps"]), ("source_kc95_syscheck.txt", [PY, IN + "/kc95_syscheck_1025.py", STUB, STATE, D, WTM]),
                   ("source_kc103_syscheck.txt", [PY, IN + "/kc103_syscheck_1025.py", STUB, STATE, D, WTM])):
    r = sh(cmdl, env=env)
    open(SEC + "/" + name + (".dry" if DRY else ""), "w").write(r.stdout + r.stderr + f"exit {r.returncode}\\n")
    src[name] = r.returncode
want = {"source_kc87_syscheck.txt": 0, "source_kc87_syscheck_mutate_F.txt": 1, "source_kc87_syscheck_mutate_steps.txt": 1, "source_kc95_syscheck.txt": 1, "source_kc103_syscheck.txt": 1}
say(f"the state: kc87 check exit {src['source_kc87_syscheck.txt']} (0 wanted: it accepts), --mutate=F {src['source_kc87_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc87_syscheck_mutate_steps.txt']} (1 wanted each), "
    f"kc95 check {src['source_kc95_syscheck.txt']} and kc103 check {src['source_kc103_syscheck.txt']} (1 wanted each: they refuse it); {time.time() - t0:.0f} s")
if src != want:
    refuse(f"the state is not accepted as wanted ({src}, wanted {want})")
'''
t = t[:a] + accept + t[b:]
for bad in ("kc95win2", "a14f0d50", "5381f89d", "k_c 95 root", "kc95d22875", "kc95_d22875", "win2's", "0.10 and 0.12", "kc95_syscheck_1025.py accepts", "source_kc95_syscheck_mutate"):
    assert bad not in t, (bad, t[max(0, t.index(bad) - 100):t.index(bad) + 80])
wr(S + "/kc87d22875s_secant_driver_1025.py", t)
d = "".join(difflib.unified_diff(rd(OLD + "/kc95d22875s_secant_driver_1025.py").splitlines(True), t.splitlines(True), "kc95d22875s_secant_driver_1025.py", "kc87d22875s_secant_driver_1025.py"))
wr(S + "/diff_secant_driver_vs_kc95.txt", d)


# 2. watcher, keep-awake, session check, sampler, go cmd, publish script
def conv(txt):
    txt = txt.replace("kc95d22875s", "kc87d22875s").replace("kc95_d22875_secant", "kc87_d22875_secant")
    return txt


for a_, b_ in (("kc95d22875s_watch_alert_1025.py", "kc87d22875s_watch_alert_1025.py"), ("keepawake_1025.py", "keepawake_1025.py"), ("session_check_1025.ps1", "session_check_1025.ps1")):
    x = conv(rd(OLD + "/" + a_)).replace("The k_c 95 D 22.875 {label} stage", "The k_c 87 D 22.875 {label} stage").replace("the k_c 95 D 22.875 secant lane", "the k_c 87 D 22.875 secant lane")
    assert "k_c 95" not in x and "kc95" not in x, (a_, x[x.index("95") - 60:x.index("95") + 40])
    wr(S + "/" + b_, x)
shutil.copyfile(OLD + "/sample_driver_secant_1025.ps1", S + "/sample_driver_secant_1025.ps1")
go = conv(rd(OLD + "/go_kc95d22875s_1025.cmd"))
go = rep(go, [("the k_c 95 D 22.875 secant lane (t5's order of 2026-11-26 ~06:35 UTC): one driver, win2's bracket (0.10, 0.12).", "the k_c 87 D 22.875 secant lane (t5's order of 2026-11-26 ~08:59 UTC): one driver, the scan's bracket (0.12, 0.13)."),
              ("kc87d22875s_secant_driver_1025.py 0.10 0.12 >", "kc87d22875s_secant_driver_1025.py 0.12 0.13 >")])
wr(S + "/go_kc87d22875s_1025.cmd", go)
pub = conv(rd(OLD + "/publish_kc95d22875s_1025.sh"))
pub = pub.replace("k_c 95 D 22.875 secant", "k_c 87 D 22.875 secant").replace("diff_secant_driver_vs_kc103.txt", "diff_secant_driver_vs_kc95.txt")
assert "kc95" not in pub.replace("diff_secant_driver_vs_kc95.txt", "") and "k_c 95" not in pub, pub
wr(S + "/publish_kc87d22875s_1025.sh", pub)
os.chmod(S + "/publish_kc87d22875s_1025.sh", 0o755)
print("written")

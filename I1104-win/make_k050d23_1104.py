#!/usr/bin/env python3
"""#1104 winb, the kappa 0.5 re-solve of my k_c 143 D 23.0 state (t5's order, #1104 comment 7225436553 of 2026-11-27 18:23 UTC; cap 64800 s by t5's hc of 18:27 UTC): derives this stage's regrid driver, helpers, go cmd and publish
script from the k_c 143 stage (kc143d23_1025, the lane that made the source state) by asserted text replacements. Part 1 (this file): everything the re-solve needs. The scan and secant drivers are made later (part 2),
while the re-solve runs. Refuses (assert) if a replacement does not find its text exactly the stated number of times. Output: in this folder."""
import os, re, subprocess

SRC = "C:/Users/nathan/Source/kc143d23_1025/"
DST = "C:/Users/nathan/Source/k050d23_1104/"
B_STATE, B_REC = "866c434bc1ae8854e12de9024b0ff859a7764800", "88f0be8bd3a329cadd3a4209614f1295bed61c6e"      # my k_c 143 D 23.0 kappa 0.7 state and record (local files)
B_GATE = "d145145e22bf511011ca9ee2ecd8a14e2ce124e4"


def rd(n):
    return open(SRC + n, encoding="utf-8").read()


def wr(n, t, crlf=False):
    open(DST + n, "w", encoding="utf-8", newline="\r\n" if crlf else "\n").write(t)


class Doc:
    def __init__(self, t, name):
        self.t, self.name = t, name

    def rep(self, a, b, n=1):
        assert self.t.count(a) == n, (self.name, self.t.count(a), a[:100])
        self.t = self.t.replace(a, b)

    def rx(self, pat, b, n=1, flags=re.S):
        m = re.findall(pat, self.t, flags)
        assert len(m) == n, (self.name, len(m), pat)
        self.t = re.sub(pat, lambda _m: b, self.t, flags=flags)

    def doc(self, new):
        i = self.t.index('"""')
        j = self.t.index('"""', i + 3)
        self.t = self.t[:i] + '"""' + new + '"""' + self.t[j + 3:]


# ---------------------------------------------------------------------------------------------- regrid driver
d = Doc(rd("kc143d23_regrid_driver_1025.py"), "regrid")
d.doc("""#1104 winb, the kappa 0.5 re-solve of my k_c 143 D 23.0 state (t5's order, #1104 comment 7225436553 of 2026-11-27 18:23 UTC): my accepted k_c 143 kappa 0.7 state at D 23.0 (raw I1025-win/kc143_d23:
sol_l1kc143winbd23_D23.0000.npy blob 866c434b, l1kc143winbd23.jsonl blob 88f0be8b) is re-solved on this Windows machine at kappa 0.5 with
  ell_refine.py l1kc143winbd23 143 l1kc143winbk050d23 143 1 23.0 2.0992182200 --kappa 0.5 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (2.0992182200 is lambda_0(23.0), unused with --no-gamma; checked below)
with the worktree, settings and threads of my k_c 143 regrid (worktree choptuik-i1025k79 at 48c36355, ell_refine.py 631e5801, venv, 4 threads, BelowNormal), only --kappa 0.5, the source (my k_c 143 record and state) and the
new tag (k050) changed. The cap is 64800 s (t5's hc of 2026-11-27 18:27 UTC; the order said the same cap as my regrid, 43200 s, and t5 raised it after my estimate of about 44000 s) by the exact pid, with one hc to t5 at
21600 s (6 h) if it is still running; nothing is stopped at 6 h. If a file cap_seconds.txt (one integer) exists in the output folder, the cap is read from it at every poll (only on t5's word; each change is logged).
Order of the driver (any failure stops it with an hc to t5, no re-solve, exit 2 or 1):
  1. pins: kc127_syscheck_1025.py (898ebefa), kc135_syscheck_1025.py (b353d466), kc143_syscheck_1025.py (e15b0ee2), gate_k050_1104.py (d145145e), d18_hybsign.py, d185_scan_read.py, read_lower.py, my k_c 143 kappa 0.7
     state and record (inputs/ and the worktree's copies in solver/matter/data/), the worktree (choptuik-i1025k79 at 48c36355, solver code 505d8399, ell_refine.py 631e5801);
  2. the selftest of the three checks (exit 0 each) and ell_delta.lam0_at(23.0) = 2.0992182200;
  3. the SOURCE: the k_c 143 check accepts it (exit 0), its --mutate=F and --mutate=steps exit 1; the k_c 135 and k_c 127 checks refuse it (exit 1 each); the kappa 0.5 gate refuses it (exit 1: kappa 0.7, 4705 steps);
  4. the re-solve;
  5. ACCEPTED only if (t5's bars) gate_k050_1104.py exits 0 on the result (D 23.0, k_c 143, kappa 0.5, |F| <= 5e-10, steps 6455 to 6719 = 6587 +- 132), its selftest exits 0 and its --mutate=f and --mutate=steps exit 1; and
     (my addition, the state against its record) kc143_syscheck_1025.py exits 0 on the result (it takes kappa from the record: the state's |F| within 1% of the record's and freeze_from gives the record's step count), its
     selftest exits 0, --mutate=F and --mutate=steps exit 1, and kc135_syscheck_1025.py refuses the result (exit 1).
The ACCEPTED marker regrid_accepted.txt (with the state and record blobs) is written from this python process; the scan driver starts only after it (go_k050d23_1104.cmd). Memory: no guard, the alert-only
watcher is a separate process. A keep-awake helper (SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED), power plan untouched) holds for this driver's duration.
usage: k050d23_regrid_driver_1104.py [--dry]     (--dry: pins, the three selftests and lambda_0 only, nothing written outside rows/*.dry and the .dry logs, nothing started)""")
d.rep('S = "C:/Users/nathan/Source/kc143d23_1025"', 'S = "C:/Users/nathan/Source/k050d23_1104"')
d.rep('OUT = S + "/I1025-win/kc143_d23"', 'OUT = S + "/I1104-win"')
d.rep("# win2's accepted k_c 135 D 23.0 state and record (raw I1025-win2/kc135_d23; copies in inputs/)", "# my accepted k_c 143 D 23.0 kappa 0.7 state and record (raw I1025-win/kc143_d23; copies in inputs/)")
d.rep('SRC, TAG = "l1kc135win2d23", "l1kc143winbd23"', 'SRC, TAG = "l1kc143winbd23", "l1kc143winbk050d23"\nGATE = IN + "/gate_k050_1104.py"')
d.rep('B_STATE, B_REC = "cd134e2cc283fd5beb2e5beb6ad2e1f1353efe1d", "bc295fbcc4a90adaf224128d0160ce02ce68a0f7"', f'B_STATE, B_REC = "{B_STATE}", "{B_REC}"')
d.rep('(IN + "/kc143_syscheck_1025.py", "e15b0ee2b0b1f9e48a914b6e3e75f4fec48251f4"),', f'(IN + "/kc143_syscheck_1025.py", "e15b0ee2b0b1f9e48a914b6e3e75f4fec48251f4"), (IN + "/gate_k050_1104.py", "{B_GATE}"),')
d.rep('LOG = OUT + "/kc143_regrid_w.log"', 'LOG = OUT + "/k050_regrid_w.log"')
d.rep("CAPRG = 43200\n", "CAPRG = 64800          # t5, hc 2026-11-27 18:27 UTC: cap 64800 s (18 h); OUT/cap_seconds.txt, if present, overrides it while the re-solve runs\n")
d.rep("#1025 k_c 143 regrid at D 23.0 (from win2's k_c 135 state): {m}", "#1104 kappa 0.5 re-solve at k_c 143, D 23.0 (from my kappa 0.7 state): {m}")
d.rep("        if time.time() - t0 > cap:\n",
      "        try:\n"
      "            c2 = int(open(OUT + \"/cap_seconds.txt\").read().split()[0])\n"
      "            if c2 != cap:\n"
      "                say(f\"{tag}: cap changed from {cap} s to {c2} s (cap_seconds.txt)\"); cap = c2\n"
      "        except (OSError, ValueError, IndexError):\n"
      "            pass\n"
      "        if time.time() - t0 > cap:\n")
d.rep("its cap is {cap} s as t5 ordered; nothing is stopped at 6 h.", "its cap is {cap} s (t5: 64800 s); nothing is stopped at 6 h.")
d.rep("""say(f"kc143d23_regrid_driver_1025.py: the k_c 143 regrid at D 23.0 from win2's accepted k_c 135 D 23.0 state{' (dry run)' if DRY else ''}; checking pins")""",
      """say(f"k050d23_regrid_driver_1104.py: the kappa 0.5 re-solve of my k_c 143 D 23.0 state{' (dry run)' if DRY else ''}; checking pins")""")
d.rep("""say(f"pins ok (the inputs of {IN}, win2's k_c 135 D 23.0 files, worktree 48c36355""", """say(f"pins ok (the inputs of {IN}, my k_c 143 D 23.0 kappa 0.7 files, the gate, worktree 48c36355""")
d.rep('say("kc143d23_regrid_driver_1025.py done")', 'say("k050d23_regrid_driver_1104.py done")', 2)
d.rep("/sample_driver_kc143_1025.ps1", "/sample_driver_k050_1104.ps1")
d.rep("/kc143d23_watch_alert_1025.py", "/k050d23_watch_alert_1104.py")
d.rep('S + "/keepawake_1025.py", str(os.getpid()), "regrid", str(CAPRG + 1800)]', 'S + "/keepawake_1104.py", str(os.getpid()), "regrid", str(CAPRG + 43200)]')
d.rep("would start ell_refine.py {SRC} 135 {TAG} 143 1 23.0 {LAM0} --kappa 0.7 ", "would start ell_refine.py {SRC} 143 {TAG} 143 1 23.0 {LAM0} --kappa 0.5 ")
# step 3: the source
d.rx(r"# step 3: the source, through both checks.*?# step 4: the regrid\n",
     '''# step 3: the source (my k_c 143 kappa 0.7 state), through the checks (they re-freeze the state: minutes each)
t0 = time.time()
src = {}
for name, cmd in (("source_kc143_syscheck.txt", [PY, SY143, SRCREC, SRCSTATE, "23.0", WTM]), ("source_kc143_syscheck_mutate_F.txt", [PY, SY143, SRCREC, SRCSTATE, "23.0", WTM, "--mutate=F"]),
                  ("source_kc143_syscheck_mutate_steps.txt", [PY, SY143, SRCREC, SRCSTATE, "23.0", WTM, "--mutate=steps"]), ("source_kc135_syscheck.txt", [PY, SY135, SRCREC, SRCSTATE, "23.0", WTM]),
                  ("source_kc127_syscheck.txt", [PY, SY127, SRCREC, SRCSTATE, "23.0", WTM]), ("source_gate.txt", [PY, GATE, SRCREC])):
    r = sh(cmd, env=env)
    open(OUT + "/" + name, "w").write(r.stdout + r.stderr + f"exit {r.returncode}\\n")
    src[name] = r.returncode
want = {"source_kc143_syscheck.txt": 0, "source_kc143_syscheck_mutate_F.txt": 1, "source_kc143_syscheck_mutate_steps.txt": 1, "source_kc135_syscheck.txt": 1, "source_kc127_syscheck.txt": 1, "source_gate.txt": 1}
say(f"the source: kc143 check exit {src['source_kc143_syscheck.txt']} (0 wanted), --mutate=F {src['source_kc143_syscheck_mutate_F.txt']}, --mutate=steps {src['source_kc143_syscheck_mutate_steps.txt']} (1 wanted each), kc135 check {src['source_kc135_syscheck.txt']}, kc127 check {src['source_kc127_syscheck.txt']} and the kappa 0.5 gate {src['source_gate.txt']} (1 wanted each: they refuse the source); {time.time() - t0:.0f} s")
if src != want:
    finish(1, f"the source checks are not as wanted ({src}, wanted {want}): no re-solve")

# step 4: the re-solve
''')
d.rep('cmd = ["-u", "ell_refine.py", SRC, "135", TAG, "143", "1", "23.0", LAM0, "--kappa", "0.7",', 'cmd = ["-u", "ell_refine.py", SRC, "143", TAG, "143", "1", "23.0", LAM0, "--kappa", "0.5",')
d.rep('"regrid", notify_at=21600)', '"re-solve", notify_at=21600)')
d.rep('''    if (a.returncode, s143.returncode, m1.returncode, m2.returncode, k135.returncode) == (0, 0, 1, 1, 1):''',
      '''    g0, g1, g2, gs = sh([PY, GATE, rec], env=env), sh([PY, GATE, rec, "--mutate=f"], env=env), sh([PY, GATE, rec, "--mutate=steps"], env=env), sh([PY, GATE, "--selftest"], env=env)
    open(OUT + "/gate.txt", "w").write(f"gate on the result: exit {g0.returncode} (0 wanted)\\n{g0.stdout}{g0.stderr}\\n--mutate=f exit {g1.returncode} (1 wanted)\\n{g1.stdout}\\n--mutate=steps exit {g2.returncode} (1 wanted)\\n{g2.stdout}\\nselftest exit {gs.returncode} (0 wanted)\\n{gs.stdout}")
    say(f"gate (t5's bars |F| <= 5e-10, steps 6455-6719): exit {g0.returncode} (0 wanted): {g0.stdout.strip()}; --mutate=f {g1.returncode}, --mutate=steps {g2.returncode} (1 wanted each); its selftest {gs.returncode} (0 wanted)")
    if (a.returncode, s143.returncode, m1.returncode, m2.returncode, k135.returncode, g0.returncode, g1.returncode, g2.returncode, gs.returncode) == (0, 0, 1, 1, 1, 0, 1, 1, 0):''')
d.rep('''        why = "syscheck: " + (a.stdout.strip().splitlines() or [''])[-1]''', '''        why = "syscheck: " + (a.stdout.strip().splitlines() or [''])[-1] + "; gate: " + g0.stdout.strip()''')
d.rep('if row["stage"] == "regrid":', 'if row["stage"] in ("regrid", "re-solve"):')
d.rx(r'summ = \(f"regrid \{t_start.*?cpu \{pk\[\'cpu\'\]:\.0f\} s"\)',
     '''summ = (f"re-solve {t_start:%Y-%m-%d %H:%M:%S} to {t_end:%H:%M:%S} UTC, exit {rc}, wall {wall:.0f} s (record's seconds {recj.get('seconds')}); record (kappa {recj.get('kappa')}): |F| {recj.get('F')}, F_start {recj.get('F_start')}, "
        f"steps {recj.get('steps')}, constraint {recj.get('constraint')}, Delta {recj.get('Delta')}; the kappa 0.7 source record at D 23.0: |F| {srcj.get('F')}, steps {srcj.get('steps')}, constraint {srcj.get('constraint')}, Delta {srcj.get('Delta')}; "
        f"Delta(kappa 0.5) minus Delta(kappa 0.7) = {dd}; steps ratio {sratio} (t5's bars: |F| <= 5e-10, steps 6587 +- 132 = 6455 to 6719, i.e. 1.4 times 4705; freeze_from on the source state at kappa 0.5 gives 6582); {verdict}{(': ' + why) if why else ''}; "
        f"peak working set {pk['ws']:.2f} GB, peak private {pk['priv']:.2f} GB (the largest python of the tree, {pk['n']} samples), lowest free memory {pk['free']:.2f} GB, peak commit {pk['commit']:.1f} GB, cpu {pk['cpu']:.0f} s")''')
d.rx(r'hc\(f"finished: \{summ\}\. Raw I1025-win/kc143_d23 after my next push\. ".*?"No scan\."\)\)',
     '''hc(f"finished: {summ}. Raw I1104-win after my next push. " + ("The scan (d18_secant.py scan with the Rust block, --b12=rust --b12_threads=2, lambda 0.080 0.095 0.110 0.125, 4 evaluations, 2 processes) starts by itself now." if verdict == "ACCEPTED" else "No scan."))''')
d.rep('srcj = [json.loads(x) for x in open(SRCREC) if x.strip() and json.loads(x).get("D") == 23.0][-1]', 'srcj = [json.loads(x) for x in open(SRCREC) if x.strip() and json.loads(x).get("D") == 23.0][-1]     # my kappa 0.7 record')
assert "win2" not in d.t and "macm3" not in d.t, [l for l in d.t.splitlines() if "win2" in l or "macm3" in l]
wr("k050d23_regrid_driver_1104.py", d.t)

# ---------------------------------------------------------------------------------------------- the small files
t = rd("kc143d23_watch_alert_1025.py")
t = t.replace("C:/Users/nathan/Source/kc143d23_1025/I1025-win/kc143_d23/rows/", "C:/Users/nathan/Source/k050d23_1104/I1104-win/rows/")
assert t.count("The k_c 143 D 23.0 {label} stage") == 1 and t.count("#1025 winb (successor session), the k_c 143 D 23.0 stages") == 1 and t.count("kc143d23_watch_alert_1025.py") == 1
t = t.replace("The k_c 143 D 23.0 {label} stage", "The #1104 kappa 0.5 k_c 143 D 23.0 {label} stage").replace("#1025 winb (successor session), the k_c 143 D 23.0 stages", "#1104 winb, the kappa 0.5 k_c 143 D 23.0 stages").replace("kc143d23_watch_alert_1025.py", "k050d23_watch_alert_1104.py")
wr("k050d23_watch_alert_1104.py", t)
wr("sample_driver_k050_1104.ps1", rd("sample_driver_kc143_1025.ps1"))
t = rd("keepawake_1025.py")
assert t.count("C:/Users/nathan/Source/kc143d23_1025/I1025-win/kc143_d23/rows/") == 1
wr("keepawake_1104.py", t.replace("C:/Users/nathan/Source/kc143d23_1025/I1025-win/kc143_d23/rows/", "C:/Users/nathan/Source/k050d23_1104/I1104-win/rows/").replace("keepawake_1025.py", "keepawake_1104.py"))
t = rd("session_check_1025.ps1")
assert t.count(r"$out = 'C:\Users\nathan\Source\kc143d23_1025\I1025-win\kc143_d23'") == 1
wr("session_check_1104.ps1", t.replace(r"$out = 'C:\Users\nathan\Source\kc143d23_1025\I1025-win\kc143_d23'", r"$out = 'C:\Users\nathan\Source\k050d23_1104\I1104-win'").replace("session_check_1025.ps1", "session_check_1104.ps1"))
GO = r"""@echo off
rem #1104 winb: the kappa 0.5 chain of my k_c 143 D 23.0 state (t5's order of 2026-11-27 18:23 UTC): the re-solve driver (source checks, ell_refine.py --kappa 0.5, acceptance); only if regrid_accepted.txt exists, the scan driver (d18_secant.py scan with the Rust block, 2 processes).
rem started as: conhost.exe --headless cmd.exe /c <this file> (Win32_Process.Create; no Windows Terminal handoff). Each driver runs in this console (start /b), BelowNormal, with its own keep-awake helper.
set "PATH=C:\Program Files\Git\usr\bin;C:\Program Files\Git\mingw64\bin;C:\Program Files\Git\cmd;%PATH%"
set "PYTHONDONTWRITEBYTECODE=1"
cd /d C:\Users\nathan\Source\k050d23_1104
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\k050d23_1104\k050d23_regrid_driver_1104.py > C:\Users\nathan\Source\k050d23_1104\k050d23_regrid_driver_stdout.log 2>&1
if not exist C:\Users\nathan\Source\k050d23_1104\I1104-win\regrid_accepted.txt exit /b 1
if not exist C:\Users\nathan\Source\k050d23_1104\k050d23_scan_driver_1104.py exit /b 1
start "" /wait /belownormal /b C:\Users\nathan\Source\venv-md510\Scripts\python.exe -u C:\Users\nathan\Source\k050d23_1104\k050d23_scan_driver_1104.py "0.095,0.080;0.110,0.125" > C:\Users\nathan\Source\k050d23_1104\k050d23_scan_driver_stdout.log 2>&1
"""
wr("go_k050d23_1104.cmd", GO, crlf=True)
# publish script: the k_c 143 one, renamed, with this stage's file list (only I1104-win is copied; pushes with push_1104.sh)
p = rd("publish_kc143d23_1025.sh")
p = p.replace("kc143d23_1025", "k050d23_1104").replace("I1025-win/kc143_d23", "I1104-win").replace("staged k_c 143 D 23.0 folder", "staged I1104-win folder")
p = p.replace("/c/Users/nathan/Source/choptuik-i1025/push_1025.sh", "/c/Users/nathan/Source/k050d23_1104/push_1104.sh")
i = p.index("for f in make_k050d23_1104.py")
j = p.index("; do\n", i)
p = p[:i] + ("for f in make_k050d23_1104.py k050d23_regrid_driver_1104.py k050d23_watch_alert_1104.py sample_driver_k050_1104.ps1 go_k050d23_1104.cmd keepawake_1104.py session_check_1104.ps1 steps_check_1104.py steps_check_1104.txt "
             "k050d23_regrid_driver_stdout.log publish_k050d23_1104.sh push_1104.sh") + p[j:]
assert "mkdir -p \"$D/rows\" \"$D/secant\"" in p
p = p.replace('bash /c/Users/nathan/Source/k050d23_1104/push_1104.sh', 'cp "$S/inputs/gate_k050_1104.py" "$D/"\nbash /c/Users/nathan/Source/k050d23_1104/push_1104.sh')
wr("publish_k050d23_1104.sh", p)
wr("push_1104.sh", open("C:/Users/nathan/Source/i1102_1025/push_1102.sh", encoding="utf-8").read().replace("I1102-win", "I1104-win").replace("(copy of push_1025.sh that adds I1102-win; push_1025.sh itself is unchanged)", "(copy of push_1025.sh that adds I1104-win; push_1025.sh itself is unchanged)"))
print("made")

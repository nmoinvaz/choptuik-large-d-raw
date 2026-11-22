#!/usr/bin/env python3
"""#1025 winb, k_c 79 at D 19: derives the D 19 drivers and watcher from the D 18.5 ones (kc79_1025/, raw I1025-win/kc79_d185) by exact string replacements, each asserted to occur once,
and writes the diff of each against its D 18.5 original (diff_*_vs_d185.txt). Nothing else is changed."""
import difflib

A = "C:/Users/nathan/Source/kc79_1025/"
B = "C:/Users/nathan/Source/kc79d19_1025/"


def rd(f):
    return open(A + f, newline="").read().replace("\r\n", "\n")


def rep(s, old, new, n=1):
    assert s.count(old) == n, (old[:80], s.count(old))
    return s.replace(old, new)


def out(src, dst, s, lab):
    open(B + dst, "w", newline="\n").write(s)
    d = difflib.unified_diff(rd(src).splitlines(), s.splitlines(), src + " (D 18.5)", dst + " (D 19)", lineterm="", n=0)
    open(B + "diff_" + lab + "_vs_d185.txt", "w").write("\n".join(d) + "\n")


# ---------------- regrid driver
s = rd("kc79_regrid_driver_1025.py")
doc = '''#!/usr/bin/env python3
"""#1025 winb, the k_c 79 regrid at D 19 (t5's order, hc of 2026-11-22 ~09:41 UTC): win2's accepted k_c 71 D 19 state (from its leap, raw I1025-win2/kc71_leap, found by prep_kc79d19_find_1025.sh) is
regridded to k_c 79 with the same command as at D 18.5 (raw I1025-win/kc79_d185), only D, the source tag and the lambda_0 argument changed:
  D 18.5: ell_refine.py l1kc71Wm1025 71 l1kc79Wm1025 79 1 18.5 2.1181259879 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
  D 19:   ell_refine.py SRC 71 l1kc79W19m1025 79 1 19 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (SRC and the pins from kc79d19_cfg_1025.txt; lambda_0 unused with --no-gamma)
4 threads, BelowNormal, cap 21600 s by the exact pid. Accepted only by kc79_syscheck_1025.py (win2's kc71_syscheck rule with k_c 71 replaced by k_c 79) and its two controls (|F| x 1.5 and steps + 1
refused, on the same numbers and through --mutate). Before the regrid win2's own check must accept the k_c 71 source state on this machine. A refusal, a failed control or a regrid that does not
converge stops here with a report. THE SCAN IS NOT STARTED (t5 gives the window); kc79d19_scan_driver_1025.py takes it as an argument. Memory: no guard, the alert-only watcher is a separate process.
usage: kc79d19_regrid_driver_1025.py [--selftest]"""
'''
s = doc + s[s.index("import csv, datetime"):]
s = rep(s, 'S = "C:/Users/nathan/Source/kc79_1025"\nOUT = S + "/I1025-win/kc79_d185"', 'S = "C:/Users/nathan/Source/kc79d19_1025"\nOUT = S + "/I1025-win/kc79_d19"')
s = rep(s, 'COORD = "nathans-macbook-air-m5-3/t2j"', 'COORD = "nathans-macbook-air-m5-3/t5"')
s = rep(s, 'SRC, TAG = "l1kc71Wm1025", "l1kc79Wm1025"\nSTATE_N = f"sol_{TAG}_D18.5000.npy"',
        'ST = "--selftest" in sys.argv          # the cap selftest needs no source state\n'
        'CFG = {"SRC": "none"} if ST else dict(l.strip().split("=", 1) for l in open(S + "/kc79d19_cfg_1025.txt") if "=" in l and not l.startswith("#"))\n'
        'SRC, TAG = CFG["SRC"], "l1kc79W19m1025"\nSTATE_N = f"sol_{TAG}_D19.0000.npy"\n'
        'PINS = {} if ST else {p: b for b, p in (ln.split() for ln in open(S + "/prep_kc79d19_pins_1025.txt"))}')
s = rep(s, 'say("kc79_regrid_driver_1025.py: the k_c 79 regrid at D 18.5; checking pins")', 'say("kc79d19_regrid_driver_1025.py: the k_c 79 regrid at D 19; checking pins")')
s = rep(s, 'for ln in open(S + "/prep_kc79_pins_1025.txt"):\n    b, p = ln.split()\n', 'for p, b in PINS.items():\n')
s = rep(s, 'if blob(WTM + f"/data/sol_{SRC}_D18.5000.npy") != "28bf6bacc1e8e6563896ae003a3f85ca23ddce63":\n    say("REFUSE: the source state in the worktree is not blob 28bf6bac"); sys.exit(2)',
        'if blob(WTM + f"/data/sol_{SRC}_D19.0000.npy") != PINS[CFG["SRCSTATE"]]:\n    say("REFUSE: the source state in the worktree is not the pinned blob " + PINS[CFG["SRCSTATE"]][:8]); sys.exit(2)')
s = rep(s, "(blobs in prep_kc79_pins_1025.txt;", "(blobs in prep_kc79d19_pins_1025.txt;")
s = rep(s, 'S + "/kc79_watch_alert_1025.py"', 'S + "/kc79d19_watch_alert_1025.py"')
s = rep(s, 'SY71 = RAW + "/I1025-win2/kc71_d185/kc71_syscheck.py"', 'SY71 = RAW + "/" + CFG["SRCCHECK"]')
s = rep(s, 'r2 = sh([PY, SY71, RAW + "/I1025-win2/kc71_d185/l1kc71Wm1025.jsonl", WTM + f"/data/sol_{SRC}_D18.5000.npy", "18.5", WTM], env=env)',
        'r2 = sh([PY, SY71, RAW + "/" + CFG["SRCREC"], WTM + f"/data/sol_{SRC}_D19.0000.npy", "19", WTM], env=env)')
s = rep(s, "on win2's accepted k_c 71 state: exit", "on win2's k_c 71 D 19 state: exit")
s = rep(s, '"1", "18.5", "2.1181259879"', '"1", "19", "2.1156378446"')
s = rep(s, 'a = sh([PY, SY, rec, state, "18.5", WTM], env=env)', 'a = sh([PY, SY, rec, state, "19", WTM], env=env)')
s = rep(s, '[PY, SY, rec, state, "18.5", WTM, "--mutate=F"]', '[PY, SY, rec, state, "19", WTM, "--mutate=F"]')
s = rep(s, '[PY, SY, rec, state, "18.5", WTM, "--mutate=steps"]', '[PY, SY, rec, state, "19", WTM, "--mutate=steps"]')
s = rep(s, "recj = json.loads(open(rec).read().strip().splitlines()[-1]) if os.path.exists(rec) and os.path.getsize(rec) > 0 else {}\n",
        "recj = json.loads(open(rec).read().strip().splitlines()[-1]) if os.path.exists(rec) and os.path.getsize(rec) > 0 else {}\n"
        "try:\n    srcj = [json.loads(x) for x in open(RAW + \"/\" + CFG[\"SRCREC\"]) if x.strip() and json.loads(x).get(\"D\") == 19.0][-1]\nexcept Exception:\n    srcj = {}\n")
s = rep(s, "Delta {recj.get('Delta')} (source {recj.get('Delta_src')}); {verdict}",
        "Delta {recj.get('Delta')}; the k_c 71 source record at D 19: |F| {srcj.get('F')}, steps {srcj.get('steps')}, constraint {srcj.get('constraint')}, Delta {srcj.get('Delta')}; {verdict}")
s = rep(s, '#1025 k_c 79 regrid at D 18.5 finished: {summ}. Raw I1025-win/kc79_d185 after my next push. "\n    + ("The hybrid scan (1.66 to 1.69) starts now." if verdict == "ACCEPTED" else "No scan starts.")])',
        '#1025 k_c 79 regrid at D 19 finished: {summ}. Raw I1025-win/kc79_d19 after my next push. "\n    + ("The scan is NOT started: it waits for your window." if verdict == "ACCEPTED" else "No scan.")])')
i = s.index('if verdict == "ACCEPTED":\n    q = subprocess.Popen')
j = s.index('say("kc79_regrid_driver_1025.py done")')
s = s[:i] + 'say("scan not started: the window is the coordinator\'s to give (kc79d19_scan_driver_1025.py WINDOW)")\nsay("kc79d19_regrid_driver_1025.py done")' + s[j + len('say("kc79_regrid_driver_1025.py done")'):]
out("kc79_regrid_driver_1025.py", "kc79d19_regrid_driver_1025.py", s, "regrid_driver")

# ---------------- scan driver
t = rd("kc79_scan_driver_1025.py")
doc = '''#!/usr/bin/env python3
"""#1025 winb, the k_c 79 hybrid scan at D 19 (t5's order, hc of 2026-11-22 ~09:41 UTC; the window is t5's to give and is an argument, so the driver needs no edit):
xfkappa's d18_hybsign.py (raw I1025-mac/d18, blob e089207a, unchanged) on the accepted k_c 79 state sol_l1kc79W19m1025_D19.0000.npy and its record, at the lambda list WINDOW (comma-separated),
the 1e-15 noise test on blocks 0-11 (2 seeds) and the float64 sign, ONE process, 4 threads, BelowNormal, cap 28800 s (8 h) by the exact pid. d18_hybsign.py checks the record system first
(exit 3 if the state does not come back). Starts only when regrid_accepted.txt exists and the scan file does not. Memory: no guard, the alert-only watcher is its own process. Then d18f_read.py window
(xfkappa's reader: every robust change with its det-linear estimate and range) and an hc to the coordinator t5. Never started by the regrid driver.
usage: kc79d19_scan_driver_1025.py LAMBDA_LIST [--dry]     e.g. 1.55,1.56,1.57,1.58     (--dry: runs the checks, prints the planned command, starts nothing)"""
'''
t = doc + t[t.index("import datetime, os, re"):]
t = rep(t, 'S = "C:/Users/nathan/Source/kc79_1025"\nOUT = S + "/I1025-win/kc79_d185"', 'S = "C:/Users/nathan/Source/kc79d19_1025"\nOUT = S + "/I1025-win/kc79_d19"')
t = rep(t, 'COORD = "nathans-macbook-air-m5-3/t2j"', 'COORD = "nathans-macbook-air-m5-3/t5"')
t = rep(t, 'TAG = "l1kc79Wm1025"', 'TAG = "l1kc79W19m1025"')
t = rep(t, 'STATE, REC = OUT + f"/sol_{TAG}_D18.5000.npy", OUT + f"/{TAG}.jsonl"', 'STATE, REC = OUT + f"/sol_{TAG}_D19.0000.npy", OUT + f"/{TAG}.jsonl"')
t = rep(t, 'SCAN, LOG = OUT + "/scan_kc79_D185_1025.jsonl", OUT + "/kc79_scan_w.log"', 'SCAN, LOG = OUT + "/scan_kc79_D19_1025.jsonl", OUT + "/kc79d19_scan_w.log"')
t = rep(t, 'LAMS = "1.66,1.67,1.68,1.69"\n',
        'DRY = "--dry" in sys.argv\n'
        'args = [a for a in sys.argv[1:] if not a.startswith("--")]\n'
        'if len(args) != 1:\n    print("usage: kc79d19_scan_driver_1025.py LAMBDA_LIST [--dry]"); sys.exit(2)\n'
        'LAMS = args[0]\n'
        'try:\n    LV = [float(v) for v in LAMS.split(",")]\nexcept ValueError:\n    print("REFUSE: the window is not a comma-separated list of numbers:", LAMS); sys.exit(2)\n'
        'if len(LV) < 2 or len(set(LV)) != len(LV) or not all(0.0 < v < 10.0 for v in LV):\n    print("REFUSE: the window needs at least two distinct values in (0, 10):", LAMS); sys.exit(2)\n'
        'LO, HI = f"{min(LV):g}", f"{max(LV):g}"\n'
        'if DRY:\n    LOG = LOG + ".dry"\n')
t = rep(t, 'os.makedirs(OUT + "/rows", exist_ok=True)\nopen(OUT + "/rows/scan_driver.pid", "w").write(str(os.getpid()))\n',
        'def refuse(m, h):\n    say("REFUSE: " + m)\n    if DRY:\n        say("DRY: a real run would stop here")\n        return\n    hc(h)\n    sys.exit(2)\n\n\n'
        'os.makedirs(OUT + "/rows", exist_ok=True)\nif not DRY:\n    open(OUT + "/rows/scan_driver.pid", "w").write(str(os.getpid()))\n')
t = rep(t, 'say("kc79_scan_driver_1025.py: the k_c 79 hybrid scan at D 18.5; checking pins")', 'say(f"kc79d19_scan_driver_1025.py: the k_c 79 hybrid scan at D 19, window {LAMS}{\' (dry run)\' if DRY else \'\'}; checking pins")')
t = rep(t, 'say("REFUSE: regrid_accepted.txt does not exist"); hc("not started: the regrid is not accepted."); sys.exit(2)', 'refuse("regrid_accepted.txt does not exist", "not started: the regrid is not accepted.")')
t = rep(t, 'say(f"REFUSE: {fn} is blob {got}, not {want}"); hc(f"not started: pin {fn} is blob {got[:8]}."); sys.exit(2)', 'refuse(f"{fn} is blob {got}, not {want}", f"not started: pin {fn} is blob {got[:8]}.")')
t = rep(t, 'say(f"REFUSE: worktree not at 48c36355 or {SCAN} exists"); hc("not started: worktree or scan file check failed."); sys.exit(2)', 'refuse(f"worktree not at 48c36355 or {SCAN} exists", "not started: worktree or scan file check failed.")')
t = rep(t, 'samp = subprocess.Popen(["powershell"',
        'if DRY:\n    say(f"DRY: would start d18_hybsign.py {REC} {STATE} 19 {LAMS} {SCAN} (cwd {WTM}, 4 threads, BelowNormal, cap {CAP} s); reader window {LO} {HI}; nothing started"); sys.exit(0)\n'
        'samp = subprocess.Popen(["powershell"')
t = rep(t, 'S + "/kc79_watch_alert_1025.py"', 'S + "/kc79d19_watch_alert_1025.py"')
t = rep(t, 'cmd = [PY, "-u", SCANNER, REC, STATE, "18.5", LAMS, SCAN]', 'cmd = [PY, "-u", SCANNER, REC, STATE, "19", LAMS, SCAN]')
t = rep(t, 'say(f"scan: started pid {p.pid}: d18_hybsign.py {REC} {STATE} 18.5 {LAMS} {SCAN}")', 'say(f"scan: started pid {p.pid}: d18_hybsign.py {REC} {STATE} 19 {LAMS} {SCAN}")')
t = rep(t, "scan_kc79_raw.log", "scan_kc79d19_raw.log", 2)
t = rep(t, 'OUT + "/scan_kc79_D185.log"', 'OUT + "/scan_kc79_D19.log"')
t = rep(t, "Points so far in scan_kc79_D185_1025.jsonl.", "Points so far in scan_kc79_D19_1025.jsonl.")
t = rep(t, 'say("kc79_scan_driver_1025.py done (no reading)")', 'say("kc79d19_scan_driver_1025.py done (no reading)")')
i = t.index('r = sh([PY, READER, "window", "18.5", "1.66", "1.69", SCAN]')
t = t[:i] + '''r = sh([PY, READER, "window", "19", LO, HI, SCAN], cwd=WTM, env=renv)
txt = "\\n".join(l for l in (r.stdout + "\\n" + r.stderr).splitlines() if "Warning" not in l and not l.startswith("  return "))
open(OUT + "/read_kc79_D19.log", "w").write(txt + "\\n")
for ln in txt.splitlines():
    say(ln)
chg = [l.strip() for l in txt.splitlines() if "change in" in l]
hc(f"the scan ended (exit 0, {time.time() - t0:.0f} s, window {LAMS}). Reader (d18f_read.py window 19 {LO} {HI}): " + ("; ".join(chg) if chg else "no change line") + ". Raw I1025-win/kc79_d19 after my next push; no reading by me, you rule.")
time.sleep(70)          # the sampler's last line
samp.kill()
say("kc79d19_scan_driver_1025.py done")
'''
out("kc79_scan_driver_1025.py", "kc79d19_scan_driver_1025.py", t, "scan_driver")

# ---------------- watcher
w = rd("kc79_watch_alert_1025.py")
w = rep(w, "sends the coordinator t2j ONE hc alert", "sends the coordinator t5 ONE hc alert")
w = rep(w, "#1025 winb (successor session), the k_c 79 check:", "#1025 winb (successor session), the k_c 79 check at D 19:")
w = rep(w, "usage: kc79_watch_alert_1025.py", "usage: kc79d19_watch_alert_1025.py")
w = rep(w, 'COORD = "nathans-macbook-air-m5-3/t2j"', 'COORD = "nathans-macbook-air-m5-3/t5"')
w = rep(w, "C:/Users/nathan/Source/kc79_1025/I1025-win/kc79_d185/rows/", "C:/Users/nathan/Source/kc79d19_1025/I1025-win/kc79_d19/rows/")
w = rep(w, "The k_c 79 {label} stage", "The k_c 79 D 19 {label} stage")
out("kc79_watch_alert_1025.py", "kc79d19_watch_alert_1025.py", w, "watcher")
print("ok")

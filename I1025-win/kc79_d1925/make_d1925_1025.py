#!/usr/bin/env python3
"""#1025 winb, k_c 79 at D 19.25 (t5's order, hc of 2026-11-22 ~16:10 UTC): derives the D 19.25 drivers, watcher, find script, launchers and publish script from the D 19 ones
(C:/Users/nathan/Source/kc79d19_1025, raw I1025-win/kc79_d19 at 010273bc) by regex and exact replacements, each asserted, writes the D 19.25 staging folder and a diff against the D 19 file for each
(diff_*_vs_d19.txt). Changed: D 19 -> 19.25, the state names D19.0000 -> D19.2500, tags, folder and file names (kc79d19 -> kc79d1925), lambda_0 (2.1156378446 -> 2.1144367878, ell_delta.lam0_at at 19.25,
unused with --no-gamma), the source rule of the find script (win2's D 19.25 state, record line D == 19.25). Nothing else. Prints every remaining bare '19' for a look."""
import difflib, os, re, shutil, sys

A = "C:/Users/nathan/Source/kc79d19_1025"
B = "C:/Users/nathan/Source/kc79d1925_1025"
os.makedirs(B + "/I1025-win/kc79_d1925/rows", exist_ok=True)


def sub(s, old, new, n=1, what=""):
    assert s.count(old) == n, f"{what or old[:60]!r}: found {s.count(old)}, wanted {n}"
    return s.replace(old, new)


def rsub(s, pat, new, n=None, what=""):
    s2, k = re.subn(pat, new, s)
    assert k > 0 and (n is None or k == n), f"{what or pat}: {k} matches, wanted {n}"
    return s2


def common(s):
    """names: folder, tags, state and log names; applied once to every derived file"""
    s = s.replace("kc79d19", "kc79d1925").replace("kc79_d19", "kc79_d1925")
    s = s.replace("l1kc79W19m1025", "l1kc79W1925m1025")
    s = s.replace("scan_kc79_D19", "scan_kc79_D1925").replace("read_kc79_D19", "read_kc79_D1925")
    s = s.replace("_D19.0000(00)", "_D19.2500(00)").replace("_D19.0000.npy", "_D19.2500.npy")
    s = s.replace("make_d19_1025", "make_d1925_1025")
    s = re.sub(r"diff_(\w+)_vs_d185\.txt", r"diff_\1_vs_d19.txt", s)
    s = re.sub(r"\bD 19(?![\d.])", "D 19.25", s)                 # narrative: 'D 19' -> 'D 19.25'
    return s


ORDER = "t5's order, hc of 2026-11-22 ~16:10 UTC"
made = {}

# ---- the regrid driver
s = open(A + "/kc79d19_regrid_driver_1025.py").read()
head, rest = s.split('"""', 2)[0], s.split('"""', 2)[2]
doc = f'''#1025 winb, the k_c 79 regrid at D 19.25 ({ORDER}): win2's accepted k_c 71 D 19.25 state (from its leap, raw I1025-win2/kc71_leap, found by prep_kc79d1925_find_1025.py) is
regridded to k_c 79 with the same command as at D 19 (raw I1025-win/kc79_d19), only D, the output tag and the lambda_0 argument changed:
  D 19:    ell_refine.py SRC 71 l1kc79W19m1025 79 1 19 2.1156378446 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma
  D 19.25: ell_refine.py SRC 71 l1kc79W1925m1025 79 1 19.25 2.1144367878 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma     (SRC and the pins from kc79d1925_cfg_1025.txt; lambda_0 unused with --no-gamma)
4 threads, BelowNormal, cap 21600 s by the exact pid. Accepted only by kc79_syscheck_1025.py (win2's kc71_syscheck rule with k_c 71 replaced by k_c 79) and its two controls (|F| x 1.5 and steps + 1
refused, on the same numbers and through --mutate). Before the regrid win2's own check must accept the k_c 71 source state on this machine. A refusal, a failed control or a regrid that does not
converge stops here with a report. NO SCAN IS STARTED (the window comes from the coordinator); kc79d1925_scan_driver_1025.py takes it as an argument. Memory: no guard, the alert-only watcher is a separate process.
usage: kc79d1925_regrid_driver_1025.py [--selftest]'''
s = common(head) + '"""' + doc + '"""' + common(rest)
s = sub(s, '"1", "19", "2.1156378446"', '"1", "19.25", "2.1144367878"', 1, "regrid cmd")
s = sub(s, '"19", WTM', '"19.25", WTM', 4, "check D args")
s = sub(s, '.get("D") == 19.0]', '.get("D") == 19.25]', 1, "source record line")
made["kc79d1925_regrid_driver_1025.py"] = ("kc79d19_regrid_driver_1025.py", s)

# ---- the scan driver (not started; the window is t5's)
s = open(A + "/kc79d19_scan_driver_1025.py").read()
s = common(s)
s = sub(s, "(t5's order, hc of 2026-11-22 ~09:41 UTC;", f"({ORDER};", 1, "scan order stamp")
s = sub(s, 'REC, STATE, "19", LAMS, SCAN]', 'REC, STATE, "19.25", LAMS, SCAN]', 1, "scan cmd")
s = sub(s, "{STATE} 19 {LAMS}", "{STATE} 19.25 {LAMS}", 2, "scan say")
s = sub(s, '"window", "19", LO, HI', '"window", "19.25", LO, HI', 1, "reader cmd")
s = sub(s, "window 19 {LO} {HI}", "window 19.25 {LO} {HI}", 1, "reader hc")
made["kc79d1925_scan_driver_1025.py"] = ("kc79d19_scan_driver_1025.py", s)

# ---- the watcher
s = open(A + "/kc79d19_watch_alert_1025.py").read()
s = common(s)
made["kc79d1925_watch_alert_1025.py"] = ("kc79d19_watch_alert_1025.py", s)

# ---- the find script
s = open(A + "/prep_kc79d19_find_1025.py").read()
s = common(s)
s = sub(s, "DV = float(REH) if REH else 19.0", "DV = float(REH) if REH else 19.25", 1, "DV")
s = sub(s, 'r"19\\.0000(00)?"', 'r"19\\.2500(00)?"', 1, "PAT")
i, j = s.index("    t0 = {"), s.index("    ok = True")
new = '''    P = "I1025-win2/kc71_leap/states/sol_l1kc71Lw1025"
    t0 = {P + "_D19.187500.npy": "a"}
    t1 = dict(t0, **{P + "_D19.250000.npy": "b"})
    t2 = dict(t1, **{P + "_D19.2500.npy": "b"})
    t3 = dict(t2, **{P + "b_D19.2500.npy": "c"})
    t4 = dict(t1, **{P + "_D19.2500.npy": "x"})
    cases = [("D 19.1875 only", t0, "none"), ("the .6f name only", t1, "ok"), ("both names, equal blobs", t2, "ok"), ("two tags", t3, "many"), ("two names, different blobs", t4, "differ"),
             ("a k_c 63 state at D 19.25", {"I1025-win2/x/sol_l1kc63Lw1025_D19.250000.npy": "d"}, "none"), ("D 19.0", {P + "_D19.000000.npy": "e"}, "none"),
             ("D 19.3125", {P + "_D19.312500.npy": "f"}, "none"), ("D 19.25 in a k_c 79 tag", {"I1025-win2/x/sol_l1kc79Lw1025_D19.250000.npy": "g"}, "none")]
'''
s = s[:i] + new + s[j:]
s = sub(s, "_D19.2500.npy or _D19.000000.npy)", "_D19.2500.npy or _D19.250000.npy)", 1, "find docstring")
made["prep_kc79d1925_find_1025.py"] = ("prep_kc79d19_find_1025.py", s)

# ---- launchers and publish script
for fa, fb in (("start_kc79d19_regrid_1025.cmd", "start_kc79d1925_regrid_1025.cmd"), ("start_kc79d19_scan_1025.cmd", "start_kc79d1925_scan_1025.cmd")):
    made[fb] = (fa, common(open(A + "/" + fa).read()))
s = open(A + "/publish_kc79d19_1025.sh").read()
s = common(s)
s = sub(s, "diff_regrid_driver_vs_d19.txt diff_scan_driver_vs_d19.txt diff_watcher_vs_d19.txt", "diff_regrid_driver_vs_d19.txt diff_scan_driver_vs_d19.txt diff_watcher_vs_d19.txt diff_find_vs_d19.txt", 1, "publish diffs")
s = sub(s, "selftest_find_1025.txt rehearsal_find.txt selftest_scan_dry_1025.txt", "selftest_find_1025.txt find_run_1025.txt selftest_scan_dry_1025.txt", 1, "publish rehearsal")
made["publish_kc79d1925_1025.sh"] = ("publish_kc79d19_1025.sh", s)

# ---- write, diff, look for leftovers
for name, (srcname, text) in made.items():
    open(f"{B}/{name}", "w", newline="\n").write(text)
for key, (name, srcname) in {"regrid_driver": ("kc79d1925_regrid_driver_1025.py", "kc79d19_regrid_driver_1025.py"), "scan_driver": ("kc79d1925_scan_driver_1025.py", "kc79d19_scan_driver_1025.py"),
                             "watcher": ("kc79d1925_watch_alert_1025.py", "kc79d19_watch_alert_1025.py"), "find": ("prep_kc79d1925_find_1025.py", "prep_kc79d19_find_1025.py")}.items():
    d = "".join(difflib.unified_diff(open(f"{A}/{srcname}").read().splitlines(1), open(f"{B}/{name}").read().splitlines(1), srcname, name, n=0))
    open(f"{B}/diff_{key}_vs_d19.txt", "w", newline="\n").write(d)
for f in ("kc79_syscheck_1025.py", "sample_driver4_1025.ps1", "prep_kc79d19_pins_fixed.txt"):
    shutil.copy(f"{A}/{f}", f"{B}/{f.replace('kc79d19', 'kc79d1925')}")
for name in made:
    for n, ln in enumerate(open(f"{B}/{name}").read().splitlines(), 1):
        for m in re.finditer(r"(?<![\d.A-Za-z_])19(?![\d.]|25)", ln):
            print(f"leftover bare 19: {name}:{n}: ...{ln[max(0, m.start() - 40):m.end() + 40]}...")
print("derived:", ", ".join(made))

"""#937: c1_pred (--project_start pred) against dh610's chain_k160.log (the default), the step from D 234.

From each log, in order, the a = 0.5 attempt's (D 234.5) Newton iteration-0 trial lines ("on 0 trial lam L: max|F| F;
simplified correction / |dz| = R ... refused/accepted"), and from c1_pred's [937] project lines the stages of each
projection (pred_q, u0, u0q: |R| before and after; ladder). dh610's log gives the u0 and u0q stages in its
"projection failed" lines (why_failed). Printed: one row per trial with both runs' max|F|, ratio and verdict and whether
they agree as printed, and the projection's stages in each run. Then the a = 1 attempt's re-seed line in each log.

Check (can fail): the outcome of each trial (refused or accepted) is the same in both runs, and the printed max|F|
and ratio agree. That is the control A2 holding and A1 failing; any trial where c1_pred accepts or prints different
numbers is a changed outcome.

Run: python3 compare937.py C1_PRED.log DH610_CHAIN.log
"""
import re
import sys

TRIAL = re.compile(r"^\s+on 0 trial lam (\S+): max\|F\| (\S+); simplified correction / \|dz\| = (\S+) .*?(refused|accepted)")
PROJ = re.compile(r"^\s+\[937\] project: (\w+); (.*); (\S+) s$")
FAILED = re.compile(r"^\s+on 0, lam (\S+): projection failed \(\d+\): point max\|F\| (\S+); u0 rung (\d+) its, \|R\| (\S+) -> "
                    r"(\S+), [^;]*; u0 quad-double (\d+) its, \|R\| (\S+) -> (\S+),")
RESEED = re.compile(r"^\s+a 1\.0000: re-seeded \((.*)")


def read(path, mine):
    trials, projs, fails, reseed, last = [], [], {}, None, None
    in_half = False
    for ln in open(path, errors="replace"):
        if "a 0.5000: re-seeded" in ln:
            in_half = True
        if not in_half:
            m = RESEED.match(ln)
            if m:
                reseed = m.group(1).strip()     # the last a = 1 re-seed before the a = 0.5 attempt (D 234 -> 235)
        if not in_half:
            continue
        m = TRIAL.match(ln)
        if m:
            trials.append(m.groups())
            projs.append(last)          # the projection of this trial's point: the last [937] line before it
            last = None
            if len(trials) >= 8:
                break
            continue
        m = PROJ.match(ln) if mine else FAILED.match(ln)
        if m:
            if mine:
                last = m.groups()
            else:
                fails[m.group(1)] = m.groups()
    return trials, projs, fails, reseed


a_t, a_p, _, a_r = read(sys.argv[1], True)
b_t, _, b_f, b_r = read(sys.argv[2], False)
print(f"a = 1 re-seed: c1_pred {a_r}")
print(f"               dh610   {b_r}")
proj_of_trial = a_p
ok = True
print("| lam | c1_pred max|F|, ratio, verdict | dh610 | same | c1_pred projection stages | dh610's u0, u0q |")
print("|---|---|---|---|---|---|")
for i, t in enumerate(a_t):
    u = b_t[i] if i < len(b_t) else None
    same = u is not None and t == u
    ok &= same
    pr = proj_of_trial[i] or ("-", "-", "-")
    f = b_f.get(t[0])
    fd = f"u0 {f[3]} -> {f[4]}; u0q {f[6]} -> {f[7]}" if f else "-"
    print(f"| {t[0]} | {t[1]}, {t[2]}, {t[3]} | " + (f"{u[1]}, {u[2]}, {u[3]}" if u else "-") +
          f" | {'yes' if same else 'NO'} | {pr[0]}: {pr[1]} | {fd} |")
print(f"trials compared {len(a_t)}; check (every outcome and printed value the same): {'pass' if ok else 'FAIL'}")

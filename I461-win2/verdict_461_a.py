#!/usr/bin/env python3
"""I461-win2 part A: the six verdicts of `hp/reseed.py checkq` and `truthq`, with their numbers beside the M5 Mac's (issue #461).

    python -I verdict_461_a.py [DIR]
        DIR (default: this folder) holds A_<n>_*.log and exits.txt written by run_i461_a.sh. Each log's last `checkq`/`truthq` line gives the
        verdict (PASS or FAIL) and the number; exits.txt gives the exit code (0 for PASS, 1 for FAIL). A run is "as required" when its
        verdict is the one the issue's table demands (PASS for runs 1, 3, 4, 5; FAIL for the two --sweeps 1 controls, runs 2 and 6) and the
        exit code agrees with the verdict. Exit 0: all six as required (part A passes). Exit 1: some run is not as required, among them a
        control that did not fail (the comparison could not fail). Exit 2: a log or an exit line is missing.
    python -I verdict_461_a.py --selftest
        synthetic logs: the required verdicts pass, a must-PASS run that FAILs and a control that PASSes each make the exit 1, a missing log exit 2."""
import os
import re
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
# (log stem, must, what the issue's table gives for the Mac)
RUNS = [
    ("A_1_checkq_d6_D215.0", "PASS", "checkq d6 D 215.0", "u0 residual 8.78e-32"),
    ("A_2_checkq_d6_D215.0_sweeps1", "FAIL", "the same, --sweeps 1 (control)", "stops at 1.21e-06"),
    ("A_3_checkq_d6_D209.0", "PASS", "checkq d6 D 209.0", "1.08e-32"),
    ("A_4_checkq_crawl_D215.0344", "PASS", "checkq the crawl's D 215.0344 prediction", "not run there"),
    ("A_5_truthq_d6_D214.5", "PASS", "truthq d6 D 214.5", "error left 5.6e-63 in m_h, 1.1e-64 in a_h"),
    ("A_6_truthq_d6_D214.5_sweeps1", "FAIL", "the same, --sweeps 1 (control)", "error left 1.2e-32"),
]
LINE = re.compile(r"^(checkq|truthq) .*: (PASS|FAIL)\s*$")
NUM_Q = re.compile(r"u0 quad-double \|R\| (\S+?),")
NUM_T = re.compile(r"error left in m_h (\S+), in a_h (\S+) ")


def read(d):
    """[(name, must, got, exit code, number text, mac text)] and a list of problems"""
    ex = {}
    p = os.path.join(d, "exits.txt")
    if os.path.exists(p):
        for ln in open(p, encoding="utf-8"):
            m = re.match(r"(A_\S+) exit (\d+) ", ln)
            if m:
                ex[m.group(1)] = int(m.group(2))
    rows, bad = [], []
    for stem, must, name, mac in RUNS:
        lp = os.path.join(d, stem + ".log")
        if not os.path.exists(lp) or stem not in ex:
            bad.append(f"missing {'log' if not os.path.exists(lp) else 'exit line'} for {stem}")
            continue
        last = [ln.rstrip("\n") for ln in open(lp, encoding="utf-8", errors="replace") if LINE.match(ln)]
        if not last:
            bad.append(f"{stem}: no checkq/truthq verdict line (exit {ex[stem]})")
            continue
        line = last[-1]
        got = LINE.match(line).group(2)
        n = NUM_Q.search(line)
        t = NUM_T.search(line)
        num = (n.group(1) if n else (f"m_h {t.group(1)}, a_h {t.group(2)}" if t else "?"))
        rows.append((name, must, got, ex[stem], num, mac))
    return rows, bad


def run(d, out=print):
    rows, bad = read(d)
    out(f"{'run':44} {'must':5} {'got':5} {'exit':4}  {'win2':38} on the M5 Mac")
    ok = True
    for name, must, got, rc, num, mac in rows:
        fine = got == must and rc == (0 if got == "PASS" else 1)
        ok = ok and fine
        out(f"{name:44} {must:5} {got:5} {rc:<4}  {num:38} {mac}" + ("" if fine else "   <-- NOT AS REQUIRED" + (" (control did not fail)" if must == "FAIL" and got == "PASS" else "")))
    for b in bad:
        out("PROBLEM: " + b)
    if bad:
        return 2
    out("PART A PASSES" if ok else "PART A DOES NOT PASS")
    return 0 if ok else 1


def selftest():
    fails = []

    def write(d, verdicts, codes=None, drop=None):
        ex = []
        for i, (stem, must, _, _) in enumerate(RUNS):
            if stem == drop:
                continue
            v = verdicts[i]
            kind = "checkq" if "checkq" in stem else "truthq"
            body = (f"{kind} x.npz: D 215, a_h, m_h steps and Newton: re-seed ok, u0 quad-double |R| 8.78e-32, 12 s: {v}\n" if kind == "checkq"
                    else f"truthq x.npz: D 214.5, planted 1e-32: re-seed ok, error left in m_h 5.6e-63, in a_h 1.1e-64 (limit 1e-35), 30 s: {v}\n")
            open(os.path.join(d, stem + ".log"), "w", encoding="utf-8").write("noise\n" + body)
            ex.append(f"{stem} exit {(codes or {}).get(stem, 0 if v == 'PASS' else 1)} wall 1s t\n")
        open(os.path.join(d, "exits.txt"), "w", encoding="utf-8").write("".join(ex))

    good = ["PASS", "FAIL", "PASS", "PASS", "PASS", "FAIL"]
    cases = [("required verdicts", good, None, None, 0),
             ("a must-PASS run FAILs", ["FAIL"] + good[1:], None, None, 1),
             ("a control PASSes", good[:1] + ["PASS"] + good[2:], None, None, 1),
             ("exit code disagrees with the verdict", good, {RUNS[0][0]: 1}, None, 1),
             ("a log is missing", good, None, RUNS[3][0], 2)]
    for name, verdicts, codes, drop, want in cases:
        with tempfile.TemporaryDirectory() as td:
            write(td, verdicts, codes, drop)
            rc = run(td, out=lambda s: None)
            if rc != want:
                fails.append(f"{name}: exit {rc}, wanted {want}")
    print("selftest: ok" if not fails else "selftest FAILED:\n  " + "\n  ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    sys.exit(run(args[0] if args else HERE))

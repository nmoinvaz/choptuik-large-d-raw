#!/usr/bin/env python3
"""table1064f.py DIR | --selftest [--break]: the readings of run1064f.sh (#1064, the largest order a polish reaches at D 237.7132) from DIR: per run (ks307 the control, ks331, ks347: <label>.log,
exits_1064f.txt, delta1064_<label>.json) the gate's verdict, exit and wall, the start |F| (the first 'on 0: |F|' value), the lines of the octo-double corrector (the first strong chord and each step with
|F| before -> after, lam and seconds, or converged) and, for a converged rung, Delta(K) - Delta(307).
Reading (the coordinator's, fixed before the run): the largest converging K is the order for a new chain from D 237.7.
--selftest runs planted logs and the #973 log of the stored state's own polish through the same parser, each with its expected cells, and exits 0 when all are as expected; --break flips one expectation and must exit 1."""
import json
import os
import re
import subprocess
import sys

FL = r"[0-9.]+e[+-]\d+"


def od_lines(text):
    out = []
    for ln in text.splitlines():
        s = ln.strip()
        c = re.match(r"on 0: (strong chord .*?): (\w+), ([0-9.]+) s$", s)
        a = re.match(rf"on (\d+): \|F\| ({FL}) -> ({FL}), \|dz\| \S+ -> \S+, lam (\S+),.*?([0-9.]+) s$", s)
        b = re.match(rf"on (\d+): \|F\| ({FL}) converged", s)
        if c:
            out.append(f"first {c.group(1)} ({c.group(2)}, {c.group(3)} s)")
        elif a:
            out.append(f"step {a.group(1)}: {a.group(2)} -> {a.group(3)}, lam {a.group(4)}, {a.group(5)} s")
        elif b:
            out.append(f"step {b.group(1)}: {b.group(2)} converged")
    return out


def start_F(text):
    m = re.search(rf"^\s*on 0: \|F\| ({FL})", text, re.M)
    return m.group(1) if m else None


def selftest(brk):
    base = ("# 2026-11-21 20:00:00 UTC cmd: python3 -u anm_run.py R O --state S --steps 0 --ks 331\n"
            "  on 0: strong chord (4 weak directions), 1 steps after the full first step; theta at its point 1.702e+15 (bound 0.750): refused, 1106.73 s\n"
            "  on 0: |F| 8.38e-35 -> 8.52e-44, |dz| 1.29e-23 -> 6.53e-46, lam 1, dDelta +1.29e-23, piv 3.2e-15..6.3e+42, 1660.99 s\n"
            "  on 1: |F| 8.52e-44 -> 6.82e-49, |dz| 6.53e-46 -> 5.68e-77, lam 0.5, dDelta +6.53e-46, piv 3.2e-15..6.3e+42, 103.73 s\n"
            "  on 2: |F| 6.82e-49 converged, Delta 1.68705448620253429 +2.8557e-17\n")
    capped = "# x cmd: y\n    on 0 chord 0: max|F| 8.6e+29, |dw| 1.5e+30\n  on 0: strong chord (4 weak directions), 1 steps after the full first step; theta at its point inf (bound 0.750): refused, 304.72 s\nexit 143\n"
    real = "../I973-dh610/ks307_r2.log"
    cases = [
        ("start |F| is the first on-0 value", base, lambda t: start_F(t) == "8.38e-35"),
        ("chord line", base, lambda t: od_lines(t)[0] == "first strong chord (4 weak directions), 1 steps after the full first step; theta at its point 1.702e+15 (bound 0.750) (refused, 1106.73 s)"),
        ("step 0 line", base, lambda t: od_lines(t)[1] == "step 0: 8.38e-35 -> 8.52e-44, lam 1, 1660.99 s"),
        ("step 1 line carries its lam", base, lambda t: od_lines(t)[2] == "step 1: 8.52e-44 -> 6.82e-49, lam 0.5, 103.73 s"),
        ("converged line", base, lambda t: od_lines(t)[3] == "step 2: 6.82e-49 converged"),
        ("four od lines in all", base, lambda t: len(od_lines(t)) == 4),
        ("a capped run has the chord line only", capped, lambda t: len(od_lines(t)) == 1 and start_F(t) is None),
        ("a log without on-lines", "# x cmd: y\n", lambda t: od_lines(t) == [] and start_F(t) is None),
    ]
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), real)):
        rt = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), real)).read()
        cases.append(("the #973 ks307_r2 log: start 8.38e-35 and 5 od lines ending converged 5.96e-86", rt,
                      lambda t: start_F(t) == "8.38e-35" and len(od_lines(t)) == 5 and od_lines(t)[-1] == "step 3: 5.96e-86 converged"))
    if brk:
        cases[0] = (cases[0][0], cases[0][1], lambda t: start_F(t) == "8.52e-44")
    bad = 0
    for name, text, chk in cases:
        ok = chk(text)
        print(f"  {name}: {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


def table(d):
    exits = open(f"{d}/exits_1064f.txt").read() if os.path.exists(f"{d}/exits_1064f.txt") else ""
    here = os.path.dirname(os.path.abspath(__file__))
    print("| run | K | exit | wall s | start max\\|F\\| (first `on 0:`) | verdict | od lines (|F| before -> after) | Delta(K) - Delta(307) |")
    print("|---|---|---|---|---|---|---|---|")
    for L in ("ks307", "ks331", "ks347"):
        log = f"{d}/{L}.log"
        if not os.path.exists(log):
            continue
        text = open(log, errors="replace").read()
        g = subprocess.run([sys.executable, f"{here}/gate1064.py", log, f"{d}/{L}"], capture_output=True, text=True).stdout.strip()
        m = re.search(rf"1064 {L} exit (\S+) wall (\d+) s", exits)
        capped = re.search(rf"1064 {L} cap ", exits) is not None
        dj = f"{d}/delta1064_{L}.json"
        dl = f"{json.load(open(dj))['change']:+.6e}" if os.path.exists(dj) else "-"
        print(f"| {L} | {L[2:]} | {(m.group(1) if m else '?') + (' (capped)' if capped else '')} | {m.group(2) if m else '?'} | {start_F(text) or '-'} | {g.replace('|', chr(92) + '|')} | "
              f"{'; '.join(od_lines(text)).replace('|', chr(92) + '|') or 'no od lines'} | {dl} |")
    print()
    print("Wall is each run's own, in 30 s polls. The od lines are the first strong chord and each `on N:` step of the octo-double corrector; Delta(K) - Delta(307) is for a converged rung.")


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    table(sys.argv[1])

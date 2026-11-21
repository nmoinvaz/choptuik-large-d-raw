#!/usr/bin/env python3
"""table1064e.py DIR | --selftest [--break]: the readings of run1064e.sh (#1064, the projection switch) from DIR: per run (ks293, ks315own, ks315nat: <label>.log, exits_1064e.txt,
delta1064_<label>.json) the gate's verdict, exit and wall, the flags of its command line (--elim_switch, --od_accept), the start |F| (the first 'on 0: |F|' value), the first two 'on' lines of the
octo-double corrector verbatim, steps 0 and 1 (|F| before -> after and the ratio after/before) and, for a converged rung, Delta(rung) - Delta(293).
Readings (the coordinator's, fixed before the run): start |F| near 1e-30 at ks 315 (taken here as at most 1e-28) confirms the projection as the source of the 4e-11 start; a converging 315
means the switch was the whole obstacle; a first step that sends |F| up by many orders (taken here as a ratio of at least 1e3) confirms dh170's curvature mechanism.
--selftest runs planted logs through the same parser, each with its expected cells, and exits 0 when all are as expected; --break flips one expectation and must exit 1."""
import glob
import json
import os
import re
import subprocess
import sys

FL = r"[0-9.]+e[+-]\d+"


def parse(text):
    first2 = [ln.strip() for ln in text.splitlines() if re.match(r"^ +on \d", ln)][:2]
    st = re.search(rf"^\s*on 0: \|F\| ({FL})", text, re.M)
    steps = {}
    for m in re.finditer(rf"^\s*on (\d+): \|F\| ({FL}) -> ({FL}), \|dz\| \S+ -> \S+, lam (\S+),", text, re.M):
        steps.setdefault(int(m.group(1)), (float(m.group(2)), float(m.group(3)), m.group(4)))
    ch = re.search(r"^\s*on 0: (strong chord .*?): (\w+), ([0-9.]+) s$", text, re.M)
    cmd = re.search(r"^# .* UTC cmd: (.*)$", text, re.M)
    cmd = cmd.group(1) if cmd else ""
    acc = re.search(r"--od_accept (\w+)", cmd)
    sw = re.search(r"--elim_switch (\S+)", cmd)
    return dict(first2=first2, start=st.group(1) if st else None, steps=steps, chord=f"{ch.group(2)} ({ch.group(3)} s)" if ch else None,
                accept=acc.group(1) if acc else "?", switch=sw.group(1) if sw else "default", reseed_base="--reseed_base" in cmd)


def ratio(steps, n):
    if n not in steps:
        return None
    a, b, _ = steps[n]
    return b / a


def selftest(brk):
    base = ("# 2026-11-21 15:00:00 UTC cmd: python3 -u anm_run.py R O --state S --od_accept own --elim_switch 1e-9 --steps 0 --ks 315\n"
            "    on 0 chord 0: max|F| 1.28e+13, |dw| 2.850e+11\n"
            "  on 0: strong chord (4 weak directions), 1 steps after the full first step; theta at its point inf (bound 0.750): refused, 271.63 s\n"
            "  on 0: |F| 1.67e-30 -> 4.50e-20, |dz| 4.23e-18 -> 7.88e-19, lam 1, dDelta +4.23e-18, piv 4.8e-16..3.0e+50, 3067.32 s\n"
            "  on 1: |F| 4.50e-20 -> 2.00e-21, |dz| 7.88e-19 -> 3.40e-20, lam 0.5, dDelta -7.88e-19, piv 1.0e-12..3.0e+50, 1147.34 s\n")
    nat = base.replace("--od_accept own", "--od_accept natural")
    noswitch = base.replace(" --elim_switch 1e-9", "")
    rb = base.replace("--steps 0", "--reseed_base 1 --steps 0")
    up = base.replace("1.67e-30 -> 4.50e-20", "1.67e-30 -> 1.67e-20")
    cases = [  # name, text, check(parse) -> bool
        ("start |F| is the first on-0 value", base, lambda p: p["start"] == "1.67e-30"),
        ("two on-lines are the first two, verbatim", base, lambda p: len(p["first2"]) == 2 and p["first2"][0].startswith("on 0 chord 0:") and p["first2"][1].startswith("on 0: strong chord")),
        ("step 0 ratio after/before", base, lambda p: abs(ratio(p["steps"], 0) - 4.50e-20 / 1.67e-30) / 2.7e10 < 1e-6),
        ("step 1 present", base, lambda p: 1 in p["steps"] and abs(ratio(p["steps"], 1) - 2.00e-21 / 4.50e-20) < 1e-9),
        ("a changed step 0 changes the ratio", up, lambda p: abs(ratio(p["steps"], 0) - 1e10) / 1e10 < 1e-6),
        ("accept own", base, lambda p: p["accept"] == "own"),
        ("accept natural", nat, lambda p: p["accept"] == "natural"),
        ("elim_switch read", base, lambda p: p["switch"] == "1e-9"),
        ("elim_switch absent is the default", noswitch, lambda p: p["switch"] == "default"),
        ("reseed_base absent", base, lambda p: not p["reseed_base"]),
        ("reseed_base present is seen", rb, lambda p: p["reseed_base"]),
        ("no on-lines at all", "# 2026-11-21 15:00:00 UTC cmd: x\n", lambda p: p["start"] is None and p["first2"] == [] and p["steps"] == {}),
    ]
    if brk:
        cases[0] = (cases[0][0], cases[0][1], lambda p: p["start"] == "4.50e-20")
    bad = 0
    for name, text, chk in cases:
        ok = chk(parse(text))
        print(f"  {name}: {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAIL" if bad else "PASS")
    return 1 if bad else 0


def table(d):
    exits = open(f"{d}/exits_1064e.txt").read() if os.path.exists(f"{d}/exits_1064e.txt") else ""
    here = os.path.dirname(os.path.abspath(__file__))
    print("| run | --od_accept | --elim_switch | exit | wall s | start max\\|F\\| (first `on 0:`) | first two `on` lines | step 0 after/before | step 1 after/before | verdict | Delta - Delta(293) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for L in ("ks293", "ks315own", "ks315nat"):
        log = f"{d}/{L}.log"
        if not os.path.exists(log):
            continue
        text = open(log, errors="replace").read()
        p = parse(text)
        g = subprocess.run([sys.executable, f"{here}/gate1064.py", log, f"{d}/{L}"], capture_output=True, text=True).stdout.strip()
        m = re.search(rf"1064 {L} exit (\S+) wall (\d+) s", exits)
        capped = re.search(rf"1064 {L} cap ", exits) is not None
        dj = f"{d}/delta1064_{L}.json"
        dl = "-"
        if os.path.exists(dj):
            dl = f"{json.load(open(dj))['change']:+.6e}"
        r0, r1 = ratio(p["steps"], 0), ratio(p["steps"], 1)
        f2 = "<br>".join(x.replace("|", "\\|")[:230] for x in p["first2"]) or "none"
        print(f"| {L} | {p['accept']} | {p['switch']} | {(m.group(1) if m else '?') + (' (capped)' if capped else '')} | {m.group(2) if m else '?'} | {p['start'] or '-'} | {f2} | "
              f"{f'{r0:.3g}' if r0 is not None else '-'} | {f'{r1:.3g}' if r1 is not None else '-'} | {g.replace('|', chr(92) + '|')} | {dl} |")
    print()
    print("Wall is each run's own, in 30 s polls. The start |F| is the first `on 0: |F|` value of the log; step 0 and 1 are the first two `on N: |F| a -> b` lines (the accepted step's |F|, lam in the log).")


if __name__ == "__main__":
    if sys.argv[1] == "--selftest":
        sys.exit(selftest("--break" in sys.argv))
    table(sys.argv[1])

#!/usr/bin/env python3
"""#1039 (win): this folder's logs of notes/P6_route3.md 10.6's eight commands against the issue's pass criteria and I1030-rpi5's logs of the same commands.
From I1030-rpi5/compare1030.py.
    python -I -X utf8 compare1039.py RPI5_RAW              # RPI5_RAW = a checkout of choptuik-large-d-raw holding I1030-rpi5 (raw cc9c41c5)
    python -I -X utf8 compare1039.py RPI5_RAW --mutate     # the controls: four altered copies of this folder's logs, each must be reported (exit 1 when all are, 2 otherwise)
    python -I -X utf8 compare1039.py RPI5_RAW --selftest   # no run of this folder needed: I1030's logs against themselves (0 differ), the controls on them, and planted numeric and timing cases
1. every run's last line is `exit N` with the expected N (0 for a verdict run, whose line before it is PASS; 1 for a control, FAIL);
2. `route3_bound.py --constants` prints C_m, C_0, C_p = 28.45, 56.87, 4.77e6, and with --J0=100 1.60, 3.17, 3.63e5 (rounded to the quoted digits);
3. every printed line of each of the eight logs equals the line of I1030-rpi5's log of the same command (line endings stripped, `[N s]` timings masked). A differing
   line is reported with its size: when it has the same text around the same number of numbers, the largest relative difference of those numbers, else 'text differs'.
   The conclusion line (the verdict and the exit code) is compared separately and reported whether it is the same.
4. extra, not a criterion: the J0 = 10 sups, P, W and Cr appear in the constants log at 10.2's digits."""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXPECT = {"route3_bound_lemmas": 0, "route3_bound_constants": 0, "route3_bound_constants_J0100": 0, "route3_bound_check": 0,
          "route3_bound_check_plant": 1, "route3_bound_check_psi": 1, "route3_tuned_7_800": 0, "route3_tuned_7_800_demix": 1}
MASK = [re.compile(p) for p in (r"\[\d+(\.\d+)? s\]", r"\(\d+ s\)", r"\d+ s\)")]
NUM = re.compile(r"[-+]?(?:\d+\.\d*|\.\d+|\d+)(?:[eE][-+]?\d+)?")
OWN = os.path.join(HERE, "logs")                 # this folder's logs; --selftest points it at the reference's own


def mask(t):
    for m in MASK:
        t = m.sub("<t>", t)
    return t


def lines_of(text):
    return mask(text.replace("\r", "")).splitlines()


def size(x, y):
    """what a differing pair of lines differs by: ('numeric', largest relative difference of its numbers) or ('text', None)"""
    if NUM.sub("#", x) != NUM.sub("#", y):
        return "text", None
    a, b = NUM.findall(x), NUM.findall(y)
    if len(a) != len(b):
        return "text", None
    rel = 0.0
    for u, v in zip(a, b):
        fu, fv = float(u), float(v)
        if fu != fv:
            rel = max(rel, abs(fu - fv) / max(abs(fu), abs(fv)))
    return "numeric", rel


def read(name, mut, base=None):
    p = os.path.join(base or OWN, f"{name}.log")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    if mut == "digit" and name == "route3_bound_check":      # one printed digit moved
        t = t.replace("worst ratio by perturbation: m 1.335e-05", "worst ratio by perturbation: m 1.336e-05", 1)
    if mut == "tuned" and name == "route3_tuned_7_800":
        t = t.replace("| 3 | 3 | yes | 2.543e-6", "| 3 | 3 | yes | 2.544e-6", 1)
    if mut == "const" and name == "route3_bound_constants":
        t = t.replace("C_0 = 56.8735", "C_0 = 57.8735", 1)
    if mut == "exit" and name == "route3_bound_check_plant":
        t = re.sub(r"exit 1\s*$", "exit 0\n", t)
    return t


def checks(ref, mut=""):
    """the list of (label, ok, detail) of every check, ref = the directory of I1030-rpi5's logs"""
    out = []
    for name, want in EXPECT.items():                                         # 1. exits and verdicts
        t = read(name, mut)
        if t is None:
            out.append((f"{name}: exit {want}", None, "log missing"))
            continue
        ls = [l for l in lines_of(t) if l.strip()]
        m = re.fullmatch(r"exit (\d+)", ls[-1]) if ls else None
        got = int(m.group(1)) if m else None
        verdict = ls[-2].strip() if len(ls) > 1 else ""
        want_v = "PASS" if want == 0 else "FAIL"
        out.append((f"{name}: exit {want}, verdict {want_v}", got == want and verdict == want_v, f"exit {got}, last line before it {verdict[:60]!r}"))
    for name, tag, want in (("route3_bound_constants", "J0 10", ("28.45", "56.87", "4.77e+6")),
                            ("route3_bound_constants_J0100", "J0 100", ("1.60", "3.17", "3.63e+5"))):          # 2. the constants
        t = read(name, mut)
        if t is None:
            out.append((f"{name}: C_m, C_0, C_p", None, "log missing"))
            continue
        got = []
        for k in ("m", "0", "p"):
            mm = re.search(rf"^C_{k} = (\S+):", t.replace("\r", ""), re.M)
            got.append(float(mm.group(1)) if mm else float("nan"))
        e = int(f"{got[2]:e}".split("e")[1]) if got[2] == got[2] else 0
        fmt = [f"{got[0]:.2f}", f"{got[1]:.2f}", f"{got[2] / 10 ** e:.2f}e+{e}"]
        out.append((f"{name}: C_(nu-2), C_nu, C_(nu+2) = {', '.join(want)} ({tag})", fmt == list(want), f"printed {got}, rounded {fmt}"))
    t = read("route3_bound_constants", mut)                                    # 4. extra
    if t is not None:
        extra = ["0.56382", "0.92291", "1.1028", "1.0454", "0.95300", "1.1775", "2.6323", "0.47186", "0.90033", "0.99435", "1.0071",
                 "0.91830", "1.0320", "2.5528", "1.63995e+5", "0.0004728", "27.885", "55.770", "28.4491", "56.8735", "4.76610e+6"]
        miss = [x for x in extra if x not in t]
        out.append(("extra: 10.2's sups, P, W, Cr and the three constants appear in the constants log", not miss, f"missing {miss}"))
    for name in EXPECT:                                                         # 3. against rpi5, line by line
        t, p = read(name, mut), os.path.join(ref, f"{name}.log")
        if t is None or not os.path.exists(p):
            out.append((f"{name} = I1030-rpi5", None, "log missing on one side"))
            continue
        a, b = lines_of(t), lines_of(open(p, encoding="utf-8").read())
        diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        n = len(diffs) + abs(len(a) - len(b))
        d = f"{len(a)} lines vs {len(b)}; {n} differ"
        for i, x, y in diffs[:6]:
            kind, rel = size(x, y)
            d += f"\n      line {i + 1}: {'largest relative difference of its numbers ' + format(rel, '.3g') if kind == 'numeric' else 'text differs'}\n        win:  {x[:200]}\n        rpi5: {y[:200]}"
        concl = (a[-2:] == b[-2:])
        out.append((f"{name} = I1030-rpi5 line by line (conclusion lines {'the same' if concl else 'DIFFERENT'})", n == 0, d))
    return out


def show(res):
    bad = 0
    for label, ok, detail in res:
        print(("ok     " if ok else "MISSING" if ok is None else "DIFFER ") + " " + label + ("" if ok else f"  [{detail}]"))
        bad += ok is False
    return bad


def selftest(ref):
    bad = 0
    # 1. the reference against itself: nothing differs
    res = checks(ref)
    n = sum(ok is not True for _, ok, _ in res)
    print(f"  I1030's own logs against themselves: {len(res)} checks, {n} not ok {'ok' if n == 0 else 'WRONG'}")
    bad += n != 0
    # 2. the controls are reported
    base = {l: ok for l, ok, _ in res}
    for mut in ("digit", "tuned", "const", "exit"):
        flipped = [l for l, ok, _ in checks(ref, mut) if ok is False and base.get(l) is not False]
        ok = bool(flipped)
        print(f"  control {mut}: {len(flipped)} check(s) reported {'ok' if ok else 'WRONG'}")
        bad += not ok
    # 3. size reporting and timing masks
    cases = [("a last digit of 1.335e-05", "worst m 1.335e-05", "worst m 1.336e-05", "numeric", 7.0e-4, 8.0e-4),    # 1e-8 / 1.336e-5 = 7.49e-4
             ("a changed word", "worst m 1.0 PASS", "worst m 1.0 FAIL", "text", None, None),
             ("a different number of numbers", "x 1 2", "x 1", "text", None, None),
             ("a timing only", "amp_flint to order 7 [554 s]", "amp_flint to order 7 [610 s]", "equal", None, None)]
    for nm, x, y, kind, lo, hi in cases:
        mx, my = mask(x), mask(y)
        if mx == my:
            got, rel = "equal", None
        else:
            got, rel = size(mx, my)
        ok = got == kind and (lo is None or lo < rel < hi)
        print(f"  size: {nm}: {got}{'' if rel is None else f', {rel:.3g}'} (want {kind}) {'ok' if ok else 'WRONG'}")
        bad += not ok
    print("selftest", "FAILED" if bad else "passed")
    return bad


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit("usage: compare1039.py RPI5_RAW [--mutate | --selftest]")
    ref = os.path.join(args[0], "I1030-rpi5", "logs")
    if "--selftest" in sys.argv:
        global OWN
        OWN = ref
        sys.exit(selftest(ref))
    if "--mutate" not in sys.argv:
        print("== checks")
        res = checks(ref)
        bad = show(res)
        missing = sum(ok is None for _, ok, _ in res)
        print(f"TOTAL differing: {bad}; missing: {missing}")
        sys.exit(1 if bad or missing else 0)
    print("== controls: each altered copy must be reported")
    base = {l: ok for l, ok, _ in checks(ref)}
    caught = 0
    for mut in ("digit", "tuned", "const", "exit"):
        flipped = [l for l, ok, _ in checks(ref, mut) if ok is False and base.get(l) is not False]
        print(f"control {mut}: {len(flipped)} check(s) now reported: {flipped}")
        caught += bool(flipped)
    print(f"controls reported: {caught} of 4 (a control that is not reported would be a defect of this script)")
    sys.exit(1 if caught == 4 else 2)


if __name__ == "__main__":
    main()

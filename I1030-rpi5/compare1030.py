"""#1030: this folder's logs against the issue's pass criteria and I1015-mac's logs.
    python3 compare1030.py MAC_RAW_DIR [--mutate]      # MAC_RAW_DIR = a checkout of choptuik-large-d-raw holding I1015-mac
1. every run's last line is `exit N` with the expected N (0 for a verdict run, which also prints PASS; 1 for a control, which prints FAIL);
2. `route3_bound.py --constants` prints C_m, C_0, C_p = 28.45, 56.87, 4.77e6, and with --J0=100 1.60, 3.17, 3.63e5 (rounded to the quoted digits);
3. route3_head.py's six logs equal I1015-mac's line by line (timings masked; the logs print none);
4. extra, not a criterion: the J0 = 10 sups, P, W and Cr equal notes/P6_route3.md 10.2's table at its digits.
--mutate runs the same checks on three altered copies of this folder's text (one printed digit of route3_head_check.log, the 56.87 of the
constants log, the exit line of route3_bound_check_plant.log): each must be reported as a difference, and the script then exits 1."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); MAC = sys.argv[1]; MUT = "--mutate" in sys.argv
EXPECT = {"route3_bound_lemmas": 0, "route3_bound_constants": 0, "route3_bound_constants_J0100": 0, "route3_bound_check": 0,
          "route3_bound_check_plant": 1, "route3_bound_check_psi": 1, "route3_tuned_7_800": 0, "route3_tuned_7_800_demix": 1,
          "route3_head_scope": 0, "route3_head_lemmas": 0, "route3_head_check": 0, "route3_head_check_plant": 1,
          "route3_head_check_gsmall": 1, "route3_head_certify": 0}
HEAD = [k for k in EXPECT if k.startswith("route3_head")]
MASK = [re.compile(p) for p in (r"\[\d+(\.\d+)? s\]", r"\(\d+ s\)", r"\d+ s\)")]


def mask(t):
    for m in MASK:
        t = m.sub("<t>", t)
    return t


def read(name, mut):
    p = f"{HERE}/logs/{name}.log"
    if not os.path.exists(p):
        return None
    t = open(p).read()
    if mut == "digit" and name == "route3_head_check":     # one printed digit moved
        t = re.sub(r"(worst exact/bound m 2\.352e-0)2", r"\g<1>3", t, count=1)
    if mut == "const" and name == "route3_bound_constants":
        t = t.replace("C_0 = 56.8735", "C_0 = 57.8735", 1)
    if mut == "exit" and name == "route3_bound_check_plant":
        t = re.sub(r"exit 1\s*$", "exit 0\n", t)
    return t


def checks(mut=""):
    """the list of (label, ok, detail) of every check"""
    out = []
    for name, want in EXPECT.items():                                     # 1. exits and verdicts
        t = read(name, mut)
        if t is None:
            out.append((f"{name}: exit {want}", None, "log missing")); continue
        lines = [l for l in t.splitlines() if l.strip()]
        m = re.fullmatch(r"exit (\d+)", lines[-1]) if lines else None
        got = int(m.group(1)) if m else None
        verdict = lines[-2] if len(lines) > 1 else ""
        want_v = "PASS" if want == 0 else "FAIL"
        out.append((f"{name}: exit {want}, verdict {want_v}", got == want and verdict.strip() == want_v,
                    f"exit {got}, last line before it {verdict.strip()[:60]!r}"))
    for name, tag, want in (("route3_bound_constants", "J0 10", ("28.45", "56.87", "4.77e+6")),
                            ("route3_bound_constants_J0100", "J0 100", ("1.60", "3.17", "3.63e+5"))):      # 2. the constants
        t = read(name, mut)
        if t is None:
            out.append((f"{name}: C_m, C_0, C_p", None, "log missing")); continue
        got = []
        for k in ("m", "0", "p"):
            mm = re.search(rf"^C_{k} = (\S+):", t, re.M)
            got.append(float(mm.group(1)) if mm else float("nan"))
        e = int(f"{got[2]:e}".split("e")[1]) if got[2] == got[2] else 0
        fmt = [f"{got[0]:.2f}", f"{got[1]:.2f}", f"{got[2] / 10 ** e:.2f}e+{e}"]         # 2 decimals; the last as a.bce+k
        want_f = list(want)
        out.append((f"{name}: C_(nu-2), C_nu, C_(nu+2) = {', '.join(want)} ({tag})", fmt == want_f, f"printed {got}, rounded {fmt}"))
    t = read("route3_bound_constants", mut)                                 # 4. extra: 10.2's table at its digits
    if t is not None:
        extra = ["0.56382", "0.92291", "1.1028", "1.0454", "0.95300", "1.1775", "2.6323", "0.47186", "0.90033", "0.99435", "1.0071",
                 "0.91830", "1.0320", "2.5528", "1.63995e+5", "0.0004728", "27.885", "55.770", "28.4491", "56.8735", "4.76610e+6"]
        miss = [x for x in extra if x not in t]
        out.append(("extra: 10.2's sups, P, W, Cr and the three constants appear in the constants log", not miss, f"missing {miss}"))
    for name in HEAD:                                                        # 3. the head against the Mac
        t, p = read(name, mut), f"{MAC}/I1015-mac/{name}.log"
        if t is None or not os.path.exists(p):
            out.append((f"{name} = I1015-mac", None, "log missing on one side")); continue
        a, b = mask(t).splitlines(), mask(open(p).read()).splitlines()
        diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
        n = len(diffs) + abs(len(a) - len(b))
        d = f"{len(a)} lines vs {len(b)}; {n} differ"
        for i, x, y in diffs[:4]:
            d += f"\n      line {i + 1}\n        rpi5: {x[:200]}\n        Mac:  {y[:200]}"
        out.append((f"{name} = I1015-mac line by line", n == 0, d))
    return out


def show(res):
    bad = 0
    for label, ok, detail in res:
        print(("ok     " if ok else "MISSING" if ok is None else "DIFFER ") + " " + label + ("" if ok else f"  [{detail}]"))
        bad += ok is False
    return bad


if not MUT:
    print("== checks")
    bad = show(checks())
    missing = sum(ok is None for _, ok, _ in checks())
    print(f"TOTAL differing: {bad}; missing: {missing}")
    sys.exit(1 if bad or missing else 0)
else:
    print("== controls: each altered copy must be reported")
    base = {l: ok for l, ok, _ in checks()}
    caught = 0
    for mut in ("digit", "const", "exit"):
        res = checks(mut)
        flipped = [l for l, ok, _ in res if ok is False and base.get(l) is not False]
        print(f"control {mut}: {len(flipped)} check(s) now reported: {flipped}")
        caught += bool(flipped)
    print(f"controls reported: {caught} of 3 (a control that is not reported would be a defect of this script)")
    sys.exit(1 if caught == 3 else 2)

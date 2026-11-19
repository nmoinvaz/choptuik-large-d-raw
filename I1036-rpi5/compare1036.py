"""#1036: this folder's logs against the issue's pass criteria and I1010-mac's logs (adapted from I1030-rpi5/compare1030.py).
    python3 compare1036.py MAC_RAW_DIR [--wt=WORKTREE] [--mutate]
        MAC_RAW_DIR = a checkout of choptuik-large-d-raw holding I1010-mac;  WORKTREE = the code worktree whose data/ the runs wrote
1. every run's last line is `exit N` with the expected N (notes/L2_MODE.md section 10), and the verdict line before it where §10 gives one;
2. every log that has a Mac log equals it line by line with timings ("[12 s]") masked and the directory of a "wrote ..." line masked
   (the file name is not masked). Mac's l2_c2_checks.log holds four runs in sections "=== --checks MUTATION" (no exit lines, a stray
   last line "exit"): each section is compared with this folder's log of the same command, without its exit line; its plain section was
   made before the radius diagnostic existed, so it is compared with l2_c2_checks_main.log minus its two "diagnostic" lines;
3. with --wt: each result JSON the runs wrote to WORKTREE/solver/inner_pert/data (tracked there from the Mac's) against HEAD's, leaf by
   leaf: equal, or the largest relative difference of the numbers (extra, not a criterion);
4. c2's sign and c2 + lambda_1 at M = 1, 3, 5, read from l2_c2_M{1,3,5}.log (printed, not a pass/fail check).
--mutate runs the same checks on three altered copies of this folder's text (a digit of c2 in l2_c2_M1.log, a digit of the M = 3 control line in
l2_c2_summary.log, the exit line of l2_c2_checks_main.log): each must be reported (an exit or verdict check that was ok turns to DIFFER,
or a log's count of differing lines rises: most logs differ from the Mac's already, so a flip alone would not show), and the script
then exits 1."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); MAC = sys.argv[1]
WT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--wt=")), None)
MUT = "--mutate" in sys.argv
# (name, expected exit, verdict line before `exit N` or None)
EXPECT = [("l2_mode_flat", 0, "PASS"), ("l2_mode_check", 0, "PASS"), ("l2_mode_check_curv", 1, "FAIL"),
          ("l2_mode_first_order", 0, "PASS"), ("l2_mode_first_order_print", 0, "PASS"),
          ("l2_c2_forcing", 0, "PASS"), ("l2_c2_forcing_p1", 0, "PASS"), ("l2_c2_checks_main", 1, "FAIL"),
          ("l2_c2_checks_ident", 1, "FAIL"), ("l2_c2_checks_series", 1, "FAIL"), ("l2_c2_checks_force", 1, "FAIL"),
          ("l2_c2_M1_planted", 0, "PASS")] + [(f"l2_c2_M{M}{g}", 0, "PASS") for g in ("", "_G") for M in (1, 3, 5)] + [
         ("l2_c2_M5_mutate_gsign", 1, None), ("l2_c2_summary", 0, "PASS")]
DIRECT = ["l2_c2_forcing", "l2_c2_forcing_p1", "l2_c2_checks_main", "l2_c2_M1_planted", "l2_c2_M1", "l2_c2_M3", "l2_c2_M5",
          "l2_c2_M1_G", "l2_c2_M3_G", "l2_c2_M5_G", "l2_c2_M5_mutate_gsign", "l2_c2_summary"]
SECTIONS = {"l2_c2_checks_ident": "--checks --mutate=ident", "l2_c2_checks_series": "--checks --mutate=series",
            "l2_c2_checks_force": "--checks --mutate=force", "l2_c2_checks_main": "--checks "}   # last: the plain section
MASK = [(re.compile(p), r) for p, r in (
    (r"\[\d+(\.\d+)? s\]", "<t>"), (r"\(\d+ s\)", "<t>"), (r"wrote \S*/(\S+\.json)", r"wrote <dir>/\1"))]


def mask(t):
    for rx, r in MASK:
        t = rx.sub(r, t)
    return t


def read(name, mut):
    p = f"{HERE}/logs/{name}.log"
    if not os.path.exists(p):
        return None
    t = open(p).read()
    if mut == "digit" and name == "l2_c2_M1":       # a line equal to the Mac's at base: its differing-line count must rise by one
        t = t.replace("l2: c2 = -7.959089", "l2: c2 = -7.959088", 1)
    if mut == "table" and name == "l2_c2_summary":
        t = t.replace("|c2_ctrl - c2| = 5.647", "|c2_ctrl - c2| = 5.648", 1)
    if mut == "exit" and name == "l2_c2_checks_main":
        t = re.sub(r"exit 1\s*$", "exit 0\n", t)
    return t


def mac_log(name):
    p = f"{MAC}/I1010-mac/{name}.log"
    return open(p).read() if os.path.exists(p) else None


def mac_section(header):
    t = mac_log("l2_c2_checks")
    if t is None:
        return None
    parts = re.split(r"^=== (.*)$", t, flags=re.M)               # [pre, header1, body1, header2, body2, ...]
    for h, b in zip(parts[1::2], parts[2::2]):
        if h == header:
            return b.strip("\n")
    return None


def lines_diff(a, b):
    diffs = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
    return diffs, len(diffs) + abs(len(a) - len(b))


def checks(mut=""):
    out = []
    for name, want, want_v in EXPECT:                                     # 1. exits and verdicts
        t = read(name, mut)
        if t is None:
            out.append((f"{name}: exit {want}", None, "log missing")); continue
        lines = [l for l in t.splitlines() if l.strip()]
        m = re.fullmatch(r"exit (\d+)", lines[-1]) if lines else None
        got = int(m.group(1)) if m else None
        verdict = lines[-2].strip() if len(lines) > 1 else ""
        ok = got == want and (want_v is None or verdict == want_v)
        out.append((f"{name}: exit {want}" + (f", verdict {want_v}" if want_v else ""), ok, f"exit {got}, line before it {verdict[:60]!r}"))
    for name in DIRECT:                                                  # 2. against the Mac
        t, m = read(name, mut), mac_log(name)
        if name == "l2_c2_checks_main" and t is not None and m is not None:
            pass
        if t is None or m is None:
            out.append((f"{name} = I1010-mac line by line", None, "log missing on one side")); continue
        a, b = mask(t).splitlines(), mask(m).splitlines()
        diffs, n = lines_diff(a, b)
        d = f"{len(a)} lines vs {len(b)}; {n} differ"
        for i, x, y in diffs[:4]:
            d += f"\n      line {i + 1}\n        rpi5: {x[:230]}\n        Mac:  {y[:230]}"
        out.append((f"{name} = I1010-mac line by line", n == 0, d))
    for name, header in SECTIONS.items():                                # Mac's concatenated checks log
        t, sec = read(name, mut), mac_section(header)
        if t is None or sec is None:
            out.append((f"{name} = section '=== {header}' of l2_c2_checks.log", None, "missing on one side")); continue
        a = [l for l in mask(t).splitlines() if not re.fullmatch(r"exit \d+", l)]
        if header == "--checks ":
            a = [l for l in a if not l.startswith("diagnostic")]
        b = mask(sec).splitlines()
        diffs, n = lines_diff(a, b)
        d = f"{len(a)} lines vs {len(b)}; {n} differ"
        for i, x, y in diffs[:4]:
            d += f"\n      line {i + 1}\n        rpi5: {x[:230]}\n        Mac:  {y[:230]}"
        out.append((f"{name} = section '=== {header.strip()}' of l2_c2_checks.log", n == 0, d))
    return out


def leaves(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from leaves(v, f"{path}/{k}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from leaves(v, f"{path}[{i}]")
    else:
        yield path, o


def json_check():
    """3. the result JSONs of the worktree against HEAD's (the Mac's, tracked)"""
    data = os.path.join(WT, "solver/inner_pert/data")
    names = sorted(f for f in os.listdir(data) if f.startswith("l2_c2_") and f.endswith(".json"))
    res = []
    for f in names:
        cur = json.load(open(os.path.join(data, f)))
        try:
            old = json.loads(subprocess.run(["git", "-C", WT, "show", f"HEAD:solver/inner_pert/data/{f}"], capture_output=True,
                                            text=True, check=True).stdout)
        except subprocess.CalledProcessError:
            res.append((f, "not tracked at HEAD")); continue
        lc, lo = dict(leaves(cur)), dict(leaves(old))
        worst, nd, ns = 0.0, 0, 0
        for p in sorted(set(lc) | set(lo)):
            u, v = lc.get(p), lo.get(p)
            if u == v:
                continue
            if isinstance(u, (int, float)) and isinstance(v, (int, float)) and not isinstance(u, bool):
                r = abs(u - v) / abs(v) if v else abs(u - v)
                worst = max(worst, r); nd += 1
            else:
                ns += 1
        res.append((f, "identical" if not (nd or ns) else f"{nd} numeric leaves differ (largest relative {worst:.2e}), {ns} other"))
    return res


def c2_lines():
    """4. c2, lambda_1 (l0, sym) and c2 + lambda_1 per M from the logs"""
    out = []
    for M in (1, 3, 5):
        t = read(f"l2_c2_M{M}", "")
        if t is None:
            continue
        g = lambda k: float(re.search(rf"^   {k}: (?:c2|lambda_1) = (\S+)", t, re.M).group(1))
        c2, l0, sy = g("l2"), g("l0"), g("sym")
        out.append(f"M {M}: c2 {c2:+.4f} ({'negative' if c2 < 0 else 'POSITIVE'}), lambda_1 {l0:.4f} (l0) / {sy:.4f} (SymForce), "
                   f"c2 + lambda_1 {c2 + l0:+.4f} ({abs(c2 + l0) / l0 * 100:.2f}% of lambda_1)")
    return out


def show(res):
    bad = 0
    for label, ok, detail in res:
        print(("ok     " if ok else "MISSING" if ok is None else "DIFFER ") + " " + label + ("" if ok else f"  [{detail}]"))
        bad += ok is False
    return bad


if not MUT:
    print("== checks (exits, verdicts, the Mac's logs)")
    res = checks()
    bad = show(res)
    missing = sum(ok is None for _, ok, _ in res)
    if WT:
        print("== result JSONs against HEAD's (extra)")
        for f, s in json_check():
            print(f"   {f}: {s}")
    print("== c2 and lambda_1")
    for l in c2_lines():
        print("   " + l)
    print(f"TOTAL differing: {bad}; missing: {missing}")
    sys.exit(1 if bad or missing else 0)
else:
    print("== controls: each altered copy must be reported")
    ndiff = lambda d: int(m.group(1)) if (m := re.search(r"; (\d+) differ", d)) else 0
    base = {l: ok for l, ok, _ in checks()}
    base_n = {l: ndiff(d) for l, _, d in checks()}
    caught = 0
    for mut in ("digit", "table", "exit"):
        flipped = [l for l, ok, d in checks(mut) if (ok is False and base.get(l) is True) or (ndiff(d) > base_n.get(l, 0))]
        print(f"control {mut}: {len(flipped)} check(s) now reported: {flipped}")
        caught += bool(flipped)
    print(f"controls reported: {caught} of 3 (a control that is not reported would be a defect of this script)")
    sys.exit(1 if caught == 3 else 2)

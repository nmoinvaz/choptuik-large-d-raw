"""#1036: the SIZE of every difference between this folder's logs and I1010-mac's (extra to compare1036.py, which reports
whether a line is equal). Per log pair, timings masked: lines equal; lines whose text is equal but whose printed numbers differ (the
largest relative difference |a-b|/max(|a|,|b|) and where); lines whose text differs (the code's printing changed). Also the result
JSONs of the code worktree against HEAD's, leaf by leaf (largest relative difference of numbers; the five largest leaves).
    python3 numdiff1036.py MAC_RAW_DIR [--wt=WORKTREE] [--mutate]
--mutate: c2 of l2_c2_M1.log (equal to the Mac's at base) is changed by 12% (-7.959089 -> -8.959089); the log's largest relative
difference must then be >= 1e-1 (base 3e-2) and its count of lines with other numbers must rise by one."""
import difflib, json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); MAC = sys.argv[1]
WT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--wt=")), None)
MUT = "--mutate" in sys.argv
NAMES = ["l2_c2_forcing", "l2_c2_forcing_p1", "l2_c2_checks_main", "l2_c2_M1_planted", "l2_c2_M1", "l2_c2_M3", "l2_c2_M5",
         "l2_c2_M1_G", "l2_c2_M3_G", "l2_c2_M5_G", "l2_c2_M5_mutate_gsign", "l2_c2_summary"]
SECTIONS = {"l2_c2_checks_ident": "--checks --mutate=ident", "l2_c2_checks_series": "--checks --mutate=series",
            "l2_c2_checks_force": "--checks --mutate=force", "l2_c2_checks_main (section)": "--checks "}
TIME = [re.compile(p) for p in (r"\[\d+(\.\d+)? s\]", r"\(\d+ s\)")]
WROTE = re.compile(r"wrote \S*/(\S+\.json)")
NUM = re.compile(r"(?<![\w.])[-+]?\d+(?:\.\d+)?(?:[eE][-+]?\d+)?(?![\w])")


def prep(t):
    t = "\n".join(l for l in t.splitlines() if not re.fullmatch(r"exit \d+", l))
    for m in TIME:
        t = m.sub("<t>", t)
    return WROTE.sub(r"wrote <dir>/\1", t).splitlines()


def split(l):
    nums = [float(x) for x in NUM.findall(l)]
    return NUM.sub("#", l), nums


def rel(a, b):
    return 0.0 if a == b else abs(a - b) / max(abs(a), abs(b))


def mac_section(header):
    p = f"{MAC}/I1010-mac/l2_c2_checks.log"
    parts = re.split(r"^=== (.*)$", open(p).read(), flags=re.M)
    for h, b in zip(parts[1::2], parts[2::2]):
        if h == header:
            return b.strip("\n")


def compare(a, b):
    """-> (equal lines, [(rel, line_no, label)] numeric, [(rpi5 line, Mac line)] text differs)"""
    sa, sb = [split(l) for l in a], [split(l) for l in b]
    sm = difflib.SequenceMatcher(None, [s for s, _ in sa], [s for s, _ in sb], autojunk=False)
    eq, num, txt = 0, [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            for k in range(i2 - i1):
                (s, na), (_, nb) = sa[i1 + k], sb[j1 + k]
                if na == nb:
                    eq += 1
                else:
                    r, at = max((rel(x, y), q) for q, (x, y) in enumerate(zip(na, nb)))
                    num.append((r, i1 + k + 1, f"number {at + 1}: {na[at]:g} vs {nb[at]:g}; {a[i1 + k].strip()[:70]}"))
        else:
            for k in range(max(i2 - i1, j2 - j1)):
                txt.append((a[i1 + k] if i1 + k < i2 else "(none)", b[j1 + k] if j1 + k < j2 else "(none)"))
    return eq, num, txt


def logs(mut=""):
    out = []
    for n in NAMES + list(SECTIONS):
        if n in SECTIONS:
            base, hdr = n.split(" ")[0], SECTIONS[n]
            p = f"{HERE}/logs/{base}.log"
            m = mac_section(hdr)
        else:
            p = f"{HERE}/logs/{n}.log"
            q = f"{MAC}/I1010-mac/{n}.log"
            m = open(q).read() if os.path.exists(q) else None
        if not os.path.exists(p) or m is None:
            out.append((n, None)); continue
        t = open(p).read()
        if mut and n == "l2_c2_M1":
            t = t.replace("l2: c2 = -7.959089", "l2: c2 = -8.959089", 1)
        a, b = prep(t), prep(m)
        if n == "l2_c2_checks_main (section)":
            a = [l for l in a if not l.startswith("diagnostic")]
        out.append((n, compare(a, b)))
    return out


def jsons():
    data = os.path.join(WT, "solver/inner_pert/data")

    def leaves(o, p=""):
        if isinstance(o, dict):
            for k, v in o.items():
                yield from leaves(v, f"{p}/{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                yield from leaves(v, f"{p}[{i}]")
        else:
            yield p, o
    res = []
    for f in sorted(x for x in os.listdir(data) if x.startswith("l2_c2_") and x.endswith(".json")):
        try:
            old = subprocess.run(["git", "-C", WT, "show", f"HEAD:solver/inner_pert/data/{f}"], capture_output=True, text=True,
                                 check=True).stdout
        except subprocess.CalledProcessError:
            res.append((f, None)); continue
        lc, lo = dict(leaves(json.load(open(os.path.join(data, f))))), dict(leaves(json.loads(old)))
        d = []
        for p in sorted(set(lc) | set(lo)):
            u, v = lc.get(p), lo.get(p)
            if u != v:
                if isinstance(u, (int, float)) and isinstance(v, (int, float)) and not isinstance(u, bool):
                    d.append((rel(u, v), p, u, v))
                else:
                    d.append((None, p, u, v))
        res.append((f, d))
    return res


def headline():
    """c2 and lambda_1 of each M, this folder against I1010-mac (6 printed digits), and c2 + lambda_1"""
    rx = re.compile(r"^   (l2|l2_ctrl|l0|sym|G): (?:c2|lambda_1) = (\S+)", re.M)
    for M in (1, 3, 5):
        r = dict(rx.findall(open(f"{HERE}/logs/l2_c2_M{M}.log").read()))
        m = dict(rx.findall(open(f"{MAC}/I1010-mac/l2_c2_M{M}.log").read()))
        row = ", ".join(f"{k} {float(r[k]):.6f} vs {float(m[k]):.6f} ({rel(float(r[k]), float(m[k])):.1e})" for k in r)
        s0, s1 = float(r["l2"]) + float(r["l0"]), float(m["l2"]) + float(m["l0"])
        print(f"M {M}: {row}; c2 + lambda_1(l0) {s0:+.6f} vs {s1:+.6f}")


def report(res, top=2):
    worst_all = {}
    for n, r in res:
        if r is None:
            print(f"{n}: missing"); continue
        eq, num, txt = r
        w = max((x[0] for x in num), default=0.0)
        worst_all[n] = w
        print(f"{n}: {eq} lines equal; {len(num)} lines with the same text and other numbers (largest relative {w:.1e}); "
              f"{len(txt)} lines with other text")
        for r_, ln, lab in sorted(num, reverse=True)[:top]:
            print(f"      {r_:.1e}  line {ln}  {lab}")
        for x, y in txt[:3]:
            print(f"      text  rpi5: {x[:160]}\n            Mac:  {y[:160]}")
    return worst_all


if not MUT:
    print("== c2 and lambda_1 (l2_c2_M{1,3,5}.log), rpi5 vs Mac (relative difference)")
    headline()
    print("== logs: sizes of the differences (timings masked)")
    report(logs())
    if WT:
        print("== result JSONs against HEAD's (the Mac's tracked ones), leaf by leaf")
        for f, d in jsons():
            if d is None:
                print(f"{f}: not tracked at HEAD"); continue
            nn = [x for x in d if x[0] is not None]
            oth = [x for x in d if x[0] is None]
            print(f"{f}: {len(nn)} numeric leaves differ (largest relative {max((x[0] for x in nn), default=0):.1e}), "
                  f"{len(oth)} non-numeric leaves differ")
            for r_, p, u, v in sorted(nn, key=lambda x: -x[0])[:3]:
                print(f"      {r_:.1e}  {p}: rpi5 {u:.6g}, Mac {v:.6g}")
            for _, p, u, v in oth[:2]:
                print(f"      other  {p}: rpi5 {str(u)[:60]!r}, Mac {str(v)[:60]!r}")
else:
    def stat(mut=""):
        return {n: (len(r[1]), max((x[0] for x in r[1]), default=0.0)) for n, r in logs(mut) if r}
    b, m = stat(), stat("c2")
    (n0, w0), (n1, w1) = b["l2_c2_M1"], m["l2_c2_M1"]
    print(f"control: l2_c2_M1 lines with other numbers {n0} -> {n1}, largest relative difference {w0:.1e} -> {w1:.1e} "
          "(c2 changed by 12%; must be one more line and >= 1e-1)")
    sys.exit(0 if n1 == n0 + 1 and w1 >= 1e-1 and w0 < 1e-1 else 1)

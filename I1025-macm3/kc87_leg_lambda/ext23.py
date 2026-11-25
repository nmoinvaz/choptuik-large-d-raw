#!/usr/bin/env python3
"""ext23.py: the extension of a late-point scan that found no change in its window (#1025 macm3 kc87_leg_lambda).
Order (t5, hc 25 Nov ~14:07 UTC): "if D 22.875 shows no change in 0.100-0.160, extend it at once to 0.060-0.100 by 0.01 (plus a repeat), no need to ask; the same rule for the later points
(extend by the window's width on the side the end signs point to)".
A lone F is the upper root of the multiplet pair (S lies below the window), so the hybrid sign is + below F and - above it: both end signs '-' put F below the window (extend down), both '+' above it (extend up).
usage: ext23.py need D          reads D/read_lower.txt: prints NO (one or more changes: nothing to extend), EXT LO HI SIDE (extension window), or STOP why
       ext23.py setup D LO HI   writes D_ext/point.env (the extension's grid: the new values by 0.01, the middle one twice first) and appends the README section (before any run); prints the folder name
       ext23.py merge D         D_ext must have SCAN_DONE.txt: merges both scans' evaluations, runs read_lower.py on the merged window and repeat_check.py, writes D_ext/read_lower_merged.txt,
                                moves D/read_lower.txt to D/read_lower_first.txt and puts the merged reading in its place (the chain's record reads it)
       ext23.py selftest [--mutate=side|width|merge]
"""
import glob, json, os, re, subprocess, sys, tempfile

L = os.environ.get("EXT23_L") or os.path.expanduser("~/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_leg_lambda")
PY = os.path.expanduser("~/Source/venv-macm3-1058b/bin/python")
MUT = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), None)
EXPLICIT_DOWN = {22.875: 0.060}      # t5's own window for D 22.875: 0.060 to 0.100 (the window's width would give 0.040)
STEP = 0.01


def endpoints(text):
    m = re.search(r"endpoint signs: ([+-]) at (-?[\d.]+), ([+-]) at (-?[\d.]+)", text)
    return (m.group(1), float(m.group(2)), m.group(3), float(m.group(4))) if m else None


def decide(text, D):
    """-> ('NO',) | ('EXT', lo, hi, side) | ('STOP', why)"""
    m = re.search(r"robust changes: (\d+);", text)
    if not m:
        return ("STOP", "no 'robust changes' line in the reading")
    if int(m.group(1)) != 0:
        return ("NO",)
    e = endpoints(text)
    if not e:
        return ("STOP", "no change and no endpoint signs line")
    s_lo, lo, s_hi, hi = e
    if s_lo != s_hi:
        return ("STOP", "no change but different end signs (%s at %r, %s at %r)" % (s_lo, lo, s_hi, hi))
    w = hi - lo
    if MUT == "width":
        w = w / 2
    down = (s_lo == "-") != (MUT == "side")
    if down:
        a = EXPLICIT_DOWN.get(D, round(lo - w, 3)) if MUT != "width" else round(lo - w, 3)
        return ("EXT", a, lo, "down")
    return ("EXT", hi, round(hi + w, 3), "up")


def ext_values(lo, hi, side):
    """the new lambda values of the extension, by STEP, without the endpoint the first scan already holds"""
    n = round((hi - lo) / STEP)
    vals = [round(lo + i * STEP, 3) for i in range(n + 1)]
    return vals[:-1] if side == "down" else vals[1:]


def grid(vals):
    """the middle value twice first (the repeat lands on another process: indices 0 and 1), then the others in order"""
    m = vals[len(vals) // 2]
    others = list(vals); others.remove(m)
    return m, [m, m] + others


def build_merged(dirs, out, D):
    """copies every scan_*_p*.jsonl of the folders (the later folders' files renamed p10, p11, ...) into out and writes the union as scan_D<D>_1025.jsonl; returns the number of evaluations"""
    os.makedirs(out, exist_ok=True)
    rows = []
    for k, d in enumerate(dirs):
        for f in sorted(glob.glob(os.path.join(d, "scan_*_p*.jsonl"))):
            idx = int(re.search(r"_p(\d+)\.jsonl$", f).group(1))
            name = "scan_D%s_p%d.jsonl" % (D, idx + 10 * k)
            txt = open(f).read()
            open(os.path.join(out, name), "w").write(txt)
            rows += [json.loads(l) for l in txt.splitlines() if l.strip()]
    rows.sort(key=lambda r: r["lam"])
    open(os.path.join(out, "scan_D%s_1025.jsonl" % D), "w").write("".join(json.dumps(r) + "\n" for r in rows))
    return len(rows)


def read_merged(dirs, out, D, lo, hi):
    """the merged reading text: read_lower.py on the merged window, then repeat_check.py on the merged file"""
    n = build_merged(dirs, out, D) if MUT != "merge" else build_merged(dirs[:1], out, D)
    rl = "%s/common/in" % L
    r = subprocess.run([PY, "-I", "read_lower.py", out, "%.3f" % lo, "%.3f" % hi], cwd=rl, capture_output=True, text=True)
    text = "== window: read_lower.py scan %.3f %.3f (merged: %d evaluations of the folders %s)\n%s(exit %d)\n" % (lo, hi, n, " + ".join(os.path.basename(os.path.dirname(d.rstrip("/"))) for d in dirs), r.stdout + r.stderr, r.returncode)
    c = subprocess.run([PY, "-I", "repeat_check.py", "%s/scan_D%s_1025.jsonl" % (out, D)], cwd=rl, capture_output=True, text=True)
    return text + c.stdout + c.stderr


def read_first_env(path):
    """point.env of the first scan -> the lines to keep (everything except comments, LAMP and WIN)"""
    keep = []
    for l in open(path):
        if l.startswith("#") or l.startswith("LAMP=") or l.startswith("WIN="):
            continue
        keep.append(l.rstrip("\n"))
    return keep


def now():
    return subprocess.check_output(["date", "-u", "+%Y-%m-%d %H:%M:%S"]).decode().strip()


def do_setup(D, lo, hi):
    dn = repr(D)
    side = "down" if hi <= float(re.search(r"WIN=\"(-?[\d.]+) (-?[\d.]+)\"", open("%s/%s/point.env" % (L, dn)).read()).group(1)) + 1e-9 else "up"
    vals = ext_values(lo, hi, side)
    rep, lamp = grid(vals)
    fe = "%s/%s_ext" % (L, dn)
    os.makedirs(fe, exist_ok=True)
    env = read_first_env("%s/%s/point.env" % (L, dn))
    win = "%.3f %.3f" % (lo, hi)
    order = ("t5's order (hc 25 Nov ~14:07 UTC, quoted): \"if D 22.875 shows no change in 0.100-0.160, extend it at once to 0.060-0.100 by 0.01 (plus a repeat), no need to ask; the same rule for the later points "
             "(extend by the window's width on the side the end signs point to)\"")
    with open(fe + "/point.env", "w") as f:
        f.write("\n".join(env) + "\n")
        f.write("# the extension of D %s (the first window's reading: ../%s/read_lower_first.txt after the merge): %s\n" % (dn, dn, order))
        f.write("LAMP=(%s)\n" % " ".join('"%.3f"' % x for x in lamp))
        f.write('WIN="%s"; REP=%.3f\n' % (win, rep))
    first = open("%s/%s/read_lower.txt" % (L, dn)).read()
    e = endpoints(first)
    sec = (
        "\n## D %s extension (written before its check and scan, %s UTC)\n\n" % (dn, now()) +
        "**Order** " + order + "\n"
        "**Why:** the first scan of D %s (window %.3f to %.3f, `%s/read_lower.txt`) found no robust change; its end signs are %s at %.3f and %s at %.3f, so a lone F (the upper root of the multiplet pair, hybrid sign + below it and - above it) lies %s the window.\n" % (dn, e[1], e[3], dn, e[0], e[1], e[2], e[3], "below" if side == "down" else "above") +
        "**Inputs:** the same state, record and pins as D %s (`%s_ext/pins.txt`, written by prepare87.sh from point.env).\n" % (dn, dn) +
        "**Grid:** the extension window %s, by 0.01 (the endpoint %.3f is the first scan's own): lambda %s (%d values), the middle one %.3f twice first (a repeat on another process); NP=4 processes of 1 thread at nice 15. The merged reading (`ext23.py merge`) reads the first scan and this one together on lambda %.3f to %.3f; the first window's own reading is kept as `%s/read_lower_first.txt`.\n" % (
            win, lo if side == "up" else hi, ", ".join("%.3f" % x for x in vals), len(vals), rep, min(lo, e[1]), max(hi, e[3]), dn) +
        "**Predictions (mine, before the run):** the source check accepts with all controls firing and the k_c 79 check refusing about 90%%; the repeat of %.3f bit-identical about 90%%; all %d noise-robust about 80%%; "
        "exactly one robust change in the merged window about 85%% (none about 10%%: F outside it again, the chain then stops; two or more about 5%%); its orientation '+ to -' about 90%% (given one); "
        "it lies in the extension window %s about 85%% (given one); no ln|det| minimum without a sign change about 85%%; the float64 sign equals the hybrid at every evaluation about 60%%; scan wall 15 to 60 min about 70%%; no memory alert about 90%%.\n"
        % (rep, len(lamp), win) +
        "## Log\n")
    open(L + "/README.md", "a").write(sec)
    print(dn + "_ext")


def do_merge(D):
    dn = repr(D)
    fe = "%s/%s_ext" % (L, dn)
    if not os.path.exists(fe + "/SCAN_DONE.txt"):
        print("STOP no SCAN_DONE.txt in %s_ext" % dn); return 1
    if os.path.exists("%s/%s/read_lower_first.txt" % (L, dn)):
        print("STOP read_lower_first.txt exists already"); return 1
    wlo, whi = [float(x) for x in re.search(r"WIN=\"(-?[\d.]+) (-?[\d.]+)\"", open(fe + "/point.env").read()).groups()]
    first = open("%s/%s/read_lower.txt" % (L, dn)).read()
    e = endpoints(first)
    lo, hi = min(wlo, e[1]), max(whi, e[3])
    text = read_merged(["%s/%s/scan" % (L, dn), fe + "/scan"], fe + "/merged", dn, lo, hi)
    open(fe + "/read_lower_merged.txt", "w").write(text)
    os.rename("%s/%s/read_lower.txt" % (L, dn), "%s/%s/read_lower_first.txt" % (L, dn))
    open("%s/%s/read_lower.txt" % (L, dn), "w").write("== the merged reading of the first scan and its extension (%s_ext; the first window's own reading is read_lower_first.txt); the same text as %s_ext/read_lower_merged.txt\n" % (dn, dn) + text)
    print("merged: window %.3f %.3f" % (lo, hi))
    return 0


def selftest():
    ok = True
    def chk(name, cond):
        nonlocal ok
        print("planted:", name, "PASS" if cond else "FAIL"); ok = ok and cond
    base = "points 7 in 0.100-0.160; not noise-robust: none\nhybrid signs: ...\nrobust changes: %d; touching a non-robust point (not counted): none\nendpoint signs: %s at %s, %s at %s\n(exit 0)\n"
    down = base % (0, "-", "0.100", "-", "0.160")
    up = base % (0, "+", "0.100", "+", "0.160")
    r = decide(down, 22.875)
    chk("no change, both end signs '-': extend down; D 22.875 takes t5's own window 0.060 to 0.100", r == ("EXT", 0.06, 0.1, "down"))
    r = decide(down, 22.8125)
    chk("no change, both end signs '-', another point: down by the window's width (0.060): 0.040 to 0.100", r == ("EXT", 0.04, 0.1, "down"))
    r = decide(up, 22.8125)
    chk("no change, both end signs '+': extend up by the width: 0.160 to 0.220", r == ("EXT", 0.16, 0.22, "up"))
    chk("one change: nothing to extend", decide(base % (1, "+", "0.100", "-", "0.160"), 22.875) == ("NO",))
    chk("no change and different end signs: STOP", decide(base % (0, "+", "0.100", "-", "0.160"), 22.875)[0] == "STOP")
    chk("a text without the changes line: STOP", decide("nothing", 22.875)[0] == "STOP")
    chk("extension values down 0.060 to 0.100 by 0.01 without the endpoint 0.100", ext_values(0.06, 0.1, "down") == [0.06, 0.07, 0.08, 0.09])
    chk("extension values up 0.160 to 0.220 without the endpoint 0.160", ext_values(0.16, 0.22, "up") == [0.17, 0.18, 0.19, 0.2, 0.21, 0.22])
    m, lamp = grid([0.06, 0.07, 0.08, 0.09])
    chk("grid: the middle value (0.080) twice first, then the rest in order", m == 0.08 and lamp == [0.08, 0.08, 0.06, 0.07, 0.09])
    chk("grid: the two copies sit on processes 0 and 1 of 4", [i % 4 for i, x in enumerate(lamp) if x == m] == [0, 1])
    # the merge plumbing on real data: D 23.0's scan split into two folders must read like the whole scan
    src = L + "/23.0/scan"
    if os.path.isdir(src):
        with tempfile.TemporaryDirectory() as t:
            a, b = t + "/A/scan", t + "/B/scan"
            os.makedirs(a); os.makedirs(b)
            for p in (0, 1):
                open("%s/scan_D23.0_p%d.jsonl" % (a, p), "w").write(open("%s/scan_D23.0_p%d.jsonl" % (src, p)).read())
            for p in (2, 3):
                open("%s/scan_D23.0_p%d.jsonl" % (b, p - 2), "w").write(open("%s/scan_D23.0_p%d.jsonl" % (src, p)).read())
            txt = read_merged([a, b], t + "/M", "23.0", -0.1, 0.3)
            whole = open(L + "/23.0/read_lower.txt").read()
            core = lambda s: [l for l in s.splitlines() if l.startswith(("points", "hybrid signs", "  robust change", "robust changes", "endpoint signs", "repeat check", "ln|det|"))]
            c_m = [re.sub(r"/[^ ]*scan_D23.0_1025.jsonl", "", l) for l in core(txt)]
            c_w = [re.sub(r"/[^ ]*scan_D23.0_1025.jsonl", "", l) for l in core(whole)]
            chk("merge: D 23.0's scan split in two folders and merged reads like the whole (changes, signs, repeat)", c_m == c_w and len(c_m) >= 6)
            if c_m != c_w:
                print("  merged:", c_m, "\n  whole:", c_w)
    else:
        chk("merge: D 23.0's scan folder exists", False)
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    cmd = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    if cmd == "selftest":
        sys.exit(selftest())
    D = float(args[0])
    if cmd == "need":
        r = decide(open("%s/%r/read_lower.txt" % (L, D)).read(), D)
        print(" ".join(str(x) for x in r))
    elif cmd == "setup":
        do_setup(D, float(args[1]), float(args[2]))
    elif cmd == "merge":
        sys.exit(do_merge(D))
    else:
        sys.exit("unknown command")

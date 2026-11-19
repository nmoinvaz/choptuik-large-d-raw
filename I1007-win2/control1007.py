"""#1007 control for the moved worktree (efad7afd -> ec7cfea7), from logs only. Level 5's approach solve does not depend on the polish radius, so the lines a new log
prints before level 5's first `(low)` stop line (pretune, levels 9 and 7, the approach solve) must equal the first lines of #999's 0.11/0.105 log (efad7afd, same approach
radius) after normalizing seconds, memory addresses and the radii line's polish radius, and after dropping the stop lines and verbose-3 trial lines (the old code printed a stop
line only for a noise-floor stop). The count m of compared lines is taken from the new log.

    python control1007.py NEWLOG [--mutate=other|shift]
--mutate=other compares against #999's 0.10/0.095 log (approach 0.095) and --mutate=shift drops one line of the new prefix: both must differ.  Exit 0 when equal."""
import os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)
new = sys.argv[1]
ref = f"{R}/I999-win2/logs/hier_nb_M9_polish5_0.11_approach5_0.105_win2.log"
if "--mutate=other" in sys.argv:
    ref = f"{R}/I999-win2/logs/hier_nb_M9_polish5_0.10_approach5_0.095_win2.log"


def kept(path):
    """the normalized lines without stop and trial lines, and the index in them of the first level-5 (low) stop line (None if there is none)"""
    out, first = [], None
    for l in open(path, encoding="utf-8", errors="replace").read().replace("\r", "").splitlines():
        if "Exception ignored" in l:
            continue
        if re.match(r"\s+level \d+ \((low|top)\): stop at", l):
            if first is None and re.match(r"\s+level 5 \(low\)", l):
                first = len(out)
            continue
        if "trial lam" in l:
            continue
        l = re.sub(r"0x[0-9A-Fa-f]+", "ADDR", l)
        l = re.sub(r"\[\d+ s( total)?\]", "[T s]", l)
        l = re.sub(r"\((\d+) residuals, \d+ s\)", r"(\1 residuals, T s)", l)
        l = re.sub(r"\[\d+ s, (\d+) residuals\]", r"[T s, \1 residuals]", l)
        l = re.sub(r"(r_5 \S+) -> \S+,", r"\1 -> XI,", l)
        out.append(l)
    return out, first


a, m = kept(new)
b, _ = kept(ref)
if m is None:
    print("no level 5 (low) stop line in the new log yet"); sys.exit(2)
pa = a[:m]
if "--mutate=shift" in sys.argv:
    pa = pa[:20] + pa[21:]
pb = b[:len(pa)]
same = pa == pb and len(b) >= len(pa)
print(f"{os.path.basename(new)} against {os.path.basename(ref)}: {len(pa)} lines before level 5's first (low) stop line, equal after normalization: {same}")
if not same:
    for i, (x, y) in enumerate(zip(pa, pb)):
        if x != y:
            print(f"first difference at line {i + 1}:\n  new: {x[:150]}\n  ref: {y[:150]}"); break
sys.exit(0 if same else 1)

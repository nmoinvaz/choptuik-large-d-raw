"""#1012 stage 5 control for run (b) (--h5=1e-4 without --predict): K is computed after level 5's first solve, so (b)'s log must equal stage 1's (--h5=1e-4 with --predict) line for line up to, and
excluding, the `Jacobian K computed` line (which says 10 residuals with --predict and 8 without), and must differ after it. Exit 0 when the prefixes are equal and the K lines are 10 and 8.
    python control1012e.py NEWLOG REFLOG [--mutate=shift|ref_other]
--mutate=shift drops a line of the new prefix; --mutate=ref_other is given a reference of another h5 by the caller: both must fail."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import control1012 as C


def kline(path):
    m = re.search(r"Jacobian K computed \((\d+) residuals\)", open(path, encoding="utf-8", errors="replace").read())
    return int(m.group(1)) if m else None


def idx_k(lines):
    return next((i for i, l in enumerate(lines) if "Jacobian K computed" in l), None)


new, ref = sys.argv[1], sys.argv[2]
a, _ = C.kept(new)
b, _ = C.kept(ref)
ka, kb = idx_k(a), idx_k(b)
if ka is None or kb is None:
    print("no K line yet"); sys.exit(2)
pa, pb = a[:ka], b[:kb]
if "--mutate=shift" in sys.argv:
    pa = pa[:20] + pa[21:]
same = pa == pb
print(f"{os.path.basename(new)} against {os.path.basename(ref)}: {len(pb)} lines before the K line, equal: {same}; K line residuals new {kline(new)} (want 8), ref {kline(ref)} (want 10)")
if not same:
    k = next((i for i, (x, y) in enumerate(zip(pa, pb)) if x != y), min(len(pa), len(pb)))
    print(f"first difference at line {k + 1}:\n  new: {(pa[k] if k < len(pa) else '(ends)')[:150]}\n  ref: {(pb[k] if k < len(pb) else '(ends)')[:150]}")
sys.exit(0 if same and kline(new) == 8 and kline(ref) == 10 else 1)

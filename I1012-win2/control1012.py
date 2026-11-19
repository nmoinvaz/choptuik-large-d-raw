"""#1012 plumbing control, from logs only. A run with --h5=1e-6 (level 5's default relative step) must reproduce #1011 run 1's log line for line up to and including its first
`level 5 (low): stop at` line; a run with --h5=1e-4 must not. Both logs have the stop reasons (verbose 2); seconds and memory addresses are normalized.

    python control1012.py NEWLOG REFLOG [--mutate=shift]
--mutate=shift drops one line of the new prefix and must fail.  Exit 0 when the first m+1 lines of NEWLOG equal those of REFLOG (m = index of REFLOG's first level-5 (low) stop line)."""
import re, sys


def drop_pool_traceback(ls):
    """after the FIXED-A line, drop a Traceback block that ends in the exit-time multiprocessing.Pool.__del__ 'BytesIO' AttributeError (present in some logs of identical
    code, absent in others; control989.py v2 does the same)"""
    k = next((i for i, l in enumerate(ls) if "FIXED-A M" in l), len(ls))
    out, i = ls[:k + 1], k + 1
    while i < len(ls):
        if ls[i].startswith("Traceback (most recent call last)"):
            j = i
            while j < len(ls) and not ls[j].startswith("AttributeError"):
                j += 1
            if j < len(ls) and "BytesIO" in ls[j]:
                i = j + 1
                continue
        out.append(ls[i])
        i += 1
    return out


def kept(path):
    out, first = [], None
    lines = open(path, encoding="utf-8", errors="replace").read().replace("\r", "").splitlines()
    for l in drop_pool_traceback(lines):
        if "Exception ignored" in l or "trial lam" in l:
            continue
        l = re.sub(r"0x[0-9A-Fa-f]+", "ADDR", l)
        l = re.sub(r"\[\d+ s( total)?\]", "[T s]", l)
        l = re.sub(r"\((\d+) residuals, \d+ s\)", r"(\1 residuals, T s)", l)
        l = re.sub(r"\[\d+ s, (\d+) residuals\]", r"[T s, \1 residuals]", l)
        if first is None and re.match(r"\s+level 5 \(low\): stop at", l):
            first = len(out)
        out.append(l)
    return out, first


def main():
    new, ref = sys.argv[1], sys.argv[2]
    a, _ = kept(new)
    b, m = kept(ref)
    if m is None:
        print("no level 5 (low) stop line in the reference")
        return 2
    pa, pb = a[:m + 1], b[:m + 1]
    if "--mutate=shift" in sys.argv:
        pa = pa[:20] + pa[21:]
    same = pa == pb and len(a) >= m + 1
    print(f"{new.split('/')[-1]} against {ref.split('/')[-1]}: the first {m + 1} lines (to the reference's first level-5 (low) stop, inclusive), equal: {same}")
    if not same:
        k = next((i for i, (x, y) in enumerate(zip(pa, pb)) if x != y), min(len(pa), len(pb)))
        print(f"first difference at line {k + 1}:\n  new: {(pa[k] if k < len(pa) else '(ends)')[:160]}\n  ref: {(pb[k] if k < len(pb) else '(ends)')[:160]}")
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())

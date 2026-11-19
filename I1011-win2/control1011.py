"""#1011 control, from logs only. --floor_max=1e-4 changes only the slow-progress stop of a level whose |g| is above 1e-4, so a new log must equal a reference log
of the same radii (XI, AP) from the code before it, line for line, up to the reference's first level-5 (low) stop line, which the new log must not print there.
Both logs are ec7cfea7/656396fd format (stop reasons at verbose 2); verbose-3 trial lines of the reference are dropped, seconds and addresses normalized.

    python control1011.py NEWLOG REFLOG [--mutate=other|shift]
--mutate=other must be given a reference of other radii (the caller passes it) and --mutate=shift drops one line of the new prefix: both must differ.
Exit 0 when the new log equals the reference over the m lines before the reference's first level-5 (low) stop and does not print that stop at line m, else 1."""
import re, sys


def kept(path):
    out, first = [], None
    for l in open(path, encoding="utf-8", errors="replace").read().replace("\r", "").splitlines():
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


new, ref = sys.argv[1], sys.argv[2]
a, _ = kept(new)
b, m = kept(ref)
if m is None:
    print("no level 5 (low) stop line in the reference"); sys.exit(2)
pa, pb = a[:m], b[:m]
if "--mutate=shift" in sys.argv:
    pa = pa[:20] + pa[21:]
eq = pa == pb and len(a) > m
nxt = a[m] if len(a) > m else "(the new log ends)"
absent = not re.match(r"\s+level 5 \(low\): stop at .*no longer halves", nxt)
print(f"{new.split('/')[-1]} against {ref.split('/')[-1]}: {m} lines before the reference's first level-5 (low) stop, equal: {eq}; "
      f"the new log's next line is {'not ' if absent else ''}that stop: {nxt.strip()[:100]}")
if not eq:
    for i, (x, y) in enumerate(zip(pa, pb)):
        if x != y:
            print(f"first difference at line {i + 1}:\n  new: {x[:150]}\n  ref: {y[:150]}"); break
sys.exit(0 if eq and absent else 1)

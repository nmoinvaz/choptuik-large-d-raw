"""#1012: test of control1012.py's drop of the exit-time pool Traceback block on a real log that carries it (#976's M = 7 xi1 0.15 `zero` log, whose last 5 lines are the block).

    python selftest_traceback1012.py [--mutate=keep]
1. kept(log with the block) must equal kept(the same log without its last 5 lines)   (the block is dropped).
2. kept(log with one extra line before the FIXED-A line) must differ                  (a real difference is not dropped).
3. a Traceback block that does not end in the BytesIO error is kept                    (only the pool block is dropped).
--mutate=keep disables the drop (drop_pool_traceback returns its input): check 1 must fail.   Exit 0 when all three checks pass."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import control1012 as C

REF = "D:/choptuik-i935-raw/I976-win2/logs/hier_nb_M7_win2_rtol14_xi015_zero.log"
SC = os.environ.get("SCRATCH", ".")
if "--mutate=keep" in sys.argv:
    C.drop_pool_traceback = lambda ls: ls
lines = open(REF, encoding="utf-8", errors="replace").read().replace("\r", "").splitlines()
k = next(i for i, l in enumerate(lines) if "FIXED-A M" in l)
tail = lines[k + 1:]
block = [i for i, l in enumerate(tail) if l.startswith("Traceback")]
assert block and "BytesIO" in tail[-1], "the reference log has no pool Traceback block at its end"


def write(name, ls):
    p = os.path.join(SC, name)
    open(p, "w", encoding="utf-8", newline="\n").write("\n".join(ls) + "\n")
    return p


full = write("tb_full.log", lines)
nobl = write("tb_nobl.log", lines[:k + 1 + block[0]])
extra = write("tb_extra.log", lines[:5] + ["an extra line"] + lines[5:])
other = write("tb_other.log", lines[:k + 1] + ["Traceback (most recent call last):", "  File x", "ValueError: something else"])
ok1 = C.kept(full) == C.kept(nobl)
ok2 = C.kept(extra) != C.kept(nobl)
ok3 = C.kept(other)[0][-3:] == ["Traceback (most recent call last):", "  File x", "ValueError: something else"]
print(f"1. the pool block is dropped: {ok1}; 2. a real extra line is kept: {ok2}; 3. another Traceback is kept: {ok3}")
sys.exit(0 if ok1 and ok2 and ok3 else 1)

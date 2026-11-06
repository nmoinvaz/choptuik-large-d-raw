"""check (e): the anm_run.py logs of the code before and after the change, every line with times removed, must be
equal, and so must the records' Delta and |F| strings. python compare_e.py BEFORE.log AFTER.log BEFORE_DIR AFTER_DIR;
exit 1 when they differ."""
import json, re, sys

def strip(line):
    line = re.sub(r"\b\d+(\.\d+)? s\b", "<t> s", line)              # "41 s", "19.2 s"
    line = re.sub(r"'seconds': [0-9.]+", "'seconds': <t>", line)
    line = re.sub(r"(\d+)(\.\d+)? s,", r"<t> s,", line)
    return line.rstrip()

a = [strip(x) for x in open(sys.argv[1])]
b = [strip(x) for x in open(sys.argv[2])]
diff = [(i, x, y) for i, (x, y) in enumerate(zip(a, b)) if x != y]
print(f"log lines {len(a)} and {len(b)}, differing (times removed) {len(diff)}")
for i, x, y in diff[:10]:
    print(f"  line {i}:\n    before {x}\n    after  {y}")
ra = [json.loads(x) for x in open(sys.argv[3] + "/anm_run.jsonl")]
rb = [json.loads(x) for x in open(sys.argv[4] + "/anm_run.jsonl")]
keys = ("D_str", "F_pred", "F_final", "Delta", "steps", "accepted", "moved")
sa = [[repr(at.get(k)) for k in keys] for r in ra for at in r.get("attempts", [])]
sb = [[repr(at.get(k)) for k in keys] for r in rb for at in r.get("attempts", [])]
for x, y in zip(sa, sb):
    print("  attempt before " + " ".join(x) + "\n          after  " + " ".join(y))
same = not diff and len(a) == len(b) and sa == sb
print("PASS: identical" if same else "FAIL: different")
sys.exit(0 if same else 1)

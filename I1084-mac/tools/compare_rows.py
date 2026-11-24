"""compare two value_mp rows (the last JSON line of each file) field by field; seconds and calls are reported, not
compared. Exit 0 iff every other field is identical.

    python compare_rows.py NAME OLD_FILE NEW_FILE
"""
import json
import sys


def last_row(path):
    row = None
    for line in open(path):
        line = line.strip()
        if line.startswith("{"):
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if "re" in d and "sig" in d:
                row = d
    return row


name, a, b = sys.argv[1:4]
old, new = last_row(a), last_row(b)
skip = {"seconds", "calls", "J"}
keys = sorted((set(old) | set(new)) - skip)
diff = [k for k in keys if old.get(k) != new.get(k)]
print(f"{name}: {len(keys) - len(diff)} of {len(keys)} fields identical"
      + (f"; DIFFER: {', '.join(diff)}" if diff else "")
      + f"; calls old {old['calls']} ({sum(old['calls'])}), new {new['calls']} ({sum(new['calls'])}); "
      f"seconds old {old['seconds']}, new {new['seconds']}")
for k in diff:
    print(f"  {k}: old {old.get(k)!r} new {new.get(k)!r}")
sys.exit(1 if diff else 0)

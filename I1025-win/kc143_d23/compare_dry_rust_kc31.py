import json, sys
a = [json.loads(l) for l in open(sys.argv[1]) if l.strip()]
b = [json.loads(l) for l in open(sys.argv[2]) if l.strip()]
SKIP = {"sec", "sec_parts", "b12", "mm", "role", "kind", "it"}
print(f"records: rust {len(a)}, ddm {len(b)}")
ok = len(a) == len(b) and len(a) > 0
for ra, rb in zip(a, b):
    keys = sorted((set(ra) | set(rb)) - SKIP)
    diff = [k for k in keys if ra.get(k) != rb.get(k)]
    print(f"lambda {ra['lam']!r}: rust b12={ra.get('b12')} sign {ra['sign']:+.0f} ln {ra['ln']!r}; ddm b12={rb.get('b12')} sign {rb['sign']:+.0f} ln {rb['ln']!r}; fields differing (excluding the timings): {diff or 'none'}; "
          f"seconds rust {ra.get('sec')} {ra.get('sec_parts')} ddm {rb.get('sec')} {rb.get('sec_parts')}")
    ok = ok and not diff
print("ALL FIELDS EQUAL (bit for bit, excluding the timings)" if ok else "DIFFERENCE FOUND")
sys.exit(0 if ok else 1)

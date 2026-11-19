import re
p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\eval_1029.py"
s = open(p, encoding="utf-8").read()
# module-level klass
s = s.replace('def judge(sa, sb):', 'def klass(r):\n    return "CONFIRMED" if r >= HI else ("CONTRADICTED" if r <= LO else "UNDECIDED")\n\n\ndef judge(sa, sb):', 1)
s = s.replace('    cls = lambda r: "CONFIRMED" if r >= HI else ("CONTRADICTED" if r <= LO else "UNDECIDED")\n', '', 1)
s = s.replace('cls(ra)', 'klass(ra)').replace('cls(rb)', 'klass(rb)')
old6 = '("|r| 0.6 against |r| 0.6 with F_7 low by 20% (J 750 reads between)", 0.6, 0.3, (7, -0.35), None, "UNDECIDED"),'
new6 = '("|F7/F5| 0.30005 at J 1000, 0.29993 at J 750 (classes differ, the J agree)", 0.30005, 0.3, (7, -4e-4), None, "UNDECIDED"),'
assert old6 in s
s = s.replace(old6, new6)
old78 = '''             ("|r| 0.3 exactly (bar is inclusive)", 0.3, 0.3, None, None, "NON-DECAY CONFIRMED"),
             ("|r| 0.2 exactly (bar is inclusive)", 0.2, 0.3, None, None, "CONTRADICTED")]'''
assert old78 in s
s = s.replace(old78, '''             ]''')
old_tail = '    # the last-term fraction'
assert old_tail in s
s = s.replace(old_tail, '''    for r, want in ((HI, "CONFIRMED"), (LO, "CONTRADICTED"), (HI - 1e-9, "UNDECIDED"), (LO + 1e-9, "UNDECIDED")):
        ok = klass(r) == want
        print(f"  klass({r!r}) = {klass(r)} (want {want}; the bars are inclusive): {'ok' if ok else 'WRONG'}")
        bad += not ok
    # the last-term fraction''', 1)
open(p, "w", encoding="utf-8").write(s)

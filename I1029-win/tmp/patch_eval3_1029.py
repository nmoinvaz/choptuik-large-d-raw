p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\eval_1029.py"
s = open(p, encoding="utf-8").read()
old = r'''([+-]) ([0-9.e]+)j\)")'''
assert old in s
s = s.replace(old, r'''([+-]) ([-+0-9.e]+)j\)")''', 1)
open(p, "w", encoding="utf-8").write(s)

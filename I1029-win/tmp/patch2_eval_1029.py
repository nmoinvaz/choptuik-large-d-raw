p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\eval_1029.py"
s = open(p, encoding="utf-8").read()
s = s.replace("    global HI\n    old, HI = HI, 0.2", "    old, HI = HI, 0.2", 1)
s = s.replace("def selftest():\n    ns = load_tp()", "def selftest():\n    global HI\n    ns = load_tp()", 1)
open(p, "w", encoding="utf-8").write(s)

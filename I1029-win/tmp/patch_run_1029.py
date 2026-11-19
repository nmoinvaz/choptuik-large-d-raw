p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\run_1029.py"
s = open(p, encoding="utf-8").read()
old = '        open(stop, "w").write("x")\n        rc, codes = drive([dummy("r0", slow, env), dummy("r1", slow, env)]'
assert old in s
s = s.replace(old, '        import threading\n        threading.Timer(1.5, lambda: open(stop, "w").write("x")).start()      # the file appears after both runs started\n        rc, codes = drive([dummy("r0", slow, env), dummy("r1", slow, env)]', 1)
open(p, "w", encoding="utf-8").write(s)

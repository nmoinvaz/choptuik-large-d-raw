p = r"C:\Users\nathan\Source\choptuik-large-d-raw\I1029-win\run_1029.py"
s = open(p, encoding="utf-8").read()
assert "l.split()[3] for l in" in s
s = s.replace("l.split()[3] for l in", "l.split()[4] for l in", 1)
open(p, "w", encoding="utf-8").write(s)

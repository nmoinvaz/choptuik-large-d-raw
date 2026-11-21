"""#966: one new base's row, from its nextcheck and rows outputs, into the README table and the comment body.
    python addrow.py D RAWHASH README COMMENT_IN COMMENT_OUT PUSHHASH STAMP"""
import re, sys
D, raw, readme, cin, cout, push, stamp = sys.argv[1:8]
O = __file__.rsplit("/", 1)[0] + "/out"
nc = open(f"{O}/nextcheck966_D{D}.txt").read()
mv = open(f"{O}/nextcheck966_D{D}_move.txt").read()
ty = open(f"{O}/type966_D{D}.txt").read()
m = re.search(r"nearest stable pole off the axis (\S+) \+- (\S+)i \(n (\d+)\).*root test (\S+), \|D0 - P1\| (\S+), (\S+) ->", nc)
re_, im, n, root, dist, diff = m.groups()
ok, okm = "PASS, Re stays" in nc, "FAIL (--mutate=move)" in mv
r = re.search(r"Delta ratio: D\* (\S+) \(s \S+\), mu (\S+)", ty)
d = re.search(r"Delta dlog: D\* (\S+) \(s \S+\), mu (\S+)", ty)
fmt = lambda x: f"{float(x):+.1f}"
rows = f"{r.group(1)} ({fmt(r.group(2))}), " + (f"{d.group(1)} ({float(d.group(2)):+.3f})" if d else "no Dlog estimate")
diff = diff.replace("-", "−")
row_readme = f"| {D} | {raw} | {re_} ± {im}i ({n} approximants) | {root}, {dist}, {diff} | {265.078 - float(D):.4f} | {'PASS (0)' if ok else 'FAIL (1)'}, {'FAIL (1)' if okm else 'PASS (0)'} | {rows} |"
row_comment = f"| {D} | {raw} | {re_} ± {im}i ({n} approximants) | {root}, {dist}, {diff} | {265.078 - float(D):.4f} | {'PASS' if ok else 'FAIL'}, {'FAIL' if okm else 'PASS'} | {rows} |"
open(readme, "a").write(row_readme + "\n")
s = open(cin).read()
rows_t = re.findall(r"^\| 26\d\.\d+ \|.*\|$", s, flags=re.M)
s = s.replace(rows_t[-1], rows_t[-1] + "\n" + row_comment)
bases = [x.split("|")[1].strip() for x in rows_t] + [D]
s = re.sub(r"At [0-9., and]+ Re stays at 262\.08", "At " + (", ".join(bases[:-1]) + " and " + bases[-1]) + " Re stays at 262.08"
           if ok and all("PASS" in x.split("|")[6] for x in rows_t) else "At " + ", ".join(bases) + " see the table", s)
s = re.sub(r"last update \S+ \S+ UTC", f"last update {stamp} UTC", s)
s = re.sub(r"Raw: `I966-mac-sing/` at \w+\.", f"Raw: `I966-mac-sing/` at {push}.", s)
open(cout, "w").write(s)
print(row_comment)
print("reading PASS" if ok else "reading FAIL", "| control fails" if okm else "| CONTROL DID NOT FAIL")

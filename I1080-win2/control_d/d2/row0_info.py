import json
import sys

r = json.loads(open(sys.argv[1]).readline())
A1, w1 = r["A"] + float(r["dA"]), r["wf"] + float(r["dwf"])          # zero_mp: A + float(dx[0]), wf + float(dx[1])
print("|".join([repr(r["A"]), repr(r["wf"]), repr(A1), repr(w1), ",".join(repr(float(s)) for s in r["F3"])]))

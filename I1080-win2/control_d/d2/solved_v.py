import json
import sys

x = json.load(open(sys.argv[1]))
print(",".join(repr(t) for t in x[2:6]))

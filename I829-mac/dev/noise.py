# the jets' coefficient noise: the plateau of the two-base weighted least-squares residual (no mirror is evaluated)
import sys, os
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-xf-829/hp")
sys.argv = [sys.argv[0]] + sys.argv[1:]
import mpmath as mp
import fold_mirror as F
import t3
mp.mp.dps = 80
RAW = "/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/d012cdf9-58a7-44fd-8235-23e0811480fc/scratchpad/raw-wt"
which = os.environ["WHICH"]
pairs = [("259.8352", "259.7864"), ("259.8068", "259.7603"), ("259.7510", "259.7053")]
ser = {}
for jp in F.jets(RAW):
    Db, c = F.delta_series(jp)
    ser["%.4f" % float(Db)] = (Db, c)
for a, b in pairs:
    if which == "real":
        inputs = [ser[a], ser[b]]
    else:
        pl = F.Plant(0.0, 0.3, float(which))
        inputs = [(ser[a][0], pl.series(ser[a][0], 1)), (ser[b][0], pl.series(ser[b][0], 2))]
    out = []
    for d in range(10, 16):
        for kind in ("QP", "DA"):
            try:
                _, res = t3.forms_ls(inputs, (d, d, d), kind)
                out.append("%s%d %.1e" % (kind, d, float(res)))
            except Exception as ex:
                out.append("%s%d err" % (kind, d))
    print(which, a, b, " ".join(out), flush=True)

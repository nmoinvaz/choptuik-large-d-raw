"""#1025 D 18.46875: the repeat check of one scan file: every lambda that occurs more than once must repeat its sign, ln|det|, noise
signs and float64 sign exactly (bar 1e-6 on ln|det|; the first runs' repeats were bit-identical). Exit 0 agree, 1 disagree, 2 no repeat.
usage: repeat_check.py SCAN.jsonl | repeat_check.py selftest (a planted agreeing set must pass, and a planted sign flip and a planted
ln|det| shift of 1e-3 must each fail)"""
import sys, json, collections
def check(rows):
    g = collections.defaultdict(list)
    for r in rows:
        g[r["lam"]].append(r)
    rep = {k: v for k, v in g.items() if len(v) > 1}
    if not rep:
        return 2, "no repeated lambda"
    bad = [k for k, v in rep.items() if any(x["sign"] != v[0]["sign"] or abs(x["ln"] - v[0]["ln"]) > 1e-6 or x["noise"] != v[0]["noise"]
                                            or x["f64_sign"] != v[0]["f64_sign"] for x in v[1:])]
    return (1, f"DISAGREE at {bad}") if bad else (0, f"lambda {sorted(rep)}: {[len(v) for k, v in sorted(rep.items())]} evaluations each, agree")
def selftest():
    mk = lambda lam, s, ln: dict(lam=lam, sign=s, ln=ln, noise=[s, s], f64_sign=s)
    ok = [mk(1.71, 1.0, -5.0), mk(1.62, -1.0, -4.0), mk(1.71, 1.0, -5.0)]
    flip = [mk(1.71, 1.0, -5.0), mk(1.62, -1.0, -4.0), mk(1.71, -1.0, -5.0)]
    shift = [mk(1.71, 1.0, -5.0), mk(1.62, -1.0, -4.0), mk(1.71, 1.0, -5.001)]
    r = [check(ok)[0], check(flip)[0], check(shift)[0]]
    print(f"selftest: agreeing {r[0]} (want 0), sign flip {r[1]} (want 1), shift {r[2]} (want 1)")
    sys.exit(0 if r == [0, 1, 1] else 1)
if __name__ == "__main__":
    if sys.argv[1] == "selftest":
        selftest()
    c, msg = check([json.loads(l) for l in open(sys.argv[1])])
    print(f"repeat check {sys.argv[1]}: {msg} -> {'PASS' if c == 0 else 'FAIL'}")
    sys.exit(c)

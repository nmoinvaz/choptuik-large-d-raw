"""#1025: table of signtest results from signtest.py's JSON lines (two per record: lambda - 0.02 and + 0.02).
Pass = agree true at both lambda and the two signs opposite (the coordinator's rule). Reads only the log(s); the selftest feeds planted lines (pass, same sign, disagree, missing second line) and
must give pass, FAIL, FAIL, FAIL.
usage: python -I signtest_table1025.py LOG [LOG ...] > table.md      python -I signtest_table1025.py --selftest"""
import json
import sys


def rows_from(lines):
    recs = {}
    order = []
    for ln in lines:
        ln = ln.strip()
        if not ln.startswith("{"):
            continue
        try:
            r = json.loads(ln)
        except ValueError:
            continue
        if "signs" not in r:
            continue
        k = (r["state"], r["D"], r["kc"])
        if k not in recs:
            recs[k] = []
            order.append(k)
        recs[k].append(r)
    return [(k, recs[k]) for k in order]


def verdict(rs):
    if len(rs) != 2:
        return "FAIL", "needs two lambda lines, got %d" % len(rs)
    if not all(r["agree"] for r in rs):
        return "FAIL", "agree false at " + " and ".join("%.5f" % r["lam"] for r in rs if not r["agree"])
    s = [r["signs"][0] for r in rs]
    if s[0] == s[1]:
        return "FAIL", "same sign at both lambda"
    return "pass", "opposite signs, all four agree at both lambda"


def table(lines):
    out = ["| row (state) | D | k_c | lambda -0.02 / +0.02 | result | signs at lambda -0.02 | signs at lambda +0.02 | count < 1e-12 sigma_max (-/+) | count < 1e-15 (-/+) | reason |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    n_pass = 0
    n = 0
    for (st, D, kc), rs in rows_from(lines):
        v, why = verdict(rs)
        n += 1
        n_pass += v == "pass"
        g = lambda i, key: (rs[i][key] if i < len(rs) else "-")
        sg = lambda i: ("%s" % [int(x) for x in rs[i]["signs"]]) if i < len(rs) else "-"
        out.append("| %s | %g | %d | %s / %s | **%s** | %s | %s | %s / %s | %s / %s | %s |" % (
            st.replace("sol_", "").replace(".npy", ""), D, kc, ("%.5f" % rs[0]["lam"]) if rs else "-", ("%.5f" % rs[1]["lam"]) if len(rs) > 1 else "-", v, sg(0), sg(1),
            g(0, "n_below_1e_12"), g(1, "n_below_1e_12"), g(0, "n_below_1e_15"), g(1, "n_below_1e_15"), why))
    out.append("")
    out.append("%d of %d records pass." % (n_pass, n))
    return "\n".join(out)


def selftest():
    def rec(st, lam, signs, agree):
        return json.dumps(dict(state=st, D=1.0, kc=47, lam=lam, signs=signs, agree=agree, n_below_1e_12=0, n_below_1e_15=0))
    cases = [("pass", [rec("a", 1.0, [1, 1, 1, 1], True), rec("a", 1.1, [-1, -1, -1, -1], True)]),
             ("FAIL", [rec("b", 1.0, [1, 1, 1, 1], True), rec("b", 1.1, [1, 1, 1, 1], True)]),
             ("FAIL", [rec("c", 1.0, [1, -1, 1, 1], False), rec("c", 1.1, [-1, -1, -1, -1], True)]),
             ("FAIL", [rec("d", 1.0, [1, 1, 1, 1], True)])]
    ok = True
    for want, ls in cases:
        got = verdict(rows_from(ls)[0][1])[0]
        print("selftest planted case must be %s, got %s %s" % (want, got, "ok" if got == want else "WRONG"))
        ok &= got == want
    print("selftest", "passes" if ok else "FAILS")
    return 0 if ok else 1


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    lines = []
    for fn in sys.argv[1:]:
        lines += open(fn, encoding="utf-8", errors="replace").read().splitlines()
    print(table(lines))

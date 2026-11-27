"""#1105 step 1d: reads the two re-solves of k_c 55 continuation states (D 15.0 as r150, D 16.5 as r165) and the roots of all four states (c150, r150, c165, r165;
d18_secant.py run, bracket 2.410-2.435 at D 15 and 2.148-2.172 at D 16.5) and forms offset(D) = root(re-solve) - root(continuation state) against the bars in README.md.

usage: read_1105d.py DIR            DIR holds l1kc55r150.jsonl, l1kc55r165.jsonl (ell_refine records) and root_{c150,r150,c165,r165}.jsonl (d18_secant.py run)
       read_1105d.py selftest [--mutate=sign]    planted cases; exit 0 only if each reads as written

Bars: both offsets above 5e-4 and positive (D 16's sign: +8.6e-4): systematic. Both below 2e-4 in size: a one-off. Otherwise mixed. The verdict is taken on the
ranges [a - d, b - c] of the offset from the robust final brackets [a, b] (re-solve) and [c, d] (continuation state); the lam_lin difference is printed beside it.
A root run that was refused (a bracket with same-signed ends) or that has a non-robust end is not read."""
import json
import os
import sys

HI, LO = 5e-4, 2e-4
D16_OFFSET = +8.59e-4          # U40 against the source record at D 16 (step 1b)
MUTATE = ""
DS = (("150", 15.0), ("165", 16.5))


def last(path, kind=None):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    if kind:
        rows = [r for r in rows if r.get("kind") == kind]
    return rows[-1] if rows else None


def root(path):
    if not os.path.exists(path):
        return None, "no root run"
    r = last(path, "root")
    if r is None:
        return None, "no root record (refused or killed)"
    if r.get("status") == "refused" or not all(r["robust"]) or r["signs"][0] == r["signs"][1]:
        return None, f"not read: status {r.get('status')}, robust {r['robust']}, signs {r['signs']}"
    return r, ""


def offsets(cont, resv):
    """cont, resv: root records -> (range lo, range hi, lam_lin difference)"""
    a, b = resv["bracket"]
    c, d = cont["bracket"]
    s = -1.0 if MUTATE == "sign" else 1.0
    lo, hi = a - d, b - c
    if s < 0:
        lo, hi = -hi, -lo
    return lo, hi, s * (resv["lam_lin"] - cont["lam_lin"])


def verdict(offs):
    """offs: list of (lo, hi) ranges (None for an unread one) -> text"""
    if any(o is None for o in offs):
        return "a root is not read: no verdict from the bars"
    if all(lo > HI for lo, hi in offs):
        return "both offsets are above 5e-4 and positive, as at D 16: the continuation offset is systematic"
    if all(-LO <= lo and hi <= LO for lo, hi in offs):
        return "both offsets are below 2e-4 in size: D 16's was a one-off"
    if all(lo > HI or hi < -HI for lo, hi in offs):
        return "both offsets are above 5e-4 in size but not both positive: not D 16's sign, mixed"
    return "mixed, reported as measured (a range may straddle a bar)"


def main(d):
    out = []
    print("| D | state | role | status | final bracket | root (lam_lin) | evals | \\|F\\| | steps | Delta | Delta - source |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    rec = {}
    for k, D in DS:
        rec[k] = last(os.path.join(d, f"l1kc55r{k}.jsonl"))
    src_rec = {k: [json.loads(l) for l in open(os.path.join(d, "in", "l1kc55Fb1025.jsonl")) if l.strip() and json.loads(l)["D"] == D][-1] for k, D in DS}
    res = {}
    for k, D in DS:
        for tag, role in (("c" + k, "continuation"), ("r" + k, "re-solve")):
            rp = os.path.join(d, f"root_{tag}w.jsonl")        # the widened run, if the first was refused (run_root_wide1d.sh)
            wide = os.path.exists(rp)
            r, why = root(rp if wide else os.path.join(d, f"root_{tag}.jsonl"))
            res[tag] = r
            bk = why if r is None else f"({r['bracket'][0]!r}, {r['bracket'][1]!r}), width {r['width']:.2e}"
            lam = "-" if r is None else f"{r['lam_lin']:.9f}"
            ne = "-" if r is None else r["n_eval"]
            st = "-" if r is None else r["status"] + (" (widened)" if wide else "")
            if role == "re-solve":
                rr = rec[k]
                Fv, sv, Dl, dd = f"{rr['F']:.4e}", rr["steps"], repr(rr["Delta"]), f"{rr['Delta'] - src_rec[k]['Delta']:+.3e}"
            else:
                Fv, sv, Dl, dd = f"{src_rec[k]['F']:.4e}", src_rec[k]["steps"], repr(src_rec[k]["Delta"]), "0"
            print(f"| {D} | {tag} | {role} | {st} | {bk} | {lam} | {ne} | {Fv} | {sv} | {Dl} | {dd} |")
    print()
    offs = []
    for k, D in DS:
        c, r = res["c" + k], res["r" + k]
        if c is None or r is None:
            print(f"- offset(D {D}): not formed")
            offs.append(None)
            continue
        lo, hi, mid = offsets(c, r)
        offs.append((lo, hi))
        print(f"- offset(D {D}) = root(r{k}) - root(c{k}): lam_lin difference {mid:+.4e}; range from the brackets {lo:+.4e} .. {hi:+.4e}")
    print(f"- D 16 for comparison: {D16_OFFSET:+.2e} (U40 against the source; U40b +7.5e-4, U40c +9.2e-4)")
    print(f"- verdict: {verdict(offs)}")
    return 0


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)

    def rec(lam, w=1e-7):
        return dict(kind="root", status="tol", bracket=[lam - w / 2, lam + w / 2], width=w, signs=[-1, 1], robust=[True, True], lam_lin=lam, lam_brent=lam, n_eval=9)
    for o1, o2, want in ((8e-4, 7e-4, "systematic"), (5.1e-4, 9e-4, "systematic"), (1e-4, -1.5e-4, "one-off"), (1.9e-4, 0.0, "one-off"),
                         (8e-4, 1e-4, "mixed"), (-8e-4, -7e-4, "mixed"), (3e-4, 4e-4, "mixed")):
        offs = []
        for o in (o1, o2):
            lo, hi, _ = offsets(rec(2.2), rec(2.2 + o))
            offs.append((lo, hi))
        t = verdict(offs)
        got = "systematic" if "systematic" in t else "one-off" if "one-off" in t else "mixed" if "mixed" in t else t
        chk(f"planted offsets {o1:+.1e}, {o2:+.1e}: {want}", got == want)
    # a wide bracket that straddles the 5e-4 bar is mixed, not systematic
    lo, hi, _ = offsets(rec(2.2, 9e-5), rec(2.2 + 5.2e-4, 9e-5))
    chk("a 9e-5 bracket on offset 5.2e-4 straddles the bar: mixed", "mixed" in verdict([(lo, hi), (lo, hi)]) and lo < HI < hi + 1e-3)
    chk("an unread root: no verdict", "not read" in verdict([None, (1e-3, 1e-3)]))
    import tempfile
    d = tempfile.mkdtemp()
    open(f"{d}/root_x.jsonl", "w").write(json.dumps(dict(kind="root", status="refused", bracket=[2.4, 2.5], width=0.1, signs=[1, 1], robust=[True, True], lam_lin=None,
                                                         lam_brent=None, n_eval=2)) + "\n")
    chk("a refused run is not read", root(f"{d}/root_x.jsonl")[0] is None)
    chk("a status-tol run with robust opposite-signed ends is read", root(f"{d}/root_y.jsonl")[0] is not None if open(f"{d}/root_y.jsonl", "w").write(json.dumps(rec(2.2)) + "\n") else False)
    print("selftest:", "FAIL " + "; ".join(bad) if bad else "all cases read as written")
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--mutate="):
            MUTATE = a.split("=", 1)[1]
    if not args:
        sys.exit(__doc__)
    sys.exit(selftest() if args[0] == "selftest" else main(args[0]))

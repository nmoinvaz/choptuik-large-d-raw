"""#1105 step 1e: reads the roots of r165b (a re-solve of r165's own state at D 16.5), r155 (the re-solve of the continuation state at D 15.5) and c155 (that continuation state),
and r165's root from step 1d, and forms (1) T = root(r165b) - root(r165) against t5's bar and (2) offset(15.5) = root(r155) - root(c155), against the offsets of step 1d.

usage: read_1105e.py DIR1E DIR1D          DIR1E holds l1kc55r165b.jsonl, l1kc55r155.jsonl (ell_refine records) and root_{r165b,r155,c155}[w].jsonl (d18_secant.py run);
                                          DIR1D holds root_r165w.jsonl (step 1d), root_c150.jsonl, root_r150.jsonl, root_c165w.jsonl
       read_1105e.py selftest [--mutate=bar|sign]    planted cases; exit 0 only if each reads as written

Bar (t5's): |T| <= 3e-4: re-solved states are reproducible at D 16.5; larger: the re-solve scatter at D 16.5 is itself of order 1e-3. T's range from the robust final brackets
[a, b] (r165b) and [c, d] (r165) is [a - d, b - c]: within +-3e-4 -> reproducible, entirely outside -> scatter, else straddles (reported with lam_lin's difference).
D 15.5 has no bar: the offset and its range are reported beside D 15, D 16 and D 16.5 as measured. A root run is read only if not refused and both final ends are robust
with opposite hybrid signs (a `w` file is the run on the widened bracket after a refusal)."""
import json
import os
import sys

BAR = 3e-4
MUTATE = ""
OFFSETS_1D = {15.0: -5.2640e-4, 16.0: +8.59e-4, 16.5: +3.2521e-3}


def last(path, kind=None):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    if kind:
        rows = [r for r in rows if r.get("kind") == kind]
    return rows[-1] if rows else None


def root(d, tag):
    """-> (record or None, why, widened) for root_<tag>.jsonl, preferring the widened run root_<tag>w.jsonl"""
    wp = os.path.join(d, f"root_{tag}w.jsonl")
    p, wide = (wp, True) if os.path.exists(wp) else (os.path.join(d, f"root_{tag}.jsonl"), False)
    if not os.path.exists(p):
        return None, "no root run", wide
    r = last(p, "root")
    if r is None:
        return None, "no root record (refused or killed)", wide
    if r.get("status") == "refused" or not all(r["robust"]) or r["signs"][0] == r["signs"][1]:
        return None, f"not read: status {r.get('status')}, robust {r['robust']}, signs {r['signs']}", wide
    return r, "", wide


def diff(new, old):
    """new, old: root records -> (range lo, range hi, lam_lin difference) of root(new) - root(old); the mutation 'sign' flips the sign"""
    a, b = new["bracket"]
    c, d = old["bracket"]
    s = -1.0 if MUTATE == "sign" else 1.0
    lo, hi = a - d, b - c
    if s < 0:
        lo, hi = -hi, -lo
    return lo, hi, s * (new["lam_lin"] - old["lam_lin"])


def verdict_T(rng):
    bar = 3e-5 if MUTATE == "bar" else BAR
    if rng is None:
        return "not formed: a root is not read"
    lo, hi, _ = rng
    if -bar <= lo and hi <= bar:
        return f"|T| <= {bar:g}: re-solved states are reproducible here (the whole bracket range is within the bar)"
    if lo > bar or hi < -bar:
        return f"|T| > {bar:g}: the re-solve scatter at D 16.5 is itself of order 1e-3 or more (the whole bracket range is outside the bar)"
    return f"the range straddles the {bar:g} bar: reported as measured (lam_lin's difference is beside it)"


def main(d, d1):
    rec = {t: last(os.path.join(d, f"l1kc55{t}.jsonl")) for t in ("r165b", "r155")}
    src15 = [json.loads(l) for l in open(os.path.join(d, "in", "l1kc55Fb1025.jsonl")) if l.strip() and json.loads(l)["D"] == 15.5][-1]
    src165 = [json.loads(l) for l in open(os.path.join(d, "in", "l1kc55r165.jsonl")) if l.strip()][-1]
    srcs = {"r165b": (src165, "r165"), "r155": (src15, "continuation c155")}
    print("| re-solve | from | D | \\|F\\| | source \\|F\\| | steps | source steps | Delta | Delta change | psi-constraint | re-solve s |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for t, D in (("r165b", 16.5), ("r155", 15.5)):
        r, (s, frm) = rec[t], srcs[t]
        print(f"| {t} | {frm} | {D} | {r['F']:.4e} | {s['F']:.4e} | {r['steps']} | {s['steps']} | {r['Delta']!r} | {r['Delta'] - s['Delta']:+.3e} | {r['constraint']:.4e} | {r['seconds']} |")
    print()
    print("| D | state | role | run | status | final bracket | root (lam_lin) | evals |")
    print("|---|---|---|---|---|---|---|---|")
    res = {}
    for D, t, role, dd in ((16.5, "r165", "re-solve (step 1d)", d1), (16.5, "r165b", "re-solve of r165", d), (15.5, "c155", "continuation", d), (15.5, "r155", "re-solve", d)):
        tt = "r165" if t == "r165" else t
        r, why, wide = root(dd, tt)
        res[t] = r
        if r is None:
            print(f"| {D} | {t} | {role} | {'widened' if wide else 'first'} | {why} | - | - | - |")
        else:
            print(f"| {D} | {t} | {role} | {'widened' if wide else 'first'} | {r['status']} | ({r['bracket'][0]!r}, {r['bracket'][1]!r}), width {r['width']:.2e} | {r['lam_lin']:.9f} | {r['n_eval']} |")
    print()
    T = None if res["r165b"] is None or res["r165"] is None else diff(res["r165b"], res["r165"])
    if T is None:
        print("- T = root(r165b) - root(r165): not formed")
    else:
        print(f"- T = root(r165b) - root(r165): lam_lin difference {T[2]:+.4e}; range from the brackets {T[0]:+.4e} .. {T[1]:+.4e}")
    print(f"- verdict on T: {verdict_T(T)}")
    O = None if res["r155"] is None or res["c155"] is None else diff(res["r155"], res["c155"])
    if O is None:
        print("- offset(15.5) = root(r155) - root(c155): not formed")
    else:
        print(f"- offset(15.5) = root(r155) - root(c155): lam_lin difference {O[2]:+.4e}; range from the brackets {O[0]:+.4e} .. {O[1]:+.4e}")
    offs = dict(OFFSETS_1D)
    if O is not None:
        offs[15.5] = O[2]
    print("- offset(D), re-solve minus continuation: " + ", ".join(f"D {k}: {v:+.3e}" for k, v in sorted(offs.items())) + " (D 16: step 1b, 1c; D 15, 16.5: step 1d; D 15.5: this step)")
    print("- D 15.5 has no bar: reported as measured")
    return 0


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)

    def rec(lam, w=1e-7):
        return dict(kind="root", status="tol", bracket=[lam - w / 2, lam + w / 2], width=w, signs=[-1, 1], robust=[True, True], lam_lin=lam, lam_brent=lam, n_eval=9)
    for t, want in ((1e-5, "reproducible"), (-2.9e-4, "reproducible"), (2.0e-4, "reproducible"), (3.5e-4, "scatter"), (-1.2e-3, "scatter"), (3.25e-3, "scatter")):
        v = verdict_T(diff(rec(2.1459392 + t), rec(2.1459392)))
        got = "reproducible" if "reproducible" in v else "scatter" if "order 1e-3" in v else v
        chk(f"planted T {t:+.1e}: {want}", got == want)
    v = verdict_T(diff(rec(2.1459392 + 3.0e-4, 2e-4), rec(2.1459392, 2e-4)))
    chk("a 2e-4 bracket on T 3.0e-4 straddles the bar", "straddles" in v)
    chk("an unread root: not formed", "not formed" in verdict_T(None))
    lo, hi, mid = diff(rec(2.0 + 5.2e-4), rec(2.0))
    chk("offset: lam_lin difference +5.2e-4 with a range around it", abs(mid - 5.2e-4) < 1e-12 and lo < mid < hi)
    import tempfile
    d = tempfile.mkdtemp()
    open(f"{d}/root_x.jsonl", "w").write(json.dumps(dict(kind="root", status="refused", bracket=[2.4, 2.5], width=0.1, signs=[1, 1], robust=[True, True], lam_lin=None, lam_brent=None, n_eval=2)) + "\n")
    chk("a refused run is not read", root(d, "x")[0] is None)
    open(f"{d}/root_xw.jsonl", "w").write(json.dumps(rec(2.2)) + "\n")
    r, why, wide = root(d, "x")
    chk("the widened run is preferred and read", r is not None and wide)
    print("selftest:", "FAIL " + "; ".join(bad) if bad else "all cases read as written")
    return 1 if bad else 0


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for a in sys.argv[1:]:
        if a.startswith("--mutate="):
            MUTATE = a.split("=", 1)[1]
    if not args:
        sys.exit(__doc__)
    sys.exit(selftest() if args[0] == "selftest" else main(args[0], args[1]))

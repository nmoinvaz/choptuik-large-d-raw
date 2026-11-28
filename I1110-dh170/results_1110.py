"""#1110 dh170: reads the chord state's maps (.map.json) and the root records of `i1101_weakdir.py root` against the bars of #1110.

usage: results_1110.py maps MAP035.json MAP034.json
           bar 1: the kappa=0.35 chord state has exactly 8351 steps and |F| <= 5e-10; bar 2: the kappa=0.34 control has another count.
           exit 0 both pass, 1 bar 1 fails, 5 only bar 2 fails
       results_1110.py read ROOT.jsonl [ROOT_WIDE.jsonl]
           the root records (the second file is the widened bracket (0.05, 0.16), read only if the first has no bracket):
           exit 0 a root formed (status tol, both ends robust with opposite signs), 4 no root but a robust bracket (the cap),
           2 no bracket (refused, or no records); prints the evaluations, delta = root - 0.117824909 (its range over the bracket) and the verdict
       results_1110.py selftest [--mutate=bar7|bar2|ref|count|sign]     planted cases; exit 0 only if each reads as written

Verdict on delta (the range [a - R2, b - R2] of the final bracket [a, b]): entirely inside [-2e-3, 2e-3] "<= 2e-3" (the scatter does not hide the
order, #1104 may use it); entirely at |delta| >= 7e-3 ">= 7e-3" (the order is not readable either); any other range "between (mixed)"."""
import json
import math
import sys

R2_ROOT = 0.117824909            # R2's det-linear root (I1101-dh170/secant_r2w.jsonl)
BAR_LO, BAR_HI = 2e-3, 7e-3      # #1110's bars on |delta|
STEPS_R2, F_BAR = 8351, 5e-10
MUTATE = next((a.split("=", 1)[1] for a in sys.argv if a.startswith("--mutate=")), "")


def maps(m35, m34):
    """-> list of (bar, passed, text)"""
    ref = STEPS_R2 - 1 if MUTATE == "count" else STEPS_R2
    fbar = 5e-9 if MUTATE == "bar7" else F_BAR
    out = [("bar 1: the kappa=0.35 chord state has exactly 8351 steps", m35["steps"] == ref, f"{m35['steps']} steps (R2's record: {STEPS_R2})"),
           ("bar 1: |F| <= 5e-10", m35["F"] <= fbar, f"|F| {m35['F']:.4e}")]
    out.append(("bar 2: the kappa=0.34 control has a count other than 8351", m34["steps"] != ref, f"{m34['steps']} steps"))
    if MUTATE == "bar2":
        out[-1] = (out[-1][0], True, out[-1][2])
    return out


def classify(lo, hi):
    """lo, hi: the range of delta"""
    bl, bh = (2e-2, 7e-2) if MUTATE == "bar7" else (BAR_LO, BAR_HI)
    if lo >= -bl and hi <= bl:
        return "le2e-3", f"delta in [{lo:+.6f}, {hi:+.6f}] inside +-{BAR_LO:g}: the scatter does not hide R0-R2's order, and #1104 may use it"
    if lo >= bh or hi <= -bh:
        return "ge7e-3", f"delta in [{lo:+.6f}, {hi:+.6f}], |delta| >= {BAR_HI:g}: the order from R0-R2 is not readable either; #1104's kappa step waits for #1111's roots"
    return "between", f"delta in [{lo:+.6f}, {hi:+.6f}] reaches between {BAR_LO:g} and {BAR_HI:g} or straddles a bar: between, mixed"


def read_one(recs):
    """-> dict(status formed|partial|nobracket, bracket, root, ...) from one root file's records"""
    ev = [r for r in recs if r.get("kind") == "eval"]
    fin = [r for r in recs if r.get("kind") == "root"]
    ok = [r for r in ev if r["robust"]]
    if fin and fin[-1]["status"] == "tol" and all(fin[-1]["robust"]) and fin[-1]["signs"][0] != fin[-1]["signs"][1]:
        f = fin[-1]
        return dict(status="formed", bracket=tuple(f["bracket"]), root=f["lam_lin"], n=len(ev), sec=f.get("sec"), evals=ev)
    pos = [r["lam"] for r in ok if r["sign"] > 0]
    neg = [r["lam"] for r in ok if r["sign"] < 0]
    if pos and neg:          # the + and - robust evaluations nearest each other (+ below the root, - above, as measured at R0, R2)
        lo_p = [p for p in pos if any(q > p for q in neg)]
        if lo_p:
            a = max(lo_p)
            b = min(q for q in neg if q > a)
            return dict(status="partial", bracket=(a, b), root=None, n=len(ev), sec=None, evals=ev)
    return dict(status="nobracket", bracket=None, root=None, n=len(ev), sec=None, evals=ev)


def read(files):
    """files: one or two lists of records; the second (widened) is used only if the first has no bracket -> dict with verdict"""
    res = read_one(files[0])
    res["wide"] = False
    if res["status"] == "nobracket" and len(files) > 1:
        res = read_one(files[1])
        res["wide"] = True
    if res["status"] == "nobracket":
        res.update(kind=None, verdict="no bracket: reported as measured")
        return res
    ref = R2_ROOT + (1e-3 if MUTATE == "ref" else 0.0)
    a, b = res["bracket"]
    sg = -1.0 if MUTATE == "sign" else 1.0
    lo, hi = sg * (a - ref), sg * (b - ref)
    if lo > hi:
        lo, hi = hi, lo
    res["range"] = (lo, hi)
    res["delta"] = None if res["root"] is None else sg * (res["root"] - ref)
    res["kind"], res["verdict"] = classify(lo, hi)
    return res


def plant(lam, r, robust=True):
    d = r - lam
    return dict(kind="eval", lam=lam, sign=1.0 if d > 0 else -1.0, robust=robust, ln=math.log(abs(d)), dln=1e-5, role="interior", it=0, sec=1)


def planted(r, lams, status="tol", half=1e-6):
    ev = [plant(x, r) for x in lams]
    recs = list(ev)
    if status == "tol":
        recs.append(dict(kind="root", status="tol", why="", bracket=[r - half, r + half], width=2 * half, signs=[1.0, -1.0], robust=[True, True], lam_lin=r,
                         lam_brent=r, n_eval=len(ev), tol=1e-6, sec=1))
    elif status == "refused":
        recs.append(dict(kind="root", status="refused", why="the ends have the same hybrid sign", bracket=[lams[0], lams[1]], width=lams[1] - lams[0],
                         signs=[ev[0]["sign"], ev[1]["sign"]], robust=[True, True], lam_lin=None, lam_brent=None, n_eval=len(ev), tol=1e-6, sec=1))
    return recs


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)
    for steps35, F35, steps34, want, name in ((8351, 3e-10, 8100, 0, "both bars pass"), (8300, 3e-10, 8100, 1, "bar 1 fails on the count"), (8351, 6e-10, 8100, 1, "bar 1 fails on |F|"),
                                              (8351, 3e-10, 8351, 5, "bar 2 fails when the control gives 8351")):
        res = maps(dict(steps=steps35, F=F35), dict(steps=steps34, F=1e-10))
        code = 0 if all(p for _, p, _ in res) else (5 if all(p for n, p, _ in res if n.startswith("bar 1")) else 1)
        chk(f"maps: {name}", code == want)
    # roots: planted exact roots around R2's; the range is the final bracket
    for dlt, want in ((0.0, "le2e-3"), (1.5e-3, "le2e-3"), (-1.5e-3, "le2e-3"), (2.5e-3, "between"), (5e-3, "between"), (-6.9e-3, "between"), (7.5e-3, "ge7e-3"),
                      (-0.0719, "ge7e-3"), (0.012, "ge7e-3")):
        r = R2_ROOT + dlt
        o = read([planted(r, [0.10, 0.13, r + 0.01, r - 0.004])])
        chk(f"root at delta {dlt:+g}: {want}, formed", o["status"] == "formed" and o["kind"] == want and abs(o["delta"] - dlt) < 1e-12)
    # the cap: no final record, a robust bracket from the evaluations
    o = read([planted(R2_ROOT + 1e-3, [0.10, 0.13, 0.12, 0.116], status="cap")])
    chk("cap: bracket (0.116, 0.12) of a root at delta +1e-3 reads between (not decided), status partial",
        o["status"] == "partial" and o["bracket"] == (0.116, 0.12) and o["kind"] == "between")
    o = read([planted(R2_ROOT + 1e-4, [0.10, 0.13, 0.1182, 0.1176], status="cap")])
    chk("cap: bracket (0.1176, 0.1182) of a root at delta +1e-4 reads <= 2e-3", o["status"] == "partial" and o["bracket"] == (0.1176, 0.1182) and o["kind"] == "le2e-3")
    o = read([planted(R2_ROOT + 0.08, [0.10, 0.13, 0.0], status="cap")])
    chk("cap: no + below a - gives no bracket", o["status"] == "nobracket" or o["status"] == "partial" and o["bracket"][0] < o["bracket"][1])
    o = read([planted(0.2, [0.10, 0.13], status="refused")])
    chk("same-signed ends: no bracket, reported as measured", o["status"] == "nobracket" and "no bracket" in o["verdict"])
    # the widened file is used only when the first has no bracket
    w = planted(0.08, [0.05, 0.16, 0.10, 0.07])
    o = read([planted(0.2, [0.10, 0.13], status="refused"), w])
    chk("widened (0.05, 0.16): used when (0.10, 0.13) gives no bracket", o["wide"] and o["status"] == "formed" and o["kind"] == "ge7e-3")
    o = read([planted(R2_ROOT, [0.10, 0.13, 0.118]), w])
    chk("widened file ignored when the first brackets", not o["wide"])
    # a non-robust end does not form a root
    bad_ev = planted(R2_ROOT, [0.10, 0.13, 0.118])
    bad_ev[0]["robust"] = False
    for r in bad_ev:
        if r.get("kind") == "root":
            r["robust"] = [False, True]
    o = read([bad_ev])
    chk("a final record with a non-robust end is not a root", o["status"] != "formed")
    print("selftest:", "FAIL " + "; ".join(bad) if bad else "all cases read as written")
    return 1 if bad else 0


def load(path):
    return [json.loads(line) for line in open(path) if line.strip()]


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    if args[0] == "selftest":
        sys.exit(selftest())
    if args[0] == "maps":
        res = maps(json.load(open(args[1])), json.load(open(args[2])))
        for n, p, t in res:
            print(f"- {'PASS' if p else 'FAIL'}: {n}: {t}")
        sys.exit(0 if all(p for _, p, _ in res) else (5 if all(p for n, p, _ in res if n.startswith("bar 1")) else 1))
    if args[0] == "read":
        recs = [load(f) for f in args[1:] if f]
        if not recs:
            sys.exit("no records")
        o = read(recs)
        print("| # | lambda | role | hybrid sign | robust | dln | ln\\|det\\| | seconds |")
        print("|---|---|---|---|---|---|---|---|")
        for i, r in enumerate(o["evals"]):
            print(f"| {i + 1} | {r['lam']:.10f} | {r.get('role')} | {r['sign']:+.0f} | {r['robust']} | {r['dln'] if r['dln'] is None else format(r['dln'], '.2e')} | {r['ln']:.10f} | {r.get('sec')} |")
        print()
        print(f"- bracket used: {'the widened (0.05, 0.16)' if o['wide'] else '(0.10, 0.13)'}; status {o['status']}")
        if o["status"] == "nobracket":
            print(f"- {o['verdict']}")
            sys.exit(2)
        print(f"- final bracket {o['bracket']}" + (f"; det-linear root {o['root']:.9f}; delta = root - {R2_ROOT} = {o['delta']:+.6f}" if o["root"] is not None else "; no root formed (not status tol)"))
        print(f"- verdict: {o['verdict']}")
        sys.exit(0 if o["status"] == "formed" else 4)
    sys.exit(__doc__)

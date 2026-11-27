"""#1105 step 1c: reads the two re-solves at u0 0.04 (U40b from U30's state, U40c from U50's state) and their roots (d18_secant.py run) and forms
each root's difference from r40 = 2.2449017 (U40) against the bars in README.md (step 1c).

usage: read_1105c.py DIR            DIR holds l1kc55u040b.jsonl, l1kc55u040c.jsonl (ell_refine records) and root_u040b.jsonl, root_u040c.jsonl (d18_secant.py run)
       read_1105c.py selftest [--mutate=ref]    planted cases; exit 0 only if each reads as written

Bars: both within 1e-4 of r40: one root (the source state was off). Either more than 5e-4 from r40: a solve scatter of order 1e-3. Otherwise mixed.
A re-solve with |F| > 1e-8 is not rooted. A root is read only from a run with status tol, both bracket ends robust and of opposite hybrid signs; for any
other final record the robust bracket bounds the difference from r40 (outside the rule, labelled so). The root is lam_lin."""
import json
import os
import sys

R40 = 2.2449017            # t5's value; U40's lam_lin is 2.2449017148
DELTA_U40 = 1.0017134267209413
DELTA_SRC = 1.0017135137307174
LO, HI = 1e-4, 5e-4
TAGS = (("u040b", "U40b", "U30"), ("u040c", "U40c", "U50"))
MUTATE = ""


def last(path, kind=None):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    if kind:
        rows = [r for r in rows if r.get("kind") == kind]
    return rows[-1] if rows else None


def read(d):
    out = {}
    for tag, name, src in TAGS:
        rec = last(os.path.join(d, f"l1kc55{tag}.jsonl"))
        e = dict(name=name, src=src, F=rec["F"], F_start=rec["F_start"], steps=rec["steps"], Delta=rec["Delta"], constraint=rec["constraint"],
                 seconds=rec["seconds"], root=None, bound=None, why="")
        rp = os.path.join(d, f"root_{tag}.jsonl")
        if rec["F"] > 1e-8:
            e["why"] = "|F| above 1e-8: not rooted"
        elif not os.path.exists(rp):
            e["why"] = "no root run"
        else:
            r = last(rp, "root")
            if r is None:
                e["why"] = "no root record"
            elif not all(r["robust"]) or r["signs"][0] == r["signs"][1]:
                e["why"] = f"not read: robust {r['robust']}, signs {r['signs']}"
            else:
                e.update(bracket=r["bracket"], width=r["width"], n_eval=r["n_eval"], status=r["status"], brent=r["lam_brent"])
                if r["status"] == "tol":
                    e["root"] = r["lam_lin"]
                else:
                    e["why"] = f"not read: status {r['status']}"
                    e["bound"] = (r["bracket"][0] - R40, r["bracket"][1] - R40)
        out[tag] = e
    return out


def verdict(res):
    """-> (text, ds) from the two roots (None for an unread root)"""
    ref = R40 + (1e-3 if MUTATE == "ref" else 0.0)
    ds = {t: (None if e["root"] is None else e["root"] - ref) for t, e in res.items()}
    v = [d for d in ds.values()]
    if any(d is not None and abs(d) > HI for d in v):
        return "either root is more than 5e-4 from r40: a solve scatter of order 1e-3 at k_c 55, D 16; no u0 effect below that is readable from single solves", ds
    if any(d is None for d in v):
        return "a root is not read: no verdict from the bars", ds
    if all(abs(d) <= LO for d in v):
        return "both roots are within 1e-4 of r40: the u0 0.04 system has one root; the source state was off", ds
    return "neither root is beyond 5e-4 and at least one is beyond 1e-4: mixed, reported as measured", ds


def main(d):
    res = read(d)
    print(f"r40 = {R40} (U40 lam_lin 2.2449017148); Delta U40 {DELTA_U40!r}, source {DELTA_SRC!r}\n")
    print("| run | start | \\|F\\| | F_start | steps | Delta | Delta - U40 | Delta - source | psi-constraint | re-solve s | status | final bracket | root (lam_lin) | root - r40 | evals |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    text, ds = verdict(res)
    for tag, name, src in TAGS:
        e = res[tag]
        rt = "-" if e["root"] is None else f"{e['root']:.9f}"
        df = "-" if ds[tag] is None else f"{ds[tag]:+.3e}"
        st = e.get("status", e["why"])
        bk = "-" if "bracket" not in e else f"({e['bracket'][0]!r}, {e['bracket'][1]!r}), width {e['width']:.2e}"
        print(f"| {name} | {src} | {e['F']:.4e} | {e['F_start']:.4e} | {e['steps']} | {e['Delta']!r} | {e['Delta'] - DELTA_U40:+.3e} | {e['Delta'] - DELTA_SRC:+.3e} | "
              f"{e['constraint']:.6e} | {e['seconds']} | {st} | {bk} | {rt} | {df} | {e.get('n_eval', '-')} |")
    print()
    for tag, name, src in TAGS:
        e = res[tag]
        if e["bound"] is not None:
            print(f"- {name}: not read (status {e['status']}); its robust bracket bounds root - r40 to {e['bound'][0]:+.3e} .. {e['bound'][1]:+.3e} (outside the rule)")
        elif e["root"] is None:
            print(f"- {name}: {e['why']}")
    print(f"- verdict: {text}")
    return 0


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)
    for a, b, want in ((2e-5, -5e-5, "one root"), (9.9e-5, 0.0, "one root"), (2e-4, 1e-5, "mixed"), (-4.9e-4, 0.0, "mixed"),
                       (6e-4, 0.0, "scatter"), (0.0, -1e-3, "scatter"), (None, 0.0, "not read")):
        res = {"u040b": dict(root=None if a is None else R40 + a), "u040c": dict(root=R40 + b)}
        t = verdict(res)[0]
        got = "one root" if "one root" in t else "scatter" if "solve scatter" in t else "mixed" if "mixed" in t else "not read" if "not read" in t else t
        chk(f"planted differences {a}, {b}: {want}", got == want)
    import tempfile
    d = tempfile.mkdtemp()
    for tag, F, st, rb in (("u040b", 2e-8, None, None), ("u040c", 1e-10, "nonrobust", [2.24, 2.25])):
        open(f"{d}/l1kc55{tag}.jsonl", "w").write(json.dumps(dict(u0=0.04, F=F, F_start=1e-9, steps=2565, Delta=1.0, constraint=1e-4, seconds=1)) + "\n")
    open(f"{d}/root_u040c.jsonl", "w").write(json.dumps(dict(kind="root", status="nonrobust", bracket=[R40 - 1e-3, R40 - 9e-4], width=1e-4, signs=[-1, 1],
                                                              robust=[True, True], lam_lin=R40 - 9e-4, lam_brent=R40 - 9e-4, n_eval=8, sec=1)) + "\n")
    r = read(d)
    chk("|F| 2e-8: not rooted", r["u040b"]["root"] is None and "not rooted" in r["u040b"]["why"])
    chk("status nonrobust: not read, bracket bounds the difference", r["u040c"]["root"] is None and r["u040c"]["bound"] is not None
        and r["u040c"]["bound"][1] < -8e-4)
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

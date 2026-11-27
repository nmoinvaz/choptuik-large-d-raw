"""#1105 step 1b: reads the three re-solves (u0 0.03, 0.04, 0.05 of the k_c 55 D 16 state) and their roots (d18_secant.py run) and forms
T3 = root(U30) - root(U40) and T5 = root(U50) - root(U40) against the bars in README.md (step 1b).

usage: read_1105b.py DIR            DIR holds l1kc55u0X0.jsonl (ell_refine records) and root_u0X0.jsonl (d18_secant.py run records)
       read_1105b.py selftest [--mutate=ref]    planted cases; exit 0 only if each reads as written

A re-solve with |F| > 1e-8 is not rooted. A root is read only from a run whose final record has status tol and whose bracket ends are robust and of
opposite hybrid signs; the root is lam_lin (det-linear inside the final bracket), lam_brent printed beside it. Bars on T3: |T3| <= 1e-4 (the shift falls at
least as fast as u0^-9.7, which predicts -1.5e-5), |T3| >= 3e-4 (the bias is smooth in u0: u0 0.04 is biased too), between: mixed. T5 against |T5| <= 1e-4."""
import json
import os
import sys

TAGS = (("u030", 0.03), ("u040", 0.04), ("u050", 0.05))
LO, HI = 1e-4, 3e-4
P4_U40 = 2.2440428096          # P4's hybrid re-root of the record at u0 0.04 (information)
MUTATE = ""


def last(path, kind=None):
    rows = [json.loads(l) for l in open(path) if l.strip()]
    if kind:
        rows = [r for r in rows if r.get("kind") == kind]
    return rows[-1] if rows else None


def read(d):
    out = {}
    for tag, u0 in TAGS:
        rec = last(os.path.join(d, f"l1kc55{tag}.jsonl"))
        e = dict(u0=u0, F=rec["F"], steps=rec["steps"], Delta=rec["Delta"], constraint=rec["constraint"], seconds=rec["seconds"], root=None, why="")
        rp = os.path.join(d, f"root_{tag}.jsonl")
        if rec["F"] > 1e-8:
            e["why"] = "|F| above 1e-8: not rooted"
        elif not os.path.exists(rp):
            e["why"] = "no root run"
        else:
            r = last(rp, "root")
            if r is None:
                e["why"] = "no root record"
            elif r["status"] != "tol" or not all(r["robust"]) or r["signs"][0] == r["signs"][1]:
                e["why"] = f"not read: status {r['status']}, robust {r['robust']}, signs {r['signs']}"
            else:
                e.update(root=r["lam_lin"], brent=r["lam_brent"], bracket=r["bracket"], width=r["width"], n_eval=r["n_eval"], rsec=r["sec"])
        out[tag] = e
    return out


def verdicts(res):
    """-> dict(T3, T5, v3, v5) from {tag: {root...}}"""
    ref = res["u050" if MUTATE == "ref" else "u040"]["root"]
    out = dict(T3=None, T5=None, v3="T3 not formed", v5="T5 not formed")
    if ref is None:
        return out
    if res["u030"]["root"] is not None:
        t = res["u030"]["root"] - ref
        out["T3"] = t
        out["v3"] = ("|T3| <= 1e-4: the lambda shift falls with u0 at least as fast as u0^-9.7; u0 0.04 carries no u0 bias above about 1e-4/16" if abs(t) <= LO
                     else "|T3| >= 3e-4: the bias is smooth in u0, so u0 0.04 is biased too; the issue becomes a correction" if abs(t) >= HI
                     else "between 1e-4 and 3e-4: mixed, reported as measured")
    if res["u050"]["root"] is not None:
        t = res["u050"]["root"] - ref
        out["T5"] = t
        out["v5"] = "|T5| <= 1e-4: as predicted" if abs(t) <= LO else "|T5| > 1e-4: not as predicted"
    return out


def main(d):
    res = read(d)
    print("| run | u0 | \\|F\\| | steps | psi-constraint | Delta | re-solve s | root (lam_lin) | lam_brent | final bracket | evals |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for tag, u0 in TAGS:
        e = res[tag]
        rt = "-" if e["root"] is None else f"{e['root']:.9f}"
        br = "-" if e["root"] is None else f"{e['brent']:.9f}"
        bk = e["why"] if e["root"] is None else f"({e['bracket'][0]!r}, {e['bracket'][1]!r}), width {e['width']:.2e}"
        print(f"| U{tag[2:]} | {u0} | {e['F']:.4e} | {e['steps']} | {e['constraint']:.6e} | {e['Delta']!r} | {e['seconds']} | {rt} | {br} | {bk} | "
              f"{e.get('n_eval', '-')} |")
    v = verdicts(res)
    print()
    if res["u040"]["root"] is not None:
        print(f"- root(U40) = {res['u040']['root']:.9f}; against P4's re-root of the record at u0 0.04 ({P4_U40}): {res['u040']['root'] - P4_U40:+.3e} (information)")
    for k, tag in (("T3", "u030"), ("T5", "u050")):
        if v[k] is not None:
            print(f"- {k} = root(U{tag[2:]}) - root(U40) = {v[k]:+.4e}: {v['v3' if k == 'T3' else 'v5']}")
        else:
            print(f"- {k}: {v['v3' if k == 'T3' else 'v5']} ({res[tag]['why']})")
    print("- predictions for information: T3 about -1.5e-5 (u0^-9.7), a linear law about -4e-4; T5 about +9e-7")
    return 0


def selftest():
    bad = []

    def chk(name, cond):
        print(("pass " if cond else "FAIL ") + name)
        if not cond:
            bad.append(name)
    base = 2.2440428096
    for t3, want in ((-1.5e-5, "<= 1e-4"), (-9.9e-5, "<= 1e-4"), (-2.0e-4, "between"), (-3.01e-4, ">= 3e-4"), (-4.0e-4, ">= 3e-4"), (1.2e-4, "between")):
        res = {"u030": dict(root=base + t3), "u040": dict(root=base), "u050": dict(root=base + 5e-6)}
        v = verdicts(res)["v3"]
        got = "<= 1e-4" if "<= 1e-4" in v else ">= 3e-4" if ">= 3e-4" in v else "between" if "between" in v else v
        chk(f"planted T3 {t3:+.2e}: {want}", got == want)
    v = verdicts({"u030": dict(root=base - 1e-5), "u040": dict(root=base), "u050": dict(root=base + 2e-4)})
    chk("planted T5 +2e-4: not as predicted", "not as predicted" in v["v5"])
    v = verdicts({"u030": dict(root=None), "u040": dict(root=base), "u050": dict(root=base)})
    chk("a state without a root: T3 not formed", v["T3"] is None)
    v = verdicts({"u030": dict(root=base), "u040": dict(root=None), "u050": dict(root=base)})
    chk("no U40 root: nothing formed", v["T3"] is None and v["T5"] is None)
    # files: |F| above 1e-8 is not rooted; a non-tol root is not read
    import tempfile
    d = tempfile.mkdtemp()
    for tag, u0, F in (("u030", 0.03, 2e-8), ("u040", 0.04, 1e-10), ("u050", 0.05, 1e-10)):
        json.dump(dict(u0=u0, F=F, steps=2565, Delta=1.0, constraint=1e-4, seconds=1), open(f"{d}/l1kc55{tag}.jsonl", "w"))
        open(f"{d}/l1kc55{tag}.jsonl", "a").write("\n")
    for tag, st in (("u040", "tol"), ("u050", "maxev")):
        open(f"{d}/root_{tag}.jsonl", "w").write(json.dumps(dict(kind="root", status=st, bracket=[2.2, 2.3], width=1e-8, signs=[1, -1], robust=[True, True],
                                                                  lam_lin=base, lam_brent=base, n_eval=9, sec=1)) + "\n")
    r = read(d)
    chk("|F| 2e-8: not rooted", r["u030"]["root"] is None and "not rooted" in r["u030"]["why"])
    chk("status maxev: not read", r["u050"]["root"] is None and "not read" in r["u050"]["why"])
    chk("status tol with both robust: read", r["u040"]["root"] == base)
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

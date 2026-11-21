"""#1025 D 18 / 18.5: the pass rules for a p4_hybrid.py root on a stub record (d18_criteria.log). The P4 rules (record system,
one sign change on the window's grid, one over all evaluations, noise-robust, bracket <= 1e-7) plus the edge rule: the root at least
0.05 grid steps from the window's outer grid point on its side (guess (1 - w) or guess (1 + w)), where a root could lie outside
the window. The middle grid point is the guess, and a root near it is not flagged (the coordinator's amendment, 2026-11-21).
usage: d18_check.py OUT.jsonl [D] | d18_check.py selftest"""
import sys, json
WS = (0.02, 0.06, 0.15, 0.35)                           # p4_hybrid's windows, relative to the guess


def check(r):
    g, root = r["lam_guess"], r["lam"]
    ev = {float(k): v["sign"] for k, v in r["evals"].items()}
    out = dict(record_system=bool(r["record_system"]), grid_changes=r["n_signchanges_grid"] == 1, changes_all=r["n_changes_all"] == 1,
               noise_robust=bool(r["noise_robust"]), bracket=(r["bracket_width"] or 1) <= 1e-7)
    win = edge = None
    for w in WS:                                        # the first window whose grid has a sign change (p4_hybrid stops there)
        gr = [g * (1 - w), g, g * (1 + w)]
        sg = [ev.get(min(ev, key=lambda l: abs(l - x))) if ev and min(abs(l - x) for l in ev) <= 1e-14 * g else None for x in gr]
        if None in sg:
            break
        ch = [i for i in range(2) if sg[i] != sg[i + 1]]
        if ch:
            i = [k for k in ch if gr[k] <= root <= gr[k + 1]]
            win = (w, gr)
            if root is not None and i:
                st = g * w; lo, hi = (root - gr[i[0]]) / st, (gr[i[0] + 1] - root) / st
                edge = (lo, hi, lo if i[0] == 0 else hi)   # the last: the distance from the outer grid point
            break
    out["edge"] = edge is not None and edge[2] >= 0.05
    ok = all(out.values()) and root is not None
    return ok, out, win, edge


def report(r):
    ok, out, win, edge = check(r)
    print(f"D {r['D']} k_c {r['kc']} {r['mode']}: lam {r['lam']!r}, guess {r['lam_guess']!r} ({(r['lam'] / r['lam_guess'] - 1) * 100:+.3f}%), "
          f"window {win[0] if win else None}, grid {[round(x, 7) for x in win[1]] if win else None}")
    print(f"  edge distances (grid steps from the interval's lower, upper edge; from the outer grid point): "
          f"{None if edge is None else [round(x, 3) for x in edge]}")
    print("  " + ", ".join(f"{k} {'ok' if v else 'FAIL'}" for k, v in out.items()) + f" -> {'PASS' if ok else 'FAIL'}")
    return ok


if sys.argv[1] == "selftest":                           # planted records through the same code; each failing case must fail
    def rec(root, signs, nch=1, nall=1, robust=True, bw=2e-8, system=True, g=2.0, w=0.02):
        grid = [g * (1 - w), g, g * (1 + w)]
        ev = {repr(l): dict(sign=s) for l, s in zip(grid, signs)}
        return dict(D=18.0, kc=63, mode="hybrid", lam=root, lam_guess=g, evals=ev, record_system=system, n_signchanges_grid=nch,
                    n_changes_all=nall, noise_robust=robust, bracket_width=bw)
    cases = [("pass", rec(2.01, [1, 1, -1]), True), ("0.01 steps from the middle point (the guess)", rec(2.0004, [1, 1, -1]), True),
             ("root at the middle point", rec(2.0, [1, 1, -1]), True), ("0.01 steps from the middle point, lower interval", rec(1.9996, [1, -1, -1]), True),
             ("0.01 steps from the outer upper point", rec(2.0396, [1, 1, -1]), False), ("0.01 steps from the outer lower point", rec(1.9604, [1, -1, -1]), False), ("two changes", rec(2.01, [1, 1, -1], nall=2), False),
             ("not noise-robust", rec(2.01, [1, 1, -1], robust=False), False), ("not the record system", rec(2.01, [1, 1, -1], system=False), False),
             ("bracket 1e-6", rec(2.01, [1, 1, -1], bw=1e-6), False)]
    bad = 0
    for name, r, want in cases:
        got = check(r)[0]; bad += got != want
        print(f"selftest {name}: {'PASS' if got else 'FAIL'} (want {'PASS' if want else 'FAIL'}) {'ok' if got == want else 'WRONG'}")
    print("selftest", "passes" if bad == 0 else f"FAILS ({bad} wrong)"); sys.exit(1 if bad else 0)
rs = [json.loads(l) for l in open(sys.argv[1])]
if len(sys.argv) > 2:
    rs = [r for r in rs if r["D"] == float(sys.argv[2])]
sys.exit(0 if all([report(r) for r in rs]) else 1)

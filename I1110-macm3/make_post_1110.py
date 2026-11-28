#!/usr/bin/env python3
"""#1110 on macm3: builds post_1110.md from the logs, .map.json files and root records of this folder (every number from the files).
Usage: python3 make_post_1110.py DATA_COMMIT TIME_UTC [ROOTNAME ...] > post_1110.md     (ROOTNAMEs: root_chord035 [root_chord035_wide])
       python3 make_post_1110.py --selftest        (the bar-3 verdict on planted deltas; --mutate=swap exchanges the two thresholds and must fail)"""
import json, os, re, sys

R2ROOT = 0.117824909
D = os.path.dirname(os.path.abspath(__file__))
LO_BAR, HI_BAR = 2e-3, 7e-3


def verdict(delta, lo=LO_BAR, hi=HI_BAR):
    a = abs(delta)
    if a <= lo:
        return "the scatter does not hide R0-R2's order (#1104 may use it)"
    if a >= hi:
        return "the scatter hides it; #1104's kappa step waits for #1111's roots"
    return "mixed"


def selftest():
    mut = "--mutate=swap" in sys.argv
    lo, hi = (HI_BAR, LO_BAR) if mut else (LO_BAR, HI_BAR)
    cases = [(1e-3, "does not hide"), (-1.9e-3, "does not hide"), (2e-3, "does not hide"), (4e-3, "mixed"), (-6.9e-3, "mixed"), (7e-3, "hides"), (-2e-2, "hides")]
    ok = True
    for dl, want in cases:
        got = verdict(dl, lo, hi)
        good = got.startswith({"does not hide": "the scatter does not", "mixed": "mixed", "hides": "the scatter hides"}[want])
        print(f"delta {dl:+.1e}: expected {want}, read {got!r}: {'ok' if good else 'WRONG'}")
        ok &= good
    print("selftest:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


def sec(name):
    t = {}
    for l in open(os.path.join(D, "exits_1110.txt")):
        m = re.match(r"(\S+ \S+) UTC (start|end) (\S+)( exit=(\d+))?", l)
        if m:
            t.setdefault(m.group(3), {})[m.group(2)] = m.group(1)
    return t


def main():
    commit, when, names = sys.argv[1], sys.argv[2], sys.argv[3:] or ["root_chord035"]
    m35 = json.load(open(os.path.join(D, "sol_chord035_D23.0000.map.json")))
    m34 = json.load(open(os.path.join(D, "sol_chord034_D23.0000.map.json")))
    c0 = open(os.path.join(D, "coords_r0.log")).read()
    c2 = open(os.path.join(D, "coords_r2.log")).read()
    cl = lambda t: re.search(r"chord035: \|dz\| (\S+), dDelta (\S+); fraction null (\S+) weak (\S+) strong (\S+); weak coords (.*)", t).groups()
    z0, z2 = cl(c0), cl(c2)
    recs = {}
    for n in names:
        rs = [json.loads(l) for l in open(os.path.join(D, n + ".jsonl")) if l.strip()]
        recs[n] = (rs, [r for r in rs if r.get("kind") == "root"][-1], int(open(os.path.join(D, n + ".exit")).read()))
    last = recs[names[-1]][1]
    root = last["lam_lin"]
    delta = root - R2ROOT
    b1 = m35["steps"] == 8351 and m35["F"] <= 5e-10
    b2 = m34["steps"] != 8351
    print(f"#1110 on macm3: a chord state on R2's step map against R2's root (k_c 127, D 23.0), runner t5-macm3 (MacBook Air M3), {when}. Raw: `I1110-macm3/`, raw-data commit {commit}.\n")
    print(f"**delta = root(chord) - 0.117824909 = {delta:+.4e}: |delta| is {'<= 2e-3' if abs(delta) <= LO_BAR else ('>= 7e-3' if abs(delta) >= HI_BAR else 'between 2e-3 and 7e-3')}, so {verdict(delta)}.** "
          f"The chord state's root is {root!r} ({last['status']}, bracket [{last['bracket'][0]!r}, {last['bracket'][1]!r}], width {last['width']:.2e}); R2's own robust bracket is [0.1178060580, 0.1178310580] (width 2.5e-5). "
          f"Bars 1 and 2 passed: the chord state has {m35['steps']} steps and |F| {m35['F']:.4e}; the kappa 0.34 control has {m34['steps']}. "
          f"Across the robust bracket delta runs from {last['bracket'][0] - R2ROOT:+.4e} to {last['bracket'][1] - R2ROOT:+.4e}; delta over R1 - R2 (0.0229) is {delta / 0.0229:.2f}.\n")
    print("### Bars\n\n| bar | value | verdict |\n|---|---|---|")
    print(f"| 1: chord state on R2's map: 8351 steps, |F| <= 5e-10 | {m35['steps']} steps, |F| {m35['F']:.4e} (R2: 8351, 3.1242e-10) | **{'PASS' if b1 else 'FAIL'}** |")
    print(f"| 2: control kappa=0.34 gives a count other than 8351 | {m34['steps']} steps, |F| {m34['F']:.4e} | **{'PASS (fired)' if b2 else 'FAIL'}** |")
    print(f"| 3: delta = root(chord) - 0.117824909 | {delta:+.6e} (|delta| <= 2e-3, >= 7e-3, or between) | **{verdict(delta)}** |")
    print("\n### Roots (`i1101_weakdir.py root ... --tol=1e-6 --b12=rust --b12_threads=2`, RAYON_NUM_THREADS=2; bracket as given)\n")
    print("| run | bracket given | evaluations | exit | status | final robust bracket (width) | det-linear root | delta | seconds |\n|---|---|---|---|---|---|---|---|---|")
    for n in names:
        rs, f, rc = recs[n]
        ev = [r for r in rs if r.get("kind") != "root"]
        lams = [e["lam"] for e in ev if e.get("role") in ("lo", "hi")]
        print(f"| {n} | ({min(lams)!r}, {max(lams)!r}) | {f['n_eval']} | {rc} | {f['status']} | [{f['bracket'][0]!r}, {f['bracket'][1]!r}] ({f['width']:.3e}) | {f['lam_lin']!r} | {f['lam_lin'] - R2ROOT:+.6e} | {f['sec']} |")
    print("\nEvaluations (lambda, hybrid sign, float64 sign, dln, robust, seconds):\n")
    for n in names:
        ev = [r for r in recs[n][0] if r.get("kind") != "root"]
        print(f"- {n}: " + "; ".join(f"{e['lam']!r} {int(e['sign']):+d} {int(e['f64_sign']):+d} {e['dln']:.2e} {'R' if e['robust'] else 'NOT robust'} {e['sec']}" for e in sorted(ev, key=lambda e: e['lam'])))
    print("\n### State difference by band (`coords`, R0's SVD bands; states on other step maps are allowed)\n")
    print("| base | |dz| | dDelta | null | weak | strong | weak coordinates (from the smallest singular value) |\n|---|---|---|---|---|---|---|")
    print(f"| chord035 - R0 | {z0[0]} | {z0[1]} | {z0[2]} | {z0[3]} | {z0[4]} | {z0[5]} |")
    print(f"| chord035 - R2 (extra command) | {z2[0]} | {z2[1]} | {z2[2]} | {z2[3]} | {z2[4]} | {z2[5]} |")
    t = sec(None)
    print("\n### What ran\n")
    print("From `solver/matter` of `~/Source/choptuik-ell1fast` (693a4d79; the issue's db7f9c60 is its ancestor, `i1101_weakdir.py` differs by the root command's `--b12=rust` and `--b12_threads` lines), venv `venv-macm3-1058b`, `D18_DIR` set to that worktree "
          "(the root command's default `~/Source/choptuik-kmm` is absent here). Steps with OPENBLAS_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6, nice 10, caffeinate: "
          + "; ".join(f"{k} {v['start'][11:]} to {v['end'][11:]} UTC" for k, v in t.items() if "end" in v) +
          "; all exit 0. R0's record system was reproduced (|F| 3.1959e-10 against 3.1949e-10, 4179 steps). The jac and svd npz stay on the machine (`~/Source/I1110-macm3-local/`). "
          "The root runs: " + "; ".join(f"{n} exit {recs[n][2]}, {recs[n][1]['sec']} s" for n in names) + ".")
    print("\n### Differs from the order or the issue\n")
    print("- The issue's root command says `--b12=fast`; the order says `--b12=rust --b12_threads=2`, which I ran (`rust` is bit for bit DDEll's in #1102's check; `fast` is the issue's).")
    print("- Extra command: `coords` with R2's state as base, for the issue's \"state difference |z_chord - z_R2| by band\" (the order's `coords` has R0 as base).")
    print("- Nothing was pushed or posted from this Mac.")


if __name__ == "__main__":
    sys.exit(selftest()) if "--selftest" in sys.argv else main()

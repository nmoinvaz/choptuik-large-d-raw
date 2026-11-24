#!/usr/bin/env python3
"""#1025 kc79_far (dh610) roots_pair.py D [selftest [--mutate]]: the lambda_1 roots of tag g (../kc79_leg/D<D>/) and tag i (D<D>/i/) at one shared D side by side, from the files.
No number is typed by hand. Reads read_lower.txt (the robust change line), scan/scan_D<D>_all.jsonl (ln|det| per lambda) and in/<tag>.jsonl (Delta) of each, and the previous tag g point's read_lower.txt and record
(PREV, default the D one grid step of 0.03125 below) for the root's slope along the g leg per unit Delta (context only: it assumes Delta alone moves the root).
usage (from this folder): python3 -I roots_pair.py 21.34375 21.3125 > D21.34375/roots_pair.txt
selftest: planted read_lower texts with known roots; the difference, the bracket test and the range overlap must come out as planted; --mutate swaps the two texts, the signed difference must change sign and the selftest exits 1."""
import json, re, sys

PAT = re.compile(r"robust change \(([\d.]+), ([\d.]+)\), (\S+ to \S+), det-linear ([\d.]+), range \[([\d.]+), ([\d.]+)\]")


def change(txt):
    m = PAT.findall(txt)
    if len(m) != 1:
        raise SystemExit(f"roots_pair: {len(m)} robust change lines, one wanted")
    a, b, ori, root, lo, hi = m[0]
    return dict(a=float(a), b=float(b), ori=ori, root=float(root), lo=float(lo), hi=float(hi))


def pair(g, i):
    return dict(diff=i["root"] - g["root"], same_bracket=(g["a"], g["b"]) == (i["a"], i["b"]),
                overlap=(max(g["lo"], i["lo"]), min(g["hi"], i["hi"])))


def selftest(mutate):
    tg = "robust change (0.795, 0.800), + to -, det-linear 0.798768, range [0.798216, 0.798768]"
    ti = "robust change (0.795, 0.800), + to -, det-linear 0.798701, range [0.798136, 0.798701]"
    if mutate:
        tg, ti = ti, tg
    p = pair(change(tg), change(ti))
    ok = abs(p["diff"] - (-0.000067)) < 1e-9 and p["same_bracket"] and abs(p["overlap"][0] - 0.798216) < 1e-9 and abs(p["overlap"][1] - 0.798701) < 1e-9
    q = pair(change(tg.replace("(0.795, 0.800)", "(0.790, 0.795)")), change(ti))
    ok = ok and not q["same_bracket"]
    print("selftest" + (" --mutate" if mutate else ""), "PASS" if ok else "FAIL" + (" (FIRED)" if mutate else ""))
    return 0 if ok else 1


def rec(path, D):
    return [json.loads(l) for l in open(path) if l.strip() and json.loads(l)["D"] == float(D)][-1]


def lns(path):
    return {r["lam"]: r["ln"] for r in (json.loads(l) for l in open(path) if l.strip())}


if __name__ == "__main__":
    if sys.argv[2:3] == ["selftest"]:
        sys.exit(selftest("--mutate" in sys.argv))
    D = sys.argv[1]
    PREV = sys.argv[2] if len(sys.argv) > 2 else None
    g_dir, i_dir = f"../kc79_leg/D{D}", f"D{D}/i"
    g, i = change(open(f"{g_dir}/read_lower.txt").read()), change(open(f"{i_dir}/read_lower.txt").read())
    p = pair(g, i)
    print(f"D {D}, k_c 79 roots, not yet physical; orientation as the reader prints it (g: {g['ori']}, i: {i['ori']}), identified by position")
    print("| tag | bracket | det-linear root | estimator range (spread over interpolation choices, not an enclosure) |")
    print("|---|---|---|---|")
    for n, c in (("g (h 0.03125)", g), ("i (h 0.0625)", i)):
        print(f"| {n} | ({c['a']:.3f}, {c['b']:.3f}) | {c['root']:.6f} | [{c['lo']:.6f}, {c['hi']:.6f}] |")
    print(f"\nroot i - root g = {p['diff']:+.6f}; same bracket: {p['same_bracket']}; the estimator ranges overlap on [{p['overlap'][0]:.6f}, {p['overlap'][1]:.6f}]: {p['overlap'][0] <= p['overlap'][1]}")
    dg, di = rec(f"{g_dir}/in/l1kc79Lw1025g.jsonl", D)["Delta"], rec(f"{i_dir}/in/l1kc79Lw1025i.jsonl", D)["Delta"]
    print(f"Delta g {dg!r}, Delta i {di!r}, i - g {di - dg:+.6e}")
    if PREV:
        pg = change(open(f"../kc79_leg/D{PREV}/read_lower.txt").read())
        dp = rec(f"../kc79_leg/D{PREV}/in/l1kc79Lw1025g.jsonl", PREV)["Delta"]
        slope = (g["root"] - pg["root"]) / (dg - dp)
        print(f"context: along the tag g leg D {PREV} to {D} the root moves {g['root'] - pg['root']:+.6f} for a Delta move of {dg - dp:+.6e}, slope {slope:.3f} per unit Delta; "
              f"if Delta alone moved the root, the Delta difference {di - dg:+.4e} would move it by {slope * (di - dg):+.3e} (observed {p['diff']:+.3e})")
    lg, li = lns(f"{g_dir}/scan/scan_D{D}_all.jsonl"), lns(f"{i_dir}/scan/scan_D{D}_all.jsonl")
    print("\n| lambda | ln abs det, tag g | ln abs det, tag i | i - g |")
    print("|---|---|---|---|")
    for lam in sorted(set(lg) & set(li)):
        print(f"| {lam:.3f} | {lg[lam]!r} | {li[lam]!r} | {li[lam] - lg[lam]:+.6f} |")

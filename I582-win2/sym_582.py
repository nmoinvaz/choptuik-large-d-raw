#!/usr/bin/env python3
"""Conjugate symmetry of det M(lambda) at kf 27, read off the evaluation caches: for each lower circle of #582 (and #574's mirrors) and its upper twin of #574,
the evaluation at (re, -im) of the lower circle must equal the one at (re, im) of the upper circle with ln|det| the same and arg(det) negated (mod 2 pi).
usage: python sym_582.py            (prints, per pair, the matched points, max |d ln|det||, max |arg_lower + arg_upper| mod 2 pi)
       python sym_582.py --mutate=arg   (control: one lower arg is shifted by 0.5, the check must fail, exit 1)
Pass: at least 5 matched points per pair and both maxima below 1e-6 (the evaluations are one floating-point computation at conjugate arguments, so rounding only)."""
import glob, json, math, os, sys
RAW = "D:/choptuik-large-d-raw"
PAIRS = []  # (lower folder in task, upper folder in I574)
for re_, im in [(2.85, 1.25), (3.85, 1.25), (4.35, 1.25)] + [(r, 1.75) for r in (1.85, 2.35, 2.85, 3.35, 3.85, 4.35)]:
    PAIRS.append((f"I582-win2/k27_re{re_:.2f}_im-{im:.2f}", f"I574-win2/k27_re{re_:.2f}_im+{im:.2f}"))
PAIRS += [("I574-win2/k27_mirror_re1.85_im-1.25", "I574-win2/k27_re1.85_im+1.25"),
          ("I574-win2/k27_mctl_re2.35_im-1.25", "I574-win2/k27_re2.35_im+1.25"),
          ("I574-win2/k27_mctl_re3.35_im-1.25", "I574-win2/k27_re3.35_im+1.25")]


def load(folder):
    f = glob.glob(os.path.join(RAW, folder, "modecount_*_evals.jsonl"))[0]
    return [json.loads(l) for l in open(f)]


mut = "--mutate=arg" in sys.argv
ok = True
for ci, (lo, up) in enumerate(PAIRS):
    L, U = load(lo), load(up)
    if mut and ci == 0:
        L = [dict(r, arg=r["arg"] + 0.5) for r in L]
    Uk = {(round(r["re"], 9), round(r["im"], 9)): r for r in U}
    n, dl, da = 0, 0.0, 0.0
    for r in L:
        u = Uk.get((round(r["re"], 9), round(-r["im"], 9)))
        if u is None:
            continue
        n += 1
        dl = max(dl, abs(r["lnabs"] - u["lnabs"]))
        s = r["arg"] + u["arg"]
        da = max(da, abs(math.remainder(s, 2 * math.pi)))
    good = n >= 5 and dl < 1e-6 and da < 1e-6
    ok &= good
    print(f"{lo.split('/')[1]:<34} vs upper twin: {n:>2} of {len(L):>2} points matched, max |d ln|det|| {dl:.2e}, max |arg sum| {da:.2e}  {'ok' if good else 'FAIL'}")
print("all pairs ok" if ok else "FAIL")
sys.exit(0 if ok else 1)

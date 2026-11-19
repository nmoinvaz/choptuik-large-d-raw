#!/usr/bin/env python3
"""#966: per step (its last attempt) of ks_chain3b's anm_run.log files, what the corrector's evaluations cost and how the projection counter
reads: a, D, chord seconds, trials of 300 s or more, 'elim projections' ladder count, the attempt line's seconds, accepted.
A section is one step's attempts (the a rule's line starts it, a retry after a failed start continues it): a is the last
attempt's, tries counts the re-seeds, the counters are those of the last attempt's elim line.
usage: python3 -I proj966.py CHAIN_OUT [--all]   (without --all only attempts with a ladder projection or a start failure)
       python3 -I proj966.py --selftest [--mutate]"""
import glob, re, sys


def attempts(text):
    L = text.splitlines()
    st = [i for i, l in enumerate(L) if re.match(r"\s+a_rule reseed:", l)] + [len(L)]
    out = []
    for s, e in zip(st, st[1:]):
        sec = L[s:e]
        h = re.search(r"level ([0-9.]+) of the pole line .*: a ([0-9.]+)\s*$", sec[0])
        if not h:
            continue
        tr = [float(m.group(1)) for l in sec for m in [re.search(r"trial lam [0-9.]+: .*, ([0-9.]+) s$", l)] if m]
        ch = [float(m.group(1)) for l in sec for m in [re.search(r"strong chord .*refused, ([0-9.]+) s$", l)] if m]
        el = [re.search(r"'ladder': (\d+), 'failed': (\d+), 'skipped': (\d+)", l) for l in sec if "elim projections" in l]
        al = [re.search(r" (\d+) s$", l) for l in sec if re.match(r"\s+a [0-9.]+ -> D", l)]
        dl = [re.search(r"a [0-9.]+ -> D ([0-9.]+):", l) for l in sec if re.match(r"\s+a [0-9.]+ -> D", l)]
        rs = [re.search(r"\s+a ([0-9.]+): re-seeded", l) for l in sec if re.match(r"\s+a [0-9.]+: re-seeded", l)]
        out.append(dict(a=rs[-1].group(1) if rs else h.group(2), D=dl[-1].group(1) if dl else "-", tries=len(rs), trials=len(tr), slow=sum(t >= 300 for t in tr),
                        chord=ch[0] if ch else 0.0, ladder=int(el[-1].group(1)) if el else None,
                        failed=int(el[-1].group(2)) if el else None, skipped=int(el[-1].group(3)) if el else None,
                        s=int(al[-1].group(1)) if al else None, acc=any("Delta of the saved state" in l for l in sec)))
    return out


def selftest(mutate):
    txt = """  a_rule reseed: x, level 0.0226 of the pole line 1e-38: a 0.7147
    a 0.7147: re-seeded (ok), 230.1 s
    on 0 trial lam 1: max|F| 1e-36; simplified correction / |dz| = 1e-17 (bound 0.750); accepted, 337.4 s
    on 1 trial lam 1: max|F| 1e-36; simplified correction / |dz| = 1e-17 (bound 0.750); accepted, 2.1 s
  on 0: strong chord (4 weak directions), 2 steps after the full first step; theta at its point inf (bound 0.750): refused, 343.08 s
      elim projections {'u0': 0, 'u0q': 0, 'ladder': 2, 'failed': 0, 'skipped': 4}
    a 0.715 -> D 249.4664: predicted |F| 3.3e+25, od 4 steps -> 9.4e+25 (tol 2.3e-20), 1135 s
      Delta of the saved state, its eight parts summed exactly: 1.68
"""
    if mutate:
        txt = txt.replace("337.4 s", "33.7 s")
    a = attempts(txt)[0]
    want = dict(a="0.7147", D="249.4664", tries=1, trials=2, slow=1, chord=343.08, ladder=2, failed=0, skipped=4, s=1135, acc=True)
    bad = {k: (a[k], v) for k, v in want.items() if a[k] != v}
    print("selftest", "FAIL" if bad else "PASS", bad or "")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest("--mutate" in sys.argv)
    allr = "--all" in sys.argv
    print("| leg | D | a | re-seeds | chord s | trials (>=300 s) | ladder | skipped | attempt s | accepted |\n|---|---|---|---|---|---|---|---|---|---|")
    for log in sorted(glob.glob(sys.argv[1] + "/leg*/anm_run.log")):
        for r in attempts(open(log, errors="replace").read()):
            if allr or r["ladder"] or r["failed"] or r["ladder"] is None:
                print(f"| {log.split('/')[-2][:5]} | {r['D']} | {r['a']} | {r['tries']} | {r['chord']:.0f} | {r['trials']} ({r['slow']}) | "
                      f"{'in flight' if r['ladder'] is None else r['ladder']} | {r['skipped']} | {r['s']} | {'yes' if r['acc'] else 'no'} |")

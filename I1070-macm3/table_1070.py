#!/usr/bin/env python3
"""#1070 macm3b: the det table of one run from its log (run_MODE.log) and record (lowD_gamma_D3.15_MMODE.jsonl), every number computed
from the files. Usage: table_1070.py M128 -> table_M128.md. Also lam_guess at D 3.5 against the issue's gamma(3.5) 0.3223855827556097
(#628), read-only, from hp/lowD_gamma.py of the worktree."""
import json, re, sys, os
mode = sys.argv[1]; O = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.expanduser("~/Source/choptuik-large-d-1070/hp"))
import lowD_gamma as g
L = open(f"{O}/run_{mode}.log").read().splitlines()
rows = [(float(m.group(1)), int(float(m.group(2))), float(m.group(3)), m.group(4), float(m.group(5)))
        for l in L if (m := re.match(r"\s+lam (\S+): sign ([+-]\d) ln\|det\| (\S+) pivots (\S+) \(([\d.]+) s\)", l))]
nw = [l.strip() for l in L if l.strip().startswith("newton")]
rec = json.loads(open(f"{O}/lowD_gamma_D3.15_{mode}.jsonl").read().splitlines()[-1])
out = [f"{mode}: D {rec['D']}, M {rec['M']}, F after the polish {rec['F']:.3e}, guess lam {rec['lam_guess']:.9f} (gamma guess {1/rec['lam_guess']:.6f}), "
       f"sign changes {rec['n_signchanges']}, determinants {rec['n_det']}, lam {rec['lam']}, gamma {rec['gamma']}, own seconds {rec['seconds']}", ""]
out += ["polish lines:"] + [f"- {l}" for l in nw] + [""]
out += ["| lam | sign | ln\\|det\\| | pivots | s |", "|---|---|---|---|---|"]
for lam, sg, ld, pv, s in sorted(rows): out.append(f"| {lam:.12f} | {sg:+d} | {ld:.6f} | {pv} | {s:.1f} |")
srt = sorted(rows); lo, hi = srt[0], srt[-1]
sl = [(srt[i + 1][2] - srt[i][2]) / (srt[i + 1][0] - srt[i][0]) for i in range(len(srt) - 1)]
out += ["", f"bracket scanned: lam {lo[0]:.6f} .. {hi[0]:.6f}, gamma {1/hi[0]:.6f} .. {1/lo[0]:.6f}; signs {sorted(set(r[1] for r in rows))}",
        f"d ln|det| / d lam between neighbouring points: min {min(sl):.1f}, max {max(sl):.1f} (ln|det| rises with lam at every pair: {all(s > 0 for s in sl)})",
        f"seconds per determinant: mean {sum(r[4] for r in rows)/len(rows):.1f}, min {min(r[4] for r in rows):.1f}, max {max(r[4] for r in rows):.1f}; sum {sum(r[4] for r in rows):.0f} of the run's {rec['seconds']:.0f} s"]
g35 = 1 / 0.3223855827556097
out += [f"lam_guess(3.5) = {g.lam_guess(3.5):.6f} against 1/gamma(3.5) = {g35:.6f} (#628's M 128 gamma 0.3223855827556097): the guess misses by {g.lam_guess(3.5)-g35:+.6f} at D 3.5"]
open(f"{O}/table_{mode}.md", "w").write("\n".join(out) + "\n"); print("\n".join(out))

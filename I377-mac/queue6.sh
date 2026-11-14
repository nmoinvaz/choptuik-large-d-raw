#!/bin/bash
# I377 queue 6: kappa_c at D = infinity refined from the inner kappa path (css_inner_pert.py kcrit), settings A and B
source ~/venv-314/bin/activate
cd "$(dirname "$0")"
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') kcrit"
nice -n 10 python /Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter/css_inner_pert.py kcrit kpath_inf.jsonl --set=A,B --out=kcrit_inf.jsonl
echo "== exit $?"
# the jump method at D = 4, kappa = 0.0754 (HE97's kappa_c) and 0.076: background and lambda_osc at both radii
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') D = 4 at kappa 0.0754, 0.076"
nice -n 10 python - <<'PY' >> at_D4.jsonl
import sys, json
sys.path.insert(0, "/Users/nathan/Source/choptuik-large-d-xf-kappa/solver/matter")
import css_kappa_crit as kc
c = [json.loads(l) for l in open("crit.jsonl") if '"D": 4.0' in l][0]
for k in (0.0754, 0.076):
    om, f0, xh, aJ = kc.solve_bg(4.0, k, c["omega"], c["f0"])
    (res,) = kc.roots(4.0, k, om, f0, xh, [complex(0.0, c["lam_osc"][1])])
    print(json.dumps(dict(kind="at", D=4.0, kappa=k, omega=om, f0=f0, xh=xh, absJ=aJ,
                          osc=[[q[0], q[1].real, q[1].imag, q[2]] for q in res])), flush=True)
PY
echo "== exit $?"
echo "== done $(date -u '+%Y-%m-%d %H:%M:%S')"

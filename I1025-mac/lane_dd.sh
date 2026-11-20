#!/bin/bash
{
# #1025 route (c) E1/E2 (dd_e1e2_criteria.log, written first). Starts when lane T-a or T-b2 has finished (its signtest included).
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
until grep -q 'T-a done' $R/lane_t_a.log || grep -q 'T-b2 done' $R/lane_t_b2.log; do sleep 60; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') a lane T slot is free"
run 14400 ell_dd.py sens data/sol_l1kc31L1025_D13.0000.npy 13 31 2.6641484641099442,2.7041484641099442 --blocks --out data/ell_dd_sens_1025.jsonl
if /Users/nathan/venv-314/bin/python - <<'PY'
import json, sys
rs = [json.loads(l) for l in open("data/ell_dd_sens_1025.jsonl") if json.loads(l)["D"] == 13.0][-2:]
ok = len(rs) == 2 and all(r["e1_dd_agree"] and r["e1_f64_agree"] and r["e1"][0]["sign_dd"] == r["e1"][0]["sign_f64"] for r in rs)
ok = ok and rs[0]["e1"][0]["sign_dd"] != rs[1]["e1"][0]["sign_dd"]
ok = ok and all(all(s == r["e1"][0]["sign_dd"] for e in r["e2"] for s in e["signs"]) for r in rs)
print(f"control D 13: {'PASS' if ok else 'FAIL'}"); sys.exit(0 if ok else 1)
PY
then
  run 43200 ell_dd.py sens data/sol_l1kc55Fs1025_D17.5000.npy 17.5 55 1.93,1.97 --blocks --out data/ell_dd_sens_1025.jsonl
else
  echo "== CONTROL FAILED at D 13: the D 17.5 run does not start"
fi
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane dd done"
exit
}

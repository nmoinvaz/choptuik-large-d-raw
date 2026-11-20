#!/bin/bash
{
# #1025 route (c) E1b/E2b (dd_e1e2b_criteria.log, written first), in the slot lane dd freed.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
M=/Users/nathan/Source/choptuik-1025/solver/matter
cd $M
run() { local to=$1; shift; echo "== $(date -u '+%Y-%m-%d %H:%M:%S') $*"; timeout $to nice -n 10 /Users/nathan/venv-314/bin/python -u "$@" 2>&1 | grep --line-buffered -v 'Warning\|sl.solve'; rc=${PIPESTATUS[0]}; echo "== exit $rc $(date -u '+%Y-%m-%d %H:%M:%S')"; return $rc; }
ST=data/sol_l1kc55Fs1025_D17.5000.npy; SC=data/ell_dd_scan_1025.jsonl
pick() { /Users/nathan/venv-314/bin/python - "$@" <<'PY'
import json, sys
lo, hi = float(sys.argv[1]), float(sys.argv[2])
rs = [json.loads(l) for l in open("data/ell_dd_scan_1025.jsonl")]
w = sorted({r["lam"] for r in rs if r["D"] == 17.5 and r["kc"] == 55 and not r["agree"] and lo - 1e-9 <= r["lam"] <= hi + 1e-9},
           key=lambda l: abs(l - 1.9522284485089008))[:2]
print(",".join(repr(x) for x in w))
PY
}
run 5400 ell_dd.py scan $ST 17.5 55 1.935,1.94,1.945,1.95,1.955,1.96,1.965 --out $SC
L=$(pick 1.935 1.965)
if [ -z "$L" ]; then
  echo "== no float64 disagreement in 1.935-1.965: the finer scan"
  run 7200 ell_dd.py scan $ST 17.5 55 1.95,1.9505,1.951,1.9515,1.952,1.9525,1.953,1.9535,1.954,1.9545,1.955 --out $SC
  L=$(pick 1.95 1.955)
fi
if [ -z "$L" ]; then
  echo "== no noise window found: stop and report"
else
  echo "== window lambda chosen: $L"
  run 14400 ell_dd.py sens $ST 17.5 55 $L --blocks --out data/ell_dd_sens_1025.jsonl
fi
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane dd2 done"
exit
}

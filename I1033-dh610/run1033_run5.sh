#!/bin/bash
# #1033 run 5 on dh610 (coordinator, 2026-11-20): hp/tau_map_gain.py of perf/tau-map-lowd 32e5825d at D 3.044375.
# Run 0 first (selftest exit 0, its eight controls exit 1; stop otherwise), then run 5's solve, then its report.
# 8 threads, nice 10; each step capped at 3 times its estimate by timeout on its own pid.
set -u
CODE=/home/nathan/Source/choptuik-1033; PY=/home/nathan/Source/venv-ccc/bin/python
RAW=/home/nathan/Source/choptuik-large-d-raw-1033; OUT=$RAW/I1033-dh610
cd "$CODE/hp" || exit 1
[ "$(git rev-parse HEAD)" = 32e5825d2073a9ce5e3281ee79fa690395524bb7 ] || { echo "CODE is not at 32e5825d"; exit 1; }
X=$OUT/exits_1033.txt; st() { date -u '+%F %T'; }
export PYTHONFAULTHANDLER=1
B=$RAW/T100-win2/states/lowDhm_x0.000157-0.975_D3.0444
G="nice -n 10 timeout -s TERM"
echo "# $(st) UTC run 5 start, code $(git rev-parse --short=8 HEAD), $($PY -c 'import sys, hpkernel, numpy, mpmath; print(sys.version.split()[0], "numpy", numpy.__version__, "mpmath", mpmath.__version__, "hpkernel", hpkernel.__file__)'), load $(cut -d' ' -f1-3 /proc/loadavg)" >> $X
# run 0: caps 180 s each (estimate: under a minute)
$G 180 $PY tau_map_gain.py selftest > $OUT/selftest.log 2>&1; s=$?
echo "run 0 selftest exit $s (0)" >> $X
bad=$s
for m in lo parity dps40 inverse gp phase_gp lenient unbound; do
  $G 180 $PY tau_map_gain.py selftest --mutate $m > $OUT/control_$m.log 2>&1; c=$?
  echo "run 0 control $m: exit $c (1)" >> $X
  [ $c = 1 ] || bad=1
done
[ "$s" = 0 ] && [ "$bad" = 0 ] || { echo "# $(st) UTC run 0 failed: stop" >> $X; exit 1; }
# run 5: cap 54000 s (3 x the note's 5 h)
t0=$(date +%s)
$G 54000 $PY tau_map_gain.py solve ${B}_M384.npz --pairs 1:384,1:320,0.5:192,0.5:160,0.4:192,0.4:160 --threads 8 --states $OUT/states --out $OUT/solve_D3.0444.jsonl > $OUT/solve_D3.0444.log 2>&1
r=$?
echo "run 5 solve exit $r wall $(( $(date +%s) - t0 )) s ($(st) UTC)" >> $X
# report: cap 1800 s (estimate: minutes)
$G 1800 $PY tau_map_gain.py report $OUT/solve_D3.0444.jsonl --ref ${B}_M384.npz --ref2 ${B}_M320.npz --cost $RAW/I1033-win2/cost2.jsonl --json $OUT/report_D3.0444.json > $OUT/report_D3.0444.txt 2>&1
echo "run 5 report exit $? ($(st) UTC)" >> $X
# the report's control (notes/LOW_D_SPEEDUP.md, check 4): every stored Delta moved by 1e-10, must exit 1
$G 1800 $PY tau_map_gain.py report $OUT/solve_D3.0444.jsonl --ref ${B}_M384.npz --ref2 ${B}_M320.npz --cost $RAW/I1033-win2/cost2.jsonl --mutate delta > $OUT/report_control_delta.txt 2>&1
echo "run 5 report --mutate delta: exit $? (1)" >> $X
echo "end $(st) UTC" >> $X

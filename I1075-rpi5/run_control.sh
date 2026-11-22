#!/bin/bash
# #1075 steps 0 and 1 (t5's order, 2026-11-22): the imports, then the control: d18_hybsign.py (e089207a, unmodified) on dh370's k_c 79 D 19.125 state and record at
# lambda 1.50, one process of 3 threads at nice 10, 4 h cap by exact pid; it must print the record system and dh370's hybrid sign and ln|det| to 1e-9 relative
# (dh170's control_check_k79.py). Run as a systemd user unit. usage: run_control.sh [dry]
{
set -u
MODE=${1:-}
F=/home/nathan/Source/choptuik-large-d-raw/I1075-rpi5          # live folder
RAWSRC=/home/nathan/Source/choptuik-large-d-raw-964            # origin/main snapshot the inputs come from
PY=/home/nathan/Source/venv-1025/bin/python
WT=/home/nathan/Source/choptuik-large-d-1075; W=$WT/solver/matter
L=$F/exits_control.txt
export OPENBLAS_NUM_THREADS=3 OMP_NUM_THREADS=3 VECLIB_MAXIMUM_THREADS=3 MKL_NUM_THREADS=3 RAYON_NUM_THREADS=3 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC control: $*" | tee -a $L; }
mkdir -p $F/in $F/control
declare -A PIN=(
  [I1025-dh370/kc79_d19125/sol_l1kc79dh370_D19.1250.npy]=3ff3fcb5
  [I1025-dh370/kc79_d19125/l1kc79dh370.jsonl]=15ac964f
  [I1025-mac/d18/d18_hybsign.py]=e089207a
  [I1025-dh170/kc79_d19125low/in/control_check_k79.py]=484801fd )
bad=0
for p in "${!PIN[@]}"; do
  b=$(basename $p)
  [ "$(git hash-object --no-filters $RAWSRC/$p | cut -c1-8)" = "${PIN[$p]}" ] || { say "refuse: $p is not blob ${PIN[$p]}"; bad=1; continue; }
  cp $RAWSRC/$p $F/in/$b
done
cp $RAWSRC/I1025-dh370/kc79_d19125/scan/scan_D19.125_1025.jsonl $F/in/ref_dh370_scan_D19.125_1025.jsonl
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $F/control/scan_D19.125_p0.jsonl $F/control/control.raw; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
[ $bad = 0 ] || exit 2
say "pins checked, worktree 505d8399 clean; python $($PY -V 2>&1); 3 threads"
# step 0: the imports
(cd $W && $PY -I - <<PYEOF
import sys
sys.path.insert(0, "$W")
import numpy, scipy, mpmath, multidouble
import importlib.metadata as im
print("numpy", numpy.__version__, "scipy", scipy.__version__, "mpmath", mpmath.__version__, "multidouble", im.version("multidouble"), "isa", multidouble.isa())
multidouble.dd_logdet
import dss_ell, ell_ddm, ell_delta
print("dss_ell, ell_ddm, ell_delta import")
t = ell_delta.lam0_table()
for D in (19.0, 19.125, 19.5, 20.0):
    print("lam0_at", D, "%.10f" % ell_delta.lam0_at(D, *t)[0])
PYEOF
) > $F/imports.txt 2>&1; i0=$?
say "imports exit $i0 (0 wanted): $(tail -2 $F/imports.txt | tr '\n' ' ')"
[ $i0 = 0 ] || exit 3
(cd $W && $PY -I ell_refine.py -h > $F/imports_ell_refine_h.txt 2>&1); i1=$?
say "ell_refine.py -h (argparse at import; imports dss_ell) exit $i1 (0 wanted)"
[ $i1 = 0 ] || exit 3
$PY -I $F/in/control_check_k79.py selftest > $F/control/selftest_control_check.txt 2>&1; s0=$?
$PY -I $F/in/control_check_k79.py selftest --mutate > $F/control/selftest_control_check_mutate.txt 2>&1; s1=$?
say "control_check selftest exit $s0 (0 wanted), --mutate exit $s1 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] || { say "STOP: the control checker's selftest or mutation did not read as written"; exit 4; }
[ "$MODE" = dry ] && { say "dry run: stop here"; exit 0; }
s0=$(date +%s)
nice -n 10 /usr/bin/time -v $PY -u $F/in/d18_hybsign.py $F/in/l1kc79dh370.jsonl $F/in/sol_l1kc79dh370_D19.1250.npy 19.125 1.50 $F/control/scan_D19.125_p0.jsonl < /dev/null > $F/control/control.raw 2>&1 &
tp=$!; say "control started under /usr/bin/time pid $tp (lambda 1.50, D 19.125, k_c 79)"
while kill -0 $tp 2>/dev/null; do
  if [ $(( $(date +%s) - s0 )) -gt 14400 ]; then py=$(ps -o pid= --ppid $tp | head -1 | tr -d ' '); say "4 h cap reached: TERM to python pid $py and time pid $tp"; kill -TERM $py $tp 2>/dev/null; break; fi
  py=$(pgrep -P $tp | head -1)
  [ -n "$py" ] && [ -d /proc/$py ] && echo "$(date -u '+%T') MemAvailable $(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo) MiB, python pid $py RSS $(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status) MiB, cputime $(ps -o cputime= -p $py | tr -d ' ')" >> $F/control/samples.txt
  sleep 30
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $F/control/control.raw > $F/control/control.log
say "control scan exit $r, $(( $(date +%s) - s0 )) s wall"
$PY -I $F/in/control_check_k79.py $F/control/control.log $F/control/scan_D19.125_p0.jsonl $F/in/ref_dh370_scan_D19.125_1025.jsonl 1.50 > $F/control/control_check.txt 2>&1; c=$?
cut -c1-500 $F/control/control_check.txt | tee -a $L
[ $c = 0 ] && say "CONTROL PASS" || say "CONTROL FAIL (control_check exit $c, scan exit $r)"
exit 0
}

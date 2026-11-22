#!/bin/bash
{
# #1025 k_c break bisection, step 1: the k_c state at D 18.46875 by ell_leap.py, from the two nearest accepted states below it (D 18.375 and
# D 18.4375, the Mac's leap states), flags as the Mac's leaps (--tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold), h 0.03125 (one step, the secant
# predictor over the seeds' spacing 0.0625). usage: leap_kcbreak_dh170.sh 63|55 [dry]. 4 threads, nice 10, 3 h cap by exact pid.
# Acceptance: ell_leap's own bars (|F| < 1e-8, psi-constraint <= 1e-2, no failed solve), then accept_check.py (the record-system check of
# d18_hybsign.py alone) on the new state and its record row, with its planted pass and mismatch controls run first (they take seconds).
set -u
KC=${1:?63 or 55}; MODE=${2:-}
D=/home/nathan/Source/choptuik-large-d-raw-p4/I1025-dh170/kc_break_D18.46875; I=/home/nathan/scratch1025kc/in2; I1=/home/nathan/scratch1025kc/in
PY=/home/nathan/Source/choptuik-large-d-1058b/.venv/bin/python; WT=/home/nathan/Source/choptuik-large-d-1025leap; W=$WT/solver/matter
case $KC in
  63) TAG=l1kc63dh1025; SA=$I/sol_l1kc63Wm1025_D18.375000.npy; SAH=aa04459266643be3dfd46c2d83c52f556ed6254c
      SB=$I/sol_l1kc63Wm1025_D18.437500.npy; SBH=16a17e5f6c93ffc425c71e1e2d9a2cab42c4827d;;
  55) TAG=l1kc55dh1025; SA=$I/sol_l1kc55F1025_D18.375000.npy; SAH=6a1df3d65f5baa6611feaea06cf8fa631cadea21
      SB=$I/sol_l1kc55F1025_D18.437500.npy; SBH=2b8864095ed78a4a9d7999d6f9bc26114e64ed65;;
  *) echo "usage: $0 63|55 [dry]"; exit 9;;
esac
L=$D/exits_leap_kc$KC.txt; RAW=$D/leap_kc$KC.raw; LOG=$D/leap_kc$KC.log; STN=sol_${TAG}_D18.468750.npy
export OPENBLAS_NUM_THREADS=4 OMP_NUM_THREADS=4 VECLIB_MAXIMUM_THREADS=4 MKL_NUM_THREADS=4 RAYON_NUM_THREADS=4 P4_WT_MATTER=$W
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC k_c $KC: $*" | tee -a $L; }
hb() { git hash-object --no-filters "$1"; }
bad=0
for pb in "$SA $SAH" "$SB $SBH" "$W/ell_leap.py 1eb873e49348f400d9d0dfc1cd95be5761473d0c" "$D/accept_check.py $(hb $D/accept_check.py)"; do
  set -- $pb
  [ -f $1 ] && [ "$(hb $1)" = "$2" ] || { say "refuse: $1 missing or not blob $2"; bad=1; }
done
[ "$(git -C $WT rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C $WT status --short)" ] || { say "refuse: worktree $WT is not clean at 505d8399"; bad=1; }
for f in $W/data/$TAG.jsonl $W/data/$STN $RAW $LOG $D/$TAG.jsonl $D/$STN; do [ -e $f ] && { say "refuse: $f exists"; bad=1; }; done
$PY -c "import numpy, scipy, multidouble" || { say "refuse: $PY lacks numpy/scipy/multidouble"; bad=1; }
[ $bad = 0 ] || exit 2
say "pins checked: seeds D 18.375 $SAH and D 18.4375 $SBH, ell_leap 1eb873e4, worktree 505d8399 clean; $PY; 4 threads"
[ "$MODE" = dry ] && { say "dry run: pins ok, nothing started"; exit 0; }
cd $W
say "1. planted control: ell_ddm.py selftest (must PASS), then --mutate=slices (must FAIL), 1800 s each"
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest < /dev/null > $D/ell_ddm_selftest_leap_kc$KC.log 2>&1; r1=$?
timeout 1800 nice -n 10 $PY -u ell_ddm.py selftest --mutate=slices < /dev/null >> $D/ell_ddm_selftest_leap_kc$KC.log 2>&1; r2=$?
grep -E '^selftest:' $D/ell_ddm_selftest_leap_kc$KC.log | tee -a $L
[ $r1 = 0 ] && [ $r2 = 1 ] || { say "STOP: the planted control did not behave (selftest exit $r1, --mutate=slices exit $r2)"; exit; }
say "2. accept_check.py controls on the D 18.4375 state: its own record row must give exit 0, the D 18.5 row exit 3"
case $KC in 63) R1=$I1/l1kc63Wm1025.jsonl;; 55) R1=$I1/l1kc55F1025.jsonl;; esac
nice -n 10 $PY -W ignore $D/accept_check.py $R1 $SB 18.4375 > $D/ctl_leap_accept_kc$KC.log 2>&1; c1=$?
nice -n 10 $PY -W ignore $D/accept_check.py $R1 $SB 18.5 >> $D/ctl_leap_accept_kc$KC.log 2>&1; c2=$?
tail -n 2 $D/ctl_leap_accept_kc$KC.log | cut -c1-200 | tee -a $L
[ $c1 = 0 ] && [ $c2 = 3 ] || { say "STOP: the acceptance control did not behave (own row exit $c1, D 18.5 row exit $c2)"; exit; }
say "3. leap: ell_leap.py $TAG 1 $KC D 18.375, 18.4375 -> 18.46875, h 0.03125 (3 h cap by exact pid)"
s0=$(date +%s)
nice -n 10 /usr/bin/time -v timeout 10800 $PY -u ell_leap.py $TAG 1 $KC $SA 18.375 $SB 18.4375 18.46875 0.03125 --tol 1e-12 --fmax 1e-8 --cmax 1e-2 --fold \
  < /dev/null > $RAW 2>&1 &
tp=$!; echo $tp > $D/time_pid_leap_kc$KC.txt; say "leap started under /usr/bin/time pid $tp"
n=0
while kill -0 $tp 2>/dev/null; do
  if [ $((n % 3)) = 0 ]; then
    py=$(pgrep -P $(pgrep -P $tp | head -1) | head -1)
    av=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
    if [ -n "$py" ] && [ -d /proc/$py ]; then rss=$(awk '/VmRSS/ {print int($2/1024)}' /proc/$py/status); ni=$(ps -o ni= -p $py | tr -d ' '); cpu=$(ps -o cputime= -p $py | tr -d ' '); else rss=0; ni=-; cpu=-; fi
    echo "$(date -u '+%T') k_c $KC MemAvailable $av MiB, python pid ${py:-none} RSS $rss MiB, cputime $cpu, nice $ni" >> $D/memlog_leap_kc$KC.log
    [ "$av" -lt 2048 ] && echo "ALERT $(date -u '+%F %T') UTC k_c $KC leap: MemAvailable $av MiB (alert only, nothing stopped)" >> $D/alert_leap.log
  fi
  n=$((n+1)); sleep 10
done
wait $tp; r=$?
grep -vE 'Warning|^  [a-z]+ = |slogdet' $RAW | grep -E '^\{|^reached|^stop|^failed|^fold watch|Traceback|Error' | sed -E 's/"(sv_J_small|cos_t_v|sv_reg_small|cos_t_reg)": \[[^]]*\], //g' > $LOG
say "leap exit $r (timeout 124), $(( $(date +%s) - s0 )) s wall"
grep -E '^(reached|stop|failed|fold watch)' $LOG | tee -a $L
[ $r = 0 ] && grep -q '^reached D 18.46875' $LOG && [ -f $W/data/$STN ] && [ -f $W/data/$TAG.jsonl ] || { say "STOP: the leap did not reach D 18.46875"; exit; }
cp $W/data/$TAG.jsonl $W/data/$STN $D/ && [ "$(hb $W/data/$STN)" = "$(hb $D/$STN)" ] && [ "$(hb $W/data/$TAG.jsonl)" = "$(hb $D/$TAG.jsonl)" ] || { say "STOP: copy into the folder failed"; exit; }
say "state $STN blob $(hb $D/$STN); record $TAG.jsonl blob $(hb $D/$TAG.jsonl)"
nice -n 10 $PY -W ignore $D/accept_check.py $D/$TAG.jsonl $D/$STN 18.46875 > $D/accept_kc$KC.log 2>&1; ca=$?
cat $D/accept_kc$KC.log | cut -c1-220 | tee -a $L
if [ $ca = 0 ]; then
  echo "$KC $(hb $D/$STN) $(hb $D/$TAG.jsonl)" > $D/pins_kc$KC.txt
  say "ACCEPTED: state D 18.46875 accepted (leap bars met, the record-system check passed, exit $ca)"
else
  say "STOP: NOT ACCEPTED (the record-system check exit $ca)"; exit
fi
say "lane leap kc$KC done"
exit
}

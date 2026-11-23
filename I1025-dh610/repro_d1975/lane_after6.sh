#!/bin/bash
# #1025 repro_d1975 (dh610), after the 6-thread ell_refine run (lane_refine6.sh, state l1kc87linRe6): the coordinator's order: (info) the k_c 87 check on the new state with its two controls; ell_cond.py (branch wip/ell-cond, worktree
# ~/Source/choptuik-large-d-1025h at ee2c1dbd, ell_cond.py blob 1bb7b995) with its plant control first (--mutate=plant on (linRe, linRe6), exit 0 and "plant check: PASS", else the lane stops and nothing else runs), then at the same
# time ell_cond on (A = linRe, B = linRe6) with 6 threads and d18_hybsign.py (e089207a, unmodified) on linRe6 at 1.32 and 1.33 (2 processes of 1 thread, nice 10, each printing the record system), then repro_read.py into summary_repro.txt.
# A bit-for-bit comparison of the two states (numpy array_equal and the blobs) is logged first. Free memory: refuses to start the d18 and ell_cond runs with less than 2 x 2.5 GB + 6 GB + 4 GB available; nothing is stopped or
# terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt. usage: bash lane_after6.sh
{
set -u
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/repro_d1975; IN=$F/in; C=$F/cond; S=$F/scan
WTC=/home/nathan/Source/choptuik-large-d-1025h; WC=$WTC/solver/matter; WTM=/home/nathan/Source/choptuik-large-d-1025g/solver/matter
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=19.75; L=$F/exits_repro.txt; MEMSTOP=4194304
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC repro_d1975: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $C $S
say "waiting for ref6/DONE.txt (6 h cap)"
tw=$(date +%s)
while true; do
  a=$(head -1 $F/ref6/DONE.txt 2>/dev/null)
  case "$a" in *REFUSED*) say "STOP: the ell_refine lane was refused ($a)"; exit 1;; esac
  [ "${a:0:4}" = DONE ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || { say "STOP: the wait of 6 h ended"; exit 1; }
  sleep 60
done
say "the 6-thread ell_refine run is done: $a"
LIN=$IN/sol_l1kc87linRe_D19.7500.npy; L6=$IN/sol_l1kc87linRe6_D19.7500.npy
while read bb f; do [ -f $IN/$f ] && [ "$(blob $IN/$f)" = "$bb" ] || { say "STOP: $IN/$f missing or not blob $bb"; exit 1; }; done < <(cat $F/in_blobs.txt $F/in_blobs_refine6.txt)
[ "$(blob $WC/ell_cond.py | cut -c1-8)" = 1bb7b995 ] || { say "STOP: ell_cond.py is not blob 1bb7b995"; exit 1; }
[ "$(git -C $WTC rev-parse --short=8 HEAD)" = ee2c1dbd ] && [ -z "$(git -C $WTC status --short)" ] || { say "STOP: worktree $WTC is not clean at ee2c1dbd"; exit 1; }
[ "$(git -C /home/nathan/Source/choptuik-large-d-1025f rev-parse HEAD)" = 505d839940456a3d04321d75cf66cc3b5bc831c4 ] && [ -z "$(git -C /home/nathan/Source/choptuik-large-d-1025f status --short)" ] || { say "STOP: worktree 1025f is not clean at 505d8399"; exit 1; }
( cd $IN && $PY -I repro_read.py selftest > $F/selftest_repro_read.log 2>&1; r0=$?; $PY -I repro_read.py selftest --mutate > $F/selftest_repro_read_mutate.log 2>&1; r1=$?; echo "$r0 $r1" > $F/selftest_exits_repro.txt )
read r0 r1 < $F/selftest_exits_repro.txt
[ $r0 = 0 ] && [ $r1 = 1 ] || { say "STOP: the repro_read selftests did not behave (exits $r0 $r1; wanted 0 1)"; exit 1; }
eq=$($PY -I -c "import numpy as np; a, b = np.load('$LIN'), np.load('$L6'); print(bool(np.array_equal(a, b)), 'entries differing', int(np.count_nonzero(a - b)), 'norm', float(np.linalg.norm(a - b)))")
say "the two states (8 threads, 6 threads): array_equal and difference: $eq; blobs $(blob $LIN | cut -c1-8) and $(blob $L6 | cut -c1-8)"
# info: the k_c 87 check on the new state, with its controls
CK="nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $IN/l1kc87linRe6.jsonl $L6 $D $WTM"
$CK > $F/syscheck_linRe6.txt 2>&1; c0=$?; $CK --mutate=F > $F/syscheck_linRe6_mutF.txt 2>&1; c1=$?; $CK --mutate=steps > $F/syscheck_linRe6_mutsteps.txt 2>&1; c2=$?
say "info: kc87_syscheck_1025.py on l1kc87linRe6: exit $c0; controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each)"
# ell_cond: its control first
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
EC="nice -n 10 $PY -u ell_cond.py"
say "ell_cond control: --mutate=plant on (linRe, linRe6), 8 threads"
( cd $WC && $EC $LIN $L6 87 1 $D --kappa 0.7 --Ks 30 --u0 0.04 --mutate=plant --out $C/f_plant.json ) > $C/plant.txt 2>&1; rp=$?
say "ell_cond control exit $rp ($(grep 'plant check' $C/plant.txt | cut -c1-120))"
if [ $rp != 0 ] || ! grep -q 'plant check: PASS' $C/plant.txt; then say "STOP: the ell_cond control did not exit 0 with PASS; nothing else is run"; exit 1; fi
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
[ "$av" -ge $(( 2 * 2500000 + 6000000 + 4000000 )) ] || { say "STOP: MemAvailable $av kB is below 2 x 2.5 GB + 6 GB + 4 GB"; exit 1; }
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
say "ell_cond (A = linRe, B = linRe6), 6 threads, and d18_hybsign.py on linRe6 at 1.32 and 1.33, 2 processes of 1 thread, nice 10, at the same time"
pc=()
( cd $WC && OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 $EC $LIN $L6 87 1 $D --kappa 0.7 --Ks 30 --u0 0.04 --out $C/f_lin_lin6.json > $C/lin_lin6.txt 2>&1; echo "$(date -u '+%F %T') UTC ell_cond lin_lin6 exit $?" >> $L ) & pc+=($!)
j=0
for lam in 1.32 1.33; do
  ( cd $W && nice -n 10 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $IN/l1kc87linRe6.jsonl $L6 $D $lam $S/repro_D19.75_p$j.jsonl < /dev/null > $S/repro_p$j.raw 2>&1
    echo "$(date -u '+%F %T') UTC d18 $lam exit $?" >> $L ) & pc+=($!)
  j=$((j + 1))
done
( sleep 10; while pgrep -f 'ell_cond.py.*linRe6|d18_hybsign.py.*linRe6' > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'ell_cond.py.*linRe6|d18_hybsign.py.*linRe6' | wc -l), MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg)" >> $S/sampler_repro.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $F/MEMALERT_after.txt
    sleep 30
  done ) &
wait "${pc[@]}"
for j in 0 1; do grep -vE 'Warning|^  [a-z]+ = |slogdet' $S/repro_p$j.raw > $S/repro_p$j.log; say "d18 p$j: $(grep -E 'record system' $S/repro_p$j.log | head -1 | cut -c1-140)"; done
cd $IN && $PY -I repro_read.py read $LIN $L6 $IN/l1kc87linRe.jsonl $IN/l1kc87linRe6.jsonl $C/f_lin_lin6.json $S/repro_D19.75_p0.jsonl $S/repro_D19.75_p1.jsonl $IN/ref_linRe_D19.75_1.32.jsonl $IN/ref_linRe_D19.75_1.33.jsonl > $F/summary_repro.txt 2>&1
say "all runs done; the reading is in summary_repro.txt; repro done"
exit 0
}

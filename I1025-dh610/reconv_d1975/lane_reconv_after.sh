#!/bin/bash
# #1025 reconv_d1975 (dh610), steps 3 and 4 of the coordinator's re-convergence test of 23 Nov. Waits for both ell_refine runs (lin/DONE.txt and mac/DONE.txt, both "DONE exit 0"; stops if either is REFUSED), then:
#  info: kc87_syscheck_1025.py on both re-converged states (its record and state), with its two controls (they must exit 1).
#  step 3: solver/matter/ell_cond.py from branch wip/ell-cond (ee2c1dbd, worktree ~/Source/choptuik-large-d-1025h, no changes; blob 1bb7b995): first its control --mutate=plant once on (linRe, macRe), which must exit 0
#          and print "plant check: PASS" (a failing control stops the work), then, at the same time, (linRe, macRe), (dh170's start state, linRe) and (macm3's start state, macRe), each
#          "STATE_A STATE_B 87 1 19.75 --kappa 0.7 --Ks 30 --u0 0.04 --out f.json", 6 threads each, nice 10. (ell_cond builds dss_ell.DSSEll as ell_refine.py does; the branch's dss_ell.py and the regrid worktree's differ only
#          in mode_matrix_c and svd_robust, which ell_cond does not use; its |F(A)| at each start state is printed beside the record's |F| as a check.)
#  step 4: only if |dz| between linRe and macRe (the "dz" of cond/f_lin_mac.json: the L2 norm of B - A, Delta entry included) is below 1e-7: d18_hybsign.py (e089207a, unmodified) on both re-converged states at
#          lambda 1.32, 1.33, 1.34: 6 processes of 1 thread, nice 10, each printing the record system. Otherwise it writes "STEP 4 NOT RUN" with the |dz| and ends.
# Free memory: refuses a start of step 4 with less than 6 x 4 GB + 4 GB available; nothing is stopped or terminated for memory (Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes MEMALERT.txt.
{
set -u
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/reconv_d1975; IN=$F/in; C=$F/cond; S=$F/scan
WTC=/home/nathan/Source/choptuik-large-d-1025h; WC=$WTC/solver/matter; WTM=/home/nathan/Source/choptuik-large-d-1025g/solver/matter
WT=/home/nathan/Source/choptuik-large-d-1025f; W=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
D=19.75; L=$F/exits_reconv.txt; MEMSTOP=4194304
export PYTHONDONTWRITEBYTECODE=1
say() { echo "== $(date -u '+%Y-%m-%d %H:%M:%S') UTC reconv_d1975: $*" | tee -a $L; }
blob() { git hash-object --no-filters "$1"; }
mkdir -p $C $S
say "waiting for lin/DONE.txt and mac/DONE.txt (6 h cap)"
tw=$(date +%s)
while true; do
  a=$(head -1 $F/lin/DONE.txt 2>/dev/null); b=$(head -1 $F/mac/DONE.txt 2>/dev/null)
  case "$a$b" in *REFUSED*) say "STOP: an ell_refine lane was refused (lin: $a; mac: $b)"; exit 1;; esac
  [ "${a:0:4}" = DONE ] && [ "${b:0:4}" = DONE ] && break
  [ $(( $(date +%s) - tw )) -lt 21600 ] || { say "STOP: the wait of 6 h ended"; exit 1; }
  sleep 60
done
say "both ell_refine runs are done: lin: $a; mac: $b"
LIN=$IN/sol_l1kc87linRe_D19.7500.npy; MAC=$IN/sol_l1kc87macRe_D19.7500.npy
DH=$IN/sol_l1kc87dh170d1975_D19.7500.npy; MM=$IN/sol_l1kc87macm3d1975_D19.7500.npy
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" "$IN/kc87_syscheck_1025.py 6df5d9600edebeae8cc4e602025e42e79925b7d6" "$WC/ell_cond.py 1bb7b9959bbae0196f81ce581feb60b29f1e4818"; do
  set -- $pb; [ -f $1 ] && [ "$(blob $1)" = "$2" ] || { say "STOP: $1 missing or not blob $2"; exit 1; }
done
[ "$(git -C $WTC rev-parse --short=8 HEAD)" = ee2c1dbd ] && [ -z "$(git -C $WTC status --short)" ] || { say "STOP: worktree $WTC is not clean at ee2c1dbd"; exit 1; }
while read bb f; do [ "$(blob $IN/$f)" = "$bb" ] || { say "STOP: $IN/$f is not blob $bb"; exit 1; }; done < <(cat $F/in_blobs_reconv_lin.txt $F/in_blobs_reconv_mac.txt)
# info: the k_c 87 check on both re-converged states (its record and state), with its controls
for t in lin mac; do
  case $t in lin) TG=l1kc87linRe;; mac) TG=l1kc87macRe;; esac
  CK="nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $IN/$TG.jsonl $IN/sol_${TG}_D19.7500.npy $D $WTM"
  $CK > $F/syscheck_$t.txt 2>&1; c0=$?; $CK --mutate=F > $F/syscheck_${t}_mutF.txt 2>&1; c1=$?; $CK --mutate=steps > $F/syscheck_${t}_mutsteps.txt 2>&1; c2=$?
  say "info: kc87_syscheck_1025.py on $TG: exit $c0; controls --mutate=F exit $c1, --mutate=steps exit $c2 (1 wanted each)"
done
# step 3: ell_cond; its control first
export OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
EC="nice -n 10 $PY -u ell_cond.py"
say "ell_cond control: --mutate=plant on (linRe, macRe), 8 threads"
( cd $WC && $EC $LIN $MAC 87 1 $D --kappa 0.7 --Ks 30 --u0 0.04 --mutate=plant --out $C/f_plant.json ) > $C/plant.txt 2>&1; rp=$?
say "ell_cond control exit $rp ($(grep 'plant check' $C/plant.txt | cut -c1-120))"
if [ $rp != 0 ] || ! grep -q 'plant check: PASS' $C/plant.txt; then say "STOP: the ell_cond control did not exit 0 with PASS; nothing else is run"; exit 1; fi
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6
say "ell_cond: (linRe, macRe), (dh170 start, linRe), (macm3 start, macRe), at the same time, 6 threads each"
pc=()
( cd $WC && $EC $LIN $MAC 87 1 $D --kappa 0.7 --Ks 30 --u0 0.04 --out $C/f_lin_mac.json > $C/lin_mac.txt 2>&1; echo "$(date -u '+%F %T') UTC ell_cond lin_mac exit $?" >> $L ) & pc+=($!)
( cd $WC && $EC $DH $LIN 87 1 $D --kappa 0.7 --Ks 30 --u0 0.04 --out $C/f_dh170_lin.json > $C/dh170_lin.txt 2>&1; echo "$(date -u '+%F %T') UTC ell_cond dh170_lin exit $?" >> $L ) & pc+=($!)
( cd $WC && $EC $MM $MAC 87 1 $D --kappa 0.7 --Ks 30 --u0 0.04 --out $C/f_macm3_mac.json > $C/macm3_mac.txt 2>&1; echo "$(date -u '+%F %T') UTC ell_cond macm3_mac exit $?" >> $L ) & pc+=($!)
wait "${pc[@]}"
say "ell_cond runs done"
dz=$($PY -I -c "import json; print(repr(json.load(open('$C/f_lin_mac.json'))['dz']))" 2>/dev/null)
[ -n "$dz" ] || { say "STOP: no dz in cond/f_lin_mac.json"; exit 1; }
ok=$($PY -I -c "print(1 if $dz < 1e-7 else 0)")
say "|dz| between linRe and macRe: $dz (step 4 only if below 1e-7)"
if [ "$ok" != 1 ]; then echo "STEP 4 NOT RUN: |dz| between linRe and macRe is $dz, not below 1e-7" > $F/STEP4.txt; say "STEP 4 NOT RUN: |dz| $dz is not below 1e-7; reconv done"; exit 0; fi
# step 4: d18_hybsign on both
av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
if [ "$av" -lt $(( 6 * 4000000 + 4000000 )) ]; then say "STOP: step 4 refused to start: MemAvailable $av kB below 6 x 4 GB + 4 GB"; exit 1; fi
export OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 RAYON_NUM_THREADS=1 P4_WT_MATTER=$W
cd $W
say "step 4: d18_hybsign.py on linRe and macRe at 1.32, 1.33, 1.34: 6 processes of 1 thread, nice 10, cap 28800 s each by exact pid"
pids=()
for t in lin mac; do
  case $t in lin) TG=l1kc87linRe;; mac) TG=l1kc87macRe;; esac
  for lam in 1.32 1.33 1.34; do
    ( nice -n 10 /usr/bin/time -v timeout -s TERM 28800 $PY -u $IN/d18_hybsign.py $IN/$TG.jsonl $IN/sol_${TG}_D19.7500.npy $D $lam $S/rc_${t}_D19.75_$lam.jsonl < /dev/null > $S/rc_${t}_$lam.raw 2>&1
      echo "$(date -u '+%F %T') UTC step 4 $t $lam exit $?" >> $L ) &
    pids+=($!)
  done
done
( while pgrep -f 'd18_hybsign.py.*reconv_d1975' > /dev/null; do
    avs=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    echo "$(date -u '+%F %T') UTC alive $(pgrep -f 'd18_hybsign.py.*reconv_d1975' | wc -l) python, MemAvailable_kB $avs, load $(cut -d' ' -f1 /proc/loadavg), points $(cat $S/rc_*_D19.75_*.jsonl 2>/dev/null | wc -l)" >> $S/sampler.log
    [ "$avs" -lt $MEMSTOP ] && echo "$(date -u '+%F %T') UTC MemAvailable $avs kB below 4 GiB (alert only; nothing is stopped)" >> $S/MEMALERT.txt
    sleep 30
  done ) &
wait "${pids[@]}"
for f in $S/rc_*_*.raw; do echo "== $f"; grep -vE 'Warning|^  [a-z]+ = |slogdet' $f | head -1 | cut -c1-200; done | tee -a $L
cat $S/rc_*_D19.75_*.jsonl > $S/rc_all_rows.jsonl
say "step 4 done; reconv done"
exit 0
}

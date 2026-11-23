#!/bin/bash
# #1025 kc95_d195 (dh610), step 1 of the coordinator's order of 23 Nov: my accepted k_c 87 D 19.5 state (raw I1025-dh610/kc87_d195/, a373049a: state 57f8e2d3, record 64b8db7c) regridded to k_c 95 with ell_refine.py as
# the k_c 87 regrid (../kc87_d195/lane_kc87_regrid.sh: worktree 48c36355, `--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, lambda_0(19.5) = 2.1132623525 from ell_delta.lam0_at). The source is checked first with
# kc87_syscheck_1025.py (must accept, both controls refuse); the result is accepted only by kc95_syscheck_1025.py (the k_c 87 check with the k_c test changed to 95, its message and the selftest's planted record, nothing else,
# kc95_syscheck_1025.diff), its selftest and both controls (must refuse), and the k_c 87 check must refuse the result. 8 threads, nice 10, cap 21600 s, a systemd unit (i1025t). Free memory: the lane refuses to start with
# less than 8 GiB available; nothing is stopped or terminated for memory (the coordinator's correction of 23 Nov, Nathan's rule of 2026-11-08): below 4 GiB the sampler only writes regrid/MEMALERT.txt, which the runner
# session posts to the coordinator. Steps and verdicts go to regrid/steps.txt and regrid/VERDICT.txt. usage: bash lane_kc95_regrid.sh [dry]
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc95_d195; IN=$F/in; OUT=$F/regrid
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
SRC=l1kc87dh610d195; TAG=l1kc95dh610d195; D=19.5; LAM0=2.1132623525; MEMSTOP=4194304; MEMSTART=8388608
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
mkdir -p $OUT
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
av0=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
step "start (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $av0 kB)"
[ "$av0" -ge $MEMSTART ] || stop "MemAvailable $av0 kB is below 8 GiB"
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" \
          "$IN/sol_l1kc87dh610d195_D19.5000.npy 57f8e2d3653e4e7f1c5ecc1a9f9d972f396bbd19" "$IN/l1kc87dh610d195.jsonl 64b8db7ca087f452a3825e90e39c2663fbe67623" \
          "$IN/kc87_syscheck_1025.py 6df5d9600edebeae8cc4e602025e42e79925b7d6" "$IN/kc95_syscheck_1025.py d487e628f61d1accae8e09f7d1ad438c1d787883" \
          "$IN/read_lower.py 89309d3c8e4f758bb5f936f7d24796b594e4cbdb" "$IN/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" \
          "$IN/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$IN/repeat_check.py aaf598a98c05d8d67f740b5a3b0675b422daad6a"; do
  set -- $pb
  [ -f $1 ] && [ "$(blob $1)" = "$2" ] || stop "$1 missing or not blob $2"
done
# the k_c 95 check differs from the k_c 87 check in the k_c test only (the diff is in the folder and is rebuilt here)
diff -u $IN/kc87_syscheck_1025.py $IN/kc95_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
tail -n +3 $F/kc95_syscheck_1025.diff | cmp -s - $OUT/diff_rebuilt.txt || stop "kc95_syscheck_1025.diff is not the diff of the two checks"
[ "$(grep -c '^[-+][^-+]' $OUT/diff_rebuilt.txt)" = 6 ] || stop "the diff of the two checks is not three changed lines"
[ "$(git -C $WT rev-parse --short=8 HEAD)" = 48c36355 ] || stop "worktree not at 48c36355"
for f in dss_ell ell_ddm ell_dd ddnp; do git -C $WT diff --quiet 505d8399 HEAD -- solver/matter/$f.py || stop "$f.py differs from 505d8399"; done
[ "$(blob $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
[ -e $WTM/data/$TAG.jsonl ] && stop "$WTM/data/$TAG.jsonl exists"
L0=$($PY -c "import sys; sys.path.insert(0, '$WTM'); import ell_delta; print(round(ell_delta.lam0_at($D, *ell_delta.lam0_table())[0], 10))")
[ "$L0" = "$LAM0" ] || stop "lambda_0(19.5) reads $L0, not $LAM0"
step "pins checked (in_blobs.txt), diff of the two checks rebuilt (3 changed lines), worktree 48c36355: dss_ell, ell_ddm, ell_dd, ddnp equal 505d8399; ell_refine.py 631e5801; lambda_0(19.5) $L0; $($PY -V 2>&1), multidouble $($PY -c 'import multidouble as m; print(m.isa())')"
cp $IN/sol_${SRC}_D19.5000.npy $WTM/data/sol_${SRC}_D19.5000.npy
[ "$(blob $WTM/data/sol_${SRC}_D19.5000.npy | cut -c1-8)" = 57f8e2d3 ] || stop "copied source state blob differs"
# selftests
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py --selftest > $OUT/selftest_kc87_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $IN/kc95_syscheck_1025.py --selftest > $OUT/selftest_kc95_syscheck.txt 2>&1; r2=$?
step "selftests: kc87_syscheck exit $r1, kc95_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# the source check on this machine, with its controls; and the k_c 95 check must refuse the k_c 87 source
C87="nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $IN/l1kc87dh610d195.jsonl $WTM/data/sol_${SRC}_D19.5000.npy $D $WTM"
$C87 > $OUT/source_syscheck.txt 2>&1; s0=$?
$C87 --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
$C87 --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $IN/l1kc87dh610d195.jsonl $WTM/data/sol_${SRC}_D19.5000.npy $D $WTM > $OUT/source_kc95check_refuses.txt 2>&1; s3=$?
step "source check (kc87_syscheck_1025.py on my k_c 87 D 19.5 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc95_syscheck on the k_c 87 source exit $s3 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
[ "$MODE" = dry ] && { step "dry run: the regrid is not started"; exit 0; }
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 87 $TAG 95 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $OUT/regrid.log
step "regrid starts: $CMD"
( while sleep 60; do
    echo "$(stamp),$(ps -C python -o rss=,pcpu=,nlwp=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-4)" >> $OUT/regrid_samples.csv
    av=$(awk '/MemAvailable/ {print $2}' /proc/meminfo)
    [ "$av" -lt $MEMSTOP ] && echo "$(stamp) UTC MemAvailable $av kB below 4 GiB (alert only; nothing is stopped)" >> $OUT/MEMALERT.txt
  done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D19.5000.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $F/ ; cp $WTM/data/sol_${TAG}_D19.5000.npy $F/
# the acceptance: kc95_syscheck_1025.py with its two controls; the k_c 87 check must refuse the k_c 95 result
C95="nice -n 10 $PY -I $IN/kc95_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.5000.npy $D $WTM"
$C95 > $OUT/syscheck.txt 2>&1; a0=$?
$C95 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
$C95 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.5000.npy $D $WTM > $OUT/syscheck_kc87check_refuses.txt 2>&1; a3=$?
step "kc95 syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); kc87_syscheck on the k_c 95 result exit $a3 (1 wanted)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else echo "REFUSED: syscheck $a0, controls $a1 $a2, kc87 check on the result $a3" > $OUT/VERDICT.txt; fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}

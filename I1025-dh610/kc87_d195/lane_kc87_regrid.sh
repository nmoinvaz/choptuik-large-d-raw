#!/bin/bash
# #1025 kc87_d195 (dh610), step 1 of the coordinator's order of 22 Nov: dh370's accepted k_c 79 D 19.5 state (raw I1025-dh370/kc79_d195/, f40a4556) regridded to k_c 87 with ell_refine.py as dh370 ran its k_c 79
# regrids (worktree 48c36355, `--kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma`, lambda_0(19.5) = 2.1132623525 from ell_delta.lam0_at). The source is checked first with kc79_syscheck_1025.py (must accept, both
# controls refuse); the result is accepted only by kc87_syscheck_1025.py (the k_c 79 check with the k_c 79 test changed to k_c 87 and nothing else, kc87_syscheck_1025.diff), its selftest and both controls (must refuse).
# 8 threads, nice 10, cap 21600 s, a systemd unit (i1025p). Steps and verdicts go to regrid/steps.txt and regrid/VERDICT.txt. usage: bash lane_kc87_regrid.sh [dry]
{
set -u
MODE=${1:-}
RAW=/home/nathan/Source/choptuik-large-d-raw; F=$RAW/I1025-dh610/kc87_d195; IN=$F/in; OUT=$F/regrid
WT=/home/nathan/Source/choptuik-large-d-1025g; WTM=$WT/solver/matter; PY=/home/nathan/Source/venv-i1058/bin/python
SRC=l1kc79dh370d195; TAG=l1kc87dh610d195; D=19.5; LAM0=2.1132623525
export PYTHONDONTWRITEBYTECODE=1 OMP_NUM_THREADS=8 OPENBLAS_NUM_THREADS=8 MKL_NUM_THREADS=8
mkdir -p $OUT
stamp() { date -u '+%F %T'; }
step() { echo "$(stamp) UTC $*" | tee -a $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1"; }
step "start (load $(cut -d' ' -f1-3 /proc/loadavg), MemAvailable $(awk '/MemAvailable/ {print $2}' /proc/meminfo) kB)"
for pb in "$IN/d18_hybsign.py e089207a61fbd98614716abd309571cbc4888db2" \
          "$IN/sol_l1kc79dh370d195_D19.5000.npy 9528b355f7c93c9e7dc868fead7106af59b27c17" "$IN/l1kc79dh370d195.jsonl 5777d2a24cb527acc2b8df13be1669e65f795ace" \
          "$IN/kc79_syscheck_1025.py 29dce7eab9677e568566a8ba05d7073109296a69" "$IN/kc87_syscheck_1025.py 6df5d9600edebeae8cc4e602025e42e79925b7d6" \
          "$IN/read_lower.py 89309d3c8e4f758bb5f936f7d24796b594e4cbdb" "$IN/d185_scan_read.py 7c9d400fd0966a35ac306b5495febb4ec4efe7da" \
          "$IN/d18c_read.py 1383470feaa976e4185e423626a0d5fec328de86" "$IN/repeat_check.py aaf598a98c05d8d67f740b5a3b0675b422daad6a"; do
  set -- $pb
  [ -f $1 ] && [ "$(blob $1)" = "$2" ] || stop "$1 missing or not blob $2"
done
# the k_c 87 check differs from the k_c 79 check in the k_c test only (the diff is in the folder and is rebuilt here)
diff -u $IN/kc79_syscheck_1025.py $IN/kc87_syscheck_1025.py | tail -n +3 > $OUT/diff_rebuilt.txt
tail -n +3 $F/kc87_syscheck_1025.diff | cmp -s - $OUT/diff_rebuilt.txt || stop "kc87_syscheck_1025.diff is not the diff of the two checks"
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
[ "$(blob $WTM/data/sol_${SRC}_D19.5000.npy | cut -c1-8)" = 9528b355 ] || stop "copied source state blob differs"
# selftests
nice -n 10 $PY -I $IN/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py --selftest > $OUT/selftest_kc87_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc87_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# the source check on this machine, with its controls; and the k_c 87 check must refuse the k_c 79 source
C79="nice -n 10 $PY -I $IN/kc79_syscheck_1025.py $IN/l1kc79dh370d195.jsonl $WTM/data/sol_${SRC}_D19.5000.npy $D $WTM"
$C79 > $OUT/source_syscheck.txt 2>&1; s0=$?
$C79 --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
$C79 --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $IN/l1kc79dh370d195.jsonl $WTM/data/sol_${SRC}_D19.5000.npy $D $WTM > $OUT/source_kc87check_refuses.txt 2>&1; s3=$?
step "source check (kc79_syscheck_1025.py on dh370's k_c 79 D 19.5 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc87_syscheck on the k_c 79 source exit $s3 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
[ "$MODE" = dry ] && { step "dry run: the regrid is not started"; exit 0; }
CMD="nice -n 10 timeout 21600 $PY -u ell_refine.py $SRC 79 $TAG 87 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 8 threads, nice 10, cap 21600 s): $CMD" > $OUT/regrid.log
step "regrid starts: $CMD"
( while sleep 60; do echo "$(stamp),$(ps -C python -o rss=,pcpu=,nlwp=,args= | grep 'ell_refine.py' | grep -v grep | head -1 | cut -d' ' -f1-4)" >> $OUT/regrid_samples.csv; done ) &
SAMP=$!
t0=$(date +%s)
( cd $WTM && $CMD >> $OUT/regrid.log 2>&1 ); rc=$?
kill $SAMP 2>/dev/null
step "regrid exit $rc, wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc (0 wanted; 124 is the cap)"
[ -s $WTM/data/$TAG.jsonl ] && [ -s $WTM/data/sol_${TAG}_D19.5000.npy ] || stop "the regrid wrote no record or state"
cp $WTM/data/$TAG.jsonl $F/ ; cp $WTM/data/sol_${TAG}_D19.5000.npy $F/
# the acceptance: kc87_syscheck_1025.py with its two controls; the k_c 79 check must refuse the k_c 87 result
C87="nice -n 10 $PY -I $IN/kc87_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.5000.npy $D $WTM"
$C87 > $OUT/syscheck.txt 2>&1; a0=$?
$C87 --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
$C87 --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
nice -n 10 $PY -I $IN/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.5000.npy $D $WTM > $OUT/syscheck_kc79check_refuses.txt 2>&1; a3=$?
step "kc87 syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); kc79_syscheck on the k_c 87 result exit $a3 (1 wanted)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else echo "REFUSED: syscheck $a0, controls $a1 $a2, kc79 check on the result $a3" > $OUT/VERDICT.txt; fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}

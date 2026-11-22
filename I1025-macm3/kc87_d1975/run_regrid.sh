#!/bin/bash
# #1025 macm3b kc87_d1975 (t5's hc 2026-11-22 ~23:35 UTC): dh170's accepted k_c 79 D 19.75 state (raw I1025-dh170/kc79_d1975/, 5d0c8f74) regridded to k_c 87 with ell_refine.py as I did at D 19.375 (../kc87_d19375/)
# (raw I1025-dh610/kc87_d195/lane_kc87_regrid.sh, ec9fb489), accepted only by dh610's kc87_syscheck_1025.py (6df5d960) with its two controls; kc79_syscheck_1025.py must refuse the result.
# Own session (launch_1070.py: setsid), under caffeinate -is, 6 threads, nice 10, cap 21600 s by exact pid (capped_run.py; macOS has no timeout).
# Steps and verdicts go to steps.txt and VERDICT.txt; no hc from here. Stops at the first failure.
{
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc87_d1975
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
SRC=l1kc79dh170d1975; TAG=l1kc87macm3d1975; D=19.75; LAM0=2.1120935738
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
cd $OUT || exit 9
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
chk() { [ "$(blob $OUT/in/$1)" = "$2" ] || stop "in/$1 is not blob $2"; }
step "start (loadavg $(sysctl -n vm.loadavg), free memory $(memory_pressure | tail -1 | sed 's/.*: //'), disk $(df -h /System/Volumes/Data | tail -1 | awk '{print $4}') free)"
chk sol_l1kc79dh170d1975_D19.7500.npy f2ad34b5; chk l1kc79dh170d1975.jsonl 0508163e; chk kc87_syscheck_1025.py 6df5d960; chk kc79_syscheck_1025.py 29dce7ea
chk d18_hybsign.py e089207a; chk read_lower.py 89309d3c; chk d185_scan_read.py 7c9d400f
step "inputs pinned in in/ (state f2ad34b5 and record 0508163e from raw 5d0c8f74 (dh170's k_c 79 D 19.75); kc87_syscheck 6df5d960 from raw ec9fb489; kc79_syscheck 29dce7ea, d18_hybsign e089207a, read_lower 89309d3c, d185_scan_read 7c9d400f from raw 8e4797ff)"
# the k_c 87 check is the k_c 79 check with three lines changed, and its diff is dh610's
diff -u in/kc79_syscheck_1025.py in/kc87_syscheck_1025.py > $OUT/kc87_diff_rebuilt.txt
nl=$(grep -c '^<' <(diff in/kc79_syscheck_1025.py in/kc87_syscheck_1025.py)); nr=$(grep -c '^>' <(diff in/kc79_syscheck_1025.py in/kc87_syscheck_1025.py))
[ "$nl" = 3 ] && [ "$nr" = 3 ] || stop "kc87_syscheck differs from kc79_syscheck in $nl and $nr lines (3 and 3 wanted)"
diff <(tail -n +3 $OUT/kc87_diff_rebuilt.txt) <(tail -n +3 $OUT/in/kc87_syscheck_1025.diff.dh610) > /dev/null || stop "the rebuilt diff differs from dh610's"
step "kc87_syscheck_1025.py = kc79_syscheck_1025.py with 3 lines changed; the rebuilt diff's hunks equal dh610's (kc87_diff_rebuilt.txt)"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 505d8399 ] || stop "worktree not at 505d8399"
[ "$(git hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801 (dh370's)"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 505d8399, ell_refine.py 631e5801 (dh370's), clean outside solver/matter/data; $($PY -V 2>&1), multidouble isa $($PY -c 'import multidouble as m; print(m.isa())')"
L0=$(cd $WTM && $PY -c "import ell_delta as e; print('%.10f' % e.lam0_at($D, *e.lam0_table())[0])")
[ "$L0" = "$LAM0" ] || stop "lambda_0 from ell_delta.lam0_at($D) is $L0, not $LAM0"
step "lambda_0 = ell_delta.lam0_at($D, *lam0_table()) = $L0 (ell_delta.py blob $(blob $WTM/ell_delta.py); --no-gamma does not use it)"
[ ! -e $WTM/data/$TAG.jsonl ] && [ -z "$(ls $WTM/data/sol_${TAG}_* 2>/dev/null)" ] || stop "data/ already holds $TAG files"
# the source state under the name ell_refine reads (D:.4f), and its record
cp $OUT/in/sol_${SRC}_D19.7500.npy $WTM/data/sol_${SRC}_D19.7500.npy; cp $OUT/in/$SRC.jsonl $WTM/data/$SRC.jsonl
[ "$(blob $WTM/data/sol_${SRC}_D19.7500.npy)" = f2ad34b5 ] && [ "$(blob $WTM/data/$SRC.jsonl)" = 0508163e ] || stop "copied source blobs differ"
# selftests
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py --selftest > $OUT/selftest_kc87_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc87_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# source check on this machine, with its controls (kc79_syscheck on the k_c 79 source), and the k_c 87 check must refuse the k_c 79 source
SS=$WTM/data/sol_${SRC}_D19.7500.npy; SR=$WTM/data/$SRC.jsonl
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $SR $SS $D $WTM > $OUT/source_kc87check_refuses.txt 2>&1; s3=$?
step "source check (kc79_syscheck_1025.py on dh170's k_c 79 D 19.75 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each); kc87_syscheck_1025.py on the k_c 79 source exit $s3 (1 wanted)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] && [ $s3 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
[ "$1" = source ] && { step "source only: done"; exit 0; }
# the regrid (ell_refine.py as dh610's D 19.5 command; D, tags and lambda_0 changed; --no-gamma does not use lambda_0)
CMD="nice -n 10 $PY -u $OUT/capped_run.py 21600 $PY -u ell_refine.py $SRC 79 $TAG 87 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 6 threads, nice 10, cap 21600 s by exact pid): $CMD" > $OUT/regrid.log
step "regrid starts: $CMD"
( cd $WTM && nice -n 10 $PY -u $OUT/capped_run.py 21600 $PY -u ell_refine.py $SRC 79 $TAG 87 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma >> $OUT/regrid.log 2>&1 ) &
RP=$!
t0=$(date +%s)
CP=""
for i in $(seq 1 60); do CP=$(grep -o 'child pid [0-9]*' $OUT/regrid.log | head -1 | awk '{print $3}'); [ -n "$CP" ] && break; sleep 1; done
step "regrid child pid $CP (capped_run wrapper $RP)"
echo "time_utc,rss_kB,pcpu,free_mem_pct,load1" > $OUT/regrid_samples.csv
while kill -0 $RP 2>/dev/null; do
  sleep 60
  echo "$(stamp),$(ps -o rss=,pcpu= -p $CP 2>/dev/null | awk '{print $1","$2}'),$(memory_pressure | tail -1 | sed 's/.*: //;s/%//'),$(sysctl -n vm.loadavg | awk '{print $2}')" >> $OUT/regrid_samples.csv
done
wait $RP; rc=$?
step "regrid exit $rc (capped_run's; 0 wanted, 124 is the cap), wall $(( $(date +%s) - t0 )) s"
[ $rc = 0 ] || stop "the regrid exit $rc"
cp $WTM/data/$TAG.jsonl $OUT/; cp $WTM/data/sol_${TAG}_D19.7500.npy $OUT/
# the acceptance: dh610's kc87 check and its controls; the k_c 79 check must refuse the result
RS=$WTM/data/sol_${TAG}_D19.7500.npy; RR=$WTM/data/$TAG.jsonl
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $RR $RS $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $RR $RS $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc87_syscheck_1025.py $RR $RS $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $RR $RS $D $WTM > $OUT/syscheck_kc79check_refuses.txt 2>&1; a3=$?
step "kc87 syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each); kc79_syscheck_1025.py on the k_c 87 result exit $a3 (1 wanted)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ] && [ $a3 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else echo "REFUSED: syscheck $a0, controls $a1 $a2, kc79 check $a3" > $OUT/VERDICT.txt; fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}

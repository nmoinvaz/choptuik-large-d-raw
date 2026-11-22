#!/bin/bash
# #1025 macm3b kc79_d1925 (t5's hc 2026-11-22 ~19:10 UTC): win2's k_c 71 D 19.25 state regridded to k_c 79 with ell_refine.py as dh370 did at D 19.125
# (raw I1025-dh370/kc79_d19125/run_regrid.sh, 79b57212), accepted only by kc79_syscheck_1025.py and its two controls. Own session (launch_1070.py: setsid), under caffeinate -is,
# 6 threads, nice 10, cap 21600 s by exact pid (capped_run.py; macOS has no timeout). Steps and verdicts go to steps.txt and VERDICT.txt; no hc from here.
# Stops at the first failure. Usage: run_regrid.sh [source]  (with "source": the pins, selftests and source check only, no regrid)
{
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_d1925
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
SRC=l1kc71Lw1025; TAG=l1kc79macm3; D=19.25; LAM0=2.1144367878
export OMP_NUM_THREADS=6 OPENBLAS_NUM_THREADS=6 MKL_NUM_THREADS=6 VECLIB_MAXIMUM_THREADS=6 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
cd $OUT || exit 9
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
chk() { [ "$(blob $OUT/in/$1)" = "$2" ] || stop "in/$1 is not blob $2"; }
step "start (loadavg $(sysctl -n vm.loadavg), free memory $(memory_pressure | tail -1 | sed 's/.*: //'), disk $(df -h /System/Volumes/Data | tail -1 | awk '{print $4}') free)"
chk sol_l1kc71Lw1025_D19.250000.npy 36bc6b83; chk l1kc71Lw1025.jsonl c5fc14a9; chk kc71_syscheck.py 4cd86cd4; chk kc79_syscheck_1025.py 29dce7ea
chk d18_hybsign.py e089207a; chk read_lower.py 89309d3c; chk d185_scan_read.py 7c9d400f
step "inputs pinned in in/ (state 36bc6b83, record c5fc14a9 from raw 8e4797ff, kc71_syscheck 4cd86cd4, kc79_syscheck 29dce7ea, d18_hybsign e089207a, read_lower 89309d3c, d185_scan_read 7c9d400f)"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 505d8399 ] || stop "worktree not at 505d8399"
[ "$(git hash-object $WTM/ell_refine.py | cut -c1-8)" = 631e5801 ] || stop "ell_refine.py is not blob 631e5801 (dh370's)"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 505d8399, ell_refine.py 631e5801 (dh370's), clean outside solver/matter/data; $($PY -V 2>&1), multidouble isa $($PY -c 'import multidouble as m; print(m.isa())')"
# the source state under the name ell_refine reads (D:.4f)
cp $OUT/in/sol_${SRC}_D19.250000.npy $WTM/data/sol_${SRC}_D19.2500.npy
[ "$(blob $WTM/data/sol_${SRC}_D19.2500.npy)" = 36bc6b83 ] || stop "copied source state blob differs"
# selftests
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py --selftest > $OUT/selftest_kc71_syscheck.txt 2>&1; r2=$?
step "selftests: kc79_syscheck exit $r1, kc71_syscheck exit $r2 (0 wanted)"
[ $r1 = 0 ] && [ $r2 = 0 ] || stop "a selftest failed"
# source check on this machine, with its controls
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025.jsonl $WTM/data/sol_${SRC}_D19.2500.npy $D $WTM > $OUT/source_syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025.jsonl $WTM/data/sol_${SRC}_D19.2500.npy $D $WTM --mutate=F > $OUT/source_syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc71_syscheck.py $OUT/in/l1kc71Lw1025.jsonl $WTM/data/sol_${SRC}_D19.2500.npy $D $WTM --mutate=steps > $OUT/source_syscheck_mutsteps.txt 2>&1; s2=$?
step "source check (win2's kc71_syscheck.py on the k_c 71 D 19.25 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each)"
[ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ] || stop "the source check or a control did not read as written"
echo "SOURCE ACCEPTED $(stamp) UTC" > $OUT/SOURCE_OK.txt
[ "$1" = source ] && { step "source only: done"; exit 0; }
# the regrid (ell_refine.py as dh370's D 19.125 command; D, tag and lambda_0 changed; --no-gamma does not use lambda_0)
CMD="nice -n 10 $PY -u $OUT/capped_run.py 21600 $PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma"
echo "# $(stamp) UTC cmd (cwd $WTM, 6 threads, nice 10, cap 21600 s by exact pid): $CMD" > $OUT/regrid.log
step "regrid starts: $CMD"
( cd $WTM && nice -n 10 $PY -u $OUT/capped_run.py 21600 $PY -u ell_refine.py $SRC 71 $TAG 79 1 $D $LAM0 --kappa 0.7 --u0 0.04 --Ks 30 --tol 1e-12 --wait 60 --no-gamma >> $OUT/regrid.log 2>&1 ) &
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
cp $WTM/data/$TAG.jsonl $OUT/; cp $WTM/data/sol_${TAG}_D19.2500.npy $OUT/
# the acceptance
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.2500.npy $D $WTM > $OUT/syscheck.txt 2>&1; a0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.2500.npy $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; a1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $WTM/data/$TAG.jsonl $WTM/data/sol_${TAG}_D19.2500.npy $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; a2=$?
step "syscheck exit $a0 (0 wanted); controls --mutate=F exit $a1, --mutate=steps exit $a2 (1 wanted each)"
if [ $a0 = 0 ] && [ $a1 = 1 ] && [ $a2 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else echo "REFUSED: syscheck $a0, controls $a1 $a2" > $OUT/VERDICT.txt; fi
step "verdict: $(cat $OUT/VERDICT.txt)"
exit 0
}

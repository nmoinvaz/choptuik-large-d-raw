#!/bin/bash
# #1025 macm3b kc79_d2075 step 1 (t5's hc 2026-11-23 ~14:55 UTC): win2's accepted k_c 79 D 20.75 state (raw I1025-win2/kc79_leap/, 60d75f9f; no regrid) accepted by kc79_syscheck_1025.py (29dce7ea) on this build, with its selftest and both controls.
# Steps and the verdict go to steps.txt and VERDICT.txt; no hc from here. Stops at the first failure.
{
OUT=$HOME/Source/choptuik-large-d-raw-903/I1025-macm3/kc79_d2075
WT=$HOME/Source/choptuik-large-d-1025m; WTM=$WT/solver/matter
PY=$HOME/Source/venv-macm3-1058b/bin/python
TAG=l1kc79win2d2075; D=20.75
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 P4_WT_MATTER=$WTM PYTHONFAULTHANDLER=1
cd $OUT || exit 9
stamp() { date -u '+%Y-%m-%d %H:%M:%S'; }
step() { echo "$(stamp) UTC $*" >> $OUT/steps.txt; }
stop() { echo "REFUSED: $*" > $OUT/VERDICT.txt; step "STOP: $*"; exit 1; }
blob() { git hash-object --no-filters "$1" | cut -c1-8; }
chk() { [ "$(blob $OUT/in/$1)" = "$2" ] || stop "in/$1 is not blob $2"; }
step "start (loadavg $(sysctl -n vm.loadavg), free memory $(memory_pressure | tail -1 | sed 's/.*: //'), disk $(df -h /System/Volumes/Data | tail -1 | awk '{print $4}') free)"
chk sol_${TAG}_D20.7500.npy 1368e4ac; chk $TAG.jsonl c83fa5b2; chk kc79_syscheck_1025.py 29dce7ea
chk d18_hybsign.py e089207a; chk read_lower.py 89309d3c; chk d185_scan_read.py 7c9d400f
step "inputs pinned in in/ (state 1368e4ac and record c83fa5b2 from raw 60d75f9f (win2's k_c 79 D 20.75); kc79_syscheck 29dce7ea, d18_hybsign e089207a, read_lower 89309d3c, d185_scan_read 7c9d400f from raw 8e4797ff)"
[ "$(git -C $WT rev-parse HEAD | cut -c1-8)" = 505d8399 ] || stop "worktree not at 505d8399"
[ -z "$(git -C $WT status --short solver | grep -v 'solver/matter/data/')" ] || stop "worktree solver/ has changes"
step "worktree 505d8399, clean outside solver/matter/data; $($PY -V 2>&1), multidouble isa $($PY -c 'import multidouble as m; print(m.isa())')"
[ ! -e $WTM/data/$TAG.jsonl ] && [ -z "$(ls $WTM/data/sol_${TAG}_* 2>/dev/null)" ] || stop "data/ already holds $TAG files"
cp $OUT/in/sol_${TAG}_D20.7500.npy $WTM/data/sol_${TAG}_D20.7500.npy; cp $OUT/in/$TAG.jsonl $WTM/data/$TAG.jsonl
[ "$(blob $WTM/data/sol_${TAG}_D20.7500.npy)" = 1368e4ac ] && [ "$(blob $WTM/data/$TAG.jsonl)" = c83fa5b2 ] || stop "copied blobs differ"
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py --selftest > $OUT/selftest_kc79_syscheck.txt 2>&1; r1=$?
step "selftest: kc79_syscheck exit $r1 (0 wanted)"
[ $r1 = 0 ] || stop "the selftest failed"
SS=$WTM/data/sol_${TAG}_D20.7500.npy; SR=$WTM/data/$TAG.jsonl
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM > $OUT/syscheck.txt 2>&1; s0=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM --mutate=F > $OUT/syscheck_mutF.txt 2>&1; s1=$?
nice -n 10 $PY -I $OUT/in/kc79_syscheck_1025.py $SR $SS $D $WTM --mutate=steps > $OUT/syscheck_mutsteps.txt 2>&1; s2=$?
step "source check (kc79_syscheck_1025.py on win2's k_c 79 D 20.75 state): exit $s0 (0 wanted); controls --mutate=F exit $s1, --mutate=steps exit $s2 (1 wanted each)"
if [ $s0 = 0 ] && [ $s1 = 1 ] && [ $s2 = 1 ]; then echo "ACCEPTED $(stamp) UTC" > $OUT/VERDICT.txt; else stop "the source check or a control did not read as written (exit $s0, $s1, $s2)"; fi
step "verdict: ACCEPTED"
exit 0
}

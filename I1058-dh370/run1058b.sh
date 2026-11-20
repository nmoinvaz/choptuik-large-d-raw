#!/usr/bin/env bash
# #1058 on dh370 (second build, the target moved): hp at main 8179068d in a new venv (worktree ~/Source/choptuik-large-d-1058b), low-memory recipe, 2 jobs, nice 19, beside ks_chain3b's leg 11; then the four stored-reference checks (2 threads, nice 19).
# usage: bash run1058.sh     (as user unit i1058c; its OOMScoreAdjust 1000 makes the build the kernel's first victim, never the chain)
WT=/home/nathan/Source/choptuik-large-d-1058b
RAW=/home/nathan/Source/choptuik-large-d-raw-wt613
OUT=$RAW/I1058-dh370/at8179068d
cd $WT/hp || exit 9
. $WT/.venv/bin/activate
export CARGO_PROFILE_RELEASE_LTO=false CARGO_PROFILE_RELEASE_CODEGEN_UNITS=16 CARGO_BUILD_JOBS=2 PIP_NO_CACHE_DIR=1
log() { echo "1058 $* $(date -u '+%F %T UTC')" >> $OUT/exits_1058.txt; }
log "build start (8179068d, LTO off, 16 codegen units, 2 jobs, nice 19)"
git -C $WT log -1 --format='%H %s' >> $OUT/build.log
pip uninstall -y multidouble >> $OUT/build.log 2>&1
nice -n 19 /usr/bin/time -v -o $OUT/build_time.txt bash build.sh >> $OUT/build.log 2>&1
rc=$?
log "build exit $rc"
[ $rc = 0 ] || exit $rc
DU=$(ls $WT/.venv/lib/python3.14/site-packages/multidouble-*.dist-info/direct_url.json 2>/dev/null | head -1)
[ -n "$DU" ] && cp "$DU" $OUT/direct_url.json && log "direct_url $(python3 -c "import json,sys; d=json.load(open('$DU')); print(d.get('vcs_info',{}).get('commit_id'))")"
python -c "import hpkernel, multidouble; print('import', hpkernel.isa(), multidouble.isa(), hpkernel.__file__)" >> $OUT/build.log 2>&1
run() { name=$1; shift; echo "== $name $(date -u '+%F %T')" > $OUT/check_$name.log; nice -n 19 python -u highm_check.py "$@" >> $OUT/check_$name.log 2>&1; ec=$?; echo "exit $ec" >> $OUT/check_$name.log; log "check $name exit $ec"; }
run ref ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80
run scaled scaled --compare=$RAW/T81/scaled_main.json
run jets jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json
run jets_mutate jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa    # must exit 1
log "checks done"

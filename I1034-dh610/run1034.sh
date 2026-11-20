#!/bin/bash
# #1034 steps 1-6 on dh610 at main 9980cd93, with #1040's step_timing_check after the build (README.md). One step at a time, nice 10, each under timeout (3 x its estimate)
# on the exact command's pid; the exit, wall seconds and, where there is one, the checksum line go to summary_1034.txt.
. "$(dirname "$0")/common1034.sh"
X=$OUT/exits_1034.txt; S=$OUT/summary_1034.txt
log() { echo "1034 $* $(stamp) UTC" >> $X; }
cd $WT || exit 1
[ "$(git rev-parse HEAD | cut -c1-8)" = 9980cd93 ] || { echo "WT is not at 9980cd93"; exit 1; }
[ -z "$(git status --short)" ] || { echo "worktree not clean"; exit 1; }
log "start, code $(git rev-parse --short=8 HEAD), load $(cut -d' ' -f1-3 /proc/loadavg), $(cargo --version), $(rustc --version)"
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 CARGO_BUILD_JOBS=6
# runin DIR NAME WANT CAP cmd...: from hp/, log to DIR/NAME.log, summary line
runin() { local dir=$1 name=$2 want=$3 cap=$4; shift 4; cd $WT/hp || return 99; { echo "# $(stamp) UTC cmd: $*"; } > $dir/$name.log
  local s=$(date +%s); nice -n 10 timeout -s TERM $cap "$@" >> $dir/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $dir/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s (cap $cap s) $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $S; log "$name exit $rc (expected $want)"; return $rc; }
run() { runin $OUT "$@"; }
# 0. venv
if [ ! -x $VENV/bin/python ]; then uv venv --python 3.14 --seed $VENV > $OUT/venv.log 2>&1 && uv pip install -p $VENV/bin/python -r $WT/requirements.txt >> $OUT/venv.log 2>&1; fi
. $VENV/bin/activate
echo "# $(stamp) UTC start, hp $(git -C $WT rev-parse --short=8 HEAD), $($VENV/bin/python -V), maturin $(maturin --version 2>&1 | head -1), multidouble $(grep -A1 'name = "multidouble"' $WT/hp/Cargo.lock | sed -n 2p), load $(cut -d' ' -f1-3 /proc/loadavg)" > $S
# 1. the build (est. 31 min, 24 GB; cap 93 min)
run step1_build 0 5580 bash build.sh
python -c "import hpkernel, multidouble; print('hpkernel', hpkernel.isa(), hpkernel.__file__, 'multidouble', multidouble.isa())" > $OUT/hpkernel_import.log 2>&1; echo "hpkernel import: exit $? $(cat $OUT/hpkernel_import.log | tail -1)" >> $S
# #1040's check, once, after the build (est. a few minutes; cap 30 min each)
runin $OUT40 step_timing_ok 0 1800 python3 step_timing_check.py --reps=3 --threads=4
runin $OUT40 step_timing_mutate_drop 1 1800 python3 step_timing_check.py --reps=2 --threads=4 --mutate=drop
cp $OUT/exits_1034.txt /dev/null; grep -E "step_timing" $X | sed 's/^1034/1040/' > $OUT40/exits_1040.txt
# 2. the split_ and fastmul_planted tests (est. 18 min each; cap 1 h)
run step2_split 0 3600 cargo test --profile release-dev --lib split_ -- --nocapture
echo "   checksums in step2_split.log: $(grep -oE "(split|fast) series' checksum [0-9a-f]{16}" $OUT/step2_split.log | tr '\n' ';') (expect split a0aada9b8fe95419, fast 30acdab9851616fb)" >> $S
run step2_fastmul_planted 0 3600 cargo test --profile release-dev --lib fastmul_planted -- --nocapture
# 5. bit identity of the existing paths (est. 10 + 40 + 5 + 5 min; caps 30, 120, 30, 30 min)
run step5_ref 0 1800 python3 highm_check.py ref --compare=$RAW/T81/ref_main.json --Ms=48,64,80
run step5_scaled 0 7200 python3 highm_check.py scaled --compare=$RAW/T81/scaled_main.json
run step5_jets 0 1800 python3 highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json
run step5_jets_kappa 1 1800 python3 highm_check.py jets --compare=$RAW/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
# 3. series_split_check at D 253.3382 (est. 60-90 min each; cap 4.5 h)
run step3_split2_D253 0 16200 python3 series_split_check.py $RAW I608-dh610/restart4_d6/anm_pin3_D253.3382.npz --N 24 --threads 9 --Np 6 --split 2 --out $OUT/split2_D253
run step3_split2_D253_mutate31 1 16200 python3 series_split_check.py $RAW I608-dh610/restart4_d6/anm_pin3_D253.3382.npz --N 24 --threads 9 --Np 6 --split 2 --mutate 31 --out $OUT/split2_D253_mut31
# 4. the same at I903-win2's leg08 D 237.5270 (est. 90 min each; cap 4.5 h)
run step4_split2_D237 0 16200 python3 series_split_check.py $RAW I903-win2/ks_chain/leg08_D232.0000_ks250/anm_pin3_D237.5270.npz --N 24 --threads 9 --Np 6 --split 2 --out $OUT/split2_D237
run step4_split2_D237_mutate31 1 16200 python3 series_split_check.py $RAW I903-win2/ks_chain/leg08_D232.0000_ks250/anm_pin3_D237.5270.npz --N 24 --threads 9 --Np 6 --split 2 --mutate 31 --out $OUT/split2_D237_mut31
# 6. chain step timing at --series_split 0, 1, 2 (est. 70-90 min each; cap 4.5 h)
for sp in 0 1 2; do
  run step6_chain_s$sp 0 16200 python3 anm_run.py $RAW I1034-dh610/step_s$sp --state I903-win2/ks_chain/leg08_D232.0000_ks250/anm_pin3_D237.5270.npz --kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 9 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred --steps 1 --series_split $sp
  echo "   series lines of s$sp: $(grep -E 'series saved' $OUT/step6_chain_s$sp.log | tail -2 | tr '\n' ';')" >> $S
done
log "all steps done"

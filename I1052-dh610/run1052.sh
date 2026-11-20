#!/bin/bash
# PR #1052's A/B on dh610: the coordinator's commands (PR #1052, comment of 20 Nov 10:22 UTC), one run after another, 10 threads, nice 10, the #1050 build's venv for both arms.
. "$(dirname "$0")/common1052.sh"
X=$OUT/exits_1052.txt; S=$OUT/summary_1052.txt
log() { echo "1052 $* $(stamp) UTC" >> $X; }
[ "$(git -C $W rev-parse HEAD | cut -c1-8)" = 2b883799 ] || { echo "$W is not at 2b883799"; exit 1; }
[ "$(git -C $WB rev-parse HEAD | cut -c1-8)" = 1c02b15b ] || { echo "$WB is not at 1c02b15b"; exit 1; }
[ -x $PY ] || { echo "no $PY"; exit 1; }
log "start, A/B worktrees 2b883799 / 1c02b15b, hpkernel $($PY -c 'import hpkernel;print(hpkernel.__file__, hpkernel.isa())'), load $(cut -d' ' -f1-3 /proc/loadavg)"
echo "# $(stamp) UTC PR #1052 A/B: hp $(git -C $W rev-parse --short=8 HEAD) (B) against base $(git -C $WB rev-parse --short=8 HEAD) (A); kernel: $($PY -c 'import hpkernel;print(hpkernel.__file__, hpkernel.isa())')" > $S
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
cd $W/hp || exit 1
P=T129-win2/chain/anm_pin3_D180.5246.npz
# one(NAME WANT CAP DIR cmd...): from DIR, log to $OUT/NAME.log, a summary line
one() { local name=$1 want=$2 cap=$3 dir=$4; shift 4; { echo "# $(stamp) UTC cwd $dir cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s); (cd $dir && nice -n 10 timeout -s TERM $cap "$@") >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s (cap $cap s) $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $S; log "$name exit $rc (expected $want)"; return $rc; }
CMP="import numpy as np,sys;a,b=(np.load(f) for f in sys.argv[1:]);k=['zh','zl','z2','z3','z4','z5','z6','z7'];ok=all(np.array_equal(a[x],b[x]) for x in k);print('bit for bit' if ok else 'DIFFER');sys.exit(not ok)"
# K1: the default path bit for bit on the kernel (est. 15 min each; cap 1.5 h)
one k1_base 0 5400 $WB/hp $PY -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --out $OUT/k1_base
one k1_off 0 5400 $W/hp $PY -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --out $OUT/k1_off
$PY -c "$CMP" $OUT/k1_base.npz $OUT/k1_off.npz > $OUT/k1_compare.log 2>&1; rc=$?; echo "k1_compare (k1_base against k1_off): expected exit 0 (bit for bit), got $rc: $(cat $OUT/k1_compare.log)" >> $S; log "k1_compare exit $rc"
# K2: planted with the updates; pass "(a) PASS"; controls --mutate_offset qd and --mutate 10 exit 1 (est. 15 min each; cap 1.5 h)
DREF=$($PY -c "import json;print(json.loads(open('$OUT/k1_off.json').readline())['od']['Delta'])")
echo "# Delta_ref (k1_off.json): $DREF" >> $S
one k2_on 0 5400 $W/hp $PY -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --broyden 1 --Delta_ref $DREF --out $OUT/k2_on
echo "   k2_on: $(grep -c '(a) PASS' $OUT/k2_on.log) lines with '(a) PASS'" >> $S
$PY -c "$CMP" $OUT/k1_base.npz $OUT/k2_on.npz > $OUT/k1_control_compare.log 2>&1; rc=$?; echo "k1 control (k1_base against k2_on): expected exit 1 (DIFFER), got $rc: $(cat $OUT/k1_control_compare.log)" >> $S; log "k1 control exit $rc"
one k2_mut_offset_qd 1 5400 $W/hp $PY -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --broyden 1 --Delta_ref $DREF --mutate_offset qd --out $OUT/k2_mut_offset_qd
one k2_mut_10 1 5400 $W/hp $PY -u octo_corrector.py planted $RAW $P --threads 10 --accept natural --qd 0 --broyden 1 --Delta_ref $DREF --mutate 10 --out $OUT/k2_mut_10
# the chain A/B: leg 10's flags, two steps (est. 45-55 min per arm; cap 3 h)
F="--kfreeze 3 --held_fit data/held_fit.json --N 31 --eps 1e-14 --h_max 2 --threads 10 --corrector od --tol_od 2e-34 --qd_it 40 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --jet_tangent_from 1 --series_split 1 --proj_start pred --reseed_o_stop 1 --od_floor_delta 1e-30 --proj_o 1 --reseed_qd_bar 1e-13 --ks 293 --keep_plan 0 --D_max 266.1776 --steps 1 --a_rule step --od_times 1"
L=I966-dh370/ks_chain3b/leg10_D256.1776_ks293
for arm in a b; do X2=; D=$W/hp; [ $arm = b ] && X2="--od_broyden 1"      # both arms run the PR's scripts (--od_times is the PR's); A has the updates off
  one c1_$arm 0 10800 $D $PY -u anm_run.py $RAW $OUT/c1_$arm --state $L/anm_pin3_D256.5265.npz $F --a0 0.32135254397862245 $X2
  one c2_$arm 0 10800 $D $PY -u anm_run.py $RAW $OUT/c2_$arm --state $L/anm_pin3_D256.8479.npz $F --a0 0.2973364879993668 $X2; done
cd $W/hp
$PY od_broyden_ab.py $OUT/c1_a.log $OUT/c1_b.log $OUT/c1_a/anm_pin3_D256.8479.npz $OUT/c1_b/anm_pin3_D256.8479.npz > $OUT/ab_c1.txt 2>&1; log "od_broyden_ab c1 exit $?"
$PY od_broyden_ab.py $OUT/c2_a.log $OUT/c2_b.log $OUT/c2_a/anm_pin3_D257.1452.npz $OUT/c2_b/anm_pin3_D257.1452.npz > $OUT/ab_c2.txt 2>&1; log "od_broyden_ab c2 exit $?"
# #1008 arc step 4: AB1's inputs at --elim_switch 0 (est. 75 min per arm; cap 4 h)
AF="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 10 --corrector od --tol_od 1e-60 --qd_it 40 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --ks 135 --keep_plan 1 --steps 1 --D_max 262 --arclength 1 --arc_sign 1 --turns_max 2 --guard 0.05 --border 1 --arc_dhold 1e-12 --a0 0.07109375 --elim_switch 0 --od_times 1 --state I1008-macm3/run1/arc_002_D259.311977.npz --arc_jet $RAW/I1008-macm3/run1/arcjet_002_D259.311977.npz"
for arm in a b; do X2=; D=$W/hp; [ $arm = b ] && X2="--od_broyden 1"      # both arms run the PR's scripts (--od_times is the PR's); A has the updates off
  one arc_$arm 0 14400 $D $PY -u anm_run.py $RAW $OUT/arc_$arm $AF $X2; done
cd $W/hp
$PY od_broyden_ab.py $OUT/arc_a.log $OUT/arc_b.log $OUT/arc_a/arc_001_D259.383071.npz $OUT/arc_b/arc_001_D259.383071.npz --kind arc > $OUT/ab_arc.txt 2>&1; log "od_broyden_ab arc exit $?"
log "all steps done"

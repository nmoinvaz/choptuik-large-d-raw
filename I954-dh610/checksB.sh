#!/bin/bash
# #954 on dh610, build B (perf/dup-eval 7583e787 + multidouble PR #72), after checksA.sh: 1. highm_check jets and scaled against A's saved json (exit 0); 2. octo_hashes at ST
# and ST2, diffed against A's (empty) and --mutate_dz 1 (differs only on the newton_o dz line); 3. cargo test jacobian_sub_bitwise ([0,0,0,0,0,0], control [1, 1]);
# 4. dup_eval_check at ST (exit 0, "check: pass") and each --sites m --mutate m (exit 1) for m in base pinned near_null reseed; 5. jac_tangents_check, jet_by_order_check,
# octo_corrector planted (+ its --mutate 10 control), reseed.py checkq (+ its --sweeps 1 control). 8 threads, nice 10, one check after another.
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954b
SUM=$OUT/summary_B.txt
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
so=$(python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
hdr() { echo "# $(stamp) UTC build B, hp $(git -C $WT rev-parse --short HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)')"; echo "# multidouble in the .so: $(strings -n 8 $so 2>/dev/null | grep -oE 'multidouble[-/][^/ ]+' | sort -u | head -3 | tr '\n' ' ')"; }
run() { local name=$1 want=$2; shift 2; { hdr; echo "# cmd: $*"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
runo() { local name=$1 want=$2 f=$3; shift 3; { hdr; echo "# cmd: $* > $f"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" > $OUT/$f 2>> $OUT/$name.log; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
: > $SUM
run B_jets 0 python highm_check.py jets --compare=$OUT/jets_A.json
run B_scaled 0 python highm_check.py scaled --compare=$OUT/scaled_A.json
runo B_octo_ST 0 octo_B_ST.txt python octo_hashes.py $R $ST --threads $T --N 6
runo B_octo_ST2 0 octo_B_ST2.txt python octo_hashes.py $R $ST2 --threads $T --N 6
runo B_octo_ST_mutate 0 octo_B_ST_mutate.txt python octo_hashes.py $R $ST --threads $T --N 6 --mutate_dz 1
runo B_octo_ST2_mutate 0 octo_B_ST2_mutate.txt python octo_hashes.py $R $ST2 --threads $T --N 6 --mutate_dz 1
for s in ST ST2; do
  d=$(diff $OUT/octo_A_$s.txt $OUT/octo_B_$s.txt | wc -l); echo "octo_hashes $s: diff of A against B has $d lines $([ $d = 0 ] && echo OK || echo DIFFERS)" >> $SUM
  m=$(diff $OUT/octo_B_$s.txt $OUT/octo_B_${s}_mutate.txt | grep '^>' | cut -c1-60 | tr '\n' '|')
  echo "octo_hashes $s: --mutate_dz 1 changes: $m" >> $SUM
done
{ hdr; echo "# cmd: cargo test --release --lib jacobian_sub_bitwise -- --nocapture"; } > $OUT/B_jacobian_sub.log
s=$(date +%s); RUSTFLAGS="-C target-cpu=native" CARGO_BUILD_JOBS=8 nice -n 10 cargo test --release --lib jacobian_sub_bitwise -- --nocapture >> $OUT/B_jacobian_sub.log 2>&1; rc=$?; echo "exit $rc" >> $OUT/B_jacobian_sub.log
echo "B_jacobian_sub: expected exit 0, got $rc, $(( $(date +%s) - s )) s; $(grep -E '^\[|control|test result' $OUT/B_jacobian_sub.log | tr '\n' ' ' | cut -c1-300)" >> $SUM
run B_dup_eval 0 python dup_eval_check.py $R $ST --threads $T
for m in base pinned near_null reseed; do run B_dup_eval_mutate_$m 1 python dup_eval_check.py $R $ST --threads $T --sites $m --mutate $m; done
run B_jac_tangents 0 python jac_tangents_check.py $R $ST --threads $T
run B_jet_by_order 0 python jet_by_order_check.py $R $ST --threads $T --N 6
run B_planted 0 python octo_corrector.py planted $R $ST --threads $T
run B_planted_control 1 python octo_corrector.py planted $R $ST --threads $T --mutate 10
run B_checkq 0 python reseed.py checkq $R/$PRED --threads $T
run B_checkq_control 1 python reseed.py checkq $R/$PRED --threads $T --sweeps 1
echo "# checksB done $(stamp) UTC" >> $SUM

#!/bin/bash
# #954 on dh610, build A (main 4c3bb0ef), the reference: 1. highm_check ref, scaled, jets (exit 0) and jets --mutate=kappa (exit 1); 2. the saved jets and scaled
# json; 3. octo_hashes at ST and ST2; 4. series_split_check at ST2 and ST (exit 0) and its --mutate 31 control (exit 1); 5. jet_by_order_check at ST.
# 8 threads at nice 10, one check after another; the issue's `--threads 9` of series_split_check is 8 here (the budget).
. "$(dirname "$0")/common954.sh"
WT=/home/nathan/Source/choptuik-large-d-954a
SUM=$OUT/summary_A.txt
cd "$WT/hp" || exit 1; . ../.venv/bin/activate
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
so=$(python -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
hdr() { echo "# $(stamp) UTC build A, hp $(git -C $WT rev-parse --short HEAD), hpkernel $(python -c 'import hpkernel; print(hpkernel.__file__)')"; echo "# multidouble in the .so: $(strings -n 8 $so 2>/dev/null | grep -oE 'multidouble[-/][^/ ]+' | sort -u | head -3 | tr '\n' ' ')"; }
run() { local name=$1 want=$2; shift 2; { hdr; echo "# cmd: $*"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" >> $OUT/$name.log 2>&1; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
runo() { local name=$1 want=$2 f=$3; shift 3; { hdr; echo "# cmd: $* > $f"; } > $OUT/$name.log; local s=$(date +%s); nice -n 10 "$@" > $OUT/$f 2>> $OUT/$name.log; local rc=$?; echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM; }
: > $SUM
run A_ref 0 python highm_check.py ref --compare=$R/T81/ref_main.json --Ms=48,64,80
run A_scaled 0 python highm_check.py scaled --compare=$R/T81/scaled_main.json
run A_jets 0 python highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json
run A_jets_kappa 1 python highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
run A_jets_save 0 python highm_check.py jets --save=$OUT/jets_A.json
run A_scaled_save 0 python highm_check.py scaled --save=$OUT/scaled_A.json
runo A_octo_ST 0 octo_A_ST.txt python octo_hashes.py $R $ST --threads $T --N 6
runo A_octo_ST2 0 octo_A_ST2.txt python octo_hashes.py $R $ST2 --threads $T --N 6
run A_split_D253 0 python series_split_check.py $R $ST2 --N 24 --threads $T --Np 6 --out $OUT/split_D253
run A_split_D229 0 python series_split_check.py $R $ST --N 24 --threads $T --Np 6 --out $OUT/split_D229
run A_split_mutate31 1 python series_split_check.py $R $ST2 --N 6 --Np 3 --mutate 31 --threads $T --out $OUT/split_mutate
run A_jet_by_order 0 python jet_by_order_check.py $R $ST --threads $T --N 6
echo "# checksA done $(stamp) UTC" >> $SUM

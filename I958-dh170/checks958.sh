#!/bin/bash
# #958 on dh170: checks 1 to 3 of the issue on build D (hp at deps/multidouble-4.9.0 5b7cef1b, venv of choptuik-large-d-958) and the octo_hashes of build A (the
# 4.8.2 build, venv of choptuik-large-d-935) on the same two states, all from build D's hp/ so the scripts and the Python modules are the same bytes.
# 6 threads at nice 10, one check after another. Each writes NAME.log (first lines: hpkernel.__file__, the .so's crate strings, the command; last: exit N)
# and a line in summary_958.txt. usage: bash checks958.sh
OUT=/home/nathan/Source/choptuik-large-d-raw/I958-dh170
WT=/home/nathan/Source/choptuik-large-d-958
VA=/home/nathan/Source/choptuik-large-d-935/.venv
R=/home/nathan/scratch958/raw
ST=I903-win2/ks_chain/leg07_D222.0000_ks240/anm_pin3_D229.0509.npz
ST2=I608-dh610/restart4_d6/anm_pin3_D253.3382.npz
T=6
SUM=$OUT/summary_958.txt
cd "$WT/hp" || exit 1
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
stamp() { date -u '+%F %T'; }
hdr() {   # python, tag
  local py=$1 tag=$2 so
  so=$($py -c 'import hpkernel,os; print(os.path.dirname(hpkernel.__file__))')/*.so
  echo "# $(stamp) UTC build $tag, hp worktree $(git -C $WT rev-parse --short HEAD), python $py"
  echo "# hpkernel $($py -c 'import hpkernel; print(hpkernel.__file__)')"
  echo "# crate strings in the .so: $(strings -n 8 $so 2>/dev/null | grep -oE '(multidouble|multishoot|multisolver)[-/][0-9][^/ ]*' | sort -u | head -12 | tr '\n' ' ')"
}
run() {   # name, expected exit, python, tag, command...
  local name=$1 want=$2 py=$3 tag=$4; shift 4
  { hdr $py $tag; echo "# cmd: $*"; } > $OUT/$name.log
  local s=$(date +%s)
  nice -n 10 "$py" "$@" >> $OUT/$name.log 2>&1; local rc=$?
  echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM
}
runo() {  # name, expected exit, output file, python, tag, command...  (stdout to the file, stderr to the log)
  local name=$1 want=$2 f=$3 py=$4 tag=$5; shift 5
  { hdr $py $tag; echo "# cmd: $* > $f"; } > $OUT/$name.log
  local s=$(date +%s)
  nice -n 10 "$py" "$@" > $OUT/$f 2>> $OUT/$name.log; local rc=$?
  echo "exit $rc" >> $OUT/$name.log
  echo "$name: expected exit $want, got $rc, $(( $(date +%s) - s )) s $([ $rc = $want ] && echo OK || echo MISMATCH)" >> $SUM
}
PD=$WT/.venv/bin/python; PA=$VA/bin/python
: > $SUM
echo "# checks958 start $(stamp) UTC, raw commit $(cat $OUT/raw_commit.txt)" >> $SUM
run D_ref 0 $PD D highm_check.py ref --compare=$R/T81/ref_main.json --Ms=48,64,80
run D_scaled 0 $PD D highm_check.py scaled --compare=$R/T81/scaled_main.json
run D_jets 0 $PD D highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json
run D_jets_kappa 1 $PD D highm_check.py jets --compare=$R/anm-mac/jets_inputs/jets_inputs.json --mutate=kappa
runo D_octo_ST 0 octo_D_ST.txt $PD D octo_hashes.py $R $ST --threads $T --N 6
runo D_octo_ST2 0 octo_D_ST2.txt $PD D octo_hashes.py $R $ST2 --threads $T --N 6
runo D_octo_ST_mut 0 octo_D_ST_mut.txt $PD D octo_hashes.py $R $ST --threads $T --N 6 --mutate_dz 1
runo A_octo_ST 0 octo_A_ST.txt $PA A octo_hashes.py $R $ST --threads $T --N 6
runo A_octo_ST2 0 octo_A_ST2.txt $PA A octo_hashes.py $R $ST2 --threads $T --N 6
run D_jet_by_order 0 $PD D jet_by_order_check.py $R $ST --threads $T --N 6
run D_jac_tangents 0 $PD D jac_tangents_check.py $R $ST --threads $T
# the diffs of check 2 (run from the raw folder; the first version ran in hp/ and exited 2, rerun by hand 2026-11-18)
cd $OUT || exit 1
for s in ST ST2; do
  diff octo_A_$s.txt octo_D_$s.txt > diff_A_D_$s.txt; echo "diff A D $s: exit $? ($(grep -c '^<' diff_A_D_$s.txt) lines differ)" >> $SUM
  diff octo_A_$s.txt $R/I954-dh610/octo_A_$s.txt > diff_A_dh610_$s.txt; echo "diff A(dh170) A(dh610,#954) $s: exit $? ($(grep -c '^<' diff_A_dh610_$s.txt) lines differ)" >> $SUM
done
diff octo_D_ST.txt octo_D_ST_mut.txt > diff_D_mut_ST.txt; echo "diff D D_mut ST: exit $? ($(grep -c '^<' diff_D_mut_ST.txt) lines differ, want exactly the step line)" >> $SUM
echo "# checks958 done $(stamp) UTC" >> $SUM

#!/usr/bin/env bash
# I196-win2: lemma 6a(5) at p^ on win2 (#184's commands), its controls, #39's float control of B, and the cross-load of
# macm3's B (I184-macm3) under #111's rule. From solver/proof/ of D:\choptuik-large-d, one thread, Normal priority.
cd /d/choptuik-large-d/solver/proof || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/venv-t177/Scripts/python.exe
RAW=../../../choptuik-large-d-raw
R=$RAW/I196-win2
BOX=$RAW/I103-macm3/A_M2_6a_M5_sub1e-18.json
BM=$RAW/I184-macm3/B_M5_sub1e-18_phat.json
EX=$R/exits.txt
PHAT=$("$PY" -c "import json; print(','.join(json.load(open('$BOX'))['p']))")
echo "$PHAT" > $R/centre_passed.txt
echo "--x=$PHAT" > $R/cmd_run.txt
echo "start $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $R/driver.txt
step() {  # step NAME LOG ARGS...
  local name=$1 log=$2; shift 2
  local t0=$(date +%s)
  "$PY" -u "$@" > "$log" 2>&1
  local rc=$?
  echo "$name exit $rc wall $(( $(date +%s) - t0 ))s  $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $EX
  return $rc
}
L="lemma6_jump_M.py --M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20"
step run $R/lemma6a_M5_phat.log $L --save-B=$R/B_M5_sub1e-18_phat.json --json=$R/lemma6a_M5_sub1e-18_phat.json
if [ ! -s $R/B_M5_sub1e-18_phat.json ]; then echo "no B saved, controls not run" >> $EX; exit 1; fi
step partial $R/lemma6a_M5_phat_partial.log $L --load-B=$R/B_M5_sub1e-18_phat.json --mutate=partial
step coords $R/lemma6a_M5_phat_coords.log $L --load-B=$R/B_M5_sub1e-18_phat.json --mutate=coords
step swap $R/lemma6a_M5_phat_swap.log $L --mutate=swap
step b_float $R/b_float_new.log review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX
step b_float_mutate_w $R/b_float_new_mutate_w.log review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX --mutate=w
# cross-load: win2 with macm3's B at p^ (#111's rule: its own bound passes, and the stored enclosures cross-load)
step loadB_macm3 $R/lemma6a_loadB_macm3_phat.log $L --load-B=$BM --json=$R/lemma6a_loadB_macm3_phat.json
step b_diff $R/b_diff_win2_vs_macm3_phat.log $RAW/I110-win2/b_diff.py $R/B_M5_sub1e-18_phat.json $BM
step b_diff_selftest $R/b_diff_selftest.log $RAW/I110-win2/b_diff.py --selftest
echo "end $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> $R/driver.txt

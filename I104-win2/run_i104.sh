#!/usr/bin/env bash
# The four commands of #104, in order, from solver/proof/ of the I104 worktree.
cd /c/Users/nathan/Source/choptuik-i104/solver/proof || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1
PY=/c/Users/nathan/Source/choptuik-venv/Scripts/python.exe
R='C:/Users/nathan/Source/choptuik-large-d-raw/I104-win2'
EX="/c/Users/nathan/Source/choptuik-large-d-raw/I104-win2/exits.txt"
step() {  # step NAME LOG ARGS...
  local name=$1 log=$2; shift 2
  local t0=$(date +%s)
  "$PY" -u "$@" > "$log" 2>&1
  local rc=$?
  echo "$name exit $rc wall $(( $(date +%s) - t0 ))s  $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> "$EX"
  return $rc
}
step krawczyk "$R/krawczyk_sub1e-18.log" certify_M2.py krawczyk --box=data/A_M2_box_M5_1e-10.json \
  --sub=1e-18,1e-26,1e-27 || exit 1
step export6a "$R/export6a_sub1e-18.log" certify_M2.py export6a --box=data/A_M2_box_M5_1e-10.json \
  --sub=1e-18,1e-26,1e-27 --out="$R/A_M2_6a_M5_sub1e-18.json" || exit 2
step lemma6a "$R/lemma6a_M5_sub1e-18.log" lemma6_jump_M.py --M=5 --box="$R/A_M2_6a_M5_sub1e-18.json" \
  --rp=0.08 --k=20 --save-B="$R/B_M5_sub1e-18.json" --json="$R/lemma6a_M5_sub1e-18.json"
step partial "$R/lemma6a_M5_sub1e-18_partial.log" lemma6_jump_M.py --M=5 --box="$R/A_M2_6a_M5_sub1e-18.json" \
  --rp=0.08 --k=20 --load-B="$R/B_M5_sub1e-18.json" --mutate=partial
echo "chain end $(date -u '+%Y-%m-%d %H:%M:%S') UTC" >> "$EX"

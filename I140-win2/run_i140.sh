#!/usr/bin/env bash
# #140: repeat-and-compare. Seven detached-in-parallel processes from one launcher: three lemma 6a(5) copies, one control
# copy with --rp=0.079, three amp_flint_par copies. PYTHONFAULTHANDLER=1 so a native crash prints its stack.
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1 PYTHONFAULTHANDLER=1
PY=/c/Users/nathan/Source/choptuik-venv/Scripts/python.exe
W=/c/Users/nathan/Source/choptuik-i140
R=C:/Users/nathan/Source/choptuik-large-d-raw
D=$R/I140-win2
EX=$D/exits.txt
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
echo "start $(stamp)" >> $EX
run() {  # run NAME DIR LOG ARGS...  (waits in a subshell, records the exit)
  local name=$1 dir=$2 log=$3; shift 3
  ( cd "$dir" || exit 9; t=$(date +%s)
    "$PY" -u "$@" > "$log" 2>&1; rc=$?
    echo "$name exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $EX ) &
}
for i in 1 2 3; do
  run l6a_copy$i $W/solver/proof $D/l6a_copy$i.log lemma6_jump_M.py --M=5 --box=$R/I104-win2/A_M2_6a_M5_sub1e-18.json \
    --rp=0.08 --k=20 --save-B=$D/B_copy$i.json --json=$D/l6a_copy$i.json
done
run l6a_control $W/solver/proof $D/l6a_control.log lemma6_jump_M.py --M=5 --box=$R/I104-win2/A_M2_6a_M5_sub1e-18.json \
  --rp=0.079 --k=20 --save-B=$D/B_control.json --json=$D/l6a_control.json
for i in 1 2 3; do
  run amp_copy$i $W/solver/inner_amp $D/amp_copy$i.log amp_flint_par.py 1.10 15 750 640 --procs 1 --fit phys --mf 6:12 \
    --out $D/amp_copy$i.json
done
wait
echo "all end $(stamp)" >> $EX

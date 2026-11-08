#!/usr/bin/env bash
# #121: lemma 6b1(5) on win2. From solver/proof/ of the I121 worktree. Normal priority, threads pinned to 1.
cd /c/Users/nathan/Source/choptuik-i121/solver/proof || exit 9
export OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 RAYON_NUM_THREADS=1
PY=/c/Users/nathan/Source/choptuik-venv/Scripts/python.exe
R=C:/Users/nathan/Source/choptuik-large-d-raw/I121-win2
EX=$R/exits.txt
X=2.71857918921174241298383648012843280883,0.99922840320656778341382852244561290493,0.14920357491144750568385993252030607895,0.01471905249025135288037099322184756733,0.00840534690576166107173716067740959800,0.00147034518159157802673581431742815600
COMMON="--M=5 --x=$X --h=1e-18 --tag=_cert"
stamp() { date -u '+%Y-%m-%d %H:%M:%S UTC'; }
echo "chain start $(stamp)" >> $EX

t0=$(date +%s)
"$PY" -u lemma6b1_cover_M.py ray --M=5 --c1 --x=$X --h=1e-18 --tag=_cert > $R/ray.log 2>&1
rc=$?; echo "ray exit $rc wall $(( $(date +%s) - t0 ))s $(stamp)" >> $EX
[ $rc -eq 0 ] || exit 1

declare -A PID T0
for n in a:0,10,15 b:1,12,16 c:2,11,13,17 d:3,4,14 e:5,6,7,8,9; do
  name=${n%%:*}; rows=${n#*:}
  T0[$name]=$(date +%s)
  "$PY" -u lemma6b1_cover_M.py rows $COMMON --only=$rows > $R/rows_$name.log 2>&1 &
  PID[$name]=$!
done
bad=0
for name in a b c d e; do
  wait ${PID[$name]}; rc=$?
  echo "rows_$name exit $rc wall $(( $(date +%s) - ${T0[$name]} ))s $(stamp)" >> $EX
  [ $rc -eq 0 ] || bad=1
done
[ $bad -eq 0 ] || { echo "rows failed, chain stopped $(stamp)" >> $EX; exit 2; }

step() {  # step NAME LOG ARGS...
  local name=$1 log=$2; shift 2; local t=$(date +%s)
  "$PY" -u lemma6b1_cover_M.py "$@" > "$log" 2>&1
  local rc=$?; echo "$name exit $rc wall $(( $(date +%s) - t ))s $(stamp)" >> $EX
}
step check $R/check.log check $COMMON --json=$R/lemma6b1_check_M5_cert.json
step check_drop_9_5 $R/check_drop_9_5.log check $COMMON --drop=9,5
step mutate_row00 $R/mutate_row00.log mutate --M=5 --j=0 --x=$X --h=1e-18 --tag=_cert
cp -r lemma6b1_runs_M5_cert $R/ && echo "copied lemma6b1_runs_M5_cert" >> $EX
echo "chain end $(stamp)" >> $EX

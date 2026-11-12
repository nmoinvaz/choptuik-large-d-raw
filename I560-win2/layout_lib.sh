# sourced by the lanes of #543 and #544
PY=/c/Users/nathan/Source/venv-t126/Scripts/python.exe
RAW=/d/choptuik-large-d-raw
J=I461-win2/crawlJ/anm_pin3_D242.3642.npz
MAIN=/d/choptuik-i446g/hp
EQ=/d/choptuik-i505/hp
export PYTHONFAULTHANDLER=1
# step FOLDER LANE NAME WORKDIR EXPECT(0|1) LOG cmd...   runs cmd, logs start and exit to FOLDER/exits.txt, stops the lane on an unexpected exit code or a Traceback
step() {
  local folder=$1 lane=$2 name=$3 wd=$4 expect=$5 log=$6; shift 6
  local R=$RAW/$folder
  cd $wd || { echo "$lane $name: no $wd" >> $R/exits.txt; exit 9; }
  echo "$lane $name start $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  "$@" > $R/$log 2>&1
  local rc=$?
  echo "$lane $name exit $rc (expected $expect) $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits.txt
  if grep -q Traceback $R/$log; then echo "$lane $name: Traceback in $log, lane stopped" >> $R/exits.txt; exit 8; fi
  if [ "$expect" = 0 ] && [ $rc -ne 0 ]; then echo "$lane $name: nonzero exit, lane stopped" >> $R/exits.txt; exit 7; fi
  if [ "$expect" = 1 ] && [ $rc -eq 0 ]; then echo "$lane $name: control did not fail, lane stopped" >> $R/exits.txt; exit 6; fi
  return 0
}
# layout FOLDER LANE TAG NODES   renode, then near_null and near_null_eq on the new start
layout() {
  local folder=$1 lane=$2 tag=$3 nodes=$4
  local R=$RAW/$folder
  step $folder $lane renode_$tag $MAIN 0 renode_$tag.log "$PY" -u renode_o.py $RAW $J $folder/renode_${tag}_D242.3642.npz --nodes $nodes --threads 2
  step $folder $lane near_null_$tag $MAIN 0 nn_$tag.log "$PY" -u near_null.py $RAW $folder/renode_${tag}_D242.3642.npz --k=4 --threads=2 --json=$R/nn_$tag.json
  step $folder $lane near_null_eq_$tag $EQ 0 eq_$tag.log "$PY" -u near_null_eq.py $RAW $folder/renode_${tag}_D242.3642.npz --plant=7 --threads=2 --json=$R/eq_$tag.json
}
# ctl_renode FOLDER LANE TAG NODES   the renode control --mutate sign (must exit 1)
ctl_renode() {
  step $1 $2 renode_$3_mut_sign $MAIN 1 renode_$3_mut.log "$PY" -u renode_o.py $RAW $J $1/renode_$3_mut.npz --nodes $4 --threads 2 --mutate sign
}
# ctl_nn FOLDER LANE TAG   the near_null control --mutate=sigma (must exit 1)
ctl_nn() {
  step $1 $2 near_null_$3_mut_sigma $MAIN 1 nn_${3}_ctl_sigma.log "$PY" -u near_null.py $RAW $1/renode_$3_D242.3642.npz --k=4 --threads=2 --mutate=sigma
}
[ "$(cd $MAIN && git rev-parse --short=7 HEAD)" = "14dc386" ] || { echo "D:/choptuik-i446g is not at 14dc386" >&2; exit 9; }
[ "$(cd $EQ && git rev-parse --short=7 HEAD)" = "0cce81e" ] || { echo "D:/choptuik-i505 is not at 0cce81e" >&2; exit 9; }

#!/bin/bash
# #847, the second part (the coordinator): the d2check controls of proof/A_M2.md section 7 that run847.sh left out.
# M = 1: box runs at h 1e-9 with --mutate=none, lin2 and w0, then d2check on each (none passes; lin2 and w0 must fail).
# M = 3: box runs with --mutate=lin2 and chart, then d2check on each (both must fail). Two processes at a time.
R=/home/nathan/Source/choptuik-large-d-raw/I847-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-847
cd $WT/solver/proof || exit 9
log() { echo "847b $1 $(date -u '+%F %T') UTC" >> $R/exits_847.txt; }
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
m1() {  # T
  run run box1_d2_$1 certify_M2.py box 1 --chart=data/A_M2_chart_M1.json --h=1e-9 --w=0 --mutate=$1 \
    --out=$R/A_M2_box_M1_1e-9_d2_$1.json --log=$R/A_M2_box_M1_1e-9_d2_$1.log
}
m3() {  # T
  run run box3_mut_$1 certify_M2.py box 3 --chart=data/A_M2_chart_M3.json --h=1e-8 --w=1e-13 --mutate=$1 \
    --out=$R/A_M2_box_M3_1e-8_mut_$1.json --log=$R/A_M2_box_M3_1e-8_mut_$1.log
}
m3 lin2 & m3 chart &
m1 none; m1 lin2; m1 w0
wait
run run  d2check1_none  certify_M2.py d2check --box=$R/A_M2_box_M1_1e-9_d2_none.json --fd=data/A_M2_fd_M1.json
run ctrl d2check1_lin2  certify_M2.py d2check --box=$R/A_M2_box_M1_1e-9_d2_lin2.json --fd=data/A_M2_fd_M1.json
run ctrl d2check1_w0    certify_M2.py d2check --box=$R/A_M2_box_M1_1e-9_d2_w0.json --fd=data/A_M2_fd_M1.json
run ctrl d2check3_lin2  certify_M2.py d2check --box=$R/A_M2_box_M3_1e-8_mut_lin2.json --fd=data/A_M2_fd_M3.json
run ctrl d2check3_chart certify_M2.py d2check --box=$R/A_M2_box_M3_1e-8_mut_chart.json --fd=data/A_M2_fd_M3.json
log "all done"

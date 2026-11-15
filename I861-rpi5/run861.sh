#!/bin/bash
# #861 on rpi5 (the coordinator): Theorem A(M = 5)'s remaining lemmas reproduced on aarch64 Linux. Step (i)'s tables,
# lemma S with the old sector lemma and the flat estimate (and its series control), lemma S's scan, and lemma 6a(5) at
# the certificate's p^ with #184's commands (I184-macm3/run_i184.sh) and controls, then macm3's stored B on the Pi.
# Every output goes to the raw folder, so the stored lemmas_M_runs/ files stay as they are. One process at a time.
R=/home/nathan/Source/choptuik-large-d-raw/I861-rpi5
RAW=/home/nathan/Source/choptuik-large-d-raw
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-861
cd $WT/solver/proof || exit 9
mkdir -p $R
log() { echo "861 $1 $(date -u '+%F %T') UTC" >> $R/exits_861.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  nice -n 10 $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
# step (i), lemma S, the old sector lemma and the flat estimate
run run  fpm_table5    fixed_point_M.py --table --Ms=5 --json=$R/fixed_point_M_table_M5.json
run run  fpm_data5     fixed_point_M.py --data-table --Ms=5 --json=$R/fixed_point_M_data_M5.json
run run  sector5       lemma6_sector_M.py --M=5 --rp=0.08 --k=20 --box=1e-6 --Z=0.004489 --json=$R/lemma6_sector_M5_rp0.08_1e-6.json
run ctrl sector5_series lemma6_sector_M.py --M=5 --rp=0.08 --k=20 --box=1e-6 --mutate=series
run run  scan5         lemma6_sector_M.py --M=5 --scan --json=$R/lemmaS_scan_M5.json
# lemma 6a(5) at p^ (#184), its controls, and #39's float control of B
BOX=$RAW/I103-macm3/A_M2_6a_M5_sub1e-18.json
[ -f $BOX ] || { log "STOP: no $BOX (pull the raw clone first)"; exit 9; }
PHAT=$($PY -c "import json; print(','.join(json.load(open('$BOX'))['p']))")
echo "$PHAT" > $R/centre_passed.txt
J="--M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20"
run run  jump5         lemma6_jump_M.py $J --save-B=$R/B_M5_sub1e-18_phat.json --json=$R/lemma6a_M5_sub1e-18_phat.json
[ -s $R/B_M5_sub1e-18_phat.json ] || { log "STOP: no B saved, controls not run"; exit 9; }
run ctrl jump5_partial lemma6_jump_M.py $J --load-B=$R/B_M5_sub1e-18_phat.json --mutate=partial
run ctrl jump5_coords  lemma6_jump_M.py $J --load-B=$R/B_M5_sub1e-18_phat.json --mutate=coords
run ctrl jump5_swap    lemma6_jump_M.py $J --mutate=swap
run run  bfloat        review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX
run ctrl bfloat_w      review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX --mutate=w
# the cross-load: macm3's stored B (I184-macm3) on the Pi
run run  jump5_macB    lemma6_jump_M.py $J --load-B=$RAW/I184-macm3/B_M5_sub1e-18_phat.json --json=$R/lemma6a_M5_macB.json
log "all done"

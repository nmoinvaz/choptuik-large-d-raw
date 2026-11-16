#!/bin/bash
# #876 on winb (the coordinator): Theorem A's M = 3 lemma set (#849's commands, plus lemma 6a(3) at the certificate's
# box) and the rest of the M = 5 set (#861's) on Windows x86-64, for Git Bash. The covering of 6b1(3) is computed under
# the tag _winb, so no stored row is reused. Every output goes to the raw folder. Only the three path lines below may be
# changed to match the machine; nothing else.
WT=/c/Users/nathan/Source/choptuik-i876
PY=/c/Users/nathan/Source/venv-choptuik-314/Scripts/python.exe
RAW=/c/Users/nathan/Source/choptuik-large-d-raw-754
R=$RAW/I876-winb
export PYTHONUTF8=1
cd $WT/solver/proof || exit 9
mkdir -p $R
log() { echo "876 $1 $(date -u '+%F %T') UTC" >> $R/exits_876.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__, platform.platform(), platform.machine(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(( $(date +%s) - t )) s ($kind)"
}
# --- lemma 6b1(3) at the certificate's box (#849), own tag
P=2.7264758856311463335934955261561100705557331671411,1.0156030948577872100059533565790022881883333496973,0.14441947847010155933389143095194965903793037966287,0.011087425888116783540971263261694760868044985018780
C="--M=3 --h=1.1e-9 --tag=_winb --x=$P"
[ -e lemma6b1_runs_M3_winb ] && { log "STOP: lemma6b1_runs_M3_winb exists already"; exit 9; }
run run cover_ray    lemma6b1_cover_M.py ray --c1 $C &
run run cover_row11  lemma6b1_cover_M.py row $C --j=11 &
run run cover_rows_a lemma6b1_cover_M.py rows $C --only=0,2,4,6,8,10 &
run run cover_rows_b lemma6b1_cover_M.py rows $C --only=1,3,5,7,9 &
wait
run run  cover_check          lemma6b1_cover_M.py check $C --json=$R/lemma6b1_check_M3_winb.json
run run  cover_c1check        lemma6b1_cover_M.py c1check $C
run ctrl cover_c1check_mut    lemma6b1_cover_M.py c1check --mutate=nov $C
run ctrl cover_check_drop11_0 lemma6b1_cover_M.py check $C --drop=11,0
cp -r lemma6b1_runs_M3_winb $R/
# --- step (i), lemma S and D at M = 3 (#849)
run run usys_M         lemma6_usys_M.py
run run fpm_check_m1   fixed_point_M.py --check-m1
run run fpm_M3         fixed_point_M.py --M=3
run run fpm_M3_diag    fixed_point_M.py --M=3 --diag --r0=0.0741 --arg=5pi/16 --cbox=1e-3
run run fpm_table_M3   fixed_point_M.py --table --Ms=3 --json=$R/fixed_point_M_table_M3.json
run run fpm_data_M3    fixed_point_M.py --data-table --Ms=3 --json=$R/fixed_point_M_data_M3.json
run run sector_scan_M3 lemma6_sector_M.py --M=3 --scan --json=$R/lemmaS_scan_M3.json
run run sector_M3      lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --json=$R/lemma6_sector_M3_rp0.1_1e-6.json
run run disc_M         lemma6b1_disc_M.py
run run mutations_M    mutations_M.py --all
# --- lemma 6a(3) at the certificate's box (A_lemmas_M.md 7)
run run jump3          lemma6_jump_M.py --M=3 --box=data/A_M_6a_M3_1e-10_in.json --json=$R/lemma6a_M3_cert.json
# --- the rest of the M = 5 set (#861)
run run  fpm_table5    fixed_point_M.py --table --Ms=5 --json=$R/fixed_point_M_table_M5.json
run run  fpm_data5     fixed_point_M.py --data-table --Ms=5 --json=$R/fixed_point_M_data_M5.json
run run  sector5       lemma6_sector_M.py --M=5 --rp=0.08 --k=20 --box=1e-6 --Z=0.004489 --json=$R/lemma6_sector_M5_rp0.08_1e-6.json
run run  scan5         lemma6_sector_M.py --M=5 --scan --json=$R/lemmaS_scan_M5.json
BOX=$RAW/I103-macm3/A_M2_6a_M5_sub1e-18.json
[ -f $BOX ] || { log "STOP: no $BOX"; exit 9; }
PHAT=$($PY -c "import json; print(','.join(json.load(open(r'$(cygpath -w $BOX 2>/dev/null || echo $BOX)'))['p']))")
echo "$PHAT" > $R/centre_passed.txt
J="--M=5 --box=$BOX --x=$PHAT --rp=0.08 --k=20"
run run  jump5         lemma6_jump_M.py $J --save-B=$R/B_M5_sub1e-18_phat.json --json=$R/lemma6a_M5_sub1e-18_phat.json
[ -s $R/B_M5_sub1e-18_phat.json ] || { log "STOP: no B saved, controls not run"; exit 9; }
run ctrl jump5_partial lemma6_jump_M.py $J --load-B=$R/B_M5_sub1e-18_phat.json --mutate=partial
run ctrl jump5_coords  lemma6_jump_M.py $J --load-B=$R/B_M5_sub1e-18_phat.json --mutate=coords
run ctrl jump5_swap    lemma6_jump_M.py $J --mutate=swap
run run  bfloat        review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX
run ctrl bfloat_w      review_39/b_float.py --B=$R/B_M5_sub1e-18_phat.json --box=$BOX --mutate=w
run run  jump5_macB    lemma6_jump_M.py $J --load-B=$RAW/I184-macm3/B_M5_sub1e-18_phat.json --json=$R/lemma6a_M5_macB.json
run run  jump5_piB     lemma6_jump_M.py $J --load-B=$RAW/I861-rpi5/B_M5_sub1e-18_phat.json --json=$R/lemma6a_M5_piB.json
log "all done"

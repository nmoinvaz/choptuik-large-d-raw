#!/bin/bash
# #849 on rpi5 (the coordinator): the lemmas around Theorem A(M = 3)'s point certificate (proof/A_lemmas_M.md section
# 10) reproduced on aarch64 Linux: step (i), lemma S and lemma 6b1's covering on the certificate's box, with the
# controls. The covering runs under the tag _rpi5, so every row is computed here (rows skips a row whose file exists,
# and the stored x86 rows are under _cert). The JSON outputs that the commands write into lemmas_M_runs/ overwrite the
# stored x86 files in this worktree; git diff --stat at the end lists the ones that differ. Up to 4 processes.
R=/home/nathan/Source/choptuik-large-d-raw/I849-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-849
cd $WT/solver/proof || exit 9
mkdir -p $R
log() { echo "849 $1 $(date -u '+%F %T') UTC" >> $R/exits_849.txt; }
{
  echo "commit $(git rev-parse --short=8 HEAD)"
  $PY -c "import flint, numpy, mpmath, scipy, sys, platform; print('python-flint', flint.__version__, 'FLINT', flint.__FLINT_VERSION__, 'numpy', numpy.__version__, 'mpmath', mpmath.__version__, 'scipy', scipy.__version__, platform.platform(), 'python', sys.version.split()[0])"
} > $R/env.txt 2>&1
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
P=2.7264758856311463335934955261561100705557331671411,1.0156030948577872100059533565790022881883333496973,0.14441947847010155933389143095194965903793037966287,0.011087425888116783540971263261694760868044985018780
C="--M=3 --h=1.1e-9 --tag=_rpi5 --x=$P"
# the covering: the C1 ray run, the hardest row (11) and the other eleven rows in two lists, four processes at once
run run cover_ray   lemma6b1_cover_M.py ray --c1 $C &
run run cover_row11 lemma6b1_cover_M.py row $C --j=11 &
run run cover_rows_a lemma6b1_cover_M.py rows $C --only=0,2,4,6,8,10 &
run run cover_rows_b lemma6b1_cover_M.py rows $C --only=1,3,5,7,9 &
wait
run run cover_check   lemma6b1_cover_M.py check $C --json=$R/lemma6b1_check_M3_rpi5.json
run run cover_c1check lemma6b1_cover_M.py c1check $C
run ctrl cover_c1check_mut lemma6b1_cover_M.py c1check --mutate=nov $C
run ctrl cover_check_drop11_0 lemma6b1_cover_M.py check $C --drop=11,0
cp -r lemma6b1_runs_M3_rpi5 $R/
# step (i), lemma S and the disc lemma, one process
run run usys_M          lemma6_usys_M.py
run run fpm_check_m1    fixed_point_M.py --check-m1
run run fpm_M3          fixed_point_M.py --M=3
run run fpm_M3_diag     fixed_point_M.py --M=3 --diag --r0=0.0741 --arg=5pi/16 --cbox=1e-3
run run fpm_table_M3    fixed_point_M.py --table --Ms=3 --json=lemmas_M_runs/fixed_point_M_table_M3.json
run run fpm_table_M5    fixed_point_M.py --table --Ms=5 --json=lemmas_M_runs/fixed_point_M_table_M5.json
run run fpm_data_M3     fixed_point_M.py --data-table --Ms=3 --json=lemmas_M_runs/fixed_point_M_data_M3.json
run run sector_scan_M3  lemma6_sector_M.py --M=3 --scan --json=lemmas_M_runs/lemmaS_scan_M3.json
run run sector_M3       lemma6_sector_M.py --M=3 --rp=0.1 --k=20 --box=1e-6 --Z=0.004489 --json=lemmas_M_runs/lemma6_sector_M3_rp0.1_1e-6.json
run run sector_M5       lemma6_sector_M.py --M=5 --rp=0.08 --k=20 --box=1e-6 --Z=0.004489 --json=lemmas_M_runs/lemma6_sector_M5_rp0.08_1e-6.json
run run disc_M          lemma6b1_disc_M.py
run run mutations_M     mutations_M.py --all
mkdir -p $R/lemmas_M_runs
for f in fixed_point_M_table_M3 fixed_point_M_table_M5 fixed_point_M_data_M3 lemmaS_scan_M3 lemma6_sector_M3_rp0.1_1e-6 lemma6_sector_M5_rp0.08_1e-6; do
  cp lemmas_M_runs/$f.json $R/lemmas_M_runs/
done
git diff --stat > $R/diff_against_stored.txt 2>&1
git status --short >> $R/diff_against_stored.txt 2>&1
log "all done"

#!/bin/bash
# #873 on rpi5 (the coordinator): Theorem A(M = 1)'s lemmas S, 6a and 6b1 reproduced on aarch64 Linux, with the
# commands of proof/A_certify.md 11.7 and 12. Outputs go to the raw folder. lemma6b1_cover.py's ray and rows write the
# worktree's lemma6b1_runs/, so the stored covering is checked first and the folder is copied out at the end.
R=/home/nathan/Source/choptuik-large-d-raw/I873-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-873
cd $WT/solver/proof || exit 9
mkdir -p $R
log() { echo "873 $1 $(date -u '+%F %T') UTC" >> $R/exits_873.txt; }
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
# lemma S, the old sector lemma and the flat estimate (11.3-11.5)
run run  sector        lemma6_sector.py --json=$R/lemma6_sector_1e-9.json
run ctrl sector_series lemma6_sector.py --mutate=series
run run  usys          lemma6_usys.py
# lemma 6a: the lower path and the backward jump (11.6)
run run  path_point    lemma6_path.py point --out=$R/lemma6_path_point.json
run run  path_box      lemma6_path.py box --h=1e-9 --out=$R/lemma6_path_box_1e-9.json
run run  path_krawczyk lemma6_path.py krawczyk --point=$R/lemma6_path_point.json --box=$R/lemma6_path_box_1e-9.json
run run  jump          lemma6_jump.py --box=$R/lemma6_path_box_1e-9.json --json=$R/lemma6_jump_1e-9.json
run run  jump_stored   lemma6_jump.py --box=lemma6_path_box_1e-9.json --json=$R/lemma6_jump_stored_box.json
run ctrl jump_swap     lemma6_jump.py --box=$R/lemma6_path_box_1e-9.json --mutate=swap
run ctrl jump_coords   lemma6_jump.py --box=$R/lemma6_path_box_1e-9.json --mutate=coords
# lemma 6b1 (12): the stored covering on the Pi first, then the Pi's own
run run  disc               lemma6b1_disc.py
run run  cover_check_stored lemma6b1_cover.py check
run run  cover_ray          lemma6b1_cover.py ray
[ -f lemma6b1_runs/ray.json ] || { log "STOP: no ray.json"; exit 9; }
run run  cover_rows         lemma6b1_cover.py rows
run run  cover_check        lemma6b1_cover.py check --json=$R/lemma6b1_check_1e-9.json
mkdir -p $R/lemma6b1_runs_rpi5 && cp lemma6b1_runs/*.json $R/lemma6b1_runs_rpi5/ 2>> $R/exits_873.txt
run ctrl cover_sign         lemma6b1_cover.py --mutate=sign
run ctrl cover_drop         lemma6b1_cover.py check --drop=5,6
run ctrl cover_control      lemma6b1_cover.py control
log "all done"

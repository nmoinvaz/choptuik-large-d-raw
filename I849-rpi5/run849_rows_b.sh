#!/bin/bash
# #849 on rpi5 (rpi5 runner, approved by the coordinator): run849.sh started the three covering row jobs at the same
# time as the C1 ray run, so they exited 1 (no ray.json). This runs the same commands after cover_ray has exited, then
# the check and control commands again, every name ending _b. Same arguments, tag and logging as run849.sh.
R=/home/nathan/Source/choptuik-large-d-raw/I849-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-849
cd $WT/solver/proof || exit 9
log() { echo "849 $1 $(date -u '+%F %T') UTC" >> $R/exits_849.txt; }
until grep -q '^849 cover_ray exit' $R/exits_849.txt; do sleep 5; done
[ -f lemma6b1_runs_M3_rpi5/ray.json ] || { log "rows_b aborted, no ray.json"; exit 8; }
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
run run cover_row11_b   lemma6b1_cover_M.py row $C --j=11 &
run run cover_rows_a_b  lemma6b1_cover_M.py rows $C --only=0,2,4,6,8,10 &
run run cover_rows_b_b  lemma6b1_cover_M.py rows $C --only=1,3,5,7,9 &
wait
run run  cover_check_b            lemma6b1_cover_M.py check $C --json=$R/lemma6b1_check_M3_rpi5_b.json
run run  cover_c1check_b          lemma6b1_cover_M.py c1check $C
run ctrl cover_c1check_mut_b      lemma6b1_cover_M.py c1check --mutate=nov $C
run ctrl cover_check_drop11_0_b   lemma6b1_cover_M.py check $C --drop=11,0
cp -r lemma6b1_runs_M3_rpi5 $R/
log "rows_b all done"

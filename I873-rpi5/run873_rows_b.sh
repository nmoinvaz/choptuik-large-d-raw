#!/bin/bash
# #873 on rpi5 (rpi5 runner; to run only once the coordinator approves): run873.sh's cover_rows exited 0 in 0.19 s because
# lemma6b1_cover.py rows skips rows whose lemma6b1_runs/row_JJ.json exists, and the worktree holds the stored rows. This
# runs `row --j=J` (it recomputes the row) for J = 0..11, one process at a time at nice 10 like run873.sh, then the check
# and the drop control again, every name ending _b. No file is deleted.
R=/home/nathan/Source/choptuik-large-d-raw/I873-rpi5
PY=/home/nathan/Source/venv-choptuik/bin/python
WT=/home/nathan/Source/choptuik-large-d-873
cd $WT/solver/proof || exit 9
log() { echo "873 $1 $(date -u '+%F %T') UTC" >> $R/exits_873.txt; }
run() {  # kind (run|ctrl), name, then the command's arguments
  local kind=$1 name=$2; shift 2
  log "$name start ($kind)"
  local t=$(date +%s.%N)
  nice -n 10 $PY -u "$@" > $R/$name.log 2>&1
  local rc=$?
  log "$name exit $rc wall $(echo "$(date +%s.%N) - $t" | bc) s ($kind)"
}
log "rows_b begin"
for j in 0 1 2 3 4 5 6 7 8 9 10 11; do
  run run $(printf 'rows_%02d_b' $j) lemma6b1_cover.py row --j=$j
done
run run  cover_check_b lemma6b1_cover.py check --json=$R/lemma6b1_check_1e-9_b.json
mkdir -p $R/lemma6b1_runs_rpi5b && cp lemma6b1_runs/*.json $R/lemma6b1_runs_rpi5b/ 2>> $R/exits_873.txt
run ctrl cover_drop_b  lemma6b1_cover.py check --drop=5,6
log "rows_b all done"

#!/usr/bin/env bash
# #743: s132's first Newton step (rung ks 132 at D 245.1366, from r131k's base, with #696's single-order ladder flags and
# --keep_plan 0), rerun with --log_proj 1 (one line per failed ElimO projection, main 624e7236) and --qd_it 1, so only the
# first step runs. Worktree D:/choptuik-i743 at main 807d74d8 (since #696's 16cfdfec only 1fc37c03 and 624e7236 touch
# anm_run.py, octo_corrector.py, reseed.py and hp/src), venv-i600 (s132's build). anm_run.py takes the FIRST occurrence of
# an option, so --qd_it and --log_proj are given once, in FLAGS.
PY=/c/Users/nathan/Source/venv-i600/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I743-win2
cd /d/choptuik-i743/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "807d74d8" ] || { echo "worktree is not at 807d74d8" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
log() { echo "$1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_743.txt; }
# the plant of the log line: projlog must pass, and each mutation must fail
"$PY" -u reseed.py projlog > $R/projlog.log 2>&1; log "743 projlog exit $? (must be 0)"
"$PY" -u reseed.py projlog --mutate=silent > $R/projlog_silent.log 2>&1; log "743 projlog --mutate=silent exit $? (must be 1)"
"$PY" -u reseed.py projlog --mutate=stage > $R/projlog_stage.log 2>&1; log "743 projlog --mutate=stage exit $? (must be 1)"
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --tol_od 1e-60 --qd_it 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --keep_plan 0 --log_proj 1"
for o in qd_it keep_plan log_proj; do [ "$(echo "$FLAGS" | grep -o -e "--$o " | wc -l)" = 1 ] || { log "743 --$o not exactly once in FLAGS"; exit 9; }; done
mkdir -p $R/s132p
log "743 s132p start, state I696-win2/D245/r131k/base_pin3_D245.1366.npz ks 132"
"$PY" -u anm_run.py $RAW $R/s132p --state I696-win2/D245/r131k/base_pin3_D245.1366.npz $FLAGS --ks 132 > $R/s132p.log 2>&1
log "743 s132p exit $?"
# the checks: the step-0 lines against s132's, the line count against the failed count, a stage named on every line
"$PY" -I $R/compare_743.py $RAW/I696-win2/D245/s132.log $R/s132p.log > $R/compare_743.txt 2>&1; log "743 compare exit $? (must be 0)"
"$PY" -I $R/compare_743.py $RAW/I696-win2/D245/s132.log $R/s132p.log --mutate=drop > $R/compare_743_drop.txt 2>&1; log "743 compare --mutate=drop exit $? (must be 1)"
"$PY" -I $R/compare_743.py $RAW/I696-win2/D245/s132.log $R/s132p.log --mutate=count > $R/compare_743_count.txt 2>&1; log "743 compare --mutate=count exit $? (must be 1)"
log "743 all done"

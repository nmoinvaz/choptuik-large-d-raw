#!/usr/bin/env bash
# #797: two rungs of the order-132 climb at D 245.1366 between #783's: w = 13/32 from #783's w = 3/8 base and w = 15/32
# from its w = 7/16 base, run_783.sh's flags at 5 threads (beside #603 and #796). Worktree D:/choptuik-i744 at wip/i744
# c6468d2b, venv-i744.
PY=/c/Users/nathan/Source/venv-i744/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I797-win2
cd /d/choptuik-i744/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "c6468d2b" ] || { echo "worktree is not at c6468d2b" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 5 --corrector od --tol_od 1e-60 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --log_proj 1"
log() { echo "797 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_797.txt; }
converged() { grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1 | grep -q ", converged"; }
rel() { b=$(ls $RAW/$1/base_pin3_D*.npz 2>/dev/null | head -n 1); echo "${b#$RAW/}"; }
run() {  # tag state w
  mkdir -p $R/$1
  log "$1 start, state $2, ks_w $3"
  "$PY" -u anm_run.py $RAW $R/$1 --state $2 $FLAGS --qd_it 20 --ks 132 --ks_w $3 > $R/$1.log 2>&1
  log "$1 exit $? converged: $(converged $R/$1.log && echo yes || echo NO)"
}
run w40625 $(rel I783-win2/w375) 0.40625
run w46875 $(rel I783-win2/w4375) 0.46875
"$PY" -I $R/table_797.py $R > $R/table_797.txt 2>&1; log "table exit $?"
log "all done"

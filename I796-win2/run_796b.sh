#!/usr/bin/env bash
# #796, the resumption (run_796b.sh): w = 3/4 again from w75's saved (stalled) base with up to 40 steps (w75r), then w875
# and w1, each from the last's base, stopping at the first that does not converge, then cold1 (--qd_it 2, at most 2
# steps); run_783.sh's flags at 10 threads. Worktree D:/choptuik-i744 at wip/i744 c6468d2b, venv-i744.
PY=/c/Users/nathan/Source/venv-i744/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I796-win2
cd /d/choptuik-i744/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "c6468d2b" ] || { echo "worktree is not at c6468d2b" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --tol_od 1e-60 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --log_proj 1"
log() { echo "796 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_796.txt; }
converged() { grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1 | grep -q ", converged"; }
base_of() { ls $1/base_pin3_D*.npz 2>/dev/null | head -n 1; }
rel() { b=$(base_of $RAW/$1); echo "${b#$RAW/}"; }
run() {  # tag state w qd_it
  mkdir -p $R/$1
  log "$1 start, state $2, ks_w $3, qd_it $4"
  "$PY" -u anm_run.py $RAW $R/$1 --state $2 $FLAGS --qd_it $4 --ks 132 --ks_w $3 > $R/$1.log 2>&1
  log "$1 exit $? converged: $(converged $R/$1.log && echo yes || echo NO)"
}
b=$(rel I796-win2/w75); [ -n "$b" ] || { log "no w75 base"; exit 9; }
run w75r $b 0.75 40
prev=I796-win2/w75r
if converged $R/w75r.log; then
  for w in 0.875 1; do
    tag=w${w#0.}; [ "$w" = 1 ] && tag=w1
    b=$(rel $prev); [ -n "$b" ] || { log "$tag: no base from $prev, the climb stops"; break; }
    run $tag $b $w 20
    converged $R/$tag.log || { log "$tag did not converge, the climb stops"; break; }
    prev=I796-win2/$tag
  done
else
  log "w75r did not converge, the climb stops"
fi
if converged $R/w1.log 2>/dev/null; then run cold1 $(rel I796-win2/w1) 1 2; fi
"$PY" -I $R/table_796.py $R > $R/table_796.txt 2>&1; log "table exit $?"
log "all done"

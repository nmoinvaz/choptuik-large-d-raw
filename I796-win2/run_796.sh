#!/usr/bin/env bash
# #796: the order-132 climb from #783's w = 1/2 base to w = 1 at D 245.1366, run_783.sh's flags, 6 threads: w625, w75,
# w875 and w1, each from the last's base, stopping at the first that does not converge; then cold1, a polish of w1's base
# at w = 1 (--qd_it 2), which must converge in at most 2 steps. Worktree D:/choptuik-i744 at wip/i744 c6468d2b, venv-i744.
PY=/c/Users/nathan/Source/venv-i744/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I796-win2
cd /d/choptuik-i744/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "c6468d2b" ] || { echo "worktree is not at c6468d2b" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 6 --corrector od --tol_od 1e-60 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1 --log_proj 1"
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
prev=I783-win2/w5b
for w in 0.625 0.75 0.875 1; do
  tag=w${w#0.}; [ "$w" = 1 ] && tag=w1
  b=$(rel $prev); [ -n "$b" ] || { log "$tag: no base from $prev, the climb stops"; break; }
  run $tag $b $w 20
  converged $R/$tag.log || { log "$tag did not converge, the climb stops"; break; }
  prev=I796-win2/$tag
done
if converged $R/w1.log 2>/dev/null; then run cold1 $(rel I796-win2/w1) 1 2; fi
"$PY" -I $R/table_796.py $R > $R/table_796.txt 2>&1; log "table exit $?"
log "all done"

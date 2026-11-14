#!/usr/bin/env bash
# #744: the homotopy in the horizon order at D 245.1366, from #696's r131k base (ks 131): the order-132 term weighted w
# (anm_run.py --ks 132 --ks_w W), w = 1/16, 1/8, 1/4, 1/2, 1, each rung from the last's base, with s132's flags
# (I696-win2/run_696_single.sh). Worktree D:/choptuik-i744 at wip/i744 c6468d2b, venv-i744 (its own hp build), 10 threads.
#   control  c131 (--ks 131 --keep_plan 0) and w0 (--ks 132 --ks_w 0, which plans again as a changed ks does) from
#            r131k's base: Delta must agree to 1e-40, since w = 0 is order 131 bit for bit;
#   ladder   w0625 from w0's base, w125 from w0625's, ... w1 from w5's (each keeps the plan of the rung before);
#   mutation jump: --ks 132 --ks_w 1 from r131k's base, its first Newton step only (--qd_it 1), which must reproduce
#            s132's first full step, max|F| about 1.18e20.
# A rung that does not converge stops the ladder (its log and the exits line say so).
PY=/c/Users/nathan/Source/venv-i744/Scripts/python.exe
RAW=/d/choptuik-large-d-raw; R=$RAW/I744-win2
cd /d/choptuik-i744/hp || exit 9
[ "$(git rev-parse --short=8 HEAD)" = "c6468d2b" ] || { echo "worktree is not at c6468d2b" >&2; exit 9; }
"$PY" -c "import sys; from hpkernel._hpkernel import Solver; sys.exit(0 if hasattr(Solver, 'set_ks_w') else 1)" || { echo "this venv's hpkernel has no set_ks_w: build it first" >&2; exit 9; }
export PYTHONFAULTHANDLER=1 OPENBLAS_NUM_THREADS=1
FLAGS="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --steps 0 --threads 10 --corrector od --tol_od 1e-60 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --od_accept natural --od_strong 4 --reseed_start pred --save_base 1 --base_adopt 1"
log() { echo "744 $1 $(date -u '+%Y-%m-%d %H:%M:%S UTC')" >> $R/exits_744.txt; }
converged() { grep -E "octo-double Newton: [0-9]+ steps" "$1" | tail -n 1 | grep -q ", converged"; }
base_of() { ls $R/$1/base_pin3_D*.npz 2>/dev/null | head -n 1; }
run() {  # tag state qd_it extra...
  local tag=$1 st=$2 qi=$3; shift 3
  mkdir -p $R/$tag
  log "$tag start, state $st, $*"
  "$PY" -u anm_run.py $RAW $R/$tag --state $st $FLAGS --qd_it $qi "$@" > $R/$tag.log 2>&1
  local rc=$?
  log "$tag exit $rc converged: $(converged $R/$tag.log && echo yes || echo NO)"
  return $rc
}
B0=I696-win2/D245/r131k/base_pin3_D245.1366.npz
run c131 $B0 20 --ks 131 --keep_plan 0
run w0 $B0 20 --ks 132 --ks_w 0
"$PY" -I $R/compare_744.py control $R > $R/control_744.txt 2>&1; log "control compare exit $? (must be 0)"
prev=w0
for w in 0.0625 0.125 0.25 0.5 1; do
  tag=w${w#0.}; [ "$w" = 1 ] && tag=w1
  b=$(base_of $prev); [ -n "$b" ] || { log "$tag: no base from $prev, the ladder stops"; break; }
  run $tag "I744-win2/$prev/$(basename $b)" 20 --ks 132 --ks_w $w
  converged $R/$tag.log || { log "$tag did not converge, the ladder stops"; break; }
  prev=$tag
done
run jump $B0 1 --ks 132 --ks_w 1 --keep_plan 0
"$PY" -I $R/compare_744.py table $R > $R/table_744.txt 2>&1; log "table exit $?"
log "all done"

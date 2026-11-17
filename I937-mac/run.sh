#!/bin/bash
# #937: run.sh NAME [ANM_ARGS...] runs run937.py (anm_run.py of the worktree choptuik-large-d-937 at fe489b42, with
# the logging wrappers) from D 234 of dh610's order-160 chain with chain_k160's flags (run903c.sh, raw I903-dh610),
# --threads 3 instead of 10, --steps 1, on the site2 hpkernel (main 3c35f0c's build, no series_o, no
# set_octo_tangents: the series by jets and one tangent per Jacobian evaluation, the same bits). Output OUT = NAME/,
# log NAME.log, nice 10, at most 4 h (gtimeout; exit 124 when it stops).
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad
IN=$S/raw903in
HP=/Users/nathan/Source/choptuik-large-d-937/hp
SITE=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
PY=/Users/nathan/venv-314/bin/python3
O=$(cd "$(dirname "$0")" && pwd)
name=$1; shift
F="--kfreeze 3 --held_fit data/held_fit.json --N 24 --eps 1e-14 --h_max 1.0 --threads 3 --corrector od --tol_od 1e-60 --qd_it 20 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_pred 1 --od_accept natural --save_jet 1 --od_strong 4 --reseed_start pred"
cd "$HP" || exit 9
{
  echo "== $name $(date -u '+%Y-%m-%d %H:%M:%S') UTC, hp at $(git rev-parse --short=8 HEAD)$(git diff --quiet HEAD -- . || echo '+dirty'), args: $*"
  OPENBLAS_NUM_THREADS=1 PYTHONPATH=$SITE PYTHONFAULTHANDLER=1 nice -n 10 gtimeout 4h "$PY" -u "$O/run937.py" "$IN" "$O/$name" \
    --state I903-dh610/chain_k160/anm_pin3_D234.0000.npz $F --ks 160 --keep_plan 1 --steps 1 --D_max 262 "$@"
  echo "exit $?"
  echo "== end $(date -u '+%Y-%m-%d %H:%M:%S') UTC"
} > "$O/$name.log" 2>&1

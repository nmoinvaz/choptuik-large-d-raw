#!/usr/bin/env bash
# #636 at D 200 and 240.12, from 2026-11-13 08:12 UTC: 2 threads at nice 10 (the coordinator's cap), 4 corrector steps,
# 1 polish step, at most 2 halvings of a Newton step (at the quad-double floor each trial is a full residual and LU, about
# 4 min at M 32 and longer at M 48). D 240.12 skips the M 32 solve (--m32=0): its stored state is the octo-double
# chain's, which the quad-double path can only move by its floor, so the difference is taken against the stored state.
# Usage: run_i636_large.sh STEP... (d200 d240 dd20_D). Each step appends its command and exit status to exits.txt.
PY=/Users/nathan/venv-314/bin/python3
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i636
F=$RAW/I636-mac
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a85c4feb2fd2f0829/hp
cd $HP || exit 9
run() {
  local log=$1; shift
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') start: chain_dM.py $*" >> $F/exits.txt
  nice -n 10 $PY -u chain_dM.py "$@" > $log 2>&1
  local rc=$?
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') exit $rc: chain_dM.py $*" >> $F/exits.txt
  return $rc
}
LARGE="--threads=2 --it=4 --polish_it=1 --halvings=2"
for step in "$@"; do
  case $step in
    d200) run $F/chain/d200.log run $RAW $F/chain T138-win2/chain_o/anm_pin3_D200.0000.npz $LARGE ;;
    d240) run $F/chain/d240.log run $RAW $F/chain I603-win2/chain/anm_pin3_D240.1244.npz $LARGE --m32=0 ;;
    dd20_D) run $F/controls/planted_dd20_D.log planted $RAW $F/controls --threads=2 --only=dd20 --reseed=0 --m32=0 --mutate=D ;;
    *) echo "unknown step $step" >&2; exit 9 ;;
  esac
done

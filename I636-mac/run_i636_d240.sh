#!/usr/bin/env bash
# #636 at D 240.12 from 2026-11-13 10:12 UTC, and the dd20 plant's --mutate=D control: 2 threads at nice 10. D 240.12
# takes one M 48 corrector step (--it=1, no halving, no polish): its first step reached the quad-double floor
# (d240_it4_stopped.log), and the floor steps that follow cost about 10 min a trial for moves below the floor's bound.
# M 32 is not solved (--m32=0): the difference is taken against the stored octo-double state.
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
run $F/chain/d240.log run $RAW $F/chain I603-win2/chain/anm_pin3_D240.1244.npz --threads=2 --it=1 --polish_it=0 --halvings=0 --m32=0
run $F/controls/planted_dd20_D.log planted $RAW $F/controls --threads=2 --only=dd20 --reseed=0 --m32=0 --mutate=D

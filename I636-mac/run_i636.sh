#!/usr/bin/env bash
# #636 runs on the Mac, one at a time, nice 10, 5 threads: the pinned plant at D 80 (re-seed and elimination), then the
# chain states in order D 100 (the pilot), 150, 200, 240.12. Usage: run_i636.sh STEP... (planted80 d100 d150 d200 d240
# unconv). Each step appends its command and exit status to exits.txt.
PY=/Users/nathan/venv-314/bin/python3
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i636
F=$RAW/I636-mac
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a85c4feb2fd2f0829/hp
cd $HP || exit 9
mkdir -p $F/planted $F/chain $F/controls
run() {
  local log=$1; shift
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') start: chain_dM.py $*" >> $F/exits.txt
  nice -n 10 $PY -u chain_dM.py "$@" > $log 2>&1
  local rc=$?
  echo "$(date -u '+%Y-%m-%d %H:%M:%S') exit $rc: chain_dM.py $*" >> $F/exits.txt
  return $rc
}
for step in "$@"; do
  case $step in
    planted80) run $F/planted/planted_chain80.log planted $RAW $F/planted --threads=5 --only=chain80 ;;
    planted80_held) run $F/controls/planted_chain80_held.log planted $RAW $F/controls --threads=5 --only=chain80 --mutate=held --m32=0 ;;
    d100) run $F/chain/d100.log run $RAW $F/chain T138-win2/chain/anm_pin3_D100.0000.npz --threads=5 ;;
    d150) run $F/chain/d150.log run $RAW $F/chain T138-win2/chain/anm_pin3_D150.0000.npz --threads=5 ;;
    # from D 200 the quad-double Newton sits at its floor and each step costs about 3 min under the Mac's load: 6 steps
    d200) run $F/chain/d200.log run $RAW $F/chain T138-win2/chain_o/anm_pin3_D200.0000.npz --threads=5 --it=6 ;;
    d240) run $F/chain/d240.log run $RAW $F/chain I603-win2/chain/anm_pin3_D240.1244.npz --threads=5 --it=6 ;;
    unconv) run $F/controls/unconverged_d100.log run $RAW $F/controls T138-win2/chain/anm_pin3_D100.0000.npz --threads=5 --m32=0 --save=0 --mutate=unconverged ;;
    *) echo "unknown step $step" >&2; exit 9 ;;
  esac
done

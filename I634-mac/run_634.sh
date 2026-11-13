#!/usr/bin/env bash
# #634 runs on the Mac, one heavy run at a time, 2 threads at nice 10 (the coordinator's cap from 07:39 UTC; the first
# reproduction at D 236.63 ran with 4 threads). Usage: run_634.sh STAGE D... with STAGE variants:<list> | n24 | polish
# Code: choptuik-large-d branch wip/i634-subagent (hp/anm_run.py --save_jet, hp/jet_singularity.py); hpkernel of main 3c35f0c.
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a114b904fe4457623/hp
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i634
R=$RAW/I634-mac
PY=/Users/nathan/venv-314/bin/python3
T=2
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
cd $HP || exit 9
CH="--kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 --h_max 1.0 --steps 1 --D_max 400 --threads $T --corrector od --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3"
log() { echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') $*" >> $R/exits_634.txt; }
stage=$1; shift
for D in "$@"; do
  case $D in 225.1312) S=I603-win2/base/base_pin3_D225.1312.npz ;; *) S=I603-win2/chain/anm_pin3_D$D.npz ;; esac
  case $stage in
    variants:*)
      V=${stage#variants:}
      mkdir -p $R/jets
      t=$(date +%s)
      nice -n 10 $PY -u jet_singularity.py jet $RAW $S $R/jets/D$D --N 8 --threads $T --variants $V > $R/jets/D$D.$(echo $V | tr ":," "_-").log 2>&1
      log "variants $V D $D threads $T exit $? wall $(( $(date +%s) - t ))s" ;;
    n24)
      t=$(date +%s)
      nice -n 10 $PY -u anm_run.py $RAW $R/repro --state $S --N 24 --tol_od 1e-60 $CH --save_jet 2 > $R/repro_D$D.log 2>&1
      log "repro N 24 D $D threads $T exit $? wall $(( $(date +%s) - t ))s" ;;
    polish)
      t=$(date +%s)
      nice -n 10 $PY -u anm_run.py $RAW $R/polish --state $S --N 8 --tol_od 1e-80 $CH --save_base 1 --save_jet 2 > $R/polish_D$D.log 2>&1
      log "polish N 8 D $D threads $T exit $? wall $(( $(date +%s) - t ))s" ;;
  esac
done

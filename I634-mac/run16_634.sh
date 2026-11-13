#!/usr/bin/env bash
# #634: the 16-order octo-double series at one base by anm_run.py --save_jet 2 with #603's flags, 2 threads at nice 10
# (16 orders cost about half of 24 here, and Delta's series to order 16 is enough to locate a singularity at |s| ~ 8)
HP=/Users/nathan/Source/choptuik-large-d/.claude/worktrees/agent-a114b904fe4457623/hp
RAW=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/raw-i634
R=$RAW/I634-mac
PY=/Users/nathan/venv-314/bin/python3
export PYTHONPATH=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/11bcbd25-9376-453b-88d5-a7c6ad0172dd/scratchpad/i599/site2
cd $HP || exit 9
D=$1
S=I603-win2/chain/anm_pin3_D$D.npz
mkdir -p $R/repro16
t=$(date +%s)
nice -n 10 $PY -u anm_run.py $RAW $R/repro16 --state $S --N 16 --tol_od 1e-60 --kfreeze 3 --held_fit data/held_fit.json --eps 1e-14 \
  --h_max 1.0 --steps 1 --D_max 400 --threads 2 --corrector od --qd_it 12 --a_grow 1.25 --a_hold 1 --lam_stall 0.04 --od_junk 0 \
  --jet_o 1 --reseed 2 --reseed_q 1 --held_o 1 --reseed_o 3 --save_jet 2 > $R/repro16_D$D.log 2>&1
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') repro N 16 D $D threads 2 exit $? wall $(( $(date +%s) - t ))s" >> $R/exits_634.txt

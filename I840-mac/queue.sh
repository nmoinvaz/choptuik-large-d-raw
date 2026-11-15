#!/bin/bash
# #840: the four D in order, then the repeat check's control; each with step_spread.py's defaults (rel 1e-65, seeds 1-4,
# controls 1) and --repeat 1, --ref where #837 recorded the step exactly
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
cd $R/I840-mac || exit 9
./run.sh ss_D240 step_spread.py $R I603-win2/chain/anm_pin3_D240.1244.npz --threads 3 --repeat 1 --ref -4.3765436014297066e-58 --json $R/I840-mac/ss_D240.json
./run.sh ss_D245 step_spread.py $R I603-win2/chain/anm_pin3_D245.6366.npz --threads 3 --repeat 1 --json $R/I840-mac/ss_D245.json
./run.sh ss_D250 step_spread.py $R I603-win2/chain/anm_pin3_D250.1676.npz --threads 3 --repeat 1 --json $R/I840-mac/ss_D250.json
./run.sh ss_D252 step_spread.py $R I603-win2/chain/anm_pin3_D252.6135.npz --threads 3 --repeat 1 --ref 5.2645963792835124e-82 --json $R/I840-mac/ss_D252.json
./run.sh ss_D240_repeatctl step_spread.py $R I603-win2/chain/anm_pin3_D240.1244.npz --threads 3 --repeat 1 --seeds 1 --controls 0 --mutate repeat --json $R/I840-mac/ss_D240_repeatctl.json
./run.sh selftest step_spread.py --selftest
./run.sh selftest_bar step_spread.py --selftest --mutate=bar
./run.sh selftest_band step_spread.py --selftest --mutate=band
echo "queue done $(date -u '+%H:%M:%S')" > queue.done

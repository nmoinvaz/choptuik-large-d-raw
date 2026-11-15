#!/bin/bash
# #850: the --blocks option's controls first, then the Delta block at rel 1e-65, 1e-66, 1e-67 at D 240.1244 and
# 252.6135 (seed 1, the same signs as #840's Delta control), then the power reading and the selftests. One process.
R=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/ececf14c-b4b6-41d2-ad20-2caade87ad18/scratchpad/raw781push
O=$R/I850-mac
S240=I603-win2/chain/anm_pin3_D240.1244.npz
S252=I603-win2/chain/anm_pin3_D252.6135.npz
REF240=-4.3765436014297066e-58
REF252=5.2645963792835124e-82
cd "$(dirname "$0")" || exit 9
C="--threads 3 --seeds 1 --controls 0 --repeat 0"
./run.sh selftest step_spread.py --selftest
./run.sh selftest_nosub step_spread.py --selftest --mutate=nosub
./run.sh ctl_centre_D240 step_spread.py $R $S240 $C --blocks centre --ref $REF240 --match $R/I840-mac/ss_D240.json --json $O/ctl_centre_D240.json
./run.sh ctl_noop_D240 step_spread.py $R $S240 $C --blocks centre --ref $REF240 --match $R/I840-mac/ss_D240.json --mutate noop --json $O/ctl_noop_D240.json
for k in 65 66 67; do
  m=""; [ $k = 65 ] && m="--match $R/I840-mac/ss_D240.json"
  ./run.sh dl_D240_r$k step_spread.py $R $S240 $C --blocks Delta --rel 1e-$k --ref $REF240 $m --json $O/dl_D240_r$k.json
done
for k in 65 66 67; do
  m=""; [ $k = 65 ] && m="--match $R/I840-mac/ss_D252.json"
  ./run.sh dl_D252_r$k step_spread.py $R $S252 $C --blocks Delta --rel 1e-$k --ref $REF252 $m --json $O/dl_D252_r$k.json
done
./run.sh power step_spread.py power $O/dl_D240_r65.json $O/dl_D240_r66.json $O/dl_D240_r67.json $O/dl_D252_r65.json $O/dl_D252_r66.json $O/dl_D252_r67.json --json $O/power.json
./run.sh power_start step_spread.py power $O/dl_D240_r65.json $O/dl_D240_r66.json $O/dl_D240_r67.json --mutate start
echo "queue done $(date -u '+%Y-%m-%d %H:%M:%S') UTC" > queue.done

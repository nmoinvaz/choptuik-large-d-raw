#!/bin/bash
# I178-macm3: locating the zero at kf 21. Round N takes the circles as arguments (RE,IM,R ...), kf 21, fresh evaluation cache per round.
# Round 1 starts without a saved state in hp/data (setup re-converges), later rounds find the state it saved.
# After the round the cache and log move into locate_<round>/; the state moves out only after the last round (second argument "last").
cd ~/Source/choptuik-large-d
export PATH=/Users/nathan/Source/venv-macm3/bin:$PATH
R=../choptuik-large-d-raw/I178-macm3
ROUND=$1
LAST=$2
shift 2
mkdir -p $R/locate_$ROUND
date -u '+round '$ROUND' start %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up7_D45.0507.npz "$@" --M=48 --kf=21 --fmax=1e-15 --tag=D45.0507_M48_kf21_loc$ROUND --res=$R/circles_locate.jsonl > $R/locate_$ROUND.log 2>&1
echo "locate $ROUND exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
for F in hp/data/modecount_D45.0507_M48_kf21_loc${ROUND}_evals.jsonl hp/data/modecount_D45.0507_M48_kf21_loc${ROUND}.log
do
  if [ -e "$F" ]
  then
    mv "$F" $R/locate_$ROUND/
  fi
done
if [ "$LAST" = "last" ]
then
  mv hp/data/modecount_state_D45.0507_M48_kf21.npz $R/locate_$ROUND/
fi
date -u '+round '$ROUND' end %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt

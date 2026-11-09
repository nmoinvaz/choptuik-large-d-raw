#!/bin/bash
# I249-macm3: one D: gamma_dd (unless LAM is given), then the fixed-column count. Usage: run_count.sh T S [LAM]
T=$1
S=$2
LAM=$3
cd ~/Source/choptuik-large-d
R=../choptuik-large-d-raw/I249-macm3
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
date -u '+start %Y-%m-%d %H:%M:%S UTC' >> $R/$T/driver.txt
if [ -z "$LAM" ]
then
  caffeinate -is nice -n 10 python3 hp/gamma_dd.py $R/$T/gamma.jsonl hp/data/states/$S.npz > $R/$T/gamma.log 2>&1
  echo "$T gamma_dd exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
  LAM=$(jq -r '.lam' $R/$T/gamma.jsonl | head -1)
fi
echo "$T lam $LAM" >> $R/$T/driver.txt
caffeinate -is nice -n 10 python3 hp/modecount_wind.py hp/data/states/$S.npz --M=48 --kf=23 --h0=0.6 --lam=$LAM --aLL=-0.096 --aL=0.124 --fmax=1e-15 --resolve=last --tag=${T}_M48_kf23 --data=$R/$T/data > $R/$T/count.log 2>&1
echo "$T count exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
date -u '+end %Y-%m-%d %H:%M:%S UTC' >> $R/$T/driver.txt

#!/bin/bash
# I178-macm3: the two small circles at D 45.05, M 48 for each kf given as an argument (the issue's command, one K after another).
# After each K the evaluation cache, log and any re-converged state move from hp/data into data_kf<K>/ of this folder.
cd ~/Source/choptuik-large-d
export PATH=/Users/nathan/Source/venv-macm3/bin:$PATH
R=../choptuik-large-d-raw/I178-macm3
for K in "$@"
do
  mkdir -p $R/data_kf$K
  date -u '+K '$K' start %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
  caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up7_D45.0507.npz 1.11,0,0.12 2.057,0,0.1 --M=48 --kf=$K --fmax=1e-15 --tag=D45.0507_M48_kf${K}_circ --res=$R/circles.jsonl > $R/circ_kf$K.log 2>&1
  echo "kf $K exit $? at $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> $R/exits.txt
  for F in hp/data/modecount_D45.0507_M48_kf${K}_circ_evals.jsonl hp/data/modecount_D45.0507_M48_kf${K}_circ.log hp/data/modecount_state_D45.0507_M48_kf${K}.npz
  do
    if [ -e "$F" ]
    then
      mv "$F" $R/data_kf$K/
    fi
  done
  date -u '+K '$K' end %Y-%m-%d %H:%M:%S UTC' >> $R/driver.txt
done

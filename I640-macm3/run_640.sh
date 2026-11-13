#!/bin/bash
# #640: release the chain's held harmonics (hp/release_held.py, main 9839474, worktree ~/Source/choptuik-large-d-b640), quad double, nice 10, caffeinate.
# Inputs are read from the raw-repo clone ~/Source/choptuik-large-d-raw-push (up to date); outputs go to I640-macm3 of the live clone.
# Step 1: the planted control on T81's D 73.0 full-system state: unperturbed, --perturb=1e-10, --perturb=1e-10 --it_max=0, three at once, 2 threads each.
# Step 2 (only if the control passes): the 12 releases at D 80, 100, 150, 200 with --kfreeze 13, 9, 7, three at once (2 threads each).
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
RAWIN=/Users/nathan/Source/choptuik-large-d-raw-push
OUT=/Users/nathan/Source/choptuik-large-d-raw/I640-macm3
while ! grep -q '^axis_D5 exit' /Users/nathan/Source/choptuik-large-d-raw/I632-macm3/exits.txt 2>/dev/null || ! grep -q '^axis_D6 exit' /Users/nathan/Source/choptuik-large-d-raw/I632-macm3/exits.txt 2>/dev/null; do sleep 20; done
cd /Users/nathan/Source/choptuik-large-d-b640/hp
rel() {  # tag state extra-args...
  tag=$1; state=$2; shift 2
  mkdir -p $OUT/$tag
  caffeinate -is nice -n 10 python3 -u release_held.py $OUT/$tag/release.jsonl $state "$@" --threads=2 > $OUT/$tag/release.log 2>&1
  echo "$tag exit $? at $(date -u +%FT%TZ)" >> $OUT/exits.txt
}
S73=$RAWIN/T81/conv_pin5_D73.0000_D73.000000.npz
rel control_unperturbed $S73 --kfreeze=13 &
rel control_perturbed $S73 --kfreeze=13 --perturb=1e-10 &
rel control_noreleas $S73 --kfreeze=13 --perturb=1e-10 --it_max=0 &
wait
if python3 $OUT/compare640.py > $OUT/control_result.txt 2>&1; then echo "control passes at $(date -u +%FT%TZ)" >> $OUT/exits.txt
else echo "CONTROL FAILED at $(date -u +%FT%TZ)" >> $OUT/exits.txt; exit 1; fi
state() { case $1 in 80|100|150) echo $RAWIN/T138-win2/chain/anm_pin3_D$1.0000.npz ;; 200) echo $RAWIN/T138-win2/chain_o/anm_pin3_D200.0000.npz ;; esac; }
for D in 80 100 150 200; do
  for K in 13 9 7; do
    mkdir -p $OUT/releases
    ( caffeinate -is nice -n 10 python3 -u release_held.py $OUT/releases/release_D${D}_kf${K}.jsonl $(state $D) --kfreeze=$K --threads=2 > $OUT/releases/release_D${D}_kf${K}.log 2>&1
      echo "release D$D kf$K exit $? at $(date -u +%FT%TZ)" >> $OUT/exits.txt ) &
  done
  wait
done

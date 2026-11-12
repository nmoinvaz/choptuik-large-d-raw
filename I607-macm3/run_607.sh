#!/bin/bash
# #607: #518's command at kf 55 and kf 51 (the coordinator: begin with kf 55, then bisect; two cuts at a time on the freed threads beside #605).
# Each cut in two processes with their own data dirs and caches: A = the lambda_phys control and the first four R 0.3 circles (it makes the state),
# B = the last four circles (it starts once the state file exists and #605's runs are done). Main checkout at de63a118 (the build of #518's runs).
# A starts when M 80 (#517) has ended.
raw=/Users/nathan/Source/choptuik-large-d-raw
ST=/Users/nathan/Source/choptuik-large-d/hp/data
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
C1="0.055758,1.411769,0.3 3.871717,0.105316,0.3 4.285793,0.551490,0.3 4.656327,1.390362,0.3"
C2="0.847147,4.333559,0.3 1.057045,2.913917,0.3 1.978326,3.721021,0.3 4.070967,2.532063,0.3"
while ! grep -q '^stage1 M80 exit 0' $raw/I517-macm3/exits.txt 2>/dev/null; do sleep 20; done
start() { # part kf circles
    d=$raw/I607-macm3/kf$2/$1; mkdir -p $d/data
    date -u +%FT%TZ > $d/started.txt
    (cd ~/Source/choptuik-large-d && caffeinate -is nice -n 10 python3 hp/modecount_circle.py hp/data/states/up6_D30.0688.npz $3 --M=64 --kf=$2 --fmax=1e-15 --n0=20 --tag=D30.0688_M64_kf$2 --data=$d/data > $d/stage1.log 2>&1
     echo "kf$2 $1 exit $? at $(date -u +%FT%TZ)" >> $raw/I607-macm3/exits.txt) &
}
start A 55 "2.079747703853262,0,0.2 $C1"
start A 51 "2.079747703853262,0,0.2 $C1"
while [ ! -f $ST/modecount_state_D30.0688_M64_kf55.npz ] || [ ! -f $ST/modecount_state_D30.0688_M64_kf51.npz ] || ! grep -q '^s3_extra exit' $raw/I605-macm3/exits.txt 2>/dev/null; do sleep 30; done
start B 55 "$C2"
start B 51 "$C2"
wait

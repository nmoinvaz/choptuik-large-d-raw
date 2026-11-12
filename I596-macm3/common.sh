# #596: #590's run() with --ball=320 added (issue #596, the coordinator's message of 2026-11-12 12:44 UTC), from the root of the worktree ~/Source/choptuik-large-d-b596 at main 742bb879.
cd ~/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=../choptuik-large-d-raw/I596-macm3
run() { caffeinate -is nice -n 10 python3 -u hp/gamma_dd.py $R/gamma_D55_$1.jsonl hp/data/states/up10_D55.0351.npz --threads=1 --polish=4 --Mhi=64 --kf48=33 --bracket=$2 --xtol=1e-16 --ball=320 > $R/gamma_D55_$1.log 2>&1; echo "$1 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt; }

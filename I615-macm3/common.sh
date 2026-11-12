# #615: #458's run() (I458-macm3/common.sh) with --ball=320 added, from the root of the worktree ~/Source/choptuik-large-d-b596 at main ef466c7
# (modecount_cx built from 742bb879's source). One thread per run, four at a time, nice 10, caffeinate -is.
cd /Users/nathan/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I615-macm3
run() { caffeinate -is nice -n 10 python3 -u hp/gamma_dd.py $R/gamma_$1_$2.jsonl hp/data/states/$1.npz --threads=1 --polish=4 --M48 --kf48=13 --bracket=$3 --xtol=1e-16 --ball=320 > $R/gamma_$1_$2.log 2>&1; echo "$1 $2 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt; }
D58=up12_D58.0060

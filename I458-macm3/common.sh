# #458: the coordinator's run() (issue comment 6821242579), from the root of the worktree ~/Source/choptuik-large-d-b458 at main c845cc99.
cd ~/Source/choptuik-large-d-b458
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=../choptuik-large-d-raw/I458-macm3
run() { caffeinate -is nice -n 10 python3 -u hp/gamma_dd.py $R/gamma_$1_$2.jsonl hp/data/states/$1.npz --threads=1 --polish=4 --M48 --kf48=13 --bracket=$3 --xtol=1e-16 > $R/gamma_$1_$2.log 2>&1; echo "$1 $2 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt; }
# D 40 (root 2.0627796726) and D 58 (root 2.0455297615): the brackets of the issue
D40=up7_D40.0201
D58=up12_D58.0060

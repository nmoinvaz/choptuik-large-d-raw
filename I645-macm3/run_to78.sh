#!/bin/bash
. /Users/nathan/Source/choptuik-large-d-raw-641/I645-macm3/common.sh
cd /Users/nathan/Source/choptuik-large-d-b640/hp
mkdir -p $R/I645-macm3/to78
caffeinate -is nice -n 10 python3 -u scan_qd.py $R/I645-macm3/to78/scan.jsonl $R/I642-win/released_kf13_D77.0000.npz 78 --history $R/I642-win/released_kf13_D74.0000.npz,$R/I642-win/released_kf13_D75.0000.npz,$R/I642-win/released_kf13_D76.0000.npz --kfreeze 13 --dD 0.05 --threads 4 --tag full > $R/I645-macm3/to78/scan.log 2>&1
echo "to78 exit $? at $(date -u +%FT%TZ)" >> $R/I645-macm3/exits.txt

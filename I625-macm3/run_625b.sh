#!/bin/bash
# I625, the coordinator's option (b) (message of 2026-11-13 00:18 UTC, comment on #625): gamma_dd.py --scan --scan_only on its own M 48
# background, from the root of the worktree ~/Source/choptuik-large-d-b596 at main be8bfb1 (modecount_cx built from 742bb879's source).
# Five processes, one thread each, nice 10, caffeinate: four M 48 ranges (p0 -32..-16, p1 -16..0, p2 0..16, p3 16..32; the overlaps at -16, 0, 16
# are cross-process repeats) and the same-path control at M 32 (--scan_at=base, no --M48 --kf48=13).
cd /Users/nathan/Source/choptuik-large-d-b596
export PATH=/Users/nathan/Source/venv-macm3-314/bin:$PATH
R=/Users/nathan/Source/choptuik-large-d-raw/I625-macm3
C48=2.0455297614777672
scan() { # name K0 K1
  (caffeinate -is nice -n 10 python3 -u hp/gamma_dd.py $R/scan48_$1.jsonl hp/data/states/up12_D58.0060.npz --threads=1 --polish=4 --M48 --kf48=13 --ball=320 --scan=$C48,1e-14,$2,$3 --scan_only > $R/scan48_$1.log 2>&1
   echo "scan48_$1 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt) &
}
scan p0 -32 -16
scan p1 -16 0
scan p2 0 16
scan p3 16 32
(caffeinate -is nice -n 10 python3 -u hp/gamma_dd.py $R/scan32.jsonl hp/data/states/up12_D58.0060.npz --threads=1 --polish=4 --ball=320 --scan_at=base --scan=2.045529761477775,1e-14,-4,4 --scan_only > $R/scan32.log 2>&1
 echo "scan32 exit $? at $(date -u +%FT%TZ)" >> $R/exits.txt) &
wait

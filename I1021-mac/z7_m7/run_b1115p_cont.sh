#!/bin/bash
# #1021 slot 2, continued: b11-15's xi1 0.2 repeats after m5_repeat.py v1 stopped on repeat 2's 3600 s timeout
# (m5/b1115p_repeat_xi0.2_crash.log), by m5_repeat.py --resume (v2: a timed-out attempt counts as failed, the attempts
# already run are reused when their command matches), then run_m7d.sh b1115p from the counted attempt.
set -u
{ # read whole before it runs
. "$(dirname "$0")/common_z7.sh"
M5=$(cd $D/../m5 && pwd); CODE=/Users/nathan/Source/choptuik-large-d-1021c; P3=/Users/nathan/venv-314/bin/python
EX=$D/xi015d/b1115p_m5_exits.txt
log() { echo "b1115p $* $(stamp) UTC" >> $EX; }
[ "$(git -C $CODE rev-parse HEAD | cut -c1-8)" = 6da7da7b ] || { echo "$CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git -C $CODE status --short)" ] || { echo "$CODE not clean"; exit 1; }
[ -e $D/xi015d/README.md ] || { echo "$D/xi015d/README.md missing"; exit 1; }
[ -e $M5/b1115p_repeat_xi0.2.log ] && { echo "$M5/b1115p_repeat_xi0.2.log exists"; exit 1; }
log "continued: m5_repeat.py --resume"
s=$(date +%s); $P3 $M5/m5_repeat.py $CODE $P3 $M5/b1115p_6da7da7b_xi0.2.log --resume > $M5/b1115p_repeat_xi0.2.log 2>&1; rc=$?
echo "repeat exit $rc $(stamp)" >> $M5/b1115p_repeat_xi0.2.log
log "m5_repeat.py --resume exit $rc (0 when an attempt is under the bar) wall $(( $(date +%s) - s )) s"
grep -q "^counted: " $M5/b1115p_repeat_xi0.2.log || { log "no counted attempt; stop"; exit 1; }
bash $D/run_m7d.sh b1115p
log "run_m7d.sh b1115p exit $?"
exit
}

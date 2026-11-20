#!/bin/bash
# #1021 slot 2 of the xi015d runs: b11-15's +1 zero (located at xi1 0.18, loc/b1115p_r0.18_6da7da7b). Its fixed-(A, w) M = 5
# solve at xi1 0.2 first, as boxes 7 and 16 had it (hier.py at 6da7da7b, numpy backend, venv-314, from the M = 3 harmonics
# m5/b1115p_start.txt, then #1027's three repeats by m5/m5_repeat.py), then run_m7d.sh b1115p from the counted attempt.
set -u
{ # read whole before it runs
. "$(dirname "$0")/common_z7.sh"
M5=$(cd $D/../m5 && pwd); CODE=/Users/nathan/Source/choptuik-large-d-1021c; P3=/Users/nathan/venv-314/bin/python
EX=$D/xi015d/b1115p_m5_exits.txt
log() { echo "b1115p $* $(stamp) UTC" >> $EX; }
[ "$(git -C $CODE rev-parse HEAD | cut -c1-8)" = 6da7da7b ] || { echo "$CODE is not at 6da7da7b"; exit 1; }
[ -z "$(git -C $CODE status --short)" ] || { echo "$CODE not clean"; exit 1; }
[ -e $D/xi015d/README.md ] || { echo "$D/xi015d/README.md missing"; exit 1; }
LOG=$M5/b1115p_6da7da7b_xi0.2.log
[ -e $LOG ] && { echo "$LOG exists"; exit 1; }
read -r A W B3 C3 < $M5/b1115p_start.txt
log "start, code $(git -C $CODE rev-parse --short=8 HEAD), $($P3 -c 'import sys,numpy,scipy;print("python",sys.version.split()[0],"numpy",numpy.__version__,"scipy",scipy.__version__)')"
ARG="-u hier.py 5 $A $W --x=$B3,$C3 --fixA --schur --procs 1 --verbose=1 --xi1=0.2"
echo "# $P3 $ARG (6da7da7b, numpy backend; b11-15's +1 zero located at xi1 0.18, loc/b1115p_r0.18_6da7da7b; start $(stamp))" > $LOG
s=$(date +%s); (cd $CODE/solver/inner_stokes && exec nice -n 10 timeout -s TERM 3600 $P3 $ARG >> $LOG 2>&1); log "first attempt exit $? wall $(( $(date +%s) - s )) s, cap 3600 s"
s=$(date +%s); $P3 $M5/m5_repeat.py $CODE $P3 $LOG > $M5/b1115p_repeat_xi0.2.log 2>&1; rc=$?; echo "repeat exit $rc $(stamp)" >> $M5/b1115p_repeat_xi0.2.log
log "m5_repeat.py exit $rc (0 when an attempt is under the bar) wall $(( $(date +%s) - s )) s"
grep -q "^counted: " $M5/b1115p_repeat_xi0.2.log || { log "no counted attempt; stop"; exit 1; }
bash $D/run_m7d.sh b1115p
log "run_m7d.sh b1115p exit $?"
exit
}

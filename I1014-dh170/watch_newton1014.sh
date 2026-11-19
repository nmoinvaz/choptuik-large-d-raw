#!/bin/bash
# #1014: notify (the task's completion) when stage1.log gets a new Newton line (the log labels every call "newton 0", so count the lines, do not match a number), or a Traceback/Error,
# or the lift exits. usage: bash watch_newton1014.sh N   (N = the number of newton lines already seen)
N=${1:?lines seen}
LOG=/home/nathan/Source/choptuik-large-d-raw/I1014-dh170/stage1.log
until [ "$(grep -c '^  newton' $LOG)" -gt "$N" ] || grep -qE 'Traceback|Error' $LOG || ! pgrep -f '^/home/nathan/Source/choptuik-large-d-935/.venv/bin/python -u lowD_dd.py' >/dev/null; do sleep 20; done
date -u '+%F %T'; tail -n 3 $LOG | cut -c1-230

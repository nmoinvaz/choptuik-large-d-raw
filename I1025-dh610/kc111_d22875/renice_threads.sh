#!/bin/bash
# renice_threads.sh [--mutate] PID: sets nice 19 on every thread of PID (on Linux nice is per thread; 'renice -p PID' moves only the main thread), by exact tid.
# Prints one line: the threads' nice values before and after; exits 1 if a thread is not at 19 afterwards. --mutate renices the main thread only (the control: must exit 1 for a multi-threaded PID).
M=0; [ "$1" = "--mutate" ] && { M=1; shift; }
P=$1; [ -d /proc/$P/task ] || { echo "renice_threads: no process $P"; exit 2; }
snap() { ps -L -o ni= -p $P | tr -s ' \n' ' ' | sed 's/^ //; s/ $//'; }
before=$(snap)
if [ $M = 1 ]; then renice -n 19 -p $P > /dev/null 2>&1
else for t in $(ps -L -o tid=,ni= -p $P | awk '$2 < 19 {print $1}'); do renice -n 19 -p $t > /dev/null 2>&1; done; fi
after=$(snap)
echo "pid $P threads $(ps -L -o tid= -p $P | wc -l): nice before [$before] after [$after]"
[ -z "$(ps -L -o ni= -p $P | awk '$1 != 19')" ]

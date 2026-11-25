#!/bin/bash
# renice_threads.sh PID [NICE]: raise the nice value of every thread (TID listed by ps -L) of the exact process PID to NICE (default 19). On Linux a nice value is per thread, so
# renicing the PID alone leaves the other threads of a multithreaded process (the 6 BLAS threads of the regrid) where they were. Prints "changed/total threads". Only raises.
p=$1; n=${2:-19}; ch=0; tot=0
while read -r t cur; do
  [ -n "$t" ] || continue
  tot=$((tot + 1))
  [ "$cur" -lt "$n" ] && renice -n $n -p $t > /dev/null 2>&1 && ch=$((ch + 1))
done < <(ps -L -o tid=,ni= -p $p 2>/dev/null)
echo "$ch/$tot"

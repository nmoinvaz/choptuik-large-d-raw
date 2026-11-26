#!/bin/bash
# The chord switch (#1088, ab2446b8): when the running ladder solve (unit $1, folder out/$2) has saved its state after
# its first dd step, stop it and start $3 (run script) from that state, whose ladder takes one more dd step and then
# chord steps with that step's Jacobian; usage chord_switch.sh UNIT FOLDER RUNSCRIPT STEPFILE
{
W=/home/nathan/Source/choptuik-large-d-1088a
U=$1
O=$W/out/$2
R=$W/$3
S=$O/$4
n=0
while [ $n -lt 720 ]; do
  if [ -s $S ]; then
    a=$(stat -c %s $S); sleep 15; b=$(stat -c %s $S)
    [ "$a" = "$b" ] && break
  fi
  systemctl --user is-active --quiet $U || exit 2
  sleep 20; n=$((n + 1))
done
[ -s $S ] || exit 1
systemctl --user stop $U
echo "stopped at $(date -u '+%Y-%m-%d %H:%M:%S') UTC by chord_switch.sh after its first dd step (state saved); continued by $3" >> $O/run.log
cp $S $W/out/$2_step0.npz
systemd-run --user --unit=$U-c --working-directory=$W nice -n 10 timeout 20h $R
exit
}

#!/bin/bash
# Move the D 2000 release (#1088) from 4 to 10 threads at its next saved step: when release_ls_h7's step state is
# saved again (h7 outer 1), stop i1088a-rls2000 and start run_rls2000b.sh from that state (1ccd32ab: h13 with the
# quad-double Jacobian, the held Delta given)
{
W=/home/nathan/Source/choptuik-large-d-1088a
O=$W/out/rls2000
S=$O/release_ls_h7_D2000.0000_step.npz
t0=$(stat -c %Y $S)
n=0
while [ $n -lt 360 ]; do
  t=$(stat -c %Y $S)
  if [ "$t" != "$t0" ]; then
    sleep 15
    break
  fi
  systemctl --user is-active --quiet i1088a-rls2000 || exit 2
  sleep 20; n=$((n + 1))
done
[ "$(stat -c %Y $S)" != "$t0" ] || exit 1
systemctl --user stop i1088a-rls2000
echo "stopped at $(date -u '+%Y-%m-%d %H:%M:%S') UTC after h7 outer 1's saved state; continued on 10 threads by run_rls2000b.sh (out/rls2000b)" >> $O/run.log
cp $S $W/out/rls2000_h7_step1.npz
systemd-run --user --unit=i1088a-rls2000b --working-directory=$W nice -n 10 timeout 30h $W/run_rls2000b.sh
exit
}

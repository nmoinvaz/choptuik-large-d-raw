#!/bin/bash
# #966 second request: locate on leg 14's five jets and leg 13's four, rows --delta on leg 13's four, and the sign
# diagnostic on leg 13; one process at nice 19, sequential.
set -u
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i966sing
P=/Users/nathan/venv-314/bin/python; C=$W/code
J14="$W/jets/jet_pin3_D261.1415.npz $W/jets/jet_pin3_D261.2061.npz $W/jets/jet_pin3_D261.2697.npz $W/jets/jet_pin3_D261.3914.npz $W/jets/jet_pin3_D261.5124.npz"
J13="$W/jets13/jet_pin3_D260.8483.npz $W/jets13/jet_pin3_D260.9271.npz $W/jets13/jet_pin3_D261.0721.npz $W/jets13/jet_pin3_D261.1415.npz"
cd $W/out
X=$W/out/exits2.txt; echo "start $(date -u '+%F %T')" > $X
for L in 14 13; do J=J$L
  /usr/bin/time -l nice -n 19 $P -I $C/jet_singularity.py locate ${!J} --json $W/out/locate966_leg$L.json > locate966_leg$L.txt 2> locate966_leg$L.time
  echo "locate leg $L exit $? $(date -u '+%F %T')" >> $X
done
/usr/bin/time -l nice -n 19 $P -I $C/singularity_type.py rows $J13 --delta > type966_leg13.txt 2> type966_leg13.time
echo "rows leg 13 exit $? $(date -u '+%F %T')" >> $X
nice -n 19 $P -I $W/signs.py $C $J13 > signs966_leg13.txt; echo "signs leg 13 exit $?" >> $X
$P -I $W/runs.py signs966_leg13.txt > runs966_leg13.txt; echo "runs leg 13 exit $?" >> $X
echo "end $(date -u '+%F %T')" >> $X
exit
}

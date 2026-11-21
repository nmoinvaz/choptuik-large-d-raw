#!/bin/bash
# #966 third request: locate and rows --delta on leg 10's 18 jets, then pairs10.py and its controls; nice 19, one process.
set -u
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i966sing
P=/Users/nathan/venv-314/bin/python; C=$W/code; O=$W/out
J=$(ls $W/jets10/jet_pin3_D*.npz | sort)
cd $O; X=$O/exits3.txt; echo "start $(date -u '+%F %T')" > $X
/usr/bin/time -l nice -n 19 $P -I $C/jet_singularity.py locate $J --json $O/locate966_leg10.json > locate966_leg10.txt 2> locate966_leg10.time
echo "locate leg 10 exit $? $(date -u '+%F %T')" >> $X
$P -I $W/pairs10.py $O/locate966_leg10.json > pairs10_966.txt; echo "pairs10 exit $?" >> $X
for m in plant move; do $P -I $W/pairs10.py $O/locate966_leg10.json --mutate=$m > pairs10_966_$m.txt; echo "pairs10 --mutate=$m exit $?" >> $X; done
/usr/bin/time -l nice -n 19 $P -I $C/singularity_type.py rows $J --delta > type966_leg10.txt 2> type966_leg10.time
echo "rows leg 10 exit $? $(date -u '+%F %T')" >> $X
echo "end $(date -u '+%F %T')" >> $X
exit
}

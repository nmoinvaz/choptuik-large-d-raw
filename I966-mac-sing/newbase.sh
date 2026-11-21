#!/bin/bash
# #966: a new ks_chain3b jet: fetch it from raw origin/main, then locate, rows --delta, nextcheck.py and its control,
# one process at nice 19. Usage: newbase.sh RAWPATH (the jet's path in the raw repository)
set -u
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad
W=$S/i966sing; P=/Users/nathan/venv-314/bin/python; C=$W/code; O=$W/out
F=$1; B=$(basename "$F" .npz); D=${B#jet_pin3_D}; mkdir -p $W/jetsnew
git -C $S/raw1021push show origin/main:"$F" > $W/jetsnew/$B.npz || { echo "fetch of $F failed"; exit 1; }
cd $O; X=$O/exits_new.txt; echo "D $D from $F at raw $(git -C $S/raw1021push rev-parse --short origin/main), start $(date -u '+%F %T')" >> $X
/usr/bin/time -l nice -n 19 $P -I $C/jet_singularity.py locate $W/jetsnew/$B.npz --json $O/locate966_D$D.json > locate966_D$D.txt 2> locate966_D$D.time
echo "  locate exit $?" >> $X
/usr/bin/time -l nice -n 19 $P -I $C/singularity_type.py rows $W/jetsnew/$B.npz --delta > type966_D$D.txt 2> type966_D$D.time
echo "  rows exit $?" >> $X
$P -I $W/nextcheck.py $O/locate966_D$D.json > nextcheck966_D$D.txt; echo "  nextcheck exit $?" >> $X
$P -I $W/nextcheck.py $O/locate966_D$D.json --mutate=move > nextcheck966_D${D}_move.txt; echo "  nextcheck --mutate=move exit $? (1)" >> $X
echo "  end $(date -u '+%F %T')" >> $X
exit
}

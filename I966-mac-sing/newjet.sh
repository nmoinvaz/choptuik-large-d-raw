#!/bin/bash
# #966/#1064: one jet from raw origin/main read as newbase.sh does, with outputs named by TAG (locate, rows --delta),
# one process at nice 19. Usage: newjet.sh TAG RAWPATH
set -u
{
S=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad
W=$S/i966sing; P=/Users/nathan/venv-314/bin/python; C=$W/code; O=$W/out; T=$1; F=$2; mkdir -p $W/jetsfront
git -C $S/raw1021push show origin/main:"$F" > $W/jetsfront/$T.npz || { echo "fetch of $F failed"; exit 1; }
cd $O; X=$O/exits_front.txt; echo "$T from $F at raw $(git -C $S/raw1021push log -1 --format=%h origin/main -- "$F"), start $(date -u '+%F %T')" >> $X
/usr/bin/time -l nice -n 19 $P -I $C/jet_singularity.py locate $W/jetsfront/$T.npz --json $O/locate966_front_$T.json > locate966_front_$T.txt 2> locate966_front_$T.time
echo "  locate exit $?" >> $X
/usr/bin/time -l nice -n 19 $P -I $C/singularity_type.py rows $W/jetsfront/$T.npz --delta > type966_front_$T.txt 2> type966_front_$T.time
echo "  rows exit $?" >> $X
echo "  end $(date -u '+%F %T')" >> $X
exit
}

#!/bin/bash
# #966: scanN.py at N 47 with the old degrees (the check), then N 47 and N 63; one process at nice 19.
set -u
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i966sing; O=$W/out; P=/Users/nathan/venv-314/bin/python
cd $O; X=$O/exits_scanN.txt; echo "start $(date -u '+%F %T')" > $X
for a in "47 --mmax 9:scanN47_m9" "47:scanN47" "63:scanN63"; do
  args=${a%%:*}; t=${a##*:}
  /usr/bin/time -l nice -n 19 $P -I $W/scanN.py $W/code $O/subdom_amp.json $args > $t.txt 2> $t.time
  echo "$t exit $? $(date -u '+%F %T')" >> $X
done
exit
}

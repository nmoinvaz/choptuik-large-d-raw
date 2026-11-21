#!/bin/bash
# #966: singularity_type.py rows --delta on the given jets (one process, nice 19), as #799 ran it. Usage: rows.sh OUT JET...
set -u
{
W=/private/tmp/claude-501/-Users-nathan-Source-choptuik-large-d/0726f216-9eae-4698-9a94-e79a55d0f725/scratchpad/i966sing
OUT=$1; shift
cd $W/out
echo "start $(date -u '+%F %T')" > $OUT.txt
/usr/bin/time -l nice -n 19 /Users/nathan/venv-314/bin/python -I $W/code/singularity_type.py rows "$@" --delta >> $OUT.txt 2> $OUT.time
echo "exit $? $(date -u '+%F %T')" >> $OUT.txt
exit
}

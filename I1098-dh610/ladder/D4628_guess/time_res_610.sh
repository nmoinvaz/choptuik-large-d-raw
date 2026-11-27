#!/bin/bash
# #1098 (Track A): form S residual times (2, 4, 8 parts) at the D 4628 guess with x_l 0.7062221, 2 threads
{
cd /home/nathan/Source/choptuik-large-d-1088a/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=/home/nathan/Source/choptuik-large-d-1088a/site_z
date -u "+start %H:%M:%S" > /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_res.log
nice -n 10 $(cat /home/nathan/Source/choptuik-large-d-1088a/python_path) -u /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_res.py /home/nathan/Source/choptuik-large-d-1088a/hp_z /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/../D4628_x706/guess/guess_D4628.0000.npz 2 >> /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_res.log 2>&1
echo "rc $? $(date -u +%H:%M:%S)" >> /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_res.log
exit
}

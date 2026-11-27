#!/bin/bash
# #1098 (Track A): the octo-double residual's time at x_l 0.7062221 (the D 4628 guess) at ks 6959 and 5500, and at
# x_l 0.7035589 (d4628b's first attempt's state) at ks 6959: whether the serial horizon block's cost follows the layout
{
cd /home/nathan/Source/choptuik-large-d-1088a/hp_z || exit 1
export HP_EXACT_RECIP=1 HP_EXACT_DMAT=1 HP_HORIZON_RELAXED=1 OPENBLAS_NUM_THREADS=1 PYTHONPATH=/home/nathan/Source/choptuik-large-d-1088a/site_z
PY=$(cat /home/nathan/Source/choptuik-large-d-1088a/python_path)
date -u '+start %H:%M:%S' > /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_od.log
nice -n 10 $PY -u /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_od.py /home/nathan/Source/choptuik-large-d-1088a/hp_z /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628/jump_fail1/jump_s_D4628.0000.npz 6959 1 >> /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_od.log 2>&1 &
nice -n 10 $PY -u /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_od.py /home/nathan/Source/choptuik-large-d-1088a/hp_z /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_x706/guess/guess_D4628.0000.npz 5500 1 >> /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_od.log 2>&1 &
wait
echo "rc $? $(date -u +%H:%M:%S)" >> /home/nathan/Source/choptuik-large-d-raw-1088a-live/I1098-dh610/ladder/D4628_guess/time_od.log
exit
}

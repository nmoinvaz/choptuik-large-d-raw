#!/bin/bash
# T84: the quad-double leg: T75's pin 7 and pin 5 states at the shared waypoints, each converged in quad-double with
# its own pin (qd_pinned.py), then the full-system Delta from it (qd_fullcorr.py). Two lanes of 2 threads.
R=/Users/nathan/Source/choptuik-large-d-raw/T75
cd /Users/nathan/Source/raw-T84 || exit 1
lane() {   # pin  D...
  pin=$1; shift
  for D in "$@"; do
    f=pin${pin}_D$D
    [ -f $R/$f.npz ] || { echo "missing $f" >> qd_leg_pin$pin.log; continue; }
    cp -n $R/$f.npz . 2>/dev/null
    OPENBLAS_NUM_THREADS=1 nice -n 10 ~/venv-qds/bin/python -u qd_pinned.py $f.npz $pin 2 dz >> qd_leg_pin$pin.log 2>&1
    [ -f ${f}_pinned${pin}_dz.npz ] && OPENBLAS_NUM_THREADS=1 nice -n 10 ~/venv-qds/bin/python -u qd_fullcorr.py ${f}_pinned${pin}_dz.npz 2 >> qd_leg_pin$pin.log 2>&1
  done
  echo "lane pin $pin done" >> qd_leg_pin$pin.log
}
lane 7 71.0000 71.5000 72.0000 72.8000 73.0000 73.1000 &
lane 5 71.0000 71.5000 72.0000 72.8000 73.0000 73.1000 &
wait

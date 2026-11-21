#!/bin/bash
# runs the zero-plant demonstration after the first control test has finished (2 threads, nice 19)
cd ~/Source/choptuik-large-d-raw/I1067-dh610 || exit 1
while pgrep -f "resid_test_call1" > /dev/null || pgrep -f "resid1067.py 2 .*after_call1" > /dev/null; do sleep 20; done
/home/nathan/Source/venv-i1058/bin/python -I control_demo1067.py $PWD/states/lowD1067_D3.0475_M512_ckpt_after_call1.npz 0 demo_noplant > control_demo_noplant.txt 2>&1; echo "exit $?" >> control_demo_noplant.txt

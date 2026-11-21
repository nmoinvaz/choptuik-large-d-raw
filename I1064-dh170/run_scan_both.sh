#!/bin/bash
# #1064 part 2 design 2: ks 315 (the raise; P3) then ks 293 (the control; P2), one after the other
cd /home/nathan/Source/choptuik-large-d-raw-p4/I1064-dh170 || exit 9
./run_scan.sh 315 0 ks315 "--expect315=1"
./run_scan.sh 293 1 ks293 "--expect293=1"

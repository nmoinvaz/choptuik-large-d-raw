#!/bin/bash
# #1078 root scans, one after the other (t5 allowed a first pass of 21 points at 2e-5; the 1e-5 points are filled only around the sign changes it finds). Unit i1078i.
# a: plan a (hmax 0.05, state unpolished): the point 5.140600 exists (scan_roots_a.jsonl, 971 s), the rest of the 21: --scan=5.14062,5.14100,20
# b: plan b (--hmax=0.0015 --polish=4): --scan=5.14060,5.14100,21
{
D=/home/nathan/Source/choptuik-large-d-raw-wt613/I1078-dh370
SCAN=5.14062,5.14100,20 bash $D/run_scan_roots.sh a
SCAN=5.14060,5.14100,21 bash $D/run_scan_roots.sh b --hmax=0.0015 --polish=4
exit 0
}

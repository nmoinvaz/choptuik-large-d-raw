#!/bin/bash
# The ten circles (control and four R 0.36 circles at kf 35 and at kf 37), at most six single-thread processes at a time, in this order: the first six are kf 35's five and kf 37's control
# (which makes kf 37's state), the kf 37 circles follow as slots free up. The R 0.05 circles around the pair are started by hand when the left circles of a cut have ended.
R=/Users/nathan/Source/choptuik-large-d-raw-641/I708-macm3
printf '%s\n' "35 control" "35 c_2.85_p0.25" "35 c_2.85_m0.25" "35 c_3.35_p0.25" "35 c_3.35_m0.25" "37 control" "37 c_2.85_p0.25" "37 c_2.85_m0.25" "37 c_3.35_p0.25" "37 c_3.35_m0.25" |
  xargs -P 6 -L 1 $R/job.sh

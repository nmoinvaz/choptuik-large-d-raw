#!/bin/bash
# starts M 48 when #506's last run has ended, to keep at most 6 compute processes
while ! grep -q 'kf22_ulp exit' ~/Source/choptuik-large-d-raw/I506-macm3/exits.txt 2>/dev/null; do sleep 20; done
date -u +%FT%TZ > ~/Source/choptuik-large-d-raw/I517-macm3/started.txt
~/Source/choptuik-large-d-raw/I517-macm3/M48/stage1.cmd

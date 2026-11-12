#!/bin/bash
# starts the control circle when #473's circles_B2 has ended, to keep at most 6 compute processes
while ! grep -q 'circles_B2 exit' ~/Source/choptuik-large-d-raw/I473-macm3/exits.txt 2>/dev/null; do sleep 30; done
~/Source/choptuik-large-d-raw/I507-macm3/ctl_left/control.cmd

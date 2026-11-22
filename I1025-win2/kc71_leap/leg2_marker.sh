#!/bin/bash
# ends the leg-2 samplers: they run until leg2/all.done exists; this touches it when leg 2's driver has written all2.done (or leap2.finished plus 10 min, in case all2.done never comes)
D=/d/choptuik-i935-raw/I1025-win2/kc71_leap
until [ -e $D/all2.done ]; do sleep 30; done
sleep 30
touch $D/leg2/all.done

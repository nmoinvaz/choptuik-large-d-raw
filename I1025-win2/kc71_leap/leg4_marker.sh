#!/bin/bash
# ends the leg-4 samplers: they run until leg4/all.done exists; this touches it when leg 4's driver has written all4.done
D=/d/choptuik-i935-raw/I1025-win2/kc71_leap
until [ -e $D/all4.done ]; do sleep 30; done
sleep 30
touch $D/leg4/all.done

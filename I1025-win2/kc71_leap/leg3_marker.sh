#!/bin/bash
# ends the leg-3 samplers: they run until leg3/all.done exists; this touches it when leg 3's driver has written all3.done
D=/d/choptuik-i935-raw/I1025-win2/kc71_leap
until [ -e $D/all3.done ]; do sleep 30; done
sleep 30
touch $D/leg3/all.done

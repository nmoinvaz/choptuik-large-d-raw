#!/bin/bash
# ends the leg-6 samplers: they run until leg6/all.done exists; this touches it when leg 6's driver has written all6.done
D=/d/choptuik-i935-raw/I1025-win2/kc71_leap
until [ -e $D/all6.done ]; do sleep 30; done
sleep 30
touch $D/leg6/all.done

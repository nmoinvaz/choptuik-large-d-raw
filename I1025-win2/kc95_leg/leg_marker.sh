#!/bin/bash
# ends the leg's samplers: they run until leg/all.done exists; this touches it when the driver has written allleg.done
D=/d/choptuik-i935-raw/I1025-win2/kc95_leg
until [ -e $D/allleg.done ]; do sleep 30; done
sleep 30
touch $D/leg/all.done

#!/bin/bash
# ends the leg-9 samplers: they run until leg9/all.done exists; this touches it when the driver has written all9.done
D=/d/choptuik-i935-raw/I1025-win2/kc71_leap
until [ -e $D/all9.done ]; do sleep 30; done
sleep 30
touch $D/leg9/all.done

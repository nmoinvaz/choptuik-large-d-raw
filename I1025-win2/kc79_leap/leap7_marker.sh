#!/bin/bash
# ends the leap7 samplers: they run until leap7/all.done exists; this touches it when the driver has written all7.done
D=/d/choptuik-i935-raw/I1025-win2/kc79_leap
until [ -e $D/all7.done ]; do sleep 30; done
sleep 30
touch $D/leap7/all.done

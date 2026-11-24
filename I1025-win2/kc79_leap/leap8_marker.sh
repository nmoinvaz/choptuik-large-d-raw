#!/bin/bash
# ends the leap8 samplers: they run until leap8/all.done exists; this touches it when the driver has written all8.done
D=/d/choptuik-i935-raw/I1025-win2/kc79_leap
until [ -e $D/all8.done ]; do sleep 30; done
sleep 30
touch $D/leap8/all.done

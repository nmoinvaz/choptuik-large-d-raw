#!/bin/bash
# ends the leapk95 samplers: they run until leapk95/all.done exists; this touches it when the driver has written allk95.done
D=/d/choptuik-i935-raw/I1025-win2/kc95_leap
until [ -e $D/allk95.done ]; do sleep 30; done
sleep 30
touch $D/leapk95/all.done

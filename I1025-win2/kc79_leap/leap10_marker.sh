#!/bin/bash
# ends the leap10 samplers: they run until leap10/all.done exists; this touches it when the driver has written all10.done
D=/d/choptuik-i935-raw/I1025-win2/kc79_leap
until [ -e $D/all10.done ]; do sleep 30; done
sleep 30
touch $D/leap10/all.done

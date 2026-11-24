#!/bin/bash
# ends the leap11 samplers: they run until leap11/all.done exists; this touches it when the driver has written all11.done
D=/d/choptuik-i935-raw/I1025-win2/kc79_leap
until [ -e $D/all11.done ]; do sleep 30; done
sleep 30
touch $D/leap11/all.done

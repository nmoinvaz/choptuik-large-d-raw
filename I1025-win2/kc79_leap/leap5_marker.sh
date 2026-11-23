#!/bin/bash
# ends the leg-5 (k_c 79 leap) samplers: they run until leap5/all.done exists; this touches it when the driver has written all5.done
D=/d/choptuik-i935-raw/I1025-win2/kc79_leap
until [ -e $D/all5.done ]; do sleep 30; done
sleep 30
touch $D/leap5/all.done

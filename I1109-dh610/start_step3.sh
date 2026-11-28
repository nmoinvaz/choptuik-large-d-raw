#!/bin/bash
# starts the three roots as three systemd user units
R=/home/nathan/Source/choptuik-large-d-raw-1102/I1109-dh610
cd ~
u() { n=$1; shift; systemd-run --user --unit=i1109-$n --collect --nice=10 systemd-inhibit --what=idle --who=i1109-$n --why="#1109 root $n" bash $R/run_root.sh $n "$@"; }
u r0  l1kc127k070w2.jsonl sol_l1kc127k070w2_D23.0000.npy 0.0440 0.0470 --pin=90d3e655,d1a3a641
u w01 sol_w01_D23.0000.jsonl sol_w01_D23.0000.npy 0.0400 0.0500
u w10 sol_w10_D23.0000.jsonl sol_w10_D23.0000.npy 0.0350 0.0550

#!/bin/bash
# #1021 slot 1 of the xi015d runs: run_m7d.sh for box 7, then for box 16 (each with its own controls)
set -u
{ # read whole before it runs
D=$(cd "$(dirname "$0")" && pwd)
bash $D/run_m7d.sh z7
bash $D/run_m7d.sh z16
exit
}

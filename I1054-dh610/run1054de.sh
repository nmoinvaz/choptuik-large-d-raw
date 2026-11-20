#!/bin/bash
# the two jobs in order, as one unit: job (1), then job (2) whatever job (1) gave
{
D=$(cd "$(dirname "$0")" && pwd)
bash $D/run1054d.sh
bash $D/run1054e.sh
exit
}

#!/bin/bash
{
# #1025 slot B after P4 control 2 passes (p4_criteria.log amendment 6): wait for lane A to finish, then the Mac's lane B rows.
R=/Users/nathan/Source/choptuik-large-d-raw-i1025/I1025-mac
until grep -q 'lane p4 .*p4_list_a.txt done' $R/lane_p4a.log; do sleep 30; done
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane A done; Mac lane B (p4_list_b_mac.txt)"
bash $R/lane_p4.sh $R/p4_list_b_mac.txt > $R/lane_p4b_mac.log 2>&1
echo "== $(date -u '+%Y-%m-%d %H:%M:%S') lane slotB done"
exit
}

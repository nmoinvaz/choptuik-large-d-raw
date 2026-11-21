# I1021-mac/final/record_checks: the recount of record's bit check and sheet check, run beside run_record.sh

Machine: the Mac, helper session xfchecks, nice 19, read-only. Issue
https://github.com/nmoinvaz/choptuik-large-d/issues/1021. These are the commands `../run_record.sh` runs after its own
plant (still running), on the same files, written here so that the record can be read before that plant ends. The
driver's own runs, when they come, write `../record/samebits.log` and `../record/sheet_check.log`.

- `argcount_samebits.py ../../merge_fu/merged.jsonl ../record/points_M3_r0.17.jsonl` (`samebits_merged_record.log`):
  bit check PASS, exit 0. 2556 valued records of the merged cache are the same records in the record's cache, and
  its 2630 lines are the record's first lines unchanged.
- `diag/sheet_check.py ../record/points_M3_r0.17.jsonl LEAVES --count ../record/count_M3_record_r0.17.json`, with the
  record's leaves and with `lines` (`sheet_check_record.log`):
  - PASS, exit 0 each: 3144 valued points; 2976 pairs on the leaves and 5382 on the lines; largest |dF_3| 0.0394
    and 0.056; 0 flagged;
  - each of the 3 zeros' cells has its boundary on one sheet.
- Control: `--mutate=switch` on the lines (`sheet_check_record_switch.log`): FAIL, exit 1, as required.

import datetime
p = "C:/Users/nathan/Source/signtest_lowD_1025/I1025-win/signtest_lowD/README.md"
s = open(p, newline="").read()
i = s.index("## Status")
tab = open("C:/Users/nathan/Source/signtest_lowD_1025/table_lowD_1025.md").read().strip()
now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M")
new = f"""## Result (driver finished 2026-11-20 18:17:16 UTC, written {now} UTC)

All seven rows PASS. Run from 17:33:36 to 18:17:16 UTC: inputs checked (all 25, `signtest.py` blob, WT commit; numpy 2.5.4, scipy 1.18.1), the planted control printed agree, agree, DISAGREE (`signtest_lowD_planted.log`), then the rows in the order D 14.5, 14, 13.5, 12, 11.5, 11, 10.5. Every row's system check had the same step count as its record and |F| within the record's (`same: true`), so each signtest ran on the record's own discrete system. A row passes if both lambda -+ 0.02 have agree true and opposite signs.

{tab}

Row wall times (4 BLAS threads, BelowNormal): D 14.5 9.1 min, D 14 5.7, D 13.5 5.4, D 12 5.6, D 11.5 5.7, D 11 5.9, D 10.5 6.2; 43.6 min for the seven rows. The counts of singular values of Q M below 1e-12 and 1e-15 fall from 40 and 10 at D 14.5 to 0 at D 11 and 10.5. The log's summary: seven lines `D <D> k_c <kc>: PASS`. A passing signtest checks the rounding of the determinant, not the accuracy of M's construction. The reading of the rows stays with #1025.

## Files

| file | what |
|---|---|
| `README.md` | this file (written before the run; the status and result sections updated) |
| `signtest_lowD_driver_v2.sh` | the driver, byte-identical to raw `I1025-mac/signtest_lowD_driver_v2.sh` (blob c4f92d36) |
| `signtest_lowD.log`, `signtest_lowD.jsonl`, `signtest_lowD_planted.log`, `signtest_lowD_rows/D*.log` | the driver's log, its 21 JSON lines (7 system checks and 14 signtest lines), the control and each row's full output |
| `prep_raw_inputs_1025.sh`, `prep_raw_inputs_1025.log` | how the RAW input folder was made from pinned blobs by `git show` (22 files) |
| `start_lowD_1025.cmd`, `publish_lowD_1025.sh` | the detached launcher and the copy-and-push script |
"""
s = s[:i] + new
open(p, "w", newline="").write(s)
print("ok", now)

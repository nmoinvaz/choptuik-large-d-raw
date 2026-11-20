# I1021-mac/sheet_rpi5cap: the sheet check of rpi5's #1013 upper box, step 1 (xi1 0.17)

Machine: the Mac, helper session xfchecks, nice 19, 20 Nov 2026. For https://github.com/nmoinvaz/choptuik-large-d/issues/1013
(the coordinator's message: rpi5's counts stay on hold until this check). Inputs: `I1013-rpi5-cap/m3/` at raw 35affed8,
`points_M3_r0.17.jsonl` (627 lines), `leaves_M3_upper_r0.17.jsonl` (198 leaves), `count_M3_upper_r0.17.json`; their
sha256 are in `in/SHA256SUMS`, and the files are not copied here. Check: `diag/sheet_check.py` (see `../README.md`), on
the leaves with `--count`, along grid lines, and with `--mutate=switch`, which must fail (`sheet_check.log`,
`sheet_check_mutate.log`).

Result: FAIL. 615 points have F_3 (fix.ok); argcount counts 614, since (4.35843935, 0.60654321) is under its 10 sigma
guard (|R| 4.6e7 against 7.8e7), while its F_3 is on the box's sheet. 3 pairs are flagged, all at the box's last column
A 4.3623456. There (4.3623456, 0.50654321) has F_3 +0.1985-0.1122j, and w/w_inf 0.5565, 0.5815 and 0.6065 have
-0.2117-0.0325j, -0.1837-0.0107j and -0.1379+0.0126j. Their neighbours on the box's sheet have +0.0034-0.3980j
(4.3584394, 0.6065) and +0.0040-0.3477j (4.3623456, 0.7065). So these four points are on other sheets: 0.5065 on one, and
0.5565-0.6065 on another (consecutive steps 0.036 and 0.052). The same points failed the partial check in
`diag/sheet_all.log`. Cells across a switch: 2 of 198, A 4.1123-4.3623 by w/w_inf 0.5065-0.6065 and 0.6065-0.7065. Both are
among the count's 13 unresolved cells. The 185 resolved leaves (all W 0) and the other 11 unresolved cells hold no
flagged pair.

# I1021-mac/sheet_rpi5fix: the sheet check of rpi5's #1013 sheetfix (the 2 failing cells recounted at 6da7da7b)

Machine: the Mac, helper session xfchecks, nice 19, 20 Nov 2026. For https://github.com/nmoinvaz/choptuik-large-d/issues/1013.
Inputs: `I1013-rpi5-cap/sheetfix/m3/` at raw e12701e3 (points 630 lines, the sheetfix leaves and count; sha256 in
`in/SHA256SUMS`, files not copied). Its first 622 lines are byte for byte step 1's points file (raw 35affed8) without the
5 removed records, in order (sha256 45856355..., as rpi5's `exits.txt`); lines 623-630 are the 8 recomputed points.
Check: `diag/sheet_check.py` on the sheetfix leaves with `--count`, along grid lines, and `--mutate=switch` (must fail).

Result: PASS. 619 valued points; 0 of 33 leaf-edge pairs and 0 of 1118 grid-line pairs flagged, largest |dF_3| 0.0563;
cells across a switch 0 of 2; the planted switch fails. The 8 recomputed points, all at A 4.3623456, read on the box's
sheet: F_3 +0.0021-0.4549i (w/w_inf 0.5065) to +0.0037-0.3724i (0.6565); (4.3623456, 0.6065) is 6e-4 from
(4.35843935, 0.6065). Both cells stay unresolved (rpi5's count: 2 leaves, 0 splits, boundary winding NaN, no zeros). 3 of
the 8 are under argcount's 10 sigma guard: w/w_inf 0.50654321 (|R| 1.14e8 against 1.20e8), 0.60966821 (4.10e7 against
5.60e7) and 0.61591821 (3.87e7 against 4.34e7). Cell 1's corner (4.1123456, 0.50654321) stays without value (info 2.4e8).

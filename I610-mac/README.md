# I610-mac: hp's D 40.020065 state polished in quad-double with and without the kf 13 cut, against RT's #404 plateau

Machine: the M5 Mac (coordinator), the hpkernel of /Users/nathan/venv-314. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/610

Commands (from hp/, choptuik-large-d 7c15f24), K = 13 and -1 (no cut):

    python3 -u scan_qd.py RAW/I610-mac/qd_kfK.jsonl data/states/up7_D40.0201.npz 40.020065 --kfreeze K --threads 4

Each converges the start in quad-double and stops (D_END is its own D): max|F| 8.3e-57 (kf 13) and 1.2e-57 (no cut). The records hold Delta in four parts (Delta_q). Both runs saved their state under the same name qd_D40.020065.npz, so only the no-cut state survived and it is not kept here; the Deltas are the records'.

Delta: kf 13 1.88845166449061383795358297124, no cut 1.88845166449061539504027634996 (no cut - kf 13 = 1.557e-15). RT's plateau (I404-win roots a101_32x107/115/123 at D 40.020065) lies -1.3e-17, -3.0e-18 and -1.7e-17 from the no-cut value and +1.54e-15 from the kf 13 value.

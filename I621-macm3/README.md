# I621-macm3: the slowest decaying test-field rate mu(D) on the DSS at D 4, 5, 6 and 8.25

Machine: macm3 (Apple M3, 24 GB RAM), venv-macm3-314 (Python 3.14.3, python-flint 0.9.0, hpkernel cp314 neon of 2026-11-09), worktree ~/Source/choptuik-large-d-b596 at main b5d69cc2, modecount_cx built from 742bb879's source. Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/621 (commands: the coordinator's comment of 2026-11-13 01:44 UTC; macm3 assigned by message of 2026-11-13 01:44 UTC). Started 01:45 UTC.

Commands (run_621.sh), from the root of the worktree, nice 10, caffeinate -is. Step 1: python3 -u hp/scan_hp.py <raw>/I621-macm3/scan_D4to6.jsonl hp/data/lowD_states/lowDn_D4.0000_M48.npz 6.0 --dD 0.5 --maxdD 0.5 --kc 80 --ks 200 --threads 6 --tag i621 --attempts <raw>/I621-macm3/scan_attempts.jsonl (saves i621_D5.0000.npz and i621_D6.0000.npz next to the jsonl). Step 2: python3 -u hp/modecount_test_axis.py STATE --lo=-1.5 --hi=-0.02 --s=0 --threads=3 --out=<raw>/I621-macm3/axis_TAG.jsonl for STATE = lowDn_D4.0000_M48.npz (the control, TAG D4_control), i621_D5.0000.npz (D5), i621_D6.0000.npz (D6) and hp/data/states/up_D8.2500.npz (D8.25), two at a time, 3 threads each (D4_control with D5, then D6 with D8.25).

Written before the run (the issue's and the comment's). Pass: the D 4 control gives -0.36512 (to 1e-6; the stored value is -0.3651202372); at D 5 the slowest decaying real zero is reported against Mittal, Gundlach and Martel's -0.448 (arXiv:2609.17207, as quoted in matter/LITERATURE.md section 8); each record holds the zeros found on the line, and the slowest decaying one per D is tabled. The coordinator then computes delta(D) = (D - 2 - mu) gamma from these mu and our gamma, with the mutation D - 2 -> D - 3 as the control that must fail at D 5. About 1 to 1.5 h.

## D 5 (the coordinator's reply of 2026-11-13 02:19 UTC)
scan_hp.py's steps are adaptive and only the last lands on D_END, so scan_D4to6 saved i621_D4.2500, 4.3281, 4.4258, 4.5479, 4.7004, 4.8912, 5.1296, 5.4276, 5.8001 and (at the end) 6.0000, not 5.0000. The coordinator's command: one step from the D 4.8912 state, python3 -u hp/scan_hp.py <raw>/I621-macm3/scan_to5.jsonl <raw>/I621-macm3/i621_D4.8912.npz 5.0 --dD 0.11 --maxdD 0.11 --kc 80 --ks 200 --threads 6 --tag i621 --attempts <raw>/I621-macm3/scan_attempts_to5.jsonl, then the D 5 axis run; fall back to the scan from D 4 with D_END 5.0 if the step fails. run_621.sh's wrapper (pid 775) was stopped with SIGTERM at 02:19 UTC while its scan (still running, D 5.8001 saved) went on, so that the D 4 control axis would not start beside the 6-thread D 5 step; run_621b.sh (waits for the scan's pid, records its end without an exit status, makes the step, then the four axis runs two at a time) replaced it.

## Results (2026-11-13 02:51 UTC; exits.txt: scan_D4to6 ended 02:20:28 (exit status not observed), scan_to5 exit 0 02:21:50, axis_D5 02:36:45, axis_D4_control 02:38:13, axis_D8.25 02:47:43, axis_D6 02:50:55 UTC, all axis runs exit 0)

| D | state | M | F of the state | real zeros on [−1.5, −0.02] | slowest decaying real zero μ | Im λ | ω | seconds |
|---|---|---|---|---|---|---|---|---|
| 4 (control) | `lowDn_D4.0000_M48.npz` | 48 | 3.76e-31 | 1 | -0.3651202705 | 3.7e-20 | 1.82361679 | 982 |
| 5 | `i621_D5.0000.npz` | 48 | 1.02e-30 | 1 | -0.4430361582 | 1.4e-19 | 1.95026896 | 894 |
| 6 | `i621_D6.0000.npz` | 48 | 2.34e-31 | 1 | -0.5052240827 | -9.9e-22 | 2.08779543 | 761 |
| 8.25 | `up_D8.2500.npz` | 48 | 5.44e-31 | 1 | -0.6124708660 | 7.7e-20 | 2.34147164 | 570 |

D4 control against -0.36512: -2.705e-07; against the stored -0.3651202372: -3.327e-08
D5 against Mittal-Gundlach-Martel -0.448: +4.964e-03 (1.11%)

Every run: 75 grid points (h = 0.02), one phase jump, no poles within omega/2 of the line, one refined zero. The D 4 control passes. The D 5 value does not match Mittal, Gundlach and Martel's -0.448 to their digits. mu is at one resolution (M 48, the 11-node layout); no M convergence at D 5, 6, 8.25 here. delta(D) = (D - 2 - mu) gamma and the mutation check are the coordinator's.

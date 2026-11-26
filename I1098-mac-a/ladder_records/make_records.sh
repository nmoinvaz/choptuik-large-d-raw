#!/bin/bash
# #1098: every ladder record in this folder, written again from its point's files by hp/ladder_record.py (wip/large-d-form-s
# or fastmul6, the version that counts a run of harmonics released at once as one pending term). Each point's
# direct_s.jsonl is replaced, not appended to, so the exporter sees one record per D.
#
#     make_records.sh HP_DIR    (PYTHONPATH must give an hpkernel with form S, for form_s.py's import)
{
HP=$1
L=$(cd "$(dirname "$0")" && pwd)
PY=${PY:-python3}
[ -s "$HP/ladder_record.py" ] || { echo "usage: make_records.sh HP_DIR"; exit 1; }
TR=$HOME/.Trash/ladder_records_$(date +%s)
mkdir -p $TR
rec() {  # D final start logs... -- options
  d=$1; shift
  [ -s $L/D$d/direct_s.jsonl ] && mv $L/D$d/direct_s.jsonl $TR/D${d}_direct_s.jsonl
  $PY $HP/ladder_record.py "$@"
}
F="fastmul6's 1.7e-60 Moebius split offset (I1098-dh610/mpcheck/horizon300_h21.log), which fastmul7 removes"
rec 250 $L/D250/release_ls_h31_D250.0000.npz $L/D250/direct_s.jsonl $L/D250/tail_release_ls.jsonl --start $L/D250/start.npz \
  --kstar 15 --gain 2.3211e27 \
  --info "mobius_stage_ks|-2.4606e-17|measured: the h13 re-converge from the Moebius M 32 state (a 8, ks 392 = 1.5n + 20, whose jump reported ks+200 |dF| 1.6e-36) to u ks 422 moved Delta by this. The final u value does not carry it (I1098-mm5/ladder/D250)" \
  --note "D 250 ladder point on mm5, fastmul6 (d368a0c0 kernel, Python 478e9d86): the jump (Moebius ks 392) and h5-h13 (ladder_point.sh), then the u tail at M 32, ks 422 (ladder_tail.sh u). Gain from gainq.py at kfreeze 15 on the h13 state (dh610)"
rec 300 $L/D300/release_ls_h31_D300.0000.npz $L/D300/direct_s.jsonl $L/D300/tail_release_ls.jsonl --start $L/D300/start.npz \
  --kstar 15 --gain 7.7459e27 \
  --xcheck "horizon|3.5e-29|Moebius (a 8, ks 800, M 32) after h23 against u (ks 506, M 32) after h21 plus u's pending h23 dDelta, fastmul6 on mm5 (I1098-mm5 h23test, raw cf9053d06). Moebius at ks 1000, a 4 and a 6 agree with ks 800 to 1e-39. The Moebius ks-600 tails turned at h23 by -3.9e-22, an artefact of its horizon truncation (1.2e-53 in F) times the kfree-23 gain;M|7.27e-26|the M 32 to 48 shift at kfree 13 on fastmul6 (I1098-mm5/ladder/D300m48, Moebius ks 600). The M 48 tail through h21 matched M 32's (h21 +1.4485e-23 against +1.4486e-23);machine|0.0|dh610 against mm5: the same Delta to 40 places after h15 outer 0 of the Moebius M 32 tail from S300 (I1098-dh610/chord_test, I1098-mm5/ladder/D300)" \
  --note "D 300 ladder point on mm5, fastmul6 (d368a0c0 kernel, Python 478e9d86): D300_u6 (u ks 306, kfree 13, I1098-mm5/fix6) at ks 506 (variant ks+200), then the u tail h15..h31 at M 32 (I1098-mm5/ladder/D300u). Gains from gainq.py on the final state (dh610): kfreeze 13 7.53e24, 15 7.75e27, 17 6.40e30, 21 2.01e36, 25 1.81e41, 29 5.09e46, 31 1.52e47"
rec 360 $L/D360/release_ls_h23_D360.0000.npz $L/D360/direct_s.jsonl $L/D360/tail_release_ls.jsonl --start $L/D360/start.npz \
  --kstar 15 --gain 1.6793e28 \
  --note "D 360 ladder point on dh610, fastmul6 (site_y: d368a0c0 kernel, Python 478e9d86, no inner chord steps): the jump (Moebius ks 557) and h5-h13 by ladder_point.sh, then the Moebius tail at M 32, ks 957, kmax 23 (ladder_tail.sh mob). ks_gate.py at the jump's state read 4.2e-50 at ks 557 and 1.6e-66 at ks 757, so ks 957 is past the 1e-64 bar. No cross-check exists. The Moebius values carry $F. Gain from gainq.py at kfreeze 15 on the final state (dh610)"
rec 432 $L/D432/release_ls_h23_D432.0000.npz $L/D432/direct_s.jsonl $L/D432/tail_release_ls.jsonl --start $L/D432/start.npz \
  --kstar 15 --gain 2.3003e28 \
  --xcheck "horizon|5.646e-28|u (ks 731, M 32) against Moebius (a 8, ks 1065, M 32) after h15, fastmul6 on mm5: the difference is u's own pending h15 dDelta (-5.65e-28), not taken. u's h17 pending (-2.49e-19) matches Moebius's h17 change (-2.4908e-19) to the printed figures. u's inner solves did not converge past h17 (the u series loses accuracy above about D 300), so the check ends there (I1098-mm5/ladder/D432/tail_u, tail_mob)" \
  --note "D 432 ladder point on mm5, fastmul6 (d368a0c0 kernel, Python 478e9d86): the jump (Moebius ks 665) and h5-h13 (ladder_point.sh), then the Moebius tail at M 32, ks 1065, kmax 23 (ladder_tail.sh mob). The Moebius values carry $F. Gains from gainq.py on the final state (dh610): kfreeze 15 2.30e28, 17 3.75e31"
rec 519 $L/D519/release_ls_h23_D519.0000.npz $L/D519/direct_s.jsonl $L/D519/tail_release_ls.jsonl --start $L/D519/start.npz \
  --kstar 15 --gain 1.9745e28 \
  --note "D 519 ladder point on mm5, fastmul6 (d368a0c0 kernel, Python 478e9d86): the jump (Moebius ks 796) and h5-h13 (ladder_point.sh), then the Moebius tail at M 32, ks 1196, kmax 23 (ladder_tail.sh mob). No u check exists (the u tail stalled at h15). The Moebius values carry $F. Gains from gainq.py on the final state (dh610): kfreeze 15 1.97e28, 17 4.08e31"
rec 1000 $L/D1000/release_ls_h31_D1000.0000.npz $L/D1000/direct_s.jsonl $L/D1000/m48_6_release_ls.jsonl $L/D1000/tail6_release_ls.jsonl \
  $L/D1000/tail6b_release_ls.jsonl --start $L/D1000/start_D1000_M48_fastmul5.npz --kstar 17 --gain 5.2732e29 \
  --xcheck "M|4.03e-34|M 48 against M 64 at kfree 31 on fastmul6: tail6b's state after h23 resampled to M 64 and released through h31 (I1098-mm5/fix6/m64_1000_6, raw 324d53fa2, state blob 59fdd0ab). The shift is +4.03e-34 at kfree 23 and at kfree 31. Earlier, the M 32 to 48 shift at kfree 13 was -2.1e-26 (D1000_M48_6 against D1000_base6)" \
  --note "D 1000 ladder point on mm5, fastmul6 (d368a0c0 kernel, Python 478e9d86): fastmul5's M 48 kfree-13 state re-converged on fastmul6 (D1000_M48_6), the tail h15, h17 (D1000_M48_tail6, whose later releases used the old residual-only criterion and are superseded) and h19..h31 with --ddelta 1e-25 (D1000_M48_tail6b), Moebius a 8 ks 1517. h23-h31 were released at once with nearly one pending dDelta (tail6b about 2.5e-27, the M 64 run +1.12e-27 at each of h25-h31), which reads as the base residual's first-order term rather than each harmonic's own, so err_tail counts that run once. The Moebius values carry $F. Gains from gainq.py on the final state (dh610): kfreeze 13 3.29e22, 17 5.27e29"
exit
}

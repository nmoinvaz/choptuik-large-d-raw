# route1-mac: route 1's tests before kernel code (notes/QUAD_DOUBLE.md section 13.4), run on the Mac

Machine: the Mac (coordinator session), 2026-11-03. `pole_test.jsonl` and `pole_test.log`: test T5, `hp/pole_test.py`
on the nine stored series states of T84-mac/horizon_radius.py (hp/data/states/up*_D40..60 of the code repository;
T73/t73/pin7_D67.7422, T84-mac/pin7_D70.5000, T75/pin7_D72.4000 and pin7_D73.2657 of this repository): the horizon
series' radius for the horizon datum a_h scaled by 1 + delta, its line in ln(1/delta), the Domb-Sykes ratios of the
a field's tau-mean, the control against horizon_radius.jsonl (D moved by 1e-4 with the state held) and the basin
thresholds delta_max(u0) each line implies. Started 16:30 UTC, after section 13 was committed (code repository 618f0b2).

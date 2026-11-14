(1) attempt times

| run | from D | a | to D | corrector steps | seconds in the corrector | accepted |
|---|---|---|---|---|---|---|
| #726 quad-double | 112.75 | 0.25 | 113 | 8 | 495 | False |
| #726 quad-double | 112.75 | 0.125 | 112.875 | 5 | 412 | False |
| #726 quad-double | 112.75 | 0.0625 | 112.812 | 9 | 686 | False |
| #726 quad-double | 112.75 | 0.03125 | 112.781 | 7 | 748 | False |
| #739 octo-double (A) | 112.75 | 0.125 | 112.875 | 5 | 577 | True |
| #739 octo-double (B) | 112.75 | 0.25 | 113 | 5 | 593 | True |

(2) Delta_full - Delta_held (extra, not asked)

control, D 112 from #726's quad-double state: +4.2096e-13 (#726 reported +4.2096e-13) ok
D 113 from the octo-double state of B: Delta_full - Delta_held = +4.3655e-13; delta_all.csv err 3.0e-12 (chain_fit), ratio 0.146
ratio of the shift D 113 to D 112: 1.037 (#726's successive ratios fell 1.055 to 1.039); ratio to the err at D 112 was 0.145

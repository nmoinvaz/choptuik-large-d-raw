# T133-macm3: setup of the runner macm3, hp build and bit-identity checks against stored references

Machine: macm3, a MacBook with an Apple M3 (4 performance + 4 efficiency cores, 8 threads), 24 GB memory, macOS 26.3.1.
Comms entry: 2026-11-06 14:39 UTC cloud to macm3 (T133). Steps: clones and git identity, Rust stable and the venv
~/Source/venv-macm3 (Python 3.13), the hp build (build.log), then highm_check.py ref, scaled, jets and its
--mutate=kappa control, and ojet_check.py against od-mac/ojet_T113_D148.jsonl, each with its own log here.

Results: build.log (exit 0, 869 s, peak 11.9 GB in build_peak_kb.txt); check_ref.log (exit 0, 72 bit-identical),
check_scaled.log (exit 0, control fires), check_jets.log (exit 0, 28 bit-identical), check_jets_mutate_kappa.log
(exit 1, 28 of 28 differ, the control); ojet_T113_D148.log/.jsonl (exit 0, 2353 s) and ojet_compare.log (every
quantity equal to od-mac/ojet_T113_D148.jsonl, d_oq largest relative difference 0). exits.txt lists the five exits.

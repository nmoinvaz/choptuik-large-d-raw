# T109-mac: qjet_check.py at six chain bases, D 79.8-88.1

Machine: mac (Apple M5), checkout ~/Source/choptuik-qdjet (hp/, branch feat/qd-jet, unchanged), python /Users/nathan/Source/venv-qdjet/bin/python.
Comms entry: 2026-11-05 02:23 UTC cloud to mac
Command per base: nice -n 10 python qjet_check.py ../../choptuik-large-d-raw ../../choptuik-large-d-raw/T109-mac/qjet_check.jsonl --threads 2 --state <S> > T109-mac/qjet_<D>.log
Bases: anm-mac/run_trend_pin3_qd3/anm_pin3_D79.7657.npz, qd4 D81.5157, qd6 D82.2188, qd7 D84.7188, qd9 D86.9494, qdj1 D88.1184.
Follow-on T109b: jet_check.py (double-double jet, 2.0.0 build), output jet_check.jsonl.
Started 2026-11-05 02:24 UTC.

Done 2026-11-05 02:27 UTC. qjet_check.py: bases D 79.7657, 81.5157, 82.2188, 84.7188 exit 0, D 86.9494 and 88.1184 exit 1 (order 1: e1q <= 1e-3 e1d fails). T109b jet_check.py: exit 1 (worst ratio 2.2e-16 against 1e-20), coef_norms and rows equal to the last record of anm-mac/jet_check.jsonl.

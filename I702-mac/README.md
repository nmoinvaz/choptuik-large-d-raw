# I702-mac: the real S₁ twins with the zero factor in place (#702)

Machine: mac (the coordinator's Apple M5 Mac), one process under `nice -n 10`, single-threaded.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/702

Records of `solver/inner_amp/pade_twin_near.py real` with the gate as amended by #702 (notes/PADE_FAR_END.md §13.8):
the real stage (`real.log`, `real.json`) and its `c1dup` mutation (`real_mutate_c1dup.log`, `real_mutate_c1dup.json`).
Each `.stdout` file is the run's terminal output.

`control.json` is a copy of `I689-mac/control.json` (raw fade0a9, sha256
8c99499bb2ee5efb27e3fa6bff2fbe60034bcc17104de2d7f32ae7c52219afe6), the control stage of #689, which the real stage
reads. The control checks are unchanged since that run.

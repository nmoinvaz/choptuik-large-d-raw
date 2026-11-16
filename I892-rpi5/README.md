# I892-rpi5: sigdss at eta = 0.3, does the smoothness prior hold Delta at D 9 to 11 (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, aarch64 Linux, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/892 (follows #846 and #859, matter/SIGMA_DSS.md 11). Script (the
coordinator's, md5 7ab78065, unedited): `run892.sh`, run from `solver/matter/` of the worktree
`~/Source/choptuik-large-d-892` (wip/i892-rpi5 at origin/main 5311991e, never committed), numpy only, one process
at nice 10, `OPENBLAS_NUM_THREADS=2`, the five walks two at a time.

Order: `sigdss_band.py width` at the six march states (D 8.0 without a prior is the control; D 9.0, 10.0, 10.5 from
`data/sigdss_m03up.npz`, D 10.5 and 11.0 from `data/sigdss_m03hi.npz`), the 20-Jacobian control walk from D 8.0,
then the five walks without the prior (up to 150 Jacobians each), then `width` at each walk's end.
Exits and wall times: `exits_892.txt`; versions: `env.txt`; each command's stdout and stderr: `<name>.log`;
JSON records: `width.jsonl`, `walk.jsonl`, `walk_*.jsonl`, `width_end.jsonl`; the walks' end states: `walk_*.npy`.

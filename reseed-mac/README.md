# reseed-mac: re-seeding the horizon data of the large-D solver from the last node (design and tests in notes/RESEED.md of branch wip/reseed)

Machine: the Mac, a coordinator subagent.

Comms: the coordinator's task of 2026-11-05 (re-seeding, after the toy study of notes/QUAD_DOUBLE.md 13.21). Code on
branch `wip/reseed` of the code repository (`hp/reseed.py`, `hp/reseed_check.py`). Inputs are read-only states of
`anm-mac/run_trend_pin3_qd9/` and `anm-mac/run_trend_pin3_qdj1/`.

# T130-mac: a second octo-double path past 175.5, steps of 0.5, for the error column of T129's rows

Machine: the Mac (Apple M5, NEON), run by the coordinator session. Main checkout at ba1637c (Python), kernel from the
octo-double build of od-mac (f18d27b, multidouble 4.0.0; main's Rust is unchanged since the merge 7d6198d). 6 threads,
nice 10. Comms entry: 2026-11-06 cloud to win2, win (T129, T130, T131).

T129-win2 runs the chain from the same state with h_max 1.0; this path takes h_max 0.5, so every other point lands on
T129's D values and hp/export_delta_all.py compares the two there.

  python3 anm_run.py <raw> <raw>/T130-mac/chain --state T127-win2/chain2/anm_pin3_D175.5246.npz --kfreeze 3 --N 24
    --eps 1e-14 --h_max 0.5 --steps 300 --D_max 200 --threads 6 --corrector qd --tol_qd 1e-28 --qd_it 12 --trend T75
    --jet_o 1 --reseed 2 --reseed_q 1

Log chain.log, states and anm_run.jsonl in chain/. Stop at D_max, on a degenerate series, or after 16 h (about 1070 s per step of 0.5 here, 49 steps).

Stopped at D 183.5246 (2026-11-06 18:24 UTC, last state chain/anm_pin3_D183.5246.npz) to give this Mac's cores to T132's probe; T134-macm3 is the second path for the rows past 193.77.

# T87-mac: sigma_18 at wf 0.99, 1.00, 1.01, K 37, J 1000 / 960 bits; pilot (b) at J 1250 / 1280 bits

Machine: mac (Apple M5), python-flint 0.9.0, 2 worker processes per run at nice 10.
Task: T87, the follow-on named in the comms entry "cloud to mac" of 2026-10-27 23:23 UTC (T86's recipe one order up). Source: `solver/inner_amp/` of origin/main 9e669de (worktree `choptuik-t83`, amp_flint_par.py unchanged since T83).

Command (from `solver/inner_amp`, wf 1.00 pilot):

    amp_flint_par.py 1.0 37 J BITS --procs 2 --fit phys --mf 6:12 --fit-step 1 --out <file>

- `scan37J1000/`: J 1000 at 960 bits, variant (a): the wf 1.00 pilot, then wf 0.99 and 1.01. Logs `w<wf>.log`.
- `scan37J1250/`: J 1250 at 1280 bits, variant (b), wf 1.00 pilot only.
Gate for (a): err18 at most 1e-10 |sigma_18|, sigma_17..15 within their errs of T86-mac's wf 1.00 file.

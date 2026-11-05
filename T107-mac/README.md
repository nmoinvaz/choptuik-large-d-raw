# T107-mac: the smoke test of the low-D Taylor leg driver (hp/lowD_taylor_leg.py) at M 48

Machine: the Mac (coordinator session), 2026-11-05, with the 1.9.0 jet build (venv-anm). Procedure
notes/LOW_D.md 15 A: from hp/data/lowD_states/lowD_D4.0000_M48.npz, targets 3.99 and 3.98, --newton_its 4,
--threads 2, the driver at branch feat/jet-all-sizes of the code repository.

- `smoke_none/`, `smoke_none.log`: no mutation; both targets in one attempt each, Newton 3.4e-30 and 8.5e-31 with
  full steps.
- `smoke_halve/`, `smoke_halve.log`: --mutate halve (the first attempt at every base given one Newton call); every
  base's first attempt fails and its half step converges, and the leg still reaches both targets.
- `smoke_const/`, `smoke_const.log`: --mutate const (the prediction replaced by the base state); the check fails at
  the first target and the driver exits 1.

The none and halve runs were piped through grep, so their exit status was not captured; both printed "done". The
const run was rerun without the pipe for its exit status.

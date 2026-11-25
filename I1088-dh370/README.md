# I1088-dh370: Track A of #1088 on dh370, the full system's weakest singular values at three chain states

Machine: dh370 (Fedora 45, i7-8700, 12 threads), the venv of `~/Source/choptuik-large-d-1082` (hpkernel at a9975061,
main's kernel), 6 threads at nice 10, systemd user units `i1088a-wsv` and `i1088a-wsv2`.
Issue: https://github.com/nmoinvaz/choptuik-large-d/issues/1088
The runs ran in `~/Source/choptuik-large-d-1088a/work/` (code of `wip/large-d-jump` fetched as a tarball), and their
files were copied here from the Mac, which pushed this folder.

- `weak_sv/`: `weak_sv.py` (from `I1088-mac-a/probes/`, its path to hp/ edited) on the order-293 chain's states at D
  245.5586, 254.5903 and 263.5987 (`I966-dh370/ks_chain3b/`), kfreeze 13, 10 directions, 6 iterations
  (`run_wsv.sh`); `weak_sv2.py` deflates the weakest six to resolve the Delta mode (`run_wsv2.sh`, logs added when
  done).

Form S jumps (#1088, `hp/form_s.py jump` on branch `wip/large-d-form-s`, the kernel built on dh370 by the low-memory
release recipe from 38943f4f, `~/Source/choptuik-large-d-1088a/fs`), each in its own folder with `run.log` (start, end,
the command), `jump.log` and `jump_s.jsonl` (one record per Newton step), via `run_jump.sh`:
- `j300_junk10/`: D 300 with the 10 weakest no-Delta directions frozen; stopped by hand after step 0.
- `j300_held/`: D 300 with p1's harmonics 5-13 held at the guess's values; converged, the state `jump_s_D300.0000.npz`
  (form S's layout, eight parts).

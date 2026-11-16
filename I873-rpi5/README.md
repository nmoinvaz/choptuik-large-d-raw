# I873-rpi5: Theorem A(M = 1)'s lemmas S, 6a and 6b1 reproduced on aarch64 Linux (Raspberry Pi 5)

Machine rpi5 (Raspberry Pi 5 Model B, 4 cores, 8 GB, Ubuntu), issue
https://github.com/nmoinvaz/choptuik-large-d/issues/873. Script (the coordinator's): `run873.sh`, the commands of
proof/A_certify.md 11.7 and 12 from `solver/proof/` of the worktree `~/Source/choptuik-large-d-873` (wip/i873-rpi5 at
origin/main 724d45b9, never committed), one process at a time at nice 10. Exits and wall times in `exits_873.txt`;
versions in `env.txt`; each step's output in `<name>.log`.

- `sector.log`, `lemma6_sector_1e-9.json`: lemma S, the old sector lemma and the flat estimate; `sector_series.log` is the
  series control (must report False). `usys.log`: the u-system against validated_int's.
- `path_point.log`, `lemma6_path_point.json`, `path_box.log`, `lemma6_path_box_1e-9.json`, `path_krawczyk.log`: lemma 6a's
  lower path, at the point and over the box h = 1e-9, and the Krawczyk test.
- `jump.log`, `lemma6_jump_1e-9.json`: the backward jump on the Pi's own box; `jump_stored.log`,
  `lemma6_jump_stored_box.json`: on the stored box. `jump_swap.log` and `jump_coords.log` are its controls (coords is not
  caught, A_certify.md 11.6).
- `disc.log`: lemma6b1_disc.py's self-test. `cover_check_stored.log`: the stored covering checked on the Pi before
  anything is recomputed. `cover_ray.log`, `cover_rows.log`, `lemma6b1_runs_rpi5/`: the Pi's own ray and 12 rows.
  `cover_check.log`, `lemma6b1_check_1e-9.json`: the check of the Pi's covering. `cover_sign.log`, `cover_drop.log` and
  `cover_control.log` are its controls.

Script fault and the rerun (reported to the coordinator, who approved the rerun):

- `cover_rows` in `run873.sh` exited 0 in 0.19 s. `lemma6b1_cover.py rows` skips every row whose
  `lemma6b1_runs/row_JJ.json` exists, and the worktree holds the stored rows, so the script recomputed only the ray
  (`cover_ray.log`, 41 s). Its `cover_check.log` (PASS) is therefore the Pi's ray over the STORED rows, and
  `lemma6b1_runs_rpi5/` (copied by the script) holds the Pi's `ray.json` and the stored `row_*.json` (byte for byte) and
  `control.json`; `lemma6b1_check_1e-9.json` is that first check.
- `run873_rows_b.sh` (mine, approved) then recomputed every row with `lemma6b1_cover.py row --j=J` (`rows_JJ_b.log`),
  checked again (`cover_check_b.log`, `lemma6b1_check_1e-9_b.json`), copied the run folder to `lemma6b1_runs_rpi5b/`
  (the Pi's own ray and 12 rows) and ran the drop control again (`cover_drop_b.log`). The exits are in `exits_873.txt`
  with names ending `_b`.
- `cmp873.py`, `compare_stored.txt`: this folder's JSON against the stored files of `solver/proof/`, and the per-row
  table of `lemma6b1_runs_rpi5b/` against the stored rows. The stored folder was copied before the run, since the
  worktree's `lemma6b1_runs/` was overwritten.

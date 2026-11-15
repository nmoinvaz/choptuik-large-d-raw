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

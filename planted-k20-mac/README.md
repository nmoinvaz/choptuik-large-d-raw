# planted-k20-mac: the K = 20 stage logs of planted_k20.py (notes/PLANTED_SELECTION.md section 12)

Machine: the Mac (coordinator session), 2026-10-31. `dry/`: the dry run of section 12.0 item 0 on a synthetic sigma_20
(planted_k20_dry.py, the C19-BP [6/13] sum's own, section 11.6's first ring-free type-passing sum; its scan files and
records are not kept, the script regenerates them), started 05:4x UTC after the procedure (section 12.0, code repository
557dca2 of 2026-10-30, amended ff66864) and the scripts (7f96edd) were committed. `generate.log` is the
generator's output, `converge.log` and `converge_mutate_<err|low|pilot|ratiolaw|amend>.log` the first stage and its five
mutations (each firing), `stages.log` the start and exit of each later stage. `real/`: the stages on the real sigma_20
(T89-mac's scan41J1250 and scan41J1500 files), 06:00-06:26 UTC after the dry run: `converge.log` (margins 123-154, every
check passing) and its five mutations (each firing), then `plants.log`, `real.log`, `ring.log`, `calib.log`,
`recomplete.log`, `project.log`, `combine.log`, all exit 0; `stages.log` has the times. Sections 12.1-12.10 of the notes.

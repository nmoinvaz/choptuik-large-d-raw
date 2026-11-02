# planted-k21-mac: the K = 21 stage logs of planted_k21.py (notes/PLANTED_SELECTION.md section 13)

Machine: the Mac (coordinator session), 2026-10-31. `dry/`: the dry run of section 13.0 item 0 on a synthetic sigma_21
(planted_k21_dry.py, the C20-BP [6/14] sum's own, section 12.7's first ring-free type-passing sum; its scan files and
records are not kept, the script regenerates them), started 09:5x UTC after the procedure (section 13.0, code repository
32f958d) and the scripts (49a1041) were committed. `generate.log` is the generator's output, `converge.log` and
`converge_mutate_<err|low|pilot|ratiolaw|amend>.log` the first stage and its five mutations (each firing), `stages.log`
the start and exit of each later stage. `real/`: the stages on the real sigma_21, run 2026-11-02 05:37-06:43 UTC on the four K 43 files (T94-mac's pilots,
a769589 and f25c18c; win2's nodes, 8676d14; code repository 805371f): converge and its five mutations (each firing),
then plants, real, ring, calib, recomplete, project, combine and table, each exiting 0 (`stages.log` has every start
and exit). The records and checks they wrote are in the code repository (planted_results_k21.jsonl,
planted_checks_k21.json); the write-up is section 13.2-13.10.

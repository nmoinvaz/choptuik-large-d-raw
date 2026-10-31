# planted-k19-mac: the K = 19 stage logs of planted_k19.py (notes/PLANTED_SELECTION.md section 11)

Machine: the Mac (coordinator session), 2026-10-28. `dry/`: the dry run of section 11.0 item 0 on a synthetic sigma_19
(planted_k19_dry.py, the C18-BP [7/11] sum's own; its scan files and records are not kept, the script regenerates them),
started 16:29 UTC beside T88, after the procedure was committed (code repository d6952ec, 16:26 UTC). The real sigma_19
stages (T88's scans) follow in the folder root once T88 posts.

Dry run 16:26-16:42 UTC: eight stages, 72 checks passing. `dry/combine_before_fix.log` is the combine stage's first run,
reading the twelve-sum calibration family where section 11.0 item 7 asks for the sixteen-sum one; `dry/combine.log` is
the rerun after the fix (code repository, the commit after d6952ec). The two ranges coincide on the synthetic data.

`real/`: the `converge` stage run as written (section 11.0 item 1) on the real sigma_19 scans, 2026-10-28 23:16 UTC, after
the three T88 nodes landed: items 1(a), (b), (d) pass at every node, item 1(c) fails (pilot (b) 3.39e-27 from (a) at
sigma_19 against (a)'s err19 2.79e-27); `converge_mutate_<err|low|pilot|ratiolaw>.log` are the four mutations, each
firing. The later stages wait for T91 (the J-or-bits attribution) and the dated amendment of item 1.

`real/converge_amend.log`: the `converge` stage under the amendment of item 1 (`--amend scan41J1250`, section 11.0's
amendment of 2026-10-29), run 2026-10-31 04:23 UTC once T89's node files had landed (raw T89-mac d9d0c01): (a') fails at
wf 0.99 (plateau 2.07e-26 + pilot difference 2.02e-26 = 1.59e-10 of |sigma_19|, margin 0.63) and passes at 1.00 and 1.01;
(b) and (d) pass. The work stopped there and the fallback named in that amendment was taken (the second amendment,
2026-10-31 04:32 UTC, code repository fcfeb4a).

`nodes/`: the stages under the second amendment (`--nodes scan41J1250`: the K 41 / J 1250 / 1280-bit files are the node
data, err19 their recomputed plateau error plus the J 1500 pilot difference at wf 1.00), started 2026-10-31 04:38 UTC;
`stages.log` has the start and exit of each stage. `converge.log` passes (margins 179-223, sigma_0..19 bitwise T88's
pilot (b) at wf 1.00, the sigma_0..18 differences from the 960-bit values recorded); `converge_mutate_<err|low|pilot|
ratiolaw>.log` are the four mutations, each firing. `plants.log` passes (51 plants). `real.log`: item 3's reproduction
check fires (the K = 17, 18 estimates of the 1280-bit node data differ from the 960-bit record "N0 scan37J1000" by up to
3.3e-8, in Pade crossings); the stages stopped there. `noise_test.py`, `noise_test.log`, `noise_test.json`: the cause
(the 960-bit data with Gaussian noise of their own plateau errors move those estimates by 1e-7 to 1e-6; every observed
difference is at most 0.61 of its rms); the third amendment (05:01 UTC, code repository d1fbfab) reads item 3 within
3 rms of that reference, `real_mutate_real.log` is its mutation (fires), and `real.log` is the rerun (05:04 UTC, passes).
`ring.log` first fired the K = 17, 18 completions' reproduction check against the 1280-bit record (fourth amendment,
05:09 UTC, ff66864: the reference is the 960-bit record they carry); the rerun at 05:10 UTC and `calib.log`,
`recomplete.log`, `project.log`, `combine.log` (05:10-05:12 UTC) pass every check. Sections 11.1-11.9 of the notes.

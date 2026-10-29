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

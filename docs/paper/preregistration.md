# What was declared in advance, and when

Compiled 2026-11-23 from git and the GitHub API (pull requests, PR timelines, the repository event log),
not from notes or memory. The paper calls these "declared in advance in the public repository, with commit
timestamps". None is a registry entry.

## How to read the times

All times are UTC. There are three kinds, and they prove different things:

- **Commit time** is written by the author's machine. It can be set to anything, so on its own it proves
  nothing about order.
- **Ancestry** is cryptographic. If a result file records the commit it ran at, and that commit descends from
  the declaration commit, the run's code contained the declaration. A commit cannot be made before its parent
  exists. This still trusts the result file to record its commit truthfully.
- **GitHub time** is the server's: when a PR was opened or merged, or a push arrived. This is the only kind a
  reader can check independently. It shows when the declaration became public, not when a run happened.

"Order provable" below means a GitHub time shows the declaration was public before the run's code or result
existed anywhere public, and ancestry ties the run to that declaration.

Commit hashes are lumenCell_V2's (`github.com/shreyandhawa/lumenCell_V2`) for rows 1-8; result files name those
hashes. This repository's history before 2026-11-23 was imported from lumenCell_V2 with rewritten hashes (`38043c7`);
the matching commit here is given in brackets. Rows 9-10 are in this repository. Ancestry was checked with
`git merge-base --is-ancestor` on a bare clone of lumenCell_V2 (read only).

## The table

| # | Declaration | Declaration commit, PR | Declared (commit time) | Public on GitHub (server) | First run that scored data against it | Run commit and time | Result public (server) | Order provable? |
|---|---|---|---|---|---|---|---|---|
| 1 | Real-data gates: pancreas, bone marrow, gastrulation (`[real.*.gates]`) | `0621edc` [`7ab1d7d`], no PR (pushed to main) | 2026-11-10 15:55:11 | **no record**: pushed to main without a PR, before the start of GitHub's event log (which keeps 300 events; it begins 2026-11-12 13:57) | `real-2026-11-10.json` | at `abe3f73` (descends from `0621edc`), commit 16:04:25; recorded in `40adb93`, 16:07:46 | no record (same push window) | **No.** Ancestry only; times are commit times, 9 minutes apart. Supplement only. |
| 2 | Clonal agreement definitions, nulls N1-N3, gates, runtime constants, calibration seeds 100-299 | `1664b27`, PR #7 (merged as `6ff4676`) [`9ef9337`] | 2026-11-12 17:01:03 | PR opened 2026-11-12 17:01:07, merged 17:48:48 | Synthetic clone scoring, PR #12 | merged `857d03d`, 2026-11-13 16:40:25 (branch first pushed 16:22:22) | PR #12 opened 2026-11-13 15:53:48 | **Yes.** Public about 23 hours before the scoring PR. |
| 3 | Clonal calibration: how NaN p-values count, before the 200-seed run | `cb5c9c3`, PR #14 [`15cc4eb`] | 2026-11-13 17:20:44 | **only with the result**: PR #14's branch was first created 18:08:33, with the result in it | `clonal-calibration-2026-11-13.json` | file says run at `cb5c9c3` itself, **with the calibration code uncommitted in the working tree** (the file's own `provenance` note; the code was first committed in `52f739d`, 18:08:31) | PR #14 opened 18:08:34 | **No.** Commit time only. The run's code was not committed when it ran. A reviewer later re-ran seeds 100-139 on `52f739d` and matched the p-values exactly (same note). Supplement only. |
| 4 | Verdict rule (C1-C5, levels), threshold calibration rule, four negative controls, verification seeds 3-5, pass bar `max_controls_supported = 0`, `on_failure = "provisional"` | `59d8213`, PR #26 (merged as `c8a50d9`) [`fdc200a`] | 2026-11-17 09:53:29 | push 09:54:16; PR opened 09:53:32, merged 10:18:55 | (a) `verdict-calibration-2026-11-17.json`; (b) `verdict-verification-2026-11-17.json` (the 28 of 31) | (a) at `0a584d5` (descends), file says generated 11:43:59; (b) at `37197c8` (descends), generated 12:19:23 | (a) PR #32 opened 11:51:02; (b) PR #33 opened 12:25:33 | **Yes.** Public about 2.5 hours before the verification ran. The count of 31 was not declared: it is 36 control runs minus 5 that failed. |
| 5 | Amended pseudotime shuffle (N2a) and its calibration on seeds 300-499 | `b0e235a`, PR #30 [`aa799f4`] | 2026-11-17 10:13:03 | **only with the result**: PR #30's branch was first created 11:08:57, after the result commit | `clonal-calibration-n2-amended-2026-11-17.json` | at `2b15c77` (child of `b0e235a`), commit 10:20:34; recorded in `7adf711`, 11:03:39 | PR #30 opened 11:08:59 | **No.** Ancestry shows the run's code held the declaration; that it was written before the result was seen rests on commit times. Supplement only. |
| 6 | Owner ruling H-1: under the cap, a failed clone check is shown as "weak", and only "supported" is capped | `169a3ff`, PR #38 (merged as `53d0dc1`) [`86d7671`] | 2026-11-19 19:30:18 | PR opened 19:30:21, merged 19:57:13 | applied to the Sheih runs (row 7) | — | — | **Made after a result.** It came two days after the verification failure (row 4) and changes how verdicts are shown, not any rule, threshold or null. Disclose it as a post-result change. |
| 7 | Sheih 2020 case study: clone definition, patient namespace, time-point strata (N3), root = infusion product, per-patient runs, m = 2 and 3, B = 1000 | `a0b4255` (final `5634406`), PR #51 (merged as `5ef3151`) [`4d1fe06`] | 2026-11-20 07:46:46 | PR opened 07:46:54; push to main 08:15:39 | `benchmarks/case_studies/results/sheih2020-2026-11-20.json` | at `5b4f83f` (descends from `5ef3151`), commit 13:06:26; recorded in `ebeba6d`, 13:30:40 | PR #57 opened 13:30:53 | **Yes**, with one disclosure: before the declaration, PR #45 (merged 2026-11-19 23:04:07) opened the TCR tables and the matrix header to check that barcodes join. Its note records a freeze rule: only headers, barcodes and counts were printed, and no clone, CDR3 or gene value. The dataset was built after the declaration (PR #52, merged 09:03:17). |
| 8 | Daniel 2022: subset, namespace, clone definition, truth, gates, clonal "not assessable" | `17fac72`, PR #54 (merged as `fb06f05`) [`4c93057`] | 2026-11-20 10:09:37 | PR opened 10:09:41, merged 10:38:21 | `real-2026-11-20.json` (Daniel rows) | at `a7d69c4` (descends from `fb06f05`), main push 12:00:38 | PR #56 opened 13:14:49 | **Yes for the run.** But the builder that calls clones (PR #53) merged at 09:29:01, 40 minutes before the declaration. That no clone was counted before the declaration rests on the declaration note's own statement. Not in the paper (declined). |
| 9 | Verdict diagnosis (Q1): four explanations, which count to report (Check R), decision rules | `4eec6f8` (rebased; first authored 15:31:44), PR #4 (merged as `9d63351`) | 2026-11-23 15:31:44 | PR opened 15:31:53; branch force-pushed 16:57:10; merged 17:01:10 | `diagnosis-verdict-2026-11-23.json` | **no run commit or time in the file**; results commit `20c5646`, 17:22:07 | PR #7 opened 17:22:11 | **Public before the result, yes; run order, not provable.** The declaration file is identical from `4eec6f8` to the merge, but the version first pushed at 15:31 was replaced by the force-push and cannot be compared. Supporting only, local: the run's log files on the author's machine were created from 17:01:41 to 17:13:29, after the merge. |
| 10 | Clonal-confound diagnosis (Q2): synthetic check D0-D3, clone bootstrap, Daniel reasons | `02abb12` (rebased; first authored 15:35:55), PR #5 (merged as `3f3bb99`) | 2026-11-23 15:35:55 | PR opened 15:35:58; force-pushed 16:58:22; merged 17:01:16 | `diagnosis-clonal-2026-11-23.json` | **no run commit or time in the file**; results commit `092290f`, 17:28:27 | PR #8 opened 17:28:30 | **Same as row 9.** Local log files were created from 17:01:50 (synthetic) and 17:13:29 (Sheih). |

## Flags, in plain words

1. **Rows 1, 3 and 5 cannot be shown to precede their runs** by anything a reader can check. The declaration
   reached GitHub with the result, or before GitHub's event log begins. None of the three is in the main text:
   the real-data gates and both clone-score calibrations are supplement material.
2. **Row 3 ran on uncommitted code.** The result file says so itself, and a later partial re-run on the committed
   code matched.
3. **Row 6 is a change made after a result was seen.** It changes how a verdict is shown, not what is computed.
   The paper discloses it.
4. **Rows 9 and 10 (the diagnoses behind the paper's two findings) record no run time.** GitHub shows the
   declarations were merged 21 and 27 minutes before the results were pushed. The only evidence that the runs
   started after the merge is local file times, which a reader cannot check. Future result files should record
   their commit and start time.
5. **Row 7 touched the data before the declaration**, under a recorded freeze rule (headers, barcodes and counts
   only).

## The run behind each paper number

| Paper number | Result file | Row |
|---|---|---|
| 27 of 30 controls supported (lumencell 0.5.0) | `diagnosis-verdict-2026-11-23.json`, `reproduce_on_0_5_0` | 9 (applies row 4's rule) |
| 28 of 31 (record), 31 of 34 at `37197c8` | `verdict-verification-2026-11-17.json`; `diagnosis-verdict-…`, `reproduce_at_37197c8` | 4, 9 |
| 2 of 31 with all four criteria | `diagnosis-verdict-…`, `criteria` | 9 |
| Sheih per-run scores, ratios, intervals, k-means lift | `diagnosis-clonal-2026-11-23.json`, `sheih_bootstrap` | 10 (applies row 7's plan) |
| Synthetic time-only check | `diagnosis-clonal-…`, `synthetic` | 10 |

## Sources

- PRs and merge times: `gh api repos/shreyandhawa/lumenCell_V2/pulls?state=all` and the same for
  `clonal-trajectory-research`; per-PR commits: `.../pulls/<n>/commits`; force-pushes: `.../issues/<n>/timeline`.
- Push and branch-creation times: `gh api repos/shreyandhawa/lumenCell_V2/events` (read 2026-11-23; GitHub keeps
  at most 300 events over 90 days, so this record will disappear; the times above are copied from it).
- Run commits and times: each result file's `commit` and `generated` fields.
- Local log times (rows 9-10): file birth times in the author's scratch directory, read 2026-11-23. Not checkable
  by a reader; given as supporting detail only.
